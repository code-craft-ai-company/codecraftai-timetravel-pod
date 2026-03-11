# F2.4 — Stream Backend Registry: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/automojo/timetravel/pod/backends/registry.py`
- [x] 2. Implement `StreamBackendRegistry` with `register()` and `create_backend()` methods
- [x] 3. Implement built-in factory functions for `file`, `tcp`, `unix` schemes
- [x] 4. Implement `create_default_registry()` function
- [x] 5. Export public symbols from the module

## Testing Tasks

- [x] 6. Create test file `source/tests/automojo/timetravel/pod/backends/test_registry.py`
- [x] 7. Test: `create_backend("file:///tmp/trace.bin")` returns a `FileStreamBackend`
- [x] 8. Test: `create_backend("tcp://localhost:9090")` returns a `TcpStreamBackend`
- [x] 9. Test: `create_backend("unix:///var/run/trace.sock")` returns a `UnixStreamBackend`
- [x] 10. Test: unknown scheme raises `ValueError`
- [x] 11. Test: custom factory registration works via `register()`
- [x] 12. Test: `create_default_registry()` has all three built-in schemes
