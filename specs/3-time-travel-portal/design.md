# F3.2 — TimeTravelPortal: Design

## Technical Design

### Module Location
`source/packages/automojo/timetravel/pod/portal.py`

### Class Design

```python
import threading
from automojo.timetravel.pod.tracingstate import get_tracing_state, is_gateway_active
from automojo.timetravel.pod.portalregistry import get_portal_registry
from automojo.timetravel.pod.gateway import get_active_gateway
from automojo.timetravel.pod.tracehookmanager import TraceHookManager
from automojo.timetravel.pod.traceevents import PortalEnterEvent, PortalExitEvent
from automojo.timetravel.pod.traceclock import get_trace_clock


class TimeTravelPortal:
    """Named portal context manager for scoped time travel tracing."""

    __slots__ = ("_name", "_activated_tracing", "_hook_manager")

    def __init__(self, name: str):
        self._name = name
        self._activated_tracing = False
        self._hook_manager = None

    @property
    def name(self) -> str:
        rtnval = self._name
        return rtnval

    def __enter__(self):
        # Fast path: if gateway is not active, do nothing
        if not is_gateway_active():
            return self

        state = get_tracing_state()

        if state.is_tracing:
            # Already inside an active portal — this is a nested portal
            state.portal_depth += 1
            gateway = get_active_gateway()
            if gateway and gateway.configuration.record_inner_portals:
                clock = get_trace_clock()
                event = PortalEnterEvent(
                    timestamp_ns=clock.timestamp(),
                    thread_id=threading.get_ident(),
                    portal_name=self._name,
                )
                state.recorder.record(event)
            return self

        # Check if this portal is activated
        registry = get_portal_registry()
        if not registry.is_portal_active(self._name):
            return self

        # Activate tracing on this thread
        gateway = get_active_gateway()
        # Create recorder and hook manager (implementation details in integration)
        # For now, the recorder is obtained from the gateway/backend setup
        ...

        self._activated_tracing = True
        state.is_tracing = True
        state.portal_depth = 1
        state.active_portal_name = self._name

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._activated_tracing:
            # This portal did not activate tracing
            state = get_tracing_state()
            if state.is_tracing and state.portal_depth > 1:
                # Nested portal exit
                state.portal_depth -= 1
                gateway = get_active_gateway()
                if gateway and gateway.configuration.record_inner_portals:
                    clock = get_trace_clock()
                    event = PortalExitEvent(
                        timestamp_ns=clock.timestamp(),
                        thread_id=threading.get_ident(),
                        portal_name=self._name,
                    )
                    state.recorder.record(event)
            return False

        # This portal activated tracing — tear down
        try:
            if self._hook_manager is not None:
                self._hook_manager.uninstall()

            state = get_tracing_state()
            if state.recorder is not None:
                state.recorder.flush()
                state.recorder.close()

            state.reset()
        finally:
            self._activated_tracing = False
            self._hook_manager = None

        return False
```

### Control Flow Summary

```
__enter__:
  ├─ gateway not active → no-op
  ├─ already tracing (nested) → increment depth, optional annotation
  ├─ portal not activated → no-op
  └─ activate tracing → install hook, create recorder, set state

__exit__:
  ├─ did not activate → decrement depth if nested, optional annotation
  └─ activated → uninstall hook, flush/close recorder, reset state
```

### Design Rationale

- The `__slots__` and fast boolean checks ensure minimal overhead for inactive portals.
- `_activated_tracing` is an instance flag to know whether this specific portal instance
  was responsible for starting tracing — critical for correct cleanup in nested scenarios.
- The portal always returns `False` from `__exit__` to never suppress exceptions.
- Thread-local state access (`get_tracing_state()`) is the single source of truth for
  whether the current thread is tracing.
