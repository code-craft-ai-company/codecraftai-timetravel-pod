# F4.2 — Convenience Decorators: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/ccai/timetravel/pod/decorators.py`
- [x] 2. Implement `trace_portal(name)` decorator with sync and async support
- [x] 3. Implement `create_gateway()` factory function
- [x] 4. Export public symbols from the module

## Testing Tasks

- [x] 5. Create test file `source/tests/ccai/timetravel/pod/test_decorators.py`
- [x] 6. Test: `@trace_portal("x")` on a sync function — function name and docstring preserved
- [x] 7. Test: decorated function executes normally
- [x] 8. Test: `@trace_portal("x")` on an async function works correctly
- [x] 9. Test: `create_gateway()` returns a `TimeTravelGateway` with correct defaults
- [x] 10. Test: `create_gateway()` with custom parameters creates correct configuration
