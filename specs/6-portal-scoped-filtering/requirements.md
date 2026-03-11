# F6.3 — Portal-Scoped Filtering: Requirements

## Overview
Provide a filter that extracts events occurring within a specific named portal scope from a
reconstructed timeline.

## User Stories

### US-1: Focused Analysis
As a developer, I want to extract only the events that occurred within a specific portal so that
I can focus my analysis on a particular area of the code.

## Requirements (EARS Notation)

### REQ-6.3.1
The system shall provide a `PortalFilter` class or function that accepts a timeline (list of
`TraceEvent` objects) and a portal name, and returns only the events occurring between the
matching `PortalEnterEvent` and `PortalExitEvent` boundaries.

### REQ-6.3.2
WHEN events are produced by the outermost portal (which does not emit PortalEnter/Exit events),
THE filter SHALL use the thread-level tracing activation boundaries (first and last events on
that thread) as the scope.

### REQ-6.3.3
The filter SHALL support filtering across multiple enter/exit pairs for the same portal name
(the portal may be entered multiple times during an application run).

### REQ-6.3.4
The filter SHALL return events in their original chronological order.

## Acceptance Criteria

- AC-1: Filtering by an inner portal name returns only events between its enter/exit markers.
- AC-2: Multiple enter/exit pairs for the same portal return events from all occurrences.
- AC-3: Events are returned in timestamp order.
