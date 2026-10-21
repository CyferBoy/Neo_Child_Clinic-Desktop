# CON-004 · Delete consultation

> **Design specification 23 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `CON-004` |
| Section | Consultations |
| Feature | Consultation Management |
| Source specification | `06-Consultation-Management.md` |
| Prototype | [CON-004.html](../prototype/screens/CON-004.html) |
| Rendered reference | [CON-004.png](../screenshots/CON-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Delete or cancel a consultation with a reason while preserving the linked visit, payment and audit.

## Users

Admin, doctor (confirmation)

## Permissions

Deletion requires confirmation and audit.

## Entry points

Consultation detail Delete / cancel.

## Navigation

Delete → detail/list with audit. Cancel → detail.

## Layout regions

- Detail context behind scrim
- Narrow destructive dialog
- Linked payment warning
- Reason
- Confirmation

## Components

- Destructive dialog
- Context summary
- Reason field
- Required acknowledgement

## Data shown

- C-2084
- ₹500 paid
- Receipt NCC-R-004197

## Actions

- Delete consultation
- Cancel

## Forms and fields

- Reason (required)
- Acknowledgement (required)

## States

- Ready
- Validation error
- Deleting
- Conflict
- Permission denied

## Offline and data behavior

Delete is audit-required; offline policy for deletion is unresolved at the sync boundary.

## Keyboard

Focus trapped; Escape cancels; delete requires explicit acknowledgement.

## Accessibility

Destructive action clearly labelled; consequence text; no timeout.

## Dependencies

CON-003; AUD; finance; receipts; sync deletion contract.

## Open questions / not approved

What happens to a receipt when a consultation is deleted? Is cancellation distinct from deletion?

## Design notes and evidence boundary

This mockup preserves the visit and payment; that is proposed, not implemented.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
