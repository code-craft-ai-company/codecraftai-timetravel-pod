# F6.1 — Trace File Reader: Design

## Technical Design

### Module Location
`source/packages/automojo/timetravel/pod/reader.py`

### Class Design

```python
import io
from automojo.timetravel.pod.traceserializer import TraceDeserializer, ENVELOPE_SIZE
from automojo.timetravel.pod.traceevents import TraceEvent


class TraceFileReader:
    """Reads and deserializes trace files into TraceEvent objects."""

    def __init__(self, source):
        """Accept a file path (str), list of file paths, or BytesIO object."""
        self._deserializer = TraceDeserializer()
        self._sources = []
        self._current_handle = None

        if isinstance(source, str):
            self._sources = [source]
        elif isinstance(source, list):
            self._sources = source
        elif isinstance(source, io.BytesIO):
            self._sources = [source]
        else:
            raise TypeError(f"Unsupported source type: {type(source)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def read_events(self):
        """Yield all TraceEvent objects from the source(s)."""
        for source in self._sources:
            data = self._read_source(source)
            offset = 0
            while offset < len(data):
                event, offset = self._deserializer.deserialize(data, offset)
                yield event

    def scan_headers(self):
        """Yield envelope-only tuples without deserializing payloads."""
        for source in self._sources:
            data = self._read_source(source)
            offset = 0
            while offset < len(data):
                header, _ = self._deserializer.read_header(data, offset)
                yield header
                offset = self._deserializer.skip_event(data, offset)

    def _read_source(self, source) -> bytes:
        if isinstance(source, str):
            with open(source, "rb") as f:
                rtnval = f.read()
        elif isinstance(source, io.BytesIO):
            rtnval = source.getvalue()
        else:
            rtnval = b""
        return rtnval

    def close(self) -> None:
        pass  # File handles are opened/closed per read
```

### Design Rationale

- Sources are read fully into memory for simplicity. For very large trace files, a
  streaming reader could be added later as an optimization.
- The `scan_headers` method enables efficient filtering without paying the pickle
  deserialization cost.
- Context manager support (`__enter__`/`__exit__`) follows the project's convention.
