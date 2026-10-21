# PAT-005 · Duplicate warning

> **Design specification 12 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `PAT-005` |
| Section | Patients |
| Feature | Patient Management |
| Source specification | `04-Patient-Management.md` |
| Prototype | [PAT-005.html](../prototype/screens/PAT-005.html) |
| Rendered reference | [PAT-005.png](../screenshots/PAT-005.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Warn before creating a likely duplicate and offer a clear route to the existing record.

## Users

Registration and clinical roles

## Permissions

Create/read patient records.

## Entry points

Registration submit when name/phone fuzzy match exists.

## Navigation

Review existing → profile. Create new → requires documented reason.

## Layout regions

- Registration context behind scrim
- Wide warning dialog
- Match cards
- Reason field
- Decision footer

## Components

- Warning dialog
- Match cards
- Badges
- Reason input

## Data shown

- Two fictional similar records
- Same phone, different visit history

## Actions

- Review existing record
- Create new record
- Cancel

## Forms and fields

- Override reason (required to continue with a new record)

## States

- One match
- Multiple matches
- Exact clinic ID conflict
- Offline local match

## Offline and data behavior

Duplicate checks use the local index; remote-only matches may appear later and must not merge silently.

## Keyboard

Focus trap; primary action is review, not blind creation; Escape cancels.

## Accessibility

Dialog title names the risk; match similarity explained in text; destructive/override action visually distinct.

## Dependencies

PAT-003/007; local search; audit.

## Open questions / not approved

Override permissions, fuzzy-match threshold and whether phone is mandatory for registration remain unresolved.

## Design notes and evidence boundary

The dialog is a warning, not an automatic merge. It must not expose more PHI than needed.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
