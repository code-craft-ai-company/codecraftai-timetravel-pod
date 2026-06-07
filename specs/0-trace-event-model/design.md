# F0.4 — Trace Event Model: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/traceevents.py`

### Event Type Constants

```python
class EventType:
    """Integer tags for each trace event type, used in the struct serialization envelope."""

    CALL = 1
    RETURN = 2
    LINE = 3
    VARIABLE_SNAPSHOT = 4
    PORTAL_ENTER = 5
    PORTAL_EXIT = 6
    GATEWAY_START = 7
    GATEWAY_STOP = 8
    EXCEPTION = 9
```

Using a plain class with integer class attributes rather than `enum.IntEnum` to avoid
import overhead on the tracing hot path.

### Base Event Class

```python
class TraceEvent:
    """Base class for all trace events."""

    __slots__ = ("event_type", "timestamp_ns", "thread_id")

    def __init__(self, event_type: int, timestamp_ns: int, thread_id: int):
        self.event_type = event_type
        self.timestamp_ns = timestamp_ns
        self.thread_id = thread_id
```

### Concrete Event Classes

Each concrete event class extends `TraceEvent` with `__slots__` for its additional fields:

```python
class CallEvent(TraceEvent):
    __slots__ = ("filename", "lineno", "function_name", "args", "kwargs")

    def __init__(self, timestamp_ns: int, thread_id: int,
                 filename: str, lineno: int, function_name: str,
                 args: tuple = (), kwargs: dict | None = None):
        super().__init__(EventType.CALL, timestamp_ns, thread_id)
        self.filename = filename
        self.lineno = lineno
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs


class ReturnEvent(TraceEvent):
    __slots__ = ("filename", "lineno", "function_name", "return_value")

    def __init__(self, timestamp_ns: int, thread_id: int,
                 filename: str, lineno: int, function_name: str,
                 return_value=None):
        super().__init__(EventType.RETURN, timestamp_ns, thread_id)
        self.filename = filename
        self.lineno = lineno
        self.function_name = function_name
        self.return_value = return_value


class LineEvent(TraceEvent):
    __slots__ = ("filename", "lineno")

    def __init__(self, timestamp_ns: int, thread_id: int,
                 filename: str, lineno: int):
        super().__init__(EventType.LINE, timestamp_ns, thread_id)
        self.filename = filename
        self.lineno = lineno


class VariableSnapshotEvent(TraceEvent):
    __slots__ = ("filename", "lineno", "local_variables")

    def __init__(self, timestamp_ns: int, thread_id: int,
                 filename: str, lineno: int, local_variables: dict):
        super().__init__(EventType.VARIABLE_SNAPSHOT, timestamp_ns, thread_id)
        self.filename = filename
        self.lineno = lineno
        self.local_variables = local_variables


class ExceptionEvent(TraceEvent):
    __slots__ = ("filename", "lineno", "function_name", "exception_type", "exception_value", "traceback_str")

    def __init__(self, timestamp_ns: int, thread_id: int,
                 filename: str, lineno: int, function_name: str,
                 exception_type: str, exception_value: str, traceback_str: str):
        super().__init__(EventType.EXCEPTION, timestamp_ns, thread_id)
        self.filename = filename
        self.lineno = lineno
        self.function_name = function_name
        self.exception_type = exception_type
        self.exception_value = exception_value
        self.traceback_str = traceback_str


class PortalEnterEvent(TraceEvent):
    __slots__ = ("portal_name",)

    def __init__(self, timestamp_ns: int, thread_id: int, portal_name: str):
        super().__init__(EventType.PORTAL_ENTER, timestamp_ns, thread_id)
        self.portal_name = portal_name


class PortalExitEvent(TraceEvent):
    __slots__ = ("portal_name",)

    def __init__(self, timestamp_ns: int, thread_id: int, portal_name: str):
        super().__init__(EventType.PORTAL_EXIT, timestamp_ns, thread_id)
        self.portal_name = portal_name


class GatewayStartEvent(TraceEvent):
    __slots__ = ("wall_clock_time",)

    def __init__(self, timestamp_ns: int, thread_id: int, wall_clock_time: float):
        super().__init__(EventType.GATEWAY_START, timestamp_ns, thread_id)
        self.wall_clock_time = wall_clock_time


class GatewayStopEvent(TraceEvent):
    __slots__ = ("wall_clock_time",)

    def __init__(self, timestamp_ns: int, thread_id: int, wall_clock_time: float):
        super().__init__(EventType.GATEWAY_STOP, timestamp_ns, thread_id)
        self.wall_clock_time = wall_clock_time
```

### Design Rationale

- `__slots__` is used on all event classes for memory efficiency (trace sessions may produce
  millions of events) and attribute access speed.
- Plain classes with explicit `__init__` rather than `dataclasses` to avoid the decorator overhead
  and to keep full control over the initialization path.
- `ExceptionEvent` is included to capture exception propagation through traced code.
- `EventType` uses plain integer constants rather than `enum.IntEnum` because the event type tag
  is used in the hot path of the trace hook and struct packing — integer comparison is faster
  than enum comparison.
