# F3.1 — TimeTravelGateway: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/gateway.py`

### Class Design

```python
import time
import threading
from ccai.timetravel.pod.traceclock import get_trace_clock
from ccai.timetravel.pod.tracingstate import set_gateway_active
from ccai.timetravel.pod.traceevents import GatewayStartEvent, GatewayStopEvent
from ccai.timetravel.pod.traceconfiguration import TraceConfiguration, DEFAULT_TRACE_CONFIGURATION


class TimeTravelGateway:
    """Main application gateway that marks the tracing timespan."""

    def __init__(self, configuration: TraceConfiguration = None,
                 backend_uri: str | None = None):
        self._configuration = configuration or DEFAULT_TRACE_CONFIGURATION
        self._backend_uri = backend_uri
        self._clock = get_trace_clock()
        self._active_recorders: list = []

    def __enter__(self):
        # Start the clock
        self._clock.start()

        # Mark gateway as active
        set_gateway_active(True)

        # Emit gateway start event
        start_event = GatewayStartEvent(
            timestamp_ns=0,  # Origin
            thread_id=threading.get_ident(),
            wall_clock_time=time.time(),
        )
        self._broadcast_event(start_event)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            # Emit gateway stop event
            stop_event = GatewayStopEvent(
                timestamp_ns=self._clock.timestamp(),
                thread_id=threading.get_ident(),
                wall_clock_time=time.time(),
            )
            self._broadcast_event(stop_event)

            # Flush and close all active recorders
            for recorder in self._active_recorders:
                recorder.flush()
                recorder.close()
            self._active_recorders.clear()
        finally:
            # Always stop the clock and clear the gateway flag
            self._clock.stop()
            set_gateway_active(False)

        # Do not suppress exceptions
        return False

    @property
    def configuration(self) -> TraceConfiguration:
        rtnval = self._configuration
        return rtnval

    def register_recorder(self, recorder) -> None:
        """Register an active recorder for cleanup on gateway exit."""
        self._active_recorders.append(recorder)

    def _broadcast_event(self, event) -> None:
        """Send an event to all active recorders."""
        for recorder in self._active_recorders:
            recorder.record(event)
```

### Singleton Access

The gateway instance needs to be accessible by portals (so they can check if the
gateway is active and access the configuration). A module-level reference is set:

```python
_active_gateway: TimeTravelGateway | None = None

def get_active_gateway() -> TimeTravelGateway | None:
    return _active_gateway

def set_active_gateway(gateway: TimeTravelGateway | None) -> None:
    global _active_gateway
    _active_gateway = gateway
```

The `__enter__` and `__exit__` methods call `set_active_gateway(self)` and
`set_active_gateway(None)` respectively.

### Design Rationale

- The `finally` block ensures clock stop and gateway flag reset even on exceptions.
- `__exit__` returns `False` to propagate exceptions — the gateway never suppresses them.
- Recorder registration is explicit via `register_recorder()` rather than automatic,
  giving portals control over when and which recorders are registered.
- The `_active_gateway` module-level reference avoids passing the gateway object
  through every portal constructor.
