# F2.4 — Stream Backend Registry: Requirements

## Overview
Provide a registry and factory that resolves stream backends by URI scheme, enabling the startup
configuration to specify backends using simple URI strings.

## User Stories

### US-1: URI-Based Backend Selection
As a developer, I want to specify a trace output destination as a URI string (e.g., `file:///tmp/trace.bin`)
so that backend selection is simple and uniform.

## Requirements (EARS Notation)

### REQ-2.4.1
The system shall provide a `StreamBackendRegistry` that maps URI schemes to backend factory functions.

### REQ-2.4.2
The registry SHALL support the built-in schemes: `file`, `tcp`, `unix`.

### REQ-2.4.3
The system shall provide a `create_backend(uri: str)` function that parses the URI, looks up the
scheme in the registry, and returns an initialized stream backend instance.

### REQ-2.4.4
IF an unknown URI scheme is provided, THEN THE `create_backend` function SHALL raise a `ValueError`.

### REQ-2.4.5
The registry SHALL support registration of custom backend factories via `register(scheme, factory)`.

## Acceptance Criteria

- AC-1: `create_backend("file:///tmp/trace.bin")` returns a `FileStreamBackend` instance.
- AC-2: `create_backend("tcp://localhost:9090")` returns a `TcpStreamBackend` instance.
- AC-3: `create_backend("unix:///var/run/trace.sock")` returns a `UnixStreamBackend` instance.
- AC-4: Unknown scheme raises `ValueError`.
- AC-5: Custom factories can be registered and used.
