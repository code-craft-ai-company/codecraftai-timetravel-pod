"""
    Tests for the F2.2 TCP Socket Stream Backend module.

    Uses a local TCP server thread for integration testing.
"""

import socket
import threading
import unittest

from ccai.timetravel.pod.backends.tcpbackend import TcpStreamBackend


class TcpTestServer:
    """
        A simple TCP server for testing that accumulates received data.
    """

    def __init__(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(("127.0.0.1", 0))
        self._server_socket.listen(1)
        self.host = "127.0.0.1"
        self.port = self._server_socket.getsockname()[1]
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
        return


class TestTcpStreamBackend(unittest.TestCase):
    """
        Tests for the TcpStreamBackend class.
    """

    def setUp(self):
        self._server = TcpTestServer()
        self._server.start()
        return

    def tearDown(self):
        self._server.stop()
        return

    def test_write_sends_data_to_server(self):
        """
            Verify write sends data to the TCP server.
        """
        backend = TcpStreamBackend(
            host=self._server.host, port=self._server.port
        )

        backend.write(b"trace data over tcp")
        backend.close()

        # Give the server a moment to receive
        import time
        time.sleep(0.1)

        self.assertEqual(bytes(self._server.received_data), b"trace data over tcp")

        return

    def test_multiple_writes_accumulate(self):
        """
            Verify multiple writes all arrive at the server.
        """
        backend = TcpStreamBackend(
            host=self._server.host, port=self._server.port
        )

        backend.write(b"part1")
        backend.write(b"part2")
        backend.close()

        import time
        time.sleep(0.1)

        self.assertEqual(bytes(self._server.received_data), b"part1part2")

        return

    def test_close_without_error(self):
        """
            Verify close completes without error.
        """
        backend = TcpStreamBackend(
            host=self._server.host, port=self._server.port
        )
        backend.close()

        return

    def test_connection_refused_raises_error(self):
        """
            Verify connecting to a closed port raises an error.
        """
        with self.assertRaises(OSError):
            TcpStreamBackend(host="127.0.0.1", port=1)

        return


if __name__ == "__main__":
    unittest.main()
