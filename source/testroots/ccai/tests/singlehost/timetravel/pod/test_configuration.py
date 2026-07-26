"""
    Tests for the F4.1 Startup Configuration module.
"""

from ccai.timetravel.pod.configuration import TimeTravelConfig
from ccai.timetravel.pod.configuration import configure_timetravel
from ccai.timetravel.pod.traceconfiguration import TraceConfiguration
from ccai.timetravel.pod.traceconfiguration import DEFAULT_TRACE_CONFIGURATION
from ccai.timetravel.pod.portalregistry import PortalRegistry
from ccai.timetravel.pod.portalregistry import get_portal_registry


def _setup_configure_timetravel() -> PortalRegistry:
    """
        Replicates the TestConfigureTimetravel.setUp behaviour, acquiring the
        portal registry used by the configure_timetravel tests.

        :returns: The portal registry instance.
    """
    registry = get_portal_registry()
    return registry


def test_defaults_are_correct() -> None:
    """
        Verify TimeTravelConfig defaults are correct.
    """
    config = TimeTravelConfig()

    assert config.active_portals == []
    assert config.trace_configuration is DEFAULT_TRACE_CONFIGURATION
    assert config.backend_uri is None
    assert not config.remote_enabled
    assert config.remote_host == "127.0.0.1"
    assert config.remote_port == 9876
    assert config.remote_credential is None
    assert config.service_url is None
    assert config.service_credential is None
    assert not config.mcp_enabled
    assert config.mcp_transport == "stdio"
    # Loopback, NOT 0.0.0.0.  This is the MCP control server's BIND
    # address, and it was deliberately narrowed by the commit "Shut down
    # the timetravel-pod RCE surface".  Restoring 0.0.0.0 here would
    # re-expose that surface on every interface by default.
    assert config.mcp_host == "127.0.0.1"
    assert config.mcp_port == 9999
    assert config.mcp_pipe is None

    return


def test_as_dict_from_dict_round_trip() -> None:
    """
        Verify as_dict() / from_dict() round-trip.
    """
    trace_config = TraceConfiguration(
        trace_calls=True, trace_lines=True, trace_variables=True
    )
    original = TimeTravelConfig(
        active_portals=["portal_a", "portal_b"],
        trace_configuration=trace_config,
        backend_uri="file:///tmp/trace.bin",
        remote_enabled=True,
        remote_host="0.0.0.0",
        remote_port=8080,
        mcp_enabled=True,
        mcp_transport="pipe",
        mcp_host="10.0.0.1",
        mcp_port=10000,
        mcp_pipe="/tmp/test.sock"
    )

    data = original.as_dict()
    restored = TimeTravelConfig.from_dict(data)

    assert restored.active_portals == ["portal_a", "portal_b"]
    assert restored.backend_uri == "file:///tmp/trace.bin"
    assert restored.remote_enabled
    assert restored.remote_host == "0.0.0.0"
    assert restored.remote_port == 8080
    assert restored.trace_configuration.trace_calls
    assert restored.trace_configuration.trace_lines
    assert restored.trace_configuration.trace_variables
    assert restored.mcp_enabled
    assert restored.mcp_transport == "pipe"
    assert restored.mcp_host == "10.0.0.1"
    assert restored.mcp_port == 10000
    assert restored.mcp_pipe == "/tmp/test.sock"

    return


def test_as_dict_excludes_credentials() -> None:
    """
        Verify credentials are excluded from as_dict().
    """
    config = TimeTravelConfig(
        remote_credential="secret", service_credential="token"
    )

    data = config.as_dict()

    assert "remote_credential" not in data
    assert "service_credential" not in data

    return


def test_active_portals_returns_copy() -> None:
    """
        Verify active_portals returns a copy, not the internal list.
    """
    config = TimeTravelConfig(active_portals=["a", "b"])

    portals = config.active_portals
    portals.append("c")

    assert len(config.active_portals) == 2

    return


def test_activates_specified_portals() -> None:
    """
        Verify configure_timetravel activates specified portals in the registry.
    """
    registry = _setup_configure_timetravel()

    try:
        config = TimeTravelConfig(
            active_portals=["portal_x", "portal_y"]
        )

        configure_timetravel(config)

        assert registry.is_portal_active("portal_x")
        assert registry.is_portal_active("portal_y")
    finally:
        registry.deactivate_all()

    return


def test_no_backend_uri_does_not_create_backend() -> None:
    """
        Verify configure_timetravel with no backend URI does not create
        a backend (no error occurs).
    """
    registry = _setup_configure_timetravel()

    try:
        config = TimeTravelConfig()

        # This should not raise
        configure_timetravel(config)
    finally:
        registry.deactivate_all()

    return


def test_from_dict_with_empty_dict() -> None:
    """
        Verify from_dict with empty dict uses defaults.
    """
    registry = _setup_configure_timetravel()

    try:
        config = TimeTravelConfig.from_dict({})

        assert config.active_portals == []
        assert config.backend_uri is None
        assert not config.remote_enabled
        assert not config.mcp_enabled
        assert config.mcp_transport == "stdio"
    finally:
        registry.deactivate_all()

    return
