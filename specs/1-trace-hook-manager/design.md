# F1.1 — Trace Hook Manager: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/tracehookmanager.py`

### Class Design

```python
import sys
import threading
from ccai.timetravel.pod.traceevents import (
    CallEvent, ReturnEvent, LineEvent, VariableSnapshotEvent, ExceptionEvent
)
from ccai.timetravel.pod.traceclock import get_trace_clock
from ccai.timetravel.pod.traceconfiguration import TraceConfiguration


class TraceHookManager:
    """Manages sys.settrace installation and event dispatch for a single thread."""

    __slots__ = (
        "_record_callback", "_trace_calls", "_trace_lines",
        "_trace_variables", "_clock", "_thread_id",
    )

    def __init__(self, configuration: TraceConfiguration, record_callback):
        self._record_callback = record_callback
        self._trace_calls = configuration.trace_calls
        self._trace_lines = configuration.trace_lines
        self._trace_variables = configuration.trace_variables
        self._clock = get_trace_clock()
        self._thread_id = threading.get_ident()

    def install(self) -> None:
        """Install the trace function on the current thread."""
        sys.settrace(self._trace_function)

    def uninstall(self) -> None:
        """Remove the trace function from the current thread."""
        sys.settrace(None)

    def _trace_function(self, frame, event, arg):
        """The trace function installed via sys.settrace."""
        ...
```

### Trace Function Implementation

The `_trace_function` is the hot path. It extracts configuration booleans into
local instance attributes in `__init__` to avoid dictionary lookups on every call.

```python
def _trace_function(self, frame, event, arg):
    timestamp_ns = self._clock.timestamp()
    record = self._record_callback

    if event == "call":
        if self._trace_calls:
            record(CallEvent(
                timestamp_ns=timestamp_ns,
                thread_id=self._thread_id,
                filename=frame.f_code.co_filename,
                lineno=frame.f_lineno,
                function_name=frame.f_code.co_name,
            ))
        return self._trace_function

    elif event == "return":
        if self._trace_calls:
            record(ReturnEvent(
                timestamp_ns=timestamp_ns,
                thread_id=self._thread_id,
                filename=frame.f_code.co_filename,
                lineno=frame.f_lineno,
                function_name=frame.f_code.co_name,
                return_value=arg,
            ))

    elif event == "line":
        if self._trace_lines:
            record(LineEvent(
                timestamp_ns=timestamp_ns,
                thread_id=self._thread_id,
                filename=frame.f_code.co_filename,
                lineno=frame.f_lineno,
            ))
        if self._trace_variables:
            record(VariableSnapshotEvent(
                timestamp_ns=timestamp_ns,
                thread_id=self._thread_id,
                filename=frame.f_code.co_filename,
                lineno=frame.f_lineno,
                local_variables=dict(frame.f_locals),
            ))

    elif event == "exception":
        exc_type, exc_value, exc_tb = arg
        record(ExceptionEvent(
            timestamp_ns=timestamp_ns,
            thread_id=self._thread_id,
            filename=frame.f_code.co_filename,
            lineno=frame.f_lineno,
            function_name=frame.f_code.co_name,
            exception_type=exc_type.__name__ if exc_type else "",
            exception_value=str(exc_value) if exc_value else "",
            traceback_str="",  # Full traceback formatting deferred to avoid overhead
        ))

    return self._trace_function
```

### Performance Considerations

- Configuration booleans are cached as instance attributes (not re-read from config object).
- `frame.f_code.co_filename` and `frame.f_code.co_name` are direct C-level attribute
  accesses — no method call overhead.
- `dict(frame.f_locals)` creates a shallow copy of locals, which is necessary because
  `frame.f_locals` is a live proxy.
- The trace function always returns itself so that it remains installed for sub-calls.
- Traceback string formatting is deferred (stored as empty string) to avoid expensive
  `traceback.format_tb()` calls in the hot path.  The exception type and value are
  sufficient for most debugging use cases.

### Design Rationale

- `__slots__` is used to avoid `__dict__` overhead since the manager is created per portal
  activation.
- The `record_callback` is a callable (typically `TraceRecorder.record`) passed at
  construction to decouple the hook manager from specific recorder implementations.
- Thread ID is captured once at construction rather than on every event because the
  hook manager is thread-specific.
