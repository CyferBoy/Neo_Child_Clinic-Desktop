---
title: ADR-0007 Money, Dates, and Identity
doc_status: proposed
evidence: Android/schema type findings
updated: 2026-10-20
---

# ADR-0007 — Money, Dates, and Identity

**Status:** Proposed.

## Context

The shared schema and Android reference use floating-point money, text dates, formatted strings for sorting, and a separate human-facing clinic ID. These patterns have produced confirmed sorting, rounding, and timezone defects.

## Decision

- **Money:** store/calculate in integer minor units (paise) in the desktop domain. Convert explicitly at the shared-schema boundary with documented rounding. Never compare floats for equality.
- **Dates:** use typed date/time values in Go and ISO-8601 at boundaries. Business dates are not timestamps. Reporting/due classification uses IST (`Asia/Kolkata`). Display formats are presentation-only; never sort formatted strings.
- **Identity:** UUIDs for entity identity; a separate human-facing patient clinic ID with a unique constraint. Never key records by display name, phone, or formatted date.
- **Receipts:** server-assigned; immutable; never computed locally.
- **Soft delete:** explicit tombstone/filter policy across reads, reports, exports, and sync.

## Alternatives considered

| Alternative | Assessment |
|---|---|
| Mirror floats/text exactly | Repeats known defects |
| Store money as decimal strings | Better than float, but integer arithmetic is simpler and exact |
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
- Existing Android clients may still write floats/text; reconciliation needed.

## Validation

- Property tests for money arithmetic and rounding.
- Clock/timezone tests for due lists and reports.
- Duplicate-name patient tests; clinic ID uniqueness.
- Replay tests for receipt/stock/payment identities.

## Open questions

- Can the shared schema adopt numeric money, or must desktop convert?
- What rounding rule applies to legacy float values?
- Is the clinic ID format fixed, and who can change it?
- How are soft-delete tombstones retained?

## Related

[[Architecture/Offline-and-Sync-Design|Offline and Sync]] · [[Database/Database-Architecture|Database Architecture]] · [[Features/04-Patient-Management|Patient Management]]
