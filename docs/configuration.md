# Configuration Guide

This document describes how to configure the FHIR Query Validator Factory for different environments and servers, including public test servers and authenticated/protected servers.

## 1. Overview

The system is designed to be **configuration-driven**. You can switch between different FHIR servers (public or protected) without changing code by using environment variables or configuration files.

Configuration is primarily handled through:
- `.env` files (recommended for local development)
- Environment variables (recommended for deployment)

## 2. Environment Variables

| Variable                        | Description                                                                 | Example                              | Required |
|--------------------------------|-----------------------------------------------------------------------------|--------------------------------------|----------|
| `FHIR_DEFAULT_SERVER_KEY`      | Default server key to use when none is specified                            | `hapi`                               | Yes      |
| `FHIR_SERVER_BASE`             | Base URL of the FHIR server (can be overridden by `server_key`)             | `https://hapi.fhir.org/baseR4`       | Yes      |
| `FHIR_METADATA_URL`            | URL to fetch the CapabilityStatement (usually `{base}/metadata`)            | `https://hapi.fhir.org/baseR4/metadata` | No     |
| `FHIR_USE_AUTH`                | Whether to use authentication (`true` / `false`)                            | `false`                              | Yes      |
| `FHIR_AUTH_TYPE`               | Authentication type (`bearer` or `oauth2`)                                  | `bearer`                             | No       |
| `FHIR_AUTH_TOKEN`              | Static Bearer token (for simple cases)                                      | `eyJhbGciOi...`                      | No       |
| `OAUTH_CLIENT_ID`              | Client ID for OAuth2 client credentials flow                                | `my-client-id`                       | No       |
| `OAUTH_CLIENT_SECRET`          | Client secret for OAuth2                                                    | `my-secret`                          | No       |
| `OAUTH_TOKEN_URL`              | Token endpoint URL for OAuth2                                               | `https://auth.example.com/token`     | No       |
| `OAUTH_SCOPE`                  | OAuth2 scope (optional)                                                     | `fhir.read`                          | No       |

## 3. Supported Public Test Servers

The following servers are supported out of the box via `server_key`:

| server_key   | Server Name       | Base URL                                      | Auth Required | Notes |
|--------------|-------------------|-----------------------------------------------|---------------|-------|
| `hapi`       | HAPI FHIR         | https://hapi.fhir.org/baseR4                  | No            | Default |
| `firely`     | Firely            | https://server.fire.ly/R4                     | No            | - |
| `spark`      | Spark             | https://spark.fhir.org/r4                     | No            | - |
| `wildfhir`   | WildFHIR          | https://wildfhir4.wildfhir.org/r4             | No            | - |

You can add more servers by extending the configuration.

## 4. Authentication Workflow

### Public Servers (No Auth)
- Set `FHIR_USE_AUTH=false`
- No additional credentials needed

### Authenticated Servers

#### Option A: Static Bearer Token
```env
FHIR_USE_AUTH=true
FHIR_AUTH_TYPE=bearer
FHIR_AUTH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Option B: OAuth2 Client Credentials Flow
```env
FHIR_USE_AUTH=true
FHIR_AUTH_TYPE=oauth2
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
OAUTH_TOKEN_URL=https://auth.example.com/oauth2/token
OAUTH_SCOPE=fhir.read
```

The system will automatically obtain and refresh access tokens when needed.

## 5. Example `.env.local` File

```env
# Default server
FHIR_DEFAULT_SERVER_KEY=hapi

# Public HAPI server (default)
FHIR_SERVER_BASE=https://hapi.fhir.org/baseR4
FHIR_USE_AUTH=false

# Example: Authenticated server
# FHIR_DEFAULT_SERVER_KEY=my-protected-server
# FHIR_SERVER_BASE=https://fhir.example.com/R4
# FHIR_USE_AUTH=true
# FHIR_AUTH_TYPE=oauth2
# OAUTH_CLIENT_ID=abc123
# OAUTH_CLIENT_SECRET=secret456
# OAUTH_TOKEN_URL=https://auth.example.com/token
```

## 6. Switching Servers at Runtime

You can override the default server by passing `server_key` in the request:

```python
result = validator.validate(
    query_url="Patient?gender=male",
    server_key="firely"
)
```

## 7. Security Considerations

- Never commit real credentials or tokens to version control.
- Use `.env.local` (which should be git-ignored) for local secrets.
- For production, prefer environment variables or secret managers (e.g., Google Secret Manager, AWS Secrets Manager).
- When using OAuth2, prefer short-lived tokens and implement proper token refresh logic.

## 8. Related Files (from original repository)

- `config/.env.example`
- `docs/public-test-servers.md`
- `docs/configuration.md` (original)

Refer to the original `yogesh-parte/fhirqueryvalidator` repository for the baseline implementation patterns.
