# STF-004 · Reset staff password

> **Design specification 55 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `STF-004` |
| Section | Administration |
| Feature | Staff and Role Management |
| Source specification | `03-Staff-and-Role-Management.md` |
| Prototype | [STF-004.html](../prototype/screens/STF-004.html) |
| Rendered reference | [STF-004.png](../screenshots/STF-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Trigger a password reset email without exposing or generating a password in the desktop UI.

## Users

Admin only (open question)

## Permissions

Admin only; reset authorization policy unresolved.

## Entry points

Staff list row Reset password.

## Navigation

Send → staff list with audit. Cancel → list.

## Layout regions

- Staff list behind scrim
- Narrow dialog
- Reset consequence
- Account context
- Identity verification

## Components

- Dialog
- Info alert
- Key-values
- Verification checkbox

## Data shown

- Dr. Meera Nair
- Work email delivery
- Active account

## Actions

- Send reset email
- Cancel

## Forms and fields

- Identity verification acknowledgement

## States

- Ready
- Sending
- Email delivery failure
- Inactive account
- Permission denied

## Offline and data behavior

Disabled; reset requires Auth connectivity.

## Keyboard

Focus trap; Escape cancel; primary action explicit.

## Accessibility

No password disclosure; delivery and session caveats in text.

## Dependencies

STF-001/003; Auth; audit.

## Open questions / not approved

Who may reset passwords, whether reset revokes sessions, inactive-user reset behavior.

## Design notes and evidence boundary

No password is displayed or generated in the renderer.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
