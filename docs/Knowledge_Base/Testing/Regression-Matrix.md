---
title: Regression Matrix
doc_status: proposed
evidence: feature inventory + Android confirmed findings
updated: 2026-10-20
---

# Regression Matrix

> **Desktop tests: none.** Every row is a proposed regression check. "Reference risk" names the Android failure mode the desktop must not repeat.

| # | Module | Critical scenario | Test type | Reference risk | Desktop status |
|---|---|---|---|---|---|
| 01 | Shell/navigation | Offline start, guarded route, sync banner, sign-out warning | E2E/component | No desktop shell | Missing |
| 02 | Auth/session | Login, refresh, revoke, inactive account, missing role, cold start offline | Integration/E2E | Role defaulting, revoked token | Missing |
| 03 | Staff/roles | Create, edit, deactivate, self-guard, role claim update | Backend integration/E2E | Self-role change, stale token | Missing |
| 04 | Patients | Create offline, duplicate clinic ID, edit, merge, stale timeline | Unit/integration/E2E | Validation swallowed, stale cache | Missing |
| 05 | Vaccinations | Transaction rollback, retry idempotency, stock reversal, reminder creation | Integration/chaos/E2E | Duplicate visit, missing ledger | Missing |
| 06 | Consultations | Create/edit, follow-up, linked payment, delete | Integration/E2E | Orphan payment, wrong visit link | Missing |
| 07 | Inventory | Batch add, FEFO, expiry, concurrent adjustment, low stock | Unit/integration/chaos | String date sort, lost update, trigger double-apply | Missing |
| 08 | Wastage | Waste reduces batch once, reason, audit | Integration | Double deduction | Missing |
| 09 | Borrow/return | Borrow quantity, partial return, batch link, overdue | Integration | Batch mismatch | Missing |
| 10 | Vaccination reminders | Due/overdue/completed, IST boundary, tombstone | Unit/clock/E2E | Device timezone, resurrection | Missing |
| 11 | Personal reminders | Blank date, advance payment, status transition, notification | Unit/integration | Blank-date notification loop | Missing |
| 12 | Finance | Cash/online/mixed, edit, one income per visit, expense validation | Unit/integration | Double-count, duplicate income | Missing |
| 13 | Receipts/printing | Server number, immutable, print preview, printer failure | Integration/E2E/manual | Client-computed number | Missing |
| 14 | Dashboard | Today counts, empty/offline, role visibility | Component/E2E | Stale aggregates | Missing |
| 15 | Reports | Date windows, soft delete, income once, vaccine brand filter | Golden data | Double-count, inconsistent filter | Missing |
| 16 | Local persistence | Migration, crash/restart, disk full, corruption | Integration/fault | No local DB | Missing |
| 17 | Sync | Replay, partial group, 401/403/409/429/500, tombstone, cursor | Chaos | Waiter reports success, unbounded chain | Missing |
| 18 | Backup/recovery | Round-trip, wrong passphrase, tamper, interruption, safety snapshot | CLI/E2E | Destructive untested restore | Missing |
| 19 | Notifications | Permission, quiet hours, due reminder, no PHI preview | Integration/manual | Timezone/preview leak | Missing |
| 20 | Settings | Theme, pharmacy/inventory thresholds, security, backup prefs | Component | Unsafe defaults | Missing |
| 21 | Audit | Append-only, actor identity, paging, export redaction | Integration/E2E | Forged/overwritten audit | Missing |
| 22 | Updates | Signature, version monotonicity, rollback, offline | Harness/manual | Unsigned update | Missing |

## Cross-cutting regression suite

- Authorization: every role, every sensitive route, direct binding calls.
- Money: integer minor units, rounding, receipt totals.
- Dates: IST, DST-free assumption for India, invalid/empty dates.
- Soft delete: reads, reports, exports, sync tombstones.
- PHI: logs, crash reports, window titles, notifications, print spool.
- Accessibility: keyboard-only core workflows.
- Performance: 10k patients, 50k vaccination items, 5k batches (synthetic benchmark sizes are targets, not measured facts).

## Related

[[Testing/Test-Strategy|Test Strategy]] · [[Product/Feature-Inventory|Feature Inventory]] · [[Roadmap/Requirements-Traceability|Requirements Traceability]]
