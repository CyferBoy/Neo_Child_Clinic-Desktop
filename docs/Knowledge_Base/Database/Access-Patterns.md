---
title: Database Access Patterns
doc_status: baseline
evidence: migrations + Android source/repositories + RLS analysis + shared-backend investigation
updated: 2026-10-20
---

# Database Access Patterns

> **Do not treat this as a live RLS certification.** The repository shows intent and policy SQL. The hosted project may differ. Every access rule below needs a live verification query before release.

## Authorization model

`[VERIFIED]` The Android client reads the role from `app_metadata.role` and sends the user's Supabase JWT. RLS functions read the JWT claim. The desktop must do the same.

`[INFERRED]` The database is a **single-clinic** model. Most clinical tables grant active staff broad read/write access. It is not a per-doctor or per-department authorization model. UI restrictions (for example, patient edit only for admin/doctor) are narrower than the likely RLS surface.

## Existing client access path

`[VERIFIED]` Android reaches the database through HTTPS Supabase APIs, not a direct PostgreSQL connection:

| Path | Verified source | Desktop implication |
|---|---|---|
| Auth | `SupabaseModule` installs `Auth`; `AuthViewModel.login` uses email/password | Use the same Auth users; no second identity store |
| PostgREST | 21 direct `postgrest.from(...)` targets plus `patient_notes` through `SyncUploader` | Same tables/columns and user JWT; no direct database driver |
| RPC | No `postgrest.rpc(...)` calls found | Do not invent RPCs; server-side receipt/stock logic is trigger/function driven |
| Edge Functions | Only `manage-staff` is invoked by Android | Reuse for staff lifecycle; keep service role server-side |
| Storage | `patient-docs` private bucket via user session | Same bucket/policy; no desktop-only bucket |
| Realtime | `patients`/`patient_visits`/`consultations` and todo tables; refresh trigger only | Subscribe for freshness, then reconcile from PostgREST |
| Local database | Room 25 entities, SQLCipher, `sync_queue` outbox | SQLite is a working copy, not a second backend |

`[VERIFIED]` The older Android-repository CSV is stale: it lists 23 tables/361 columns and camelCase `waste_records` names, while current migrations and source use snake_case and soft-delete fields. The newer desktop CSV lists 24/416 but still has ordinal gaps and no connection/policy fields. Neither CSV is a schema authority.

`[DECISION]` Both clients must target the **same existing Supabase project**; see [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]. No new project, separate database, duplicate tables, or parallel schema is approved.

## Policy summary

| Table group | Read | Write | Notes |
|---|---|---|---|
| Patients, visits, notes, vaccination items, reminders, vaccines, batches, inventory, finance, consultations, borrow, waste | Active staff | Active staff | Broad single-clinic access; verify specific policies |
| Audit logs | Staff select; append insert | No update/delete | Intended append-only; verify legacy permissive policies |
| Expenses | Active staff select/insert | Admin/doctor update/delete | Role policies exist; accountability trigger missing |
| Doctor slots/exceptions | Authenticated read | Admin or owning doctor | `doctor_id = auth.uid()` checks |
| Profiles | Active staff can read broadly | Own-row update; privileged fields guarded | NSC-001 over-read; admin edge function for lifecycle |
| User devices | Own rows | Own rows plus staff rules | Push/device registration |
| Receipt sequences | No client access | No client access | Security-definer functions assign numbers |
| Rate limits | No client access | No client access | Internal only |
| Todo notification events | No client access | No client access | Internal; live status unknown |

## Query patterns

### Patient search
- Search by name, clinic ID, phone.
- Current Android search uses `LIKE` patterns; an unindexed address is a confirmed low-severity finding.
- Desktop should use trigram/full-text or normalized search columns, with a result cap and pagination.
- Never fetch all patients to filter in the renderer.

### Patient timeline
- Join visits, vaccinations, consultations, payments, reminders, notes, and audit by patient ID.
- Avoid N+1 queries. The Android `refreshPatients` path has a known N+1; the desktop should use set-based reads.
- Invalidate the timeline on any dependent write, not only the patient row.

### Due list
- Filter by due date, status, category, and soft-delete state.
- Use IST date boundaries.
- Do not rely on formatted text sorting.
- Apply tombstones during pull.

### Inventory
- Aggregate stock from batches, excluding expired batches where the reference does.
- Use a single ledger path for deductions.
- Read batch quantities transactionally; do not use read-modify-write without a version/guard.
- Reconcile server trigger effects; the Android KB records trigger double-apply and update-arithmetic defects.

### Finance and reports
- Payments are per visit/consultation with cash/online split.
- A visit's vaccination income should have one deterministic identity.
- Exclude soft-deleted rows consistently.
- Use integer minor units in the desktop; convert at the shared-schema boundary.
- Receipt numbers come from the database function, not a local sequence.

### Audit
- Read paged, newest first, with patient/entity filters.
- Write through an append-only path.
- Never expose update/delete controls.
- Log the actor from the session/server, not a renderer-supplied string.

### Sync
- Upload in dependency order within a transaction group.
- Pull by cursor with a safety overlap.
- Apply tombstones.
- Reject unknown columns/shapes with a visible schema-drift error.
- Do not let a stale pull overwrite an unacknowledged local write.

## Index and performance notes

`[VERIFIED]` repository migrations include index hardening in `20261016_rls_index_and_stock_trigger_hardening.sql`, but index coverage is not a substitute for query review. The existing KB records an unindexed `user_devices(user_id)` and an unindexed patient address search.

`[PROPOSED]` Desktop query budgets:
- Patient search: bounded result set, indexed prefix/trigram.
- Timeline: one set of batched queries, not per-row.
- Due list: indexed status/date/category.
- Inventory: indexed vaccine/batch/expiry.
- Reports: pre-aggregated or bounded date windows; no unbounded full-table scans on the UI thread.

## Security requirements

| ID | Requirement |
|---|---|
| DB-001 | Every desktop request uses the signed-in user's JWT; no service-role key is shipped. |
| DB-002 | RLS is verified with at least two roles and a deactivated account through an approved non-destructive path against the existing project. A separate test harness requires explicit approval and must not become the desktop backend. |
| DB-003 | The desktop queries only the columns it needs; no blanket `select *` on PHI tables. |
| DB-004 | Every mutation is parameterized and validated server-side; the client is not the only validator. |
| DB-005 | Receipt numbers and stock arithmetic are server-authoritative where the schema makes them so. |
| DB-006 | Audit writes are append-only and attributable to the authenticated actor. |
| DB-007 | Both clients use the same existing Supabase project/schema; no new project, separate database, duplicate tables, or parallel schema. Verify with a redacted project fingerprint. |

## Open questions

- What is the actual hosted project identity, and how is it verified without exposing secrets?
- Are broad active-staff policies intentional for a small trusted clinic, or a temporary simplification?
- Which role should be allowed to read clinical notes versus demographics?
- Can the desktop use RPCs for multi-table writes, or must it issue ordered PostgREST calls?
- What is the live grant state for tables not covered by migration `GRANT` statements?
- Are there legacy policies that OR with the new role policies?
- What is the approved verification path for deactivated-account and cross-client tests?

## Related

[[Database/Database-Architecture|Database Architecture]] · [[Security/Security-Model|Security Model]] · [[Security/Threat-Model|Threat Model]] · [[Features/17-Supabase-Sync|Supabase Sync]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
