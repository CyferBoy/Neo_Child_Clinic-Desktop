# INV-002 · Vaccine catalogue

> **Design specification 25 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `INV-002` |
| Section | Inventory |
| Feature | Vaccine and Batch Inventory |
| Source specification | `07-Vaccine-and-Batch-Inventory.md` |
| Prototype | [INV-002.html](../prototype/screens/INV-002.html) |
| Rendered reference | [INV-002.png](../screenshots/INV-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Maintain vaccine identity, brand, manufacturer, category, schedule, storage and reference prices.

## Users

Admin, inventory manager

## Permissions

Catalog edit admin/inventory manager; read all clinical roles.

## Entry points

Inventory tabs or catalogue link.

## Navigation

Add/edit vaccine; return to stock.

## Layout regions

- Page header
- Search/filter toolbar
- Catalogue table
- Historical-price note

## Components

- Table
- Status badges
- Add/edit actions
- Info alert

## Data shown

- 8 fictional catalogue items
- MRP and net rates
- Manufacturer and category

## Actions

- Add vaccine
- Import catalogue
- Edit
- Filter

## Forms and fields

- Search
- Category filter

## States

- Loading
- Empty
- Ready
- Duplicate brand
- Archived catalog item

## Offline and data behavior

Local edit with outbox; conflict on catalog identity is surfaced.

## Keyboard

Search focus; edit actions labelled with brand.

## Accessibility

MRP/net rate columns labelled; status text; table headers.

## Dependencies

INV-003; INV-007; vaccination pricing.

## Open questions / not approved

Catalog identity/uniqueness policy and supplier return handling remain unresolved.

## Design notes and evidence boundary

Editing a catalog item never reprices historical batches or visits.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
