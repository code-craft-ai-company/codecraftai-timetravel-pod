# F6.2 — Timeline Reconstruction: Design

## Technical Design

### Module Location
`source/packages/automojo/timetravel/pod/timeline.py`

### Class Design

```python
from automojo.timetravel.pod.traceevents import TraceEvent


class TimelineBuilder:
    """Builds a sorted timeline from one or more event sources."""

    def __init__(self):
        self._events: list[TraceEvent] = []

    def add_events(self, events) -> None:
        """Add an iterable of TraceEvent objects to the builder."""
        self._events.extend(events)

    def build(self, thread_id: int | None = None,
              event_types: list[int] | None = None,
              start_ns: int | None = None,
              end_ns: int | None = None) -> list[TraceEvent]:
        """Build the sorted, filtered timeline."""
        # Sort by timestamp (stable sort preserves source ordering for equal timestamps)
        self._events.sort(key=lambda e: e.timestamp_ns)

        filtered = self._events
        if thread_id is not None:
            filtered = [e for e in filtered if e.thread_id == thread_id]
        if event_types is not None:
            type_set = set(event_types)
            filtered = [e for e in filtered if e.event_type in type_set]
        if start_ns is not None:
            filtered = [e for e in filtered if e.timestamp_ns >= start_ns]
        if end_ns is not None:
            filtered = [e for e in filtered if e.timestamp_ns <= end_ns]

        rtnval = filtered
        return rtnval
```

### Design Rationale

- Python's built-in `list.sort` is stable, preserving insertion order for events with
  equal timestamps.
- Filtering is done after sorting for simplicity. For very large datasets, filtering
  before sorting would be more efficient, but correctness is prioritized here.
- The builder pattern allows incremental addition of events from multiple readers.
