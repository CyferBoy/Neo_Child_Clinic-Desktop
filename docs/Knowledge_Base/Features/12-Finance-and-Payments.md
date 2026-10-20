---
title: Finance and Payments
feature_id: FIN
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base
updated: 2026-10-20
---

# 12. Finance and Payments

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/finance/`, `FinanceRepositoryImpl.kt`, `ExpenseValidator.kt`, Android KB `Statistics Dashboard`.

**Requirement IDs:** `FIN-001`, `FIN-002`, `FIN-003`, `FIN-004`, `FIN-005`, `FIN-006`

## 1. Purpose and scope

Record visit income with cash/online/mixed splits, expenses, and reconciliation to receipts and reports without double-counting or floating-point errors.

## 2. Actors

- Admin
- Doctor
- Receptionist

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Record payment for a vaccination or consultation.
2. Split cash and online amounts; derive payment method.
3. Edit payment linked to the same visit/consultation identity.
4. Record an expense with date, category, title, amount, method, reference.
5. List/filter/search expenses.
6. Reconcile payment totals to reports and receipts.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Payment/expense list. |
| Empty | No transactions. |
| Ready | List and totals. |
| Saving | Single submit; local commit. |
| Conflict | Duplicate/mismatched payment identity. |
| Offline | Local record; pending badge. |
| Permission denied | No finance access. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `FIN-001` | Money is stored/calculated exactly; the desktop uses integer minor units internally. | P0 |
| `FIN-002` | Every payment is linked to a visit and, where applicable, a consultation identity. | P0 |
| `FIN-003` | A visit has at most one vaccination income row; edits update, not duplicate. | P0 |
| `FIN-004` | Cash/online/mixed totals reconcile to the payment amount. | P0 |
| `FIN-005` | Expenses require date, category, title, amount > 0, and payment method. | P1 |
| `FIN-006` | Payment edits/deletes are audited and do not silently change receipts. | P0 |

## 7. Validation and business rules

### Validation

- Amount > 0 unless explicitly free.
- Cash + online = amount.
- Cash/online non-negative.
- Expense category/title/date/method required.
- Reference optional and length-bounded.

### Business rules

- A visit's vaccination income identity is deterministic.
- Consultation edits preserve the linked payment identity.
- Receipt numbers are immutable and server-assigned.
- Reports count a visit's income once.
- Refunds/corrections need an explicit audited workflow, not a negative edit.

## 8. Permissions

- Admin/doctor/receptionist can record income (proposed).
- Admin/doctor can manage expenses; receptionist may record but not edit (open).
- Reports restricted by role.

## 9. Offline and data behavior

- Local record/edit and outbox.
- Receipt finalization waits for server number.
- Payment conflicts visible.

## 10. Errors and recovery

- Amount mismatch -> field error.
- Duplicate income -> reconcile to same ID.
- Receipt already issued -> correction flow.
- Permission -> 403.
- Server timeout -> pending, not lost.

## 11. Edge cases

- Free dose.
- Mixed payment.
- Refund.
- Partial payment.
- Multiple consultations per visit.
- Expense edited after reporting.
- Currency rounding.

## 12. Acceptance criteria

- [ ] Cash/online/mixed totals match.
- [ ] Replay does not duplicate income.
- [ ] One visit's vaccination income counted once.
- [ ] Receipt number unchanged by edit.
- [ ] Expense validation matches rules.
- [ ] Offline payment syncs once.

## 13. Test notes

- Unit: money/rounding/payment split/expense validation.
- Integration: income identity/edit/replay.
- Golden reports.
- E2E: payment and expense.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

## 14. Dependencies

- [[Features/05-Vaccination-Management|Vaccination]]
- [[Features/06-Consultation-Management|Consultation]]
- [[Features/13-Receipts-and-Printing|Receipts]]
- [[Features/15-Statistics-and-Reports|Reports]]

## 15. Open questions

- Are refunds/discounts in Phase 1?
- Which roles can edit expenses?
- How are payment references stored?
- Should money be migrated to numeric in the shared schema?

## 16. Related

- [[Audits/Risk-Register|Risk Register]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
