# F5.3 — Service Registration: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/ccai/timetravel/pod/remote/registration.py`
- [x] 2. Implement `ServiceRegistration.__init__` with service URL, credentials, remote info
- [x] 3. Implement `register()` — send JSON POST to `/register` endpoint
- [x] 4. Implement `unregister()` — send JSON POST to `/unregister` endpoint
- [x] 5. Implement `_send_request()` helper with `urllib.request`

## Testing Tasks

- [x] 6. Create test file `source/tests/ccai/timetravel/pod/remote/test_registration.py`
- [x] 7. Test: `register()` sends correct payload (using mock HTTP server)
- [x] 8. Test: `unregister()` sends correct payload
- [x] 9. Test: registration failure is caught and returns `False`
- [x] 10. Test: `unregister()` is a no-op if not registered
- [x] 11. Test: instance_id is a valid UUID string
