# AUTH-005 · Sign out with pending writes

> **Design specification 5 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `AUTH-005` |
| Section | Authentication |
| Feature | Authentication and Session |
| Source specification | `02-Authentication-and-Session.md` |
| Prototype | [AUTH-005.html](../prototype/screens/AUTH-005.html) |
| Rendered reference | [AUTH-005.png](../screenshots/AUTH-005.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Prevent an unsafe sign-out while local writes are pending, and offer a safe sync path.

## Users

Signed-in staff

## Permissions

Own session only.

## Entry points

User chooses sign out while the outbox has pending or conflicted writes.

## Navigation

Sync now → Sync center. Cancel → previous screen. Sign out is blocked in this design.

## Layout regions

- Dashboard context behind scrim
- Narrow warning dialog
- Pending write summary
- Sync-first actions

## Components

- Warning dialog
- Pending write list
- Sync now
- Sync center

## Data shown

- Fictional patient name
- Visit and stock item counts
- No payment credentials

## Actions

- Sync now
- Open sync center
- Cancel

## Forms and fields



## States

- Pending writes
- Sync in progress
- Sync conflict
- No pending writes (dialog not shown)

## Offline and data behavior

When offline, the dialog should explain that sync is unavailable and block destructive sign-out; policy confirmation required.

## Keyboard

Focus trapped; Escape cancels; primary action syncs and remains in the app.

## Accessibility

Warning uses text and icon; counts are readable; no auto-dismiss.

## Dependencies

SYNC-001–007; ADR-0004; local outbox.

## Open questions / not approved

The final sign-out policy and cache-clearing behavior are unresolved. This mockup deliberately blocks sign-out.

## Design notes and evidence boundary

The dialog does not claim that unsynced changes are safe across sign-out.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
