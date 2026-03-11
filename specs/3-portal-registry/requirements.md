# F3.3 — Portal Registry: Requirements

## Overview
Provide a thread-safe in-process registry that tracks portal names and their activation state. This
registry is queried by portals on entry and managed by the startup configuration and remote control
interface.

## User Stories

### US-1: Portal Activation Management
As a developer, I want a central registry to activate and deactivate portals by name so that I can
control which code sections are traced.

### US-2: Dynamic Runtime Changes
As a developer, I want to activate and deactivate portals at runtime so that I can start or stop
tracing specific areas without restarting the application.

## Requirements (EARS Notation)

### REQ-3.3.1
The system shall provide a `PortalRegistry` class with `activate_portal(name)` and
`deactivate_portal(name)` methods.

### REQ-3.3.2
The `PortalRegistry` shall provide `is_portal_active(name) -> bool` to check activation state.

### REQ-3.3.3
The `PortalRegistry` shall provide `list_portals() -> list[dict]` returning name and active status
for all known portals.

### REQ-3.3.4
The `PortalRegistry` shall provide bulk operations: `activate_portals(names)` and `deactivate_all()`.

### REQ-3.3.5
All `PortalRegistry` methods SHALL be thread-safe, using a lock for concurrent access.

### REQ-3.3.6
The system shall provide a module-level singleton registry accessible via `get_portal_registry()`.

## Acceptance Criteria

- AC-1: `activate_portal("x")` followed by `is_portal_active("x")` returns `True`.
- AC-2: `deactivate_portal("x")` followed by `is_portal_active("x")` returns `False`.
- AC-3: An unknown portal name returns `False` for `is_portal_active`.
- AC-4: Concurrent access from multiple threads does not corrupt state.
- AC-5: `deactivate_all()` clears all activations.
