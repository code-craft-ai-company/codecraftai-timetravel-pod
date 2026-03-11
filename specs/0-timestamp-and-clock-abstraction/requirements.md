# F0.3 — Timestamp and Clock Abstraction: Requirements

## Overview
Provide a monotonic clock wrapper that supplies high-resolution timestamps for all trace events. Timestamps are
recorded relative to the gateway start time so that traced data can later be plotted onto a timeline.

## User Stories

### US-1: High-Resolution Timestamps
As a developer, I want trace events to carry high-resolution timestamps so that I can distinguish the ordering of
closely-spaced events.

### US-2: Relative Timeline
As a developer, I want all timestamps to be relative to the gateway start so that I can plot events on a unified
timeline that begins at zero.

## Requirements (EARS Notation)

### REQ-0.3.1
The system shall provide a `TraceClock` class that wraps `time.perf_counter_ns()` to produce monotonic,
high-resolution timestamps in nanoseconds.

### REQ-0.3.2
WHEN the `TraceClock` is started, THE system SHALL record the origin timestamp and all subsequent timestamp
calls SHALL return nanosecond offsets relative to that origin.

### REQ-0.3.3
The `TraceClock` shall provide a `timestamp()` method that returns the current offset from the origin
as an integer number of nanoseconds.

### REQ-0.3.4
IF `timestamp()` is called before the clock has been started, THEN THE system SHALL raise a `RuntimeError`.

### REQ-0.3.5
The `TraceClock` shall be usable as a singleton — one clock per process, set when the gateway is entered.

## Acceptance Criteria

- AC-1: Two successive calls to `timestamp()` return non-decreasing values.
- AC-2: The first call to `timestamp()` after `start()` returns a value >= 0.
- AC-3: Calling `timestamp()` before `start()` raises `RuntimeError`.
- AC-4: Timestamps are integers (nanoseconds), not floats.
