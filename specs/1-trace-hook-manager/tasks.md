# F1.1 — Trace Hook Manager: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/ccai/timetravel/pod/tracehookmanager.py`
- [x] 2. Implement `TraceHookManager.__init__` — cache config flags, clock, thread ID, record callback
- [x] 3. Implement `install()` and `uninstall()` methods wrapping `sys.settrace`
- [x] 4. Implement `_trace_function` — dispatch `call`, `return`, `line`, `exception` events
- [x] 5. Implement variable snapshot capture (shallow copy of `frame.f_locals`)
- [x] 6. Export public symbols from the module

## Testing Tasks

- [x] 7. Create test file `source/tests/ccai/timetravel/pod/test_tracehookmanager.py`
- [x] 8. Test: installing the hook and calling a function produces `CallEvent` and `ReturnEvent`
- [x] 9. Test: with `trace_lines=True`, executing code produces `LineEvent` objects
- [x] 10. Test: with `trace_lines=False`, no `LineEvent` objects are produced
- [x] 11. Test: with `trace_variables=True`, `VariableSnapshotEvent` contains local variable data
- [x] 12. Test: exceptions produce `ExceptionEvent` objects regardless of configuration
- [x] 13. Test: `uninstall()` stops all event production
- [x] 14. Test: events carry the correct thread ID
