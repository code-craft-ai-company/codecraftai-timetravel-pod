# F2.2 — TCP Socket Stream Backend: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/backends/tcpbackend.py`

### Class Design

```python
import socket
import time
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONNECT_TIMEOUT = 5.0   # seconds
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 0.5     # seconds (doubles each retry)


class TcpStreamBackend:
    """Stream backend that sends trace data to a TCP endpoint."""

    def __init__(self, host: str, port: int,
                 connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
                 max_retries: int = DEFAULT_MAX_RETRIES,
                 retry_backoff: float = DEFAULT_RETRY_BACKOFF):
        self._host = host
        self._port = port
        self._connect_timeout = connect_timeout
        self._max_retries = max_retries
        self._retry_backoff = retry_backoff
        self._socket: socket.socket | None = None
        self._connect()

    def _connect(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self._connect_timeout)
        sock.connect((self._host, self._port))
        self._socket = sock

    def _reconnect(self) -> bool:
        backoff = self._retry_backoff
        for attempt in range(self._max_retries):
            try:
                self._close_socket()
                self._connect()
                return True
            except OSError:
                logger.warning("Reconnect attempt %d/%d failed, retrying in %.1fs",
                               attempt + 1, self._max_retries, backoff)
                time.sleep(backoff)
                backoff *= 2
        return False

    def write(self, data: bytes) -> None:
        try:
            self._socket.sendall(data)
        except OSError:
            if not self._reconnect():
                logger.error("Failed to reconnect to %s:%d, dropping trace data",
                             self._host, self._port)
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

- `socket.sendall()` is used to ensure complete writes — it handles partial sends internally.
- Exponential backoff prevents thundering-herd reconnection in production environments.
- Failed writes are silently dropped (with logging) rather than raising exceptions, because
  crashing the traced application is never acceptable.
- The backend uses blocking sockets because it is called from the `BufferedTraceWriter.flush()`,
  which runs on the traced thread — non-blocking I/O would add significant complexity with
  minimal benefit since flushes happen at buffer-size intervals (64 KB default).
