---
title: Borrowed and Lent Vaccines
feature_id: BRW
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 09. Borrowed and Lent Vaccines

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/borrowed/`, `domain/model/BorrowedVaccine.kt`, `BorrowReturnRecord.kt`.

**Requirement IDs:** `BRW-001`, `BRW-002`, `BRW-003`, `BRW-004`, `BRW-005`

## 1. Purpose and scope

Track vaccines lent to or borrowed from another clinic/doctor by batch, including partial returns and outstanding balances.

### User stories

- As a nurse, I can lend or borrow a batch and see the outstanding balance.
- As an inventory manager, I can record a partial return without closing the record.
- As an admin, I can mark a lost or damaged balance without creating phantom stock.

## 2. Actors

- Admin
- Nurse
- Inventory manager

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Record a borrow/lend with counterparty, vaccine, batch, quantity, date.
2. Reduce available stock for lent items or record incoming borrowed stock.
3. Record full/partial return.
4. View history and outstanding quantities.
5. Resolve lost/damaged items with an approved adjustment.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Borrow list. |
| Empty | No borrow records. |
| Ready | List with outstanding quantity/status. |
| Return | Return dialog with remaining balance. |
| Conflict | Over-return or closed record. |
| Offline | Local record/return with pending badge. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `BRW-001` | Borrow and return are batch-linked and keep an outstanding balance. | P0 |
| `BRW-002` | Returned quantity cannot exceed the outstanding borrowed/lent quantity. | P0 |
| `BRW-003` | Each movement is auditable and appears in stock history. | P1 |
| `BRW-004` | Partial returns do not duplicate or close the original record prematurely. | P0 |
| `BRW-005` | Lost/damaged items have an explicit, approved resolution path. | P2 |

## 7. Validation and business rules

### Validation

- Counterparty required.
- Vaccine/batch/quantity required.
- Quantity > 0 and <= available for lending.
- Return <= outstanding.
- Dates valid.

### Business rules

- Borrow is not a sale; it moves stock with an expected return.
- Batch identity is preserved.
- Returns restore stock once.
- No negative outstanding balance.

## 8. Permissions

- Admin/nurse/inventory manager (proposed).
- Audit read admin.

## 9. Offline and data behavior

- Local commit/outbox.
- Outstanding balance from local ledger; server conflict visible.

## 10. Errors and recovery

- Over-return -> block.
- Closed record -> block.
- Duplicate submit -> idempotent.
- Stock insufficient -> block.

## 11. Edge cases

- Partial return over multiple days.
- Borrowed item expires.
- Counterparty is a walk-in doctor.
- Lost item write-off.
- Batch merged/split.

## 12. Acceptance criteria

- [ ] Lend reduces stock once.
- [ ] Partial return restores only returned quantity.
- [ ] Outstanding balance correct.
- [ ] Over-return rejected.
- [ ] History is auditable.

## 13. Test notes

- Integration: borrow/return/partial.
- Unit: balance/validation.
- E2E: return dialog.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-BRW-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/07-Vaccine-and-Batch-Inventory|Inventory]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

`borrow_records`; `borrow_returns`; `vaccine_batches`; `inventory_transactions`; `audit_logs`.

## 15. Open questions

- Is borrowing allowed across clinics?
- Who can write off a lost item?
- Are due dates/reminders required?

## 16. Related

- [[Features/08-Wastage|Wastage]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
