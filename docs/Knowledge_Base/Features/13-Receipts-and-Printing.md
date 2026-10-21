---
title: Receipts and Printing
feature_id: RCP
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 13. Receipts and Printing

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/patient/presentation/Receipt*`, `supabase/migrations/20260824_receipt_numbering.sql`.

**Requirement IDs:** `RCP-001`, `RCP-002`, `RCP-003`, `RCP-004`, `RCP-005`

## 1. Purpose and scope

Assign an immutable server-side receipt number, render a clear receipt, and print/reprint safely without exposing PHI or duplicating numbers.

### User stories

- As a receptionist, I can issue and reprint a receipt with the server-assigned number.
- As an admin, I can audit receipt use without exposing patient details in logs.

## 2. Actors

- Admin
- Doctor
- Receptionist

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Complete a visit/payment.
2. Request the server-assigned receipt number.
3. Preview the receipt with patient, visit, vaccines/services, amounts, and balance.
4. Print or save a copy.
5. Reprint with a duplicate marker/audit.
6. Handle printer/network failure without losing the payment.

## 5. UI states

| State | Expected behavior |
|---|---|
| Waiting for number | Provisional receipt; no final print. |
| Ready | Preview with final number. |
| Printing | Progress; cancel/failure handled. |
| Printed | Success + reprint action. |
| Printer error | Payment remains; retry/choose printer. |
| Offline | Provisional only; final print blocked. |
| Permission denied | No receipt access. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `RCP-001` | Receipt numbers are assigned by PostgreSQL and are immutable. | P0 |
| `RCP-002` | The receipt is linked to the correct visit/payment and reflects the final amounts. | P0 |
| `RCP-003` | Printing is explicit, previewable, and does not alter the payment. | P0 |
| `RCP-004` | Reprints are marked/audited and use the original number. | P1 |
| `RCP-005` | An offline receipt is clearly provisional and never presents a local number as final. | P0 |

## 7. Validation and business rules

### Validation

- Visit/payment must exist.
- Receipt number must be server-issued and match the visit.
- Amounts must reconcile.
- Template fields required.

### Business rules

- Never compute a receipt number locally.
- Financial year derives from the visit date, not print time.
- No reuse of a number after delete/edit.
- A reprint never changes the number.
- Do not print more PHI than necessary; preview before print.

## 8. Permissions

- Admin/doctor/receptionist can print (proposed).
- Reprint/void requires audit and role policy.

## 9. Offline and data behavior

- Payment can be recorded offline; final receipt waits for server assignment.
- Provisional receipt must be labeled.
- Queue print until final number exists.

## 10. Errors and recovery

- Server unavailable -> provisional, no final print.
- Printer failure -> retain job/payment; retry.
- Number collision -> hard error, no renumber.
- Visit edited after receipt -> correction/void flow.

## 11. Edge cases

- Reprint after printer jam.
- Refund after receipt.
- Multiple services in one visit.
- Financial-year boundary.
- Wrong printer.
- Spool retention.

## 12. Acceptance criteria

- [ ] Receipt number matches server sequence.
- [ ] Offline print is marked provisional.
- [ ] Reprint uses same number.
- [ ] Printer failure does not lose payment.
- [ ] No duplicate number under concurrent visits.

## 13. Test notes

- Integration: receipt sequence/concurrency.
- E2E: preview/print/failure/reprint.
- Manual: printer/paper/accessibility.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-RCP-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/12-Finance-and-Payments|Finance]]
- [[Features/05-Vaccination-Management|Vaccination]]
- [[Features/17-Supabase-Sync|Sync]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

`patient_visits`; `finance_transactions`; `consultations`; `receipt_sequences` (server-only); `audit_logs`.

## 15. Open questions

- Is an offline final receipt legally allowed?
- What template/legal text is required?
- Who can void/reprint?
- Is PDF export required?

## 16. Related

- [[Features/06-Consultation-Management|Consultation]]
- [[Security/Privacy-and-Backup|Privacy]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
