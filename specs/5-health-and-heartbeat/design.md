# F5.4 — Health and Heartbeat: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/remote/heartbeat.py`

### Class Design

```python
import json
import time
import logging
import threading
import urllib.request

logger = logging.getLogger(__name__)

DEFAULT_HEARTBEAT_INTERVAL = 30.0  # seconds


class HeartbeatSender:
    """Sends periodic heartbeat to the debugging service."""

    def __init__(self, service_url: str, service_credential: str,
                 instance_id: str,
                 interval: float = DEFAULT_HEARTBEAT_INTERVAL):
        self._service_url = service_url.rstrip("/")
        self._service_credential = service_credential
        self._instance_id = instance_id
        self._interval = interval
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Start the heartbeat background thread."""
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the heartbeat background thread."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=self._interval + 2)

    def _heartbeat_loop(self) -> None:
        while not self._stop_event.is_set():
            self._send_heartbeat()
            self._stop_event.wait(timeout=self._interval)

    def _send_heartbeat(self) -> None:
        payload = {
            "instance_id": self._instance_id,
            "timestamp": time.time(),
        }
        try:
            url = f"{self._service_url}/heartbeat"
            data = json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._service_credential}",
                },
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=10) as response:
                response.read()
        except Exception as exc:
            logger.warning("Heartbeat failed: %s", exc)
```

### Design Rationale

- `threading.Event.wait(timeout)` is used instead of `time.sleep` so that `stop()` can
  interrupt the wait immediately.
- The daemon thread ensures the heartbeat does not prevent application exit.
- Failed heartbeats are logged at warning level and do not propagate exceptions.
