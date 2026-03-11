# F6.2 — Timeline Reconstruction: Requirements

## Overview
Rebuild a chronological timeline of trace events from one or more trace sources, aligned to the
gateway start timestamp.

## User Stories

### US-1: Unified Timeline
As a developer, I want to merge events from multiple trace sources into a single chronological
timeline for analysis.

## Requirements (EARS Notation)

### REQ-6.2.1
The system shall provide a `TimelineBuilder` class that accepts events from one or more
`TraceFileReader` sources and produces a sorted list of `TraceEvent` objects.

### REQ-6.2.2
Events SHALL be sorted by `timestamp_ns` (ascending).

### REQ-6.2.3
WHEN events from different sources share the same `timestamp_ns`, THE system SHALL maintain
stable ordering (events from the same source appear in their original order).

### REQ-6.2.4
The `TimelineBuilder` shall support filtering by thread ID, event type, or time range
during reconstruction.

## Acceptance Criteria

- AC-1: Events from a single source are returned in timestamp order.
- AC-2: Events from multiple sources are merged into a single sorted timeline.
- AC-3: Filters reduce the returned events to only matching criteria.
