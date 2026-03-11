# F5.3 — Service Registration: Design

## Technical Design

### Module Location
`source/packages/automojo/timetravel/pod/remote/registration.py`

### Class Design

```python
import json
import logging
import urllib.request
import uuid

logger = logging.getLogger(__name__)


class ServiceRegistration:
    """Manages registration with an external debugging service."""

    def __init__(self, service_url: str, service_credential: str,
                 remote_host: str, remote_port: int, instance_credential: str):
        self._service_url = service_url.rstrip("/")
        self._service_credential = service_credential
        self._remote_host = remote_host
        self._remote_port = remote_port
        self._instance_credential = instance_credential
        self._instance_id = str(uuid.uuid4())
        self._registered = False

    @property
    def instance_id(self) -> str:
        rtnval = self._instance_id
        return rtnval

    def register(self) -> bool:
        """Register this application instance with the debugging service."""
        payload = {
            "instance_id": self._instance_id,
            "remote_host": self._remote_host,
            "remote_port": self._remote_port,
            "instance_credential": self._instance_credential,
        }
        try:
            self._send_request("/register", payload)
            self._registered = True
            logger.info("Registered with debugging service: %s (instance: %s)",
                        self._service_url, self._instance_id)
            return True
        except Exception as exc:
            logger.error("Failed to register with debugging service: %s", exc)
            return False

    def unregister(self) -> None:
        """Unregister this application instance from the debugging service."""
        if not self._registered:
            return
        payload = {"instance_id": self._instance_id}
        try:
            self._send_request("/unregister", payload)
            self._registered = False
            logger.info("Unregistered from debugging service: %s", self._service_url)
        except Exception as exc:
            logger.error("Failed to unregister from debugging service: %s", exc)

    def _send_request(self, path: str, payload: dict) -> bytes:
        """Send a JSON POST request to the debugging service."""
        url = f"{self._service_url}{path}"
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
            rtnval = response.read()
        return rtnval
```

### Design Rationale

- `urllib.request` is used instead of `requests` to avoid third-party dependencies.
- A UUID instance ID uniquely identifies each running instance, even if multiple
  instances are on the same host.
- Registration failures are logged and swallowed — the application runs regardless.
- The service credential is sent as a Bearer token in the Authorization header.
