---
title: Neo Child Clinic Desktop — Knowledge Base
doc_status: baseline
evidence: full discovery pass against Android repository and desktop project + shared-backend connection investigation + Phase 0B reconciliation + Phase 0C Supabase metadata exports (no SQL executed)
updated: 2026-10-21
---

# Neo Child Clinic Desktop — Knowledge Base

> **Baseline, not a completion claim.** The desktop application has **no source code**. This vault documents the verified Android reference, the target desktop design, the 22 Phase 1 specifications, the audit, and the roadmap. Every statement is tagged by evidence type.

**Audit date:** 2026-10-20 (Phase 0B); **Phase 0C review:** 2026-10-21
**Android reference:** `/data/data/com.termux/files/home/Neo_Child_Clinic` — `main` @ `ca4bed406bfd246ad83878fff9a4e178ebc5670f`
**Desktop project:** `/storage/emulated/0/Neo_Child_Clinic_Desktop`
**Desktop implementation:** none
**Live Supabase access:** no SQL/HTTP session; only user-supplied metadata exports
**Desktop tests run:** 0
**Android tests run:** 0 in this pass

## Status at a glance

| | |
|---|---|
| Desktop modules specified | **22 of 22** |
| Desktop modules implemented | **0 of 22** |
| Desktop tests | **0** (no suite) |
| Android reference feature modules | 22 |
| Android reference status | 5 partially implemented, 17 unverified in this pass |
| Desktop repository | **Initialized; `main` pushed to GitHub** |
| Desktop instructions | **No `AGENTS.md`** |
| Installed skills | 17 `SKILL.md` files |
| Shared backend | **Existing Supabase project required** (ADR-0008); desktop connection **Missing** |
| Schema evidence | 16 metadata exports (2026-10-20/21): 24 tables / 416 columns / 77 constraints / 93 indexes / 179 policies / 744 ACL rows; Android repo CSV (23/361) is older; 55-row delta explained; runtime/project identity unverified |
| Android connection | Source-verified: HTTPS Supabase APIs + user JWT; live project identity unavailable |
| Supabase migration files | 23 |
| Android tracked files | 583 |
| Android test files | 41 unit + 8 instrumented |
| Existing Android KB | 37 Markdown notes; preserved unchanged |
| Critical open risks | No desktop source; **exported anon-reachable PHI/inventory path**; unverified same-project connection and runtime RLS; duplicate live stock triggers; no reproducible baseline; Oct 30 grant gap; doctor-slot contract mismatch; sync idempotency/deletion reconciliation; local PHI protection |

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
| Understand the backend/schema | [[Database/Database-Architecture|Database Architecture]] · [[Database/Schema-Reconciliation|Schema Reconciliation]] · [[Database/Data-Dictionary|Data Dictionary]] |
| Review the current schema/security evidence | [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] |
| Get live database/security evidence | [[Database/Live-Verification-Queries|Live Verification Queries — Read Only]] |
| Review the shared-backend connection evidence | [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] |
| Review security/privacy | [[Security/Security-Model|Security Model]] · [[Security/Threat-Model|Threat Model]] |
| Review the prior architecture/readiness review | [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]] |
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
- [[Database/Schema-Reconciliation|Schema Reconciliation — Phase 0B/0C]]
- [[Database/Live-Verification-Queries|Live Verification Queries — Read Only]]
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
- [[Audits/Documentation-Validation|Documentation Validation — Second Pass]]
- [[Audits/Phase-0B-Architecture-Review|Phase 0B — Blocker Resolution and Architecture Review]]
- [[Audits/Phase-0C-Schema-Export-Review|Phase 0C — Schema Export Review and Reconciliation]]
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
- The 2026-10-20 and 2026-10-21 column exports both list 24 public tables and 416 columns and agree on all 416 keys/values. The broader 2026-10-21 set reports 77 constraints, 93 indexes, 179 policy rows, 744 table ACL rows, 61 triggers, 21 functions, and 23 Realtime members. See [[Audits/Phase-0C-Schema-Export-Review|Phase 0C]].
- The older Android-repository CSV lists 23 tables and 361 columns, uses camelCase `waste_records` names, and is superseded. The 55-column difference is fully explained by soft-delete fields, the waste rename, and `api_write_rate_limits`.
- The exports contain no project URL, project reference, auth setting, key, or credential. They are metadata snapshots, not proof of runtime behavior, and no SQL was executed for this review.
- Repository migrations create only 9 of the 24 newer-snapshot tables from zero; the other 15 are baseline tables present in both snapshots. Six reported columns are not reproducible from migrations, `todo_notification_events` is absent, and at least one migration is missing. A live catalog and baseline plan are still required.
- Android constructs a supabase-kt client from `BuildConfig.SUPABASE_URL` and `BuildConfig.SUPABASE_ANON_KEY`; the values come from `.env.local` or environment at build time. The actual values are absent from the clean worktree.
- Android uses PostgREST over HTTPS with the signed-in user's JWT, plus Supabase Auth, Storage (`patient-docs`), Edge Function `manage-staff`, and Realtime refresh triggers. No direct PostgreSQL driver or `.rpc` call was found.
- Android reads authorization from `app_metadata.role`; sessions are stored in Keystore-backed encrypted preferences. Server-side `manage-staff`/`notify-update` use the service-role key only in Edge Functions.
- **Exported security state is not production-safe:** 22 tables have full anon/auth ACLs, ten tables have an anon-reachable legacy policy path, `reminders` is permissive for any authenticated user, and all 21 functions are anon-executable. This is a metadata finding needing confirmation/remediation, not an executed exploit test.
- The desktop has no connection code, configuration, database, or tests; its connection status is **Missing**, not “working.”

## What is proposed

`[PROPOSED]`
- The Wails/Go/React architecture, SQLite local store, outbox/transaction-group sync, OS keychain session handling, encrypted backup, desktop notifications, printing, and update flow.
- The 22 feature specifications and their acceptance criteria.
- The permission matrix, roadmap, milestones, test plan, and release checklist.

## What is unknown

`[UNKNOWN]`
- The actual existing project URL, project reference, and publishable-key value. They are not in the worktree; same-project identity cannot be proven yet.
- Runtime Supabase behaviour: whether the exported anon/legacy-policy path actually returns rows/writes, Storage bucket privacy/limits, Realtime RLS, Auth public-signup state, `handle_new_user` attachment, and the migration ledger.
- Whether `todo_notification_events` exists live; it is referenced by migration but absent from every export. `sync_queue`, `widget_due_cache`, `inventory_deductions`, and `backup_history` are local-only Room tables.
- Whether the project's default ACLs survive the 2026-10-30 Data API change; the seven migration-created business tables have no explicit grants.
- Whether `doctor_slot_exceptions.start_minute`/`end_minute` will be added or removed from the client contract.
- Whether the Android test suite or the repository's SQL RLS tests currently pass; neither was run.
- The approved non-destructive verification path for the existing project.
- Desktop OS support, Wails version, local encryption approach, update provider, and printing requirements.
- Clinic retention/privacy policy and pilot ownership.

## Current blockers

1. No desktop application source. The Git repository exists, but `AGENTS.md` and CI are still missing. Branch protection is not verifiable from repository contents; confirm it in GitHub settings.
2. The actual existing project identity/configuration is absent; same-project connection is not proven.
3. Metadata is now reviewed, but runtime security is not: the export reports an anon-reachable path to ten clinical/inventory tables, `reminders` open to any authenticated user, and broad table/function grants. Confirm or disprove with synthetic anon/non-staff tests before any connection.
4. Stock is evidenced as trigger mode with **two** triggers and the old function; `20261017` has not taken effect and its guard would fail. Inventory writes are blocked.
5. No reproducible baseline: 15 tables lack `CREATE TABLE`, six reported columns are absent from migrations, and `todo_notification_events` is missing from the export.
6. Seven migration-created business tables have no explicit grants and are not October 30-ready.
7. The Android `doctor_slot_exceptions` contract sends columns the reported table does not have.
8. No approved deletion/absence contract; no server tombstone feed is evidenced.
9. No approved local encryption, key recovery, backup/retention, sync, or auth design; ADR-0001–0007 remain proposed.
10. No desktop toolchain, test/release pipeline, or approved Phase 1 pilot scope.

## Immediate next actions

1. Add `AGENTS.md` and CI to the existing desktop repository; confirm and configure branch protection through authenticated GitHub settings.
2. Obtain the approved existing-project configuration through a secure channel and verify a redacted project fingerprint; do not print or commit the values.
3. Confirm the exported anon/legacy-policy path with synthetic data, then remediate and re-test `anon` plus a non-staff authenticated account. Do not use real PHI.
4. Reconcile table/function grants, including the seven business tables and `service_role`; plan a post-2026-10-30 ACL re-export.
5. Fix the stock duplicate/guard and verify exactly one writer; reconcile ledger to physical stock before enabling inventory writes.
6. Resolve the doctor-slot contract and approve a reviewed baseline covering the six live-only columns.
7. Review and approve or reject D1–D14 in [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]]; ADR-0008 is already accepted.
8. Approve the deletion/absence contract and the local encryption/backup/retention policy.
9. Implement the trust-boundary spike only after approvals: same-project auth, keychain, local DB, typed binding, redacted logging.
10. Keep the Phase 0C backend-readiness matrix current; re-run link and secret checks before handoff.

## Documentation conventions

- Stable requirement IDs: `PLAT`, `AUTH`, `STF`, `PAT`, `VAC`, `CON`, `INV`, `WAS`, `BRW`, `REM`, `PER`, `FIN`, `RCP`, `DSH`, `RPT`, `OFF`, `SYNC`, `BAK`, `NOT`, `SET`, `AUD`, `UPD` plus cross-cutting `ERR`, `DB`, `SEC`.
- Every feature spec separates verified reference behavior, proposed desktop behavior, open questions, and acceptance criteria.
- No dates or effort estimates are invented. Roadmap phases are evidence gates.
- The Android KB remains the authoritative Android-specific vault. This vault does not overwrite it.
- The user-supplied metadata exports are under `docs/Schemas/`; they are evidence, not a live schema authority, runtime certification, or connection configuration.
- Connection evidence, redaction rules, and the same-project verification gate are recorded in [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]].
- The desktop must use the existing Supabase project and remote schema under [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]; no new project, separate remote PostgreSQL database, or parallel remote schema is approved. Local SQLite is expected.

## Relationship to the Android Knowledge Base

The existing Android vault is at `/data/data/com.termux/files/home/Neo_Child_Clinic/docs/Knowledge_Base/`. It contains source-cited Android notes including `Architecture Map`, `Database Schema`, `Row Level Security`, `Offline Synchronization`, `Inventory Management`, `Vaccination Management`, `Due Vaccination`, `Statistics Dashboard`, `Backup and Restore`, `Testing`, and the `Quality/` registers.

This desktop vault **links by path reference** rather than duplicating those notes. It records a verified drift: the Android `Home.md` cites commit `f8e5d8a`, while the current HEAD is `ca4bed4`; counts also differ (`351` main / `43` test / `22` migrations in the older note versus `352` / `41+8` / `23` now). The Android vault was intentionally left unchanged.

---

**Bottom line:** the 55-row column discrepancy is reconciled, and Phase 0C now gives a coherent metadata picture: 24 tables, 416 columns, 77 constraints, 93 indexes, 179 policies, and 744 ACL rows. That picture is **not production-safe as reported** — anon can reach ten clinical/inventory tables through legacy policies, `reminders` is open to any authenticated user, and all functions are anon-executable. The stock fix is not deployed; seven business tables lack explicit grants. The desktop implementation remains unstarted and connection **Missing**. The Phase 0C conclusion is **BLOCKED ON CRITICAL SECURITY/SCHEMA EVIDENCE**, not on documentation polish.
