# Spec: Generalized Query Validation

**Status:** Draft  
**Version:** 0.2  
**Last Updated:** 2026-06-28  
**Owner:** [Your Name]  
**Related ADRs:** ADR-001

## 1. Overview

This specification defines the expected behavior of the **generalized FHIR Query Validation** capability. 

The system should dynamically validate **any** search query against a FHIR server’s `CapabilityStatement`, support multiple public test servers, and handle both public and authenticated servers.

## 2. Goals

- Validate any resource type, search parameter, modifier, and comparator declared in the server’s `CapabilityStatement`.
- Support multiple public test servers out of the box (HAPI, Firely, Spark, WildFHIR, etc.).
- Support authenticated servers via configuration (OAuth / Bearer token).
- Provide clear, actionable error messages.
- Detect repeated invalid query patterns from the same user.
- Support both `validate_only` and `validate_and_execute` modes.

## 3. Inputs

| Input                    | Type          | Description                                                                 | Required |
|--------------------------|---------------|-----------------------------------------------------------------------------|----------|
| `query_url`              | string        | Full FHIR search query URL                                                  | Yes      |
| `server_key`             | string        | Logical key for the target server (e.g., `hapi`, `firely`)                  | Yes      |
| `user_id` (optional)     | string        | Identifier for pattern tracking and personalization                         | No       |
| `mode`                   | enum          | `validate_only` or `validate_and_execute`                                   | Yes      |
| `auth_token` (optional)  | string        | Bearer token or OAuth token for authenticated servers                       | No       |

## 4. Supported Public Test Servers (Default)

The system should support the following public servers by default (via configuration):

- **HAPI FHIR** (`hapi`)
- **Firely** (`firely`)
- **Spark** (`spark`)
- **WildFHIR** (`wildfhir`)

Configuration is driven by environment variables or a config file.

## 5. Authentication & Configuration

- Public servers: No authentication required.
- Protected servers: Support for Bearer token or OAuth2 client credentials flow.
- Configuration is loaded from `.env` / `config/.env.local`.
- The system should allow switching between servers using a `server_key`.

See related documentation in the original repository:
- `docs/configuration.md`
- `docs/public-test-servers.md`

## 6. Outputs

```json
{
  "valid": true,
  "server_used": "hapi",
  "errors": [],
  "warnings": [],
  "executed": false,
  "results": null
}
```

## 7. Core Behavior

1. Resolve `server_key` to actual base URL and auth settings.
2. Fetch (or retrieve from cache) the server’s `CapabilityStatement` (respecting auth if needed).
3. Dynamically interpret supported resources, search parameters, modifiers, and comparators.
4. Validate the query.
5. If valid and `mode = validate_and_execute` → execute via QueryExecution Agent.
6. Handle pattern detection and escalation via Rule Agent.

## 8. Edge Cases & Error Handling

- Unknown `server_key`
- Missing or invalid authentication for protected servers
- CapabilityStatement not accessible due to auth issues
- Repeated invalid queries from the same user

## 9. Acceptance Criteria

- [ ] Supports switching between multiple public test servers via configuration
- [ ] Can authenticate against protected servers using Bearer token or OAuth
- [ ] Validates any parameter declared in the CapabilityStatement
- [ ] Pattern detection and escalation work across different servers
- [ ] Clear error messages when authentication fails

## 10. Open Questions

- Preferred OAuth flow for protected servers?
- Should we support multiple auth methods per server?
