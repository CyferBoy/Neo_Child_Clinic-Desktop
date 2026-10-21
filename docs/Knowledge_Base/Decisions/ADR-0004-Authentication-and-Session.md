---
title: ADR-0004 Authentication and Session
doc_status: proposed
evidence: Android auth reference + desktop threat model
updated: 2026-10-20
---

# ADR-0004 — Authentication and Session

**Status:** Proposed — awaiting approval.

## Context

Staff need individual accounts and role-aware access. The desktop renderer is an untrusted boundary. A stolen refresh token or a role guessed from local data would be a critical security failure.

## Decision

- Use Supabase Auth email/password as the baseline.
- Perform auth and token refresh in Go.
- Store the refresh token only in the OS keychain.
- Keep access tokens in Go memory; never expose them to the renderer.
- Read the authorization role from validated `app_metadata.role`; never default on missing/malformed values.
- On cold start, validate the account is active and the role exists before loading PHI.
- On logout/account switch, clear tokens, local caches, and renderer state; block/confirm if unsynced writes exist.
- Deactivation must revoke/ban refresh capability, not just hide UI.

## Alternatives considered

| Alternative | Assessment |
|---|---|
| Renderer stores tokens in localStorage | XSS token theft; rejected |
| Shared clinic login | Destroys accountability; rejected |
| Local password database | Duplicates identity; sync/revocation complexity |
| Role from `user_metadata` | Client-writable; rejected by reference design |
| Default to nurse on missing role | Silent privilege ambiguity; rejected |

## Consequences

Positive:
- Tokens are outside the renderer.
- Role source matches RLS.
- Account deactivation has a real effect.

Negative / risks:
- Keychain access differs by OS.
- Offline cold start requires a cached, validated session and local data.
- Re-auth flows add UX work.
- Staff account lifecycle depends on the admin edge function.

## Validation

- Renderer storage/network inspection finds no refresh/access token.
- Missing role -> denied, not defaulted.
- Deactivated account -> refresh fails, local PHI clears.
- Offline cold start with a valid cached session -> read-only/offline work; sync waits for auth.
- Sign-out with pending writes -> explicit confirmation.

## Open questions

- Is OS biometric/hello required for unlock?
- Session idle timeout and re-auth policy?
- Device registration/limit per staff?
- Is SSO required?

## Related

[[Security/Security-Model|Security Model]] · [[Security/Threat-Model|Threat Model]] · [[Features/02-Authentication-and-Session|Authentication]]
