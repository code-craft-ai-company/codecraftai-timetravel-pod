"""
    Provides the remote control TCP server for portal management.

    This module contains the :class:`RemoteControlServer` which runs as a
    background daemon thread, accepts JSON-lines over TCP, and dispatches
    commands to manage portals and configuration at runtime.
"""

import json
import socket
import logging
import threading

from typing import Optional

from automojo.timetravel.pod.portalregistry import get_portal_registry
from automojo.timetravel.pod.remote.auth import verify_credential


logger = logging.getLogger(__name__)


class RemoteControlServer:
    """
        Background TCP server for remote portal management.

        Protocol: JSON-lines over TCP. Each message is a single JSON object
        terminated by a newline character. One request-response per connection.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 9876,
                 credential: Optional[str] = None) -> None:
        """
            Create a RemoteControlServer.

            :param host: The host to bind to.
            :param port: The port to bind to.
            :param credential: Optional credential for authentication.
        """
        self._host = host
        self._port = port
        self._credential = credential
        self._server_socket: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
        return

    @property
    def host(self) -> str:
        """
            The host the server is bound to.
        """
        rtnval = self._host
        return rtnval

    @property
    def port(self) -> int:
        """
            The port the server is bound to.
        """
        rtnval = self._port
        return rtnval

    def start(self) -> None:
        """
            Start the server in a background daemon thread.
        """
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen(5)
        self._server_socket.settimeout(1.0)
        self._running = True

        self._thread = threading.Thread(target=self._serve_loop, daemon=True)
        self._thread.start()
        return

    def stop(self) -> None:
        """
            Stop the server and wait for the background thread to exit.
        """
        self._running = False
        if self._server_socket is not None:
            self._server_socket.close()
            self._server_socket = None
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            self._thread = None
        return

    def _serve_loop(self) -> None:
        """
            Accept loop that runs on the background thread.
        """
        while self._running:
            try:
                client_socket, addr = self._server_socket.accept()
                self._handle_client(client_socket)
            except socket.timeout:
                continue
            except OSError:
                break
        return

    def _handle_client(self, client_socket: socket.socket) -> None:
        """
            Handle a single client connection (one request-response).

            :param client_socket: The client socket.
        """
        try:
            data = b""
            while b"\n" not in data:
                chunk = client_socket.recv(4096)
                if not chunk:
                    return
                data += chunk

            line = data.split(b"\n", 1)[0]
            request = json.loads(line.decode("utf-8"))
            response = self._dispatch(request)
            response_bytes = json.dumps(response).encode("utf-8") + b"\n"
            client_socket.sendall(response_bytes)
        except Exception as exc:
            logger.error("Error handling remote control request: %s", exc)
        finally:
            client_socket.close()
        return

    def _dispatch(self, request: dict) -> dict:
        """
            Route a command to the appropriate handler.

            :param request: The parsed JSON request dictionary.

            :returns: A response dictionary.
        """
        # Authentication check
        token = request.get("token")
        if not verify_credential(token, self._credential):
            rtnval = {"status": "error", "message": "Authentication failed"}
            return rtnval

        command = request.get("command", "")
        params = request.get("params", {})

        handler = _COMMAND_HANDLERS.get(command)
        if handler is None:
            rtnval = {
                "status": "error",
                "message": f"Unknown command: {command}",
            }
            return rtnval

        rtnval = handler(self, params)
        return rtnval


def _handle_list_portals(server, params: dict) -> dict:
    """
        Handle the list_portals command.

        :param server: The RemoteControlServer instance.
        :param params: The command parameters.

        :returns: A response dict with portal data.
    """
    registry = get_portal_registry()
    rtnval = {"status": "ok", "data": {"portals": registry.list_portals()}}
    return rtnval


def _handle_activate_portal(server, params: dict) -> dict:
    """
        Handle the activate_portal command.

        :param server: The RemoteControlServer instance.
        :param params: The command parameters.

        :returns: A response dict.
    """
    name = params.get("name")
    if name is None:
        rtnval = {"status": "error", "message": "Missing 'name' parameter"}
        return rtnval
    expression = params.get("expression")
    once = params.get("once", False)
    registry = get_portal_registry()
    registry.activate_portal(name, expression=expression, once=once)
    rtnval = {"status": "ok", "data": {"activated": name}}
    return rtnval


def _handle_deactivate_portal(server, params: dict) -> dict:
    """
        Handle the deactivate_portal command.

        :param server: The RemoteControlServer instance.
        :param params: The command parameters.

        :returns: A response dict.
    """
    name = params.get("name")
    if name is None:
        rtnval = {"status": "error", "message": "Missing 'name' parameter"}
        return rtnval
    registry = get_portal_registry()
    registry.deactivate_portal(name)
    rtnval = {"status": "ok", "data": {"deactivated": name}}
    return rtnval


_COMMAND_HANDLERS = {
    "list_portals": _handle_list_portals,
    "activate_portal": _handle_activate_portal,
    "deactivate_portal": _handle_deactivate_portal,
}
