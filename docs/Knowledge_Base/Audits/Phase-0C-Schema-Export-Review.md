---
title: Phase 0C — Live Schema Export Review and Reconciliation
doc_status: review
evidence: 16 Supabase metadata CSVs (2026-10-20/21) + 23 repository migrations + Android source/Kotlin/Room + prior Phase 0B reconciliation; no SQL executed, no live connection
updated: 2026-10-21
---

# Phase 0C — Live Schema Export Review and Reconciliation

> **Read-only review.** No SQL was executed against Supabase. No database, migration, RLS policy, grant, trigger, function, Storage setting, Android file, or application dependency was changed. The exports are user-supplied metadata snapshots, not a connection or a credential. Their project identity and capture environment are not stated.

> **Evidence status.** This review materially narrows the Phase 0B unknowns: the exports now cover columns, keys, constraints, indexes, RLS state, policy definitions, table ACLs, default ACLs, function metadata, triggers, role memberships, and Realtime publication membership. They do **not** prove runtime behaviour, project identity, migration history, Storage bucket settings, Auth signup settings, or that the exports are complete. All "live" statements below mean **reported by the export**, not "verified by a query we ran."

## 1. Source inventory

All files are under `docs/Schemas/` in the desktop repository. Sizes are bytes; times are the file timestamps observed on 2026-10-21.

| # | File | Rows | Actual content | Capture | Reliability / caveat |
|---:|---|---:|---|---|---|
| 1 | `Supabase Snippet List Public Table Columns.csv` | 416 | 24 `public` tables; name/type/null/default/ordinal | 2026-10-20 12:25 | Column-only; no keys/policies. Matches #2 exactly. |
| 2 | `Supabase Snippet Public Table Column Inventory.csv` | 416 | Same 416 columns plus `udt_name`, identity/generated flags | 2026-10-21 16:41 | Independent corroboration of #1; all 416 values match. |
| 3 | `Supabase Snippet List constraints in public schema.csv` | 77 | 24 PK, 38 FK, 3 UNIQUE, 12 CHECK | 2026-10-21 16:42 | Constraint names and definitions; `convalidated` all true. |
| 4 | `Supabase Snippet List Indexes in Public Schema.csv` | 93 | 93 index definitions (33 unique, including PK/unique constraints) | 2026-10-21 16:42 | Real index export. |
| 5 | `Supabase Snippet List Indexes in Public Schema (1).csv` | 179 | **RLS policies, not indexes** | 2026-10-21 16:44 | Misnamed. 178 `public` + 1 `storage.objects`; 22 public tables have policies. |
| 6 | `Supabase Snippet List Public Schema Triggers.csv` | 61 | Trigger names, enabled flag, definitions | 2026-10-21 16:48 | All `tgenabled = O`. |
| 7 | `Supabase Snippet Public Schema Object Privileges.csv` | 744 | Table ACL rows (`schema_name`, object, grantee, privilege) | 2026-10-21 16:44 | Tables only; no schema/sequence/column ACLs. |
| 8 | `Supabase Snippet List Relations in Public and Storage Schemas.csv` | 32 | 24 `public` + 8 `storage` relations; RLS enabled/forced; owner | 2026-10-21 16:39 | All relation kind `r` (tables); no views. |
| 9 | `Supabase Snippet List Relations in Target Schemas.csv` | 32 | Identical to #8 | 2026-10-21 16:41 | Duplicate export; no new evidence. |
| 10 | `Supabase Snippet List Public Functions with Definitions.csv` | 21 | Function metadata (definer/invoker, volatility, config, owner) | 2026-10-21 16:47 | **No definitions**, despite the filename. |
| 11 | `Supabase Snippet List Selected Functions in public Schema.csv` | 13 | Function definitions for 13 of 21 functions | 2026-10-21 16:47 | Missing 8 definitions, including `check_is_active`, `check_is_admin`, `recalculate_all_stocks`, `rls_auto_enable`. |
| 12 | `Supabase Snippet Schema, Function, and Default Privilege Audit.csv` | 24 | `pg_default_acl` rows by schema/object type/owner | 2026-10-21 16:45 | Shows future-object defaults for `public`, `storage`, `graphql`, `graphql_public`, etc. |
| 13 | `Supabase Snippet Role Privilege Matrix for Public Objects.csv` | 63 | 21 functions × `anon`/`authenticated`/`service_role` EXECUTE | 2026-10-21 16:46 | All 63 cells `true`. |
| 14 | `Supabase Snippet Role Membership and Admin Options.csv` | 25 | Role membership edges | 2026-10-21 16:45 | Confirms `authenticator` membership in `anon`/`authenticated`/`service_role`. |
| 15 | `Supabase Snippet Role Coverage Summary for Auth and Profiles.csv` | 2 | Active, non-deleted profiles by role | 2026-10-21 16:48 | Only `admin = 1`, `doctor = 1`; no receptionist/nurse/inventory rows. |
| 16 | `Supabase Snippet List Storage Buckets and Publication_Policy Settings.csv` | 30 | **Realtime publication membership only** | 2026-10-21 16:49 | **No bucket metadata.** Misnamed for the bucket half. |

### 1.1 What the exports cover

| Area | Covered? | Notes |
|---|---|---|
| Tables and columns | Yes | 24 public tables, 416 columns; no views, enums, domains, or sequences. |
| Primary/foreign/unique/check constraints | Yes | 77 constraints; names and definitions. |
| Indexes | Yes | 93, including unique/partial indexes. |
| RLS enabled/forced | Yes | All 24 enabled; none forced. |
| Policies | Yes | 179 policy rows; roles, command, `USING`, `WITH CHECK`. |
| Table ACLs | Yes | 744 rows; 4 roles × 24 tables, with two exceptions. |
| Schema/sequence/column ACLs | **No** | Not captured. No serial sequences observed. |
| Function metadata/definitions | Partial | 21 metadata; 13 definitions. |
| Triggers | Yes | 61. |
| Storage buckets/objects policies | Partial | One `storage.objects` policy; **no bucket rows**. |
| Realtime publication | Yes | 23 public tables + `realtime.messages_*` partitions. |
| Migration history | **No** | `supabase_migrations.schema_migrations` not exported. |
| Project/auth settings | **No** | No project URL, signup setting, JWT config, or Data API setting. |

## 2. Verified counts

| Metric | Count | Cross-check |
|---|---:|---|
| Public tables | 24 | 24 PKs; 24 rows in relations export; 24 table ACL objects |
| Public columns | 416 | Two independent exports match exactly |
| Constraints | 77 | 24 PK + 38 FK + 3 UNIQUE + 12 CHECK |
| Indexes | 93 | 33 unique (24 PK + 3 unique constraints + 6 other unique) |
| Policy rows | 179 | 178 public + 1 storage; 22 public tables have policies |
| Triggers | 61 | Includes duplicate stock triggers on `inventory_transactions` |
| Functions | 21 | 15 `SECURITY DEFINER`, 6 invoker; 13 with pinned `search_path` |
| Table ACL rows | 744 | 22 tables × 4 roles × 8 + receipt 24 + api 16 |
| Relations | 32 | 24 public + 8 storage |
| Realtime member tables | 23 | All public tables except `api_write_rate_limits` |
| Active staff profiles | 2 | 1 admin, 1 doctor; no other roles |

The two column exports are not merely similar: their 416 `(table, column)` keys and all type/null/default values are identical. The one-day gap therefore shows a stable column shape, not two different schemas.

## 3. Structural reconciliation

**Source codes:** `L` = 2026-10-21 metadata export; `D` = 2026-10-20 column export; `M` = repository migration; `K` = Android Kotlin/Room/PostgREST; `A` = older Android CSV (23/361). `Baseline` means no `CREATE TABLE` exists in the repository; the table pre-exists and is altered/policy-managed.

| Table (`public`) | Cols | Origin | Live keys / constraints | Indexes | Android | Drift / discrepancy | Evidence |
|---|---:|---|---|---:|---|---|---|
| `api_write_rate_limits` | 3 | `M` | PK `(user_id, window_started_at)` | 1 | none (server-only) | None vs `20260929001000` | L,M |
| `audit_logs` | 17 | Baseline | PK `id`; FK `patient_id → patients(id)` | 3 | `AuditLogEntity`, sync | FK is live-only evidence; no `CREATE TABLE` in repo | L,M,K |
| `borrow_records` | 18 | Baseline | PK `id`; FKs `vaccine_id → vaccines`, `batch_id → vaccine_batches` | 3 | `BorrowEntity`, sync | No column drift vs D/A; baseline DDL absent | L,D,A,M,K |
| `borrow_returns` | 14 | `M` | PK `id`; FKs `borrow_record_id`, `batch_id` both `ON DELETE CASCADE`; CHECK `quantity > 0` | 4 | `BorrowReturnEntity`, sync | **Live-only `updated_at`** not in `20260902`; soft-delete cols from `20260925` | L,M,K |
| `consultation_todos` | 18 | `M` | PK `id`; FKs `patient_id`/`doctor_id`/`availability_slot_id`, all `SET NULL` | 6 | `ConsultationTodoEntity`, sync | Matches `20260825` + `20260911` + `20260925` | L,M,K |
| `consultations` | 21 | Baseline | PK `id`; FKs `patient_id`/`visit_id` CASCADE, `availability_slot_id` SET NULL | 4 | `ConsultationEntity`, sync | No column drift; baseline DDL absent | L,D,A,M,K |
| `doctor_slot_exceptions` | 14 | `M` | PK `id`; FKs `doctor_id`/`weekly_slot_id` CASCADE; CHECK type/slot consistency | 5 | `DoctorSlotExceptionEntity`, sync | **Live-only `is_synced` (nullable)**; **Android sends `start_minute`/`end_minute`, which the DB does not have** | L,M,K |
| `doctor_weekly_slots` | 14 | `M` | PK `id`; FK `doctor_id → profiles` CASCADE; 3 CHECKs | 5 | `DoctorWeeklySlotEntity`, sync | **Live-only `is_synced`** not in `20260911` | L,M,K |
| `expenses` | 18 | `M` | PK `id` (text); 3 CHECKs (category/payment/amount) | 6 | `ExpenseEntity`, sync | Matches `20260909` + `20260925` | L,M,K |
| `finance_transactions` | 23 | Baseline | PK `id`; FKs `patient_id`, `visit_id` | 4 | `FinanceEntity`, sync | No column drift; baseline DDL absent | L,D,A,M,K |
| `inventory_transactions` | 18 | Baseline | PK `id`; 4 FKs (`vaccine`, `batch`, `patient`, `visit`) | 7 | `InventoryTransactionEntity`, sync | **Two stock triggers live**; function is the old version | L,M,K |
| `patient_notes` | 13 | Baseline | PK `id`; FK `patient_id → patients` CASCADE | 2 | `PatientNotesEntity`, sync | No column drift; baseline DDL absent | L,D,A,M,K |
| `patient_visits` | 33 | Baseline | PK `id`; FKs `patient_id` CASCADE, `availability_slot_id` SET NULL; unique receipt index | 5 | `VisitEntity`, sync | Receipt trigger live; baseline DDL absent | L,D,A,M,K |
| `patients` | 18 | Baseline | PK `id`; unique `patient_clinic_id` | 5 | `PatientEntity`, sync | Ordinal gaps 10–11 (dropped columns); duplicate unique indexes | L,D,A,M,K |
| `personal_vaccine_reminders` | 22 | `M` | PK `id`; FKs `patient_id` CASCADE, `vaccine_id` SET NULL; 2 CHECKs | 6 | `PersonalReminderEntity`, sync | Matches `20260901` + `20260902` + `20260925` | L,M,K |
| `profiles` | 16 | Baseline | PK `id`; FK `id → auth.users` CASCADE; UNIQUE `email`; CHECK role list | 3 | `ProfileEntity`, sync (update) | Legacy policies still live; role-source split | L,M,K |
| `receipt_sequences` | 6 | `M` | PK `financial_year` | 1 | none (trigger only) | **Live-only `created_at`, `created_by`, `updated_by`**; **live anon/auth CRUD grants despite migration revoke** | L,M |
| `reminders` | 24 | Baseline | PK `id`; FKs `patient_id`/`original_visit_id` CASCADE; UNIQUE natural key | 4 | `ReminderEntity` (+ `RemoteReminder`), sync | Duplicate identical unique indexes; permissive ALL-true policy | L,M,K |
| `user_devices` | 12 | Baseline | PK `id`; FK `user_id → profiles` CASCADE | 4 | `DeviceRepositoryImpl` + `UserDevice` | Duplicate unique FCM indexes; legacy owner policies | L,M,K |
| `vaccination_items` | 17 | Baseline | PK `id`; FKs `vaccination_id → patient_visits` CASCADE, `vaccine_id`, `batch_id` | 3 | `VaccinationItemEntity`, sync | No column drift; baseline DDL absent | L,D,A,M,K |
| `vaccination_todos` | 19 | `M` | PK `id`; FKs `patient_id`/`doctor_id`/`availability_slot_id`, all SET NULL | 6 | `VaccinationTodoEntity`, sync | Matches `20260825` + `20260911` + `20260925` | L,M,K |
| `vaccine_batches` | 23 | Baseline | PK `id`; FK `vaccine_id → vaccines` CASCADE | 2 | `VaccineBatchEntity`, sync | Stock trigger target; no `vaccine_id` index | L,D,A,M,K |
| `vaccines` | 18 | Baseline | PK `id`; no FK | 2 | `VaccineEntity`, sync | No column drift; baseline DDL absent | L,D,A,M,K |
| `waste_records` | 17 | Baseline | PK `id`; FKs `vaccine_id`, `batch_id` | 2 | `WasteEntity`, sync | **No `set_updated_at` trigger**; snake_case confirmed | L,D,A,M,K |

### 3.1 Structural conclusions

1. **The 416-column shape is corroborated.** The 2026-10-20 and 2026-10-21 column exports agree on every key and value.
2. **The older 23/361 Android CSV is stale.** The 55-row delta is still exactly explained by soft-delete additions, the waste rename, and `api_write_rate_limits`; the new exports add keys/policies but do not change that arithmetic.
3. **Six live columns are not reproducible from the repository migrations:** `borrow_returns.updated_at`, `doctor_weekly_slots.is_synced`, `doctor_slot_exceptions.is_synced`, and `receipt_sequences.created_at`/`created_by`/`updated_by`. `create table if not exists` allowed a pre-existing table shape to survive. This is schema drift, not a count error.
4. **All 24 tables are owned by `postgres`; all have RLS enabled and none forced.** Forced RLS is not the control here; grants and policies are.
5. **There are no views, enums, sequences, or generated/identity columns in the export.** All IDs are UUID/text with defaults; no serial sequence ACL is applicable.
6. **`todo_notification_events` is absent from the 24-table relation export**, despite `20261016` describing it as an existing table. Either it does not exist in this project or the export was taken from a database where that migration was not applied. Its live status remains `[UNKNOWN]`.
7. **The export is not a baseline migration.** Fifteen tables still have no `CREATE TABLE`; a clean rebuild remains impossible from the repository alone.

## 4. Security reconciliation

### 4.1 Table ACLs (GRANT) are not RLS

The export separates two controls that must not be conflated:

- **GRANT** decides whether `anon`/`authenticated` can reach a table at all.
- **RLS** decides which rows the role can read or write.

Live table ACLs:

| Group | Tables | `anon` | `authenticated` | `service_role` / `postgres` |
|---|---|---|---:|---|
| Full eight privileges (`SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, MAINTAIN`) | 22 tables | Yes | Yes | Yes |
| `receipt_sequences` | 1 | 4 (`SELECT, INSERT, UPDATE, DELETE`) | 4 | 8 |
| `api_write_rate_limits` | 1 | None | None | 8 |

The 22 full-grant tables are every public table except `receipt_sequences` and `api_write_rate_limits`. `anon` having `TRUNCATE`/`REFERENCES`/`TRIGGER` is broader than PostgREST needs, but the immediately exploitable privileges are `SELECT`/`INSERT`/`UPDATE`/`DELETE`.

**Cause `[INFERRED, high]`:** the uniform 8-privilege pattern is consistent with the project's default ACLs at table creation; `receipt_sequences` has only the four PostgREST DML privileges, which is consistent with a later blanket `GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES` that re-granted the table after `20260824` revoked it. The exact manual grant is not in the repository. The effect is confirmed by the export; the cause is inferred.

### 4.2 Default privileges for future objects

The `pg_default_acl` export shows, for both `postgres`-owned and `supabase_admin`-owned defaults:

| Schema | Object type | `anon` / `authenticated` / `service_role` |
|---|---|---|
| `public` | tables | `arwdDxtm` (all eight) |
| `public` | functions | `X` (EXECUTE) |
| `public` | sequences | `rwU` |
| `storage` | tables/functions/sequences | same pattern |
| `graphql`, `graphql_public` | tables/functions/sequences | same pattern |
| `extensions` | all | restricted to `postgres`/`supabase_admin` |

This is the legacy auto-exposure model that Supabase is removing on **2026-10-30**. It is also why `REVOKE ... FROM public` inside the migrations did not remove `anon`/`authenticated` access: the default ACL grants those roles explicitly, and `PUBLIC` is a different grantee.

### 4.3 Policy reachability

**Critical:** thirteen tables still carry `{public}` policies, and ten of them pass for `anon` because `get_my_role()` is fail-open:

```sql
-- live definition (export)
SELECT role INTO user_role FROM public.profiles WHERE id = auth.uid();
RETURN COALESCE(user_role, 'nurse');
```

For `anon`, `auth.uid()` is null, no profile row is found, and the function returns `'nurse'`. The legacy `{public}` policies then compare that value against role lists that include `nurse`. Because `anon` also has full table grants, the two gates are open together.

| Table | Policies (public/authenticated) | `anon` policy path | `authenticated` policy path | Severity |
|---|---|---|---:|---|
| `patients` | 11 (3/8) | **Yes** — `get_my_role() = nurse` on two `ALL` policies + one `SELECT` | Active staff + legacy nurse path | **Critical** |
| `patient_visits` | 9 (1/8) | **Yes** — legacy `ALL` | Active staff + legacy nurse path | **Critical** |
| `patient_notes` | 9 (1/8) | **Yes** — legacy `ALL` | Active staff + legacy nurse path | **Critical** |
| `consultations` | 9 (1/8) | **Yes** — legacy `ALL` | Active staff + legacy nurse path | **Critical** |
| `vaccination_items` | 9 (1/8) | **Yes** — legacy `ALL` | Active staff + legacy nurse path | **Critical** |
| `vaccines` | 9 (1/8) | **Yes** — legacy `ALL` | Active staff + legacy nurse path | **Critical** |
| `vaccine_batches` | 9 (1/8) | **Yes** — legacy `ALL` | Active staff + legacy nurse path | **Critical** |
| `inventory_transactions` | 9 (1/8) | **Yes** — legacy `ALL` | Active staff + legacy nurse path | **Critical** |
| `waste_records` | 9 (1/8) | **Yes** — legacy `ALL` | Active staff + legacy nurse path | **Critical** |
| `borrow_records` | 9 (1/8) | **Yes** — legacy `ALL` | Active staff + legacy nurse path | **Critical** |
| `finance_transactions` | 9 (1/8) | No — nurse is not in `admin/receptionist/doctor` | Active staff + legacy role path | High |
| `profiles` | 8 (5/3) | No — admin/active/own predicates fail | Own update + active-staff read + legacy admin `ALL` | High |
| `audit_logs` | 6 (2/4) | No — admin or `auth.uid()` predicate fails | Active staff read/insert; **any authenticated insert** | High |
| `reminders` | 9 (0/9) | No | **Any authenticated user: `ALL` with `USING (true)` / `WITH CHECK (true)`** | **Critical** |
| `borrow_returns` | 8 (0/8) | No | Active staff only | Medium |
| `consultation_todos` | 8 (0/8) | No | Active staff only | Medium |
| `vaccination_todos` | 8 (0/8) | No | Active staff only | Medium |
| `personal_vaccine_reminders` | 8 (0/8) | No | Active staff only | Medium |
| `expenses` | 5 (0/5) | No | Active staff select/insert; admin/doctor update/delete | Medium |
| `doctor_weekly_slots` | 3 (0/3) | No | Active staff read; admin/own write | Medium |
| `doctor_slot_exceptions` | 3 (0/3) | No | Active staff read; admin/own write | Medium |
| `user_devices` | 11 (0/11) | No | Any authenticated owner (legacy) + active-staff owner (new) | Medium |
| `receipt_sequences` | 0 | No policy; table ACL alone cannot read | No policy | High (function path) |
| `api_write_rate_limits` | 0 | No ACL, no policy | No ACL, no policy | Low |

**Live-export conclusion (not an executed exploit test):** if the export is accurate and current, the public `anon` key embedded in every Android APK can read and write **ten core clinical/inventory tables without a login**, including patient demographics, visits, notes, consultations, vaccination items, vaccines, batches, stock movements, wastage, and borrow records. This is the most serious finding in this review. It requires immediate confirmation against the live API and remediation before any desktop client is connected.

### 4.4 Confirmed policy defects

| ID | Finding | Evidence | Consequence |
|---|---|---|---|
| SEC-0C-01 | Legacy `{public}` `ALL` policies on ten tables plus `get_my_role()` fallback `'nurse'` | Policies export; function definition | Unauthenticated PHI/inventory CRUD with the anon key |
| SEC-0C-02 | `reminders` has `{authenticated}` `ALL` with `USING (true)` and `WITH CHECK (true)` | Policy export | Any Supabase auth user, including non-staff, can read/write all reminders |
| SEC-0C-03 | `profiles` still has `{public}` admin `ALL` policies using `get_my_role()` / `check_is_admin()` | Policy export | Role source split: `profiles.role` can still authorize after `app_metadata.role` was made authoritative |
| SEC-0C-04 | `audit_logs` has a `{public}` INSERT policy with `auth.uid() IS NOT NULL` | Policy export | Any authenticated user can forge audit entries; no update/delete policy, so append-only is otherwise intact |
| SEC-0C-05 | `user_devices` legacy owner policies do not require active staff | Policy export | A deactivated user with a valid JWT can still manage their device row until token expiry |
| SEC-0C-06 | All 21 functions are executable by `anon` | Role privilege matrix | Includes `neo_next_receipt_number` (sequence burn), `cleanup_write_rate_limits` (delete), `recalculate_all_stocks` (stock recalculation), `get_my_role`, `handle_new_user` |
| SEC-0C-07 | `get_my_role()` and `handle_new_user()` are `SECURITY DEFINER` with no `search_path` | Function metadata | Hardening gap; both use schema-qualified `public.profiles`, which reduces immediate hijack risk |
| SEC-0C-08 | `handle_new_user()` copies `raw_user_meta_data->>'role'` into `profiles.role`, defaulting to `nurse` | Function definition (not in repo) | If public signup is enabled and this trigger is attached, a signup can choose `profiles.role`; combined with SEC-0C-03 this is a potential privilege path |
| SEC-0C-09 | `receipt_sequences` has `anon`/`authenticated` CRUD grants despite the `20260824` revoke; no policy | Table ACL + policy export | Direct table access is RLS-denied, but `neo_next_receipt_number()` is anon-executable and can burn receipt numbers |
| SEC-0C-10 | Realtime publishes 23 tables, including `profiles`, `user_devices`, `receipt_sequences`, and all clinical tables | Publication export | Change events are broadcast; Realtime RLS must be verified separately, and unnecessary membership widens metadata exposure |
| SEC-0C-11 | `storage.objects` has one `patient-docs` policy, but the export contains no bucket rows | Policy + publication export | Bucket existence, `public=false`, size/MIME limits, and object ownership are unverified |
| SEC-0C-12 | All tables have `rls_forced = false` | Relations export | Table owner and `service_role` bypass RLS by design; the control depends on correct grants and policies, not forced RLS |

### 4.5 Function exposure details

| Function | Security | `search_path` | Client-relevant risk |
|---|---|---|---|
| `get_my_role()` | DEFINER | **none** | Fail-open `'nurse'`; drives legacy policies; anon-executable |
| `handle_new_user()` | DEFINER | **none** | Copies user-metadata `role`; trigger attachment unverified |
| `neo_next_receipt_number(date)` | DEFINER | `public` | Anon-executable; increments/burns the receipt sequence |
| `neo_assign_receipt_number()` | DEFINER | `public` | Trigger-only; anon-executable but not directly useful |
| `neo_current_staff_label()` | DEFINER | `public` | Revoked in migration; live anon can execute; returns null for anon |
| `cleanup_write_rate_limits()` | DEFINER | `public` | Anon-executable delete of old rate-limit rows |
| `enforce_write_rate_limit()` | DEFINER | `public, auth` | Anon-executable trigger function; direct call raises without a trigger context |
| `recalculate_all_stocks()` | INVOKER | none | Anon-executable; if it updates batches, legacy anon policies permit the write |
| `is_admin()` | DEFINER | `public` | Anon-executable; returns false for anon; explicit grant only to `authenticated` is contradicted by default ACL |
| `is_active_staff()` | DEFINER | `public, auth` | Anon-executable; returns false for anon |
| `check_is_admin()`, `check_is_active()` | DEFINER | `public` | Legacy helpers; definitions not exported |
| `protect_profile_privileged_fields()` | DEFINER | `public` | Blocks self-service role/email/activation changes |
| `notify_todays_patient()` | DEFINER | `public, extensions, net` | Anon-executable; notification abuse surface unverified |
| `rls_auto_enable()` | DEFINER | `pg_catalog` | Event-trigger helper; anon-executable but not directly useful |
| `update_batch_stock()` | INVOKER | none | **Live old version**; duplicate trigger; see §5.2 |
| `set_updated_at()`, `set_expenses_updated_at()` | INVOKER | none | Trigger helpers; anon-executable but require trigger context |
| `neo_financial_year_label(date)`, `neo_parse_visit_date(text)` | INVOKER | none | Pure helpers; low risk |

## 5. Migration reconciliation

### 5.1 Table-creating migrations and explicit grants

No migration contains a table-level `GRANT`. The only table grants in repository SQL are revokes.

| Migration | Creates | Explicit `GRANT` | Explicit `REVOKE` | Oct 30 assessment |
|---|---|---|---|---|
| `20260824_receipt_numbering.sql` | `receipt_sequences` | None | `anon`, `authenticated` | Intended server-only; live grants contradict it |
| `20260825_patient_todos.sql` | `consultation_todos`, `vaccination_todos` | None | None | **No durable API privileges for new tables** |
| `20260901_personal_vaccine_reminders.sql` | `personal_vaccine_reminders` | None | None | **No durable API privileges** |
| `20260902_borrow_returns.sql` | `borrow_returns` | None | None | **No durable API privileges** |
| `20260909_expenses.sql` | `expenses` | None | None | **No durable API privileges** |
| `20260911_doctor_availability_slots.sql` | `doctor_weekly_slots`, `doctor_slot_exceptions` | None | None | **No durable API privileges** |
| `20260929001000_write_rate_limit.sql` | `api_write_rate_limits` | None | `anon`, `authenticated` | Intended server-only; no `service_role` grant, but definer functions use owner rights |
| `20261016_rls_index_and_stock_trigger_hardening.sql` | No table (conditional `todo_notification_events`, bucket/policy) | None | `todo_notification_events` anon/auth | Not a table-creation grant fix |

**October 30 conclusion:** if the announced platform change removes the exported default ACLs, all seven business tables created by these migrations will be unreachable through PostgREST (`42501 permission denied`) until explicit grants are added. The same applies to `service_role` for server-side Edge Functions that touch a newly created table. The migrations are **not** Oct 30-ready. A durable convention is required:

```sql
grant select, insert, update, delete on table public.<table> to authenticated;
grant all on table public.<table> to service_role;
-- only if anon genuinely needs access:
-- grant select on table public.<table> to anon;
```

Exact privilege sets must be least-privilege; the above is a shape, not an approved policy. `anon` should not receive business-table access by default.

### 5.2 Stock trigger: the live database is in the pre-fix state

The live export shows:

- **Two** `AFTER` triggers on `inventory_transactions` calling `update_batch_stock()`: `inventory_transactions_update_batch_stock` **and** `tr_update_batch_stock`.
- The live `update_batch_stock()` definition is the **old** version: on `UPDATE` it applies only `- OLD.quantity`; it does not add `NEW.quantity` or move batches.

`20261017_stock_trigger_duplicate_and_update_arithmetic.sql` is supposed to drop `tr_update_batch_stock`, install the corrected function, and guard against a second trigger. It has **not** taken effect in the exported database. The migration is also not safely deployable as written: after dropping the legacy trigger, its guard counts **all** other non-internal triggers on `inventory_transactions` except `inventory_transactions_update_batch_stock`; the live table also has `neo_stamp_accountability`, `set_updated_at`, and `trg_inventory_transactions_write_rate_limit`, so the guard would raise and the migration would fail. This explains the live duplicate without assuming manual rollback.

**Consequence:** every insert/update/delete that reaches both triggers applies the stock movement twice. `20261018` only ensures its own trigger exists; it does not detect or remove the legacy duplicate. Do not enable desktop inventory writes until this is fixed and verified.

### 5.3 Other migration/drift findings

| ID | Finding | Evidence | Impact |
|---|---|---|---|
| MIG-0C-01 | No table-level `GRANT` baseline | All migrations | Oct 30 breakage; clean rebuild lacks API privileges |
| MIG-0C-02 | `REVOKE ... FROM public` does not remove explicit `anon`/`authenticated` default grants | Live ACLs + function matrix | Anon can still execute all 21 functions; `receipt_sequences` grants survived |
| MIG-0C-03 | `CREATE TABLE IF NOT EXISTS` masks pre-existing shapes | 6 live-only columns on 4 “created” tables | Migrations are not a reproducible schema |
| MIG-0C-04 | `20261017` cannot pass its own guard on the live trigger set | Live triggers + migration text | Stock fix not deployed; duplicate remains |
| MIG-0C-05 | Duplicate indexes/constraints | `patients` (2 unique + 1 non-unique on clinic id), `reminders` (2 identical natural keys), `profiles` (email + lower(email)), `user_devices` (2 identical FCM uniques) | Write overhead, ambiguous upsert conflict targets, drift signal |
| MIG-0C-06 | Duplicate/redundant policies | 179 policies; most tables have two copies of each CRUD policy; `patients` 11, `user_devices` 11 | Harder review; legacy policies never dropped |
| MIG-0C-07 | `waste_records` lacks `set_updated_at` | Trigger export | `updated_at` text is client-maintained; inconsistent accountability |
| MIG-0C-08 | `todo_notification_events` absent from the 24-table export | Relations/columns exports | Conditional migration target unverified |
| MIG-0C-09 | `receipt_sequences` extra columns and grants | Live vs `20260824` | Shape and ACL drift on a security-sensitive table |
| MIG-0C-10 | `borrow_returns.updated_at` and doctor-slot `is_synced` are live-only | Live vs migrations | Models generated from migrations would omit live columns |
| MIG-0C-11 | Android expects `doctor_slot_exceptions.start_minute`/`end_minute`; live DB has neither | Android Room migration + entity vs live columns | Custom SLOT exceptions can fail PostgREST with `PGRST204` unknown column |
| MIG-0C-12 | All 15 baseline tables still lack `CREATE TABLE` | Repository inventory | Clean rebuild impossible; disaster recovery risk |

## 6. Table-by-table security and grant matrix

Legend: **ACL** = table GRANT reachability; **RLS** = row policy. “Anon path” is the policy path that would apply to the `anon` role, not proof of an executed request. All tables are `public`, owner `postgres`, RLS enabled, not forced, and in the Realtime publication unless noted.

| Table | ACL anon / auth | Policies | Anon path | Auth path | Verdict |
|---|---|---|---|---|---|
| `api_write_rate_limits` | none / none | 0 | none | none (server definer only) | Locked down; not published |
| `audit_logs` | full / full | 6 | no (admin/uid predicates fail) | active staff read/insert + any-auth insert | Append-only; insert too broad |
| `borrow_records` | full / full | 9 | **yes (legacy ALL)** | active staff + legacy | Critical |
| `borrow_returns` | full / full | 8 | no | active staff | Medium |
| `consultation_todos` | full / full | 8 | no | active staff | Medium |
| `consultations` | full / full | 9 | **yes (legacy ALL)** | active staff + legacy | Critical |
| `doctor_slot_exceptions` | full / full | 3 | no | active staff read; admin/own write | Medium |
| `doctor_weekly_slots` | full / full | 3 | no | active staff read; admin/own write | Medium |
| `expenses` | full / full | 5 | no | active staff; admin/doctor write | Medium |
| `finance_transactions` | full / full | 9 | no (nurse not in list) | active staff + legacy roles | High |
| `inventory_transactions` | full / full | 9 | **yes (legacy ALL)** | active staff + legacy | Critical |
| `patient_notes` | full / full | 9 | **yes (legacy ALL)** | active staff + legacy | Critical |
| `patient_visits` | full / full | 9 | **yes (legacy ALL)** | active staff + legacy | Critical |
| `patients` | full / full | 11 | **yes (legacy ALL ×2 + SELECT)** | active staff + legacy | Critical |
| `personal_vaccine_reminders` | full / full | 8 | no | active staff | Medium |
| `profiles` | full / full | 8 | no | own update + active staff + legacy admin ALL | High |
| `receipt_sequences` | 4 / 4 | 0 | no policy; direct denied | no policy; direct denied | High via function |
| `reminders` | full / full | 9 | no | **any authenticated ALL true** | Critical |
| `user_devices` | full / full | 11 | no | any auth owner + active staff owner | Medium |
| `vaccination_items` | full / full | 9 | **yes (legacy ALL)** | active staff + legacy | Critical |
| `vaccination_todos` | full / full | 8 | no | active staff | Medium |
| `vaccine_batches` | full / full | 9 | **yes (legacy ALL)** | active staff + legacy | Critical |
| `vaccines` | full / full | 9 | **yes (legacy ALL)** | active staff + legacy | Critical |
| `waste_records` | full / full | 9 | **yes (legacy ALL)** | active staff + legacy | Critical |

## 7. October 30, 2026 readiness

**Platform statement (verified from Supabase’s published changelog/docs):** new tables in `public` will no longer be exposed to the Data API automatically; the change is enforced on all projects on **2026-10-30**. Existing projects currently grant `anon`, `authenticated`, and `service_role` broad default privileges on new tables/functions/sequences. Projects must opt in to auto-exposure or grant explicitly.

**This project’s live state:** the default ACLs still grant the old broad privileges, and the existing 22 business tables already have full `anon`/`authenticated` grants. The October change is therefore a **future-table** risk, not the cause of the current exposure.

**Readiness verdict: NOT READY.**

1. Seven business tables are created by migrations with no explicit table grant. If the platform default changes, PostgREST will return `42501` for those tables.
2. `service_role` also has no explicit grant in those migrations. Server-side code that touches a new table can fail even when RLS is irrelevant.
3. Function grants are still governed by `PUBLIC` EXECUTE plus the explicit default ACL. New functions remain callable by `anon` unless the creator revokes from `PUBLIC`, `anon`, and `authenticated`, then grants only the intended roles.
4. The existing `receipt_sequences` table demonstrates the failure mode: the migration revoked `anon`/`authenticated`, but live ACLs show four DML privileges. A later blanket grant (inferred) re-opened it. Only explicit, reviewed grants are durable.
5. Any remediation must be a new migration (not applied in this review) that grants least privilege to the seven tables and verifies with `has_table_privilege` for each role. Do not grant broad `anon` access to clinical tables.

## 8. Required roles and privileges vs RLS

| Control | What it answers | Live evidence | What it does not prove |
|---|---|---|---|
| Table `GRANT` | Can this role reach the table through PostgREST? | 744 ACL rows; 22 tables full for anon/auth | Row visibility; runtime role switching; column-level grants |
| RLS `ENABLE`/`FORCE` | Is row filtering active for non-owners? | All 24 enabled; none forced | Policy correctness; owner/service bypass |
| Policies | Which rows/commands pass? | 179 rows; 13 tables have public policies | Actual JWT claims, Auth signup state, function behaviour at runtime |
| Function `EXECUTE` | Can this role call the function? | All 21 executable by anon/auth/service | Whether the function is safe or intended for clients |
| Default ACL | What will new objects grant? | Broad grants in `public`/`storage`/`graphql` | Whether the platform will revoke them on Oct 30 |
| Schema `USAGE` | Can the role resolve objects? | **Not exported** | Needed for a complete ACL proof |

The critical distinction: `anon` currently has **both** the table grants and a policy path on ten tables. Removing either gate closes that path; removing only the grant leaves SQL-function paths (e.g. `recalculate_all_stocks`, `neo_next_receipt_number`) able to run as definer/invoker. Removing only the policies leaves the grants in place for any future policy mistake.

## 9. Verification limits and required follow-up

This review did **not** run SQL. The following remain unverified and must be checked before any desktop connection:

1. **Project identity:** no URL, project ref, or JWT issuer in the exports. Confirm same project as Android with a redacted fingerprint.
2. **Runtime anon test:** issue a read/write request with only the anon key against one non-production patient row, then roll it back/delete; confirm the policy logic in §4.3. Do not use real PHI.
3. **Auth signup state:** confirm whether public signup is enabled and whether `handle_new_user` is attached to `auth.users`; test a synthetic account cannot choose `profiles.role`.
4. **Migration history:** inspect `supabase_migrations.schema_migrations` to see whether `20261017`/`20261018` were attempted, and whether `todo_notification_events` ever existed.
5. **Stock trigger:** run the two verification queries in `20261017`; expect exactly one stock trigger and the corrected function body.
6. **Default ACL after Oct 30:** re-run the `pg_default_acl` query; confirm whether project-level grants survive the platform change.
7. **Storage:** list `storage.buckets` (id, name, public, limits) and `storage.objects` policies; confirm `patient-docs` is private.
8. **Realtime:** confirm Realtime RLS/authorization for the 23 published tables; remove `receipt_sequences`/`profiles`/`user_devices` if not needed.
9. **Function definitions:** export the missing 8 definitions, especially `check_is_active`, `check_is_admin`, `recalculate_all_stocks`, `rls_auto_enable`.
10. **Column contract:** confirm whether `doctor_slot_exceptions.start_minute`/`end_minute` are planned server columns; until then, the desktop must not send them.

## 10. Desktop implementation blockers

No desktop implementation was started. These are the evidence-backed blockers that must close first:

| ID | Blocker | Why it blocks desktop | Evidence |
|---|---|---|---|
| B-0C-01 | Project identity/config unverified | Wrong project or parallel backend | No URL/ref in exports; ADR-0008 |
| B-0C-02 | Critical anon/legacy-policy and role-source exposure | Desktop cannot safely share the backend until PHI and authorization are gated | §4.3–4.4; SEC-0C-01..04, SEC-0C-08 |
| B-0C-03 | Explicit grants / Oct 30 gap | New tables will be unreachable or over-exposed | §5.1, §7 |
| B-0C-04 | Stock trigger duplicate + old function | Inventory writes double-apply or fail | §5.2 |
| B-0C-05 | No reproducible baseline / shape drift | Cannot build a trustworthy test DB | §3.1, §5.3 |
| B-0C-06 | Doctor-slot exception contract mismatch | Custom SLOT sync fails with unknown columns | §5.3 MIG-0C-11 |
| B-0C-07 | Storage bucket metadata unverified | Patient-document access cannot be certified | §4.4 SEC-0C-11 |
| B-0C-08 | Realtime publication over-broad | Desktop subscription design must not assume filtering | §4.4 SEC-0C-10 |
| B-0C-09 | Anon function EXECUTE / receipt sequence | Data-integrity and abuse surface | §4.5; SEC-0C-06, SEC-0C-09 |
| B-0C-10 | RLS not forced; owner/service bypass | Desktop must never use service role; role tests required | §4.4 SEC-0C-12 |

## 11. Recommendations (not executed)

Priority order:

1. **Contain the anon path:** drop the legacy `{public}` policies on the ten tables, or at minimum replace `get_my_role()` with a fail-closed helper that returns null for unauthenticated users; verify with an anon-key request. Do not run this review’s SQL automatically.
2. **Fix `reminders`:** replace the `{authenticated}` `ALL`/`true` policy with active-staff predicates.
3. **Remove legacy `profiles` admin policies** and reconcile `profiles.role` vs `app_metadata.role`; confirm signup and `handle_new_user`.
4. **Revoke `EXECUTE` from `anon`/`authenticated` on all functions except the explicit RLS helpers and intended RPCs**; use `REVOKE ... FROM PUBLIC, anon, authenticated`, then grant the minimum.
5. **Add explicit, least-privilege table grants** to the seven table-creating migrations (or a new forward migration), including `service_role`; verify with `has_table_privilege`.
6. **Fix the stock trigger migration**: narrow the guard to stock triggers only, drop `tr_update_batch_stock`, install the corrected function, and verify exactly one trigger.
7. **Add the missing server columns or stop sending them** for `doctor_slot_exceptions.start_minute`/`end_minute`.
8. **Create a reviewed baseline migration** covering the 15 pre-existing tables, with exact columns/constraints/indexes and no `IF NOT EXISTS` masking.
9. **Deduplicate indexes/policies** and record the intended canonical set.
10. **Verify Storage and Realtime** before desktop subscriptions/uploads.

## 12. Related

[[Database/Schema-Reconciliation|Schema Reconciliation]] · [[Database/Data-Dictionary|Data Dictionary]] · [[Database/Database-Architecture|Database Architecture]] · [[Database/Live-Verification-Queries|Live Verification Queries]] · [[Security/Security-Model|Security Model]] · [[Audits/Risk-Register|Risk Register]] · [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]] · [[Roadmap/Phase-1-Implementation-Plan|Phase 1 Implementation Plan]]
