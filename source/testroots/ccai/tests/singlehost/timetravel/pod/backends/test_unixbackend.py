"""
    Tests for the F2.3 Unix Socket Stream Backend module.

    Uses a local Unix domain socket server thread for integration testing.
"""

import os
import socket
import tempfile
import threading

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


def _setup_server() -> tuple:
    """
        Replicate the original ``setUp`` per test: create a temporary
        directory, derive a socket path, and start a Unix domain socket
        test server.

        :returns: A tuple of ``(temp_dir, socket_path, server)``.
    """
    temp_dir = tempfile.mkdtemp()
    socket_path = os.path.join(temp_dir, "test.sock")
    server = UnixTestServer(socket_path)
    server.start()
    rtnval = (temp_dir, socket_path, server)
    return rtnval


def _teardown_server(temp_dir: str, server: "UnixTestServer") -> None:
    """
        Replicate the original ``tearDown`` per test: stop the server and
        remove any remaining files in the temporary directory.

        :param temp_dir: The temporary directory created during setup.
        :param server: The Unix domain socket test server to stop.
    """
    server.stop()
    if os.path.exists(temp_dir):
        # Clean up any remaining files
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
    return


def test_write_sends_data_to_server() -> None:
    """
        Verify write sends data to the Unix socket server.
    """
    temp_dir, socket_path, server = _setup_server()

    try:
        backend = UnixStreamBackend(socket_path=socket_path)

        backend.write(b"unix trace data")
        backend.close()

        import time
        time.sleep(0.1)

        assert bytes(server.received_data) == b"unix trace data"
    finally:
        _teardown_server(temp_dir=temp_dir, server=server)

    return


def test_multiple_writes_accumulate() -> None:
    """
        Verify multiple writes all arrive at the server.
    """
    temp_dir, socket_path, server = _setup_server()

    try:
        backend = UnixStreamBackend(socket_path=socket_path)

        backend.write(b"chunk1")
        backend.write(b"chunk2")
        backend.close()

        import time
        time.sleep(0.1)

        assert bytes(server.received_data) == b"chunk1chunk2"
    finally:
        _teardown_server(temp_dir=temp_dir, server=server)

    return


def test_close_without_error() -> None:
    """
        Verify close completes without error.
    """
    temp_dir, socket_path, server = _setup_server()

    try:
        backend = UnixStreamBackend(socket_path=socket_path)
        backend.close()
    finally:
        _teardown_server(temp_dir=temp_dir, server=server)

    return


def test_connection_to_nonexistent_socket_raises_error() -> None:
    """
        Verify connecting to a nonexistent socket path raises an error.
    """
    temp_dir, socket_path, server = _setup_server()

    try:
        raised = False
        try:
            UnixStreamBackend(socket_path="/tmp/nonexistent_test_socket.sock")
        except OSError:
            raised = True

        assert raised
    finally:
        _teardown_server(temp_dir=temp_dir, server=server)

    return
