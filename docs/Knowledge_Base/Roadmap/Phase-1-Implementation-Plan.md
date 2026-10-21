---
title: Phase 1 Implementation Plan
doc_status: proposed
evidence: 22 feature specifications + audit + Phase 0C Supabase metadata exports (no SQL executed)
updated: 2026-10-21
---

# Phase 1 Implementation Plan

> **Proposed sequence, no dates.** Each step ends at a verifiable gate. Do not start a dependent step while its gate is open.

## Workstreams

| ID | Workstream | Output | Owner role |
|---|---|---|---|
| W0 | Repository and CI | Build, lint, tests, docs checks, dependency scan | Engineering lead |
| W1 | Backend readiness | Existing Supabase project verification, baseline reconciliation, RLS tests, functions | Backend owner |
| W2 | Desktop core | Wails shell, typed bindings, local DB, migrations, keychain | Desktop lead |
| W3 | Sync | Outbox, groups, idempotency, pull cursor, deletion reconciliation (contract TBD), retries | Sync owner |
| W4 | Clinical | Patients, vaccinations, consultations, reminders | Clinical lead |
| W5 | Inventory | Catalog, batches, ledger, waste, borrow/return | Inventory lead |
| W6 | Money | Finance, expenses, receipts, printing | Finance lead |
| W7 | Insight/ops | Dashboard, reports, audit, settings, notifications, updates | Product/ops lead |
| W8 | Assurance | Threat model, test strategy, backup drills, accessibility, release | QA/security lead |

## Step sequence

### Step 0 — Control the workspace
Deliverables: existing Git repository; add `AGENTS.md`, issue/PR templates, docs location, and CI skeleton; confirm/configure branch protection in GitHub settings.
Gate: clean clone builds a hello-world Wails app and docs validation runs; no secrets committed.

### Step 1 — Make the existing backend verifiable
Deliverables: approved non-destructive access to the existing Supabase project; reconcile the 2026-10-21 metadata exports against the catalog, migrations, and Android contract; confirm or remediate the anon/legacy-policy path; inventory explicit table/function grants; baseline migration/reconciliation; RLS test harness; synthetic seed data.
Gate: **Phase 0C critical findings are confirmed or disproved and closed or formally risk-accepted**; baseline evidence reviewed; role matrix tests pass for `anon`, non-staff authenticated, active staff, and server-side paths; explicit grants verified for new tables and functions; no new project or remote database; no production data mutation; no production credentials in the desktop test client; local SQLite is expected.

### Phase 0C backend-readiness matrix

The exports make the schema **structurally known**, but they do not certify runtime security. No Step 2 trust-boundary work should start until the critical items below are closed or explicitly accepted by the owners.

| Area | Phase 0C evidence | Status | Required before desktop connection |
|---|---|---|---|
| Schema shape | 24 tables/416 columns/77 constraints/93 indexes reported; two column exports agree | **PARTIAL** | Approve the reviewed catalog/baseline; record the six live-only columns |
| Baseline/reproducibility | 15 tables lack `CREATE TABLE`; six columns not reproducible; `todo_notification_events` absent | **BLOCKED** | Reviewed baseline migration and clean-rebuild or signed exception |
| RLS/legacy policies | 179 policies; 13 tables retain `{public}` policies; 10 pass for anon | **BLOCKED — critical** | Confirm with anon test; remove/replace legacy policies; fail closed |
| Table grants | 22 tables full anon/auth; `receipt_sequences` four DML; `api_write_rate_limits` none | **BLOCKED** | Least-privilege reconciliation; anon no business access |
| Default ACL/Oct 30 | Seven migration-created tables have no explicit grant; broad default ACLs | **BLOCKED** | Forward grants for seven tables including `service_role`; re-export after 2026-10-30 |
| Functions | 21 functions anon-executable; two `SECURITY DEFINER` without `search_path` | **BLOCKED** | Revoke/allowlist; verify `handle_new_user` and signup role path |
| Stock | Two triggers, old function; `20261017` guard fails as written | **BLOCKED** | Exactly one writer; corrected function; replay/reconciliation |
| Scheduling contract | `doctor_slot_exceptions` lacks `start_minute`/`end_minute` that Android sends | **BLOCKED** | Approve schema addition or stop sending the fields; test upsert |
| Storage/Realtime | One `storage.objects` policy; no buckets; 23 published tables | **PARTIAL** | List buckets, verify private access, review publication necessity and Realtime RLS |
| Project identity | No URL/ref/issuer in exports | **BLOCKED** | Approved config + redacted same-project fingerprint |
| Auth/migration history | Signup state, trigger attachment, migration ledger not exported | **UNKNOWN** | Verify Auth settings, trigger, and `schema_migrations` |

**Gate rule:** any row marked **BLOCKED — critical** or **BLOCKED** that affects PHI, stock, receipts, or the same-project contract cannot be waived silently. A written owner acceptance must state the exposure, the interim control, and the expiry/review date.

### Step 2 — Prove the trust boundary
Deliverables: auth spike, keychain storage, typed Wails binding, local DB open/migrate, PHI-safe logging.
Gate: login/refresh/logout/revoke; renderer cannot access tokens or DB; redaction test passes.

### Step 3 — Prove offline write and sync
Deliverables: outbox schema, transaction group, idempotent patient create, retry/backoff, duplicate/replay tests.
Gate: network loss/restart preserves the write; replay creates one row; 401/403/409/429/500 paths classified.

### Step 4 — Patient vertical slice
Deliverables: registration, search, detail, edit, merge, notes/todos/documents scope, audit, dashboard count.
Gate: offline create/search; duplicate clinic ID handling; merge conflict test; no stale timeline after edit.

### Step 5 — Vaccination + inventory vertical slice
Deliverables: catalog, batches, vaccination transaction, stock ledger, due reminder, payment, receipt link.
Gate: one logical transaction; stock arithmetic replay; due-date IST test; receipt number from server; failure rollback.

### Step 6 — Consultation + finance slice
Deliverables: consultation create/edit, follow-up, cash/online/mixed payment, expense, receipt print preview.
Gate: one payment per visit identity; totals match; receipt immutable; print failure does not lose payment.

### Step 7 — Operations slice
Deliverables: waste, borrow/return, personal reminders, notifications, audit viewer, reports, settings.
Gate: stock ledger reconciles; audit append-only; report golden data; notification preference behavior.

### Step 8 — Recovery and release
Deliverables: backup export/restore, sync repair tooling, updater, signed builds, release checklist.
Gate: restore round-trip and interruption tests; signed update and rollback; pilot acceptance.

## Vertical slice contract

Every slice must include:
- specification and requirement IDs;
- UI states: loading, empty, ready, offline, error, permission denied, saving, conflict where applicable;
- local transaction and outbox behavior;
- authorization checks;
- audit intent;
- automated tests;
- manual acceptance evidence;
- documentation update.

## Environments

| Environment | Purpose | Data |
|---|---|---|
| Local dev | Fast feedback | Synthetic |
| CI | Build/test/lint/docs | Synthetic |
| Shared-backend verification | RLS, functions, sync contracts against the existing project | Approved test accounts and synthetic/reversible rows; no new backend |
| Pre-release/pilot | Release candidate against the existing project | Synthetic or approved de-identified data; no production mutation without approval |
| Production | Clinic | Real PHI; no developer direct access |

**No separate desktop backend.** If a disposable harness is proposed for destructive tests, it requires explicit approval and must never become the desktop backend. A test harness is not a production database, and the local SQLite working copy is not a second backend.

## Data migration

No production data migration is authorized by this plan. If local Android data must be imported, a separate approved runbook is required with backup, field mapping, duplicate handling, and reconciliation.

## Phase 1 exit criteria

- All 22 module specs accepted.
- P0 risks closed or explicitly accepted.
- Phase 0C blockers B-0C-01–B-0C-10 closed or formally risk-accepted; anon has no PHI/inventory access and `reminders` is staff-scoped.
- Explicit grants verified for every new table/function, including after the 2026-10-30 Data API change.
- Stock has exactly one verified writer and ledger/batch reconciliation passes.
- Desktop tests and RLS/role tests green.
- Backup restore drill passed.
- Signed build and rollback passed.
- Pilot acceptance signed by clinical, operations, and security owners.

## Related

[[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Roadmap/Dependencies-and-Milestones|Dependencies and Milestones]] · [[Roadmap/Requirements-Traceability|Requirements Traceability]] · [[Releases/Release-Checklist|Release Checklist]] · [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
