# F4.1 — Startup Configuration: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/configuration.py`

### Config Model

```python
from ccai.timetravel.pod.traceconfiguration import TraceConfiguration, DEFAULT_TRACE_CONFIGURATION


class TimeTravelConfig:
    """Top-level configuration for the time travel pod."""

    def __init__(
        self,
        active_portals: list[str] | None = None,
        trace_configuration: TraceConfiguration | None = None,
        backend_uri: str | None = None,
        remote_enabled: bool = False,
        remote_host: str = "127.0.0.1",
        remote_port: int = 9876,
        remote_credential: str | None = None,
        service_url: str | None = None,
        service_credential: str | None = None,
    ):
        self._active_portals = active_portals or []
        self._trace_configuration = trace_configuration or DEFAULT_TRACE_CONFIGURATION
        self._backend_uri = backend_uri
        self._remote_enabled = remote_enabled
        self._remote_host = remote_host
        self._remote_port = remote_port
        self._remote_credential = remote_credential
        self._service_url = service_url
        self._service_credential = service_credential

    # Read-only properties for each field...
    @property
    def active_portals(self) -> list[str]:
        rtnval = list(self._active_portals)
        return rtnval

    @property
    def trace_configuration(self) -> TraceConfiguration:
        rtnval = self._trace_configuration
        return rtnval

    @property
    def backend_uri(self) -> str | None:
        rtnval = self._backend_uri
        return rtnval

    @property
    def remote_enabled(self) -> bool:
        rtnval = self._remote_enabled
        return rtnval

    @property
    def remote_host(self) -> str:
        rtnval = self._remote_host
        return rtnval

    @property
    def remote_port(self) -> int:
        rtnval = self._remote_port
        return rtnval

    @property
    def remote_credential(self) -> str | None:
        rtnval = self._remote_credential
        return rtnval

    @property
    def service_url(self) -> str | None:
        rtnval = self._service_url
        return rtnval

    @property
    def service_credential(self) -> str | None:
        rtnval = self._service_credential
        return rtnval

    def as_dict(self) -> dict:
        rtnval = {
            "active_portals": self._active_portals,
            "trace_configuration": self._trace_configuration.as_dict(),
            "backend_uri": self._backend_uri,
            "remote_enabled": self._remote_enabled,
            "remote_host": self._remote_host,
            "remote_port": self._remote_port,
        }
        return rtnval

    @classmethod
    def from_dict(cls, data: dict) -> "TimeTravelConfig":
        trace_config = None
        if "trace_configuration" in data:
            trace_config = TraceConfiguration.from_dict(data["trace_configuration"])
        rtnval = cls(
            active_portals=data.get("active_portals"),
            trace_configuration=trace_config,
            backend_uri=data.get("backend_uri"),
            remote_enabled=data.get("remote_enabled", False),
            remote_host=data.get("remote_host", "127.0.0.1"),
            remote_port=data.get("remote_port", 9876),
        )
        return rtnval
```

### Bootstrap Function

```python
from ccai.timetravel.pod.portalregistry import get_portal_registry
from ccai.timetravel.pod.backends.registry import create_default_registry


def configure_timetravel(config: TimeTravelConfig) -> None:
    """Initialize the time travel pod with the given configuration."""

    # Activate portals
    registry = get_portal_registry()
    if config.active_portals:
        registry.activate_portals(config.active_portals)

    # Create backend (if URI specified)
    if config.backend_uri:
        backend_registry = create_default_registry()
        backend = backend_registry.create_backend(config.backend_uri)
        # Store backend for use by the gateway
        ...

    # Start remote control server (if enabled)
    if config.remote_enabled:
        # Deferred to Layer 5 implementation
        ...
```

### Design Rationale

- The `TimeTravelConfig` centralizes all configuration in one place, making it easy to
  construct from CLI arguments or a config file.
- Credentials are not included in `as_dict()` for security — they are only set programmatically.
- `configure_timetravel` is a procedural bootstrap function rather than a class to keep
  the initialization sequence explicit and debuggable.
