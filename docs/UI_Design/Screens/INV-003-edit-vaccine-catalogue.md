# INV-003 · Edit vaccine catalogue

> **Design specification 26 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `INV-003` |
| Section | Inventory |
| Feature | Vaccine and Batch Inventory |
| Source specification | `07-Vaccine-and-Batch-Inventory.md` |
| Prototype | [INV-003.html](../prototype/screens/INV-003.html) |
| Rendered reference | [INV-003.png](../screenshots/INV-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Edit catalogue identity and storage/pricing metadata without changing historical records.

## Users

Admin, inventory manager

## Permissions

Catalog edit admin/inventory manager.

## Entry points

Vaccine catalogue row or Add vaccine.

## Navigation

Save → catalogue. Cancel → catalogue.

## Layout regions

- Catalogue context behind scrim
- Right drawer form
- Catalogue metadata
- Footer actions

## Components

- Drawer
- Text/select fields
- Storage textarea
- Metadata

## Data shown

- Rotavac
- Bharat Biotech
- 2-dose infant schedule
- MRP/net rate

## Actions

- Save vaccine
- Cancel

## Forms and fields

- Vaccine type (required)
- Brand (required)
- Manufacturer
- Company
- Category
- Dose schedule
- Storage details
- MRP
- Net rate

## States

- Ready
- Saving
- Validation
- Duplicate identity
- Conflict

## Offline and data behavior

Local edit and outbox; no historical repricing.

## Keyboard

Focus enters drawer; Escape cancel; labels visible.

## Accessibility

Drawer dialog semantics; background inert; error association.

## Dependencies

INV-002; INV-007.

## Open questions / not approved

Whether catalog items can be archived rather than deleted is unresolved.

## Design notes and evidence boundary

No batch quantity is edited here.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
