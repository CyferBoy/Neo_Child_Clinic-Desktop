# INV-006 · Adjust stock

> **Design specification 29 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `INV-006` |
| Section | Inventory |
| Feature | Vaccine and Batch Inventory |
| Source specification | `07-Vaccine-and-Batch-Inventory.md` |
| Prototype | [INV-006.html](../prototype/screens/INV-006.html) |
| Rendered reference | [INV-006.png](../screenshots/INV-006.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Adjust stock through an audited ledger movement with reason and actor.

## Users

Admin, inventory manager (approval policy unresolved)

## Permissions

Adjust admin/inventory manager; approval for large write-offs unresolved.

## Entry points

Batch detail Adjust batch; inventory Stock adjustment.

## Navigation

Record adjustment → batch detail/ledger. Cancel → batch.

## Layout regions

- Batch context behind scrim
- Dialog form
- New balance preview
- Reason and note

## Components

- Adjustment type
- Quantity
- Reason
- Note
- Balance preview

## Data shown

- AV-2409
- 28 on hand
- −2
- new balance 26

## Actions

- Record adjustment
- Cancel

## Forms and fields

- Type (increase/decrease)
- Quantity (required)
- Reason (required)
- Note

## States

- Ready
- Validation
- Insufficient stock
- Authorization needed
- Offline
- Conflict

## Offline and data behavior

Local movement with pending badge; server conflict is surfaced, not overwritten.

## Keyboard

Focus trap; quantity/type keyboard accessible; Escape cancel.

## Accessibility

Reason taxonomy text; preview labels; destructive decrease not color-only.

## Dependencies

INV-004; audit; ledger; sync.

## Open questions / not approved

Who approves stock adjustments and the reason taxonomy are unresolved.

## Design notes and evidence boundary

This is an explicit movement, never a direct quantity edit.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
