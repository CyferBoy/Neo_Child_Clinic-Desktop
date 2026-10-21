# RCP-002 · Print queue error

> **Design specification 46 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `RCP-002` |
| Section | Receipts |
| Feature | Receipts and Printing |
| Source specification | `13-Receipts-and-Printing.md` |
| Prototype | [RCP-002.html](../prototype/screens/RCP-002.html) |
| Rendered reference | [RCP-002.png](../screenshots/RCP-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Recover from printer failure without losing the payment or issuing a different receipt number.

## Users

Admin, doctor, receptionist

## Permissions

Print/reprint role policy.

## Entry points

Print request failure; receipt queue.

## Navigation

Retry; choose printer; save PDF; return to receipt.

## Layout regions

- Page header
- Failed job card
- Job/payment details
- Print history
- Safety rail
- Print options

## Components

- Error alert
- Key-values
- Timeline
- Printer select
- Actions

## Data shown

- NCC-R-004182
- PAY-40871
- ₹2,050
- 2 attempts
- Reception A4 offline

## Actions

- Retry print
- Choose another printer
- Save as PDF
- Print test page

## Forms and fields

- Printer
- Paper size
- Duplicate marker

## States

- Printer offline
- Paper out
- Retrying
- Printed
- Spool failure

## Offline and data behavior

Print job is retained; payment remains recorded. A server-numbered receipt may be previewed but not newly numbered.

## Keyboard

Actions reachable; printer selection keyboard accessible; error announced.

## Accessibility

Error in text, not color-only; payment safety stated; print history ordered.

## Dependencies

RCP-001/003; print bridge; audit.

## Open questions / not approved

Spool retention and failure-recovery policy.

## Design notes and evidence boundary

Printer failure does not change payment or receipt identity.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
