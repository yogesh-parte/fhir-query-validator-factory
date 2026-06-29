# Spec: QueryExecution Agent

**Status:** Draft  
**Version:** 0.2  
**Last Updated:** 2026-06-28  
**Related Specs:** query-validation-spec.md

## 1. Overview

The `QueryExecution Agent` executes FHIR search queries against the target server **only after** successful validation. It supports both public and authenticated servers.

## 2. Goals

- Execute validated queries reliably on public and protected servers
- Handle authentication headers/tokens when required
- Return structured results or clear errors

## 3. Authentication Support

- For public servers: No authentication headers
- For protected servers: Forward `Authorization: Bearer <token>` header passed from configuration or upstream
- Should support token refresh mechanisms if configured at the application level

## 4. Acceptance Criteria

- [ ] Successfully executes queries on public test servers (HAPI, Firely, etc.)
- [ ] Correctly passes authentication headers for protected servers
- [ ] Returns structured success/error responses
- [ ] Logs execution outcome and timing
