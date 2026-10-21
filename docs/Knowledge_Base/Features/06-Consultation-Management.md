---
title: Consultation Management
feature_id: CON
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 06. Consultation Management

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/consultation/`, `domain/model/Consultation.kt`, `ConsultationRepositoryImpl.kt`.

**Requirement IDs:** `CON-001`, `CON-002`, `CON-003`, `CON-004`, `CON-005`

## 1. Purpose and scope

Record a doctor consultation linked to a visit, including problem, notes, follow-up date, payment split, and audit; support safe edit and deletion.

### User stories

- As a doctor, I can record a consultation and follow-up against the correct visit.
- As an admin, I can correct a consultation without orphaning its payment or receipt.

## 2. Actors

- Admin
- Doctor

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Open a patient and start a consultation.
2. Capture doctor, date, problem, notes, follow-up, payment.
3. Link the consultation to the visit and payment transaction.
4. Edit the consultation and reconcile payment if changed.
5. Delete/cancel with audit and payment handling.
6. Show follow-up on the patient timeline and dashboard.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Patient/visit context. |
| Ready | Clinical form and payment section. |
| Saving | Single submit; local commit. |
| Pending sync | Visible record with badge. |
| Conflict | Payment/consultation mismatch; resolve. |
| Offline | Allowed; local commit. |
| Permission denied | Non-clinical role sees no notes. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `CON-001` | A consultation is linked to a patient, visit, doctor, and date. | P0 |
| `CON-002` | Create/edit/delete are offline-capable and idempotent. | P0 |
| `CON-003` | A changed payment is reconciled to the same consultation identity, not duplicated. | P0 |
| `CON-004` | Deletion/cancellation is audited and does not orphan the visit or payment. | P1 |
| `CON-005` | Follow-up dates use IST and appear on the patient timeline. | P1 |

## 7. Validation and business rules

### Validation

- Patient, doctor, and date required.
- Problem/notes length-bounded.
- Amounts non-negative; cash + online equals total when split.
- Follow-up date valid and not before the consultation date.

### Business rules

- The visit is the financial/clinical header; do not create an orphan consultation.
- Payment edits preserve a stable consultation marker/identity.
- Deletion does not delete unrelated visit payments.
- Clinical notes are never silently overwritten by sync.

## 8. Permissions

- Admin/doctor can create/edit.
- Receptionist may schedule but not write clinical notes.
- Deletion requires confirmation and audit.

## 9. Offline and data behavior

- Local create/edit/delete.
- Outbox group links consultation and payment.
- Conflict on note/payment is visible.

## 10. Errors and recovery

- Missing visit -> block.
- Payment identity ambiguous -> stop and show.
- Follow-up invalid -> field error.
- Sync conflict -> preserve both versions.

## 11. Edge cases

- Multiple consultations for one patient.
- Doctor deactivated.
- Follow-up in the past.
- Delete with a receipt.
- Payment edited on another device.

## 12. Acceptance criteria

- [ ] Offline consultation commits and syncs once.
- [ ] Payment edit does not create a duplicate.
- [ ] Delete leaves the visit and audit intact.
- [ ] Follow-up shows in IST.
- [ ] Non-doctor cannot write clinical notes.

## 13. Test notes

- Integration: create/edit/delete + payment marker.
- Unit: validation/date.
- E2E: consultation and follow-up.
- Security: role access.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-CON-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/04-Patient-Management|Patients]]
- [[Features/12-Finance-and-Payments|Finance]]
- [[Features/13-Receipts-and-Printing|Receipts]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

`consultations`; `patient_visits`; `finance_transactions`; `receipt_sequences` (server-only); `audit_logs`.

## 15. Open questions

- Can receptionists create a consultation shell?
- Are addenda allowed instead of edits?
- Which payment categories apply?
- Is a consultation always one per visit?

## 16. Related

- [[Architecture/Data-Flows|Data Flows]]
- [[Features/15-Statistics-and-Reports|Reports]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
