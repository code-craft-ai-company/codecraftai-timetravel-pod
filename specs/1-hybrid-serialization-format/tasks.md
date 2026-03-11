# F1.3 — Hybrid Serialization Format: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/automojo/timetravel/pod/traceserializer.py`
- [x] 2. Define the `ENVELOPE_FORMAT` and `ENVELOPE_SIZE` constants
- [x] 3. Implement `TraceSerializer.__init__` with pre-compiled `struct.Struct`
- [x] 4. Implement `TraceSerializer._extract_payload` with per-event-type payload mapping
- [x] 5. Implement `TraceSerializer._extract_filename` and `_extract_lineno` helpers
- [x] 6. Implement `TraceSerializer.serialize` — pack envelope + filename + pickle payload
- [x] 7. Implement `TraceDeserializer.__init__` with pre-compiled `struct.Struct`
- [x] 8. Implement `TraceDeserializer.deserialize` — unpack envelope, decode filename, unpickle payload, reconstruct event
- [x] 9. Implement `TraceDeserializer._reconstruct_event` with per-event-type reconstruction
- [x] 10. Implement `TraceDeserializer.read_header` for header-only reads
- [x] 11. Implement `TraceDeserializer.skip_event` for fast scanning
- [x] 12. Export public symbols from the module

## Testing Tasks

- [x] 13. Create test file `source/tests/automojo/timetravel/pod/test_traceserializer.py`
- [x] 14. Test: `CallEvent` round-trips through serialize → deserialize with all fields preserved
- [x] 15. Test: `ReturnEvent` round-trips correctly, including `return_value`
- [x] 16. Test: `LineEvent` produces a zero-length payload
- [x] 17. Test: `VariableSnapshotEvent` preserves local variables dict
- [x] 18. Test: `ExceptionEvent` preserves exception details
- [x] 19. Test: `PortalEnterEvent` and `PortalExitEvent` preserve portal names
- [x] 20. Test: `GatewayStartEvent` and `GatewayStopEvent` preserve wall clock time
- [x] 21. Test: `read_header` returns correct envelope fields without deserializing payload
- [x] 22. Test: `skip_event` advances offset to the next event in a multi-event buffer
- [x] 23. Test: envelope size is exactly 29 bytes
