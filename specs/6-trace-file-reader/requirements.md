# F6.1 — Trace File Reader: Requirements

## Overview
Provide a reader that deserializes trace files (or streams) back into `TraceEvent` objects for
offline analysis. This is the complement to the serializer and stream backends.

## User Stories

### US-1: Offline Analysis
As a developer, I want to read a trace file and iterate over the events it contains so that I can
analyze traced execution after the fact.

### US-2: Selective Reading
As a developer, I want to scan event headers without deserializing payloads so that I can quickly
filter events by type, timestamp, or thread before committing to full deserialization.

## Requirements (EARS Notation)

### REQ-6.1.1
The system shall provide a `TraceFileReader` class that opens a trace file and yields `TraceEvent`
objects by iterating over the serialized records.

### REQ-6.1.2
The `TraceFileReader` shall support reading from file paths and from `io.BytesIO` objects.

### REQ-6.1.3
The `TraceFileReader` shall support header-only scanning via a `scan_headers()` method that yields
envelope tuples without deserializing payloads.

### REQ-6.1.4
The `TraceFileReader` shall be usable as a context manager for automatic file handle cleanup.

### REQ-6.1.5
The `TraceFileReader` shall handle rotated trace files by accepting a list of file paths.

## Acceptance Criteria

- AC-1: Reading a file written by the serializer reproduces the original events.
- AC-2: `scan_headers()` returns envelope data without pickle deserialization.
- AC-3: The reader cleans up file handles on exit.
