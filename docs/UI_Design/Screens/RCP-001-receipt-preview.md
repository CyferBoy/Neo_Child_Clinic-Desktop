# RCP-001 · Receipt preview

> **Design specification 45 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `RCP-001` |
| Section | Receipts |
| Feature | Receipts and Printing |
| Source specification | `13-Receipts-and-Printing.md` |
| Prototype | [RCP-001.html](../prototype/screens/RCP-001.html) |
| Rendered reference | [RCP-001.png](../screenshots/RCP-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Preview a final, server-numbered receipt linked to the visit and payment before printing or saving a copy.

## Users

Admin, doctor, receptionist

## Permissions

Print proposed for these roles; void/reprint role policy unresolved.

## Entry points

Payment detail; vaccination/consultation detail; receipt queue.

## Navigation

Print; save PDF; reprint; back to payment.

## Layout regions

- Page header
- Centered receipt paper
- Receipt status rail
- Print settings
- Privacy note

## Components

- Receipt document
- Status key-values
- Printer settings
- Reprint link

## Data shown

- NCC-R-004182
- Aarav Sharma
- V-10942
- ₹2,050
- Cash/online split

## Actions

- Print receipt
- Save PDF
- Reprint
- Change printer

## Forms and fields

- Printer (required for print)
- Paper size
- Duplicate marker (reprint only)

## States

- Provisional (blocked final print)
- Ready/final
- Printing
- Printer error
- Printed
- Reprint

## Offline and data behavior

Final print is blocked until the server assigns a receipt number. A provisional preview must be labelled.

## Keyboard

Print settings reachable before print; receipt text selectable; focus returns after dialog.

## Accessibility

Document heading hierarchy; table has headers; amounts labelled; screen readers can read receipt text.

## Dependencies

RCP-001–005; finance; visits; local print bridge.

## Open questions / not approved

Offline final receipt legality, template/legal text, void/reprint policy, PDF export requirement.

## Design notes and evidence boundary

The receipt number is server-assigned; the preview cannot create one. Clinic details are fictional.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
