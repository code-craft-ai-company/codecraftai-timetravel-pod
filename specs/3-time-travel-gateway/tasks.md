# F3.1 — TimeTravelGateway: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/automojo/timetravel/pod/gateway.py`
- [x] 2. Implement `TimeTravelGateway.__init__` with configuration, backend URI, clock, recorder list
- [x] 3. Implement `__enter__` — start clock, set gateway active, emit `GatewayStartEvent`
- [x] 4. Implement `__exit__` — emit `GatewayStopEvent`, flush/close recorders, stop clock, clear flag
- [x] 5. Implement `register_recorder()` and `_broadcast_event()` helper methods
- [x] 6. Implement module-level `_active_gateway`, `get_active_gateway()`, `set_active_gateway()`
- [x] 7. Export public symbols from the module

## Testing Tasks

- [x] 8. Create test file `source/tests/automojo/timetravel/pod/test_gateway.py`
- [x] 9. Test: entering the gateway starts the clock and sets gateway-active flag
- [x] 10. Test: exiting the gateway stops the clock and clears gateway-active flag
- [x] 11. Test: `get_active_gateway()` returns the gateway inside the `with` block, `None` outside
- [x] 12. Test: exceptions inside the gateway propagate after cleanup
- [x] 13. Test: registered recorders are flushed and closed on gateway exit
- [x] 14. Test: `GatewayStartEvent` has `timestamp_ns=0`
