# F5.1 — Remote Control Server: Tasks

## Implementation Tasks

- [x] 1. Create the `source/packages/ccai/timetravel/pod/remote/` package with `__init__.py`
- [x] 2. Create the module `source/packages/ccai/timetravel/pod/remote/server.py`
- [x] 3. Implement `RemoteControlServer.__init__` with host, port, credential
- [x] 4. Implement `start()` — socket setup, bind, listen, daemon thread creation
- [x] 5. Implement `stop()` — set running flag, close socket, join thread
- [x] 6. Implement `_serve_loop()` with accept, timeout, and shutdown checks
- [x] 7. Implement `_handle_client()` — receive, parse, dispatch, respond
- [x] 8. Implement `_dispatch()` with authentication check and command routing
- [x] 9. Implement command handlers: `list_portals`, `activate_portal`, `deactivate_portal`, `get_configuration`, `update_configuration`

## Testing Tasks

- [x] 10. Create test file `source/tests/ccai/timetravel/pod/remote/test_server.py`
- [x] 11. Test: server starts and accepts TCP connections
- [x] 12. Test: `list_portals` command returns portal data
- [x] 13. Test: `activate_portal` command activates a portal
- [x] 14. Test: `deactivate_portal` command deactivates a portal
- [x] 15. Test: authentication rejects requests with wrong token
- [x] 16. Test: unknown command returns error response
- [x] 17. Test: `stop()` cleanly shuts down the server
