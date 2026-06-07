# F1.2 — Trace Recorder Interface: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/tracerecorder.py`

### Abstract Base Class

```python
from abc import ABC, abstractmethod
from ccai.timetravel.pod.traceevents import TraceEvent


class TraceRecorder(ABC):
    """Abstract base class defining the contract for all trace recorders."""

    @abstractmethod
    def record(self, event: TraceEvent) -> None:
        """Accept a single trace event for recording.

        This method is called from the trace hook on the hot path and should
        be as fast as possible.
        """
        ...

    @abstractmethod
    def flush(self) -> None:
        """Ensure all buffered data is written to the underlying stream."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Finalize the recorder and release held resources."""
        ...
```

### Design Rationale

- `ABC` with `@abstractmethod` is used to enforce the interface contract at instantiation time.
- The interface is intentionally minimal: `record`, `flush`, `close`. Additional lifecycle
  methods would add complexity without clear benefit at this layer.
- `record()` takes a `TraceEvent` (not serialized bytes) so that recorders can choose
  their own serialization strategy or delegate to the serializer.
