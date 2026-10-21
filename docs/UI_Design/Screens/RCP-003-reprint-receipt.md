# RCP-003 · Reprint receipt

> **Design specification 47 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `RCP-003` |
| Section | Receipts |
| Feature | Receipts and Printing |
| Source specification | `13-Receipts-and-Printing.md` |
| Prototype | [RCP-003.html](../prototype/screens/RCP-003.html) |
| Rendered reference | [RCP-003.png](../screenshots/RCP-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Reprint with the original number, a duplicate marker and an audit reason.

## Users

Admin, doctor, receptionist

## Permissions

Reprint/void requires audit and role policy.

## Entry points

Receipt preview Reprint.

## Navigation

Reprint → print queue/preview. Cancel → receipt.

## Layout regions

- Receipt preview behind scrim
- Narrow dialog
- Original receipt context
- Reason
- Duplicate acknowledgement

## Components

- Dialog
- Key-values
- Reason select
- Duplicate checkbox

## Data shown

- NCC-R-004182
- Original print time
- ₹2,050

## Actions

- Reprint duplicate
- Cancel

## Forms and fields

- Reprint reason (required)
- Duplicate marker acknowledgement

## States

- Ready
- Permission denied
- Printer error
- Already printed
- Voided record

## Offline and data behavior

Reprint requires the original receipt record; final number must be server-assigned.

## Keyboard

Focus trap; explicit duplicate acknowledgement; Escape cancel.

## Accessibility

Reason and consequence text; no color-only warning.

## Dependencies

RCP-001/002; audit; print bridge.

## Open questions / not approved

Who can reprint/void; duplicate marking policy; void-after-refund.

## Design notes and evidence boundary

Reprint never changes the receipt number.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
