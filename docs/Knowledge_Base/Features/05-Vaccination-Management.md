---
title: Vaccination Management
feature_id: VAC
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base
updated: 2026-10-20
---

# 05. Vaccination Management

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/vaccination/`, Android KB `Vaccination Management`. Historical stock/retry defects are fixed at `ca4bed4`; runtime verification is still absent.

**Requirement IDs:** `VAC-001`, `VAC-002`, `VAC-003`, `VAC-004`, `VAC-005`, `VAC-006`, `VAC-007`

## 1. Purpose and scope

Record a vaccination visit as one atomic local transaction: visit, vaccine items, batch stock movements, due reminders, payment, receipt link, and audit; support correction and deletion without duplicate stock or money effects.

## 2. Actors

- Admin
- Doctor
- Nurse

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Select patient and visit date.
2. Add one or more vaccines with batch, quantity, price, and expiry.
3. Validate stock and batch expiry; deduct stock through one ledger path.
4. Capture cash/online payment and link the visit.
5. Create next-due reminders with type and date.
6. Commit locally and enqueue a transaction group.
7. Edit an existing vaccination through a diff, or delete with a safe reversal.
8. Read back the server-assigned receipt number after sync.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Patient and batch data load; no stale price silently applied. |
| Ready | Line items, batch selector, totals, due-date section. |
| Saving | Single submit; local transaction progress. |
| Pending sync | Visit visible; badge shows local-only status. |
| Conflict | Stock or receipt conflict; show exact item and resolution. |
| Error | Rollback; preserve form values for correction. |
| Offline | Allowed; receipt marked provisional until server assignment. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `VAC-001` | A vaccination visit commits locally as one atomic transaction with its stock, reminders, payment, and outbox rows. | P0 |
| `VAC-002` | Stock is deducted exactly once per item through a single ledger path and never goes negative. | P0 |
| `VAC-003` | Retries and duplicate submits do not create a second visit, item, stock movement, reminder, or payment. | P0 |
| `VAC-004` | Batch selection and validation reject expired or insufficient batches before commit. | P0 |
| `VAC-005` | Editing uses a diff and reverses/rededucts stock exactly once. | P0 |
| `VAC-006` | Deleting/correcting a vaccination is audited and does not orphan payment or reminders. | P1 |
| `VAC-007` | Receipt numbers are server-assigned and never computed by the desktop. | P0 |

## 7. Validation and business rules

### Validation

- Patient and date required.
- At least one vaccine item.
- Quantity > 0 and <= batch available.
- Batch not expired at visit date.
- Amounts non-negative; cash + online equals total.
- Due date valid and type from allowed list.
- No duplicate item identity within the visit.

### Business rules

- One logical visit groups all writes.
- Stock ledger is authoritative; do not update batch quantity independently.
- FEFO is preferred but manual batch selection must be explicit.
- Reminder dates use IST.
- Receipt number is immutable and server-assigned.
- A failed reminder/payment step rolls back the local transaction, or the group is marked repairable; never report success.

## 8. Permissions

- Admin/doctor/nurse may record (proposed).
- Inventory manager may view stock but not record vaccination unless approved.
- Deletion/correction requires admin/doctor confirmation.

## 9. Offline and data behavior

- Fully local commit.
- Transaction group uploads in dependency order.
- Final receipt number waits for server; print is provisional until assigned.
- Conflicts are visible and block blind retry.

## 10. Errors and recovery

- Insufficient stock -> no commit.
- Expired batch -> no commit.
- Duplicate submit -> same visit ID, not a new one.
- Payment mismatch -> field error.
- Receipt conflict -> hard error, no renumber.
- Partial group failure -> repairable state.

## 11. Edge cases

- Batch expires between selection and submit.
- Two devices consume the last dose.
- Edit after receipt issued.
- Delete after payment.
- Multiple vaccines in one visit.
- Zero-price/free dose.
- Timezone boundary.

## 12. Acceptance criteria

- [ ] Offline vaccination commits and syncs once.
- [ ] Replay creates one visit and one stock movement.
- [ ] Insufficient stock rolls back all rows.
- [ ] Edit corrects stock exactly once.
- [ ] Receipt is server-assigned and unchanged on retry.
- [ ] Due reminder appears with the correct IST date.

## 13. Test notes

- Integration: atomic create, rollback, edit diff, delete reversal.
- Chaos: duplicate/late response/partial group.
- Unit: FEFO, expiry, money, due date.
- E2E: offline create and reconnect.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

## 14. Dependencies

- [[Features/04-Patient-Management|Patients]]
- [[Features/07-Vaccine-and-Batch-Inventory|Inventory]]
- [[Features/10-Vaccination-Reminders|Reminders]]
- [[Features/12-Finance-and-Payments|Finance]]
- [[Features/13-Receipts-and-Printing|Receipts]]

## 15. Open questions

- Is FEFO mandatory or a default?
- Are corrections edits or linked reversal events?
- Can one visit mix vaccination and consultation?
- Who may delete after a receipt?

## 16. Related

- [[Architecture/Offline-and-Sync-Design|Offline and Sync]]
- [[Audits/Risk-Register|Risk Register]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
