---
title: Neo Child Clinic Desktop — Knowledge Base
doc_status: baseline
evidence: full discovery pass against Android repository and desktop project + shared-backend connection investigation
updated: 2026-10-20
---

# Neo Child Clinic Desktop — Knowledge Base

> **Baseline, not a completion claim.** The desktop application has **no source code**. This vault documents the verified Android reference, the target desktop design, the 22 Phase 1 specifications, the audit, and the roadmap. Every statement is tagged by evidence type.

**Audit date:** 2026-10-20
**Android reference:** `/data/data/com.termux/files/home/Neo_Child_Clinic` — `main` @ `ca4bed406bfd246ad83878fff9a4e178ebc5670f`
**Desktop project:** `/storage/emulated/0/Neo_Child_Clinic_Desktop`
**Desktop implementation:** none
**Live Supabase access:** not available
**Desktop tests run:** 0
**Android tests run:** 0 in this pass

## Status at a glance

| | |
|---|---|
| Desktop modules specified | **22 of 22** |
| Desktop modules implemented | **0 of 22** |
| Desktop tests | **0** (no suite) |
| Android reference feature modules | 22 |
| Android reference status | 10 partially implemented, 12 unverified in this pass |
| Desktop repository | **Initialized; `main` pushed to GitHub** |
| Desktop instructions | **No `AGENTS.md`** |
| Installed skills | 17 `SKILL.md` files |
| Shared backend | **Existing Supabase project required** (ADR-0008); desktop connection **Missing** |
| Schema snapshots | Desktop CSV: 24 tables / 416 columns; Android repo CSV: 23 / 361 (stale); neither contains connection fields |
| Android connection | Source-verified: HTTPS Supabase APIs + user JWT; live project identity unavailable |
| Supabase migration files | 23 |
| Android tracked files | 583 |
| Android test files | 41 unit + 8 instrumented |
| Existing Android KB | 37 Markdown notes; preserved unchanged |
| Critical open risks | No desktop source, unverified same-project connection, unreproducible schema, unverified RLS/Storage, stale CSV, sync idempotency, local PHI protection |

## Evidence legend

| Tag | Meaning |
|---|---|
| `[VERIFIED]` | Directly checked in the available source, filesystem, migration, or artifact. |
| `[INFERRED]` | A reasoned conclusion from source evidence, not a runtime observation. |
| `[PROPOSED]` | Target design or requirement; not implemented. |
| `[UNKNOWN]` | Evidence unavailable, conflicting, or live state not inspected. |
| `[DECISION]` | Explicit project direction or approved decision. ADR-0008 (shared existing Supabase backend) is accepted; all other ADRs remain proposed. See [[Decisions/README|Decision Log]]. |

## Start here

| If you want to… | Read |
|---|---|
| Use a plain-Markdown entry point | [[README|Knowledge Base Entry]] |
| Understand the product and scope | [[Product/Product-Vision|Product Vision]] · [[Product/Product-Scope|Product Scope]] |
| See the 22-module status | [[Product/Feature-Inventory|Feature Inventory]] · [[Product/Android-Desktop-Parity|Android-Desktop Parity]] |
| Understand roles and permissions | [[Product/Personas-and-Roles|Personas and Roles]] |
| Understand the target system | [[Architecture/System-Architecture|System Architecture]] |
| Understand offline/sync | [[Architecture/Offline-and-Sync-Design|Offline and Sync Design]] |
| Understand the backend/schema | [[Database/Database-Architecture|Database Architecture]] · [[Database/Data-Dictionary|Data Dictionary]] |
| Review the shared-backend connection evidence | [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] |
| Review security/privacy | [[Security/Security-Model|Security Model]] · [[Security/Threat-Model|Threat Model]] |
| Read the audit | [[Audits/Initial-Audit|Initial Audit]] · [[Audits/Risk-Register|Risk Register]] |
| Read the end-to-end report | [[Audits/Final-Report|Final Report]] |
| Plan the build | [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Roadmap/Phase-1-Implementation-Plan|Phase 1 Plan]] |
| Test the build | [[Testing/Test-Strategy|Test Strategy]] · [[Testing/Regression-Matrix|Regression Matrix]] |
| Review decisions | [[Decisions/README|Decision Log]] |
| Prepare a release | [[Releases/Release-Checklist|Release Checklist]] |

## Product

- [[Product/Product-Vision|Product Vision]]
- [[Product/Product-Scope|Product Scope]]
- [[Product/Personas-and-Roles|Personas and Roles]]
- [[Product/Feature-Inventory|Feature Inventory]]
- [[Product/Android-Desktop-Parity|Android-Desktop Parity]]

## Architecture

- [[Architecture/System-Architecture|System Architecture]]
- [[Architecture/Frontend-Architecture|Frontend Architecture]]
- [[Architecture/Go-Backend-Architecture|Go Backend Architecture]]
- [[Architecture/Data-Flows|Data Flows]]
- [[Architecture/Offline-and-Sync-Design|Offline and Sync Design]]
- [[Architecture/Cache-Strategy|Cache Strategy]]
- [[Architecture/Error-Handling|Error Handling]]

## Database

- [[Database/Database-Architecture|Database Architecture]]
- [[Database/Data-Dictionary|Data Dictionary]]
- [[Database/Access-Patterns|Database Access Patterns]]

## Security

- [[Security/Security-Model|Security Model]]
- [[Security/Threat-Model|Threat Model]]
- [[Security/Privacy-and-Backup|Privacy and Backup]]

## Features (Phase 1 specifications)

1. [[Features/01-Desktop-Shell-and-Navigation|Desktop Shell and Navigation]] — `PLAT`
2. [[Features/02-Authentication-and-Session|Authentication and Session]] — `AUTH`
3. [[Features/03-Staff-and-Role-Management|Staff and Role Management]] — `STF`
4. [[Features/04-Patient-Management|Patient Management]] — `PAT`
5. [[Features/05-Vaccination-Management|Vaccination Management]] — `VAC`
6. [[Features/06-Consultation-Management|Consultation Management]] — `CON`
7. [[Features/07-Vaccine-and-Batch-Inventory|Vaccine and Batch Inventory]] — `INV`
8. [[Features/08-Wastage|Wastage]] — `WAS`
9. [[Features/09-Borrowed-and-Lent-Vaccines|Borrowed and Lent Vaccines]] — `BRW`
10. [[Features/10-Vaccination-Reminders|Vaccination Reminders]] — `REM`
11. [[Features/11-Personal-Reminders|Personal Reminders]] — `PER`
12. [[Features/12-Finance-and-Payments|Finance and Payments]] — `FIN`
13. [[Features/13-Receipts-and-Printing|Receipts and Printing]] — `RCP`
14. [[Features/14-Dashboard|Dashboard]] — `DSH`
15. [[Features/15-Statistics-and-Reports|Statistics and Reports]] — `RPT`
16. [[Features/16-Local-Persistence-and-Offline-Operation|Local Persistence and Offline Operation]] — `OFF`
17. [[Features/17-Supabase-Sync|Supabase Synchronization]] — `SYNC`
18. [[Features/18-Backup-and-Recovery|Backup and Recovery]] — `BAK`
19. [[Features/19-Desktop-Notifications|Desktop Notifications]] — `NOT`
20. [[Features/20-Settings|Settings]] — `SET`
21. [[Features/21-Audit-Logging|Audit Logging]] — `AUD`
22. [[Features/22-Application-Updates|Application Updates]] — `UPD`

## Testing

- [[Testing/Test-Strategy|Test Strategy]]
- [[Testing/Regression-Matrix|Regression Matrix]]

## Audit and risk

- [[Audits/Initial-Audit|Initial Audit]]
- [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Connection Investigation]]
- [[Audits/Risk-Register|Risk Register]]
- [[Audits/Technical-Debt|Technical Debt]]

## Roadmap and decisions

- [[Roadmap/Desktop-Roadmap|Desktop Roadmap]]
- [[Roadmap/Phase-1-Implementation-Plan|Phase 1 Implementation Plan]]
- [[Roadmap/Dependencies-and-Milestones|Dependencies and Milestones]]
- [[Roadmap/Requirements-Traceability|Requirements Traceability]]
- [[Decisions/README|Decision Log]]
  - [[Decisions/ADR-0001-Desktop-Stack|ADR-0001 — Desktop Stack]]
  - [[Decisions/ADR-0002-Local-Persistence|ADR-0002 — Local Persistence]]
  - [[Decisions/ADR-0003-Offline-Sync|ADR-0003 — Offline Sync]]
  - [[Decisions/ADR-0004-Authentication-and-Session|ADR-0004 — Authentication and Session]]
  - [[Decisions/ADR-0005-Wails-Boundary|ADR-0005 — Wails Boundary]]
  - [[Decisions/ADR-0006-Testing-and-Release|ADR-0006 — Testing and Release]]
  - [[Decisions/ADR-0007-Money-Dates-and-Identity|ADR-0007 — Money, Dates, and Identity]]
  - [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008 — Shared Supabase Backend]] — **Accepted**
- [[Releases/Release-Checklist|Release Checklist]]

## What is actually verified

`[VERIFIED]`
- The Android repository is clean at `ca4bed4` with 583 tracked files, 352 main Kotlin files, 41 unit test files, 8 instrumented test files, and 23 SQL migrations.
- The desktop project now has a Git repository with `main` pushed to GitHub; it still has no application source, `go.mod`, `wails.json`, `package.json`, test suite, or build configuration.
- The existing Android Knowledge Base has 37 Markdown notes and was not modified.
- The desktop CSV lists 24 public tables and 416 columns. A second, older CSV in the Android repository lists 23 tables and 361 columns; it still uses camelCase `waste_records` names and is superseded by a later migration.
- Neither CSV contains a project URL, project reference, auth setting, policy, or credential. Repository migrations create only 9 of the 24 newer-snapshot tables from zero; there is no baseline migration.
- Android constructs a supabase-kt client from `BuildConfig.SUPABASE_URL` and `BuildConfig.SUPABASE_ANON_KEY`; the values come from `.env.local` or environment at build time. The actual values are absent from the clean worktree.
- Android uses PostgREST over HTTPS with the signed-in user's JWT, plus Supabase Auth, Storage (`patient-docs`), Edge Function `manage-staff`, and Realtime refresh triggers. No direct PostgreSQL driver or `.rpc` call was found.
- Android reads authorization from `app_metadata.role`; sessions are stored in Keystore-backed encrypted preferences. Server-side `manage-staff`/`notify-update` use the service-role key only in Edge Functions.
- The desktop has no connection code, configuration, database, or tests; its connection status is **Missing**, not “working.”

## What is proposed

`[PROPOSED]`
- The Wails/Go/React architecture, SQLite local store, outbox/transaction-group sync, OS keychain session handling, encrypted backup, desktop notifications, printing, and update flow.
- The 22 feature specifications and their acceptance criteria.
- The permission matrix, roadmap, milestones, test plan, and release checklist.

## What is unknown

`[UNKNOWN]`
- The actual existing project URL, project reference, and publishable-key value. They are not in the worktree; same-project identity cannot be proven yet.
- Live Supabase schema, grants, RLS policies, triggers, Storage rules, and data.
- Whether `todo_notification_events` exists live; it is referenced by migration but absent from both CSVs. `sync_queue`, `widget_due_cache`, `inventory_deductions`, and `backup_history` are local-only Room tables.
- Whether the Android test suite or the repository's SQL RLS tests currently pass; neither was run.
- The approved non-destructive verification path for the existing project.
- Desktop OS support, Wails version, local encryption approach, update provider, and printing requirements.
- Clinic retention/privacy policy and pilot ownership.

## Current blockers

1. No desktop application source. The Git repository now exists, but `AGENTS.md`, branch protection, and CI are still missing.
2. The actual existing project identity/configuration is absent; same-project connection is not proven.
3. No reproducible database baseline and no live schema/RLS/Storage verification.
4. No approved local persistence/encryption or sync contract.
5. No desktop test/release pipeline.
6. No approved non-destructive verification path against the existing project.
7. No privacy/retention decision for local PHI.

## Immediate next actions

1. Add `AGENTS.md`, branch protection, and CI to the existing desktop repository.
2. Obtain the approved existing-project configuration through a secure channel and verify a redacted project fingerprint; do not print or commit the values.
3. Capture the existing project's schema, grants, policies, triggers, and Storage rules read-only; reconcile a baseline without creating a new project or duplicate schema.
4. Approve ADR-0002, ADR-0003, ADR-0004, and ADR-0005; ADR-0008 is already accepted.
5. Implement the trust-boundary spike: same-project auth, keychain, local DB, typed binding, redacted logging.
6. Implement the patient and vaccination vertical slices with replay and stock tests against the approved verification path.
7. Re-run documentation validation and link checks before handoff.

## Documentation conventions

- Stable requirement IDs: `PLAT`, `AUTH`, `STF`, `PAT`, `VAC`, `CON`, `INV`, `WAS`, `BRW`, `REM`, `PER`, `FIN`, `RCP`, `DSH`, `RPT`, `OFF`, `SYNC`, `BAK`, `NOT`, `SET`, `AUD`, `UPD` plus cross-cutting `ERR`, `DB`, `SEC`.
- Every feature spec separates verified reference behavior, proposed desktop behavior, open questions, and acceptance criteria.
- No dates or effort estimates are invented. Roadmap phases are evidence gates.
- The Android KB remains the authoritative Android-specific vault. This vault does not overwrite it.
- The user-supplied CSV remains at the desktop project root; it is evidence, not a live schema authority or connection configuration.
- Connection evidence, redaction rules, and the same-project verification gate are recorded in [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]].
- The desktop must use the existing Supabase project and schema under [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]; no new project, database, or parallel schema is approved.

## Relationship to the Android Knowledge Base

The existing Android vault is at `/data/data/com.termux/files/home/Neo_Child_Clinic/docs/Knowledge_Base/`. It contains source-cited Android notes including `Architecture Map`, `Database Schema`, `Row Level Security`, `Offline Synchronization`, `Inventory Management`, `Vaccination Management`, `Due Vaccination`, `Statistics Dashboard`, `Backup and Restore`, `Testing`, and the `Quality/` registers.

This desktop vault **links by path reference** rather than duplicating those notes. It records a verified drift: the Android `Home.md` cites commit `f8e5d8a`, while the current HEAD is `ca4bed4`; counts also differ (`351` main / `43` test / `22` migrations in the older note versus `352` / `41+8` / `23` now). The Android vault was intentionally left unchanged.

---

**Bottom line:** the documentation baseline is complete and the shared-backend constraint is now recorded as accepted. The desktop implementation is not started, and its connection status is **Missing**. The next meaningful milestone is proof that desktop can safely reuse the existing project — not a screen.
