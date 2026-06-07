# F5.1 — Remote Control Server: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/remote/server.py`

### Package Structure

```
source/packages/ccai/timetravel/pod/remote/
    __init__.py
    server.py
    auth.py
    registration.py
    heartbeat.py
```

### Protocol

JSON-lines over TCP. Each message is a single JSON object terminated by `\n`.

**Request format:**
```json
{"command": "list_portals", "token": "...", "params": {}}
```

**Response format:**
```json
{"status": "ok", "data": {...}}
{"status": "error", "message": "..."}
```

### Server Design

```python
import socket
import json
import threading
import logging

logger = logging.getLogger(__name__)


class RemoteControlServer:
    """Background TCP server for remote portal management."""

    def __init__(self, host: str = "127.0.0.1", port: int = 9876,
                 credential: str | None = None):
        self._host = host
        self._port = port
        self._credential = credential
        self._server_socket: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._running = False

    def start(self) -> None:
        """Start the server in a background daemon thread."""
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen(5)
        self._server_socket.settimeout(1.0)  # Allow periodic shutdown checks
        self._running = True

        self._thread = threading.Thread(target=self._serve_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the server and wait for the background thread to exit."""
        self._running = False
        if self._server_socket is not None:
            self._server_socket.close()
        if self._thread is not None:
            self._thread.join(timeout=5.0)

    def _serve_loop(self) -> None:
        while self._running:
            try:
                client_socket, addr = self._server_socket.accept()
                self._handle_client(client_socket)
            except socket.timeout:
                continue
            except OSError:
                break

    def _handle_client(self, client_socket: socket.socket) -> None:
        """Handle a single client connection (one request-response per connection)."""
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

    def _dispatch(self, request: dict) -> dict:
        """Route a command to the appropriate handler."""
        # Authentication check
        if self._credential is not None:
            token = request.get("token")
            if token != self._credential:
                return {"status": "error", "message": "Authentication failed"}

        command = request.get("command", "")
        params = request.get("params", {})
        handler = self._handlers.get(command)
        if handler is None:
            return {"status": "error", "message": f"Unknown command: {command}"}
        rtnval = handler(self, params)
        return rtnval
```

### Command Handlers

Command handlers delegate to the `PortalRegistry` and `TraceConfiguration`:

```python
def _handle_list_portals(self, params: dict) -> dict:
    registry = get_portal_registry()
    rtnval = {"status": "ok", "data": {"portals": registry.list_portals()}}
    return rtnval

def _handle_activate_portal(self, params: dict) -> dict:
    name = params.get("name")
    registry = get_portal_registry()
    registry.activate_portal(name)
    rtnval = {"status": "ok", "data": {"activated": name}}
    return rtnval

# ... similar handlers for deactivate, get_config, update_config
```

### Design Rationale

- The server uses `socket.timeout` (1 second) to periodically check the `_running` flag
  for clean shutdown without requiring OS-level interrupts.
- Daemon thread ensures the server does not prevent application exit.
- One connection per request keeps the protocol simple and avoids connection management
  complexity.
- All handlers delegate to existing thread-safe components (PortalRegistry, etc.).
