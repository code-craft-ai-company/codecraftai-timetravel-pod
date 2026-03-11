# F2.3 — Unix Socket Stream Backend: Requirements

## Overview
Provide a stream backend that sends serialized trace data over a Unix domain socket for low-latency,
same-host trace collection.

## User Stories

### US-1: Low-Latency Local Streaming
As a developer, I want to stream trace data to a local collector through a Unix domain socket so that
I get lower latency and avoid TCP overhead for same-host collection.

## Requirements (EARS Notation)

### REQ-2.3.1
The system shall provide a `UnixStreamBackend` class that connects to a Unix domain socket at a
configurable path and implements `write(data: bytes)` and `close()`.

### REQ-2.3.2
IF the connection is lost during a write, THEN THE `UnixStreamBackend` SHALL attempt to reconnect
up to a configurable number of retries with exponential backoff.

### REQ-2.3.3
IF all reconnection attempts fail, THEN THE `UnixStreamBackend` SHALL log the failure and silently
drop the data.

### REQ-2.3.4
WHEN `close()` is called, THE `UnixStreamBackend` SHALL close the socket.

### REQ-2.3.5
IF the socket path does not exist at connection time, THEN THE `UnixStreamBackend` SHALL raise
a `ConnectionError`.

## Acceptance Criteria

- AC-1: Connecting to an existing Unix socket and writing data succeeds.
- AC-2: Reconnection is attempted on connection loss.
- AC-3: After max retries, data is dropped without exception.
- AC-4: `close()` closes the socket cleanly.
