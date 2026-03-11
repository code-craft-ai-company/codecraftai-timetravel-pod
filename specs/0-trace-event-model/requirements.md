# F0.4 — Trace Event Model: Requirements

## Overview
Define the dataclass models representing individual trace events produced by the tracing system. These event
objects are the common currency between the trace hook manager, serializer, recorder, and reader components.

## User Stories

### US-1: Structured Event Data
As a developer building trace analysis tools, I want each trace event to be a well-typed object with known
fields so that I can reliably inspect and process events.

### US-2: Timeline Positioning
As a developer, I want every trace event to carry a timestamp offset so that events can be ordered and
positioned on a timeline.

### US-3: Thread Attribution
As a developer, I want every trace event to carry the thread ID of the thread that generated it so that
multi-threaded traces can be disaggregated.

## Requirements (EARS Notation)

### REQ-0.4.1
The system shall define a base `TraceEvent` class with common fields: `event_type` (int tag), `timestamp_ns`
(int), and `thread_id` (int).

### REQ-0.4.2
The system shall define a `CallEvent` with fields: `filename` (str), `lineno` (int), `function_name` (str),
`args` (tuple), `kwargs` (dict or None).

### REQ-0.4.3
The system shall define a `ReturnEvent` with fields: `filename` (str), `lineno` (int), `function_name` (str),
`return_value` (any).

### REQ-0.4.4
The system shall define a `LineEvent` with fields: `filename` (str), `lineno` (int).

### REQ-0.4.5
The system shall define a `VariableSnapshotEvent` with fields: `filename` (str), `lineno` (int),
`local_variables` (dict).

### REQ-0.4.6
The system shall define a `PortalEnterEvent` and `PortalExitEvent` with field: `portal_name` (str).

### REQ-0.4.7
The system shall define a `GatewayStartEvent` and `GatewayStopEvent` with field: `wall_clock_time` (float,
`time.time()` value for correlating with external logs).

### REQ-0.4.8
Each event type shall have a unique integer type tag for use in the struct serialization envelope.

### REQ-0.4.9
The system shall define an `EventType` enum (or integer constants module) mapping event type names to their
integer tags.

## Acceptance Criteria

- AC-1: All event classes are constructible with the documented fields.
- AC-2: Each event type has a distinct `event_type` integer value.
- AC-3: The `EventType` constants cover all defined event classes.
- AC-4: Events carry `timestamp_ns` and `thread_id` as base fields.
