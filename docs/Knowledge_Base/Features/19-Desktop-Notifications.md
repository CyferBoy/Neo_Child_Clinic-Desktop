---
title: Desktop Notifications
feature_id: NOT
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base
updated: 2026-10-20
---

# 19. Desktop Notifications

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `core/notification/`, `feature/reminder/`, Android KB `Due Vaccination`. Historical notification-ID/statistics defects are fixed; no open module-specific defect is recorded.

**Requirement IDs:** `NOT-001`, `NOT-002`, `NOT-003`, `NOT-004`, `NOT-005`

## 1. Purpose and scope

Notify staff about due vaccinations and personal reminders without leaking PHI, spamming duplicates, or using the wrong timezone.

## 2. Actors

- All staff
- Admin (policy)

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Request OS notification permission.
2. Schedule/trigger a due reminder in IST.
3. Show a privacy-safe notification.
4. Click to open the correct patient/reminder.
5. Respect quiet hours/preferences.
6. Deduplicate per reminder/day.

## 5. UI states

| State | Expected behavior |
|---|---|
| Permission needed | Explain and request. |
| Denied | Settings guidance; in-app due list still works. |
| Scheduled | Next notification summary. |
| Delivered | Safe preview. |
| Quiet hours | Suppressed; visible in in-app list. |
| Error | Scheduling failure visible. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `NOT-001` | Notification scheduling and due boundaries use IST, not the device timezone. | P0 |
| `NOT-002` | Notifications do not expose patient names/PHI in the OS preview by default. | P0 |
| `NOT-003` | Duplicate notifications for the same reminder/day are suppressed. | P1 |
| `NOT-004` | Notification permission/preferences are visible and respected. | P1 |
| `NOT-005` | Click-through opens an authorized record or a safe fallback. | P1 |

## 7. Validation and business rules

### Validation

- Reminder date valid.
- Preference values valid.
- Permission state known.

### Business rules

- No PHI in previews by default.
- IST boundaries.
- No duplicate per day.
- A deleted/completed reminder does not notify.
- Click-through re-checks authorization.

## 8. Permissions

- Users control their own notification preferences.
- Admin may set clinic defaults.

## 9. Offline and data behavior

- Local scheduling works without network.
- Due list remains the source of truth.

## 10. Errors and recovery

- Permission denied -> no silent failure.
- OS scheduler unavailable -> in-app warning.
- Stale reminder -> skip.
- Clock change -> recompute.

## 11. Edge cases

- App closed.
- OS DND.
- Multiple staff on one workstation.
- Midnight IST.
- Reminder completed just before trigger.
- Notification clicked after logout.

## 12. Acceptance criteria

- [ ] No patient name in OS preview.
- [ ] Due notification correct in IST.
- [ ] No duplicate per day.
- [ ] Click opens correct record or safe login.
- [ ] Permission denial is visible.

## 13. Test notes

- Unit: scheduling/dedupe/timezone.
- Integration: permission/click-through.
- Manual: OS notification behavior.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

## 14. Dependencies

- [[Features/10-Vaccination-Reminders|Reminders]]
- [[Features/11-Personal-Reminders|Personal Reminders]]

## 15. Open questions

- Which OS notification APIs?
- Is quiet hours required?
- Should notifications be per-user or per-workstation?

## 16. Related

- [[Security/Privacy-and-Backup|Privacy]]
- [[Features/20-Settings|Settings]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
