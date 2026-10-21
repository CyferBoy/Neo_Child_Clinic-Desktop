---
title: Database Access Patterns
doc_status: baseline
evidence: migrations + Android source/repositories + RLS analysis + shared-backend investigation + Phase 0C Supabase metadata exports (no SQL executed)
updated: 2026-10-21
---

# Database Access Patterns

> **Do not treat this as a live RLS certification.** The repository shows intent and policy SQL; the 2026-10-21 exports report deployed policies/ACLs but were not executed against the API. Runtime authorization remains unverified. Every access rule below needs a role-specific test before release.

> **Phase 0C critical caveat.** The reported state is not the target model. `anon` has full table grants on 22 tables and a legacy policy path to ten clinical/inventory tables; `reminders` allows any authenticated user all operations; all 21 functions are anon-executable. See [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] §4 before using this page as an implementation contract.

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

`[VERIFIED]` The older Android-repository CSV is stale: it lists 23 tables/361 columns and camelCase `waste_records` names, while current migrations and source use snake_case and soft-delete fields. The newer desktop column CSV lists 24/416 and is corroborated by the independent 2026-10-21 column export. The separate metadata exports report keys, indexes, policies, and grants, but neither column CSV is a schema authority and no export proves runtime access. Ordinal gaps are consistent with dropped columns, not proof of omitted rows. See [[Audits/Phase-0C-Schema-Export-Review|Phase 0C]] and [[Database/Schema-Reconciliation|Schema Reconciliation]].

`[DECISION]` Both clients must target the **same existing Supabase project**; see [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]. No new project, separate remote PostgreSQL database, duplicate remote tables, or parallel remote schema is approved. The local SQLite working copy is expected.

## Policy summary (reported by export, not runtime-tested)

| Table group | Reported read | Reported write | Notes |
|---|---|---|---|
| `patients`, `patient_visits`, `patient_notes`, `consultations`, `vaccination_items`, `vaccines`, `vaccine_batches`, `inventory_transactions`, `waste_records`, `borrow_records` | Active staff **and `anon`** | Active staff **and `anon`** | Legacy `{public}` `ALL` policies pass because `get_my_role()` falls back to `'nurse'`; critical |
| `reminders` | **Any authenticated user** | **Any authenticated user** | `{authenticated}` `ALL` with `USING (true)`/`WITH CHECK (true)`; no active-staff predicate |
| `finance_transactions` | Active staff plus legacy role path | Active staff plus legacy role path | Anon fails because `nurse` is not in the legacy role list |
| `audit_logs` | Active staff | **Any authenticated insert** | No update/delete policy; insert predicate is only `auth.uid() IS NOT NULL` |
| `expenses` | Active staff select/insert | Admin/doctor update/delete | Role policies exist; accountability trigger missing |
| Doctor slots/exceptions | Active staff read | Admin or owning doctor | `doctor_id = auth.uid()` checks; exceptions lack Android's `start_minute`/`end_minute` |
| `profiles` | Active staff can read broadly | Own-row update; privileged fields guarded; legacy `{public}` admin `ALL` | Role-source split: `profiles.role` vs `app_metadata.role` |
| `user_devices` | Own rows | Own rows plus staff rules | Legacy owner policies do not require active staff |
| `receipt_sequences` | No policy; direct RLS-denied | No policy; direct RLS-denied | Four DML grants exist for anon/auth; `neo_next_receipt_number()` is anon-executable |
| `api_write_rate_limits` | No client ACL/policy | No client ACL/policy | Internal only |
| `borrow_returns`, `consultation_todos`, `vaccination_todos`, `personal_vaccine_reminders` | Active staff | Active staff | No explicit grants; not Oct 30-ready |
| `todo_notification_events` | No client policy in migrations | No client policy in migrations | Absent from export; live status unknown |

## Query patterns

### Android query dependency map

`[VERIFIED]` The Android source contains these feature/query surfaces. The table names are the reported server dependencies or the local data they project; it is a dependency map, not a claim that every request uses every table.

| Android surface | Source evidence | Primary server/local data | Notes |
|---|---|---|---|
| Authentication/session | `core/security/`, `feature/auth/` | Supabase Auth, `profiles` | Role from `app_metadata.role`; session storage is Keystore-backed |
| Staff management | `feature/staff/`, `manage-staff` function | `profiles`, `audit_logs` | Server function owns privileged Auth/profile changes |
| Patients | `feature/patient/`, `PatientDao` | `patients`, `patient_visits`, `patient_notes`, patient todo tables, Storage documents | Search is broad `LIKE`; merges affect dependents |
| Vaccinations | `feature/vaccination/` | `patient_visits`, `vaccination_items`, `vaccines`, `vaccine_batches`, `inventory_transactions`, `reminders`, `finance_transactions` | Visit aggregate; stock/reminder/payment effects |
| Consultations | `feature/consultation/` | `consultations`, `patient_visits`, `finance_transactions`, consultation todos | Linked to visit/patient |
| Inventory | `feature/inventory/` | `vaccines`, `vaccine_batches`, `inventory_transactions` | Ledger + batch projection |
| Wastage | `feature/waste/` | `waste_records`, `vaccine_batches`, `inventory_transactions` | Reason and batch required |
| Borrow/return | `feature/borrowed/` | `borrow_records`, `borrow_returns`, `vaccine_batches`, `inventory_transactions` | Partial returns and outstanding balance |
| Vaccination reminders | `feature/reminder/` | `reminders`, `patients`, `patient_visits`, `vaccination_items` | IST due classification; terminal states |
| Personal reminders | `feature/personalreminder/` | `personal_vaccine_reminders`, `patients`, `vaccines` | Separate from clinical reminders |
| Finance | `feature/finance/` | `finance_transactions`, `expenses`, `patient_visits`, `consultations` | Split payment and one-income identity |
| Receipts | Receipt service/function | `receipt_sequences`, `patient_visits`, `finance_transactions` | Server-assigned number; anon execution is a reported defect |
| Dashboard | `feature/dashboard/` | Projections over patients, visits, reminders, batches, finance, todos | Read-only; must match detail definitions |
| Statistics/reports | `feature/statistics/` | Patients, visits, vaccination items, vaccines, finance, expenses, waste | Date-bounded, deleted rows excluded |
| Sync | `core/sync/` | Public tables in the sync contract plus local outbox/cursors | Pull/push boundaries are not fully documented |
| Audit | `feature/audit/` | `audit_logs` | Append-only intent; exported insert policy is too broad |
| Storage | `SupabaseModule`, patient document code | `storage.objects`, `patient-docs` bucket | Bucket policy unverified |
| Realtime | `RealtimeChangeSubscriptions` | Published tables | Debounced refresh; authorization unverified |
| Updates | `feature/update/`, `notify-update` function | No business table; release metadata | Signature/rollback not verified |
| Settings | `feature/settings/` | Local preferences; server policy not evidenced | No clinic-settings table in export |

### Patient search
- Search by name, clinic ID, phone.
- Current Android search uses `LIKE` patterns; an unindexed address is a confirmed low-severity finding.
- Desktop should use trigram/full-text or normalized search columns, with a result cap and pagination.
- Never fetch all patients to filter in the renderer.

### Patient timeline
- Join visits, vaccinations, consultations, payments, reminders, notes, and audit by patient ID.
- Avoid N+1 queries. The former Android `refreshPatients` N+1 was fixed at `b27d945`; the desktop should still use set-based reads.
- Invalidate the timeline on any dependent write, not only the patient row.

### Due list
- Filter by due date, status, category, and soft-delete state.
- Use IST date boundaries.
- Do not rely on formatted text sorting.
- Apply the approved deletion/absence reconciliation contract during pull. No server tombstone feed is present in repository evidence; live status is unverified.

### Inventory
- Aggregate stock from batches, excluding expired batches where the reference does.
- Use a single ledger path for deductions.
- Read batch quantities transactionally; do not use read-modify-write without a version/guard.
- Reconcile server trigger effects. The 2026-10 export reports **two** stock triggers and the **old** `update_batch_stock()` body, so the double-apply defect is not fixed live; `20261017` did not take effect and its guard would fail as written. Do not enable inventory writes until the duplicate is removed and one writer is verified.

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
- Apply the approved deletion/absence reconciliation contract.
- Reject unknown columns/shapes with a visible schema-drift error.
- Do not let a stale pull overwrite an unacknowledged local write.

## Index and performance notes

`[REPORTED]` The 2026-10-21 export lists 93 indexes (33 unique), but index coverage is not a substitute for query review. Duplicate unique indexes/constraints exist on `patients`, `reminders`, `profiles`, and `user_devices`, so upsert conflict targets are ambiguous. The existing KB records an unindexed `user_devices(user_id)` and an unindexed patient address search; the export's index names are not mapped to those access paths.

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
| DB-002 | RLS **and** table/function grants are verified with `anon`, a non-staff authenticated account, active staff, a deactivated account, and server-side paths through an approved non-destructive test. A separate test harness requires explicit approval and must not become the desktop backend. |
| DB-003 | The desktop queries only the columns it needs; no blanket `select *` on PHI tables. |
| DB-004 | Every mutation is parameterized and validated server-side; the client is not the only validator. |
| DB-005 | Receipt numbers and stock arithmetic are server-authoritative where the schema makes them so; `anon` must not execute receipt/stock functions. |
| DB-006 | Audit writes are append-only and attributable to the authenticated actor; only approved server/active-staff paths may insert. |
| DB-007 | Both clients use the same existing Supabase project/schema; no new project, separate remote PostgreSQL database, duplicate remote tables, or parallel remote schema. Local SQLite is expected. Verify with a redacted project fingerprint. |
| DB-008 | Every new table/function has explicit least-privilege grants, including the intended `service_role` path, and is re-verified after the 2026-10-30 Data API change. |

## Open questions

- What is the actual hosted project identity, and how is it verified without exposing secrets?
- Are broad active-staff policies intentional for a small trusted clinic, or a temporary simplification?
- Which role should be allowed to read clinical notes versus demographics?
- Can the desktop use RPCs for multi-table writes, or must it issue ordered PostgREST calls?
- Who owns remediation of the broad exported grants, the seven tables without explicit grants, and the anon-executable functions?
- Which legacy `{public}` policies will be dropped, and what negative tests prove the `'nurse'` fallback no longer authorizes anon?
- What is the approved verification path for anon, deactivated-account, non-staff, and cross-client tests?

## Related

[[Database/Database-Architecture|Database Architecture]] · [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] · [[Security/Security-Model|Security Model]] · [[Security/Threat-Model|Threat Model]] · [[Features/17-Supabase-Sync|Supabase Sync]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
