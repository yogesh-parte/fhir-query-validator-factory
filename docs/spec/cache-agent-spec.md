# Spec: CacheAgent

**Status:** Draft  
**Version:** 0.2  
**Last Updated:** 2026-06-28  
**Related Specs:** query-validation-spec.md

## 1. Overview

The `CacheAgent` is responsible for efficiently managing `CapabilityStatement` resources from FHIR servers. It reduces repeated network calls, supports public and authenticated servers, and implements hybrid invalidation.

## 2. Goals

- Minimize latency and load on FHIR servers
- Support both public test servers and authenticated servers
- Implement hybrid invalidation (TTL + ETag/Last-Modified)
- Provide transparent cache behavior

## 3. Responsibilities

- Fetch CapabilityStatement (with optional authentication)
- Store with metadata (timestamp, ETag, auth context)
- Apply TTL and conditional header invalidation
- Serve from cache when valid
- Support conditional requests (`If-None-Match`, `If-Modified-Since`)

## 4. Authentication Support

- Public servers: No auth headers sent
- Authenticated servers: Accept and forward `Authorization` header (Bearer token) or handle OAuth token refresh if configured
- Cache entries should be keyed including auth context when relevant (to avoid leaking data across users)

## 5. Invalidation Strategy (Hybrid)

1. **Primary**: Time-based TTL (default 7 days, configurable per server)
2. **Secondary**: Conditional requests using ETag / Last-Modified
3. **Force refresh**: Via configuration or admin signal

## 6. Acceptance Criteria

- [ ] Works with both public and authenticated servers
- [ ] Correctly implements hybrid invalidation
- [ ] Logs cache decisions (hit/miss/refresh/304)
- [ ] Respects authentication when fetching from protected servers
