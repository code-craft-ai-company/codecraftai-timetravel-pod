# F0.1 — Thread-Local Tracing State: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/automojo/timetravel/pod/tracingstate.py`
- [x] 2. Implement the `TracingState` class with fields: `is_tracing`, `recorder`, `portal_depth`, `active_portal_name` and a `reset()` method
- [x] 3. Create the module-level `threading.local()` instance `_thread_local`
- [x] 4. Implement the `get_tracing_state()` function with lazy initialization
- [x] 5. Implement the `_gateway_active` flag with `is_gateway_active()` and `set_gateway_active()` functions
- [x] 6. Export public symbols from the module

## Testing Tasks

- [x] 7. Create test file `source/tests/automojo/timetravel/pod/test_tracingstate.py`
- [x] 8. Test: default `TracingState` initialization has correct defaults
- [x] 9. Test: `get_tracing_state()` returns the same instance on repeated calls from the same thread
- [x] 10. Test: `get_tracing_state()` returns different instances for different threads
- [x] 11. Test: modifying state on one thread does not affect another thread
- [x] 12. Test: `reset()` restores all fields to defaults
- [x] 13. Test: `is_gateway_active()` defaults to `False`; `set_gateway_active(True)` makes it return `True`
