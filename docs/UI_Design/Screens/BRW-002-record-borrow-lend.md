# BRW-002 · Record borrow / lend

> **Design specification 33 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `BRW-002` |
| Section | Borrow & Return |
| Feature | Borrowed and Lent Vaccines |
| Source specification | `09-Borrowed-and-Lent-Vaccines.md` |
| Prototype | [BRW-002.html](../prototype/screens/BRW-002.html) |
| Rendered reference | [BRW-002.png](../screenshots/BRW-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Record a directional, batch-linked loan and its expected return without treating it as a sale.

## Users

Admin, nurse, inventory manager

## Permissions

Record proposed for these roles.

## Entry points

Borrow list Record borrow/lend.

## Navigation

Save → borrow list/detail. Cancel → list.

## Layout regions

- Page header
- Direction/counterparty form
- Vaccine/quantity form
- Stock effect rail
- Rules

## Components

- Segmented direction
- Counterparty fields
- Batch selector
- Quantity
- Stock preview
- Info alert

## Data shown

- City Care Clinic
- Pentavalent AV-2409
- 10 doses
- Expected return 24 Oct

## Actions

- Save record
- Cancel

## Forms and fields

- Direction (required)
- Counterparty (required)
- Contact
- Record date
- Expected return
- Reference
- Vaccine/batch (required)
- Quantity (required, ≤ available)
- Note

## States

- Ready
- Saving
- Insufficient stock
- Overdue date
- Offline
- Conflict

## Offline and data behavior

Local commit/outbox; batch availability checked locally and revalidated at commit.

## Keyboard

Direction toggle keyboard accessible; form order; save shortcut documented.

## Accessibility

Direction labels not color-only; quantity errors linked; stock preview labelled.

## Dependencies

BRW-001/003; inventory; audit.

## Open questions / not approved

Who can write off a lost item and whether due dates create reminders.

## Design notes and evidence boundary

No receipt, payment or sale is created by this workflow.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
