# FIN-003 · Payment detail

> **Design specification 41 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `FIN-003` |
| Section | Finance |
| Feature | Finance and Payments |
| Source specification | `12-Finance-and-Payments.md` |
| Prototype | [FIN-003.html](../prototype/screens/FIN-003.html) |
| Rendered reference | [FIN-003.png](../screenshots/FIN-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Show one visit-linked payment, its split, receipt state, linked service and audit identity.

## Users

Finance-authorized staff

## Permissions

Role-scoped; receipt access required.

## Entry points

Transactions list; receipt preview; visit detail.

## Navigation

View receipt; edit payment; open visit/patient/report.

## Layout regions

- Page header
- Payment summary card
- Linked services
- Edit warning
- Audit rail
- Related actions

## Components

- Summary
- Key-value list
- Service table
- Audit timeline
- Status badges

## Data shown

- PAY-40871
- ₹2,050
- Cash ₹1,500 / Online ₹550
- Provisional receipt
- Aarav Sharma

## Actions

- View receipt
- Edit payment
- Open visit
- Open patient

## Forms and fields



## States

- Ready
- Pending sync
- Receipt conflict
- Edited
- Permission denied

## Offline and data behavior

Local read; provisional receipt; conflict does not renumber.

## Keyboard

Actions reachable; receipt link labelled.

## Accessibility

Payment split text; audit ordered; balance label.

## Dependencies

FIN-002/004/006; RCP; audit.

## Open questions / not approved

Refund/correction workflow and receipt void policy.

## Design notes and evidence boundary

The page never presents a locally computed receipt number.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
