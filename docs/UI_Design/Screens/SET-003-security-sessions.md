# SET-003 · Security & sessions

> **Design specification 67 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SET-003` |
| Section | Settings |
| Feature | Settings |
| Source specification | `20-Settings.md; 02-Authentication-and-Session.md` |
| Prototype | [SET-003.html](../prototype/screens/SET-003.html) |
| Rendered reference | [SET-003.png](../screenshots/SET-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Explain session, idle-lock and local-data protections while separating device preferences from clinic policy.

## Users

All staff; admin policy

## Permissions

Session actions self-service; security policy admin-only; no secrets in settings.

## Entry points

Settings Security & sessions.

## Navigation

Local data status; lock now; sign out.

## Layout regions

- Page header
- Settings nav
- Current session card
- Idle lock policy
- Local data protection
- Recent sessions
- Save row

## Components

- Session key-values
- Status badges
- Policy fields
- Checklist
- Session table

## Data shown

- Admin current session
- 12-hour expiry
- 10-minute idle lock
- SQLCipher
- 2 sessions

## Actions

- Lock now
- Sign out
- Open local data status
- Save device preferences

## Forms and fields

- Lock inactivity
- Lock behavior
- OS-lock behavior
- Maximum allowed (policy)

## States

- Active
- Expiring
- Idle/locked
- Sign-out blocked by pending writes
- Keychain locked
- Permission denied

## Offline and data behavior

Idle lock and local protection are local. Authentication/session changes may require connectivity.

## Keyboard

Lock/sign out reachable; dialogs for blocked sign-out; focus return.

## Accessibility

Security states textual; no secret displayed; lock behavior explained.

## Dependencies

AUTH; OFF; SET; STF; audit.

## Open questions / not approved

Final idle-lock/offline unlock policy, clipboard policy, session revoke API, last-admin guard.

## Design notes and evidence boundary

No token or key is displayed. The mockup flags unresolved security policy rather than inventing it.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
