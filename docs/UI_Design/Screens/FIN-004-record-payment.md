# FIN-004 · Record payment

> **Design specification 42 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `FIN-004` |
| Section | Finance |
| Feature | Finance and Payments |
| Source specification | `12-Finance-and-Payments.md` |
| Prototype | [FIN-004.html](../prototype/screens/FIN-004.html) |
| Rendered reference | [FIN-004.png](../screenshots/FIN-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Record or update one visit-linked income row with a reconciled cash/online split.

## Users

Admin, doctor, receptionist

## Permissions

Income recording proposed for these roles.

## Entry points

Finance overview/transactions; visit detail.

## Navigation

Save → payment detail/transactions. Cancel → finance.

## Layout regions

- Page header
- Patient ribbon
- Payment form
- Receipt/note
- Payment summary rail
- Reconciliation rail

## Components

- Money fields
- Payment status
- Online reference
- Balanced alert
- Integer-minor-unit note

## Data shown

- Aarav Sharma
- ₹2,050
- Cash ₹1,500 / Online ₹550
- Receipt pending

## Actions

- Save payment
- Cancel

## Forms and fields

- Amount (required)
- Payment status
- Cash (non-negative)
- Online (non-negative)
- Cash + online = amount
- Online reference
- Note

## States

- Ready
- Saving
- Mismatch
- Duplicate income
- Receipt issued
- Offline
- Permission denied

## Offline and data behavior

Local record/outbox; receipt finalization waits for server; conflict visible.

## Keyboard

Form order; money values announced as text; save shortcut documented.

## Accessibility

Balanced/mismatch in text; amount fields labelled with currency; no color-only error.

## Dependencies

FIN-001–006; RCP; visits; integer money handling.

## Open questions / not approved

Refunds/discounts, partial payments and expense edit roles.

## Design notes and evidence boundary

The renderer displays values; the Go core owns authoritative arithmetic.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
