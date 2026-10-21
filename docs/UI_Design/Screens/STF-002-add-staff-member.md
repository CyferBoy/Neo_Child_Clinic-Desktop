# STF-002 · Add staff member

> **Design specification 53 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `STF-002` |
| Section | Administration |
| Feature | Staff and Role Management |
| Source specification | `03-Staff-and-Role-Management.md` |
| Prototype | [STF-002.html](../prototype/screens/STF-002.html) |
| Rendered reference | [STF-002.png](../screenshots/STF-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Create an Auth user and clinic profile with a role, temporary password and optional employee data.

## Users

Admin only

## Permissions

Admin only; online only; backend service-role handled by the Edge Function.

## Entry points

Staff list Add staff member.

## Navigation

Create → staff list. Cancel → staff list. Auth/profile failure must roll back.

## Layout regions

- Staff list context behind scrim
- Wide right drawer
- Account fields
- Password fields
- Role summary
- Create action

## Components

- Drawer
- Text/email/password fields
- Role select
- Role capability summary
- Warnings

## Data shown

- Fictional placeholder identity
- Role choices: Admin, Doctor, Nurse, Receptionist, Inventory manager

## Actions

- Create staff account
- Cancel

## Forms and fields

- Full name (required)
- Work email (required, unique)
- Role (required, allowed values)
- Temporary password ≥12 chars (required)
- Confirm password
- Employee ID
- Phone
- Admin note

## States

- Ready
- Saving
- Validation
- Duplicate email
- Offline disabled
- Partial backend failure/rollback
- Permission denied

## Offline and data behavior

Disabled. Account creation cannot be queued offline.

## Keyboard

Focus enters drawer; password visibility control keyboard accessible; Escape cancels if no unsaved changes.

## Accessibility

Labelled fields; password guidance text; errors linked; role descriptions readable.

## Dependencies

STF-001/003; manage-staff; Auth; audit.

## Open questions / not approved

Password delivery method, email verification, employee-ID uniqueness and rollback observability.

## Design notes and evidence boundary

The temporary password is never logged or stored in plaintext. This preview displays no real credential.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
