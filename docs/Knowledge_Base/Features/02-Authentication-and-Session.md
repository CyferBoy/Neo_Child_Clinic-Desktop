---
title: Authentication and Session
feature_id: AUTH
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base
updated: 2026-10-20
---

# 02. Authentication and Session

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `core/security/AuthViewModel.kt`, `core/security/CurrentUserProvider.kt`, `feature/auth/presentation/LoginScreen.kt`.
>
> **Shared backend:** sign-in must use the **existing** Supabase project's Auth users under [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]; no second identity store.

**Requirement IDs:** `AUTH-001`, `AUTH-002`, `AUTH-003`, `AUTH-004`, `AUTH-005`, `AUTH-006`

## 1. Purpose and scope

Authenticate staff with Supabase Auth, keep tokens outside the renderer, resolve the authorization role from app_metadata, and handle expiry, revocation, account switch, and offline cold start safely.

## 2. Actors

- All staff

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Sign in with email and password.
2. Restore a cached session on cold start and validate it.
3. Refresh an expiring access token.
4. Sign out with an unsynced-write warning.
5. Switch accounts without leaking the previous user's data.
6. Handle a deactivated account or missing role claim.
7. Re-authenticate for a sensitive action or app unlock.

## 5. UI states

| State | Expected behavior |
|---|---|
| Signing in | Disabled form, progress, no password echo. |
| Invalid credentials | Inline safe error; no account enumeration. |
| Loading session | Skeleton; no PHI until validation completes. |
| Session expired | Re-authenticate dialog; preserve local work. |
| Account deactivated | Block access; explain contact admin; clear PHI. |
| Missing role | Deny access with support reference; never default. |
| Offline | Cached session may allow offline work; sync pauses. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `AUTH-001` | Sign-in uses Supabase Auth and never stores the refresh token in renderer-accessible storage. | P0 |
| `AUTH-002` | The authorization role is read from validated app_metadata and never defaulted. | P0 |
| `AUTH-003` | Inactive, deleted, or revoked accounts cannot load PHI or refresh a session. | P0 |
| `AUTH-004` | Logout and account switch clear tokens, caches, and renderer state; pending writes require confirmation. | P0 |
| `AUTH-005` | Cold start offline is allowed only for a previously validated session with local data. | P1 |
| `AUTH-006` | Sensitive actions can require re-authentication without exposing credentials to the renderer. | P2 |

## 7. Validation and business rules

### Validation

- Email and password required.
- Email format checked before submit.
- No role supplied by the client is trusted.
- Session must be active and role-known before PHI loads.

### Business rules

- Role source is `app_metadata.role`, matching RLS.
- A missing/unknown role is a deny, not a default.
- Deactivation must revoke refresh capability.
- Account switching clears previous-user caches.
- Unsynced writes block silent sign-out.

## 8. Permissions

- All roles can sign in.
- Only active staff with a known role can enter the app.
- Admin cannot be impersonated in Phase 1.

## 9. Offline and data behavior

- Offline cold start uses a validated cached session and local data.
- Token refresh waits for network; sync pauses without dropping the outbox.
- A revoked session cannot be refreshed offline; when connectivity returns, access is denied.

## 10. Errors and recovery

- 401 -> refresh once, then re-authenticate.
- 403 -> permission/inactive message.
- Network timeout -> offline mode, not a false login failure.
- Keychain unavailable -> safe failure, do not fall back to plaintext.

## 11. Edge cases

- Expired refresh token.
- Revoked account while offline.
- System clock skew.
- Two accounts on one workstation.
- Password manager autofill.
- OS keychain locked.

## 12. Acceptance criteria

- [ ] Renderer storage and network inspection find no tokens.
- [ ] Missing role denies access.
- [ ] Deactivated account cannot refresh.
- [ ] Sign-out with pending writes requires confirmation.
- [ ] Account switch shows no previous patient data.
- [ ] Offline cold start never displays another user's cached data.

## 13. Test notes

- Integration: login/refresh/revoke/inactive/missing role.
- Security: inspect storage and network.
- E2E: cold start offline, account switch, logout warning.
- Fault: keychain unavailable.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

## 14. Dependencies

- [[Features/01-Desktop-Shell-and-Navigation|Shell]]
- [[Features/17-Supabase-Sync|Sync]]
- [[Decisions/ADR-0004-Authentication-and-Session|ADR-0004]]

## 15. Open questions

- Is OS biometric/Hello required?
- Idle timeout and re-auth policy?
- Device limits per staff account?
- Is SSO required?

## 16. Related

- [[Security/Security-Model|Security Model]]
- [[Security/Threat-Model|Threat Model]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
