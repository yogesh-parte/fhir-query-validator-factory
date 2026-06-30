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
- Per-server API keys (e.g. `MOCK_HEALTH_API_KEY` for `mockhealth`) are resolved at request time from `.env.local`
- Cache entries should be keyed including auth context when relevant (to avoid leaking data across users)

## 5. Invalidation Strategy (Hybrid)

1. **Primary**: Time-based TTL (default 7 days, configurable per server)
2. **Secondary**: Conditional requests using ETag / `If-None-Match` (304 Not Modified) — **implemented** in `cache_agent.py`; `Last-Modified` / `If-Modified-Since` deferred
3. **Force refresh**: Via configuration or admin signal (`FHIR_CACHE_INVALIDATE`, `FHIR_CACHE_INVALIDATE_KEYS`)

## 6. Acceptance Criteria

- [ ] Works with both public and authenticated servers
- [ ] Correctly implements hybrid invalidation
- [ ] Logs cache decisions (hit/miss/refresh/304)
- [ ] Respects authentication when fetching from protected servers
