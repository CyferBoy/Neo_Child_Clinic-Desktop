---
title: Settings
feature_id: SET
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base
updated: 2026-10-20
---

# 20. Settings

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/settings/`, `SettingsScreen.kt`, `NotificationSettingsViewModel.kt`.

**Requirement IDs:** `SET-001`, `SET-002`, `SET-003`, `SET-004`, `SET-005`

## 1. Purpose and scope

Manage device preferences and approved clinic settings without mixing secrets, PHI, or unauthorized policy changes.

## 2. Actors

- All staff
- Admin (clinic settings)

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Change theme/appearance.
2. Configure notification preferences.
3. Configure inventory thresholds.
4. Configure security/idle behavior.
5. Configure backup/update preferences.
6. View about/legal/support.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Settings skeleton. |
| Ready | Grouped sections with current values. |
| Saving | Inline confirmation. |
| Invalid | Field error; previous value retained. |
| Permission denied | Admin-only section hidden/blocked. |
| Corrupt | Reset safe defaults with warning. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `SET-001` | Device preferences are separated from clinic-wide/admin settings. | P0 |
| `SET-002` | Settings are validated, versioned, and recover from invalid/corrupt values. | P1 |
| `SET-003` | Admin-only settings are enforced server-side and audited. | P0 |
| `SET-004` | No secret/token is stored in a settings file or renderer storage. | P0 |
| `SET-005` | Settings that affect safety (idle lock, backup, thresholds) have safe defaults. | P1 |

## 7. Validation and business rules

### Validation

- Ranges for thresholds/idle days.
- Enum values for theme/notification mode.
- Admin role for clinic settings.
- Backup/update paths valid.

### Business rules

- Device preference vs clinic policy is explicit.
- Safety settings cannot be silently disabled.
- No secrets in settings.
- Admin changes audited.

## 8. Permissions

- All users: personal preferences.
- Admin: clinic policy, backup, update, security defaults.

## 9. Offline and data behavior

- Local preferences work offline.
- Clinic-wide changes require connectivity/authorization.

## 10. Errors and recovery

- Invalid value -> field error.
- Corrupt store -> safe defaults.
- Unauthorized -> 403.
- Save failure -> retain previous.

## 11. Edge cases

- Role downgrade.
- Multiple OS users.
- Portable mode.
- Invalid threshold.
- Update channel change.

## 12. Acceptance criteria

- [ ] Settings persist across restart.
- [ ] Invalid values rejected.
- [ ] Non-admin cannot change clinic policy.
- [ ] No token in settings.
- [ ] Safe defaults after corruption.

## 13. Test notes

- Component: forms/validation.
- Integration: persistence/role.
- Security: storage inspection.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

## 14. Dependencies

- [[Features/01-Desktop-Shell-and-Navigation|Shell]]
- [[Features/02-Authentication-and-Session|Auth]]

## 15. Open questions

- Which settings are clinic-wide?
- Who approves default changes?
- Are multiple profiles/roles per workstation supported?

## 16. Related

- [[Features/19-Desktop-Notifications|Notifications]]
- [[Features/18-Backup-and-Recovery|Backup]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
