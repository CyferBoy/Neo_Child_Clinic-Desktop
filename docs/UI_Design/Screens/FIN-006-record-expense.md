# FIN-006 · Record expense

> **Design specification 44 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `FIN-006` |
| Section | Finance |
| Feature | Finance and Payments |
| Source specification | `12-Finance-and-Payments.md` |
| Prototype | [FIN-006.html](../prototype/screens/FIN-006.html) |
| Rendered reference | [FIN-006.png](../screenshots/FIN-006.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Capture a valid expense with date, category, title, positive amount and method.

## Users

Admin, doctor, receptionist (record only; edit open)

## Permissions

Admin/doctor manage; reception record may be permitted.

## Entry points

Expenses list; finance overview.

## Navigation

Save → expenses. Cancel → finance.

## Layout regions

- Page header
- Expense form
- Supporting document
- Summary rail
- Rules

## Components

- Date/category/title
- Amount/method/reference
- Upload zone
- Summary
- Warning

## Data shown

- Cold-chain supplies
- ₹2,180
- UPI
- UPI-882041

## Actions

- Save expense
- Cancel
- Upload supporting document

## Forms and fields

- Date (required)
- Category (required)
- Title (required)
- Amount > 0 (required)
- Method (required)
- Reference
- Note
- Attachment (optional)

## States

- Ready
- Saving
- Validation
- Duplicate
- Offline
- Permission denied

## Offline and data behavior

Local expense/outbox; attachment handling and storage policy unresolved.

## Keyboard

Upload accessible by keyboard; form order; errors linked.

## Accessibility

Amount label; upload instructions; no color-only validation.

## Dependencies

FIN-005; audit; reports.

## Open questions / not approved

Receipt attachment storage, expense edit roles, refunds/discounts.

## Design notes and evidence boundary

Supporting document is shown as an optional local preview, not an implemented upload.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
