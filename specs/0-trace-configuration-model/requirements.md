# F0.2 — Trace Configuration Model: Requirements

## Overview
Provide a configuration model that specifies the tracing granularity and behavioral options for the time travel
debugging system.  The configuration controls what types of trace events are captured and whether nested portal
boundaries are recorded.

## User Stories

### US-1: Configurable Trace Granularity
As a developer, I want to control the granularity of tracing (call/return only, line-level, or variable
snapshots) so that I can balance the level of debug detail against performance overhead.

### US-2: Inner Portal Annotation Control
As a developer, I want to configure whether inner (nested) portal entry/exit events are recorded in the trace
data so that I can reduce noise when I only care about the outermost portal scope.

### US-3: Runtime Reconfiguration
As a developer, I want the trace configuration to be updateable at runtime (via the remote control interface)
so that I can adjust granularity without restarting the application.

## Requirements (EARS Notation)

### REQ-0.2.1
The system shall provide a `TraceConfiguration` model with boolean fields controlling each trace granularity level:
`trace_calls`, `trace_lines`, `trace_variables`.

### REQ-0.2.2
The `TraceConfiguration` model shall provide a boolean field `record_inner_portals` that controls whether
nested portal entry/exit annotations are recorded.

### REQ-0.2.3
WHEN no explicit configuration is provided, THE system SHALL use a default configuration with `trace_calls`
enabled and `trace_lines`, `trace_variables`, and `record_inner_portals` disabled.

### REQ-0.2.4
The `TraceConfiguration` model shall be representable as a dictionary for serialization and deserialization.

### REQ-0.2.5
The `TraceConfiguration` model shall be immutable after creation to prevent unintended modification during
active tracing. A new configuration instance is created for updates.

## Acceptance Criteria

- AC-1: A `TraceConfiguration` constructed with defaults has `trace_calls=True` and all other flags `False`.
- AC-2: All granularity fields are boolean and independently controllable.
- AC-3: `as_dict()` returns a dictionary representation; `from_dict()` reconstructs the configuration.
- AC-4: Attempting to modify a field after construction raises an error or is prevented.
