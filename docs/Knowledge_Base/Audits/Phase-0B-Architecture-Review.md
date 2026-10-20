---
title: Phase 0B — Blocker Resolution and Architecture Review
doc_status: proposed
evidence: second-pass validation + Phase 0B recheck + schema reconciliation + Android source/migrations + no live access
updated: 2026-10-20
---

# Phase 0B — Blocker Resolution and Architecture Review

> **Decision-ready review, not an implementation.** This pass rechecked the failed/partial notes, reconciled the two CSV snapshots against migrations and Android source, and evaluated the unresolved architecture decisions. No desktop application, Android source, database schema, migration, RLS policy, grant, Supabase setting, or dependency was changed. No credential, project URL, JWT, or patient data is reproduced.

**Android reference:** `/data/data/com.termux/files/home/Neo_Child_Clinic` — `main` @ `ca4bed4`, clean  
**Desktop:** `/storage/emulated/0/Neo_Child_Clinic_Desktop` — documentation only, changes uncommitted  
**Live Supabase access:** none available in this environment  
**Binding decision:** [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] remains accepted

## 1. Recheck of the 18 failed and 25 partial notes

The pre-correction matrix remains historical: **20 PASS, 25 PARTIAL, 18 FAIL** for 63 pre-existing notes, and **17 PARTIAL** skills. The Phase 0B recheck does not reuse those verdicts as current defect claims.

| Pre-correction set | Count | Current meaning after recheck |
|---|---:|---|
| FAIL | 18 | Material documentation errors were corrected in the prior pass. None remains a current documentation defect. The residual issues are live-evidence gaps, architecture decisions, or explicit `[UNKNOWN]` state. |
| PARTIAL | 25 | Corrections are applied. Some feature/parity statements remain deliberately unverified because no desktop source or live test exists. |
| PASS | 20 | Rechecked. Two Data Dictionary relationship rows were corrected, and money-type wording was corrected in the Data Dictionary, Database Architecture, Product Vision, Technical Debt, and ADR-0007. No other material PASS error found. |
| Skills | 17 | No Phase 0B skill changes are needed; the prior corrections remain valid. |

**New Phase 0B documentation finding:** `P0B-DOC-01` — the Data Dictionary listed `patients.patient_id` as a high-confidence parent key for `vaccination_items`, and listed `visit_id / vaccination_id` for the visit relationship. `vaccination_items` has `vaccination_id`, not `patient_id` or `visit_id`; the supported relationships are `patients → patient_visits` and `patient_visits → vaccination_items` through `vaccination_id`. Corrected; it changes no architecture decision.

**New Phase 0B documentation finding:** `P0B-DOC-02` — several notes described the shared schema as using floating-point money. The CSV shows `numeric` amounts (and `expenses.amount_paise` as `bigint`); the floating-point risk is the Android `Double` mapping and client arithmetic, not a float column. Corrected in the Data Dictionary, Database Architecture, Product Vision, Technical Debt, and ADR-0007 context. The ADR remains Proposed and its integer-paise recommendation is unchanged.

### 1.1 Genuine blockers versus documentation quality

| Category | Current status | Why |
|---|---|---|
| Live database contract | **Blocker** | The file-level reconciliation is resolved, but actual columns, keys, constraints, and snapshot provenance require the read-only catalog export. |
| Live RLS/grants/functions/triggers/Storage/Realtime | **Blocker** | Migration SQL is intent, not deployed state. No authorized live session was available. |
| Stock integrity mode | **Blocker** | The live database may use the `update_batch_stock()` trigger or the client absolute-batch writer. Dual writing would corrupt stock; live trigger/function evidence is required. |
| Deletion/absence reconciliation | **Blocker** | Repository evidence contains no tombstone/change feed; no approved contract exists. Sync deletion tests remain blocked. |
| ADR-0001 through ADR-0007 | **Decision blocker** | All remain Proposed. ADR-0008 is accepted. |
| Local encryption, backup, retention | **Decision blocker** | No approved desktop encryption/key-recovery or retention policy. |
| Phase 1 scope and toolchain | **Open** | No signed pilot scope; no Go/Wails/Node manifests, CI, or desktop tests. |
| Stale/failed documentation claims | **Resolved** | Prior corrections plus the Phase 0B reconciliation; no historical FAIL is treated as a live defect. |
| Feature parity claims | **Unverified, not a doc defect** | 0 of 22 desktop modules implemented; Android module status remains 5 partial/17 unverified. |

The original FAIL/PARTIAL verdicts are therefore **not** an implementation blocker list. The blockers are the evidence and decision gates in section 5.

## 2. Database reconciliation summary

Full table-by-table evidence: [[Database/Schema-Reconciliation|Schema Reconciliation — Phase 0B]].

### 2.1 Verified counts

- Desktop CSV: **24 tables / 416 column rows**, explicit `public` schema.
- Android CSV: **23 tables / 361 column rows**, no schema column, camelCase `waste_records`.
- Both counts are correct for the files.

### 2.2 The 55-row difference is explained

`55 = 45 + 4 + 3 + 3`

- 15 tables × 3 soft-delete columns (`is_deleted`, `deleted_at`, `deleted_by`) = **45** (`20260925`).
- `doctor_slot_exceptions` and `expenses` × 2 additional soft-delete columns = **4**; both already had `is_deleted` in the Android snapshot.
- `waste_records`: 8 camelCase→snake_case renames plus 3 soft-delete columns = **+3 net** (`20260919`, `20260925`).
- `api_write_rate_limits`: desktop-only 3-column server table = **3** (`20260929001000`).

No shared table has a `data_type`, `is_nullable`, or `column_default` difference between the snapshots. The difference is additions plus the waste rename, not type drift.

### 2.3 Snapshot chronology `[INFERRED, high]`

- Android CSV still has camelCase waste columns and `doctor_slot_exceptions.is_deleted` without `deleted_at`/`deleted_by`; this brackets it between the `20260911` slot migration and the `20260919` waste/soft-delete changes.
- Desktop CSV has full soft-delete columns and `api_write_rate_limits`; it is after `20260929`.
- This chronology is inferred from migration signatures, not from capture metadata. It does not prove either snapshot came from production.

### 2.4 The 9-of-24 fact is not a missing-production count

Repository migrations create only **9 of the 24** desktop-snapshot tables from zero:

`api_write_rate_limits`, `borrow_returns`, `consultation_todos`, `doctor_slot_exceptions`, `doctor_weekly_slots`, `expenses`, `personal_vaccine_reminders`, `receipt_sequences`, `vaccination_todos`.

The other **15** are baseline tables that both snapshots already contain. Repository SQL alters/policies them but cannot create them. `20261016` also proves at least one missing migration and manual application: `todo_notification_events` was "created by a migration that is not in this repository," and the migration is described as safe to apply where some of it was applied by hand. `20261013` records that `update_batch_stock()` was applied to production by hand and lived only in a scratch file.

**Conclusion:** the 24-vs-23 and 416-vs-361 discrepancies are consistent with snapshot timing plus missing baseline/manual migration history. They are **not evidence that 15 tables are missing from production**. The live contract remains unverified.

### 2.5 Keys, relationships, and RLS

- Both CSVs omit keys, indexes, policies, and grants. The Android filename claiming keys/indexes is inaccurate.
- Repository-created tables provide primary/foreign keys in SQL; Room provides local foreign keys only; several remote relationships have no declared FK in the evidence (`audit_logs`, `finance_transactions`, `inventory_transactions`, `profiles`, `user_devices`).
- Migration RLS covers 25 named public tables: 16 active-staff CRUD tables, `audit_logs` (select/insert only), `profiles` (select only), `user_devices` (owner-scoped), `expenses` and doctor slots (role/owner carve-outs), `receipt_sequences` and `api_write_rate_limits` (revoked), and conditional `todo_notification_events` (enabled/forced, revoked, no client read policy).
- This is **SQL intent**, not deployed policy or grant evidence.

## 3. Live security verification status

### 3.1 Access determination

**No safe, authorized live access was available.** In the inspection environment:

- `supabase`, `psql`, `pg_dump`, and `docker` were not installed.
- No Supabase/PostgreSQL environment variable names were present.
- The OpenCode MCP resource listing returned no resources or templates.
- No `.env`, `.env.local`, `local.properties`, or `secrets.properties` was present in the Android worktree.
- The Android `supabase/config.toml` is CLI configuration, not a runtime connection; its values were not read or printed.
- The actual project URL/publishable key are build-time inputs absent from the worktree.

No live query was run. No table, policy, grant, function, trigger, Storage rule, or Realtime setting is claimed verified.

### 3.2 Migration evidence versus deployed evidence

| Layer | Evidence | Status |
|---|---|---|
| Repository migration SQL | 23 migrations; RLS policies, functions, triggers, receipt numbering, stock trigger versions | `[VERIFIED]` file-level intent |
| Existing security SQL | `supabase/verify_security.sql` (read-only); `supabase/tests/rls_role_test.sql` (not read-only; placeholders) | `[VERIFIED]` assets; neither run |
| Deployed catalog/RLS/ACL | Requires authorized read-only export | `[UNKNOWN]` |
| Deployed stock mode | Trigger vs client absolute-batch writer | `[UNKNOWN]` — critical |
| Project identity | Requires approved configuration + redacted fingerprint | `[UNKNOWN]` |

### 3.3 Exact export and reconciliation

The complete read-only SQL is in [[Database/Live-Verification-Queries|Live Verification Queries — Read Only]]. It covers:

- current `public` tables, columns, constraints, and indexes;
- RLS enabled/forced and actual policies, including `storage`;
- table/schema/sequence/function ACLs, default ACLs, and role memberships;
- effective `anon`/`authenticated`/`service_role` privileges;
- function definitions, `SECURITY DEFINER`, `search_path`, and trigger enabled state;
- aggregate auth/profile role counts without user identifiers or PHI;
- private Storage bucket metadata and Realtime publication membership.

Run through an authorized Supabase admin/read-only session in a read-only transaction. Do not run the existing `rls_role_test.sql` (it contains DML) without separate approval and synthetic test data. Do not print or commit credentials, URLs, JWTs, or patient data. The results reconcile against the CSVs and migrations by table/column/constraint/policy diff; they do not by themselves prove JWT-level row behavior.

## 4. Architecture decision review

ADR-0008 (shared existing Supabase project/schema) is accepted and not reopened. The other decisions remain **Proposed**; recommendations below do not approve them.

### 4.1 Decision summary

| ID | Decision question | Recommendation | Approval |
|---|---|---|---|
| D1 | Wails major, OS matrix, packaging | Pin the current supported Wails major after a smoke build; Windows 11 x64 first; Windows 10 only with supported ESU/approval; defer other OS | Yes |
| D2 | Local persistence and encryption | SQLCipher-compatible SQLite, WAL/single writer, key in OS keychain, per-device key | Yes |
| D3 | Sync transport and transaction groups | Ordered per-entity PostgREST upserts in outbox groups; no new server RPC by default | Yes |
| D4 | Deletion/absence reconciliation | Soft delete + pull deleted rows where columns exist; authoritative snapshot/absence for hard deletes; no client hard deletes | Yes |
| D5 | Auth and session | Go-owned auth; `app_metadata.role`; active/non-deleted profile; refresh token in keychain; no role fallback | Yes |
| D6 | Wails boundary | Narrow typed bindings only; no raw SQL/FS/URL/tokens | Yes |
| D7 | Testing and release | Layered risk-based tests, approved non-destructive live path, signed/rollback release gates | Yes |
| D8 | Money, dates, identity | Integer paise in domain, explicit numeric boundary, typed dates/IST, UUID + clinic ID, server receipts | Yes |
| D9 | Cache ownership/invalidation | Local DB is source; screen query cache; short-TTL Go lookup cache; versioned invalidation | Yes |
| D10 | Inventory integrity | Ledger append-only; live trigger mode must be proven; never dual-write trigger and absolute batch | Yes |
| D11 | Finance/receipt integrity | Server-assigned immutable receipt; one canonical payment per visit; audited corrections | Yes |
| D12 | Local encryption/backup/restore | Separate versioned AEAD backup container with AAD/KDF/manifest/safety snapshot | Yes |
| D13 | Phase 1 scope | All 22 as target; staged pilot slice first, not all 22 before pilot | Yes |
| D14 | Build/test toolchain and packaging | Pin stable Go/Wails/Node; Windows x64 signed installer; CI, lockfiles, SBOM, rollback | Yes |

### 4.2 Decision cards

#### D1 — Desktop stack, OS matrix, and packaging (ADR-0001)

**Question.** Which Wails major, operating systems, architectures, and packaging path are approved?

**Options.**
- **A. Supported stable Wails major with the most proven Windows packaging (conservative baseline: the v2 line, if still supported).** Pros: most mature packaging/printing path; fastest route to a clinic pilot; matches the Go/Wails direction. Cons: newer major features may be deferred; a later migration may be needed.
- **B. Newest Wails major (v3 or later) only after packaging proof.** Pros: newer architecture; less likely to migrate later. Cons: unproven packaging/printing/update tooling; no evidence in this repository; upgrade risk before first release.
- **C. Electron/native/other.** Rejected by project direction; larger runtime or duplicated stack.

**Evidence.** ADR-0001; no desktop source; no OS requirement recorded. Windows-first is a recommendation, not a verified clinic fact.  
**Security/integrity consequences.** Packaging and signing determine update trust; printing determines PHI spillage; keychain/OS APIs differ by platform.  
**Recommendation.** A: pin the current supported Wails major after a Windows smoke build; support Windows 11 x64 first; Windows 10 only where it receives supported security updates/ESU and is explicitly approved; add macOS/Linux only after signed packaging, keychain, printing, and update proof. Do not upgrade major versions mid-pilot.  
**Prerequisites.** Wails/Go/Node smoke build on target; signed installer test; printer test; version pin; user-approved OS matrix.  
**User approval.** Required.

#### D2 — Local persistence and encryption (ADR-0002)

**Question.** Which local database driver and at-rest encryption/key model are approved?

**Options.**
- **A. SQLCipher-compatible SQLite with key in OS keychain.** Pros: closest to Android Room+SQLCipher; page-level encryption protects the whole working copy; supports WAL/transactions. Cons: CGO/driver/build complexity; key recovery and rotation must be designed; keychain APIs differ.
- **B. Plain SQLite relying on OS full-disk encryption.** Pros: simplest. Cons: no app-level PHI protection; shared OS accounts/backup/temp files can expose data; fails the security baseline.
- **C. Field-level encryption.** Pros: selective. Cons: complex queries/indexes, metadata leakage, high implementation risk; not a substitute for database encryption.

**Evidence.** Android uses Room with SQLCipher and a Keystore-backed passphrase; ADR-0002 requires encryption at rest; no desktop driver exists.  
**Security/integrity consequences.** A stolen device or copied file is a PHI breach if plaintext. Key loss can destroy the working copy; key recovery must be explicit.  
**Recommendation.** A, with a per-device database key, OS-keychain wrapping, documented recovery/rekey, WAL, foreign keys, busy timeout, single writer, and no plaintext temp/export. If the chosen Go driver cannot meet transaction/WAL requirements, select an equivalent SQLCipher-compatible driver after a spike.  
**Prerequisites.** Driver/build spike on every target; key lifecycle/recovery; backup format; corruption/disk-full tests; no plaintext PHI verification.  
**User approval.** Required.

#### D3 — Sync transport and transaction groups (ADR-0003)

**Question.** Does the desktop upload ordered per-table PostgREST writes, or require a new server-side transaction-group RPC?

**Options.**
- **A. Ordered per-entity PostgREST upserts with an outbox transaction group.** Pros: matches Android; no schema/server changes; preserves ADR-0008; reuses existing RLS. Cons: HTTP calls are not one server transaction; partial groups need explicit repair; idempotency depends on stable IDs and uniqueness, some of which are conditional or unverified.
- **B. New server transaction-group RPC.** Pros: true server atomicity. Cons: new database function/contract, migration and security review, Android divergence, potentially a new backend component; not approved by ADR-0008's "no new backend by default."
- **C. Event sourcing/CDC for every entity.** Too broad for Phase 1; requires a change feed that repository evidence does not establish.

**Evidence.** Android uses PostgREST and no `.rpc` calls; 21 direct table targets plus `patient_notes` through the sync registry; `20261016` adds conditional unique indexes; no server transaction-group RPC exists in the evidence.  
**Security/integrity consequences.** A client-side group is a logical acknowledgment, not server atomicity. A partial failure can leave a visit without payment/stock unless repair is explicit. Never report group success on partial upload.  
**Recommendation.** A for Phase 1: outbox groups, dependency order, stable IDs/idempotency keys, explicit per-member status, no false ack, visible repair. Do not invent an RPC. Revisit B only if live evidence and replay tests prove a business event cannot be made safe with ordered upserts; that would require a separate approved ADR/migration and Android compatibility review.  
**Conflict ownership (part of D3).** Do not use one blanket policy: patient demographics may use last-write-with-audit; clinical notes/consultations must surface an append-only conflict, never silently overwrite; stock is server-ledger/trigger authoritative (D10); payments/receipts are server/audit authoritative and corrections are explicit (D11); deletion follows D4. A conflict that cannot be auto-resolved stays visible and blocks the affected group, not the whole local UI.  
**Prerequisites.** D4 deletion contract; uniqueness/idempotency evidence for each entity; live RLS/permission tests; replay/partial-failure harness; conflict-owner matrix approved per entity.  
**User approval.** Required.

#### D4 — Deletion and absence reconciliation (ADR-0003/ADR-0007)

**Question.** How do hard deletes and soft deletes propagate without resurrection or silent data loss?

**Options.**
- **A. Soft delete + pull deleted rows where columns exist.** Pros: uses current `is_deleted`/`deleted_at`/`deleted_by`; auditable; no tombstone table; works with incremental pull. Cons: retains PHI; only covers tables with soft-delete columns; requires policies/grants to read deleted rows; deletion of a parent with children remains a domain rule.
- **B. Authoritative snapshot/absence reconciliation.** Pros: can detect hard deletes without a tombstone table. Cons: full-snapshot cost, race/transaction consistency, retention of a trusted snapshot, and absence can be confused with permission/filter/network loss.
- **C. Server tombstone/change feed.** Pros: accurate incremental deletion. Cons: schema/server change, new retention/security contract, Android adoption, new ADR; not currently evidenced.

**Evidence.** `20260925` adds soft-delete columns to 18 business tables; `inventory_transactions`, `audit_logs`, `profiles`, `user_devices`, and `receipt_sequences` do not have the full set; `20261016` says there is no tombstone feed; Android pull cannot observe every hard delete (NCC-023).  
**Security/integrity consequences.** A resurrection can restore a deleted patient/stock/payment. Absence reconciliation can delete valid local data if a query is filtered or unauthorized. Soft delete retains PHI and can leak through reports/exports if filters are missed.  
**Recommendation.** A for the tables that have the soft-delete fields, with a pull that explicitly includes deleted rows and filters them from normal reads. B only as an approved fallback for hard-delete tables or a documented full-snapshot repair path. C only with a new approved ADR, migration, retention rule, and Android compatibility plan. **Prohibit desktop hard deletes** until the contract is approved. Define retention and deletion authorization before implementation.  
**Prerequisites.** Live soft-delete columns/policies; retention decision; cursor/overlap semantics; tests for delete, revive, unauthorized filter, and parent/child deletion.  
**User approval.** Required.

#### D5 — Authentication/authorization and session (ADR-0004)

**Question.** Where do authentication and role authority live, and what happens offline?

**Options.**
- **A. Go-owned Supabase Auth; role from validated `app_metadata.role`; active/non-deleted profile required.** Pros: matches RLS and Android; refresh token never enters renderer; no role fallback. Cons: keychain/offline UX complexity; live role behavior must be tested.
- **B. Renderer-owned Supabase session.** Rejected: token exposure/XSS and bypass of the trusted core.
- **C. Role from `profiles.role` or `user_metadata`.** Rejected: profiles is display/activation data; user metadata is client-writable; role must match RLS.

**Evidence.** `20261001_app_metadata_roles.sql` makes `app_metadata.role` the RLS source and strips `user_metadata.role`; `CurrentUserProvider` returns null for missing/unknown roles; `manage-staff` enforces admin/server-side lifecycle.  
**Security consequences.** A missing role must deny, not default. Deactivation must revoke refresh ability, not just hide UI. Offline cached PHI must not become an indefinite authorization bypass.  
**Recommendation.** A: Go auth/refresh; refresh token only in the OS keychain; access token only in Go memory; role only from `app_metadata`; require active/non-deleted profile; no fallback. Allow offline read-only with a previously validated cached session; require refresh/revalidation before writes/sync when the session is expired. Clear local PHI on logout/account switch; block sign-out with unsynced writes unless explicitly confirmed.  
**Prerequisites.** Live role/deactivation tests; keychain implementation; idle/re-auth policy; sign-out/unsynced-write UX.  
**User approval.** Required (ADR-0004).

#### D6 — Wails trust boundary (ADR-0005)

**Question.** Which capabilities cross the Go↔React boundary?

**Options.**
- **A. Explicit typed Go methods only.** Pros: narrow attack surface; testable contracts; tokens/DB stay in Go. Cons: binding boilerplate and versioning.
- **B. Generic RPC/SQL/HTTP bridge.** Rejected: injection, over-privilege, token/DB exposure.
- **C. Renderer calls Supabase directly.** Rejected: tokens in browser storage and bypass of validation.

**Evidence.** ADR-0005; no desktop implementation.  
**Security consequences.** A generic bridge would expose the trusted core; streaming/large exports need bounded contracts.  
**Recommendation.** A: validate every input, stable result/error envelope, authorization re-check in Go, context/timeouts, generated bindings with CI drift check, no raw SQL/FS paths/shell/arbitrary URLs/tokens/secrets.  
**Prerequisites.** Binding generator choice; contract tests; cancellation/large-export design.  
**User approval.** Recommended as part of ADR-0005.

#### D7 — Testing and release (ADR-0006)

**Question.** What evidence is required before a desktop release?

**Options.**
- **A. Layered risk-based tests + CI + signed/rollback release.** Pros: covers replay, RLS, restore, print, update; prevents known failure modes. Cons: effort and approved live test access.
- **B. Manual/unit-only.** Rejected: cannot prove replay/RLS/restore safety.
- **C. Test against production records.** Rejected: PHI/security risk.

**Evidence.** Android defects survived missing orchestrator/destructive-path tests; desktop has no suite; live RLS tests were not run.  
**Recommendation.** A: Go unit/repository tests, Wails contract tests, React component/E2E, sync chaos, backup/restore, print/update/accessibility; local synthetic data; approved non-destructive shared-backend verification; CI required; signed builds/versioned feed/rollback. No release with open P0/P1 data-integrity or security finding.  
**Prerequisites.** CI provider; test data owner; approved live verification path; signing identity; pilot rollback window.  
**User approval.** Required.

#### D8 — Money, dates, and identity (ADR-0007)

**Question.** How are money, business dates, patient identity, and receipts represented at the shared-schema boundary?

**Options.**
- **A. Integer paise in the domain; explicit conversion to the shared `numeric` columns; typed dates; IST; UUID + clinic ID.** Pros: exact arithmetic, stable sorting, no device timezone drift; receipts stay server-side. Cons: conversion/rounding rules and legacy data.
- **B. Mirror the Android `Double`/text representation everywhere.** Rejected: repeats client-side rounding/sorting/timezone defects.
- **C. Use display names/phone/formatted dates as keys.** Rejected: duplicate/renamed patients and unstable joins.

**Evidence.** Desktop CSV shows `numeric` for finance/visit amounts, `bigint amount_paise` for expenses, and `text`/`date` business dates; Android entities map most amounts to `Double` and use `Asia/Kolkata` for calendar calculations; receipt numbering is a server trigger.  
**Security/integrity consequences.** Client-side float equality/rounding corrupts totals; lossy boundary conversion can still affect exact `numeric` values; text dates can sort lexicographically; wrong timezone changes due lists; client-computed receipts can collide.  
**Recommendation.** A: integer minor units in Go; explicit documented rounding at the boundary; typed dates (business date vs timestamp), IST for due/report classification; UUID identity plus unique `patient_clinic_id`; server-assigned immutable receipt numbers.  
**Prerequisites.** Boundary conversion rules; legacy data audit; clinic ID uniqueness live check; timezone tests.  
**User approval.** Required.

#### D9 — Cache ownership and invalidation

**Question.** Where may cached PHI/read models live, and what invalidates them?

**Options.**
- **A. Local DB is the source; renderer query cache per screen; short-TTL Go lookup cache; versioned invalidation.** Pros: simple, bounded, no second source of truth; clear on logout. Cons: invalidation work for joined read models; memory cache cannot be a consistency mechanism.
- **B. No cache.** Pros: simplest. Cons: poorer UX; still needs local DB reads.
- **C. Long-lived aggregate/materialized caches.** Pros: dashboard speed. Cons: stale clinical/financial data; complex invalidation; PHI exposure.

**Evidence.** Android `MemoryCache` explicitly treats TTL as retention, not consistency; `PatientCache` stores only the patient row and is invalidated on patient changes; no desktop cache exists.  
**Security consequences.** Cross-account cache leakage; stale stock/payment totals; PHI in browser storage/logs.  
**Recommendation.** A: local DB/outbox is authoritative; renderer cache is screen/session scoped; Go cache only small lookup sets with short TTL; invalidate on committed writes and pull changes; versioned keys; clear on logout/account switch; no PHI in browser storage, service workers, logs, or diagnostics.  
**Prerequisites.** Read-model dependency map; logout/idle clearing; cache metrics; invalidation tests.  
**User approval.** Recommended as architecture.

#### D10 — Inventory transaction integrity

**Question.** Is `vaccine_batches.remaining_quantity` maintained by the server trigger or by the client's absolute batch upsert?

**Options.**
- **A. Server trigger mode.** `inventory_transactions` is the append-only ledger; `update_batch_stock()` updates batch quantities; one trigger only. Pros: server-authoritative, replay-safe, negative guard. Cons: requires live trigger/function proof; historical corruption may need reconciliation.
- **B. Client absolute-batch mode.** Client computes and uploads `remaining_quantity`. Pros: works where no trigger exists. Cons: concurrent devices can overwrite stock; no server ledger guarantee; high corruption risk.
- **C. New stock RPC.** Pros: explicit transaction/validation. Cons: new server code/schema/ADR; not currently evidenced.

**Evidence.** `20261013` says `update_batch_stock()` was hand-applied and the block is skipped if the function is absent; `20261016` conditionally installs the trigger; `20261017` fixes a duplicate legacy trigger and UPDATE arithmetic; `20261018` fails loudly if the function/table/trigger is missing. The live mode is unknown.  
**Security/integrity consequences.** Dual writing applies stock twice; absolute upserts lose concurrent movements; negative stock can reject a real vaccination after the ledger row is attempted. Historical duplicate-trigger corruption is not repaired by the migration.  
**Recommendation.** Do not implement inventory writes until live function/trigger evidence establishes the mode. If trigger mode: ledger append-only, server trigger/negative guard authoritative, desktop never writes absolute `remaining_quantity`, no second trigger. If absolute mode: stop and reconcile; do not install a trigger blindly. A new RPC requires a separate approved ADR.  
**Prerequisites.** Live `pg_proc`/`pg_trigger` export; exactly-one-trigger check; ledger/batch reconciliation against physical stock; replay/negative/concurrent tests.  
**User approval.** Required as part of inventory/finance invariants.

#### D11 — Financial transaction integrity and receipt numbering

**Question.** How are payments, visit totals, corrections, and receipt numbers kept consistent?

**Options.**
- **A. Server receipt trigger/sequence + one canonical payment per visit + audited corrections.** Pros: collision-free, immutable, matches existing behavior. Cons: relies on deployed trigger/unique index; corrections need workflow.
- **B. Client-generated receipt numbers.** Rejected: duplicates/races/tampering.
- **C. Mutable receipts/payment overwrite.** Rejected: audit/financial integrity failure.

**Evidence.** `20260824_receipt_numbering.sql` allocates per-financial-year numbers with `INSERT ... ON CONFLICT ... RETURNING`, assigns on insert, preserves on update, and creates a partial unique index; Android uploads blank and reads back; no `.rpc` call.  
**Recommendation.** A: server-assigned immutable receipt, one canonical payment identity per visit, integer paise in the desktop domain, explicit cash/online/mixed reconciliation, audited correction instead of silent overwrite. Never compute a receipt locally or expose a sequence.  
**Prerequisites.** Live trigger/unique index; receipt format/legal approval; payment identity rules; report reconciliation tests.  
**User approval.** Required.

#### D12 — Local encryption, backup, and restore

**Question.** Is the Android `.nccb` backup format reused, or does the desktop define its own encrypted container?

**Options.**
- **A. Reuse Android `.nccb`.** Pros: possible cross-restore; existing format. Cons: reviewed observations include no AAD and empty-salt acceptance; desktop would inherit them; compatibility coupling.
- **B. Separate desktop versioned AEAD container.** Pros: authenticated header/AAD, strong KDF, manifest/checksums, schema/app binding; clean safety model. Cons: no cross-restore unless a converter is built.
- **C. No local backup.** Rejected: recovery gap.

**Evidence.** Android backup covers 22 Room tables, excludes queue/cache/backup history, strips FCM tokens, is destructive on restore, and has no end-to-end restore test; crypto/validator helpers have unit tests; no desktop format exists.  
**Recommendation.** B by default: versioned encrypted container, AEAD with AAD, memory-hard KDF with random salt, manifest/record counts/checksums, explicit preview, safety snapshot, one-transaction restore, wrong-passphrase/tamper/interruption tests. Reuse `.nccb` only if cross-restore is a confirmed requirement, and then fix the reviewed weaknesses or document a converter.  
**Prerequisites.** Cross-restore decision; passphrase custody/recovery; retention; restore drills.  
**User approval.** Required.

#### D13 — Phase 1 scope

**Question.** Is the pilot all 22 modules, a staged clinical/finance slice, or a read-only shell?

**Options.**
- **A. All 22 modules before pilot.** Pros: full parity. Cons: longest exposure; no early clinical value; high rework risk.
- **B. Staged pilot: shell/auth/staff, patients, vaccination/inventory, finance/receipts, offline/outbox, backup.** Pros: covers the highest-value/highest-risk flows; proves the architecture; defers lower-risk breadth. Cons: wastage/borrow/personal reminders/notifications/updates/report polish wait.
- **C. Read-only desktop first.** Pros: lowest write risk. Cons: does not meet the clinic's offline/write need; sync/stock/finance risk stays untested.

**Evidence.** 22 specs exist; 0 implemented; Phase 1 plan already has six waves; critical risks are auth/sync/stock/finance/backup.  
**Recommendation.** B: approve all 22 as the target, but define the first pilot slice as shell/auth/staff + patients + vaccination/inventory + finance/receipts + offline/outbox + backup. Defer wastage, borrow/return, personal reminders, notifications, updater, and report polish to later Phase 1 waves. No dates or effort estimates.  
**Prerequisites.** Acceptance criteria for the pilot slice; pilot owner; rollback plan; clinical/finance sign-off.  
**User approval.** Required.

#### D14 — Build and test toolchain

**Question.** Which reproducible toolchain and packaging/release path is approved?

**Options.**
- **A. Pinned Go + Wails + Node/frontend toolchain, Windows x64 signed installer, CI/lockfiles/SBOM/rollback.** Pros: reproducible, auditable, supply-chain control. Cons: setup effort; platform dependencies.
- **B. Unpinned local builds/manual release.** Rejected: unreproducible and supply-chain risk.
- **C. Additional OS targets immediately.** Pros: broader reach. Cons: multiplies keychain/printing/signing/update work before the first release.

**Evidence.** No `go.mod`, `wails.json`, `package.json`, CI, or test suite; no desktop build has run.  
**Recommendation.** A: pin versions after a smoke build; Windows x64 first; lockfiles/dependency review/SBOM; CI builds/tests/docs/secret scan; signed installer and rollback artifact; update feed only after signing/key pinning is proven.  
**Prerequisites.** Wails smoke build; CI provider; signing identity; dependency policy; release checklist.  
**User approval.** Required.

## 5. Implementation readiness matrix

| # | Gate | Required evidence/decision | Current status | Blocking impact | Owner/action | Acceptance criteria |
|---:|---|---|---|---|---|---|
| 1 | Database contract reconciled | Live catalog + constraints + indexes, reconciled to both CSVs and migrations; baseline migration plan | **PARTIAL** — snapshot counts/chronology resolved; live catalog absent | Wrong models/queries; schema drift; no clean test DB | Backend owner: run [[Database/Live-Verification-Queries|read-only export]]; review baseline | Live table/column/key diff reviewed; 15 baseline tables confirmed; no invented schema; drift register updated |
| 2 | Live security evidence or limitation formally accepted | RLS flags/policies, ACLs, functions/triggers, Storage/Realtime, project identity | **BLOCKED** — no authorized access/tooling | Cannot certify authorization; possible PHI exposure | Security owner + project admin: run export; approve role tests or signed risk acceptance | Export reviewed; `anon`/role matrix and policies reconciled; exceptions accepted in writing |
| 3 | Auth and role model documented | ADR-0004 accepted; live `app_metadata`/profiles path; deactivation test | **PARTIAL** — source/migrations strong; live behavior untested | Wrong-role/default-role or stale-session access | Security/desktop leads: approve ADR; run approved role tests | Missing role denies; deactivated refresh fails; tokens absent from renderer |
| 4 | Offline persistence and sync design approved | ADR-0002/0003 accepted; deletion contract; replay/partial-failure design | **BLOCKED** — decisions proposed; no deletion contract | Data loss, duplicates, resurrection, false sync success | Sync owner: approve D2/D3/D4; build replay harness | Deletion contract approved; replay/partial-failure/offline tests pass |
| 5 | Inventory and finance invariants documented | Live stock trigger mode; receipt trigger; ledger/payment rules; tests | **PARTIAL** — SQL intent strong; live trigger mode unknown | Double-applied stock; negative/incorrect stock; duplicate receipts | Inventory/finance owners: live trigger evidence; approve D10/D11 | Exactly one stock writer; server receipt immutable; replay/concurrency tests pass |
| 6 | Target architecture approved | ADR-0001–0007 accepted; ADR-0008 retained; D1–D14 decisions recorded | **PARTIAL** — 0008 accepted; 1–7 proposed | Expensive rework; inconsistent clients | User/architecture owner: approve or reject decisions | Decision log reflects approvals; no silent recommendations |
| 7 | Phase 1 scope approved | Pilot slice, exclusions, acceptance criteria, owner | **OPEN** — 22 specs; staged pilot proposed | Scope creep; delayed clinical value; unclear release | Product/clinic owner: approve D13 | Signed scope with in/out list and acceptance criteria |
| 8 | Build and test toolchain confirmed | Reproducible Go/Wails/Node build; CI; test commands; packaging spike | **BLOCKED** — no manifests/CI/tests | No verifiable build or release; supply-chain risk | Engineering lead: D14 spike; add CI and instructions | Clean clone build + tests + docs/secret checks pass on target OS |
| 9 | Local encryption, backup, and retention approved | ADR-0002/D12; key custody; retention; restore drill | **BLOCKED** — no approved encryption/backup/retention | PHI exposure or unrecoverable data | Security/clinical owners: approve D2/D12; retention policy | No plaintext PHI; restore/interruption/tamper tests pass; retention signed |

**Overall:** the architecture review is decision-ready, but implementation is **blocked on specified evidence and approvals**, not on documentation polish.

## 6. Documentation changes for this pass

### 6.1 Files that needed correction or extension

- `Database/Database-Architecture.md`: add the reconciliation/chronology and correct speculative ordinal-gap wording.
- `Database/Data-Dictionary.md`: correct the unsupported `vaccination_items` key rows; add the exact 55-row delta; correct ordinal-gap wording.
- `Database/Access-Patterns.md`: correct ordinal-gap wording and link the reconciliation.
- `Audits/Initial-Audit.md`: correct AUD-015/“ordinal gaps suggest omitted columns.”
- `Audits/Shared-Backend-Connection-Investigation.md`: correct ordinal-gap/completeness wording and link the new chronology.
- `Audits/Documentation-Validation.md`: add a Phase 0B addendum for the new reconciliation and P0B-DOC-01/P0B-DOC-02.
- `Audits/Technical-Debt.md`: correct TD-006 money evidence and TD-001 baseline evidence.
- `Product/Product-Vision.md`: clarify that the shared schema is `numeric` and the Android client uses `Double`.
- `Audits/Final-Report.md`: add Phase 0B stage, current counts/links, and the new conclusion.
- `Home.md`: add the Phase 0B/reconciliation entry points and current gate status.
- `README.md`: add the new evidence/readiness links.
- `Audits/Risk-Register.md`: add the Phase 0B gate/blocker register.
- `Decisions/ADR-0007-Money-Dates-and-Identity.md`: correct the evidence context from “schema uses floats” to `numeric` schema + Android `Double` mapping. Status remains Proposed; the integer-paise decision is unchanged.
- Other ADRs: **no status changes.** The evidence supports review, not silent approval. ADR-0008 remains accepted; ADR-0001–0007 remain proposed.
- Skills: **no changes required.**

### 6.2 New notes

- `Database/Schema-Reconciliation.md` — table-by-table evidence, chronology, causes, and limitations.
- `Database/Live-Verification-Queries.md` — exact read-only SQL and reconciliation procedure.
- `Audits/Phase-0B-Architecture-Review.md` — this decision review and readiness matrix.

No application source, migration, schema, RLS policy, grant, Supabase setting, dependency, Android file, or credential was changed.

## 7. Git state

**Desktop:** `main` at `241e0b9`; **64 tracked files modified** and **4 untracked notes**. The tracked set is the 43 pre-existing corrected notes, 17 skill files, the repository README, and two pre-existing `.obsidian` UI-state files, plus the previously clean `Database/Data-Dictionary.md` corrected here. The four untracked notes are the prior `Audits/Documentation-Validation.md` and the three new Phase 0B notes. `git diff --stat` reports 64 files changed, 328 insertions, 275 deletions; all changes are documentation, skill text, repository README, or pre-existing `.obsidian` UI state. No application source, migration, schema, RLS policy, grant, Supabase setting, dependency, Android file, or credential was changed.

**Android:** `main` at `ca4bed4`, clean against `origin/main`. No Android file was modified.

**No commit or push was performed.** All desktop documentation changes remain uncommitted for review.

## 8. Decisions requiring user approval

1. **D1:** Wails baseline and Windows-first OS matrix.
2. **D2:** SQLCipher-compatible local encryption and key recovery.
3. **D3:** per-entity PostgREST sync groups; no new server RPC by default.
4. **D4:** soft-delete/absence deletion contract; no client hard deletes.
5. **D5:** Go-owned auth and `app_metadata` role authority.
6. **D6:** typed Wails-only boundary.
7. **D7:** layered tests and signed/rollback release gates.
8. **D8:** integer paise, typed dates/IST, UUID + clinic ID, server receipts.
9. **D9:** cache ownership/invalidation.
10. **D10:** inventory single-writer/trigger mode after live evidence.
11. **D11:** immutable server receipts and one canonical payment per visit.
12. **D12:** desktop backup format and cross-restore decision.
13. **D13:** staged pilot scope.
14. **D14:** pinned toolchain and packaging path.

## Conclusion

**BLOCKED ON SPECIFIED EVIDENCE**

The database discrepancy is explained at file level and the architecture is ready for a decision review, but live schema/security evidence and the D1–D14 approvals are still required. The blockers are the exact read-only export in [[Database/Live-Verification-Queries|Live Verification Queries]], the stock-trigger mode, the deletion/absence contract, and user approval of the proposed architecture. No implementation should start before those gates close.
