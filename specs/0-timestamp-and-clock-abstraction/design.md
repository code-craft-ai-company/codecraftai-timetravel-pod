# F0.3 — Timestamp and Clock Abstraction: Design

## Technical Design

### Module Location
`source/packages/automojo/timetravel/pod/traceclock.py`

### Class Design

```python
import time

class TraceClock:
    """Monotonic high-resolution clock for trace event timestamps."""

    def __init__(self):
        self._origin_ns: int | None = None

    def start(self) -> None:
        """Record the origin timestamp. Called when the gateway is entered."""
        self._origin_ns = time.perf_counter_ns()

    def stop(self) -> None:
        """Clear the origin. Called when the gateway is exited."""
        self._origin_ns = None

    def timestamp(self) -> int:
        """Return nanosecond offset from origin.

        Raises RuntimeError if the clock has not been started.
        """
        if self._origin_ns is None:
            raise RuntimeError("TraceClock has not been started. Enter the TimeTravelGateway first.")
        rtnval = time.perf_counter_ns() - self._origin_ns
        return rtnval

    @property
    def is_running(self) -> bool:
        rtnval = self._origin_ns is not None
        return rtnval
```

### Singleton Access

A module-level instance and accessor function:

```python
_trace_clock = TraceClock()

def get_trace_clock() -> TraceClock:
    return _trace_clock
```

### Design Rationale

- `time.perf_counter_ns()` is used because it is monotonic (never goes backward),
  has the highest available resolution, and returns an integer (no float precision loss).
- Nanosecond integers are used throughout to avoid floating-point accumulation errors
  in long-running applications.
- The singleton pattern is used because there is exactly one timeline per process,
  anchored to the gateway start.
