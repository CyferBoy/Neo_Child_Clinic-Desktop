# AUTH-004 · Access denied

> **Design specification 4 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `AUTH-004` |
| Section | Authentication |
| Feature | Authentication and Session |
| Source specification | `02-Authentication-and-Session.md` |
| Prototype | [AUTH-004.html](../prototype/screens/AUTH-004.html) |
| Rendered reference | [AUTH-004.png](../screenshots/AUTH-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Explain deactivated accounts or missing roles without opening patient data.

## Users

Any account that fails role or active-status validation

## Permissions

No clinic data. Access is denied.

## Entry points

Deactivated account, missing/malformed app_metadata.role, or revoked session.

## Navigation

Try another account → Sign in. Close → exit application.

## Layout regions

- Centered access card
- Warning icon
- Explanation
- Two safe actions

## Components

- Access card
- Warning alert
- Reference code

## Data shown

- No patient identifiers
- No role details beyond the reason

## Actions

- Try another account
- Close application

## Forms and fields



## States

- Deactivated account
- Missing role
- Malformed role claim
- Revoked session

## Offline and data behavior

No PHI is opened. Local caches should be cleared on this transition per ADR-0004.

## Keyboard

Two actions in logical order; Enter activates focused action; Escape does not bypass denial.

## Accessibility

Plain-language heading; reason not conveyed by color; no technical role claim shown.

## Dependencies

AUTH-002; ADR-0004; RLS role constraints.

## Open questions / not approved

Support contact details and audit visibility for denied attempts are not specified.

## Design notes and evidence boundary

This is a terminal state; no sidebar or patient route is rendered.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
