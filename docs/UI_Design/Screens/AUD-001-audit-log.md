# AUD-001 · Audit log

> **Design specification 56 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `AUD-001` |
| Section | Administration |
| Feature | Audit Logging |
| Source specification | `21-Audit-Logging.md` |
| Prototype | [AUD-001.html](../prototype/screens/AUD-001.html) |
| Rendered reference | [AUD-001.png](../screenshots/AUD-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Provide a paged, filtered, append-only audit view for sensitive actions with actor and source visible.

## Users

Admin only for read/export; system writes on behalf of authenticated actors

## Permissions

Admin read/export. No renderer write path. Policy §7 roles.

## Entry points

Sidebar Audit log, admin only.

## Navigation

Open event detail; filter; export redacted extract (approval pending).

## Layout regions

- Page header
- Event summary strip
- Category tabs
- Search/filter toolbar
- Audit table
- Unresolved warning

## Components

- Summary cards
- Tabs
- Table
- Action/status badges
- Row actions

## Data shown

- 128 events today
- 12 sensitive
- 2 unresolved
- 8 fictional events

## Actions

- Export redacted extract
- Filter
- Open event

## Forms and fields

- Search
- Date
- Actor
- Action/entity filters

## States

- Loading
- Empty
- Ready
- Permission denied
- Stale/pending
- Audit write failure
- Export denied

## Offline and data behavior

Audit intent is local with the business transaction; read view shows pending. Failed sensitive audit must roll back or flag.

## Keyboard

/ search; table rows open; filters accessible; no edit affordances.

## Accessibility

Time values explicit with timezone; actor role text; status not color-only; table headers.

## Dependencies

AUD-001–005; all sensitive modules; sync; export policy.

## Open questions / not approved

Retention, redaction rules, export approval, audit-write failure UX and PHI minimization.

## Design notes and evidence boundary

This is a business record, not a debug log. No update/delete affordance exists.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
