# F6.3 — Portal-Scoped Filtering: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/automojo/timetravel/pod/portalfilter.py`
- [x] 2. Implement `filter_by_portal(events, portal_name)` function

## Testing Tasks

- [x] 3. Create test file `source/tests/automojo/timetravel/pod/test_portalfilter.py`
- [x] 4. Test: filtering by inner portal name returns only events within enter/exit markers
- [x] 5. Test: multiple enter/exit pairs return events from all occurrences
- [x] 6. Test: events are returned in chronological order
- [x] 7. Test: filtering by a portal name that doesn't appear returns empty list
