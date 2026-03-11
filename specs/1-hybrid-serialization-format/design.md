# F1.3 — Hybrid Serialization Format: Design

## Technical Design

### Module Location
`source/packages/automojo/timetravel/pod/traceserializer.py`

### Wire Format

Each serialized event consists of three contiguous sections:

```
┌──────────────────────────────────────┐
│  Struct Envelope (29 bytes fixed)    │
├──────────────────────────────────────┤
│  Filename (variable, UTF-8 bytes)    │
├──────────────────────────────────────┤
│  Pickle Payload (variable bytes)     │
└──────────────────────────────────────┘
```

### Struct Envelope Layout

```python
import struct

# Format: ! = network byte order (big-endian)
#   B  = event_type       (1 byte,  unsigned char)
#   Q  = timestamp_ns     (8 bytes, unsigned long long)
#   Q  = thread_id        (8 bytes, unsigned long long)
#   I  = filename_length  (4 bytes, unsigned int)
#   I  = lineno           (4 bytes, unsigned int)
#   I  = payload_length   (4 bytes, unsigned int)
ENVELOPE_FORMAT = "!BQQIII"
ENVELOPE_SIZE = struct.calcsize(ENVELOPE_FORMAT)  # 29 bytes
```

### Serializer

```python
import pickle

class TraceSerializer:
    """Serializes TraceEvent objects into the hybrid struct+pickle binary format."""

    def __init__(self):
        self._pack = struct.Struct(ENVELOPE_FORMAT).pack

    def serialize(self, event: TraceEvent) -> bytes:
        """Serialize a single TraceEvent to bytes."""
        payload_data = self._extract_payload(event)
        payload_bytes = pickle.dumps(payload_data, protocol=5) if payload_data else b""

        filename = self._extract_filename(event)
        filename_bytes = filename.encode("utf-8") if filename else b""
        lineno = self._extract_lineno(event)

        envelope = self._pack(
            event.event_type,
            event.timestamp_ns,
            event.thread_id,
            len(filename_bytes),
            lineno,
            len(payload_bytes),
        )

        rtnval = envelope + filename_bytes + payload_bytes
        return rtnval

    def _extract_filename(self, event: TraceEvent) -> str:
        """Extract filename from event, or empty string for events without one."""
        rtnval = getattr(event, "filename", "")
        return rtnval

    def _extract_lineno(self, event: TraceEvent) -> int:
        """Extract line number from event, or 0 for events without one."""
        rtnval = getattr(event, "lineno", 0)
        return rtnval

    def _extract_payload(self, event: TraceEvent) -> dict | None:
        """Extract the variable-length payload data for pickling."""
        ...
        # Returns a dict specific to each event type, e.g.:
        # CallEvent -> {"function_name": ..., "args": ..., "kwargs": ...}
        # ReturnEvent -> {"function_name": ..., "return_value": ...}
        # LineEvent -> None (no payload needed)
        # VariableSnapshotEvent -> {"local_variables": ...}
        # PortalEnterEvent -> {"portal_name": ...}
        # GatewayStartEvent -> {"wall_clock_time": ...}
        # etc.
```

### Deserializer

```python
class TraceDeserializer:
    """Deserializes the hybrid struct+pickle binary format back into TraceEvent objects."""

    def __init__(self):
        self._unpack = struct.Struct(ENVELOPE_FORMAT).unpack

    def deserialize(self, data: bytes, offset: int = 0) -> tuple[TraceEvent, int]:
        """Deserialize one event starting at offset. Returns (event, next_offset)."""
        header = self._unpack(data[offset:offset + ENVELOPE_SIZE])
        event_type, timestamp_ns, thread_id, filename_len, lineno, payload_len = header
        offset += ENVELOPE_SIZE

        filename = data[offset:offset + filename_len].decode("utf-8")
        offset += filename_len

        payload_data = None
        if payload_len > 0:
            payload_data = pickle.loads(data[offset:offset + payload_len])
        offset += payload_len

        event = self._reconstruct_event(
            event_type, timestamp_ns, thread_id, filename, lineno, payload_data
        )
        rtnval = (event, offset)
        return rtnval

    def read_header(self, data: bytes, offset: int = 0) -> tuple[tuple, int]:
        """Read only the envelope header, returning (header_tuple, offset_after_header)."""
        header = self._unpack(data[offset:offset + ENVELOPE_SIZE])
        rtnval = (header, offset + ENVELOPE_SIZE)
        return rtnval

    def skip_event(self, data: bytes, offset: int = 0) -> int:
        """Skip past one event, returning the offset of the next event."""
        header = self._unpack(data[offset:offset + ENVELOPE_SIZE])
        _, _, _, filename_len, _, payload_len = header
        rtnval = offset + ENVELOPE_SIZE + filename_len + payload_len
        return rtnval
```

### Payload Mapping by Event Type

| Event Type | Payload Dict Keys |
|---|---|
| `CALL` | `function_name`, `args`, `kwargs` |
| `RETURN` | `function_name`, `return_value` |
| `LINE` | *(no payload — length 0)* |
| `VARIABLE_SNAPSHOT` | `local_variables` |
| `EXCEPTION` | `function_name`, `exception_type`, `exception_value`, `traceback_str` |
| `PORTAL_ENTER` | `portal_name` |
| `PORTAL_EXIT` | `portal_name` |
| `GATEWAY_START` | `wall_clock_time` |
| `GATEWAY_STOP` | `wall_clock_time` |

### Design Rationale

- `struct.Struct` is pre-compiled at `__init__` time for maximum packing/unpacking speed.
- Network byte order (`!`) ensures portable binary files across architectures.
- The filename is stored outside of pickle because it is a simple UTF-8 string that benefits
  from being in the scannable envelope area.
- `pickle` protocol 5 is used because it supports out-of-band buffers and is the most
  efficient protocol available in Python 3.10+.
- `LineEvent` has an empty pickle payload to minimize the per-line overhead when line
  tracing is enabled — the filename and lineno are already in the envelope.
