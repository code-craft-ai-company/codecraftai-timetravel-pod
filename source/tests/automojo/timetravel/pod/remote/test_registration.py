"""
    Tests for the F5.3 Service Registration module.

    Uses a mock HTTP server for testing without external dependencies.
"""

import json
import threading
import unittest
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler

from ccai.timetravel.pod.remote.registration import ServiceRegistration


class MockServiceHandler(BaseHTTPRequestHandler):
    """
        Mock HTTP handler that records requests.
    """
    received_requests = []

    def do_POST(self):
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

    def log_message(self, format, *args):
        pass  # Suppress output


class TestServiceRegistration(unittest.TestCase):
    """
        Tests for the ServiceRegistration class.
    """

    def setUp(self):
        self._server = HTTPServer(("127.0.0.1", 0), MockServiceHandler)
        self._server.received_requests = []
        self._port = self._server.server_address[1]
        self._thread = threading.Thread(
            target=self._server.serve_forever, daemon=True
        )
        self._thread.start()
        return

    def tearDown(self):
        self._server.shutdown()
        self._thread.join(timeout=2.0)
        return

    def test_register_sends_correct_payload(self):
        """
            Verify register() sends correct payload to /register endpoint.
        """
        reg = ServiceRegistration(
            service_url=f"http://127.0.0.1:{self._port}",
            service_credential="svc_token",
            remote_host="192.168.1.10",
            remote_port=9876,
            instance_credential="inst_cred",
        )

        result = reg.register()

        self.assertTrue(result)
        self.assertTrue(reg.registered)
        self.assertEqual(len(self._server.received_requests), 1)

        req = self._server.received_requests[0]
        self.assertEqual(req["path"], "/register")
        self.assertEqual(req["payload"]["remote_host"], "192.168.1.10")
        self.assertEqual(req["payload"]["remote_port"], 9876)
        self.assertEqual(req["payload"]["instance_credential"], "inst_cred")
        self.assertEqual(req["authorization"], "Bearer svc_token")

        return

    def test_unregister_sends_correct_payload(self):
        """
            Verify unregister() sends correct payload to /unregister endpoint.
        """
        reg = ServiceRegistration(
            service_url=f"http://127.0.0.1:{self._port}",
            service_credential="svc_token",
            remote_host="127.0.0.1",
            remote_port=9876,
            instance_credential="cred",
        )

        reg.register()
        reg.unregister()

        self.assertFalse(reg.registered)
        self.assertEqual(len(self._server.received_requests), 2)

        req = self._server.received_requests[1]
        self.assertEqual(req["path"], "/unregister")
        self.assertEqual(req["payload"]["instance_id"], reg.instance_id)

        return

    def test_registration_failure_returns_false(self):
        """
            Verify registration failure is caught and returns False.
        """
        reg = ServiceRegistration(
            service_url="http://127.0.0.1:1",
            service_credential="token",
            remote_host="127.0.0.1",
            remote_port=9876,
            instance_credential="cred",
        )

        result = reg.register()

        self.assertFalse(result)
        self.assertFalse(reg.registered)

        return

    def test_unregister_is_noop_if_not_registered(self):
        """
            Verify unregister() is a no-op if not registered.
        """
        reg = ServiceRegistration(
            service_url=f"http://127.0.0.1:{self._port}",
            service_credential="token",
            remote_host="127.0.0.1",
            remote_port=9876,
            instance_credential="cred",
        )

        reg.unregister()

        self.assertEqual(len(self._server.received_requests), 0)

        return

    def test_instance_id_is_valid_uuid(self):
        """
            Verify instance_id is a valid UUID string.
        """
        reg = ServiceRegistration(
            service_url="http://example.com",
            service_credential="token",
            remote_host="127.0.0.1",
            remote_port=9876,
            instance_credential="cred",
        )

        parsed = uuid.UUID(reg.instance_id)
        self.assertEqual(str(parsed), reg.instance_id)

        return


if __name__ == "__main__":
    unittest.main()
