# F2.3 — Unix Socket Stream Backend: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/ccai/timetravel/pod/backends/unixbackend.py`
- [x] 2. Implement `UnixStreamBackend.__init__` with socket path and retry settings
- [x] 3. Implement `_connect()`, `_reconnect()`, `write()`, `close()`

## Testing Tasks

- [x] 4. Create test file `source/tests/ccai/timetravel/pod/backends/test_unixbackend.py`
- [x] 5. Test: successful connection and write to a local Unix socket server
- [x] 6. Test: reconnection is attempted on connection loss
- [x] 7. Test: after max retries, data is dropped without exception
- [x] 8. Test: `close()` cleans up the socket
- [x] 9. Test: connection to non-existent socket path raises `ConnectionError` or `OSError`
