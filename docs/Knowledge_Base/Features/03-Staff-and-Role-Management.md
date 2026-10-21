---
title: Staff and Role Management
feature_id: STF
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 03. Staff and Role Management

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/staff/`, `supabase/functions/manage-staff/index.ts`, `domain/model/Profile.kt`.
>
> **Shared backend:** staff lifecycle must reuse the existing `manage-staff` Edge Function and Auth users under [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]; never ship the service-role key in desktop.

**Requirement IDs:** `STF-001`, `STF-002`, `STF-003`, `STF-004`, `STF-005`, `STF-006`

## 1. Purpose and scope

Allow an admin to create staff accounts, edit profiles, change roles, deactivate/reactivate, and trigger password reset, while preventing self-privilege changes and stale tokens.

### User stories

- As an admin, I can create a staff account and assign a server-controlled role.
- As an admin, I can change or deactivate a staff member without deleting their historical records.
- As an admin, I cannot change my own role or deactivate myself into an unsafe state.

## 2. Actors

- Admin

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. List staff with role and active status.
2. Create an account with name, email, temporary password, role, employee ID, phone.
3. Edit display name, phone, employee ID, or role.
4. Deactivate/reactivate an account.
5. Soft-delete an account and revoke its sessions.
6. Send a password reset email.
7. Prevent an admin from changing or disabling their own account.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Staff skeleton/table. |
| Empty | Explain how to add the first staff member. |
| Ready | Table with role/status and actions. |
| Saving | Disable duplicate submit; show progress. |
| Permission denied | Admin-only explanation; no data leak. |
| Conflict | Duplicate email or stale profile; show resolution. |
| Offline | Account administration disabled; cached read-only list may remain. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `STF-001` | Only an authenticated active admin can create or modify staff accounts. | P0 |
| `STF-002` | Creating staff creates both the Auth user and profile, with rollback on profile failure. | P0 |
| `STF-003` | Role changes update both the profile and app_metadata so the next token reflects authorization. | P0 |
| `STF-004` | Deactivation and soft-delete revoke refresh capability, not just UI access. | P0 |
| `STF-005` | An admin cannot change their own role, deactivate, or delete their own account. | P0 |
| `STF-006` | Temporary passwords meet a minimum length and are never logged or stored in plaintext. | P0 |

## 7. Validation and business rules

### Validation

- Name, email, role required.
- Email format and uniqueness checked server-side.
- Password minimum 12 characters for creation.
- Role must be one of the five known values.
- Phone normalized to E.164 when used.
- Employee ID optional; duplicates handled by policy.

### Business rules

- Authorization role is app_metadata, not user_metadata.
- Self-role change/deactivation/delete is forbidden.
- Deactivation bans refresh for existing sessions.
- Profile and Auth user must not diverge; create failure rolls back the Auth user.
- No shared accounts.
- Last-admin removal needs an explicit guard (open question).

## 8. Permissions

- Admin only.
- Non-admin direct calls return 401/403 without staff data.

## 9. Offline and data behavior

- Create/role/status changes require connectivity.
- Cached staff list may be read-only offline.
- Do not queue account-administration writes for later replay without a dedicated design.

## 10. Errors and recovery

- Duplicate email -> conflict.
- Invalid role -> validation.
- Auth user created but profile failed -> rollback.
- Deactivated target -> clear status.
- Self-guard -> explicit refusal.

## 11. Edge cases

- Last remaining admin.
- Admin edits own profile fields.
- Role downgrade while target is signed in.
- Password reset for inactive user.
- Email case/whitespace.
- Orphaned Auth user.

## 12. Acceptance criteria

- [ ] Admin creates and deactivates staff; target cannot refresh.
- [ ] Non-admin cannot call the function.
- [ ] Self-role change is refused.
- [ ] Role change reflected in the next session.
- [ ] No password appears in logs.

## 13. Test notes

- Backend integration: create/edit/role/status/delete/self-guard.
- Security: non-admin direct call, last-admin.
- E2E: staff table and form.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-STF-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/02-Authentication-and-Session|Authentication]]
- [[Database/Access-Patterns|Access Patterns]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

`profiles`; Supabase Auth users through the server-side `manage-staff` function; `audit_logs`.

## 15. Open questions

- Is last-admin protection implemented server-side?
- Is email verification required?
- Who can reset passwords?
- Should role changes force immediate sign-out?

## 16. Related

- [[Product/Personas-and-Roles|Personas and Roles]]
- [[Security/Security-Model|Security Model]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
