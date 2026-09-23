"""
    Tests for the F5.1 Remote Control Server module.
"""

import json
import socket
import threading

from typing import Any, Dict, Optional

from ccai.timetravel.pod.remote.server import RemoteControlServer
from ccai.timetravel.pod.portalregistry import get_portal_registry


# The server now fails closed (denies when no credential is configured), so the
# default setup configures this credential and _send_command sends it by default.
_TEST_CREDENTIAL = "test-secret-credential"


def _send_command(host: str, port: int, command: str, params: Optional[Dict[str, Any]] = None, token: Optional[str] = _TEST_CREDENTIAL) -> Dict[str, Any]:
    """
        Helper to send a JSON-lines command to the remote control server.
    """
    request = {"command": command}
    if params is not None:
        request["params"] = params
    if token is not None:
        request["token"] = token

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    sock.connect((host, port))
    data = json.dumps(request).encode("utf-8") + b"\n"
    sock.sendall(data)

    response_data = b""
    while b"\n" not in response_data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response_data += chunk
    sock.close()

    line = response_data.split(b"\n", 1)[0]
    rtnval = json.loads(line.decode("utf-8"))
    return rtnval


def _setup_remote_control_server() -> Any:
    """
        Replicates the ``TestRemoteControlServer.setUp`` fixture: creates a
        portal registry and a running :class:`RemoteControlServer` bound to an
        auto-assigned port.

        :returns: A tuple of (registry, server).
    """
    registry = get_portal_registry()
    server = RemoteControlServer(host="127.0.0.1", port=0, credential=_TEST_CREDENTIAL)
    # Use port=0 to auto-assign; we need to find the actual port
    server._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server._server_socket.bind(("127.0.0.1", 0))
    server._server_socket.listen(5)
    server._server_socket.settimeout(1.0)
    server._port = server._server_socket.getsockname()[1]
    server._running = True
    server._thread = threading.Thread(
        target=server._serve_loop, daemon=True
    )
    server._thread.start()

    rtnval = (registry, server)
    return rtnval


def _teardown_remote_control_server(registry: Any, server: Any) -> None:
    """
        Replicates the ``TestRemoteControlServer.tearDown`` fixture: stops the
        server and deactivates all portals on the registry.

        :param registry: The portal registry to deactivate.
        :param server: The remote control server to stop.
    """
    server.stop()
    registry.deactivate_all()
    return


def _setup_remote_control_server_auth() -> Any:
    """
        Replicates the ``TestRemoteControlServerAuth.setUp`` fixture: creates a
        running :class:`RemoteControlServer` configured with a credential and
        bound to an auto-assigned port.

        :returns: The configured server.
    """
    server = RemoteControlServer(
        host="127.0.0.1", port=0, credential="my_secret"
    )
    # Manual port setup for auto-assign
    server._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server._server_socket.bind(("127.0.0.1", 0))
    server._server_socket.listen(5)
    server._server_socket.settimeout(1.0)
    server._port = server._server_socket.getsockname()[1]
    server._running = True
    server._thread = threading.Thread(
        target=server._serve_loop, daemon=True
    )
    server._thread.start()

    rtnval = server
    return rtnval


def _teardown_remote_control_server_auth(server: Any) -> None:
    """
        Replicates the ``TestRemoteControlServerAuth.tearDown`` fixture: stops
        the server.

        :param server: The remote control server to stop.
    """
    server.stop()
    return


def test_server_accepts_connections() -> None:
    """
        Verify server starts and accepts TCP connections.
    """
    registry, server = _setup_remote_control_server()
    try:
        response = _send_command(
            host=server.host, port=server.port, command="list_portals"
        )

        assert response["status"] == "ok"
    finally:
        _teardown_remote_control_server(registry=registry, server=server)

    return


def test_list_portals_returns_portal_data() -> None:
    """
        Verify list_portals command returns portal data.
    """
    registry, server = _setup_remote_control_server()
    try:
        registry.activate_portal("test_portal")

        response = _send_command(
            host=server.host, port=server.port, command="list_portals"
        )

        assert response["status"] == "ok"
        portals = response["data"]["portals"]
        portal_names = [p["name"] for p in portals]
        assert "test_portal" in portal_names
    finally:
        _teardown_remote_control_server(registry=registry, server=server)

    return


def test_activate_portal_command() -> None:
    """
        Verify activate_portal command activates a portal.
    """
    registry, server = _setup_remote_control_server()
    try:
        response = _send_command(
            host=server.host, port=server.port,
            command="activate_portal", params={"name": "new_portal"}
        )

        assert response["status"] == "ok"
        assert registry.is_portal_active("new_portal")
    finally:
        _teardown_remote_control_server(registry=registry, server=server)

    return


def test_deactivate_portal_command() -> None:
    """
        Verify deactivate_portal command deactivates a portal.
    """
    registry, server = _setup_remote_control_server()
    try:
        registry.activate_portal("active_portal")

        response = _send_command(
            host=server.host, port=server.port,
            command="deactivate_portal", params={"name": "active_portal"}
        )

        assert response["status"] == "ok"
        assert not registry.is_portal_active("active_portal")
    finally:
        _teardown_remote_control_server(registry=registry, server=server)

    return


def test_unknown_command_returns_error() -> None:
    """
        Verify unknown command returns error response.
    """
    registry, server = _setup_remote_control_server()
    try:
        response = _send_command(
            host=server.host, port=server.port, command="nonexistent_command"
        )

        assert response["status"] == "error"
        assert "Unknown command" in response["message"]
    finally:
        _teardown_remote_control_server(registry=registry, server=server)

    return


def test_stop_cleanly_shuts_down() -> None:
    """
        Verify stop() cleanly shuts down the server.
    """
    registry, server = _setup_remote_control_server()
    try:
        server.stop()

        raised = False
        try:
            _send_command(host=server.host, port=server.port, command="list_portals")
        except OSError:
            raised = True

        assert raised
    finally:
        _teardown_remote_control_server(registry=registry, server=server)

    return


def test_auth_rejects_wrong_token() -> None:
    """
        Verify authentication rejects requests with wrong token.
    """
    server = _setup_remote_control_server_auth()
    try:
        response = _send_command(
            host=server.host, port=server.port,
            command="list_portals", token="wrong_token"
        )

        assert response["status"] == "error"
        assert "Authentication failed" in response["message"]
    finally:
        _teardown_remote_control_server_auth(server=server)

    return


def test_auth_accepts_correct_token() -> None:
    """
        Verify authentication accepts correct token.
    """
    server = _setup_remote_control_server_auth()
    try:
        response = _send_command(
            host=server.host, port=server.port,
            command="list_portals", token="my_secret"
        )

        assert response["status"] == "ok"
    finally:
        _teardown_remote_control_server_auth(server=server)

    return
