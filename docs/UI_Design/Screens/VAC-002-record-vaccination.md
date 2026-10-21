# VAC-002 · Record vaccination

> **Design specification 16 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `VAC-002` |
| Section | Vaccinations |
| Feature | Vaccination Management |
| Source specification | `05-Vaccination-Management.md` |
| Prototype | [VAC-002.html](../prototype/screens/VAC-002.html) |
| Rendered reference | [VAC-002.png](../screenshots/VAC-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Record a vaccination visit as one atomic local transaction with vaccine items, stock, reminder, payment and receipt link.

## Users

Admin, doctor, nurse (proposed)

## Permissions

Inventory manager may view but not record unless approved.

## Entry points

Vaccination list; patient profile; dashboard; patient due list.

## Navigation

Save → visit detail. Save & print → provisional receipt. Cancel → prior screen.

## Layout regions

- Page header
- Patient identity ribbon
- Vaccine items table
- Visit details and reminder
- Visit note
- Sticky totals and stock rail

## Components

- Line-item table
- Batch subtext
- Payment inputs
- Reminder controls
- Validation rail
- Atomic-save actions

## Data shown

- Fictional patient Aarav Sharma
- Pentavalent AV-2409 and Rotavirus RV-2408
- ₹2,050 total
- Cash/online split

## Actions

- Add vaccine
- Remove line
- Save visit
- Save & print
- Cancel

## Forms and fields

- Visit date (required)
- Given by
- Vaccine item (required)
- Batch (required, not expired)
- Quantity (1+, ≤ available)
- Price (non-negative)
- Cash + online = total
- Reminder type/date

## States

- Ready
- Saving/local commit
- Insufficient stock
- Expired batch
- Payment mismatch
- Offline/provisional receipt
- Partial group failure

## Offline and data behavior

Fully local commit; group uploads in dependency order; receipt remains provisional until the server assigns it.

## Keyboard

Logical form order; add/remove line actions keyboard accessible; Ctrl/Cmd+Enter saves in implementation.

## Accessibility

Line table has headers; stock warnings in text; totals associated with payment fields; errors linked to inputs.

## Dependencies

VAC-001–007; inventory ledger; reminders; finance; receipts; local transaction.

## Open questions / not approved

FEFO mandatory vs default, correction semantics, mixed visit scope and deletion permissions remain open.

## Design notes and evidence boundary

No receipt number is computed in the renderer. Stock quantity is never edited directly.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
