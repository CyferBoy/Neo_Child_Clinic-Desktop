# CON-003 · Consultation detail

> **Design specification 22 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `CON-003` |
| Section | Consultations |
| Feature | Consultation Management |
| Source specification | `06-Consultation-Management.md` |
| Prototype | [CON-003.html](../prototype/screens/CON-003.html) |
| Rendered reference | [CON-003.png](../screenshots/CON-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Read the consultation, its payment and follow-up, and review the audit trail.

## Users

Admin, doctor

## Permissions

Clinical notes role-scoped; delete requires confirmation and audit.

## Entry points

Consultation list; patient timeline.

## Navigation

Edit; print receipt; add addendum; delete/cancel; open patient.

## Layout regions

- Page header
- Patient ribbon
- Clinical note card
- Payment and follow-up cards
- Audit rail
- Delete warning

## Components

- Clinical note
- Key-value blocks
- Audit timeline
- Action list

## Data shown

- C-2084
- Mild viral fever note
- ₹500 paid
- Receipt NCC-R-004197
- Follow-up 27 Oct

## Actions

- Edit
- Print receipt
- Add addendum
- Delete/cancel

## Forms and fields



## States

- Ready
- Pending sync
- Conflict
- Corrected
- Deleted/cancelled
- Permission denied

## Offline and data behavior

Local read; pending state visible; receipt state explicit.

## Keyboard

Actions reachable in logical order; delete opens confirmation.

## Accessibility

Note heading; payment labels; audit ordered; no color-only follow-up status.

## Dependencies

CON-002/004; RCP; audit; finance.

## Open questions / not approved

Addendum behavior and deletion with receipt are unresolved.

## Design notes and evidence boundary

Deletion does not delete the visit or payment; this is stated in the UI.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
