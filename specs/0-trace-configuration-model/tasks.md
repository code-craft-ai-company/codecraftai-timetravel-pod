# F0.2 — Trace Configuration Model: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/ccai/timetravel/pod/traceconfiguration.py`
- [x] 2. Implement the `TraceConfiguration` class with `__slots__`, private backing fields, and read-only properties
- [x] 3. Implement `as_dict()` conversion method
- [x] 4. Implement `from_dict()` classmethod for deserialization
- [x] 5. Define the `DEFAULT_TRACE_CONFIGURATION` module-level constant
- [x] 6. Export public symbols from the module

## Testing Tasks

- [x] 7. Create test file `source/tests/ccai/timetravel/pod/test_traceconfiguration.py`
- [x] 8. Test: default construction yields `trace_calls=True`, all others `False`
- [x] 9. Test: explicit construction with all flags set preserves values
- [x] 10. Test: properties are read-only (setting raises `AttributeError`)
- [x] 11. Test: `as_dict()` returns correct dictionary
- [x] 12. Test: `from_dict()` round-trips with `as_dict()`
- [x] 13. Test: `from_dict()` with partial data uses defaults for missing keys
