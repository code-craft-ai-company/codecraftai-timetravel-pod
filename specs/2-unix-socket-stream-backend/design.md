# F2.3 — Unix Socket Stream Backend: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/backends/unixbackend.py`

### Class Design

```python
import socket
import time
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONNECT_TIMEOUT = 5.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 0.5


class UnixStreamBackend:
    """Stream backend that sends trace data over a Unix domain socket."""

    def __init__(self, socket_path: str,
                 connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
                 max_retries: int = DEFAULT_MAX_RETRIES,
                 retry_backoff: float = DEFAULT_RETRY_BACKOFF):
        self._socket_path = socket_path
        self._connect_timeout = connect_timeout
        self._max_retries = max_retries
        self._retry_backoff = retry_backoff
        self._socket: socket.socket | None = None
        self._connect()

    def _connect(self) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self._connect_timeout)
        sock.connect(self._socket_path)
        self._socket = sock

    def _reconnect(self) -> bool:
        backoff = self._retry_backoff
        for attempt in range(self._max_retries):
            try:
                self._close_socket()
                self._connect()
                return True
            except OSError:
                logger.warning("Unix socket reconnect attempt %d/%d failed",
                               attempt + 1, self._max_retries)
                time.sleep(backoff)
                backoff *= 2
        return False

    def write(self, data: bytes) -> None:
        try:
            self._socket.sendall(data)
        except OSError:
            if not self._reconnect():
                logger.error("Failed to reconnect to %s, dropping trace data",
                             self._socket_path)
                return
            try:
                self._socket.sendall(data)
            except OSError:
                logger.error("Write failed after reconnect, dropping trace data")

    def _close_socket(self) -> None:
        if self._socket is not None:
            try:
                self._socket.close()
            except OSError:
                pass
            self._socket = None

    def close(self) -> None:
        self._close_socket()
```

### Design Rationale

- The implementation mirrors `TcpStreamBackend` but uses `AF_UNIX` instead of `AF_INET`.
- Unix domain sockets bypass the network stack entirely, providing lower latency and higher
  throughput for same-host communication.
- The reconnection and error-handling patterns are identical to the TCP backend for consistency.
