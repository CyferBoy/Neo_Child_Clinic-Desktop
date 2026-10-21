# AUD-002 · Audit event detail

> **Design specification 57 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `AUD-002` |
| Section | Administration |
| Feature | Audit Logging |
| Source specification | `21-Audit-Logging.md` |
| Prototype | [AUD-002.html](../prototype/screens/AUD-002.html) |
| Rendered reference | [AUD-002.png](../screenshots/AUD-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Show one append-only event with server-derived actor, redacted payload, integrity and linked conflict.

## Users

Admin only

## Permissions

Admin read; no mutation.

## Entry points

Audit log row.

## Navigation

Open linked conflict; close. No edit/delete.

## Layout regions

- Audit list behind scrim
- Wide right drawer
- Actor card
- Event/integrity cards
- Redacted payload
- Event history

## Components

- Drawer
- Key-values
- Code block
- Timeline
- Status badges

## Data shown

- EVT-9F3A-2044
- Stock adjustment conflict
- PCV-2411
- Admin actor
- Redacted payload

## Actions

- Close
- Open sync conflict

## Forms and fields



## States

- Ready
- Payload redacted
- Integrity failure
- Permission denied
- Linked event unavailable

## Offline and data behavior

Local audit event read; unresolved sync shown.

## Keyboard

Focus enters drawer; Escape closes; code block scrollable with keyboard.

## Accessibility

Code block has accessible label; hash/event ID readable; timeline ordered.

## Dependencies

AUD-001; audit schema; sync conflict; export.

## Open questions / not approved

What payload fields are lawful/appropriate for audit? Hash verification implementation.

## Design notes and evidence boundary

The payload contains no patient name; the UI shows only a redacted preview.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
