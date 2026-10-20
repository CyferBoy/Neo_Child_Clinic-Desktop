---
title: Live Verification Queries — Read Only
doc_status: proposed
evidence: repository security SQL + PostgreSQL catalog inspection design; no live access
updated: 2026-10-20
---

# Live Verification Queries — Read Only

> **Status: not run.** No `psql`, Supabase CLI, database driver, MCP database resource, project URL, or publishable key was available in the inspection environment. These are the exact queries to run through an authorized administrative session. They are catalog/metadata reads only; they do not read patient rows, test production data, or change settings.

## 1. Safety rules

1. Run in a **read-only transaction**: `begin read only; ... rollback;`.
2. Use an authorized Supabase administrator or a dedicated read-only database role. Do not paste credentials, JWTs, project URLs, or connection strings into chat or documentation.
3. Do **not** run `supabase/tests/rls_role_test.sql` as part of this export. It contains `INSERT`/`UPDATE`/`DELETE` test operations and placeholder UUIDs. It requires separate approval and synthetic test data.
4. Do **not** query `storage.objects`, patient tables, auth emails, or auth user IDs. The role path uses aggregate counts only.
5. Export each result as CSV/JSON with the column headers. Store it in the approved secure evidence location, not in Git.
6. Treat query text/output as sensitive operational metadata. Do not include project secrets or PHI in the evidence file.

## 2. Session and schema scope

```sql
begin read only;

select current_database() as database_name,
       current_user as session_role,
       current_schema() as default_schema,
       now() as captured_at;

rollback;
```

This confirms scope only. Do not use it to infer project identity; use a redacted project fingerprint from an approved configuration check.

## 3. Tables, columns, keys, and indexes

### 3.1 Relations and RLS flags

```sql
select n.nspname as schema_name,
       c.relname as relation_name,
       c.relkind as relation_kind,
       c.relrowsecurity as rls_enabled,
       c.relforcerowsecurity as rls_forced,
       pg_get_userbyid(c.relowner) as owner
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname in ('public', 'storage')
  and c.relkind in ('r', 'p', 'v', 'm', 'S')
order by n.nspname, c.relname;
```

### 3.2 Columns and defaults

```sql
select table_schema,
       table_name,
       ordinal_position,
       column_name,
       data_type,
       udt_name,
       is_nullable,
       column_default,
       is_identity,
       identity_generation,
       is_generated,
       generation_expression
from information_schema.columns
where table_schema = 'public'
order by table_name, ordinal_position;
```

`ordinal_position` gaps can reflect dropped columns. A gap is not proof that the CSV omitted a row; compare the current list, not the numbers alone.

### 3.3 Primary, unique, foreign-key, check, and exclusion constraints

```sql
select n.nspname as schema_name,
       rel.relname as table_name,
       con.conname as constraint_name,
       con.contype as constraint_type,
       con.condeferrable,
       con.condeferred,
       con.convalidated,
       pg_get_constraintdef(con.oid, true) as definition
from pg_constraint con
join pg_class rel on rel.oid = con.conrelid
join pg_namespace n on n.oid = rel.relnamespace
where n.nspname = 'public'
  and con.contype in ('p', 'u', 'f', 'c', 'x')
order by rel.relname, con.contype, con.conname;
```

### 3.4 Indexes

```sql
select schemaname,
       tablename,
       indexname,
       indexdef
from pg_indexes
where schemaname = 'public'
order by tablename, indexname;
```

## 4. RLS policies and grants

### 4.1 Policies, including Storage

```sql
select schemaname,
       tablename,
       policyname,
       permissive,
       roles,
       cmd,
       qual,
       with_check
from pg_policies
where schemaname in ('public', 'storage')
order by schemaname, tablename, policyname;
```

Compare these expressions with migration SQL. `CREATE POLICY` text in the repository is intent, not the deployed policy set.

### 4.2 Explicit table and sequence ACLs

```sql
select n.nspname as schema_name,
       c.relname as object_name,
       case c.relkind
         when 'r' then 'table'
         when 'p' then 'partitioned_table'
         when 'S' then 'sequence'
         when 'v' then 'view'
         when 'm' then 'materialized_view'
         else c.relkind::text
       end as object_type,
       case when a.grantee = 0 then 'PUBLIC'
            else pg_get_userbyid(a.grantee)
       end as grantee,
       a.privilege_type,
       a.is_grantable
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
cross join lateral aclexplode(
  coalesce(
    c.relacl,
    acldefault(
      (case when c.relkind = 'S' then 'S' else 'r' end)::"char",
      c.relowner
    )
  )
) a
where n.nspname = 'public'
  and c.relkind in ('r', 'p', 'S', 'v', 'm')
order by n.nspname, c.relname, grantee, a.privilege_type;
```

`relacl` null means default owner privileges; `acldefault` makes that visible. This is not a substitute for role-membership analysis.

### 4.3 Schema, function, and default ACLs

```sql
select n.nspname as schema_name,
       case when a.grantee = 0 then 'PUBLIC'
            else pg_get_userbyid(a.grantee)
       end as grantee,
       a.privilege_type,
       a.is_grantable
from pg_namespace n
cross join lateral aclexplode(
  coalesce(n.nspacl, acldefault('n', n.nspowner))
) a
where n.nspname in ('public', 'storage', 'auth', 'realtime')
order by n.nspname, grantee, a.privilege_type;

select n.nspname as schema_name,
       p.proname as function_name,
       pg_get_function_identity_arguments(p.oid) as arguments,
       case when a.grantee = 0 then 'PUBLIC'
            else pg_get_userbyid(a.grantee)
       end as grantee,
       a.privilege_type,
       a.is_grantable
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
cross join lateral aclexplode(
  coalesce(p.proacl, acldefault('f', p.proowner))
) a
where n.nspname = 'public'
order by p.proname, arguments, grantee, a.privilege_type;

select pg_get_userbyid(defaclrole) as owner,
       case when defaclnamespace = 0 then '<global>'
            else defaclnamespace::regnamespace::text
       end as schema_name,
       defaclobjtype,
       defaclacl
from pg_default_acl
order by owner, schema_name, defaclobjtype;
```

### 4.4 Role memberships

```sql
select member.rolname as member_role,
       granted.rolname as member_of,
       am.admin_option
from pg_auth_members am
join pg_roles member on member.oid = am.member
join pg_roles granted on granted.oid = am.roleid
order by member.rolname, granted.rolname;
```

### 4.5 Effective table/schema/function privileges for client roles

```sql
select r.rolname,
       n.nspname as schema_name,
       c.relname as table_name,
       has_table_privilege(r.oid, c.oid, 'SELECT') as can_select,
       has_table_privilege(r.oid, c.oid, 'INSERT') as can_insert,
       has_table_privilege(r.oid, c.oid, 'UPDATE') as can_update,
       has_table_privilege(r.oid, c.oid, 'DELETE') as can_delete,
       has_table_privilege(r.oid, c.oid, 'TRUNCATE') as can_truncate
from pg_roles r
cross join pg_class c
join pg_namespace n on n.oid = c.relnamespace
where r.rolname in ('anon', 'authenticated', 'service_role')
  and n.nspname = 'public'
  and c.relkind in ('r', 'p')
order by r.rolname, c.relname;

select r.rolname,
       n.nspname as schema_name,
       has_schema_privilege(r.oid, n.oid, 'USAGE') as can_use,
       has_schema_privilege(r.oid, n.oid, 'CREATE') as can_create
from pg_roles r
cross join pg_namespace n
where r.rolname in ('anon', 'authenticated', 'service_role')
  and n.nspname in ('public', 'storage')
order by r.rolname, n.nspname;

select r.rolname,
       n.nspname as schema_name,
       p.proname as function_name,
       pg_get_function_identity_arguments(p.oid) as arguments,
       has_function_privilege(r.oid, p.oid, 'EXECUTE') as can_execute
from pg_roles r
cross join pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where r.rolname in ('anon', 'authenticated', 'service_role')
  and n.nspname = 'public'
order by r.rolname, p.proname, arguments;
```

`has_*_privilege` reflects privileges available to the role, including inherited grants. It does not simulate a JWT or prove row visibility.

## 5. Functions, security settings, and triggers

### 5.1 Function metadata

```sql
select n.nspname as schema_name,
       p.proname as function_name,
       pg_get_function_identity_arguments(p.oid) as arguments,
       p.prosecdef as security_definer,
       p.provolatile,
       p.proconfig,
       pg_get_userbyid(p.proowner) as owner
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public'
order by p.proname, arguments;
```

### 5.2 Definitions of authorization, stock, receipt, rate-limit, and audit functions

```sql
select n.nspname as schema_name,
       p.proname as function_name,
       pg_get_function_identity_arguments(p.oid) as arguments,
       p.prosecdef as security_definer,
       p.proconfig,
       pg_get_functiondef(p.oid) as definition
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public'
  and p.proname in (
    'is_admin',
    'is_active_staff',
    'get_my_role',
    'neo_next_receipt_number',
    'neo_assign_receipt_number',
    'neo_parse_visit_date',
    'neo_financial_year_label',
    'update_batch_stock',
    'enforce_write_rate_limit',
    'cleanup_write_rate_limits',
    'neo_stamp_accountability',
    'protect_profile_privileged_fields',
    'handle_new_user'
  )
order by p.proname, arguments;
```

The live-only legacy `get_my_role()` must be read explicitly. If it is `SECURITY DEFINER` without a pinned `search_path`, record it as a live security finding; do not copy it into desktop code.

### 5.3 Triggers and enabled state

```sql
select n.nspname as schema_name,
       c.relname as table_name,
       t.tgname as trigger_name,
       t.tgenabled,
       pg_get_triggerdef(t.oid, true) as definition
from pg_trigger t
join pg_class c on c.oid = t.tgrelid
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and not t.tgisinternal
order by c.relname, t.tgname;
```

Required checks:

- `inventory_transactions_update_batch_stock` exists exactly once and is enabled.
- No second trigger on `inventory_transactions` calls `update_batch_stock()`.
- `neo_assign_receipt_number` exists on `patient_visits` and is enabled.
- No duplicate stock/receipt trigger is enabled.
- `tgenabled = 'O'` (origin) or the intended session/replication mode is documented.

## 6. Authentication and role-resolution path (aggregate only)

```sql
select count(*) as auth_users_total,
       count(*) filter (where raw_app_meta_data ? 'role') as with_app_role,
       count(*) filter (where raw_user_meta_data ? 'role') as with_user_role,
       count(*) filter (
         where coalesce(raw_app_meta_data ->> 'role', '') not in
           ('admin', 'doctor', 'receptionist', 'nurse', 'inventory_manager')
       ) as missing_or_unknown_app_role
from auth.users;

select role,
       is_active,
       is_deleted,
       count(*) as profile_count
from public.profiles
group by role, is_active, is_deleted
order by role, is_active, is_deleted;
```

No user IDs, emails, names, tokens, or metadata values are selected. If policy prohibits reading `auth.users` even in aggregate, record that limitation; do not broaden the query.

## 7. Storage and Realtime

```sql
select id,
       name,
       public,
       file_size_limit,
       allowed_mime_types,
       created_at,
       updated_at
from storage.buckets
order by id;

select schemaname,
       tablename,
       policyname,
       permissive,
       roles,
       cmd,
       qual,
       with_check
from pg_policies
where schemaname = 'storage'
order by tablename, policyname;

select pubname,
       puballtables,
       pubinsert,
       pubupdate,
       pubdelete,
       pubtruncate
from pg_publication
order by pubname;

select pubname,
       schemaname,
       tablename
from pg_publication_tables
order by pubname, schemaname, tablename;
```

Expected review points: `patient-docs` is private; Storage object policies are active-staff gated; Realtime publishes only the tables the client subscribes to and is not treated as a write path.

## 8. Reconciliation procedure after the export

1. **Compare tables and columns.** Diff the live `information_schema.columns` result against the desktop CSV and Android CSV. Record additions/drops and the source of each difference. Do not infer missing production tables from the CSV/migration count.
2. **Confirm baseline coverage.** Identify which of the 15 baseline tables are present live. A live table with no repository `CREATE TABLE` confirms a missing baseline, not a reason to invent a new schema.
3. **Check `todo_notification_events`.** If present, capture its columns, keys, policies, and trigger writer. If absent, record that the conditional migration did not apply.
4. **Resolve keys.** Replace Room-inferred relationships with live `pg_constraint` facts. Do not generate desktop models from the old CSV or from Room FKs alone.
5. **Review RLS and ACLs.** Compare `pg_policies` and effective privileges with the migration union. Record policy drift and any `anon`/`authenticated` table privileges.
6. **Resolve stock mode.** From the trigger/function results, determine whether the live database uses the `update_batch_stock()` trigger or the client absolute-batch writer. Do not implement both. Record the mode as an architecture input.
7. **Resolve receipts.** Confirm the server receipt trigger and immutability. The desktop must never compute a receipt number.
8. **Review Storage/Realtime.** Confirm bucket privacy, object policy scope, publication membership, and no second write path.
9. **Update evidence.** Add dated `[VERIFIED-LIVE]` notes to the Knowledge Base. Do not add credentials, project URLs, JWTs, or patient data.
10. **Close or narrow gates.** Update the Phase 0B readiness matrix only for items the export actually proves.

## 9. What this export cannot prove

- That the desktop connects to the same project. That requires an approved configuration and a redacted project-identity fingerprint.
- That a policy denies/a permits a specific JWT in practice. That requires an approved synthetic-account role test, which is not a read-only catalog query.
- That data is correct or free of duplicate/negative stock. That requires synthetic/reversible tests and reconciliation, not a schema export.
- That the migration history is complete. It can reveal current shape and drift, not the intent behind missing files.

## 10. Related

[[Database/Schema-Reconciliation|Schema Reconciliation]] · [[Database/Database-Architecture|Database Architecture]] · [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]] · [[Security/Security-Model|Security Model]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]]
