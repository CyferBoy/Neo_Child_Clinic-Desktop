---
title: Personal Reminders
feature_id: PER
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 11. Personal Reminders

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/personalreminder/`, `domain/model/PersonalReminder.kt`. NCC-034 was reclassified as not a bug; no open module-specific defect is recorded.

**Requirement IDs:** `PER-001`, `PER-002`, `PER-003`, `PER-004`, `PER-005`

## 1. Purpose and scope

Track non-clinical personal follow-ups (for example a staff reminder to call a patient), with patient link, vaccine interest, advance amount, date, and status.

### User stories

- As a receptionist, I can set a non-clinical callback reminder for a patient.
- As a staff member, I can complete or cancel it without changing a clinical due date.

## 2. Actors

- Admin
- Doctor
- Receptionist
- Nurse

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Create a personal reminder with patient name/phone or linked patient.
2. Record vaccine interest, note, advance amount/date.
3. Set a reminder date and status.
4. View pending/completed/cancelled.
5. Complete or cancel with audit.
6. Notify the responsible staff member.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Reminder list. |
| Empty | No personal reminders. |
| Ready | Pending/completed/cancelled list. |
| Saving | Status/form pending. |
| Conflict | Stale status or patient link. |
| Offline | Local create/status. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `PER-001` | A personal reminder has a valid date or is explicitly saved as undated with no notification. | P0 |
| `PER-002` | Patient link is optional but, when present, uses a stable patient ID. | P0 |
| `PER-003` | Status transitions are explicit and auditable. | P1 |
| `PER-004` | Advance amounts are not treated as clinic income unless linked to an approved payment record. | P0 |
| `PER-005` | Deleted/cancelled reminders do not notify or reappear from stale sync. | P0 |

## 7. Validation and business rules

### Validation

- Patient name and phone required if not linked to a patient.
- Date optional only with an explicit undated state.
- Advance amount >= 0.
- Status from allowed values.

### Business rules

- Personal reminders are separate from clinical vaccination due reminders.
- Blank date must never notify repeatedly.
- Advance amount is informational unless a finance transaction is explicitly linked.
- Cancellation/completion is terminal and audited.

## 8. Permissions

- Clinical/reception roles can create; admin can override.
- Finance role required to post an advance as income.

## 9. Offline and data behavior

- Local create/status and outbox.
- No network needed for notification scheduling.

## 10. Errors and recovery

- Blank date with notification enabled -> block or force undated.
- Duplicate submit -> idempotent.
- Stale status -> conflict.
- Invalid amount -> field error.

## 11. Edge cases

- Walk-in patient with no record.
- Patient linked later.
- Advance refund.
- Past date.
- Cancelled reminder notification.
- Phone duplicate.

## 12. Acceptance criteria

- [ ] Blank date never causes repeated notifications.
- [ ] Status changes are terminal.
- [ ] Advance is not double-counted as income.
- [ ] Offline reminder syncs once.

## 13. Test notes

- Unit: date/status/amount.
- Integration: notification scheduling, outbox.
- E2E: create/complete/cancel.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-PER-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/10-Vaccination-Reminders|Vaccination Reminders]]
- [[Features/12-Finance-and-Payments|Finance]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

`personal_vaccine_reminders`; `patients`; `vaccines`; `audit_logs`.

## 15. Open questions

- Is advance payment a real financial transaction?
- Who owns follow-up assignment?
- Are SMS/WhatsApp messages in scope?
- Can reminders be undated?

## 16. Related

- [[Features/19-Desktop-Notifications|Notifications]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
