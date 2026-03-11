"""
    Provides the top-level startup configuration for the time travel pod.

    This module contains the :class:`TimeTravelConfig` model and the
    :func:`configure_timetravel` bootstrap function that initializes the
    pod subsystems from a single config object.
"""

from typing import Optional

from automojo.timetravel.pod.traceconfiguration import TraceConfiguration
from automojo.timetravel.pod.traceconfiguration import DEFAULT_TRACE_CONFIGURATION
from automojo.timetravel.pod.portalregistry import get_portal_registry
from automojo.timetravel.pod.backends.registry import create_default_registry


class TimeTravelConfig:
    """
        Top-level configuration for the time travel pod.

        Centralizes all configuration in one place for easy construction
        from CLI arguments, config files, or programmatic setup.
    """

    __slots__ = (
        "_active_portals", "_trace_configuration", "_backend_uri",
        "_remote_enabled", "_remote_host", "_remote_port",
        "_remote_credential", "_service_url", "_service_credential",
    )

    def __init__(
        self,
        active_portals: Optional[list] = None,
        trace_configuration: Optional[TraceConfiguration] = None,
        backend_uri: Optional[str] = None,
        remote_enabled: bool = False,
        remote_host: str = "127.0.0.1",
        remote_port: int = 9876,
        remote_credential: Optional[str] = None,
        service_url: Optional[str] = None,
        service_credential: Optional[str] = None,
    ) -> None:
        """
            Create a TimeTravelConfig.

            :param active_portals: List of portal names to activate.
            :param trace_configuration: The trace configuration controlling granularity.
            :param backend_uri: URI for the stream backend (e.g. "file:///tmp/trace.bin").
            :param remote_enabled: Whether to enable the remote control server.
            :param remote_host: Host for the remote control server.
            :param remote_port: Port for the remote control server.
            :param remote_credential: Credential for remote control authentication.
            :param service_url: URL for the time travel service.
            :param service_credential: Credential for the time travel service.
        """
        if active_portals is not None:
            self._active_portals = active_portals
        else:
            self._active_portals = []

        if trace_configuration is not None:
            self._trace_configuration = trace_configuration
        else:
            self._trace_configuration = DEFAULT_TRACE_CONFIGURATION

        self._backend_uri = backend_uri
        self._remote_enabled = remote_enabled
        self._remote_host = remote_host
        self._remote_port = remote_port
        self._remote_credential = remote_credential
        self._service_url = service_url
        self._service_credential = service_credential
        return

    @property
    def active_portals(self) -> list:
        """
            List of portal names to activate. Returns a copy.
        """
        rtnval = list(self._active_portals)
        return rtnval

    @property
    def trace_configuration(self) -> TraceConfiguration:
        """
            The trace configuration controlling granularity.
        """
        rtnval = self._trace_configuration
        return rtnval

    @property
    def backend_uri(self) -> Optional[str]:
        """
            URI for the stream backend, or None.
        """
        rtnval = self._backend_uri
        return rtnval

    @property
    def remote_enabled(self) -> bool:
        """
            Whether the remote control server is enabled.
        """
        rtnval = self._remote_enabled
        return rtnval

    @property
    def remote_host(self) -> str:
        """
            Host for the remote control server.
        """
        rtnval = self._remote_host
        return rtnval

    @property
    def remote_port(self) -> int:
        """
            Port for the remote control server.
        """
        rtnval = self._remote_port
        return rtnval

    @property
    def remote_credential(self) -> Optional[str]:
        """
            Credential for remote control authentication.
        """
        rtnval = self._remote_credential
        return rtnval

    @property
    def service_url(self) -> Optional[str]:
        """
            URL for the time travel service.
        """
        rtnval = self._service_url
        return rtnval

    @property
    def service_credential(self) -> Optional[str]:
        """
            Credential for the time travel service.
        """
        rtnval = self._service_credential
        return rtnval

    def as_dict(self) -> dict:
        """
            Serialize to a dictionary.

            Credentials are excluded for security.

            :returns: A dictionary representation of the config.
        """
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
        """
            Deserialize from a dictionary.

            :param data: The dictionary to deserialize.

            :returns: A TimeTravelConfig instance.
        """
        trace_config = None
        if "trace_configuration" in data:
            trace_config = TraceConfiguration.from_dict(
                data["trace_configuration"]
            )

        rtnval = cls(
            active_portals=data.get("active_portals"),
            trace_configuration=trace_config,
            backend_uri=data.get("backend_uri"),
            remote_enabled=data.get("remote_enabled", False),
            remote_host=data.get("remote_host", "127.0.0.1"),
            remote_port=data.get("remote_port", 9876),
        )
        return rtnval


def configure_timetravel(config: TimeTravelConfig) -> None:
    """
        Initialize the time travel pod with the given configuration.

        Activates portals in the registry and optionally creates a stream
        backend from the configured URI.

        :param config: The TimeTravelConfig to apply.
    """
    # Activate portals
    registry = get_portal_registry()
    if config.active_portals:
        registry.activate_portals(config.active_portals)

    # Create backend (if URI specified)
    if config.backend_uri:
        backend_registry = create_default_registry()
        backend_registry.create_backend(config.backend_uri)

    # Start remote control server (if enabled) — deferred to Layer 5
    return
