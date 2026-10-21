---
title: Patient Management
feature_id: PAT
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 04. Patient Management

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/patient/`, Android KB `Patient Management`. Historical validation defects are fixed; the former stale-history cache claim is not supported by current `PatientCache` source.

**Requirement IDs:** `PAT-001`, `PAT-002`, `PAT-003`, `PAT-004`, `PAT-005`, `PAT-006`, `PAT-007`

## 1. Purpose and scope

Register, find, edit, merge, and archive patients; maintain a complete clinical timeline keyed by a stable UUID and a human-facing clinic ID.

### User stories

- As a receptionist, I can register a patient offline and find them by name, clinic ID, or phone.
- As a doctor, I can review a patient timeline of visits, vaccinations, consultations, payments, and notes.
- As an admin, I can merge duplicate patient records without losing clinical or financial history.

## 2. Actors

- Admin
- Doctor
- Receptionist
- Nurse

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Register a patient with demographics and contact details.
2. Search by name, clinic ID, or phone; warn on likely duplicates.
3. Open a patient timeline with visits, vaccinations, consultations, payments, notes, documents, and audit.
4. Edit demographics with audit.
5. Merge duplicate patients while preserving history.
6. Archive/soft-delete a patient with reason.
7. Add notes, todos, and documents within approved scope.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Patient list/detail skeleton. |
| Empty | No patients or no search results; clear next action. |
| Ready | List/detail with timeline and role actions. |
| Saving | Disable duplicate submit; show local commit. |
| Conflict | Duplicate clinic ID or merge conflict; compare and resolve. |
| Offline | Local search/read/write available; pending badge. |
| Archived | Read-only with restore policy if approved. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `PAT-001` | Every patient has a stable UUID and a unique human-facing clinic ID. | P0 |
| `PAT-002` | Registration and edits are offline-capable and idempotent. | P0 |
| `PAT-003` | Search returns bounded results by name, clinic ID, and phone without loading all patients. | P0 |
| `PAT-004` | The patient timeline reflects all dependent clinical and financial changes immediately. | P0 |
| `PAT-005` | Merge preserves the surviving identity, history, payments, and audit without duplication. | P0 |
| `PAT-006` | Archive is soft-delete, audited, and excluded from active lists and reports. | P1 |
| `PAT-007` | Duplicate warnings are shown before creating a likely duplicate. | P1 |

## 7. Validation and business rules

### Validation

- Name required.
- Phone required and normalized.
- DOB valid and not in the future.
- Gender from allowed values.
- Clinic ID unique.
- Address optional but length-bounded.

### Business rules

- UUID is the database identity; clinic ID is the human key.
- Do not hard-delete a patient with clinical/financial history.
- Merge must reassign dependent rows and preserve audit.
- Timeline cache invalidates on vaccination/consultation/payment changes, not only patient edits.
- Phone/name duplicates produce a warning, not a silent merge.

## 8. Permissions

- Read: all clinical roles.
- Create: admin, doctor, receptionist, nurse (proposed).
- Edit: admin, doctor, receptionist (proposed).
- Merge/archive: admin/doctor with confirmation.

## 9. Offline and data behavior

- Create/edit/search read from the local DB.
- Outbox identity is the patient UUID; retries do not duplicate.
- Merge/archive are queued only if the conflict policy supports them; otherwise require connectivity.

## 10. Errors and recovery

- Duplicate clinic ID -> conflict with comparison.
- Validation -> field error, no silent discard.
- Merge failure -> rollback, keep both patients.
- Stale timeline -> invalidate/refetch.

## 11. Edge cases

- Same name and phone.
- Missing DOB.
- Patient created on another device.
- Merge with vaccinations/payments/reminders.
- Archived patient in an old appointment.
- Very large timeline.

## 12. Acceptance criteria

- [ ] Offline registration survives restart and syncs once.
- [ ] Duplicate clinic ID is rejected clearly.
- [ ] Timeline shows a new vaccination immediately.
- [ ] Merge moves all history and leaves one active patient.
- [ ] Archived patient disappears from active search/reports.
- [ ] A blank name never fails silently.

## 13. Test notes

- Unit: validation, merge rules, clinic ID.
- Integration: local transaction/outbox, timeline invalidation.
- E2E: register/search/edit/merge/archive offline.
- Security: role access.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-PAT-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/16-Local-Persistence-and-Offline-Operation|Local Persistence]]
- [[Features/17-Supabase-Sync|Sync]]
- [[Features/21-Audit-Logging|Audit]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

`patients`; `patient_visits`; `patient_notes`; `consultations`; `vaccination_items`; `finance_transactions`; `reminders`; `audit_logs`.

## 15. Open questions

- Which roles may create/edit patients?
- Is merge reversible?
- Are documents in Phase 1, and where are they stored?
- What is the clinic ID format and who can change it?

## 16. Related

- [[Product/Android-Desktop-Parity|Parity]]
- [[Features/05-Vaccination-Management|Vaccination]]
- [[Features/15-Statistics-and-Reports|Reports]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
