# F4.1 — Startup Configuration: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/automojo/timetravel/pod/configuration.py`
- [x] 2. Implement `TimeTravelConfig` with all properties, `as_dict()`, and `from_dict()`
- [x] 3. Implement `configure_timetravel()` bootstrap function
- [x] 4. Export public symbols from the module

## Testing Tasks

- [x] 5. Create test file `source/tests/automojo/timetravel/pod/test_configuration.py`
- [x] 6. Test: `TimeTravelConfig` defaults are correct
- [x] 7. Test: `as_dict()` / `from_dict()` round-trip
- [x] 8. Test: `configure_timetravel` activates specified portals in the registry
- [x] 9. Test: `configure_timetravel` with no backend URI does not create a backend
