# F2.4 — Stream Backend Registry: Design

## Technical Design

### Module Location
`source/packages/automojo/timetravel/pod/backends/registry.py`

### Class Design

```python
from urllib.parse import urlparse


class StreamBackendRegistry:
    """Registry mapping URI schemes to stream backend factory functions."""

    def __init__(self):
        self._factories: dict[str, callable] = {}

    def register(self, scheme: str, factory) -> None:
        """Register a factory function for a URI scheme."""
        self._factories[scheme] = factory

    def create_backend(self, uri: str):
        """Parse a URI and create the corresponding stream backend."""
        parsed = urlparse(uri)
        scheme = parsed.scheme

        if scheme not in self._factories:
            raise ValueError(f"Unknown stream backend scheme: '{scheme}'. "
                             f"Known schemes: {list(self._factories.keys())}")

        factory = self._factories[scheme]
        rtnval = factory(parsed)
        return rtnval
```

### Built-in Factory Functions

```python
from automojo.timetravel.pod.backends.filebackend import FileStreamBackend
from automojo.timetravel.pod.backends.tcpbackend import TcpStreamBackend
from automojo.timetravel.pod.backends.unixbackend import UnixStreamBackend


def _create_file_backend(parsed) -> FileStreamBackend:
    file_path = parsed.path
    rtnval = FileStreamBackend(file_path=file_path)
    return rtnval


def _create_tcp_backend(parsed) -> TcpStreamBackend:
    host = parsed.hostname or "localhost"
    port = parsed.port or 9090
    rtnval = TcpStreamBackend(host=host, port=port)
    return rtnval


def _create_unix_backend(parsed) -> UnixStreamBackend:
    socket_path = parsed.path
    rtnval = UnixStreamBackend(socket_path=socket_path)
    return rtnval
```

### Default Registry

A module-level function creates and returns a pre-configured registry:

```python
def create_default_registry() -> StreamBackendRegistry:
    registry = StreamBackendRegistry()
    registry.register("file", _create_file_backend)
    registry.register("tcp", _create_tcp_backend)
    registry.register("unix", _create_unix_backend)
    rtnval = registry
    return rtnval
```

### Design Rationale

- `urllib.parse.urlparse` handles URI parsing, keeping the registry code simple.
- Factory functions take the parsed `urllib.parse.ParseResult` and extract backend-specific
  parameters from it.
- The registry is not a singleton — the startup configuration creates one and holds it.
  This avoids global state and supports testing with isolated registries.
