# F0.3 — Timestamp and Clock Abstraction: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/ccai/timetravel/pod/traceclock.py`
- [x] 2. Implement the `TraceClock` class with `start()`, `stop()`, `timestamp()`, and `is_running`
- [x] 3. Create the module-level singleton `_trace_clock` and `get_trace_clock()` accessor
- [x] 4. Export public symbols from the module

## Testing Tasks

- [x] 5. Create test file `source/tests/ccai/timetravel/pod/test_traceclock.py`
- [x] 6. Test: `timestamp()` before `start()` raises `RuntimeError`
- [x] 7. Test: after `start()`, `timestamp()` returns a non-negative integer
- [x] 8. Test: two successive `timestamp()` calls return non-decreasing values
- [x] 9. Test: after `stop()`, `timestamp()` raises `RuntimeError` again
- [x] 10. Test: `is_running` reflects clock state correctly
- [x] 11. Test: `get_trace_clock()` returns the same instance on repeated calls
