# VAC-005 · Correct or delete vaccination

> **Design specification 19 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `VAC-005` |
| Section | Vaccinations |
| Feature | Vaccination Management |
| Source specification | `05-Vaccination-Management.md` |
| Prototype | [VAC-005.html](../prototype/screens/VAC-005.html) |
| Rendered reference | [VAC-005.png](../screenshots/VAC-005.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Offer a safe correction diff or an audited delete with stock/payment reversal.

## Users

Admin, doctor (confirmation)

## Permissions

Admin/doctor confirmation; nurse may request correction but not delete.

## Entry points

Vaccination detail Correct visit or more menu.

## Navigation

Continue to correction → editable diff. Delete with reversal → confirmation and audit.

## Layout regions

- Visit detail behind scrim
- Wide decision dialog
- Two consequence cards
- Reason field
- Correction type

## Components

- Decision dialog
- Warning
- Risk badges
- Reason textarea
- Correction type

## Data shown

- Fictional visit
- Stock and receipt implications

## Actions

- Continue to correction
- Delete with reversal
- Cancel

## Forms and fields

- Reason (required)
- Correction type

## States

- Ready
- Receipt exists
- Payment already reconciled
- Conflict
- Permission denied

## Offline and data behavior

Correction can be local; deletion may be blocked by sync policy. Policy is unresolved.

## Keyboard

Focus trap; destructive action clearly separated; Escape cancel.

## Accessibility

Consequences in text; destructive button labelled with action, not color alone.

## Dependencies

VAC-004; AUD; stock ledger; finance.

## Open questions / not approved

Who may delete after a receipt, and whether corrections are edits or linked reversal events?

## Design notes and evidence boundary

This screen intentionally does not perform deletion directly; it opens a reviewed path.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
