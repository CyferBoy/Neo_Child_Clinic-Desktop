# BRW-003 · Record return

> **Design specification 34 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `BRW-003` |
| Section | Borrow & Return |
| Feature | Borrowed and Lent Vaccines |
| Source specification | `09-Borrowed-and-Lent-Vaccines.md` |
| Prototype | [BRW-003.html](../prototype/screens/BRW-003.html) |
| Rendered reference | [BRW-003.png](../screenshots/BRW-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Record a full or partial return without exceeding the outstanding balance or closing the record early.

## Users

Admin, nurse, inventory manager

## Permissions

Record return proposed for these roles.

## Entry points

Borrow list open/partial record Return.

## Navigation

Record return → list/detail with updated balance. Cancel → list.

## Layout regions

- Borrow list behind scrim
- Return dialog
- Balance/context summary
- Return quantity and condition
- Confirmation

## Components

- Dialog
- Balance summary
- Return fields
- Condition select
- Checkbox

## Data shown

- BR-1042
- 4 outstanding
- 6 already returned
- AV-2409

## Actions

- Record return
- Cancel

## Forms and fields

- Return quantity (required, ≤ outstanding)
- Return date
- Condition
- Note
- Physical verification

## States

- Ready
- Validation
- Over-return blocked
- Closed record
- Offline
- Conflict

## Offline and data behavior

Local return and outbox; server conflict surfaced; returns restore stock once.

## Keyboard

Focus trap; quantity focus; Escape cancel.

## Accessibility

Outstanding and remaining balance in text; no color-only warning.

## Dependencies

BRW-001/002; inventory; audit; sync.

## Open questions / not approved

Closed-record behavior, condition taxonomy, and lost/damaged resolution path are unresolved.

## Design notes and evidence boundary

Partial returns keep the original record open.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
