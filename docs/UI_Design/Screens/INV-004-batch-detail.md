# INV-004 · Batch detail

> **Design specification 27 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `INV-004` |
| Section | Inventory |
| Feature | Vaccine and Batch Inventory |
| Source specification | `07-Vaccine-and-Batch-Inventory.md` |
| Prototype | [INV-004.html](../prototype/screens/INV-004.html) |
| Rendered reference | [INV-004.png](../screenshots/INV-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Show batch identity, quantities, ledger, expiry and pricing, with auditable adjustment entry points.

## Users

Admin, inventory manager; clinical read

## Permissions

Adjust/receive admin/inventory manager.

## Entry points

Inventory by batch; vaccine group.

## Navigation

Receive more; adjust; movement ledger; back to inventory.

## Layout regions

- Page header
- Batch summary strip
- Ledger table
- Batch details rail
- Controls and FEFO note

## Components

- Summary cards
- Ledger table
- Key-value details
- Warning alert

## Data shown

- AV-2409
- 28 on hand
- expiry 30 Jun 2027
- ₹21,280 value
- 5 ledger movements

## Actions

- Receive more
- Adjust batch
- View all batches
- Open ledger

## Forms and fields



## States

- Ready
- Pending sync
- Reconciliation error
- Expired
- Zero stock
- Concurrent edit

## Offline and data behavior

Ledger reads local; pending movement visible; server trigger reconciliation is required after sync.

## Keyboard

Table and actions reachable; adjustment opens an audited dialog.

## Accessibility

Balance derived from ledger; dates typed; status text; table headers.

## Dependencies

INV-005/006; VAC; WAS; sync reconciliation.

## Open questions / not approved

Server-side stock trigger reconciliation approach is still to be implemented and tested.

## Design notes and evidence boundary

Direct quantity edits are prohibited in this design.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
