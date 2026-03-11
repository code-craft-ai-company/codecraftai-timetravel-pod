# F2.1 — File Stream Backend: Requirements

## Overview
Provide a stream backend that writes serialized trace data to a file on disk, supporting configurable
file paths and optional size-based rotation.

## User Stories

### US-1: Local Trace Capture
As a developer, I want to write trace data to a local file so that I can analyze it offline after the
tracing session ends.

### US-2: Size-Based Rotation
As a developer, I want trace files to automatically rotate when they reach a configurable size so that
individual files remain manageable and disk usage is bounded.

## Requirements (EARS Notation)

### REQ-2.1.1
The system shall provide a `FileStreamBackend` class that opens a file at a configurable path and
implements `write(data: bytes)` and `close()`.

### REQ-2.1.2
The `FileStreamBackend` shall open the file in binary write mode (`"wb"`) for new traces or binary
append mode (`"ab"`) if configured to append to an existing file.

### REQ-2.1.3
WHERE size-based rotation is enabled, THE `FileStreamBackend` SHALL close the current file and open
a new file with an incremented suffix when the current file exceeds the configured maximum size.

### REQ-2.1.4
The rotation naming scheme SHALL use the pattern `{base_path}.{rotation_index}` where `rotation_index`
starts at 1 and increments.

### REQ-2.1.5
WHEN `close()` is called, THE `FileStreamBackend` SHALL flush and close the underlying file handle.

### REQ-2.1.6
The `FileStreamBackend` shall create parent directories if they do not exist.

## Acceptance Criteria

- AC-1: Writing data creates a file at the specified path.
- AC-2: With rotation enabled, exceeding the max size creates a new numbered file.
- AC-3: `close()` flushes and closes the file handle.
- AC-4: Parent directories are created automatically.
