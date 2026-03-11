# F6.2 — Timeline Reconstruction: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/automojo/timetravel/pod/timeline.py`
- [x] 2. Implement `TimelineBuilder` with `add_events()` and `build()`
- [x] 3. Implement filtering by thread_id, event_types, start_ns, end_ns

## Testing Tasks

- [x] 4. Create test file `source/tests/automojo/timetravel/pod/test_timeline.py`
- [x] 5. Test: events from a single source are returned sorted by timestamp
- [x] 6. Test: events from multiple sources merge into sorted timeline
- [x] 7. Test: thread_id filter returns only matching events
- [x] 8. Test: event_types filter returns only matching types
- [x] 9. Test: time range filter returns events within bounds
- [x] 10. Test: stable sort preserves source ordering for equal timestamps
