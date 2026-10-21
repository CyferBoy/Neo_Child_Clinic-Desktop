---
title: Performance Review
doc_status: proposed
evidence: Android source inspection + Phase 0C metadata exports + existing database access notes; no benchmark, profile, or query plan executed
updated: 2026-10-21
---

# Performance Review

> **No performance measurement was performed.** There is no desktop application to profile, no clinic dataset, and no live database access. This note records source-level findings, unmeasured risks, and proposed acceptance tests. Do not treat any number below as a measured production result.

## Scope and method

Reviewed:

- Android local queries and indexes (`data/local/`, `PatientDao.kt`, dashboard refresh paths).
- Android sync scheduling and refresh orchestration (`core/sync/`).
- The 24-table/416-column/93-index metadata export and the Phase 0C duplicate-index findings.
- The existing [Database Access Patterns](../Database/Access-Patterns.md) review.
- Desktop architecture proposals for local SQLite, Wails, and React.

Not reviewed or available:

- Desktop process, Go binary, Wails bridge, React bundle, or local SQLite file.
- Production row counts, growth rate, device specifications, network conditions, or Supabase query plans.
- A reproducible benchmark or profiling run.

## Source-level findings

| ID | Finding | Evidence | Assessment | Required desktop response |
|---|---|---|---|---|
| PERF-01 | Patient search is a broad `LIKE` query over name, phone, clinic ID, address, and visit text; address and visit search columns are not indexed by the local Room schema. | `PatientDao.kt` search query; exports report index names but no live query plan | **Potential risk requiring verification.** Small datasets may be fine; a full scan grows with visits and text columns. | Use indexed/trigram or normalized search columns, a result cap, and measured pagination. |
| PERF-02 | The export reports 93 indexes, 33 unique, with duplicate unique indexes/constraints on `patients`, `reminders`, `profiles`, and `user_devices`. | [Phase 0C](../Audits/Phase-0C-Schema-Export-Review.md) §6; export `L` | **Observed in an export.** Extra indexes add write/storage cost; duplicate uniques make upsert conflict targets ambiguous. | Do not rely on unconstrained `ON CONFLICT`; specify the exact conflict target or use server functions. Deduplicate only through an approved migration. |
| PERF-03 | Dashboard state is produced by a deeply nested `combine` graph with many dependencies and a 500 ms Realtime debounce. | `DashboardViewModel.kt` | **Confirmed in repository source.** Correctness-oriented workaround; unnecessary recomputation is possible but unmeasured. | Use one explicit reducer/selectors, targeted invalidation, and cancellation of stale loads. Measure rebuild count. |
| PERF-04 | Android has historically reloaded whole datasets after mutations and used N+1 patient refresh; the N+1 refresh was fixed at `b27d945` according to the Android KB. | Existing Android KB; repository history | **Confirmed in repository source/history.** Regression risk remains. | Use set-based queries and bounded refresh; add a regression test that counts queries or fails on N+1 fixture access. |
| PERF-05 | Android schedules sync work from queue writes; historical per-row scheduling/chain growth was fixed at `ca4bed4`. | `core/sync/SyncRepositoryImpl.kt`; Android KB | **Confirmed in repository source/history.** Do not reintroduce one worker chain per row. | Coalesce outbox work per transaction group; use a single durable scheduler key. |
| PERF-06 | The reference sync pull is a broad multi-step refresh; no pagination/cursor contract is complete for every table, and deletion reconciliation is unresolved. | `core/sync/CloudRefresh.kt`, `Offline Synchronization.md`, [Offline and Sync Design](../Architecture/Offline-and-Sync-Design.md) | **Confirmed in repository source.** Pull cost grows with table size; absence logic could amplify cost. | Define incremental pulls, cursors, page limits, and server-side indexes before pilot scale. |
| PERF-07 | The shared schema has 24 tables and 416 columns, with several text dates and text actor labels. | Phase 0C counts | **Observed in an export.** Schema size is modest; text dates and missing query predicates can still cause scans and timezone bugs. | Normalize query keys locally; do not sort formatted dates; measure the actual server queries. |
| PERF-08 | SQLCipher encryption and password KDF are on the startup/open path. | `SecurityUtils.kt`, `BackupCrypto.kt` | **Confirmed in repository source.** Cost depends on device and KDF settings; unmeasured. | Measure cold start, first query, and backup/restore on target hardware; keep key work off the UI thread. |
| PERF-09 | Backup/restore serializes business tables into a JSON container and applies a full restore. | `BackupRepositoryImpl.kt`, `BackupModels.kt` | **Confirmed in repository source.** Large backups and weak devices may exceed memory/time budgets. | Stream or chunk, enforce size limits, and test at 1×/5×/10× expected clinic size. |
| PERF-10 | Desktop report/export performance is entirely unmeasured; no dataset or query plan exists. | No desktop source | **Unknown.** | Define synthetic dataset sizes and acceptance budgets before implementation. |

## Reference evidence numbers

| Metric | Value | Meaning |
|---|---|---|
| Exported public tables | 24 | Metadata count, not row count |
| Exported columns | 416 | Metadata count |
| Exported indexes | 93 (33 unique) | Includes duplicate uniques; not a coverage measure |
| Exported policies | 179 rows | Policy count, not performance or correctness |
| Android main Kotlin files | 352 | Source size indicator only |
| Android unit/instrumented test files | 41 / 8 | Source count; not executed in this pass |
| Desktop tests | 0 | No desktop suite |
| Measured benchmarks | 0 | This review has no timing evidence |

## Proposed desktop budgets

These are **proposed acceptance targets for review**, not approved service levels and not measurements. They must be replaced or confirmed after a Phase 1 spike on named reference hardware and a synthetic dataset.

| Area | Proposed test | Provisional target |
|---|---|---|
| Cold start | Launch signed build, encrypted local DB, no network; first usable shell | ≤ 2.5 s on reference hardware |
| Patient search | 10,000 synthetic patients with visits; search by name/phone/clinic ID | First page ≤ 500 ms; bounded result count |
| Visit detail | Load one patient with 1,000 visits and linked items | ≤ 750 ms; no N+1 queries |
| Local write | Commit a 5-item vaccination group offline | ≤ 300 ms to local success |
| Sync | 1,000 queued events, partial failures | No unbounded memory; progress visible; bounded backoff |
| Dashboard | 10,000 patients, 5,000 doses, 2,000 reminders | ≤ 1 s for first paint; no full-table rebuild per event |
| Report | 12-month financial report over 50,000 payments | ≤ 3 s or documented streaming progress |
| Backup | 1×, 5×, 10× expected clinic data | Completes with size/time warning; restore verified |
| Memory | 8-hour shift with 10,000 patients cached | No unbounded growth; explicit cache eviction |

The numbers above are deliberately labelled provisional. A target without a dataset, hardware definition, and repeatable harness is not evidence.

## Query and schema risks for desktop

1. **Unbounded lists.** Every list needs a default filter, limit, and explicit pagination. “Load all patients/visits” is not a Phase 1 default.
2. **Duplicate unique indexes.** Upserts must name an exact conflict target; otherwise a duplicate natural key can produce ambiguous or failed writes.
3. **Text vs typed dates.** Search and sort predicates must use typed dates (or a canonical ISO form with a documented timezone), not display strings.
4. **Soft-delete filters.** An index that does not include the active-row predicate can still scan deleted rows. Every hot query needs an `is_deleted = false`-compatible index and a test with deleted data.
5. **Financial aggregation.** Reports must aggregate each income identity once. Performance work must not “fix” double counting by changing the report definition.
6. **Stock ledger aggregation.** Balance calculations must reconcile to the batch counter and must not scan unbounded history on the UI thread.
7. **Realtime amplification.** A change event must not trigger a full dashboard rebuild if a targeted invalidation is sufficient. Measure event-to-paint time under bursts.
8. **Encryption and backup.** Do not relax encryption to meet a performance target; measure and adjust KDF/chunking with security review.

## Required measurement plan

Before a pilot:

1. Define reference hardware (CPU, RAM, disk class) and supported OS versions.
2. Generate synthetic data at 1×, 5×, and 10× the clinic's expected annual volume; never use production PHI.
3. Measure cold start, local write, first paint, search, detail load, sync batches, report, backup, and restore.
4. Capture query counts from Go/local DB instrumentation, not just wall-clock time.
5. Store results with build hash, dataset profile, hardware, and date.
6. Add regression thresholds to CI before code is merged.
7. Re-test after encryption, index, sync, or schema changes.

No measurement plan has been executed.

## Related

[[Home]] · [[Architecture/Android-Reference-Architecture|Android Reference Architecture]] · [[Database/Access-Patterns|Database Access Patterns]] · [[Database/Database-Architecture|Database Architecture]] · [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] · [[Testing/Test-Strategy|Test Strategy]] · [[Testing/Test-Case-Catalog|Test Case Catalog]] · [[Audits/Risk-Register|Risk Register]]
