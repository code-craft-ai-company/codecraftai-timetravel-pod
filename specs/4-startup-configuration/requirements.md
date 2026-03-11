# F4.1 — Startup Configuration: Requirements

## Overview
Provide a high-level configuration API that applications use to bootstrap the time travel pod, accepting
all configuration parameters in one place and initializing the necessary components.

## User Stories

### US-1: Single Point of Configuration
As a developer, I want to configure the time travel pod with one function call, specifying portal names,
trace granularity, output destination, and remote control settings.

### US-2: CLI-Driven Activation
As a developer, I want to pass portal names from command-line arguments to the startup configuration so
that I can activate portals without modifying code.

## Requirements (EARS Notation)

### REQ-4.1.1
The system shall provide a `TimeTravelConfig` dataclass that holds all startup configuration:
active portal names, trace configuration, backend URI, record inner portals flag, and remote settings.

### REQ-4.1.2
The system shall provide a `configure_timetravel(config: TimeTravelConfig)` function that initializes
the portal registry, creates the stream backend, and optionally starts the remote control server.

### REQ-4.1.3
WHEN `configure_timetravel` is called with active portal names, THE system SHALL activate those portals
in the `PortalRegistry`.

### REQ-4.1.4
The `TimeTravelConfig` shall be serializable to and from a dictionary for configuration file support.

### REQ-4.1.5
WHEN no backend URI is specified, THE system SHALL default to no output (tracing is armed but produces
no data until a backend is configured at runtime via the remote).

## Acceptance Criteria

- AC-1: Calling `configure_timetravel` with portal names activates them in the registry.
- AC-2: A backend URI results in a stream backend being created and ready for use.
- AC-3: `TimeTravelConfig` round-trips through `as_dict()` / `from_dict()`.
