# F0.1 — Thread-Local Tracing State: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/tracingstate.py`

### Data Structure

The thread-local tracing state is implemented using Python's `threading.local()` and wrapped
in a dataclass-style accessor for clarity.

```python
import threading

class TracingState:
    """Per-thread tracing state container."""

    def __init__(self):
        self.is_tracing: bool = False
        self.recorder = None          # Reference to the active TraceRecorder (or None)
        self.portal_depth: int = 0    # Nesting depth of portal contexts
        self.active_portal_name: str | None = None  # Name of the outermost active portal

    def reset(self):
        """Reset the tracing state to defaults."""
        self.is_tracing = False
        self.recorder = None
        self.portal_depth = 0
        self.active_portal_name = None
```

### Thread-Local Storage

A module-level `threading.local()` instance is created. A module-level function
`get_tracing_state()` accesses (and lazily initializes) a `TracingState` on the
thread-local object.

```python
_thread_local = threading.local()

def get_tracing_state() -> TracingState:
    """Return the TracingState for the current thread, creating it if needed."""
    state = getattr(_thread_local, "tracing_state", None)
    if state is None:
        state = TracingState()
        _thread_local.tracing_state = state
    return state
```

### Gateway Flag

A separate module-level flag (not thread-local) indicates whether the gateway
has been entered.  This is a simple boolean that is set/cleared by the
`TimeTravelGateway` context manager (Layer 3).  It is stored alongside the
tracing state module so all state queries go through one module.

```python
_gateway_active: bool = False

def is_gateway_active() -> bool:
    return _gateway_active

def set_gateway_active(active: bool) -> None:
    global _gateway_active
    _gateway_active = active
```

### Design Rationale

- `threading.local()` is used because it is the standard Python mechanism for
  thread-isolated state with zero overhead on the hot path (attribute access).
- The `TracingState` class is a plain class (not a dataclass) to avoid import
  overhead from `dataclasses` in the tracing hot path.
- The gateway flag is module-level (not thread-local) because the gateway is a
  process-wide concept — it is entered once on the main thread and all threads
  must respect it.
