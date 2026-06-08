"""
    Tests for the F5.3 Service Registration module.

    Uses a mock HTTP server for testing without external dependencies.
"""

import json
import threading
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler

from ccai.timetravel.pod.remote.registration import ServiceRegistration


class MockServiceHandler(BaseHTTPRequestHandler):
    """
        Mock HTTP handler that records requests.
    """
    received_requests = []

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode("utf-8"))
        self.server.received_requests.append({
            "path": self.path,
            "payload": payload,
            "authorization": self.headers.get("Authorization"),
        })
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')
        return

    def log_message(self, format, *args) -> None:
        return  # Suppress output


def _setup_mock_service() -> tuple:
    """
        Replicates the original TestServiceRegistration.setUp: starts a mock
        HTTP server bound to an ephemeral port on a daemon background thread.

        :returns: A tuple of (server, port, thread) for the running mock service.
    """
    server = HTTPServer(("127.0.0.1", 0), MockServiceHandler)
    server.received_requests = []
    port = server.server_address[1]
    thread = threading.Thread(
        target=server.serve_forever, daemon=True
    )
    thread.start()

    rtnval = (server, port, thread)
    return rtnval


def _teardown_mock_service(server: HTTPServer, thread: threading.Thread) -> None:
    """
        Replicates the original TestServiceRegistration.tearDown: shuts down the
        mock HTTP server and joins its background thread.

        :param server: The running mock HTTP server to shut down.
        :param thread: The background thread serving the mock HTTP server.
    """
    server.shutdown()
    thread.join(timeout=2.0)
    return


def test_register_sends_correct_payload() -> None:
    """
        Verify register() sends correct payload to /register endpoint.
    """
    server, port, thread = _setup_mock_service()
    try:
        reg = ServiceRegistration(
            service_url=f"http://127.0.0.1:{port}",
            service_credential="svc_token",
            remote_host="192.168.1.10",
            remote_port=9876,
            instance_credential="inst_cred",
        )

        result = reg.register()

        assert result
        assert reg.registered
        assert len(server.received_requests) == 1

        req = server.received_requests[0]
        assert req["path"] == "/register"
        assert req["payload"]["remote_host"] == "192.168.1.10"
        assert req["payload"]["remote_port"] == 9876
        assert req["payload"]["instance_credential"] == "inst_cred"
        assert req["authorization"] == "Bearer svc_token"
    finally:
        _teardown_mock_service(server=server, thread=thread)

    return


def test_unregister_sends_correct_payload() -> None:
    """
        Verify unregister() sends correct payload to /unregister endpoint.
    """
    server, port, thread = _setup_mock_service()
    try:
        reg = ServiceRegistration(
            service_url=f"http://127.0.0.1:{port}",
            service_credential="svc_token",
            remote_host="127.0.0.1",
            remote_port=9876,
            instance_credential="cred",
        )

        reg.register()
        reg.unregister()

        assert not reg.registered
        assert len(server.received_requests) == 2

        req = server.received_requests[1]
        assert req["path"] == "/unregister"
        assert req["payload"]["instance_id"] == reg.instance_id
    finally:
        _teardown_mock_service(server=server, thread=thread)

    return


def test_registration_failure_returns_false() -> None:
    """
        Verify registration failure is caught and returns False.
    """
    server, port, thread = _setup_mock_service()
    try:
        reg = ServiceRegistration(
            service_url="http://127.0.0.1:1",
            service_credential="token",
            remote_host="127.0.0.1",
            remote_port=9876,
            instance_credential="cred",
        )

        result = reg.register()

        assert not result
        assert not reg.registered
    finally:
        _teardown_mock_service(server=server, thread=thread)

    return


def test_unregister_is_noop_if_not_registered() -> None:
    """
        Verify unregister() is a no-op if not registered.
    """
    server, port, thread = _setup_mock_service()
    try:
        reg = ServiceRegistration(
            service_url=f"http://127.0.0.1:{port}",
            service_credential="token",
            remote_host="127.0.0.1",
            remote_port=9876,
            instance_credential="cred",
        )

        reg.unregister()

        assert len(server.received_requests) == 0
    finally:
        _teardown_mock_service(server=server, thread=thread)

    return


def test_instance_id_is_valid_uuid() -> None:
    """
        Verify instance_id is a valid UUID string.
    """
    server, port, thread = _setup_mock_service()
    try:
        reg = ServiceRegistration(
            service_url="http://example.com",
            service_credential="token",
            remote_host="127.0.0.1",
            remote_port=9876,
            instance_credential="cred",
        )

        parsed = uuid.UUID(reg.instance_id)
        assert str(parsed) == reg.instance_id
    finally:
        _teardown_mock_service(server=server, thread=thread)

    return
