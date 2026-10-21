# VAC-004 · Vaccination visit detail

> **Design specification 18 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `VAC-004` |
| Section | Vaccinations |
| Feature | Vaccination Management |
| Source specification | `05-Vaccination-Management.md` |
| Prototype | [VAC-004.html](../prototype/screens/VAC-004.html) |
| Rendered reference | [VAC-004.png](../screenshots/VAC-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Show the atomic visit, its stock and reminder effects, payment, receipt status and audit trail.

## Users

Admin, doctor, nurse

## Permissions

Read role-scoped; correction/deletion role-gated.

## Entry points

Vaccination list; patient timeline.

## Navigation

Print receipt; correct; return to list; open reminder.

## Layout regions

- Page header
- Patient ribbon
- Vaccine items
- Payment and reminder cards
- Commit trail
- Details/validation rail

## Components

- Line table
- Status badges
- Key-value details
- Timeline
- Correct/delete actions

## Data shown

- Visit V-10942
- ₹2,050 paid
- Two stock movements
- Provisional receipt

## Actions

- Print receipt
- Correct visit
- Delete/correct
- Open reminder

## Forms and fields



## States

- Ready
- Pending sync
- Receipt conflict
- Partial group failure
- Corrected
- Deleted/reversed

## Offline and data behavior

Local commit visible; provisional receipt; conflict must block blind retry.

## Keyboard

All actions reachable; destructive action requires confirmation.

## Accessibility

Audit trail ordered; monetary values have labels; status not color-only.

## Dependencies

VAC-005/006/007; inventory; finance; receipts; audit.

## Open questions / not approved

Receipt reprint after correction and block scope are unresolved.

## Design notes and evidence boundary

The page does not imply that the server receipt number already exists.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
