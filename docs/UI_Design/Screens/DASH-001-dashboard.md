# DASH-001 · Dashboard

> **Design specification 7 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `DASH-001` |
| Section | Dashboard |
| Feature | Dashboard |
| Source specification | `14-Dashboard.md` |
| Prototype | [DASH-001.html](../prototype/screens/DASH-001.html) |
| Rendered reference | [DASH-001.png](../screenshots/DASH-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Give each role a same-day operational view of visits, due vaccinations, stock risk and collections.

## Users

All staff (role-aware content)

## Permissions

Dashboard widgets are filtered by role; financial widget requires finance permission.

## Entry points

Default post-login route; sidebar Dashboard.

## Navigation

Widgets and actions deep-link to patients, vaccinations, reminders, inventory, finance.

## Layout regions

- Page header with date and actions
- Four metric cards
- Today's clinic schedule
- Needs attention
- Due today

## Components

- Metric cards
- Schedule rows
- Alert cards
- Status badges
- Quick actions

## Data shown

- 18 visits
- 7 due vaccinations
- 3 low-stock items
- ₹18,450 collections (fictional)

## Actions

- Record vaccination
- Register patient
- Open patients
- New consultation
- View due list

## Forms and fields



## States

- Morning/ready
- Loading skeleton
- Offline (banner)
- No visits today
- Role without financial widget
- Sync conflict attention

## Offline and data behavior

Shows local data with an offline banner and pending badges; no silent freshness claim.

## Keyboard

Skip link to main content; action buttons reachable in DOM order; table/schedule rows expose links.

## Accessibility

Metric values have text labels; alerts not color-only; heading hierarchy; schedule rows have descriptive links.

## Dependencies

DSH-001–005; PAT/VAC/REM/INV/FIN data; local cache; sync status.

## Open questions / not approved

Exact widget priority per role and whether collections belong on the doctor dashboard are unresolved.

## Design notes and evidence boundary

All numbers and names are fictional design data. The dashboard is a composition, not five separate screens.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
