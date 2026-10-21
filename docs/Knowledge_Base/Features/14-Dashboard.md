---
title: Dashboard
feature_id: DSH
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 14. Dashboard

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/dashboard/`, `DashboardViewModel.kt`, `TodayPatients*`.

**Requirement IDs:** `DSH-001`, `DSH-002`, `DSH-003`, `DSH-004`, `DSH-005`

## 1. Purpose and scope

Give staff a same-day operational view: today's patients, due/overdue reminders, low stock, quick actions, and role-appropriate alerts.

### User stories

- As a receptionist, I can see today's patients, due reminders, low stock, and pending sync at a glance.
- As a doctor, I can open a card and see the same definition and filters used for its count.

## 2. Actors

- All staff

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Open the dashboard after sign-in.
2. See today's patient/visit counts and quick actions.
3. See due/overdue reminders and low-stock alerts.
4. Navigate to patient, due list, inventory, or reports.
5. Refresh/observe sync status.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Counts skeleton. |
| Empty | No visits/reminders today; clear next action. |
| Ready | Cards + today list + alerts. |
| Offline | Cached counts; stale label if needed. |
| Sync attention | Badge/link. |
| Permission denied | Role-appropriate cards only. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `DSH-001` | Dashboard counts use IST date boundaries and exclude soft-deleted records. | P0 |
| `DSH-002` | Quick actions respect role permissions and never expose PHI in previews. | P0 |
| `DSH-003` | Dashboard reads work offline from local data and label stale state. | P1 |
| `DSH-004` | Counts reconcile to their detail screens. | P0 |
| `DSH-005` | Sync/offline status is visible from the dashboard. | P1 |

## 7. Validation and business rules

### Validation

- Date is a valid IST business date.
- Counts are non-negative.
- Detail links use opaque IDs.

### Business rules

- Today is the clinic's IST day, not the OS day.
- Counts exclude deleted rows and unpaid/cancelled states per report definition.
- Cards and details must use the same definitions.
- No PHI in notification/widget previews.

## 8. Permissions

- All roles see a dashboard; cards vary by role.
- Reports/finance cards restricted.

## 9. Offline and data behavior

- Local aggregate queries.
- Label stale/unsynced contributions.
- Do not block on network refresh.

## 10. Errors and recovery

- Aggregate query failure -> card error, not blank zero.
- Stale data -> label.
- Detail link to deleted row -> safe empty state.

## 11. Edge cases

- Midnight IST.
- No visits.
- Large day.
- Unsynced vaccination not yet counted remotely.
- Role change.

## 12. Acceptance criteria

- [ ] Counts match detail lists.
- [ ] IST boundary correct.
- [ ] Deleted records excluded.
- [ ] Offline dashboard loads.
- [ ] No PHI in previews.

## 13. Test notes

- Golden aggregate data.
- Clock/timezone.
- Component/E2E cards.
- Offline.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-DSH-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/10-Vaccination-Reminders|Reminders]]
- [[Features/15-Statistics-and-Reports|Reports]]
- [[Features/07-Vaccine-and-Batch-Inventory|Inventory]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

Read-only projections over `patients`; `patient_visits`; `reminders`; `vaccine_batches`; `finance_transactions`; `consultation_todos`; `vaccination_todos`.

## 15. Open questions

- Which cards are required in Phase 1?
- Refresh cadence?
- Should each role have a different landing dashboard?

## 16. Related

- [[Features/01-Desktop-Shell-and-Navigation|Shell]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
