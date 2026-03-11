# F4.2 — Convenience Decorators: Requirements

## Overview
Provide optional convenience decorators and factory helpers that simplify common patterns of using
portals and gateways.

## User Stories

### US-1: Decorator-Based Portals
As a developer, I want a `@trace_portal("name")` decorator so that I can mark entire functions as
portal scopes without explicitly using `with` blocks.

### US-2: Quick Gateway Setup
As a developer, I want a factory function that creates a pre-configured gateway with sensible defaults
so that simple use cases require minimal boilerplate.

## Requirements (EARS Notation)

### REQ-4.2.1
The system shall provide a `@trace_portal(name)` decorator that wraps the decorated function's body
in a `TimeTravelPortal` context.

### REQ-4.2.2
The `@trace_portal` decorator SHALL preserve the decorated function's name, docstring, and signature
using `functools.wraps`.

### REQ-4.2.3
The system shall provide a `create_gateway(**kwargs)` factory function that creates a `TimeTravelGateway`
with common defaults and optional overrides.

### REQ-4.2.4
The `@trace_portal` decorator SHALL support both synchronous and asynchronous functions (using
`inspect.iscoroutinefunction` to detect async).

## Acceptance Criteria

- AC-1: A function decorated with `@trace_portal("x")` traces when portal "x" is active.
- AC-2: The decorated function's `__name__` and `__doc__` are preserved.
- AC-3: `create_gateway()` returns a usable `TimeTravelGateway` instance.
- AC-4: Async functions work correctly with `@trace_portal`.
