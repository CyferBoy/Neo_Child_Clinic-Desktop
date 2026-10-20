---
title: ADR-0008 Shared Supabase Backend and Single Schema
doc_status: accepted
evidence: explicit user direction + Android source and migration audit
updated: 2026-10-20
---

# ADR-0008 — Shared Supabase Backend and Single Schema

**Status:** Accepted. This decision is fixed by explicit user direction, not inferred from the Android implementation.
**Date:** 2026-10-20.

## Context

The Android application is already backed by a hosted Supabase project. The desktop project has no source, no connection code, and no database of its own. The user requires the Go + Wails desktop application to use the **same existing Supabase project and PostgreSQL database** as the Android application.

The supplied CSV files are schema snapshots, not connection configuration. The older Android-repository snapshot is already stale against current migrations, and neither CSV contains a project URL, project reference, authentication setting, RLS policy, or credential.

## Decision

1. **One backend.** Android and desktop use the same existing Supabase project, the same PostgreSQL database, the same Auth users, the same Storage buckets, and the same Edge Functions.
2. **No parallel backend.** Do not create a new Supabase project, a separate desktop database, duplicate tables, a parallel schema, or a second authentication system.
3. **Normal user access only.** The desktop uses the Supabase publishable/anon key plus the signed-in user's JWT over HTTPS. It must not contain a service-role key, database password, or other privileged credential.
4. **Server authority.** PostgreSQL and RLS remain authoritative for authorization and data integrity. Local SQLite is a working copy and cache, not a second source of truth.
5. **Same contract.** Desktop table names, columns, primary keys, timestamps, soft-delete fields, Storage paths, and receipt-number behavior must match the existing shared schema. Local-only tables are not created remotely.
6. **Configuration is external.** The actual project URL and publishable key are supplied through approved build/runtime configuration. They are not committed and are not reproduced in documentation.
7. **No schema changes in this investigation.** No migration, RLS policy, grant, trigger, production record, or database setting is changed by this documentation pass.
8. **No new backend service by default.** If a privileged operation genuinely requires server-side code, it belongs in an existing or separately approved server-side component, never in the desktop binary. A new service requires a concrete requirement and a new approved ADR.

## Alternatives considered

| Alternative | Assessment |
|---|---|
| Create a new Supabase project for desktop | Rejected: splits patients, identity, and financial data; violates the explicit requirement |
| Create a separate desktop PostgreSQL database | Rejected: duplicates the schema and creates a second source of truth |
| Connect directly to PostgreSQL with a database password | Rejected: exposes privileged credentials, bypasses PostgREST/RLS, and adds network exposure |
| Ship a service-role key in the desktop app | Rejected: grants unrestricted RLS bypass to every installation |
| Build a new backend service | Not justified by current evidence; would duplicate existing Auth/PostgREST/Storage/Functions |
| Keep the CSV as the schema authority | Rejected: both CSVs are incomplete and one is demonstrably stale |

## Consequences

Positive:
- One patient, clinical, inventory, and financial record set.
- One staff identity and role model.
- Existing RLS, triggers, receipt numbering, Storage policy, and Edge Functions remain applicable.
- No migration or data-copy project.

Negative / risks:
- Desktop cannot be developed safely until the actual project identity and configuration are confirmed without exposing secrets.
- The live schema, grants, policies, and triggers still need read-only verification; the CSV is not sufficient.
- Schema drift between Android, desktop, and the hosted database must be detected early.
- The current repository cannot rebuild the whole schema from zero; nine of the 24 tables in the newer snapshot are created by migrations.
- Testing against the existing project must be non-destructive and may be constrained; a separate test harness, if ever proposed, needs explicit approval and must never become the desktop backend.

## Validation

- A redacted configuration fingerprint proves Android and desktop resolve the same project host/project identity.
- A desktop sign-in obtains a normal user session and every request carries that user's JWT.
- RLS tests cover active/inactive staff, multiple roles, and an unauthenticated client.
- An Android-created row is read and updated by desktop, and a desktop-created row is read by Android, without duplicate rows.
- No service-role key, database password, refresh token, or project secret appears in desktop source, logs, crash reports, or documentation.
- No desktop code creates tables or runs production migrations.

## Open questions

- Who supplies and owns the approved desktop configuration values?
- What is the approved, non-destructive verification path against the existing project?
- Is a separate test project or local harness permitted for destructive tests, or must all verification use test accounts and reversible synthetic data in the existing project?
- Which desktop-local encryption and key-recovery design will protect the local working copy?

## Related

[[Decisions/README|Decision Log]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Architecture/System-Architecture|System Architecture]] · [[Database/Database-Architecture|Database Architecture]] · [[Security/Security-Model|Security Model]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]]
