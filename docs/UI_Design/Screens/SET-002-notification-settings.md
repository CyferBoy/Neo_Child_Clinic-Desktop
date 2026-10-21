# SET-002 · Notification settings

> **Design specification 66 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SET-002` |
| Section | Settings |
| Feature | Settings |
| Source specification | `20-Settings.md; 19-Desktop-Notifications.md` |
| Prototype | [SET-002.html](../prototype/screens/SET-002.html) |
| Rendered reference | [SET-002.png](../screenshots/SET-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Expose OS permission, privacy-safe previews, quiet hours and clinic defaults for notifications.

## Users

All staff; admin clinic defaults

## Permissions

Personal preferences self-service; clinic defaults admin-only.

## Entry points

Settings Notifications; permission prompt link.

## Navigation

Appearance; security; clinic settings; test notification.

## Layout regions

- Page header
- Settings nav
- Permission card
- Privacy card
- Quiet hours form
- Clinic defaults
- Save row

## Components

- Status pill
- Toggles/checkboxes
- Time fields
- Selects
- Test action
- Admin badge

## Data shown

- Permission allowed
- Hide names default
- Quiet hours 20:00–08:00
- 08:00 due time

## Actions

- Test notification
- Open OS settings
- Save preferences

## Forms and fields

- Enable notifications
- Sound
- Hide preview names
- Due reminder time
- Quiet hours start/end
- Behavior
- Clinic defaults

## States

- Permission allowed
- Denied
- Quiet hours
- Test sent
- Invalid time range
- Offline

## Offline and data behavior

Local scheduling works offline; due list is source of truth. Permission denial must be visible, not silent.

## Keyboard

Toggles and time fields keyboard accessible; test result announced.

## Accessibility

Privacy default explained; permission state textual; no PHI in preview examples.

## Dependencies

NOT-001–005; REM; SET; OS notification bridge.

## Open questions / not approved

Clinic preview policy, quiet-hours override, sound defaults, notification retention.

## Design notes and evidence boundary

No SMS/WhatsApp is implied. OS preview hides names by default.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
