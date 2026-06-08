# F1.4 — Buffered Writer: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/bufferedwriter.py`

### Class Design

```python
DEFAULT_BUFFER_SIZE = 65536  # 64 KB


class BufferedTraceWriter:
    """Batches serialized event bytes and flushes to a stream backend in chunks."""

    __slots__ = ("_stream", "_buffer", "_max_size")

    def __init__(self, stream, max_buffer_size: int = DEFAULT_BUFFER_SIZE):
        self._stream = stream
        self._buffer = bytearray()
        self._max_size = max_buffer_size

    def write(self, data: bytes) -> None:
        """Append serialized bytes to the buffer, auto-flushing if full."""
        self._buffer.extend(data)
        if len(self._buffer) >= self._max_size:
            self.flush()

    def flush(self) -> None:
        """Write all buffered data to the stream backend."""
        if self._buffer:
            self._stream.write(bytes(self._buffer))
            self._buffer.clear()

    def close(self) -> None:
        """Flush remaining data and close the stream backend."""
        self.flush()
        self._stream.close()
```

### Stream Backend Interface (Duck Typing)

The `stream` argument must support:
- `write(data: bytes) -> None`
- `close() -> None`

This is satisfied by `io.FileIO`, `socket.makefile()`, and the custom socket stream
backends defined in Layer 2.

### Design Rationale

- `bytearray` is used for the buffer because it supports efficient in-place extension
  via `.extend()` and `.clear()` without allocating new objects.
- The buffer is flushed as a single `write()` call to the backend, which is critical
  for file I/O (single `write` syscall) and network I/O (single `send`).
- `__slots__` is used since instances are created per-portal-activation and should
  be lightweight.
