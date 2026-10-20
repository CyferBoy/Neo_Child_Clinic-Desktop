---
title: Vaccine and Batch Inventory
feature_id: INV
doc_status: proposed
desktop_status: Missing
android_status: Partially implemented
evidence: Android source + Knowledge Base
updated: 2026-10-20
---

# 07. Vaccine and Batch Inventory

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Partially implemented. Evidence: `feature/inventory/`, Android KB `Inventory Management`. Historical sorting/lost-update/trigger findings are fixed; NCC-027 and NCC-030 remain open low-severity gaps.

**Requirement IDs:** `INV-001`, `INV-002`, `INV-003`, `INV-004`, `INV-005`, `INV-006`, `INV-007`

## 1. Purpose and scope

Maintain the vaccine catalog, batch-level stock, expiry, low-stock thresholds, and an auditable stock ledger; support safe batch receipt and adjustment.

## 2. Actors

- Admin
- Inventory manager
- Nurse (read/consume)

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Create/edit a vaccine catalog item (brand, type, manufacturer, pricing).
2. Add a batch with number, dates, quantities, supplier, cost, selling price.
3. View stock by vaccine and batch, including expiry/low stock.
4. Adjust stock with reason and audit.
5. View stock history/ledger.
6. Reserve/consume stock through clinical workflows, not direct quantity edits.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Catalog/batches skeleton. |
| Empty | No vaccines/batches; add action. |
| Ready | Stock table with expiry/low-stock indicators. |
| Editing | Batch form with calculated totals. |
| Conflict | Concurrent quantity change; reload/compare. |
| Offline | Local read/write with pending badge. |
| Error | No partial batch write. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `INV-001` | Stock is tracked per batch and every movement is recorded in a ledger. | P0 |
| `INV-002` | Quantities cannot go negative; expired batches are not available for use. | P0 |
| `INV-003` | Batch edits are transactional and protected against lost updates. | P0 |
| `INV-004` | Expiry and low-stock views use typed dates and explicit thresholds. | P1 |
| `INV-005` | Stock adjustments require a reason, actor, and audit. | P1 |
| `INV-006` | The desktop reconciles server-side stock trigger effects instead of double-applying them. | P0 |
| `INV-007` | Batch numbers and catalog identities are unique per defined policy. | P1 |

## 7. Validation and business rules

### Validation

- Vaccine brand/type required.
- Batch number required and unique per policy.
- Expiry after purchase date; not expired for use.
- Quantities >= 0; purchase >= remaining.
- Prices non-negative.
- Adjustment reason required.

### Business rules

- Batch is the stock unit; do not store only a vaccine total.
- Derived stock excludes expired batches where the reference does.
- One ledger path for consumption/waste/borrow/adjustment.
- Never sort formatted date strings.
- Low stock uses an explicit threshold policy.
- Do not let a retried sync apply a stock delta twice.

## 8. Permissions

- Read: all clinical roles.
- Catalog/batch/adjust: admin/inventory manager.
- Consumption: clinical roles via vaccination/waste/borrow.

## 9. Offline and data behavior

- Catalog/batch edits local with outbox.
- Stock reads local.
- Concurrent-device conflicts need a clear resolution; no blind overwrite.

## 10. Errors and recovery

- Duplicate batch -> conflict.
- Expired batch -> blocked for use.
- Insufficient quantity -> rollback.
- Concurrent edit -> conflict, not lost update.
- Server trigger mismatch -> reconciliation error.

## 11. Edge cases

- Same batch number from different suppliers.
- Partial receipt.
- Expiry today.
- Zero stock.
- Batch edited during vaccination.
- Date string variants.

## 12. Acceptance criteria

- [ ] Stock never negative after any workflow.
- [ ] Expired batch cannot be selected for a new vaccination.
- [ ] Concurrent adjustments do not lose a movement.
- [ ] Ledger reconciles to batch remaining quantity.
- [ ] Low-stock list uses the configured threshold.

## 13. Test notes

- Unit: expiry, thresholds, date ordering.
- Integration: batch transaction, adjustment ledger.
- Chaos: concurrent edit, retry, server trigger.
- E2E: add batch and view stock.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

## 14. Dependencies

- [[Features/16-Local-Persistence-and-Offline-Operation|Local Persistence]]
- [[Features/17-Supabase-Sync|Sync]]
- [[Features/05-Vaccination-Management|Vaccination]]

## 15. Open questions

- Is FEFO mandatory?
- Who approves stock adjustments?
- Is low-stock global or per vaccine?
- How are supplier returns handled?

## 16. Related

- [[Features/08-Wastage|Wastage]]
- [[Features/09-Borrowed-and-Lent-Vaccines|Borrow/Return]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
