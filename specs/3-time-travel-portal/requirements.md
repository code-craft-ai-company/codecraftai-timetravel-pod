# F3.2 — TimeTravelPortal: Requirements

## Overview
Provide the named portal context manager that developers embed in their code. When a thread enters
an activated portal and the gateway is active, tracing begins. Only the outermost portal on a thread
activates tracing; nested portals optionally record annotation events.

## User Stories

### US-1: Scoped Tracing
As a developer, I want to wrap code sections in named portals so that tracing is limited to specific
areas of interest.

### US-2: Nested Portal Handling
As a developer, I want nested portals to be transparent when the outer portal is already tracing, with
optional annotation events for the inner portal boundaries.

### US-3: No-Op When Inactive
As a developer, I want portals that are not activated to have near-zero overhead so that production code
runs at full speed when debugging is not needed.

## Requirements (EARS Notation)

### REQ-3.2.1
The system shall provide a `TimeTravelPortal` context manager class implementing `__enter__` and `__exit__`,
accepting a `name: str` at construction.

### REQ-3.2.2
WHEN `__enter__` is called AND the gateway is active AND the portal name is activated AND the current
thread is not already tracing, THE portal SHALL install the trace hook and start a trace recorder.

### REQ-3.2.3
WHEN `__enter__` is called AND the current thread is already tracing (nested portal), THE portal SHALL
increment the portal depth and, if `record_inner_portals` is enabled, emit a `PortalEnterEvent`.

### REQ-3.2.4
WHEN `__enter__` is called AND the gateway is not active OR the portal name is not activated, THE portal
SHALL be a no-op.

### REQ-3.2.5
WHEN `__exit__` is called AND this portal instance activated tracing, THE portal SHALL uninstall the trace
hook, flush the recorder, and reset the thread-local tracing state.

### REQ-3.2.6
WHEN `__exit__` is called for a nested portal, THE portal SHALL decrement the portal depth and, if
`record_inner_portals` is enabled, emit a `PortalExitEvent`.

### REQ-3.2.7
The `TimeTravelPortal` SHALL NOT use the `contextlib.contextmanager` decorator.

### REQ-3.2.8
IF an exception occurs within the portal scope, THE portal SHALL still perform cleanup before re-raising.

## Acceptance Criteria

- AC-1: Entering an activated portal on a clean thread starts tracing.
- AC-2: Entering an inactive portal is a no-op with minimal overhead.
- AC-3: Nested portals increment/decrement depth without installing multiple hooks.
- AC-4: Exiting the outermost portal stops tracing and flushes the recorder.
- AC-5: Exceptions propagate after portal cleanup.
