# AUTH-003 · Session expired

> **Design specification 3 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `AUTH-003` |
| Section | Authentication |
| Feature | Authentication and Session |
| Source specification | `02-Authentication-and-Session.md` |
| Prototype | [AUTH-003.html](../prototype/screens/AUTH-003.html) |
| Rendered reference | [AUTH-003.png](../screenshots/AUTH-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Re-authenticate after expiry without losing in-memory form work or exposing the previous screen's PHI.

## Users

Signed-in staff

## Permissions

Expired session; PHI must be masked until re-authentication.

## Entry points

Token expiry, refresh failure or sensitive-action re-authentication.

## Navigation

Success → return to the interrupted route. Sign out → sign-in.

## Layout regions

- Dashboard context behind a modal scrim
- Narrow dialog
- Email and password
- Unsaved-work note

## Components

- Modal dialog
- Warning icon
- Password field
- Sign-in and sign-out actions

## Data shown

- Staff email
- No patient data in the dialog

## Actions

- Sign in again
- Sign out
- Close (if safe)

## Forms and fields

- Email (read-only)
- Password (required)

## States

- Expired
- Invalid password
- Account revoked
- Network unavailable

## Offline and data behavior

Re-authentication requires Auth connectivity unless an approved offline policy exists.

## Keyboard

Focus trapped in dialog; Escape closes only if no sensitive operation is pending; Enter submits.

## Accessibility

aria-modal dialog, labelled title, focus trap, error announced, no data behind accessible scrim.

## Dependencies

AUTH-001; ADR-0004.

## Open questions / not approved

Whether unsaved form drafts survive expiry is unresolved; this mockup shows a non-PHI memory note only.

## Design notes and evidence boundary

The background is intentionally dimmed; screenshot shows the dialog state, not a separate dashboard.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
