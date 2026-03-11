# F5.2 — Authentication and Credentials: Requirements

## Overview
Provide token-based authentication for the remote control server so that only authorized callers can
manage portals and trace configuration.

## User Stories

### US-1: Secure Remote Access
As an operations engineer, I want the remote control API to require authentication so that unauthorized
users cannot activate tracing on production applications.

## Requirements (EARS Notation)

### REQ-5.2.1
The remote control server SHALL accept a credential (string token) at construction time.

### REQ-5.2.2
WHEN a credential is configured, THE server SHALL reject any request that does not include a matching
`token` field in the JSON request body.

### REQ-5.2.3
WHEN no credential is configured, THE server SHALL accept all requests without authentication.

### REQ-5.2.4
The authentication mechanism SHALL use constant-time comparison to prevent timing attacks.

### REQ-5.2.5
Rejected requests SHALL receive a JSON error response with status `"error"` and message
`"Authentication failed"`.

## Acceptance Criteria

- AC-1: With a credential set, requests with the correct token succeed.
- AC-2: Requests with an incorrect token receive an authentication error.
- AC-3: With no credential set, all requests succeed regardless of token presence.
