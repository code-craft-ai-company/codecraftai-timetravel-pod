"""
    Tests for the F5.4 Health and Heartbeat module.

    Uses a mock HTTP server for testing heartbeat delivery.
"""

import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Tuple

from ccai.timetravel.pod.remote.heartbeat import HeartbeatSender
from ccai.timetravel.pod.remote.heartbeat import DEFAULT_HEARTBEAT_INTERVAL


class MockHeartbeatHandler(BaseHTTPRequestHandler):
    """
        Mock HTTP handler that records heartbeat requests.
    """

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode("utf-8"))
        self.server.received_heartbeats.append({
            "path": self.path,
            "payload": payload,
            "authorization": self.headers.get("Authorization"),
        })
        self.send_response(200)
        self.end_headers()
        return

    def log_message(self, format, *args):
        pass  # Suppress output


def _setup_mock_server() -> Tuple[HTTPServer, int, threading.Thread]:
    """
        Replicates the original setUp: starts a mock heartbeat HTTP server on a
        random port in a daemon thread.

        :returns: A tuple of the server, the bound port, and the server thread.
    """
    server = HTTPServer(("127.0.0.1", 0), MockHeartbeatHandler)
    server.received_heartbeats = []
    port = server.server_address[1]
    server_thread = threading.Thread(
        target=server.serve_forever, daemon=True
    )
    server_thread.start()
    rtnval = (server, port, server_thread)
    return rtnval


def _teardown_mock_server(server: HTTPServer, server_thread: threading.Thread) -> None:
    """
        Replicates the original tearDown: shuts the mock server down and joins
        its thread.

        :param server: The mock HTTP server to shut down.
        :param server_thread: The server thread to join.
    """
    server.shutdown()
    server_thread.join(timeout=2.0)
    return


def test_start_sends_heartbeats() -> None:
    """
        Verify start() begins sending heartbeats.
    """
    server, port, server_thread = _setup_mock_server()
    try:
        sender = HeartbeatSender(
            service_url=f"http://127.0.0.1:{port}",
            service_credential="token",
            instance_id="test-instance-id",
            interval=0.2,
        )

        sender.start()
        time.sleep(0.5)
        sender.stop()

        assert len(server.received_heartbeats) > 0
    finally:
        _teardown_mock_server(server=server, server_thread=server_thread)

    return


def test_stop_terminates_heartbeat_thread() -> None:
    """
        Verify stop() terminates the heartbeat thread.
    """
    server, port, server_thread = _setup_mock_server()
    try:
        sender = HeartbeatSender(
            service_url=f"http://127.0.0.1:{port}",
            service_credential="token",
            instance_id="test-instance",
            interval=0.2,
        )

        sender.start()
        time.sleep(0.3)
        sender.stop()

        count_after_stop = len(server.received_heartbeats)
        time.sleep(0.5)

        assert len(server.received_heartbeats) == count_after_stop
    finally:
        _teardown_mock_server(server=server, server_thread=server_thread)

    return


def test_failed_heartbeat_does_not_crash() -> None:
    """
        Verify failed heartbeat does not crash, logs a warning.
    """
    server, port, server_thread = _setup_mock_server()
    try:
        sender = HeartbeatSender(
            service_url="http://127.0.0.1:1",
            service_credential="token",
            instance_id="test-instance",
            interval=0.1,
        )

        sender.start()
        time.sleep(0.3)
        sender.stop()
        # Should not raise
    finally:
        _teardown_mock_server(server=server, server_thread=server_thread)

    return


def test_heartbeat_payload_contains_required_fields() -> None:
    """
        Verify heartbeat payload contains instance_id and timestamp.
    """
    server, port, server_thread = _setup_mock_server()
    try:
        sender = HeartbeatSender(
            service_url=f"http://127.0.0.1:{port}",
            service_credential="hb_token",
            instance_id="my-instance-123",
            interval=0.2,
        )

        sender.start()
        time.sleep(0.3)
        sender.stop()

        assert len(server.received_heartbeats) > 0

        hb = server.received_heartbeats[0]
        assert hb["path"] == "/heartbeat"
        assert hb["payload"]["instance_id"] == "my-instance-123"
        assert "timestamp" in hb["payload"]
        assert hb["authorization"] == "Bearer hb_token"
    finally:
        _teardown_mock_server(server=server, server_thread=server_thread)

    return


def test_default_heartbeat_interval_constant() -> None:
    """
        Verify DEFAULT_HEARTBEAT_INTERVAL is 30 seconds.
    """
    server, port, server_thread = _setup_mock_server()
    try:
        assert DEFAULT_HEARTBEAT_INTERVAL == 30.0
    finally:
        _teardown_mock_server(server=server, server_thread=server_thread)

    return
