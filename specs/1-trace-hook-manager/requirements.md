# F1.1 — Trace Hook Manager: Requirements

## Overview
Provide a wrapper around `sys.settrace` that installs and uninstalls a trace function on the current thread,
dispatching `call`, `return`, `line`, and `exception` trace events according to the active `TraceConfiguration`.

## User Stories

### US-1: Automatic Trace Capture
As a developer, I want the trace hook to automatically convert `sys.settrace` callbacks into structured
`TraceEvent` objects so that the rest of the system works with typed events, not raw trace tuples.

### US-2: Configurable Dispatch
As a developer, I want the trace hook to respect the `TraceConfiguration` so that only the event types I care
about are captured, reducing overhead for simpler trace modes.

## Requirements (EARS Notation)

### REQ-1.1.1
The system shall provide a `TraceHookManager` class that installs a trace function via `sys.settrace()` on the
current thread when `install()` is called.

### REQ-1.1.2
WHEN `uninstall()` is called, THE `TraceHookManager` SHALL call `sys.settrace(None)` to remove the trace
function from the current thread.

### REQ-1.1.3
WHILE `trace_calls` is enabled in the configuration, THE trace hook SHALL produce `CallEvent` objects for every
function call and `ReturnEvent` objects for every function return.

### REQ-1.1.4
WHILE `trace_lines` is enabled in the configuration, THE trace hook SHALL produce `LineEvent` objects for every
line executed.

### REQ-1.1.5
WHILE `trace_variables` is enabled in the configuration, THE trace hook SHALL produce `VariableSnapshotEvent`
objects capturing `frame.f_locals` at each traced line.

### REQ-1.1.6
The trace hook SHALL produce `ExceptionEvent` objects for `exception` trace events regardless of configuration,
as exception propagation is always significant for debugging.

### REQ-1.1.7
The trace hook SHALL obtain timestamps from the `TraceClock` and thread IDs from `threading.get_ident()`.

### REQ-1.1.8
The trace hook SHALL pass each produced `TraceEvent` to a callback function (the recorder's `record` method)
provided at construction time.

### REQ-1.1.9
The trace hook SHALL minimize per-event overhead by performing configuration checks using simple boolean tests
rather than method calls or dictionary lookups.

## Acceptance Criteria

- AC-1: Installing the hook and running code produces `CallEvent` and `ReturnEvent` objects.
- AC-2: With `trace_lines=False`, no `LineEvent` objects are produced.
- AC-3: With `trace_variables=True`, `VariableSnapshotEvent` objects include the local variables dict.
- AC-4: Exception events are always produced when an exception propagates through traced code.
- AC-5: Uninstalling the hook stops all event production.
