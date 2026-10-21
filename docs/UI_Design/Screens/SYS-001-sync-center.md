# SYS-001 · Sync center

> **Design specification 58 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SYS-001` |
| Section | System |
| Feature | Supabase Synchronization |
| Source specification | `17-Supabase-Sync.md` |
| Prototype | [SYS-001.html](../prototype/screens/SYS-001.html) |
| Rendered reference | [SYS-001.png](../screenshots/SYS-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Make local-first sync observable: pending groups, conflicts, retries and connection state without false acknowledgement.

## Users

All staff; admin for conflict resolution

## Permissions

Own writes visible; admin can review/resolve conflicts. No raw server credentials.

## Entry points

Sidebar Sync center; status pill; pending badges; failed writes.

## Navigation

Review conflict; pull latest; open local data; pause/resume sync.

## Layout regions

- Page header
- Four health metrics
- Outbox table with status tabs
- Connection rail
- Sync actions
- Warning

## Components

- Metric cards
- Tabs
- Outbox table
- Connection key-values
- Status badges
- Actions

## Data shown

- 3 pending writes
- 1 conflict
- 2 min last sync
- 1 h 8 m oldest
- Fictional groups

## Actions

- Sync now
- Pause
- Review conflict
- Pull latest
- Open local data

## Forms and fields



## States

- Online/synced
- Syncing
- Offline
- Auth expired
- Conflict
- Retry/backoff
- Group failure
- Paused

## Offline and data behavior

Shows offline and preserves outbox. No new server acknowledgement is inferred. Retry after re-auth.

## Keyboard

Actions reachable; table rows open; sync status announced without polling noise.

## Accessibility

Status text and counts; progress not spinner-only; timestamps include timezone.

## Dependencies

SYNC-001–007; OFF; local outbox; auth; audit.

## Open questions / not approved

Deletion/absence contract (NCC-023), conflict taxonomy, retry limits, pause semantics and live Supabase status.

## Design notes and evidence boundary

This preview does not connect to Supabase. The UI must not claim success for a partial group.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
