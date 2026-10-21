# INV-001 · Inventory overview

> **Design specification 24 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `INV-001` |
| Section | Inventory |
| Feature | Vaccine and Batch Inventory |
| Source specification | `07-Vaccine-and-Batch-Inventory.md` |
| Prototype | [INV-001.html](../prototype/screens/INV-001.html) |
| Rendered reference | [INV-001.png](../screenshots/INV-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Show batch-level stock, expiry risk, value and low-stock state without direct quantity editing.

## Users

All clinical roles read; inventory manager/admin manage

## Permissions

Catalog/batch/adjust admin/inventory manager; clinical roles read and consume.

## Entry points

Sidebar Inventory; stock alerts on dashboard; vaccination batch selector.

## Navigation

By vaccine/batch/ledger/expired views; batch detail; receive stock; adjustment.

## Layout regions

- Page header
- Stock summary strip
- View tabs
- Search/filter toolbar
- Vaccine stock table
- Expiry callout

## Components

- Summary cards
- Tabs
- Table
- Status badges
- Expiry alert

## Data shown

- ₹4.28L stock value
- 3 low-stock vaccines
- 2 batches expiring ≤30 days
- 7 vaccine groups / 23 batches

## Actions

- Receive stock
- Stock adjustment
- Open vaccine group
- Export
- Filter

## Forms and fields

- Search
- Storage filter
- Health filter

## States

- Loading
- Empty
- Ready
- Low stock
- Expiring
- Expired
- Pending movement
- Concurrent conflict

## Offline and data behavior

Local stock reads/writes with pending badges; expired batches excluded from clinical use but visible for waste.

## Keyboard

/ search; table rows open with Enter; filters accessible.

## Accessibility

Status includes text; expiry typed; money tabular; table header scopes.

## Dependencies

INV-001–007; VAC; WAS; BRW; local ledger.

## Open questions / not approved

FEFO mandatory? Who approves adjustments? Is low-stock global or per vaccine?

## Design notes and evidence boundary

Stock totals are derived from batches/ledger, not a single mutable quantity.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
