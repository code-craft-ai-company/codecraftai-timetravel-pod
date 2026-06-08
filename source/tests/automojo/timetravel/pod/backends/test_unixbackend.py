"""
    Tests for the F2.3 Unix Socket Stream Backend module.

    Uses a local Unix domain socket server thread for integration testing.
"""

import os
import socket
import tempfile
import threading
import unittest

from ccai.timetravel.pod.backends.unixbackend import UnixStreamBackend


class UnixTestServer:
    """
        A simple Unix domain socket server for testing.
    """

    def __init__(self, socket_path: str):
        self._socket_path = socket_path
        self._server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._server_socket.bind(socket_path)
        self._server_socket.listen(1)
        self.received_data = bytearray()
        self._thread = None
        self._running = False
        return

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._thread.start()
        return

    def _accept_loop(self):
        while self._running:
            try:
                self._server_socket.settimeout(0.5)
                conn, _ = self._server_socket.accept()
                self._read_from_connection(conn)
            except socket.timeout:
                continue
            except OSError:
                break
        return

    def _read_from_connection(self, conn):
        try:
            while self._running:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                self.received_data.extend(chunk)
        except OSError:
            pass
        finally:
            conn.close()
        return

    def stop(self):
        self._running = False
        self._server_socket.close()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        if os.path.exists(self._socket_path):
            os.unlink(self._socket_path)
        return


class TestUnixStreamBackend(unittest.TestCase):
    """
        Tests for the UnixStreamBackend class.
    """

    def setUp(self):
        self._temp_dir = tempfile.mkdtemp()
        self._socket_path = os.path.join(self._temp_dir, "test.sock")
        self._server = UnixTestServer(self._socket_path)
        self._server.start()
        return

    def tearDown(self):
        self._server.stop()
        if os.path.exists(self._temp_dir):
            # Clean up any remaining files
            for f in os.listdir(self._temp_dir):
                os.remove(os.path.join(self._temp_dir, f))
            os.rmdir(self._temp_dir)
        return

    def test_write_sends_data_to_server(self):
        """
            Verify write sends data to the Unix socket server.
        """
        backend = UnixStreamBackend(socket_path=self._socket_path)

        backend.write(b"unix trace data")
        backend.close()

        import time
        time.sleep(0.1)

        self.assertEqual(bytes(self._server.received_data), b"unix trace data")

        return

    def test_multiple_writes_accumulate(self):
        """
            Verify multiple writes all arrive at the server.
        """
        backend = UnixStreamBackend(socket_path=self._socket_path)

        backend.write(b"chunk1")
        backend.write(b"chunk2")
        backend.close()

        import time
        time.sleep(0.1)

        self.assertEqual(bytes(self._server.received_data), b"chunk1chunk2")

        return

    def test_close_without_error(self):
        """
            Verify close completes without error.
        """
        backend = UnixStreamBackend(socket_path=self._socket_path)
        backend.close()

        return

    def test_connection_to_nonexistent_socket_raises_error(self):
        """
            Verify connecting to a nonexistent socket path raises an error.
        """
        with self.assertRaises(OSError):
            UnixStreamBackend(socket_path="/tmp/nonexistent_test_socket.sock")

        return


if __name__ == "__main__":
    unittest.main()
