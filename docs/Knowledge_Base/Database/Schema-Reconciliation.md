---
title: Schema Reconciliation — Phase 0B
doc_status: baseline
evidence: desktop CSV 24/416 + Android CSV 23/361 + 23 repository migrations + Android Kotlin/Room/PostgREST + security SQL; no live access
updated: 2026-10-20
---

# Schema Reconciliation — Phase 0B

> **Read-only reconciliation.** No database, migration, schema, RLS policy, grant, trigger, Supabase setting, Android file, or application dependency was changed. No live query was run. The CSVs are snapshots, not live catalog exports.

## 1. Scope and evidence

| Source | What it proves | What it does not prove |
|---|---|---|
| Desktop CSV `Supabase Snippet List Public Table Columns.csv` | 24 tables, 416 column rows, explicit `public` schema, column order/type/nullability/default | Capture time, project identity, keys, indexes, policies, grants, live completeness |
| Android CSV `supabase/migrations/Supabase Snippet Full Schema Catalog (Tables, Keys, Indexes).csv` | 23 tables, 361 column rows, older column shapes | Schema name (no schema column), keys/indexes despite its filename, live deployment, completeness |
| `supabase/migrations/*.sql` (23 files) | Forward migration intent, created tables, altered tables, policies, functions, triggers | Whether every migration was deployed, missing baseline, manual changes, actual policy/trigger state |
| Android Kotlin/Room/PostgREST | Client table access, local foreign keys, sync payload shapes | Remote keys/constraints or live authorization |
| `supabase/verify_security.sql`; `supabase/tests/rls_role_test.sql` | Existing read-only inspection queries; non-read-only role-test intent with placeholders | Neither was run; no live security certification |

**Source codes used below:** `D` desktop CSV; `A` Android CSV; `M` repository migration SQL; `K` Android Kotlin/Room/PostgREST; `S` existing security SQL/docs. `Live` is never a source in this note.

All table names below are in the `public` schema. The desktop CSV states this explicitly. The Android CSV has no schema column; `public` is the only schema used by the inspected client and migrations, not a live fact.

## 2. Counts verified against the files

| Metric | Desktop CSV | Android CSV | Difference |
|---|---:|---:|---:|
| Tables | 24 | 23 | +1 desktop (`api_write_rate_limits`) |
| Column rows | 416 | 361 | +55 desktop |
| Shared tables | 23 | 23 | — |
| Desktop-only tables | 1 | 0 | `api_write_rate_limits` |
| Android-only tables | 0 | 0 | — |

The reported counts are correct for the files. The 55-row difference is fully explained by migration-visible changes; it is **not** a count of production tables missing.

## 3. What changed between the snapshots

### 3.1 Exact column arithmetic

`55 = 45 + 4 + 3 + 3`

| Change | Tables | Rows | Migration evidence |
|---|---|---:|---|
| Added `is_deleted`, `deleted_at`, `deleted_by` | 15 tables × 3 | 45 | `20260925_business_soft_delete_columns.sql` |
| Added `deleted_at`, `deleted_by` (`is_deleted` already in Android CSV) | `doctor_slot_exceptions`, `expenses` (2 × 2) | 4 | Same migration; both tables already had `is_deleted` in the older snapshot |
| `waste_records`: 8 camelCase columns renamed, 3 soft-delete columns added | 1 × 11 added − 8 removed | +3 net | `20260919_waste_records_snake_case.sql`; `20260925_business_soft_delete_columns.sql` |
| Desktop-only `api_write_rate_limits` | 1 × 3 | 3 | `20260929001000_write_rate_limit.sql` |

The 15 tables with the three soft-delete additions are:

`borrow_records`, `borrow_returns`, `consultation_todos`, `consultations`, `doctor_weekly_slots`, `finance_transactions`, `patient_notes`, `patient_visits`, `patients`, `personal_vaccine_reminders`, `reminders`, `vaccination_items`, `vaccination_todos`, `vaccine_batches`, `vaccines`.

`waste_records` adds `deleted_at`, `deleted_by`, `is_deleted`; renames `batchId→batch_id`, `batchNumber→batch_number`, `brandName→brand_name`, `dateWasted→date_wasted`, `expiryDate→expiry_date`, `isSynced→is_synced`, `updatedAt→updated_at`, `vaccineId→vaccine_id`. The migration states that the primary key and both foreign keys are preserved by the renames.

### 3.2 Snapshot chronology `[INFERRED, high confidence]`

- The Android CSV still has `waste_records` camelCase columns, so it predates `20260919_waste_records_snake_case.sql`.
- It has `doctor_slot_exceptions.is_deleted` but not `deleted_at`/`deleted_by`. That column existed at creation (`20260911`), was dropped by `20260919_remove_soft_delete.sql`, and was re-added with the other two by `20260925`. Combined with camelCase waste, the snapshot is bracketed between `20260911` and `20260919`.
- The desktop CSV has the full soft-delete set on those tables and `api_write_rate_limits`, so it is after `20260929`.
- No common column changed `data_type`, `is_nullable`, or `column_default` between the two snapshots. The differences are additions and the waste rename, not type drift.

This chronology explains the table/column counts without assuming missing production tables. It does **not** prove either snapshot was taken from production, nor that the migration order was applied live in this order.

## 4. Table-by-table reconciliation

**Legend.** `Repo`: `C` = created by a repository migration; `B` = baseline table assumed to pre-exist (repository SQL alters/policies it, but no `CREATE TABLE`); `U` = only conditional policy/trigger SQL, no create. `Android`: `K` = direct PostgREST and/or Room/DAO references; `none` = no client reference. `Delta`: `SD` = `is_deleted`/`deleted_at`/`deleted_by`; `none` = no common-column difference. `RLS`: migration intent only; `AS-CRUD` = active-staff select/insert/update/delete; `AS-R/I` = select+insert only; `P-select` = active-staff select, no client write; `OWN` = owner-scoped; `ROLE` = role/owner carve-outs; `REVOKE` = enabled + revoked, no client policy; `COND` = conditional enable/force + no client read policy. Every row's live state is `[UNKNOWN]`.

| Table (all `public`) | D/A cols | Repo | Android | Column/type delta | Keys / relationships | RLS evidence | Src | Confidence / unresolved |
|---|---:|---|---|---|---|---|---|---|
| `api_write_rate_limits` | 3/0 | C | none (server-only) | D-only +3 | PK `(user_id, window_started_at)` (M) | REVOKE; no client policy (M) | D,M | High files; live table/deployment unknown |
| `audit_logs` | 17/17 | B | K: PostgREST + Room | none | PK `id`; `patient_id` logical, no declared FK | AS-R/I; no update/delete policy | D,A,M,K | High files; live append-only behavior unknown |
| `borrow_records` | 18/15 | B | K: PostgREST + Room | +3 SD | PK `id`; `vaccine_id`, `batch_id` FKs in Room (K) | AS-CRUD | D,A,M,K | High files; live FKs unknown |
| `borrow_returns` | 14/11 | C | K: PostgREST + Room | +3 SD | PK `id`; FKs to `borrow_records` and `vaccine_batches` (M/K) | AS-CRUD | D,A,M,K | High files; live FKs unknown |
| `consultation_todos` | 18/15 | C | K: PostgREST + Room | +3 SD | PK `id`; `patient_id → patients` (M) | AS-CRUD | D,A,M,K | High files; live FK unknown |
| `consultations` | 21/18 | B | K: PostgREST + Room | +3 SD | PK `id`; `patient_id`, `visit_id` (K); `availability_slot_id → doctor_weekly_slots` (M) | AS-CRUD | D,A,M,K | High files; live FKs unknown |
| `doctor_slot_exceptions` | 14/12 | C | K: PostgREST + Room | +2 (deleted_at/by; `is_deleted` already in A) | PK `id`; `doctor_id → profiles`, `weekly_slot_id → doctor_weekly_slots` (M) | ROLE: active-staff read; admin/owning doctor write | D,A,M,K | High files; live policy expressions unknown |
| `doctor_weekly_slots` | 14/11 | C | K: PostgREST + Room | +3 SD | PK `id`; `doctor_id → profiles` (M) | ROLE: active-staff read; admin/owning doctor write | D,A,M,K | High files; live policy expressions unknown |
| `expenses` | 18/16 | C | K: PostgREST + Room | +2 (deleted_at/by; `is_deleted` already in A) | PK `id`; no declared FK | ROLE: active-staff select/insert; admin/doctor update/delete | D,A,M,K | High files; live policy expressions unknown |
| `finance_transactions` | 23/20 | B | K: PostgREST + Room | +3 SD | PK `id`; `patient_id`, `visit_id` columns; no declared FK in evidence | AS-CRUD | D,A,M,K | High files; keys/amount invariants live `[UNKNOWN]` |
| `inventory_transactions` | 18/18 | B | K: PostgREST + Room | none | PK `id`; `vaccine_id`, `batch_id`, `patient_id`, `visit_id` columns; no declared FK in evidence | AS-CRUD | D,A,M,K | High files; live stock trigger mode `[UNKNOWN]` |
| `patient_notes` | 13/10 | B | K: PostgREST (sync registry) + Room | +3 SD | PK `id`; `patient_id` FK in Room (K) | AS-CRUD | D,A,M,K | High files; live FK unknown |
| `patient_visits` | 33/30 | B | K: PostgREST + Room | +3 SD | PK `id`; `patient_id` (K); server receipt trigger (M) | AS-CRUD | D,A,M,K | High files; receipt/trigger live `[UNKNOWN]` |
| `patients` | 18/15 | B | K: PostgREST + Room | +3 SD | PK `id`; unique `patient_clinic_id` index conditional (M) | AS-CRUD | D,A,M,K | High files; live unique index/keys unknown |
| `personal_vaccine_reminders` | 22/19 | C | K: PostgREST + Room | +3 SD | PK `id`; FKs to `patients`, `vaccines` (M/K) | AS-CRUD | D,A,M,K | High files; live FKs unknown |
| `profiles` | 16/16 | B | K: PostgREST + Room | none | PK `id`; logical `auth.users.id`; no declared FK | P-select; no client insert/update/delete | D,A,M,K | High files; live auth relation unknown |
| `receipt_sequences` | 6/6 | C | none (server trigger) | none | PK `financial_year` (M) | REVOKE; no client policy (M) | D,A,M | High SQL; live sequence/trigger unknown |
| `reminders` | 24/21 | B | K: PostgREST + Room | +3 SD | PK `id`; `patient_id` (K); conditional natural unique index (M) | AS-CRUD | D,A,M,K | High files; live unique index unknown |
| `user_devices` | 12/12 | B | K: PostgREST + Room | none | PK `id`; `user_id` logical auth user; no declared FK | OWN: owner + active staff; insert/update legacy policies dropped (M) | D,A,M,K | High files; live policy state unknown |
| `vaccination_items` | 17/14 | B | K: PostgREST + Room | +3 SD | PK `id`; `vaccination_id → patient_visits`, `vaccine_id`, `batch_id` (K) | AS-CRUD | D,A,M,K | High files; live FKs unknown |
| `vaccination_todos` | 19/16 | C | K: PostgREST + Room | +3 SD | PK `id`; `patient_id → patients` (M) | AS-CRUD | D,A,M,K | High files; live FK unknown |
| `vaccine_batches` | 23/20 | B | K: PostgREST + Room | +3 SD | PK `id` (entity `batchId` maps to remote `id`); `vaccine_id` (K); stock trigger target (M) | AS-CRUD | D,A,M,K | High files; live stock trigger/quantities `[UNKNOWN]` |
| `vaccines` | 18/15 | B | K: PostgREST + Room | +3 SD | PK `id`; no declared FK | AS-CRUD | D,A,M,K | High files; live keys unknown |
| `waste_records` | 17/14 | B | K: PostgREST + Room | +3 SD + 8 camelCase→snake_case renames | PK `id`; both FKs preserved by rename (M); `vaccine_id`, `batch_id` (K) | AS-CRUD | D,A,M,K | High files; live rename state `[UNKNOWN]` |
| `todo_notification_events` | 0/0 | U | none (trigger writer) | absent both | PK unknown; receives `patient_id`/`doctor_id` per migration comment (M) | COND: enable/force + revoke, no client read policy (M) | M | Low; existence, schema, trigger, and live RLS unknown |

**All 23 shared tables:** no common-column type, nullability, or default difference was found. This is a file comparison, not a live type certification.

## 5. Why the snapshots disagree — supported causes

1. **Snapshot timing `[INFERRED, high]`.** The exact 55-row delta maps to migrations dated `20260919`, `20260925`, and `20260929`. The Android snapshot has the pre-rename/pre-soft-delete signatures; the desktop snapshot has the post-change signatures.
2. **Missing baseline migration `[VERIFIED]`.** Nine of the 24 desktop tables are created by repository migrations. Fifteen are assumed to pre-exist; repository SQL alters or policies them but never creates them. The 15 are present in both snapshots, so their absence from *creation DDL* is not evidence they are absent from production.
3. **At least one missing migration and manual application `[VERIFIED]`.** `20261016_rls_index_and_stock_trigger_hardening.sql` explicitly says `todo_notification_events` was "created by a migration that is not in this repository" and that the migration is safe to apply to a database that already has some of it applied by hand. `20261013` says `update_batch_stock()` "was applied to production by hand (it lives only in a scratch file, never in a migration)." Manual/untracked changes are therefore proven for at least these objects.
4. **Snapshot scope/filtering `[INFERRED, medium]`.** Both CSVs contain only `public` column metadata, no keys, indexes, grants, or policies. The Android file's name claims keys/indexes but its header has only table/column fields. This is scope/filtering in the export, not a table-loss finding.
5. **No evidence of a different production schema `[UNKNOWN]`.** All desktop rows are `public`; the Android CSV has no schema column; Android/migrations use `public`. A different-schema explanation is not supported by the evidence, but cannot be excluded without a live catalog.

### What must not be concluded

- Do not conclude that 15 tables are missing from production because only 9 are created by migrations.
- Do not conclude that the desktop CSV is complete or current; it lacks keys, indexes, policies, grants, and provenance.
- Do not conclude that the Android CSV is a different project or schema; it is an older, narrower export.
- Do not conclude that the migration chronology above was actually applied live; it is an inference from file signatures.
- Do not treat `todo_notification_events` as absent or present live; it is absent from both CSVs and only conditionally handled by migration SQL.

## 6. Keys, relationships, and RLS coverage

### 6.1 Keys

- Both CSVs contain **no key metadata**. The Android filename is misleading.
- Repository-created tables supply primary/foreign keys in SQL: `receipt_sequences` (`financial_year`), `api_write_rate_limits` (composite), `borrow_returns`, `consultation_todos`, `vaccination_todos`, `personal_vaccine_reminders`, `expenses`, `doctor_weekly_slots`, `doctor_slot_exceptions`.
- Android Room entities supply local foreign keys for client tables, but Room is not remote-DB evidence. Several remote relationships have no declared FK in the available evidence: `audit_logs`, `finance_transactions`, `inventory_transactions`, `profiles`, `user_devices`.
- Conditional unique indexes exist in migration SQL for `patients.patient_clinic_id`, `profiles(lower(email))`, and the reminder natural key; their live existence depends on whether duplicates caused the migration to skip them. `20261016` raises a notice and skips on duplicates.

### 6.2 RLS

- Migration SQL has 18 literal `ENABLE ROW LEVEL SECURITY` statements and policy loops; the union is 25 named public tables (24 CSV tables plus conditional `todo_notification_events`).
- Twenty tables are in the active-staff baseline loop: the 16 `AS-CRUD` tables above plus `audit_logs`, `expenses`, `doctor_weekly_slots`, `doctor_slot_exceptions`.
- `profiles` and `user_devices` have separate policies; `receipt_sequences` and `api_write_rate_limits` are enabled and revoked; `todo_notification_events` is conditionally enabled/forced and revoked.
- The deployed policy set, `pg_policies` expressions, policy permissiveness, grants, and trigger/function state are **not** verified. Static `CREATE POLICY` text is not a live count.

## 7. Live evidence still required

The exact read-only queries are in [[Database/Live-Verification-Queries|Live Verification Queries]]. They cover:

- current `public` tables/columns/constraints/indexes;
- RLS enabled/forced and actual policies, including `storage`;
- table/schema/sequence/function ACLs and role memberships;
- function definitions, `SECURITY DEFINER`, `search_path`, and triggers (especially `update_batch_stock` and the receipt trigger);
- aggregate auth/profile role counts without user identifiers or PHI;
- private Storage bucket metadata and Realtime publication membership.

Until those results are reviewed, this reconciliation is a **file-level reconciliation only**. The deployed database contract is `[UNKNOWN]`.

## 8. Related

[[Database/Database-Architecture|Database Architecture]] · [[Database/Data-Dictionary|Data Dictionary]] · [[Database/Access-Patterns|Access Patterns]] · [[Database/Live-Verification-Queries|Live Verification Queries]] · [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]]
