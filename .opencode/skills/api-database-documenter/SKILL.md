---
name: api-database-documenter
description: "Document Neo Child Clinic Desktop database tables, columns, relationships, constraints, indexes, RLS policies, RPCs, storage buckets, and API contracts using migrations and schema definitions as primary evidence. Use to maintain schema, relationship, RLS, and contract notes without inferring objects from prose."
metadata:
  version: "1.0"
  mode: "docs-write-after-approval"
  scope: "neo-child-clinic-desktop"
---

# API and Database Documenter

Produce an accurate catalogue of the shared Supabase/Postgres backend, the local database, and the contracts between React, Wails, Go, and Supabase. Migrations and schema definitions are the primary evidence. A table is not real because a document names it.

## Invoke when

- You need database schema, relationships, constraints, indexes, RLS, RPC, storage, or API-contract documentation.
- A migration, policy, RPC, or Wails binding changed.
- You need to verify schema drift between migrations, local code, and documentation.
- A feature specification or security review needs a schema reference.

Do not use this skill to write migrations, apply policies, or change API contracts. Hand off changes to `implementation-planner` after approval.

## Inputs

- Desktop root and Supabase project artifacts (`supabase/config.toml`, `migrations/`, `functions/`, `tests/`).
- Local database schema, Go models, generated types, Wails bindings, and API handlers.
- Optional access to a safe local or staging database for verification.
- Whether notes may be written and the approved Knowledge Base path.

## Before you start

1. Read the root and nested `AGENTS.md` when present, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read existing schema/API notes and the documentation maintenance guide.
2. Record the commit and branch. State the migration range covered.
3. Identify whether the backend is shared with Android. Shared objects require compatibility notes.
4. Confirm whether a live database is available. Do not imply hosted state from repository migrations.

## Evidence standard

- `[VERIFIED]` — read directly from a migration, schema file, generated type, code symbol, or safe query. Cite file and line or object name.
- `[INFERENCE]` — a relationship or contract derived from names, foreign keys, or call sites; state the reasoning.
- `[PROPOSED]` — a target schema or contract; never describe it as applied.
- `[UNKNOWN]` — requires a live database, missing migration, or external owner.

Migrations prove repository intent and schema history. They do not prove the hosted project has applied them. Never state that a table, column, policy, index, RPC, bucket, or trigger exists in production without a safe verification query or owner-supplied evidence.

## Procedure

1. **Build the migration timeline.** List migrations in lexical/version order with purpose and affected objects. Note gaps, duplicate versions, or migrations that cannot be applied cleanly. Do not run them.
2. **Catalogue tables and columns.** For each table: schema, purpose, columns, types, nullability, defaults, primary key, foreign keys, unique/check constraints, generated columns, and comments. Record the defining migration and line.
3. **Catalogue relationships.** Build the entity graph: one-to-one, one-to-many, many-to-many, optionality, cascade behavior, and soft-delete semantics. Use an `erDiagram` only when the graph is readable.
4. **Catalogue indexes and performance structures.** List indexes, uniqueness, partial predicates, and the query patterns they support. Note missing indexes only as `[INFERENCE]` tied to a named query; do not claim a performance problem.
5. **Document RLS and grants.** For every exposed table/view: RLS enabled or not, policy names, operation, roles, `USING` and `WITH CHECK` predicates, helper functions, and table/column grants. For `SECURITY DEFINER` functions, record the owner, `search_path`, and caller checks. Note service-role-only paths.
6. **Document RPCs and triggers.** Record signatures, return types, volatility, security mode, authorization logic, side effects, and the tables they touch. Include trigger ordering and idempotency where relevant.
7. **Document storage.** Buckets, public/private status, allowed MIME types and size limits, path conventions, and storage policies. Do not infer a policy from client code.
8. **Document API contracts.** For each Wails binding or HTTP endpoint: name, direction, request/response shape, error shape, authentication/authorization, validation, idempotency, and versioning. Link contracts to the Go types and frontend call sites.
9. **Check drift.** Compare migrations, generated types, Go models, frontend types, documentation, and the Android client's expectations. Report each mismatch with evidence. Do not silently reconcile.
10. **Record live-verification needs.** For anything that depends on the hosted database, write the exact read-only query or owner check required, without running it against production.
11. **Write targeted notes.** Use the approved schema note and relationship note. Link to feature and flow notes instead of duplicating them.

## Output contract

```markdown
# Database and API Contracts — <commit> — <YYYY-MM-DD>

## Scope and evidence
- Migration range:
- Live database inspected: yes / no / local / staging
- Shared with Android: yes / no / unknown

## Migration timeline
| Version / file | Purpose | Objects | Notes |
|---|---|---|---|

## Tables
| Schema.table | Purpose | Primary key | Foreign keys | Soft delete | Evidence |
|---|---|---|---|---|---|

### <table>
| Column | Type | Null | Default | Constraints | Evidence |
|---|---|---|---|---|---|

## Relationships
```mermaid
erDiagram
    ...
```

## Indexes and constraints
| Table | Object | Definition | Purpose | Evidence |
|---|---|---|---|---|

## RLS and grants
| Object | Operation | Policy / grant | Roles | Predicate summary | Evidence |
|---|---|---|---|---|---|

## RPCs and triggers
| Object | Signature | Security | Authorization | Side effects | Evidence |
|---|---|---|---|---|---|

## Storage
| Bucket | Visibility | Limits | Policy summary | Evidence |
|---|---|---|---|---|

## API contracts
| Contract | Caller | Request | Response | Errors | Auth | Evidence |
|---|---|---|---|---|---|---|

## Drift and unknowns
| ID | Mismatch / unknown | Evidence | Impact | Resolution |
|---|---|---|---|---|
```

Use `DATA-<AREA>-NNN` for schema findings, `RISK-DATA-NNN` for risks, and `QUES-DATA-NNN` for unknowns. Do not reuse Android `NCC-*` or `NSC-*` IDs.

## Stop conditions

Stop and report when:

- Migrations are absent and no schema source is available.
- A production-only claim requires a live query but no safe, authorized environment exists.
- Two migrations conflict or the timeline is ambiguous.
- Documenting an object would require exposing credentials or patient data.
- An API contract is not implemented or cannot be traced to code.

## Handoff

- `security-review` — RLS, grants, auth, and IPC findings.
- `data-flow-auditor` — runtime use of tables, RPCs, and contracts.
- `architecture-documenter` — place the data layer in the system architecture.
- `feature-specification` — data changes required by a feature.
- `test-strategy-planner` — schema, RLS, and contract tests.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Never run migrations, policy changes, backfills, or destructive SQL.
- Never paste secrets or production data into documentation.
- Never infer a database object from frontend types, docs, or a feature name.
- Preserve existing notes and user changes; make targeted edits only.
