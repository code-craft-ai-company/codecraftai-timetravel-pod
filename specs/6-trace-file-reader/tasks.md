# F6.1 — Trace File Reader: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/automojo/timetravel/pod/reader.py`
- [x] 2. Implement `TraceFileReader` with source handling (path, list, BytesIO)
- [x] 3. Implement `read_events()` generator
- [x] 4. Implement `scan_headers()` generator
- [x] 5. Implement context manager support

## Testing Tasks

- [x] 6. Create test file `source/tests/automojo/timetravel/pod/test_reader.py`
- [x] 7. Test: round-trip — serialize events to file, read back with reader, compare
- [x] 8. Test: `scan_headers()` returns envelope data without full deserialization
- [x] 9. Test: reading from `BytesIO` works correctly
- [x] 10. Test: reading rotated files (list of paths) concatenates events
- [x] 11. Test: context manager cleans up properly
