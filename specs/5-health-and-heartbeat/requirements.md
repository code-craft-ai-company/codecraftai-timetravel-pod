# F5.4 — Health and Heartbeat: Requirements

## Overview
Provide a periodic heartbeat mechanism from the application to the debugging service so the service
knows the application instance is alive and reachable.

## User Stories

### US-1: Liveness Detection
As an operations engineer, I want the debugging service to know which registered application instances
are still alive so that stale entries can be identified.

## Requirements (EARS Notation)

### REQ-5.4.1
The system shall provide a `HeartbeatSender` class that sends periodic heartbeat requests to the
debugging service.

### REQ-5.4.2
The heartbeat SHALL run in a daemon background thread and send a request at a configurable interval.

### REQ-5.4.3
The heartbeat request SHALL include the instance ID and a timestamp.

### REQ-5.4.4
IF a heartbeat request fails, THE system SHALL log the failure and continue with the next interval.

### REQ-5.4.5
The `HeartbeatSender` shall provide `start()` and `stop()` methods for lifecycle management.

### REQ-5.4.6
The default heartbeat interval SHALL be 30 seconds.

## Acceptance Criteria

- AC-1: After `start()`, heartbeat requests are sent at the configured interval.
- AC-2: `stop()` terminates the heartbeat thread.
- AC-3: Failed heartbeat requests do not crash the application.
