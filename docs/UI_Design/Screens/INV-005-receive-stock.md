# INV-005 · Receive stock

> **Design specification 28 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `INV-005` |
| Section | Inventory |
| Feature | Vaccine and Batch Inventory |
| Source specification | `07-Vaccine-and-Batch-Inventory.md` |
| Prototype | [INV-005.html](../prototype/screens/INV-005.html) |
| Rendered reference | [INV-005.png](../screenshots/INV-005.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Create a batch and one incoming stock movement transactionally.

## Users

Admin, inventory manager

## Permissions

Batch receive admin/inventory manager.

## Entry points

Inventory Receive stock; batch detail Receive more.

## Navigation

Save → batch detail/inventory. Cancel → inventory.

## Layout regions

- Page header
- Vaccine/supplier form
- Dates/quantity form
- Receiving note
- Receipt preview rail
- Batch rules

## Components

- Form sections
- Date/quantity fields
- Calculated preview
- Cold-chain acknowledgement

## Data shown

- Pentavalent Pentavac SD
- 48 doses
- ₹760 purchase
- ₹850 selling
- Expiry 30 Jun 2027

## Actions

- Receive stock
- Cancel

## Forms and fields

- Vaccine (required)
- Batch number (required, unique)
- Supplier
- Invoice/GRN
- Purchase date
- Expiry date
- Quantity
- Purchase price
- Selling price
- Storage location
- Cold-chain acknowledgement

## States

- Ready
- Saving
- Duplicate batch
- Invalid expiry
- Negative quantity
- Offline
- Conflict

## Offline and data behavior

Local transaction and outbox; no partial batch write.

## Keyboard

Form order; calculated totals updated in implementation; date picker accessible.

## Accessibility

Required fields; error text; calculated values labelled; no color-only warnings.

## Dependencies

INV-001–004; local ledger; sync.

## Open questions / not approved

Partial receipt, batch-number uniqueness across suppliers, and cold-chain evidence requirements remain unresolved.

## Design notes and evidence boundary

The receipt preview is not a financial posting.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
