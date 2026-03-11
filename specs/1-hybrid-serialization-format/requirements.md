# F1.3 — Hybrid Serialization Format: Requirements

## Overview
Provide a zero-dependency serialization scheme that converts `TraceEvent` objects into a compact binary
representation using `struct` for fixed-size event envelopes and `pickle` protocol 5 for variable-size
object payloads.

## User Stories

### US-1: Fast Serialization
As a developer, I want trace events to be serialized with minimal overhead so that tracing does not
significantly degrade application performance.

### US-2: Fast Scanning
As a developer building trace analysis tools, I want to quickly scan through serialized events by reading
fixed-size headers without deserializing payloads, enabling efficient filtering and seeking.

### US-3: Full Object Fidelity
As a developer, I want function arguments, return values, and variable snapshots to be preserved with full
Python object fidelity so that I can inspect them exactly as they were at trace time.

## Requirements (EARS Notation)

### REQ-1.3.1
The system shall provide a `TraceSerializer` class that serializes `TraceEvent` objects into bytes using
a two-part format: a struct envelope followed by a pickle payload.

### REQ-1.3.2
The struct envelope SHALL contain: event type (1 byte, unsigned char), timestamp_ns (8 bytes, unsigned
long long), thread_id (8 bytes, unsigned long long), filename length (4 bytes, unsigned int),
lineno (4 bytes, unsigned int), payload length (4 bytes, unsigned int).

### REQ-1.3.3
The struct envelope SHALL be followed by the filename bytes (UTF-8 encoded), followed by the pickle
protocol 5 payload bytes.

### REQ-1.3.4
The pickle payload SHALL contain the event-specific data (arguments, return values, variable snapshots,
portal names, wall clock times) serialized using `pickle.dumps(data, protocol=5)`.

### REQ-1.3.5
The system shall provide a `TraceDeserializer` class that reads the binary format and reconstructs
`TraceEvent` objects.

### REQ-1.3.6
The `TraceDeserializer` shall support header-only reads for scanning (read envelope, skip payload).

### REQ-1.3.7
The serialization SHALL use only Python standard library modules (`struct`, `pickle`).

## Acceptance Criteria

- AC-1: A `TraceEvent` round-trips through serialize → deserialize with all fields preserved.
- AC-2: The struct envelope has a fixed size of 29 bytes (1 + 8 + 8 + 4 + 4 + 4).
- AC-3: Scanning by header-only reads correctly skips payloads.
- AC-4: No third-party imports are required.
