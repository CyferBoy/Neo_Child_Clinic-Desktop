---
title: Test Strategy
doc_status: proposed
evidence: Android test baseline + target architecture + Test Case Catalog
updated: 2026-10-21
---

# Test Strategy

> **No tests were run for this baseline.** The desktop has no test suite. Android has 41 unit test files and 8 instrumented test files; the existing Android KB reports 277 unit tests passing on 2026-10-18, but that result was **not re-run** in this pass and is not a desktop result. Backend tests must target the **existing** Supabase project through an approved non-destructive path; see [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]].

## Objectives

- Prevent patient identity, clinical, stock, payment, receipt, and audit data loss.
- Prove offline write and sync convergence.
- Prove authorization with real roles and RLS.
- Prove both clients use the same existing project identity and schema.
- Prove recovery (backup/restore) and update safety.
- Catch parity regressions against the Android reference.
- Keep tests fast enough for every change.

## Test levels

| Level | Scope | Tooling (proposed) | Runs |
|---|---|---|---|
| Domain unit | Pure Go rules: money, dates, stock, due dates, merge, validation | Go `testing` | Every commit |
| Contract | Wails bindings, request/response, error codes | Go + TS type tests | Every commit |
| Repository/integration | SQLite migrations, transactions, outbox | Go + temp SQLite | Every commit |
| Backend integration | PostgREST, RLS, functions, receipt sequence, Storage | Approved non-destructive path against the existing project | PR/nightly |
| React component | Forms, tables, states, accessibility | Component test runner | Every commit |
| E2E | Critical staff workflows | Browser/desktop automation | PR/nightly |
| Sync chaos | Timeout, 401/403/409/429/500, duplicate, partial group, deletion reconciliation (contract TBD) | Fault-injecting harness | Nightly/pre-release |
| Backup/restore | Round-trip, wrong passphrase, tamper, interruption | CLI/E2E | Pre-release |
| Printing | Preview, failure, retry, no PHI leak | Manual + integration | Pre-release |
| Update | Signature, version, rollback | Harness | Pre-release |
| Accessibility | Keyboard, focus, labels, contrast | Automated + manual | Pre-release |
| Performance | Large lists, slow disk, sync backlog; see [[Audits/Performance-Review|Performance Review]] | Benchmarks | Pre-release |

## Critical scenarios

1. Create patient offline, restart, reconnect, sync once.
2. Duplicate clinic ID rejected with a clear conflict.
3. Vaccination creates visit, items, stock, reminder, payment, receipt link, audit as one local transaction.
4. Replay the vaccination outbox group; no duplicate visit/payment/stock.
5. Batch stock insufficient/expired; transaction rolls back.
6. Delete on device A; pull on device B; row remains deleted. This is blocked until an approved deletion/absence contract exists; it is not satisfied by the current hard-delete pull behavior.
7. Concurrent patient edit; conflict visible, no silent overwrite.
8. Cash/online/mixed payment totals reconcile to the visit.
9. Receipt number is server-assigned and immutable.
10. Report totals exclude soft-deleted rows and count income once.
11. Due list uses IST, including a device in another timezone.
12. Restore backup into a clean install; counts/amounts match.
13. Interrupt restore; previous DB intact.
14. Lost laptop: locked app does not reveal PHI; local files are not plaintext.
15. Deactivated staff cannot refresh or access data.
16. Malicious note content is escaped, not executed.
17. Printer failure does not lose payment/receipt state.
18. Update signature failure keeps the current version.
19. Android and desktop resolve the same existing project identity via a redacted fingerprint.
20. Android-created patient/visit is read and updated by desktop; desktop-created row is read by Android; no duplicate records.
21. Desktop contains no service-role key, database password, or direct PostgreSQL connection; privileged staff changes go through the existing Edge Function.
22. Desktop does not create remote tables, run production migrations, or use a second remote PostgreSQL database. Local SQLite tables and migrations are expected.
23. Borrowed vaccine partial return decreases the outstanding balance once and leaves the record open until fully settled.
24. A visit with both vaccination and consultation payment is counted once in finance, dashboard, and reports.
25. The exported duplicate stock-trigger state blocks inventory writes; after an approved fix, one stock movement is applied once.
26. Receipts at a financial-year boundary use the server-assigned series and never a client-invented number.

## Test case catalog

[[Testing/Test-Case-Catalog|Test Case Catalog]] contains 126 stable planned IDs, grouped by module and cross-cutting security/database concern. It is the source for the IDs referenced by [[Roadmap/Requirements-Traceability|Requirements Traceability]].

A catalog entry is not a test implementation. Each future test must record its actual file/symbol, run date, build hash, dataset, and result. Changing a scenario requires a new ID; do not reuse a retired ID for a different assertion.

## Test data

- Synthetic patients with clearly fake names/phones.
- No production PHI in dev/CI.
- Seed data for edge cases: duplicate names, missing DOB, expired batch, zero stock, mixed payment, overdue reminder, soft-deleted patient.
- Fixed clock for date tests; explicit IST timezone.
- Deterministic IDs for replay tests.

## Environments

- Local: fast unit/component/integration.
- CI: full suite against synthetic SQLite/fake backend.
- Shared-backend verification: RLS, API contract, Storage, and cross-client tests against the existing project using approved test accounts and synthetic/reversible rows; no production data mutation. A separate harness requires explicit approval and must never be the desktop backend.
- Pre-release: signed build on target OS, real printer, slow/offline network simulation against the approved path.

## Coverage policy

No arbitrary percentage target is asserted. Coverage is risk-based:
- 100% of P0 requirements have at least one automated check.
- Every money/stock/receipt/auth/sync transaction has a failure-path test.
- Every destructive action has a negative test.
- Every role has an authorization test.

## Release gates

- No P0/P1 failing test.
- RLS suite green on the approved shared-backend verification path.
- Sync replay and deletion-reconciliation suites green; deletion contract approved.
- Backup restore and interruption tests green.
- No critical/high security finding without approved exception.
- Accessibility checklist complete.
- Test evidence attached to release checklist.

## Unavailable / not run

- Android Gradle tests: not run.
- Android instrumented tests: not run; no emulator evidence.
- Live Supabase RLS/Storage tests: not run; actual project configuration and live access were unavailable.
- Cross-client Android/desktop tests: not run; no desktop implementation.
- Desktop tests: none exist.
- Performance/print/accessibility: not run.

## Related

[[Testing/Test-Case-Catalog|Test Case Catalog]] · [[Testing/Regression-Matrix|Regression Matrix]] · [[Audits/Performance-Review|Performance Review]] · [[Roadmap/Phase-1-Implementation-Plan|Phase 1 Plan]] · [[Audits/Initial-Audit|Initial Audit]] · [[Releases/Release-Checklist|Release Checklist]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
