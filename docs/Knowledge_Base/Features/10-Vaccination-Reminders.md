---
title: Vaccination Reminders
feature_id: REM
doc_status: proposed
desktop_status: Missing
android_status: Partially implemented
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 10. Vaccination Reminders

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Partially implemented. Evidence: `feature/reminder/`, Android KB `Due Vaccination`. Historical timezone and notification defects are fixed; no deletion/absence reconciliation contract exists (NCC-023).

**Requirement IDs:** `REM-001`, `REM-002`, `REM-003`, `REM-004`, `REM-005`, `REM-006`

## 1. Purpose and scope

Create, schedule, view, complete, dismiss, and reschedule due vaccination reminders with IST date semantics and reliable notifications.

### User stories

- As a receptionist, I can see due and overdue vaccination reminders for today in IST.
- As a nurse, I can complete, dismiss, or reschedule a reminder with an audit trail.
- As a doctor, I can review the reminder history without a stale sync reopening a completed reminder.

## 2. Actors

- Admin
- Doctor
- Nurse
- Receptionist

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Create reminders from a vaccination's next-due section.
2. View due today, overdue, completed, and dismissed.
3. Mark a reminder complete with performed date/by.
4. Dismiss with reason.
5. Reschedule while preserving history.
6. Notify staff and open the patient context.
7. Reconcile deletions from other devices once an approved deletion/absence contract exists; no server tombstone feed is present in repository evidence; live status is unverified.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Due list skeleton. |
| Empty | No reminders for the selected date. |
| Ready | Grouped due/overdue/completed tabs. |
| Saving | Status transition pending. |
| Conflict | Stale status; reload/compare. |
| Offline | Local list available; notifications local. |
| Permission denied | No reminder administration. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `REM-001` | Reminder due dates use IST and are independent of the device timezone. | P0 |
| `REM-002` | Status transitions are explicit and audited: active, completed, dismissed. | P0 |
| `REM-003` | A deleted or completed reminder cannot reappear from a stale pull. | P0 |
| `REM-004` | Rescheduling preserves the prior due date/reason in history. | P1 |
| `REM-005` | Notifications are deduplicated and respect user preferences. | P1 |
| `REM-006` | Due lists exclude soft-deleted patients and reminders. | P0 |

## 7. Validation and business rules

### Validation

- Patient, vaccine label, due date, and type required for a new reminder.
- Due date valid.
- Completion date valid.
- Dismissal reason required.

### Business rules

- Reporting/due boundaries use IST, not the OS timezone.
- Terminal states win over stale active updates.
- One active reminder per clinical due item unless duplicates are explicitly allowed.
- Vaccination edits reconcile reminders.
- No blank-date reminders.

## 8. Permissions

- Clinical roles can view/complete/dismiss according to policy.
- Admin can reschedule/override with audit.

## 9. Offline and data behavior

- Local due list and status transitions.
- Outbox sync.
- Notification scheduling local but must use IST.

## 10. Errors and recovery

- Blank/invalid date -> block.
- Stale status -> conflict, not overwrite.
- Notification permission denied -> visible preference state.
- Deletion contract absent -> a hard-deleted row can resurrect; resolve an approved deletion/absence contract before sync.

## 11. Edge cases

- Device in another timezone.
- DST-free IST assumption.
- Reminder due at midnight.
- Patient archived.
- Vaccination deleted.
- Duplicate reminders.

## 12. Acceptance criteria

- [ ] Due today is correct in IST on a non-IST device.
- [ ] Complete/dismiss is terminal across sync.
- [ ] Deleted reminder stays deleted.
- [ ] No duplicate notification for the same due item/day.
- [ ] Reschedule keeps history.

## 13. Test notes

- Clock/timezone unit tests.
- Integration: status transitions and deletion reconciliation (requires an approved contract).
- E2E: due list and notification.
- Chaos: stale pull.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-REM-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/05-Vaccination-Management|Vaccination]]
- [[Features/19-Desktop-Notifications|Notifications]]
- [[Features/17-Supabase-Sync|Sync]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

`reminders`; `patients`; `patient_visits`; `vaccination_items`; `audit_logs`.

## 15. Open questions

- What statuses are legally/operationally required?
- Can a reminder be rescheduled more than once?
- Which roles can dismiss?
- Are SMS/WhatsApp reminders in scope?

## 16. Related

- [[Features/11-Personal-Reminders|Personal Reminders]]
- [[Features/14-Dashboard|Dashboard]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
