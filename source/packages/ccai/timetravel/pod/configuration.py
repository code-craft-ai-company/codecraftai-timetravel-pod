"""
    Provides the top-level startup configuration for the time travel pod.

    This module contains the :class:`TimeTravelConfig` model and the
    :func:`configure_timetravel` bootstrap function that initializes the
    pod subsystems from a single config object.
"""

from typing import Optional

from ccai.timetravel.pod.traceconfiguration import TraceConfiguration
from ccai.timetravel.pod.traceconfiguration import DEFAULT_TRACE_CONFIGURATION
from ccai.timetravel.pod.portalregistry import get_portal_registry
from ccai.timetravel.pod.backends.registry import create_default_registry
from ccai.timetravel.pod.remote.server import RemoteControlServer
from ccai.timetravel.pod.remote.mcpserver import McpServer


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
        "_mcp_enabled", "_mcp_transport", "_mcp_host", "_mcp_port", "_mcp_pipe",
        "_mcp_auth_token",
    )

    # Host values treated as local-only; binding anything else exposes the
    # MCP tool surface to the network and requires an auth token.
    LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})

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
        mcp_enabled: bool = False,
        mcp_transport: str = "stdio",
        mcp_host: str = "127.0.0.1",
        mcp_port: int = 9999,
        mcp_pipe: Optional[str] = None,
        mcp_auth_token: Optional[str] = None,
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
            :param mcp_enabled: Whether to enable the MCP server.
            :param mcp_transport: Transport for the MCP server ("stdio", "tcp", "pipe").
            :param mcp_host: Host for the MCP server.
            :param mcp_port: Port for the MCP server.
            :param mcp_pipe: Named pipe (Unix socket path) for the MCP server.
            :param mcp_auth_token: Shared-secret token required on MCP tool
                                   calls; required when binding a non-loopback
                                   host.
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
        self._mcp_enabled = mcp_enabled
        self._mcp_transport = mcp_transport
        self._mcp_host = mcp_host
        self._mcp_port = mcp_port
        self._mcp_pipe = mcp_pipe
        self._mcp_auth_token = mcp_auth_token
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

    @property
    def mcp_enabled(self) -> bool:
        """
            Whether the MCP server is enabled.
        """
        rtnval = self._mcp_enabled
        return rtnval

    @property
    def mcp_transport(self) -> str:
        """
            Transport mechanism for the MCP server.
        """
        rtnval = self._mcp_transport
        return rtnval

    @property
    def mcp_host(self) -> str:
        """
            Host for the MCP server.
        """
        rtnval = self._mcp_host
        return rtnval

    @property
    def mcp_port(self) -> int:
        """
            Port for the MCP server.
        """
        rtnval = self._mcp_port
        return rtnval

    @property
    def mcp_pipe(self) -> Optional[str]:
        """
            Named pipe (Unix socket path) for the MCP server.
        """
        rtnval = self._mcp_pipe
        return rtnval

    @property
    def mcp_auth_token(self) -> Optional[str]:
        """
            Shared-secret token required on MCP tool calls, or None.
        """
        rtnval = self._mcp_auth_token
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
            "mcp_enabled": self._mcp_enabled,
            "mcp_transport": self._mcp_transport,
            "mcp_host": self._mcp_host,
            "mcp_port": self._mcp_port,
            "mcp_pipe": self._mcp_pipe,
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
            mcp_enabled=data.get("mcp_enabled", False),
            mcp_transport=data.get("mcp_transport", "stdio"),
            mcp_host=data.get("mcp_host", "127.0.0.1"),
            mcp_port=data.get("mcp_port", 9999),
            mcp_pipe=data.get("mcp_pipe"),
            mcp_auth_token=data.get("mcp_auth_token"),
        )
        return rtnval


def configure_timetravel(config: TimeTravelConfig) -> dict:
    """
        Initialize the time travel pod with the given configuration.

        Activates portals in the registry, optionally creates a stream
        backend from the configured URI, and starts remote/MCP servers
        if enabled.

        :param config: The TimeTravelConfig to apply.

        :returns: A dictionary of created server instances that should be kept alive.
    """
    servers = {}

    # Activate portals
    registry = get_portal_registry()
    if config.active_portals:
        registry.activate_portals(config.active_portals)

    # Create backend (if URI specified)
    if config.backend_uri:
        backend_registry = create_default_registry()
        backend_registry.create_backend(config.backend_uri)

    # Start remote control server (if enabled)
    if config.remote_enabled:
        remote_server = RemoteControlServer(
            host=config.remote_host,
            port=config.remote_port,
            credential=config.remote_credential
        )
        remote_server.start()
        servers["remote"] = remote_server

    # Start MCP server (if enabled)
    if config.mcp_enabled:
        # Fail closed: binding the MCP tool surface to a non-loopback host
        # exposes activate_portal (and its predicate evaluation) to the
        # network, so a shared-secret token is required before that bind is
        # allowed.  Loopback and stdio/pipe transports remain local-trust.
        if config.mcp_transport == "tcp":
            is_loopback = config.mcp_host in TimeTravelConfig.LOOPBACK_HOSTS
            if not is_loopback and config.mcp_auth_token is None:
                err_msg_lines = [
                    "Refusing to bind the MCP server to a non-loopback host "
                    "without an auth token."
                ]
                err_msg_lines.append("MCP_HOST: {}".format(config.mcp_host))
                err_msg_lines.append(
                    "Set 'mcp_auth_token' to enable remote MCP access, or bind "
                    "a loopback host."
                )
                err_msg = "\n".join(err_msg_lines)
                raise ValueError(err_msg)

        mcp_server = McpServer(auth_token=config.mcp_auth_token)
        if config.mcp_transport == "tcp":
            mcp_server.start_background_tcp(config.mcp_host, config.mcp_port)
        elif config.mcp_transport == "pipe" and config.mcp_pipe:
            mcp_server.start_background_pipe(config.mcp_pipe)
        else:
            mcp_server.start_background_stdio()
        servers["mcp"] = mcp_server

    return servers
