# STF-003 · Deactivate staff

> **Design specification 54 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `STF-003` |
| Section | Administration |
| Feature | Staff and Role Management |
| Source specification | `03-Staff-and-Role-Management.md` |
| Prototype | [STF-003.html](../prototype/screens/STF-003.html) |
| Rendered reference | [STF-003.png](../screenshots/STF-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Deactivate an account with a reason, revoking refresh capability without deleting history.

## Users

Admin only; self-deactivation forbidden

## Permissions

Admin only; cannot target own account.

## Entry points

Staff list row Deactivate.

## Navigation

Deactivate → staff list with audited status. Cancel → list.

## Layout regions

- Staff list behind scrim
- Narrow confirmation dialog
- Session/consequence warning
- Reason and note
- Acknowledgement

## Components

- Destructive dialog
- Warning
- Key-values
- Reason select
- Note
- Checkbox

## Data shown

- Ritika Sen · Nurse
- 1 open session
- Last active today

## Actions

- Deactivate account
- Cancel

## Forms and fields

- Reason (required)
- Admin note
- Refresh-revocation acknowledgement

## States

- Ready
- Validation
- Self-target blocked
- Last-admin blocked
- Offline disabled
- Conflict

## Offline and data behavior

Disabled. Deactivation requires backend Auth session revocation.

## Keyboard

Focus trap; Escape cancels; explicit acknowledgement.

## Accessibility

Consequence text; destructive action labelled; no color-only status.

## Dependencies

STF-001/004; Auth; audit; session revocation.

## Open questions / not approved

Reactivation policy, last-admin guard and immediate session invalidation.

## Design notes and evidence boundary

Deactivation is not deletion; clinical attribution is preserved.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
