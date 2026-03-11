# F3.1 — TimeTravelGateway: Requirements

## Overview
Provide the main application gateway context manager that marks the timespan of the application,
starts the trace clock, and enables portal activation. The gateway must be entered before any
portals can trace.

## User Stories

### US-1: Application Timespan
As a developer, I want to wrap my application's main entry point in a gateway so that all trace
data is anchored to a common timeline starting at zero.

### US-2: Clean Shutdown
As a developer, I want the gateway to flush and close all active recorders and backends when the
application exits the gateway scope.

## Requirements (EARS Notation)

### REQ-3.1.1
The system shall provide a `TimeTravelGateway` context manager class implementing `__enter__`
and `__exit__`.

### REQ-3.1.2
WHEN the gateway is entered (`__enter__`), THE system SHALL start the `TraceClock`, set the
gateway-active flag to `True`, and emit a `GatewayStartEvent`.

### REQ-3.1.3
WHEN the gateway is exited (`__exit__`), THE system SHALL emit a `GatewayStopEvent`, flush and
close all active recorders, stop the `TraceClock`, and set the gateway-active flag to `False`.

### REQ-3.1.4
IF a portal attempts to activate tracing while the gateway is not active, THEN THE portal SHALL
not activate (no-op).

### REQ-3.1.5
The `TimeTravelGateway` SHALL accept a `TraceConfiguration` and a stream backend specification at
construction time.

### REQ-3.1.6
The `TimeTravelGateway` SHALL NOT use the `contextlib.contextmanager` decorator — it must be a class
with explicit `__enter__` and `__exit__` methods.

### REQ-3.1.7
IF an exception occurs within the gateway scope, THE gateway SHALL still perform cleanup (flush,
close, stop clock) before re-raising the exception.

## Acceptance Criteria

- AC-1: Entering the gateway starts the clock and sets the gateway-active flag.
- AC-2: Exiting the gateway stops the clock and clears the gateway-active flag.
- AC-3: `GatewayStartEvent` and `GatewayStopEvent` are emitted.
- AC-4: Exceptions propagate after cleanup.
- AC-5: The gateway is a class, not a `contextmanager`-decorated function.
