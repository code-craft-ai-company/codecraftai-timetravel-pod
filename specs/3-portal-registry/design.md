# F3.3 — Portal Registry: Design

## Technical Design

### Module Location
`source/packages/automojo/timetravel/pod/portalregistry.py`

### Class Design

```python
import threading


class PortalRegistry:
    """Thread-safe registry of portal names and their activation state."""

    def __init__(self):
        self._lock = threading.Lock()
        self._portals: dict[str, bool] = {}  # name -> active

    def activate_portal(self, name: str) -> None:
        with self._lock:
            self._portals[name] = True

    def deactivate_portal(self, name: str) -> None:
        with self._lock:
            self._portals[name] = False

    def is_portal_active(self, name: str) -> bool:
        with self._lock:
            rtnval = self._portals.get(name, False)
        return rtnval

    def activate_portals(self, names: list[str]) -> None:
        with self._lock:
            for name in names:
                self._portals[name] = True

    def deactivate_all(self) -> None:
        with self._lock:
            for name in self._portals:
                self._portals[name] = False

    def list_portals(self) -> list[dict]:
        with self._lock:
            rtnval = [
                {"name": name, "active": active}
                for name, active in self._portals.items()
            ]
        return rtnval
```

### Singleton Access

```python
_portal_registry = PortalRegistry()

def get_portal_registry() -> PortalRegistry:
    return _portal_registry
```

### Design Rationale

- `threading.Lock` is used for thread safety. The lock is fine-grained — held only
  during dict operations, not during tracing.
- `is_portal_active` returns `False` for unknown names, meaning portals that were never
  registered are simply inactive. This avoids requiring explicit portal declaration.
- The registry stores activation state (not portal metadata) to keep it lightweight.
