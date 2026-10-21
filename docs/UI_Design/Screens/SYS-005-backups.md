# SYS-005 · Backups

> **Design specification 62 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SYS-005` |
| Section | System |
| Feature | Backup and Recovery |
| Source specification | `18-Backup-and-Recovery.md` |
| Prototype | [SYS-005.html](../prototype/screens/SYS-005.html) |
| Rendered reference | [SYS-005.png](../screenshots/SYS-005.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Review encrypted backup history, verification, destination and restore entry points without cloud assumptions.

## Users

Admin only

## Permissions

Admin only; audited export/restore.

## Entry points

Sidebar system or settings backup; system health.

## Navigation

Create backup; restore from file; save backup settings.

## Layout regions

- Page header
- Four backup metrics
- Backup history
- PHI warning
- Backup settings
- Safety snapshot rail

## Components

- Metric cards
- Table
- Settings form
- Warnings
- Status badges

## Data shown

- 4 verified backups
- 184 MB
- external drive
- daily 03:00 IST
- 14-day retention

## Actions

- Create backup
- Restore from file
- Save backup settings

## Forms and fields

- Schedule
- Destination
- Retention
- Passphrase requirement
- Checksum verification
- Cloud upload (off by default)

## States

- No backups
- Ready
- Verifying
- Failed checksum
- Disk full
- Restore in progress
- Permission denied

## Offline and data behavior

Export/restore local. No automatic cloud upload.

## Keyboard

Table and settings accessible; destructive restore separate.

## Accessibility

Backup status textual; passphrase requirement explicit; retention range help.

## Dependencies

BAK-001–006; OFF; audit; settings.

## Open questions / not approved

Approved destination policy, encryption implementation, retention enforcement and support role.

## Design notes and evidence boundary

Backups contain PHI. The preview filenames and sizes are fictional.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
