---
title: Regression Matrix
doc_status: proposed
evidence: feature inventory + current Android source/Bug Register at ca4bed4
updated: 2026-10-20
---

# Regression Matrix

> **Desktop tests: none.** Every row is a proposed regression check. "Reference risk" names the Android failure mode the desktop must not repeat.

| # | Module | Critical scenario | Test type | Reference risk | Desktop status |
|---|---|---|---|---|---|
| 01 | Shell/navigation | Offline start, guarded route, sync banner, sign-out warning | E2E/component | No desktop shell | Missing |
| 02 | Auth/session | Login, refresh, revoke, inactive account, missing role, cold start offline | Integration/E2E | Role defaulting, revoked token | Missing |
| 03 | Staff/roles | Create, edit, deactivate, self-guard, role claim update | Backend integration/E2E | Self-role change, stale token | Missing |
| 04 | Patients | Create offline, duplicate clinic ID, edit, merge, stale timeline | Unit/integration/E2E | Historical validation fixed; duplicate clinic-ID/merge identity risk | Missing |
| 05 | Vaccinations | Transaction rollback, retry idempotency, stock reversal, reminder creation | Integration/chaos/E2E | Historical duplicate/stock defects fixed; retry idempotency remains a target | Missing |
| 06 | Consultations | Create/edit, follow-up, linked payment, delete | Integration/E2E | Orphan payment, wrong visit link | Missing |
| 07 | Inventory | Batch add, FEFO, expiry, concurrent adjustment, low stock | Unit/integration/chaos | Historical sorting/lost-update/trigger defects fixed; NCC-027/NCC-030 open | Missing |
| 08 | Wastage | Waste reduces batch once, reason, audit | Integration | Double deduction | Missing |
| 09 | Borrow/return | Borrow quantity, partial return, batch link, overdue | Integration | Batch mismatch | Missing |
| 10 | Vaccination reminders | Due/overdue/completed, IST boundary, deletion reconciliation | Unit/clock/E2E | Historical timezone defect fixed; no deletion/absence contract | Missing |
| 11 | Personal reminders | Blank date, advance payment, status transition, notification | Unit/integration | NCC-034 reclassified as not a bug; status/precedence risk | Missing |
| 12 | Finance | Cash/online/mixed, edit, one income per visit, expense validation | Unit/integration | Historical double-count fixed; replay/duplicate risk | Missing |
| 13 | Receipts/printing | Server number, immutable, print preview, printer failure | Integration/E2E/manual | Client-computed number | Missing |
| 14 | Dashboard | Today counts, empty/offline, role visibility | Component/E2E | Stale aggregates | Missing |
| 15 | Reports | Date windows, soft delete, income once, vaccine brand filter | Golden data | Historical double-count/filter defects fixed; regression target | Missing |
| 16 | Local persistence | Migration, crash/restart, disk full, corruption | Integration/fault | No local DB | Missing |
| 17 | Sync | Replay, partial group, 401/403/409/429/500, deletion reconciliation, cursor | Chaos | Historical waiter/chain/conflict defects fixed; NCC-023/025 open; NCC-038 needs a decision | Missing |
| 18 | Backup/recovery | Round-trip, wrong passphrase, tamper, interruption, safety snapshot | CLI/E2E | Destructive restore; no end-to-end test; crypto/validator tests exist | Missing |
| 19 | Notifications | Permission, quiet hours, due reminder, no PHI preview | Integration/manual | Historical notification defects fixed; preview/role risk remains | Missing |
| 20 | Settings | Theme, pharmacy/inventory thresholds, security, backup prefs | Component | Unsafe defaults | Missing |
| 21 | Audit | Append-only, actor identity, paging, export redaction | Integration/E2E | Forged/overwritten audit | Missing |
| 22 | Updates | Signature, version monotonicity, rollback, offline | Harness/manual | Unsigned update | Missing |

## Cross-cutting regression suite

- Authorization: every role, every sensitive route, direct binding calls.
- Money: integer minor units, rounding, receipt totals.
- Dates: IST, DST-free assumption for India, invalid/empty dates.
- Soft delete: reads, reports, exports, and deletion/absence reconciliation (contract TBD).
- PHI: logs, crash reports, window titles, notifications, print spool.
- Accessibility: keyboard-only core workflows.
- Performance: 10k patients, 50k vaccination items, 5k batches (synthetic benchmark sizes are targets, not measured facts).

## Related

[[Testing/Test-Strategy|Test Strategy]] · [[Product/Feature-Inventory|Feature Inventory]] · [[Roadmap/Requirements-Traceability|Requirements Traceability]]
