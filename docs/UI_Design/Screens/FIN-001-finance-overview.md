# FIN-001 · Finance overview

> **Design specification 39 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `FIN-001` |
| Section | Finance |
| Feature | Finance and Payments |
| Source specification | `12-Finance-and-Payments.md` |
| Prototype | [FIN-001.html](../prototype/screens/FIN-001.html) |
| Rendered reference | [FIN-001.png](../screenshots/FIN-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Give finance-authorized staff a same-day view of income, expenses, net and reconciliation risk.

## Users

Admin, doctor, receptionist (income); expenses admin/doctor

## Permissions

Finance permission scoped; reports restricted by role.

## Entry points

Sidebar Finance; dashboard collections widget.

## Navigation

Record payment; record expense; transactions; expenses; reports.

## Layout regions

- Page header
- Four metric cards
- Collections chart
- Payment mix
- Recent transactions
- Expenses today

## Components

- Metric cards
- Line chart
- Donut
- Tables
- Quick actions

## Data shown

- ₹18,450 income
- ₹4,280 expenses
- ₹14,170 net
- ₹1,200 pending
- Fictional payments

## Actions

- Record payment
- Record expense
- Export
- View all

## Forms and fields



## States

- Loading
- Empty day
- Ready
- Pending sync
- Permission denied
- Stale/partial data

## Offline and data behavior

Local aggregates labelled with pending/stale state; never claim a complete day while writes are pending.

## Keyboard

Chart has text alternative; actions reachable; tables use headers.

## Accessibility

Money values tabular and labelled; donut has legend/text; color not sole method.

## Dependencies

FIN-001–006; RCP; RPT; visit income identity.

## Open questions / not approved

Refunds/discounts, expense edit roles, payment reference storage and money schema migration.

## Design notes and evidence boundary

Totals are illustrative. One visit income row is counted once.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
