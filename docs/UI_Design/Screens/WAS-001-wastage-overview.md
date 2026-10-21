# WAS-001 · Wastage overview

> **Design specification 30 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `WAS-001` |
| Section | Wastage |
| Feature | Wastage |
| Source specification | `08-Wastage.md` |
| Prototype | [WAS-001.html](../prototype/screens/WAS-001.html) |
| Rendered reference | [WAS-001.png](../screenshots/WAS-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Review batch-linked wastage, reasons, value and stock impact; surface expiry risk before write-off.

## Users

Admin, nurse, inventory manager

## Permissions

Record proposed for admin/nurse/inventory manager; audit read admin.

## Entry points

Sidebar Wastage; inventory expiry review.

## Navigation

Record wastage; filter by reason/date; review expiring stock.

## Layout regions

- Page header
- Summary strip
- Search/filter toolbar
- Waste table
- Reason chart and watch rail

## Components

- Summary cards
- Table
- Bar chart
- Watch list
- Status badges

## Data shown

- 42 doses this month
- ₹31,600
- 3.8% rate
- 6 fictional records

## Actions

- Record wastage
- Export
- Filter
- Review expiring stock

## Forms and fields

- Search
- Reason filter
- Date range

## States

- Loading
- Empty
- Ready
- Pending sync
- Conflict
- No waste this month

## Offline and data behavior

Local read/write; pending record visible; batch availability rechecked at commit.

## Keyboard

/ search; chart has text alternative; table actions labelled.

## Accessibility

Chart has a table/text alternative; reasons in text; quantities and money labelled.

## Dependencies

WAS-001–004; inventory; audit; reports.

## Open questions / not approved

Reason taxonomy, partial-vial tracking, and large write-off approval are unresolved.

## Design notes and evidence boundary

Wastage totals are illustrative and must not be treated as live clinic data.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
