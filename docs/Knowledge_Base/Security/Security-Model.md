---
title: Security Model
doc_status: proposed
evidence: Android security register + shared-backend connection investigation + target architecture
updated: 2026-10-20
---

# Security Model

> **No desktop security control is implemented.** This is a target model. The Android security register is used as evidence of backend risks that the desktop will inherit unless they are fixed.

> **Accepted backend constraint `[DECISION]`:** Android and desktop must use the same existing Supabase project, PostgreSQL schema, Auth users, Storage buckets, and Edge Functions. No new project, separate desktop database, duplicate tables, or parallel schema is approved. See [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] and [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Connection Investigation]].

## Assets

- Patient identity, demographics, clinical notes, vaccination history, reminders, and documents.
- Staff identities, roles, contact details, and device registrations.
- Inventory quantities, batch costs, and stock movements.
- Payments, expenses, receipt numbers, and financial reports.
- Audit logs and backup files.
- Supabase session tokens and any local encryption keys.
- Application binaries and update metadata.

## Trust boundaries

| Boundary | Threat | Required control |
|---|---|---|
| Renderer → Go | Malicious/buggy UI input, XSS, prototype pollution | Typed validation, authorization re-check, no raw SQL/commands |
| Go → local DB | SQL injection, unsafe migrations, file tampering | Parameterized queries, embedded migrations, integrity checks |
| Go → Supabase | Token theft, MITM, replay, schema drift | TLS, short-lived tokens, idempotency, response validation |
| Local DB → OS | Stolen laptop, other OS users, backups | OS account isolation, disk encryption, local DB encryption/keychain |
| App → printer/export | Data leakage, spool retention | Explicit action, redaction, secure spool/cleanup guidance |
| Update feed → binary | Supply-chain compromise | Signed manifest and artifact, pinned keys, rollback |
| Staff → data | Insider over-access, curiosity browsing | Least privilege, RLS, audit review, no shared accounts |

## Authentication

`[PROPOSED]`
- Supabase Auth email/password as the baseline, matching the Android reference.
- Refresh token stored in the OS keychain, never in renderer storage.
- Access token kept in Go memory; short lifetime.
- On cold start, restore session only after validating the account is active and the role claim exists.
- Logout clears tokens, local PHI caches, and renderer state; unacknowledged writes require explicit confirmation.
- Account deactivation/ban must revoke refresh ability, not just hide UI.
- Optional OS-level app lock may supplement, not replace, Supabase authentication.

`[VERIFIED]` Android reference: role comes from `app_metadata.role`; missing/unknown role does not default. Staff creation enforces a 12-character minimum in the `manage-staff` edge function.

`[VERIFIED]` Reference connection controls:

- The Supabase URL and publishable key are build-time values from `.env.local` or process environment, not source literals. `.env.local` is untracked and the actual values are absent from the clean worktree.
- The session is stored in Keystore-backed encrypted preferences; a legacy plaintext session is migrated and removed.
- Android source contains no hardcoded Supabase URL, JWT-like literal, PostgreSQL URI, or `service_role` string in the inspected `app/src/main` tree.
- The `patient-docs` Storage bucket is private and active-staff-gated in migration SQL.
- `manage-staff` and `notify-update` read the service-role key only in server-side Edge Functions.
- The repository has read-only security verification SQL and an RLS role test, but neither was run in this pass.

`[UNKNOWN]` The live project's grants, policies, triggers, Storage rules, and actual configuration remain unverified. The CSV files contain no connection or policy fields and are not proof.

## Authorization

- RLS is the primary enforcement layer.
- Go services enforce permission checks for defense in depth, but do not replace RLS.
- The renderer's role is a display hint only.
- Admin-only operations (staff lifecycle, backup/restore, full sync, audit export) require server-side authorization.
- No client-side "sudo" mode, impersonation, or shared admin login in Phase 1.
- Break-glass access, if ever added, requires an approved ADR, time limit, and audit trail.

## Local data protection

`[PROPOSED]`
- Local database encrypted at rest with a key protected by the OS keychain; key recovery procedure documented.
- PHI not stored in browser storage, URL parameters, logs, crash reports, or temp files.
- Screen lock/idle timeout clears sensitive views.
- Local backups encrypted with a user-supplied passphrase and a modern KDF; no plaintext export.
- Secure deletion is best-effort on SSDs; document the limitation.
- Device enrollment/registration should be visible to admins.

## Network and API

- HTTPS only; certificate validation enabled.
- Use the same existing Supabase project as Android; no parallel backend or direct PostgreSQL credential.
- No service-role key, database password, or Edge Function secret in the desktop binary.
- Parameterized PostgREST filters; validate identifiers and sort columns against allowlists.
- Idempotency keys for retries.
- Rate-limit awareness and bounded retries.
- Validate response content type and shape; reject unexpected fields that could cause unsafe rendering.
- Verify the project identity with a redacted fingerprint; never print the URL, key, JWT, or Authorization header.

## Audit and monitoring

- Append-only audit for create/update/delete, payment, stock adjustment, role change, backup/restore, export, and sync resolution.
- Actor identity from the authenticated session/server, not a display-name string supplied by the client.
- Audit review is admin-only.
- Security-relevant events: failed login, repeated 403, account switch, restore, update signature failure, local DB integrity failure.
- Do not log PHI or tokens.

## Printing and export

- Receipt/export is an explicit user action.
- Print preview shows what will leave the system.
- Printer spool files may persist; document operational guidance.
- Export files are encrypted or placed in an access-controlled location.
- No automatic export to shared folders.

## Updates

- Signed release manifest and signed binaries.
- Pin the update public key in the app.
- Verify signature and version before install.
- Keep the previous version available for rollback.
- Never auto-update during an active write or unsynced state without a safe handoff.

## Inherited Android/backend risks

These are recorded in the Android KB; they are not claims about the live desktop or a live database.

| ID | Risk | Desktop implication |
|---|---|---|
| NSC-001 | `profiles` broadly readable by active staff | Do not assume profile fields are private; minimize display and exports |
| NSC-002 | Legacy permissive policies may defeat role migration | Verify live policies; do not rely on role claims alone |
| NSC-005 | No comprehensive table-level `GRANT`; auto-expose removed | Live grants must be verified before release |
| NSC-006 | `user_devices(user_id)` unindexed | Query performance and rate-limit behaviour |
| NSC-007 | `expenses` lacks accountability trigger | Desktop must stamp actor/time explicitly and audit |
| NSC-008 | Some Android routes lack nav guards | Desktop must guard routes and backend calls |
| NSC-009 | `manage-staff` self-guard gap for profile update | Fix before reusing the function for desktop |
| NSC-012 | Write rate limiter counts rows, not requests | Desktop batch writes may hit unexpected limits |
| NSC-013 | `SECURITY DEFINER` function without `search_path` | Verify/fix function definitions |

### Connection-specific risks

| ID | Risk | Required control |
|---|---|---|
| CONN-001 | Actual project URL/identity and publishable key are absent from the worktree | Obtain approved configuration securely; verify a redacted project fingerprint; never commit or log values |
| CONN-002 | Older Android CSV is stale and would generate the wrong schema contract | Do not use it; verify the live catalog or a reviewed baseline |
| CONN-004 | RLS/grants/Storage policies are not live-verified | Approve a non-destructive verification path and run role/Storage tests |
| CONN-008 | A desktop service-role key would bypass all RLS | Keep privileged operations in existing server-side Edge Functions; secret scanning gate |

## Security requirements

| ID | Requirement |
|---|---|
| SEC-001 | No service-role or database credential is present in the desktop client. |
| SEC-002 | Refresh tokens live only in the OS keychain; renderer never receives them. |
| SEC-003 | RLS is verified with real roles before release. |
| SEC-004 | Local PHI is encrypted at rest and cleared on logout/lock. |
| SEC-005 | Audit is append-only and attributable to the authenticated actor. |
| SEC-006 | Backups and exports are encrypted and explicitly initiated. |
| SEC-007 | Updates are signed and rollback-capable. |
| SEC-008 | No PHI or token appears in logs, crash reports, or telemetry. |

## Open questions

- Who supplies and owns the approved existing-project configuration?
- What non-destructive verification path is approved for RLS, grants, and Storage?
- Which local encryption product/approach is approved?
- Is a hardware-backed key available on all target devices?
- What is the incident-response and breach-notification process?
- Are device registrations required before access?
- What data-retention periods apply to clinical, financial, audit, and backup data?

## Related

[[Security/Threat-Model|Threat Model]] · [[Security/Privacy-and-Backup|Privacy and Backup]] · [[Database/Access-Patterns|Access Patterns]] · [[Audits/Risk-Register|Risk Register]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
