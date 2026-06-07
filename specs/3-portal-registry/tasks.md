# F3.3 — Portal Registry: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/ccai/timetravel/pod/portalregistry.py`
- [x] 2. Implement `PortalRegistry` with all methods and thread-safe locking
- [x] 3. Create module-level singleton `_portal_registry` and `get_portal_registry()` accessor
- [x] 4. Export public symbols from the module

## Testing Tasks

- [x] 5. Create test file `source/tests/ccai/timetravel/pod/test_portalregistry.py`
- [x] 6. Test: `activate_portal` and `is_portal_active` round-trip
- [x] 7. Test: `deactivate_portal` sets portal to inactive
- [x] 8. Test: unknown portal name returns `False`
- [x] 9. Test: `activate_portals` bulk activates multiple portals
- [x] 10. Test: `deactivate_all` deactivates all portals
- [x] 11. Test: `list_portals` returns correct name/active pairs
- [x] 12. Test: concurrent access from multiple threads does not corrupt state
