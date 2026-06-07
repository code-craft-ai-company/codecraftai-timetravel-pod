"""
    Tests for the F5.4 Health and Heartbeat module.

    Uses a mock HTTP server for testing heartbeat delivery.
"""

import json
import threading
import time
import unittest
from http.server import HTTPServer, BaseHTTPRequestHandler

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


class TestHeartbeatSender(unittest.TestCase):
    """
        Tests for the HeartbeatSender class.
    """

    def setUp(self):
        self._server = HTTPServer(("127.0.0.1", 0), MockHeartbeatHandler)
        self._server.received_heartbeats = []
        self._port = self._server.server_address[1]
        self._server_thread = threading.Thread(
            target=self._server.serve_forever, daemon=True
        )
        self._server_thread.start()
        return

    def tearDown(self):
        self._server.shutdown()
        self._server_thread.join(timeout=2.0)
        return

    def test_start_sends_heartbeats(self):
        """
            Verify start() begins sending heartbeats.
        """
        sender = HeartbeatSender(
            service_url=f"http://127.0.0.1:{self._port}",
            service_credential="token",
            instance_id="test-instance-id",
            interval=0.2,
        )

        sender.start()
        time.sleep(0.5)
        sender.stop()

        self.assertGreater(len(self._server.received_heartbeats), 0)

        return

    def test_stop_terminates_heartbeat_thread(self):
        """
            Verify stop() terminates the heartbeat thread.
        """
        sender = HeartbeatSender(
            service_url=f"http://127.0.0.1:{self._port}",
            service_credential="token",
            instance_id="test-instance",
            interval=0.2,
        )

        sender.start()
        time.sleep(0.3)
        sender.stop()

        count_after_stop = len(self._server.received_heartbeats)
        time.sleep(0.5)

        self.assertEqual(len(self._server.received_heartbeats), count_after_stop)

        return

    def test_failed_heartbeat_does_not_crash(self):
        """
            Verify failed heartbeat does not crash, logs a warning.
        """
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

        return

    def test_heartbeat_payload_contains_required_fields(self):
        """
            Verify heartbeat payload contains instance_id and timestamp.
        """
        sender = HeartbeatSender(
            service_url=f"http://127.0.0.1:{self._port}",
            service_credential="hb_token",
            instance_id="my-instance-123",
            interval=0.2,
        )

        sender.start()
        time.sleep(0.3)
        sender.stop()

        self.assertGreater(len(self._server.received_heartbeats), 0)

        hb = self._server.received_heartbeats[0]
        self.assertEqual(hb["path"], "/heartbeat")
        self.assertEqual(hb["payload"]["instance_id"], "my-instance-123")
        self.assertIn("timestamp", hb["payload"])
        self.assertEqual(hb["authorization"], "Bearer hb_token")

        return

    def test_default_heartbeat_interval_constant(self):
        """
            Verify DEFAULT_HEARTBEAT_INTERVAL is 30 seconds.
        """
        self.assertEqual(DEFAULT_HEARTBEAT_INTERVAL, 30.0)

        return


if __name__ == "__main__":
    unittest.main()
