---
title: Regression Matrix
doc_status: proposed
evidence: feature inventory + current Android source/Bug Register at ca4bed4 + Test Case Catalog
updated: 2026-10-21
---

# Regression Matrix

> **Desktop tests: none.** Every row is a proposed regression check. "Reference risk" names the Android failure mode the desktop must not repeat. "Planned tests" points to [[Testing/Test-Case-Catalog|Test Case Catalog]] IDs; none is implemented or executed.

## Module regressions

| # | Module | Critical scenario | Test type | Reference risk | Planned tests | Desktop status |
|---|---|---|---|---|---|---|
| 01 | Shell/navigation | Offline start, guarded route, sync banner, sign-out warning | E2E/component | No desktop shell | `TC-PLAT-01..05` | Missing |
| 02 | Auth/session | Login, refresh, revoke, inactive account, missing role, cold start offline | Integration/E2E | Role defaulting, revoked token | `TC-AUTH-01..07` | Missing |
| 03 | Staff/roles | Create, edit, deactivate, self-guard, role claim update | Backend integration/E2E | Self-role change, stale token | `TC-STF-01..05` | Missing |
| 04 | Patients | Create offline, duplicate clinic ID, edit, merge, stale timeline | Unit/integration/E2E | Historical validation fixed; duplicate clinic-ID/merge identity risk | `TC-PAT-01..06` | Missing |
| 05 | Vaccinations | Transaction rollback, retry idempotency, stock reversal, reminder creation | Integration/chaos/E2E | Historical duplicate/stock defects fixed; retry idempotency remains a target | `TC-VAC-01..07` | Missing |
| 06 | Consultations | Create/edit, follow-up, linked payment, delete | Integration/E2E | Orphan payment, wrong visit link | `TC-CON-01..04` | Missing |
| 07 | Inventory | Batch add, FEFO, expiry, concurrent adjustment, low stock, trigger gate | Unit/integration/chaos | Historical sorting/lost-update/trigger defects fixed; exported duplicate trigger remains | `TC-INV-01..06` | Missing |
| 08 | Wastage | Waste reduces batch once, reason, audit | Integration | Double deduction | `TC-WAS-01..03` | Missing |
| 09 | Borrow/return | Borrow quantity, partial return, over-return, batch link, overdue | Integration | Batch mismatch, outstanding balance | `TC-BRW-01..05` | Missing |
| 10 | Vaccination reminders | Due/overdue/completed, IST boundary, deletion reconciliation | Unit/clock/E2E | Historical timezone defect fixed; no deletion/absence contract | `TC-REM-01..05` | Missing |
| 11 | Personal reminders | Blank date, advance payment, status transition, notification | Unit/integration | NCC-034 reclassified as not a bug; status/precedence risk | `TC-PER-01..04` | Missing |
| 12 | Finance | Cash/online/mixed, edit, one income per visit, expense validation, refund | Unit/integration/security | Historical double-count fixed; replay/duplicate risk | `TC-FIN-01..05` | Missing |
| 13 | Receipts/printing | Server number, immutable, print preview, printer failure, FY boundary | Integration/E2E/manual | Client-computed number; sequence exposure | `TC-RCP-01..06` | Missing |
| 14 | Dashboard | Today counts, empty/offline, role visibility, event burst | Component/E2E | Stale aggregates; over-broad refresh | `TC-DSH-01..04` | Missing |
| 15 | Reports | Date windows, soft delete, income once, vaccine brand filter | Golden data | Historical double-count/filter defects fixed; regression target | `TC-RPT-01..05` | Missing |
| 16 | Local persistence | Migration, crash/restart, disk full, corruption, encryption | Integration/fault/security | No local DB; no encryption test | `TC-OFF-01..05` | Missing |
| 17 | Sync | Replay, partial group, 401/403/409/429/500, deletion reconciliation, cursor | Chaos | Historical waiter/chain/conflict defects fixed; NCC-023/025 open; NCC-038 needs a decision | `TC-SYNC-01..09` | Missing |
| 18 | Backup/recovery | Round-trip, wrong passphrase, tamper, interruption, safety snapshot | CLI/E2E/security | Destructive restore; no end-to-end desktop test; crypto/validator tests exist only in Android | `TC-BAK-01..06` | Missing |
| 19 | Notifications | Permission, quiet hours, due reminder, no PHI preview | Integration/manual | Historical notification defects fixed; preview/role risk remains | `TC-NOT-01..04` | Missing |
| 20 | Settings | Theme, pharmacy/inventory thresholds, security, backup prefs | Component | Unsafe defaults | `TC-SET-01..04` | Missing |
| 21 | Audit | Append-only, actor identity, paging, export redaction | Integration/E2E | Forged/overwritten audit | `TC-AUD-01..04` | Missing |
| 22 | Updates | Signature, version monotonicity, rollback, offline | Harness/manual | Unsigned update | `TC-UPD-01..05` | Missing |

## Cross-cutting regression suite

- Authorization: `TC-SEC-01..12` (anon, non-staff, active roles, deactivated, Storage, Realtime, default ACL, same-project fingerprint).
- Money: `TC-FIN-01..05`, `TC-RPT-01..05` (integer minor units, rounding, receipt totals).
- Dates: `TC-REM-01`, `TC-DSH-02`, `TC-RPT-03` (IST, DST-free assumption for India, invalid/empty dates).
- Soft delete: `TC-PAT-05`, `TC-RPT-02`, `TC-SYNC-07` (reads, reports, exports, deletion/absence reconciliation; contract TBD).
- PHI: `TC-SEC-07`, `TC-AUD-03`, `TC-NOT-03`, `TC-BAK-06` (logs, crash reports, window titles, notifications, print spool).
- Accessibility: no dedicated IDs yet; keyboard-only core workflows must be added before release.
- Performance: no execution; see [[Audits/Performance-Review|Performance Review]] for provisional 10k/50k/5k synthetic targets.

## Execution status

| Metric | Value |
|---|---|
| Implemented regression tests | 0 |
| Executed regression runs | 0 |
| Passing desktop checks | 0 |
| Blocked suites | Inventory writes, shared-backend RLS/Storage/Realtime, cross-client parity, packaging/update |

## Related

[[Testing/Test-Strategy|Test Strategy]] · [[Testing/Test-Case-Catalog|Test Case Catalog]] · [[Product/Feature-Inventory|Feature Inventory]] · [[Roadmap/Requirements-Traceability|Requirements Traceability]] · [[Audits/Performance-Review|Performance Review]]
