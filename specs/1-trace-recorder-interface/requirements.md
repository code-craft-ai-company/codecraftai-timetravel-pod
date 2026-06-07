# F1.2 — Trace Recorder Interface: Requirements

## Overview
Define an abstract base class specifying the contract that all trace recorders must implement.
This enables pluggable recording strategies (file, socket, in-memory) behind a uniform interface.

## User Stories

### US-1: Pluggable Recording
As a developer, I want a common interface for trace recorders so that different recording backends
(file, socket, in-memory) can be swapped without changing portal or hook code.

## Requirements (EARS Notation)

### REQ-1.2.1
The system shall define an abstract `TraceRecorder` class with an abstract method `record(event: TraceEvent)`.

### REQ-1.2.2
The `TraceRecorder` shall define an abstract method `flush()` that forces all buffered data to be written
to the underlying stream.

### REQ-1.2.3
The `TraceRecorder` shall define an abstract method `close()` that finalizes the recorder and releases
any held resources (file handles, sockets).

### REQ-1.2.4
The `TraceRecorder` shall be importable from `ccai.timetravel.pod` internal modules and usable as
a type annotation for the record callback.

## Acceptance Criteria

- AC-1: `TraceRecorder` cannot be instantiated directly (abstract class).
- AC-2: Subclasses that do not implement all abstract methods cannot be instantiated.
- AC-3: A concrete subclass implementing all methods can be instantiated and used.
