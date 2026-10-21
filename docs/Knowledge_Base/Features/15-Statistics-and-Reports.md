---
title: Statistics and Reports
feature_id: RPT
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 15. Statistics and Reports

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/statistics/`, Android KB `Statistics Dashboard`. Historical double-count, filter, and brand-drill-down defects are fixed; runtime verification is still absent.

**Requirement IDs:** `RPT-001`, `RPT-002`, `RPT-003`, `RPT-004`, `RPT-005`, `RPT-006`, `RPT-007`

## 1. Purpose and scope

Produce trustworthy operational and financial reports with explicit date windows, IST semantics, soft-delete filtering, and single-count income rules.

### User stories

- As an admin, I can run a date-bounded financial report that counts each visit once.
- As a doctor, I can review vaccination and patient trends with deleted records excluded.

## 2. Actors

- Admin
- Doctor

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Open overview for a day/month/range.
2. Inspect finance details, vaccine details, milestone patients, full report.
3. Filter by date/category/vaccine.
4. Export/print an approved report.
5. Drill from aggregate to source records.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Report skeleton. |
| Empty | No data for range; explain. |
| Ready | Charts/tables with drill links. |
| Stale | Banner: local/unsynced data may change. |
| Error | Partial report error; do not show zero silently. |
| Permission denied | No report access. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `RPT-001` | Reports use IST date windows and typed dates, not formatted-string sorting. | P0 |
| `RPT-002` | Soft-deleted records are excluded consistently. | P0 |
| `RPT-003` | A visit's income is counted once, with cash/online/mixed reconciliation. | P0 |
| `RPT-004` | Every aggregate drills to the same source records. | P0 |
| `RPT-005` | Vaccine/brand grouping uses stable catalog identity, not display-name equality. | P1 |
| `RPT-006` | Reports label stale/unsynced data and never present partial data as complete. | P1 |
| `RPT-007` | Export/print is explicit and follows the privacy policy. | P1 |

## 7. Validation and business rules

### Validation

- Start <= end.
- Date range within allowed bounds.
- Currency/date formats valid.
- Filters from allowlists.

### Business rules

- Income counted once per visit identity.
- Expenses are separate from income.
- Deleted records excluded.
- Vaccine grouping by catalog ID.
- No report total without a matching detail query.
- The same date belongs to one IST day.

## 8. Permissions

- Admin/doctor only (proposed, matching Android stats gate).
- Export may be admin-only.

## 9. Offline and data behavior

- Local aggregates; label unsynced/stale.
- Do not claim a complete month while writes are pending.

## 10. Errors and recovery

- Partial query failure -> error, not zero.
- Invalid range -> field error.
- Export failure -> no partial file.
- Detail mismatch -> investigate, do not hide.

## 11. Edge cases

- Month boundary.
- Leap year.
- Deleted payment.
- Refund/negative adjustment.
- Zero-amount visit.
- Duplicate vaccine names.
- Unsynced vaccinations.

## 12. Acceptance criteria

- [ ] Golden dataset totals match hand calculation.
- [ ] Deleted records excluded.
- [ ] Income counted once.
- [ ] Drill-down matches aggregate.
- [ ] IST month boundary correct.
- [ ] Export matches screen.

## 13. Test notes

- Golden dataset unit/integration.
- Property tests for totals.
- Clock/timezone.
- E2E drill-down.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-RPT-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/12-Finance-and-Payments|Finance]]
- [[Features/05-Vaccination-Management|Vaccination]]
- [[Features/07-Vaccine-and-Batch-Inventory|Inventory]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

Read-only projections over `finance_transactions`; `expenses`; `patient_visits`; `vaccination_items`; `vaccines`; `patients`; `waste_records`.

## 15. Open questions

- What are the official report definitions?
- Are refunds/discounts reportable?
- Which formats/exports are required?
- Who can export PHI?

## 16. Related

- [[Features/14-Dashboard|Dashboard]]
- [[Audits/Risk-Register|Risk Register]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
