# STF-001 · Staff list

> **Design specification 52 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `STF-001` |
| Section | Administration |
| Feature | Staff and Role Management |
| Source specification | `03-Staff-and-Role-Management.md` |
| Prototype | [STF-001.html](../prototype/screens/STF-001.html) |
| Rendered reference | [STF-001.png](../screenshots/STF-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

List clinic staff, roles, status and sessions; provide admin-only entry points for account lifecycle actions.

## Users

Admin only

## Permissions

Admin-only. Non-admin direct backend calls must return 401/403 without staff data.

## Entry points

Sidebar Staff, visible only to admins.

## Navigation

Add staff; reset password; deactivate; edit role/profile (proposed).

## Layout regions

- Page header
- Admin boundary alert
- Status tabs
- Search/filter toolbar
- Staff table
- Self-protection note

## Components

- Tabs
- Table
- Role/status badges
- Row actions
- Search

## Data shown

- 12 fictional staff
- 5 roles
- 1 deactivated account
- Current and last-active sessions

## Actions

- Add staff member
- Export staff list
- Row actions
- Filter

## Forms and fields

- Search
- Role filter

## States

- Loading
- Empty
- Ready
- Permission denied
- Offline read-only
- Conflict/stale

## Offline and data behavior

Cached list may be read-only. Account administration is disabled offline and must not be queued for replay.

## Keyboard

/ search; row menus labelled with name; tabs arrow-key semantics.

## Accessibility

Role/status text; self badge; table headers; no color-only meaning.

## Dependencies

STF-001–006; AUTH; manage-staff Edge Function; audit.

## Open questions / not approved

Last-admin protection server-side? Email verification? Who can reset passwords? Role changes forcing sign-out?

## Design notes and evidence boundary

No passwords are displayed. Shared accounts are prohibited.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
