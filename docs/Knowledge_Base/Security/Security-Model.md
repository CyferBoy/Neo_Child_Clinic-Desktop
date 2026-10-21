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

| ID | Finding | Required response |
|---|---|---|
| SEC-0C-01 | **Anon fail-open:** `get_my_role()` returns `COALESCE(role, 'nurse')`; ten `{public}` `ALL`/`SELECT` policies then pass for `anon`: `patients`, `patient_visits`, `patient_notes`, `consultations`, `vaccination_items`, `vaccines`, `vaccine_batches`, `inventory_transactions`, `waste_records`, `borrow_records` | Confirm with an anon-key read against synthetic data; drop/replace legacy policies or make the helper fail closed; verify both GRANT and RLS |
| SEC-0C-02 | **`reminders`:** `{authenticated}` `ALL` with `USING (true)` / `WITH CHECK (true)` | Any authenticated account, including non-staff, can read/write all reminders. Replace with active-staff predicates and test a non-staff account. |
| SEC-0C-03 | **Role-source split:** `is_admin()` uses `app_metadata.role`, but legacy `profiles` policies use `profiles.role` via `get_my_role()`/`check_is_admin()`; `handle_new_user()` may copy `raw_user_meta_data->>'role'` | Reconcile to one server-controlled role authority; remove legacy admin policies; verify signup cannot choose a role |
| SEC-0C-04 | **Audit forgery:** `audit_logs` has a `{public}` INSERT policy with `auth.uid() IS NOT NULL` | Any authenticated user can insert audit rows. Restrict insert to active staff/server paths; keep update/delete denied. |
| SEC-0C-05 | **Deactivated-device path:** legacy `user_devices` owner policies do not require active staff | A user with a valid JWT can manage their device row after deactivation until token expiry. Require active staff and verify with a deactivated account. |
| SEC-0C-06 | **Function exposure:** all 21 functions are anon-executable, including `neo_next_receipt_number()` (sequence burn) and `recalculate_all_stocks()` (stock write path) | Revoke from `PUBLIC`, `anon`, and `authenticated`, then grant only an allowlisted role/function set; verify with `has_function_privilege` |
| SEC-0C-07 | **Definer hardening:** `get_my_role()` and `handle_new_user()` are `SECURITY DEFINER` without `search_path` | Pin `search_path`; retain schema-qualified references and verify the functions after any migration. |
| SEC-0C-08 | **Signup role path:** `handle_new_user()` copies `raw_user_meta_data->>'role'` into `profiles.role`, defaulting to `nurse` | Confirm public signup is disabled or the trigger is safe; prevent user metadata from selecting an authorization role. |
| SEC-0C-09 | **Receipt path:** `receipt_sequences` retains anon/auth DML grants despite the revoke, and `neo_next_receipt_number()` is anon-executable | Remove direct grants and revoke function EXECUTE from client roles; keep receipt numbering server-side. |
| SEC-0C-10 | **Realtime:** 23 tables are published, including `profiles`, `user_devices`, `receipt_sequences`, and clinical tables | Remove unnecessary publication membership and verify Realtime authorization separately. |
| SEC-0C-11 | **Storage:** only one `storage.objects` policy is visible and no bucket rows were exported | Verify the `patient-docs` bucket is private, with expected limits and ownership, before any upload. |
| SEC-0C-12 | **Forced RLS:** all tables have `rls_forced = false` | Never use the table owner or `service_role` from the desktop; test all client roles and keep RLS enabled. |
| MIG-0C-01 | **Default ACL / Oct 30:** the seven migration-created business tables (`consultation_todos`, `vaccination_todos`, `personal_vaccine_reminders`, `borrow_returns`, `expenses`, `doctor_weekly_slots`, `doctor_slot_exceptions`) have no explicit table grant | Add least-privilege grants in a reviewed migration, including `service_role`; do not assume the platform default survives. |

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

[[Security/Threat-Model|Threat Model]] · [[Security/Privacy-and-Backup|Privacy and Backup]] · [[Database/Access-Patterns|Access Patterns]] · [[Audits/Risk-Register|Risk Register]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
