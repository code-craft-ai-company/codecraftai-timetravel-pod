# F3.2 — TimeTravelPortal: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/automojo/timetravel/pod/portal.py`
- [x] 2. Implement `TimeTravelPortal.__init__` with name, activated flag, hook manager reference
- [x] 3. Implement `__enter__` — gateway check, nested check, activation check, tracing setup
- [x] 4. Implement `__exit__` — nested depth decrement or full teardown with hook uninstall, flush, state reset
- [x] 5. Implement inner portal annotation (PortalEnterEvent/PortalExitEvent) guarded by configuration
- [x] 6. Export public symbols from the module

## Testing Tasks

- [x] 7. Create test file `source/tests/automojo/timetravel/pod/test_portal.py`
- [x] 8. Test: entering an activated portal on a clean thread activates tracing
- [x] 9. Test: entering an inactive portal is a no-op (no tracing state change)
- [x] 10. Test: entering a portal when gateway is not active is a no-op
- [x] 11. Test: nested portals increment/decrement depth without installing multiple hooks
- [x] 12. Test: with `record_inner_portals=True`, PortalEnterEvent and PortalExitEvent are emitted for nested portals
- [x] 13. Test: with `record_inner_portals=False`, no annotation events for nested portals
- [x] 14. Test: exiting the outermost portal resets tracing state
- [x] 15. Test: exceptions propagate through the portal after cleanup
