# F0.1 — Thread-Local Tracing State: Requirements

## Overview
Provide a thread-local storage mechanism that tracks per-thread tracing state, enabling the portal and gateway
framework to determine whether a thread is currently inside an active portal and to access the active trace
recorder for that thread.

## User Stories

### US-1: Thread-Local State Isolation
As a developer using the time travel pod, I want each thread to maintain its own independent tracing state so that
concurrent threads can enter and exit portals without interfering with each other.

### US-2: Nested Portal Awareness
As a developer, I want the tracing state to track the nesting depth of portals so that only the outermost portal
activates tracing and inner portals are handled according to the trace configuration.

### US-3: Gateway Prerequisite
As a developer, I want the tracing state to know whether the gateway has been entered so that portals cannot
activate tracing before the gateway establishes the application timespan.

## Requirements (EARS Notation)

### REQ-0.1.1
The system shall provide a thread-local storage object that maintains tracing state independently for each thread.

### REQ-0.1.2
The thread-local tracing state shall track whether the current thread is inside an active (tracing) portal.

### REQ-0.1.3
The thread-local tracing state shall hold a reference to the active trace recorder for the current thread, or
None if no recorder is active.

### REQ-0.1.4
The thread-local tracing state shall track the portal nesting depth for the current thread as an integer,
starting at 0 when no portal has been entered.

### REQ-0.1.5
The thread-local tracing state shall track the name of the outermost active portal for the current thread.

### REQ-0.1.6
WHEN a thread first accesses the tracing state, THE system SHALL initialize all fields to their default
(inactive) values without requiring explicit setup.

### REQ-0.1.7
The system shall provide a module-level function to retrieve the thread-local tracing state for the
calling thread.

## Acceptance Criteria

- AC-1: Two threads accessing the tracing state concurrently maintain completely independent values.
- AC-2: Default state for a new thread shows: not tracing, no recorder, depth 0, no portal name.
- AC-3: Modifying tracing state on one thread does not affect any other thread's state.
- AC-4: The tracing state object is importable from the package's internal modules.
