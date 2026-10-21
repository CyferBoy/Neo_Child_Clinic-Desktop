---
title: Security Model
doc_status: proposed
evidence: Android security register + Phase 0C Supabase metadata exports + shared-backend connection investigation + target architecture; no SQL executed
updated: 2026-10-21
---

# Security Model

> **No desktop security control is implemented.** This is a target model. The Android security register and the 2026-10-21 Supabase metadata exports are evidence of backend risks that the desktop will inherit unless they are fixed.

> **Critical exported-state finding — not a runtime certification.** The metadata exports report that `anon` has full table privileges on 22 public tables and that ten core tables have `{public}` policies that pass for an unauthenticated request because `get_my_role()` returns `'nurse'` when no profile exists. If the export is accurate and current, the public anon key can read and write patient, visit, note, consultation, vaccination, and inventory rows without a login. No desktop client should connect until this is confirmed and remediated. See [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] §4.

> **Accepted backend constraint `[DECISION]`:** Android and desktop must use the same existing Supabase project, PostgreSQL schema, Auth users, Storage buckets, and Edge Functions. No new project, separate remote PostgreSQL database, duplicate remote tables, or parallel remote schema is approved. Local SQLite is expected. See [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] and [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Connection Investigation]].

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

## Review coverage

This is a map of the required security concerns to their current evidence. **No desktop control is implemented, and no control in this table is verified against live configuration.**

| Concern | Requirement(s) | Evidence reviewed | Current status |
|---|---|---|---|
| Authentication and session | SEC-002, SEC-011 | Android auth/keychain source; feature 02; ADR-0004 | Design proposed; no desktop implementation |
| Authorization and RLS | SEC-003, SEC-009, SEC-011 | Phase 0C exports, Access Patterns, RLS SQL | Exported defects observed; live behaviour unverified |
| Local storage encryption | SEC-004 | Android SQLCipher/Keystore source; ADR-0002, ADR-0010 | Desktop design proposed; no implementation |
| Backup and restore | SEC-006 | Android backup source; Privacy and Backup; ADR-0010 | Desktop design proposed; no test |
| Logging, crash, telemetry | SEC-008 | Threat Model; feature 21; audit requirements | Rules proposed; no instrumentation |
| Printing and export | SEC-006, SEC-008 | Feature 13; Privacy and Backup; print threat | Rules proposed; no printer test |
| Application updates | SEC-007 | ADR-0006; feature 22 | Signing/rollback proposed; no package |
| Shared backend identity | SEC-001, SEC-003 | Shared Backend Investigation | Project identity unproven |
| Storage buckets | SEC-003 | Phase 0C SEC-0C-11 | Bucket/policy state unverified |
| Realtime authorization | SEC-003 | Phase 0C SEC-0C-10 | Publication reported; authorization unverified |
| Receipt/stock functions | SEC-009, SEC-010 | Phase 0C SEC-0C-06, SEC-0C-09 | Anon-executable functions observed; remediation deferred |
| Future object grants | SEC-010 | Phase 0C default ACL, migration gaps | Broad defaults observed; live post-Oct-30 state unknown |

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

`[PARTIAL — EXPORTED METADATA]` The 2026-10-21 exports report grants, policies, triggers, and function metadata, and they contradict several repository assumptions. They do **not** prove runtime JWT behaviour, project identity, Auth signup state, Storage bucket settings, or migration history. The column CSVs alone still contain no connection or policy fields and are not proof.

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
| NSC-002 | Legacy permissive policies may defeat role migration | **Confirmed by export:** 13 tables retain `{public}` policies; ten pass for `anon` via the `'nurse'` fallback. Runtime not tested. |
| NSC-005 | No comprehensive table-level `GRANT`; auto-expose removed | **Confirmed and extended:** 22 tables have full `anon`/`authenticated` ACLs; the seven migration-created business tables have no explicit `GRANT`, so they are not Oct 30-ready. |
| NSC-006 | `user_devices(user_id)` unindexed | Query performance and rate-limit behaviour; the export's four indexes are not mapped to this access path |
| NSC-007 | `expenses` lacks accountability trigger | Desktop must stamp actor/time explicitly and audit |
| NSC-008 | Some Android routes lack nav guards | Desktop must guard routes and backend calls |
| NSC-009 | `manage-staff` self-guard gap for profile update | Fix before reusing the function for desktop |
| NSC-012 | Write rate limiter counts rows, not requests | Desktop batch writes may hit unexpected limits |
| NSC-013 | Live-only legacy `get_my_role()` is `SECURITY DEFINER` without `search_path`; all 13 migration-authored `SECURITY DEFINER` functions pin it | **Confirmed by exported definition:** no `search_path`, fail-open `'nurse'`, and anon-executable. Do not copy it into desktop code. |

### Finding status vocabulary

| Status label | Meaning in this review |
|---|---|
| **Confirmed in repository source** | Directly proven by source/migration SQL or a repository artifact. |
| **Observed in an export** | Present in the 2026-10-21 metadata export; not exercised against the live API. |
| **Verified against live configuration** | Checked against the running project by an approved method. **No finding currently has this status.** |
| **Potential risk requiring verification** | A plausible impact derived from the evidence, not a demonstrated live exploit. |
| **Deferred by user** | Live verification or remediation is intentionally postponed to a later phase. |
| **Resolved with evidence** | The defect is fixed and verified. **No finding currently has this status.** |

An export is metadata evidence, not a runtime certification. Do not describe any row below as a confirmed production exposure.

### Phase 0C exported-state findings

These are **reported by the exports**, not verified by a query or an HTTP request. `GRANT` and RLS are separate controls: a table grant permits reachability through PostgREST; a policy decides which rows/commands pass. Neither one is a substitute for the other.

| Control | Reported state | Consequence |
|---|---|---|
| Table `GRANT` | 22 tables: `anon`/`authenticated`/`service_role`/`postgres` each have all eight privileges (`SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, MAINTAIN`); `receipt_sequences`: four DML privileges for anon/auth; `api_write_rate_limits`: none for anon/auth | `anon` can reach nearly every business table before RLS is evaluated |
| RLS enable/force | All 24 public tables enabled; none forced; owner `postgres` | The row boundary depends entirely on correct policies; `service_role`/owner bypass is by design |
| Policies | 179 rows: 178 public + one `storage.objects`; 13 public tables have `{public}` policies | Legacy policies were never removed; permissive `true` policy exists on `reminders` |
| Function `EXECUTE` | All 21 functions executable by `anon` and `authenticated` | Receipt burn, stock recalculation, rate-limit deletion, and helper exposure; `SECURITY DEFINER` functions use owner rights |
| Default ACL | New `public` tables/functions/sequences still receive broad `anon`/`authenticated`/`service_role` grants | Future-table exposure is not fixed by this snapshot; the Supabase change is enforced 2026-10-30 |
| Schema `USAGE` | Not exported | Cannot prove complete reachability or absence of other schemas |

| ID | Severity | Evidence | Potential impact | Affected components | Verification status | Recommended action |
|---|---|---|---|---|---|---|
| SEC-0C-01 | Critical | `L`: `get_my_role()` definition and the `{public}` policies on ten tables | **If current and reachable**, an unauthenticated request could read/write patient, visit, note, consultation, vaccination, vaccine, batch, inventory, waste, and borrow rows. This was not exercised. | Auth helper, RLS, PostgREST, ten clinical/inventory tables | Observed in an export; potential risk requiring verification; live verification deferred by user | Fail the helper closed, remove/replace legacy policies, then test anon and staff roles |
| SEC-0C-02 | High | `L`: `{authenticated}` `ALL` on `reminders` with `USING (true)` / `WITH CHECK (true)` | Any authenticated account, including non-staff, could read/write all reminders if reachable. | RLS, reminders, Auth-to-profile gate | Observed in an export; potential risk requiring verification; live verification deferred by user | Replace with active-staff predicates; test a non-staff account |
| SEC-0C-03 | High | `L`/`A`: `is_admin()` uses `app_metadata.role`; legacy profile policies use `profiles.role`; `handle_new_user()` may copy raw user metadata | Two role authorities can disagree; a user-controlled value may influence authorization. | Auth, profiles, role helpers, RLS | Observed in an export + confirmed in repository source; potential risk requiring verification | Reconcile to one server-controlled authority; remove legacy admin policies |
| SEC-0C-04 | High | `L`: `audit_logs` `{public}` INSERT with `auth.uid() IS NOT NULL` | Any authenticated user could forge audit rows, weakening accountability. | Audit table, RLS, audit feature | Observed in an export; potential risk requiring verification; live verification deferred by user | Restrict insert to approved server/active-staff paths; keep update/delete denied |
| SEC-0C-05 | Medium | `L`: legacy `user_devices` owner policies | A deactivated account with a still-valid JWT may manage its device row until expiry. | RLS, user_devices, account lifecycle | Observed in an export; potential risk requiring verification; live verification deferred by user | Require active staff; test a deactivated account |
| SEC-0C-06 | Critical | `L`: all 21 functions executable by `anon`/`authenticated`; definitions for receipt and stock functions | Receipt-sequence burn and stock mutation paths may be callable without appropriate staff authorization. | Functions, ACLs, receipts, inventory, rate limits | Observed in an export; potential risk requiring verification; live verification deferred by user | Revoke `PUBLIC`/`anon` execution; grant only allowlisted server/staff paths |
| SEC-0C-07 | High | `L`: `get_my_role()` and `handle_new_user()` are `SECURITY DEFINER` without pinned `search_path` | A definer function can be hijacked through object resolution; the role fallback worsens it. | Functions, schema resolution, auth path | Observed in an export; potential risk requiring verification | Pin `search_path`, schema-qualify references, and retest |
| SEC-0C-08 | High | `L`: `handle_new_user()` copies `raw_user_meta_data->>'role'` into `profiles.role` | A signup could select a stored role if public signup and legacy policies are active. | Auth trigger, profiles, role authority | Observed in an export; potential risk requiring verification; live verification deferred by user | Disable public signup or prevent user metadata from selecting an authorization role |
| SEC-0C-09 | High | `L`: `receipt_sequences` anon/auth DML grants; receipt function anon-executable | Receipt numbers could be consumed or altered, breaking audit and billing continuity. | Receipt sequence, function, grants, finance | Observed in an export; potential risk requiring verification; live verification deferred by user | Remove direct grants and revoke client execution; keep numbering server-side |
| SEC-0C-10 | High | `L`: 23 tables published to Realtime, including profiles, user_devices, receipt_sequences, clinical tables | Publication membership may expose change events; Realtime authorization is not proven. | Realtime, publication, RLS | Observed in an export; potential risk requiring verification; live verification deferred by user | Remove unnecessary membership and test Realtime authorization with each role |
| SEC-0C-11 | Medium | `L`: one `storage.objects` policy visible; no bucket rows exported | `patient-docs` privacy/limits/ownership cannot be verified; a misconfigured bucket could expose documents. | Storage, bucket policy, patient documents | Observed gap in an export; potential risk requiring verification; live verification deferred by user | Verify bucket privacy, limits, and object policies before upload |
| SEC-0C-12 | Medium | `L`: all 24 tables have `rls_forced = false` | Owner/service-role bypass is expected, but accidental owner execution would bypass RLS. | RLS, deployment role | Observed in an export; potential risk requiring verification | Never use owner/service_role at runtime; test all client roles with RLS enabled |
| MIG-0C-01 | High | `L`/`M`: seven migration-created tables lack explicit grants | Future access may fail or rely on broad defaults; the 2026-10-30 change makes this unsafe. | Grants, default ACLs, seven tables | Observed in an export; potential risk requiring verification; live verification deferred by user | Add reviewed least-privilege grants and role tests |

**No row above is `Verified against live configuration` or `Resolved with evidence`.** Those statuses require an approved live check or a completed, verified fix.

### Required roles and privileges — target, not deployed

`[PROPOSED]` This matrix is a design requirement. It does not authorize a blanket grant and does not describe the exported state.

| Role | Table/function intent | Explicitly not allowed |
|---|---|---|
| `anon` | No business-table access; no business RPC; Auth signup only if the clinic enables it | Patient/inventory/finance reads or writes; receipt sequence; stock recalculation |
| `authenticated` (non-staff) | No business-table access; no business RPC | Any clinic data, reminders, audit insert |
| Active staff | Row access through active-staff RLS; table grants limited to needed verbs; RPC allowlist | Broad `ALL` grants, `TRUNCATE`/`REFERENCES`/`TRIGGER`, service-role behavior |
| `service_role` | Server-side Edge Functions only | Desktop binary, renderer, or client-side logs |
| `postgres` | Migration/admin only | Application runtime |

### Authentication and trigger unknowns

- `[UNKNOWN]` Public signup state, whether `handle_new_user` is attached to `auth.users`, and whether a signup can influence `profiles.role`.
- `[VERIFIED]` Exported `handle_new_user()` is `SECURITY DEFINER` without `search_path` and defaults copied roles to `'nurse'`. This is a privilege path if public signup is enabled and the legacy `profiles` policies remain.
- `[PROPOSED]` The desktop must require a validated `app_metadata.role` and an active/non-deleted profile; it must never fall back to a default role or trust `profiles.role` for authorization.

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
| SEC-003 | RLS **and** table/function grants are verified with real roles, including `anon`, before release. A GRANT is not accepted as proof of RLS, or vice versa. |
| SEC-004 | Local PHI is encrypted at rest and cleared on logout/lock. |
| SEC-005 | Audit is append-only and attributable to the authenticated actor; only approved server/active-staff paths may insert. |
| SEC-006 | Backups and exports are encrypted and explicitly initiated. |
| SEC-007 | Updates are signed and rollback-capable. |
| SEC-008 | No PHI or token appears in logs, crash reports, or telemetry. |
| SEC-009 | `anon` has no business-table or business-RPC access; legacy `{public}` policies and the `'nurse'` fallback are removed or fail closed. |
| SEC-010 | Every new table/function has explicit least-privilege grants, including the intended `service_role` path, and is re-verified after the 2026-10-30 Data API change. |
| SEC-011 | Role authority is server-controlled; client-writable metadata and `profiles.role` cannot grant privileges. |

## Open questions

- Who supplies and owns the approved existing-project configuration?
- Who owns remediation of the exported anon/legacy-policy findings, and what is the approved migration/review path?
- What non-destructive verification path is approved for RLS, grants, and Storage?
- Is public signup disabled, and is `handle_new_user` attached? If signup is enabled, what prevents role selection through user metadata?
- Which project grants survive the 2026-10-30 Data API change, and when will they be re-exported?
- Which local encryption product/approach is approved?
- Is a hardware-backed key available on all target devices?
- What is the incident-response and breach-notification process?
- Are device registrations required before access?
- What data-retention periods apply to clinical, financial, audit, and backup data?

## Related

[[Security/Threat-Model|Threat Model]] · [[Security/Privacy-and-Backup|Privacy and Backup]] · [[Database/Access-Patterns|Access Patterns]] · [[Product/Business-Rules|Business Rules]] · [[Audits/Risk-Register|Risk Register]] · [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] · [[Audits/Documentation-Completion-Report|Documentation Completion Report]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] · [[Decisions/ADR-0009-Inventory-and-Financial-Integrity|ADR-0009]] · [[Decisions/ADR-0010-Backup-and-Restore|ADR-0010]]
