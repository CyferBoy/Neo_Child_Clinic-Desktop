---
title: ADR-0007 Money, Dates, and Identity
doc_status: proposed
evidence: Android/schema type findings + Phase 0B CSV/type reconciliation
updated: 2026-10-20
---

# ADR-0007 — Money, Dates, and Identity

**Status:** Proposed.

## Context

The shared schema stores most money as `numeric` (exact decimal), except `expenses.amount_paise` (`bigint`); the Android client maps most amounts to `Double`. The schema also uses text business dates, formatted strings for sorting, and a separate human-facing clinic ID. Client-side floating arithmetic and these representations have produced confirmed sorting, rounding, and timezone defects.

## Decision

- **Money:** store/calculate in integer minor units (paise) in the desktop domain. Convert explicitly at the shared-schema boundary with documented rounding. Never compare floats for equality.
- **Dates:** use typed date/time values in Go and ISO-8601 at boundaries. Business dates are not timestamps. Reporting/due classification uses IST (`Asia/Kolkata`). Display formats are presentation-only; never sort formatted strings.
- **Identity:** UUIDs for entity identity; a separate human-facing patient clinic ID with a unique constraint. Never key records by display name, phone, or formatted date.
- **Receipts:** server-assigned; immutable; never computed locally.
- **Soft delete:** explicit soft-delete/filter policy across reads, reports, exports, and sync, plus an approved deletion/absence reconciliation contract. Repository evidence contains no server tombstone feed; live status is unverified.

## Alternatives considered

| Alternative | Assessment |
|---|---|
| Mirror Android `Double`/text exactly | Repeats known client-side defects |
| Store money as decimal strings | Better than a `Double` calculation, but integer arithmetic is simpler and exact |
| Use device-local dates | Breaks IST reporting and multi-device due lists |
| Use names as keys | Duplicate/renamed patients corrupt identity |

## Consequences

Positive:
- Exact totals and receipt reconciliation.
- Stable sorting and due dates.
- Clear identity across devices.

Negative / risks:
- Boundary conversion with legacy data.
- Schema compatibility constraints.
- Existing Android clients may still send floating-point JSON numbers/text dates; boundary reconciliation is needed.

## Validation

- Property tests for money arithmetic and rounding.
- Clock/timezone tests for due lists and reports.
- Duplicate-name patient tests; clinic ID uniqueness.
- Replay tests for receipt/stock/payment identities.

## Open questions

- What precision/rounding rule applies to numeric amounts and legacy client `Double` values at the boundary?
- Is the clinic ID format fixed, and who can change it?
- Which deletion/absence reconciliation contract is approved, and how long are any deletion records retained?

## Related

[[Architecture/Offline-and-Sync-Design|Offline and Sync]] · [[Database/Database-Architecture|Database Architecture]] · [[Database/Schema-Reconciliation|Schema Reconciliation]] · [[Features/04-Patient-Management|Patient Management]] · [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]]
