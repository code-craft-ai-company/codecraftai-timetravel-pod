"""
    Tests for the F5.1 Remote Control Server module.
"""

import json
import socket
import time
import unittest

from automojo.timetravel.pod.remote.server import RemoteControlServer
from automojo.timetravel.pod.portalregistry import get_portal_registry


def _send_command(host, port, command, params=None, token=None):
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


class TestRemoteControlServer(unittest.TestCase):
    """
        Tests for the RemoteControlServer class.
    """

    def setUp(self):
        self._registry = get_portal_registry()
        self._server = RemoteControlServer(host="127.0.0.1", port=0)
        # Use port=0 to auto-assign; we need to find the actual port
        self._server._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server._server_socket.bind(("127.0.0.1", 0))
        self._server._server_socket.listen(5)
        self._server._server_socket.settimeout(1.0)
        self._server._port = self._server._server_socket.getsockname()[1]
        self._server._running = True
        import threading
        self._server._thread = threading.Thread(
            target=self._server._serve_loop, daemon=True
        )
        self._server._thread.start()
        return

    def tearDown(self):
        self._server.stop()
        self._registry.deactivate_all()
        return

    def test_server_accepts_connections(self):
        """
            Verify server starts and accepts TCP connections.
        """
        response = _send_command(
            self._server.host, self._server.port, "list_portals"
        )

        self.assertEqual(response["status"], "ok")

        return

    def test_list_portals_returns_portal_data(self):
        """
            Verify list_portals command returns portal data.
        """
        self._registry.activate_portal("test_portal")

        response = _send_command(
            self._server.host, self._server.port, "list_portals"
        )

        self.assertEqual(response["status"], "ok")
        portals = response["data"]["portals"]
        portal_names = [p["name"] for p in portals]
        self.assertIn("test_portal", portal_names)

        return

    def test_activate_portal_command(self):
        """
            Verify activate_portal command activates a portal.
        """
        response = _send_command(
            self._server.host, self._server.port,
            "activate_portal", {"name": "new_portal"}
        )

        self.assertEqual(response["status"], "ok")
        self.assertTrue(self._registry.is_portal_active("new_portal"))

        return

    def test_deactivate_portal_command(self):
        """
            Verify deactivate_portal command deactivates a portal.
        """
        self._registry.activate_portal("active_portal")

        response = _send_command(
            self._server.host, self._server.port,
            "deactivate_portal", {"name": "active_portal"}
        )

        self.assertEqual(response["status"], "ok")
        self.assertFalse(self._registry.is_portal_active("active_portal"))

        return

    def test_unknown_command_returns_error(self):
        """
            Verify unknown command returns error response.
        """
        response = _send_command(
            self._server.host, self._server.port, "nonexistent_command"
        )

        self.assertEqual(response["status"], "error")
        self.assertIn("Unknown command", response["message"])

        return

    def test_stop_cleanly_shuts_down(self):
        """
            Verify stop() cleanly shuts down the server.
        """
        self._server.stop()

        with self.assertRaises(OSError):
            _send_command(self._server.host, self._server.port, "list_portals")

        return


class TestRemoteControlServerAuth(unittest.TestCase):
    """
        Tests for RemoteControlServer authentication.
    """

    def setUp(self):
        self._server = RemoteControlServer(
            host="127.0.0.1", port=0, credential="my_secret"
        )
        # Manual port setup for auto-assign
        self._server._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server._server_socket.bind(("127.0.0.1", 0))
        self._server._server_socket.listen(5)
        self._server._server_socket.settimeout(1.0)
        self._server._port = self._server._server_socket.getsockname()[1]
        self._server._running = True
        import threading
        self._server._thread = threading.Thread(
            target=self._server._serve_loop, daemon=True
        )
        self._server._thread.start()
        return

    def tearDown(self):
        self._server.stop()
        return

    def test_auth_rejects_wrong_token(self):
        """
            Verify authentication rejects requests with wrong token.
        """
        response = _send_command(
            self._server.host, self._server.port,
            "list_portals", token="wrong_token"
        )

        self.assertEqual(response["status"], "error")
        self.assertIn("Authentication failed", response["message"])

        return

    def test_auth_accepts_correct_token(self):
        """
            Verify authentication accepts correct token.
        """
        response = _send_command(
            self._server.host, self._server.port,
            "list_portals", token="my_secret"
        )

        self.assertEqual(response["status"], "ok")

        return


if __name__ == "__main__":
    unittest.main()
