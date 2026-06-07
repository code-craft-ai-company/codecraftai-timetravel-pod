# F0.4 — Trace Event Model: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/ccai/timetravel/pod/traceevents.py`
- [x] 2. Implement the `EventType` class with integer constants for all event types
- [x] 3. Implement the `TraceEvent` base class with `__slots__` and common fields
- [x] 4. Implement `CallEvent`, `ReturnEvent`, `LineEvent`, `VariableSnapshotEvent`
- [x] 5. Implement `ExceptionEvent` for exception propagation capture
- [x] 6. Implement `PortalEnterEvent`, `PortalExitEvent`
- [x] 7. Implement `GatewayStartEvent`, `GatewayStopEvent`
- [x] 8. Export public symbols from the module

## Testing Tasks

- [x] 9. Create test file `source/tests/ccai/timetravel/pod/test_traceevents.py`
- [x] 10. Test: each concrete event class is constructible with documented fields
- [x] 11. Test: each event type has the correct `event_type` integer tag
- [x] 12. Test: all `EventType` constants are unique integers
- [x] 13. Test: base `TraceEvent` fields (`timestamp_ns`, `thread_id`) are set correctly
- [x] 14. Test: `__slots__` prevents arbitrary attribute addition on event instances
- [x] 15. Test: `ExceptionEvent` stores exception type, value, and traceback as strings
