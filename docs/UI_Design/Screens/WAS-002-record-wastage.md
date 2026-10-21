# WAS-002 · Record wastage

> **Design specification 31 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `WAS-002` |
| Section | Wastage |
| Feature | Wastage |
| Source specification | `08-Wastage.md` |
| Prototype | [WAS-002.html](../prototype/screens/WAS-002.html) |
| Rendered reference | [WAS-002.png](../screenshots/WAS-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Record a positive, batch-linked waste quantity with a reason and actor, reducing stock exactly once.

## Users

Admin, nurse, inventory manager

## Permissions

Record proposed for these roles; approval thresholds unresolved.

## Entry points

Wastage overview Record wastage; batch detail waste action.

## Navigation

Record → wastage overview. Cancel → back.

## Layout regions

- Page header
- Batch form
- Reason form
- Actor confirmation
- Before/after stock rail

## Components

- Select fields
- Quantity
- Reason taxonomy
- Details textarea
- Confirmation checkboxes

## Data shown

- Pentavalent AV-2409
- 2 doses
- ₹760 net rate
- 26 remaining

## Actions

- Record wastage
- Cancel

## Forms and fields

- Vaccine/batch (required)
- Date (required)
- Quantity (required, >0, ≤ available)
- Reason (required)
- Details
- Physical write-off and clinical-use confirmations

## States

- Ready
- Saving
- Insufficient stock
- Expired batch
- Offline
- Conflict

## Offline and data behavior

Local commit/outbox; server conflict visible.

## Keyboard

Form order; confirmation checkboxes before submit; focus ring.

## Accessibility

Errors linked; stock preview text; no color-only warnings.

## Dependencies

WAS-001–004; inventory ledger; audit; sync.

## Open questions / not approved

Is a reason taxonomy required? Are partial vials tracked? Who approves large write-offs?

## Design notes and evidence boundary

Expired stock can be wasted but not used clinically.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
