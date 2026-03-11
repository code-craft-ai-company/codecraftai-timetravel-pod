# F5.1 — Remote Control Server: Requirements

## Overview
Provide an optional lightweight TCP server running in a background thread that exposes a JSON-lines
API for listing, activating, and deactivating portals, and querying/updating trace configuration at runtime.

## User Stories

### US-1: Dynamic Portal Control
As an operations engineer, I want to connect to a running application and activate or deactivate portals
without restarting it.

### US-2: Inspect Active State
As a developer, I want to query the current portal activation state and trace configuration of a running
application from an external tool.

## Requirements (EARS Notation)

### REQ-5.1.1
The system shall provide a `RemoteControlServer` class that runs a TCP server in a daemon background thread.

### REQ-5.1.2
The server SHALL accept JSON-lines messages (one JSON object per line) and respond with JSON-lines replies.

### REQ-5.1.3
The server SHALL support the following commands:
- `list_portals` — returns all portals and their activation state
- `activate_portal` — activates a portal by name
- `deactivate_portal` — deactivates a portal by name
- `get_configuration` — returns the current `TraceConfiguration` as a dict
- `update_configuration` — creates a new `TraceConfiguration` from provided fields

### REQ-5.1.4
The server SHALL bind to a configurable host and port.

### REQ-5.1.5
The server SHALL support a `stop()` method that shuts down the server and its background thread cleanly.

### REQ-5.1.6
The server SHALL use only Python standard library modules (`socket`, `json`, `threading`).

## Acceptance Criteria

- AC-1: A TCP client can connect, send a `list_portals` command, and receive a JSON response.
- AC-2: `activate_portal` and `deactivate_portal` commands change portal state.
- AC-3: The server runs in a background thread and does not block the main application.
- AC-4: `stop()` cleanly terminates the server.
