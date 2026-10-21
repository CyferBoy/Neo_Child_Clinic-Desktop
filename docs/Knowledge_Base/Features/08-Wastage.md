---
title: Wastage
feature_id: WAS
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 08. Wastage

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/waste/`, `domain/model/WasteRecord.kt`.

**Requirement IDs:** `WAS-001`, `WAS-002`, `WAS-003`, `WAS-004`

## 1. Purpose and scope

Record vaccine wastage against a specific batch, reduce available stock exactly once, capture a reason, and preserve an audit trail.

### User stories

- As a nurse, I can record wastage against a batch with a reason.
- As an inventory manager, I can reconcile wasted stock without a manual quantity correction.

## 2. Actors

- Admin
- Nurse
- Inventory manager

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Select vaccine and batch.
2. Enter quantity, date, and reason.
3. Validate available stock and expiry.
4. Commit waste and stock movement atomically.
5. View waste history and reconcile totals.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Batch selector. |
| Ready | Form with available quantity. |
| Saving | Single submit; local commit. |
| Pending sync | Visible record with badge. |
| Error | Rollback with field message. |
| Offline | Allowed; local commit. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `WAS-001` | Waste is batch-linked and reduces available stock exactly once. | P0 |
| `WAS-002` | Quantity must be positive and not exceed the batch's available quantity. | P0 |
| `WAS-003` | Waste requires a reason and an authenticated actor. | P1 |
| `WAS-004` | Waste is auditable and visible in stock history/reports. | P1 |

## 7. Validation and business rules

### Validation

- Batch and vaccine required.
- Quantity > 0 and <= available.
- Date valid.
- Reason required.

### Business rules

- Waste is a stock movement, not a direct quantity edit.
- Expired stock can be wasted but not used clinically.
- No negative stock.
- Retries are idempotent.

## 8. Permissions

- Admin/nurse/inventory manager (proposed).
- Audit read admin.

## 9. Offline and data behavior

- Local commit and outbox.
- Batch availability checked locally; server may conflict.

## 10. Errors and recovery

- Insufficient stock -> no commit.
- Duplicate submit -> same waste ID.
- Sync conflict -> visible reconciliation.

## 11. Edge cases

- Wasting all remaining stock.
- Expired batch.
- Partial vial/waste unit.
- Concurrent vaccination consumes stock.

## 12. Acceptance criteria

- [ ] Waste reduces batch once.
- [ ] Stock cannot go negative.
- [ ] Waste appears in history/audit.
- [ ] Offline waste syncs once.

## 13. Test notes

- Integration: waste + ledger.
- Unit: quantity validation.
- Chaos: duplicate/concurrent.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-WAS-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/07-Vaccine-and-Batch-Inventory|Inventory]]
- [[Features/21-Audit-Logging|Audit]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

`waste_records`; `vaccine_batches`; `inventory_transactions`; `audit_logs`.

## 15. Open questions

- Is a reason taxonomy required?
- Are partial vials tracked?
- Who approves large write-offs?

## 16. Related

- [[Features/15-Statistics-and-Reports|Reports]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
