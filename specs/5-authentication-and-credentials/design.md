# F5.2 — Authentication and Credentials: Design

## Technical Design

### Module Location
`source/packages/automojo/timetravel/pod/remote/auth.py`

### Authentication Function

```python
import hmac


def verify_credential(provided: str | None, expected: str | None) -> bool:
    """Verify a provided credential against the expected credential.

    Uses constant-time comparison to prevent timing attacks.
    Returns True if authentication passes.
    """
    if expected is None:
        # No credential configured — allow all
        return True
    if provided is None:
        return False
    rtnval = hmac.compare_digest(provided, expected)
    return rtnval
```

### Integration with Remote Control Server

The `_dispatch` method in `RemoteControlServer` calls `verify_credential` before routing:

```python
from automojo.timetravel.pod.remote.auth import verify_credential

def _dispatch(self, request: dict) -> dict:
    token = request.get("token")
    if not verify_credential(token, self._credential):
        return {"status": "error", "message": "Authentication failed"}
    # ... dispatch to handler
```

### Design Rationale

- `hmac.compare_digest` is used for constant-time comparison (stdlib, no dependencies).
- Authentication is implemented as a standalone function to keep auth logic testable
  independently of the server.
- When no credential is configured, the auth check is a fast no-op.
