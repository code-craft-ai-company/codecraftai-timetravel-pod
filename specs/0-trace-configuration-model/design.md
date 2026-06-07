# F0.2 — Trace Configuration Model: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/traceconfiguration.py`

### Class Design

```python
class TraceConfiguration:
    """Immutable configuration controlling trace granularity and behavior."""

    __slots__ = ("_trace_calls", "_trace_lines", "_trace_variables", "_record_inner_portals")

    def __init__(
        self,
        trace_calls: bool = True,
        trace_lines: bool = False,
        trace_variables: bool = False,
        record_inner_portals: bool = False,
    ):
        self._trace_calls = trace_calls
        self._trace_lines = trace_lines
        self._trace_variables = trace_variables
        self._record_inner_portals = record_inner_portals

    @property
    def trace_calls(self) -> bool:
        return self._trace_calls

    @property
    def trace_lines(self) -> bool:
        return self._trace_lines

    @property
    def trace_variables(self) -> bool:
        return self._trace_variables

    @property
    def record_inner_portals(self) -> bool:
        return self._record_inner_portals

    def as_dict(self) -> dict:
        rtnval = {
            "trace_calls": self._trace_calls,
            "trace_lines": self._trace_lines,
            "trace_variables": self._trace_variables,
            "record_inner_portals": self._record_inner_portals,
        }
        return rtnval

    @classmethod
    def from_dict(cls, data: dict) -> "TraceConfiguration":
        rtnval = cls(
            trace_calls=data.get("trace_calls", True),
            trace_lines=data.get("trace_lines", False),
            trace_variables=data.get("trace_variables", False),
            record_inner_portals=data.get("record_inner_portals", False),
        )
        return rtnval
```

### Immutability

Immutability is enforced using `__slots__` with private backing fields exposed through
read-only `@property` accessors.  Attempting to set an attribute directly will raise
an `AttributeError` because there is no setter.  To change configuration, a new
`TraceConfiguration` instance is created — this is the pattern used by the remote
control interface (Layer 5) when updating configuration at runtime.

### Default Configuration

A module-level constant provides the default configuration:

```python
DEFAULT_TRACE_CONFIGURATION = TraceConfiguration()
```

### Design Rationale

- `__slots__` is used for memory efficiency and to prevent accidental attribute
  additions on a hot-path object.
- Read-only properties enforce immutability without the overhead of `dataclasses`
  with `frozen=True` (which adds overhead to `__init__`).
- The `as_dict` / `from_dict` pattern follows the project's naming conventions
  for conversion and encoding methods.
