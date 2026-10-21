# SYS-007 · Restore backup preview

> **Design specification 64 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SYS-007` |
| Section | System |
| Feature | Backup and Recovery |
| Source specification | `18-Backup-and-Recovery.md` |
| Prototype | [SYS-007.html](../prototype/screens/SYS-007.html) |
| Rendered reference | [SYS-007.png](../screenshots/SYS-007.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Preview a backup, verify compatibility and require passphrase, safety snapshot and destructive confirmation before restore.

## Users

Admin only

## Permissions

Admin only; audited; destructive.

## Entry points

Backups Restore from file.

## Navigation

Create safety snapshot; restore; cancel. Failure must leave current data intact.

## Layout regions

- Page header
- Danger alert
- Backup manifest
- Compatibility checklist
- Confirm restore form
- What happens rail
- Current copy rail

## Components

- Manifest key-values
- Checks list
- Passphrase and typed confirmation
- Acknowledgement
- Warnings

## Data shown

- ncc-2026-10-20.nccb
- 2,418 patients
- schema v14
- 5 of 6 checks
- 3 pending writes

## Actions

- Create safety snapshot
- Restore local data
- Cancel

## Forms and fields

- Passphrase (required)
- Type RESTORE (required)
- Loss acknowledgement (required)

## States

- Preview
- Checks pass
- Checks fail
- Snapshotting
- Restoring
- Interrupted
- Rolled back
- Reconciliation conflict

## Offline and data behavior

Local restore; sync reconciliation happens after restore.

## Keyboard

Typed confirmation; destructive action requires explicit focus/acknowledgement; no auto-submit.

## Accessibility

Destructive consequence text; checklist text; passphrase error; no color-only.

## Dependencies

BAK-001–006; OFF; SYNC; audit.

## Open questions / not approved

Account binding checks, rollback trigger, reconciliation ownership, unsynced-write preservation.

## Design notes and evidence boundary

Restore is shown as blocked until a safety snapshot exists. This prototype performs no restore.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
