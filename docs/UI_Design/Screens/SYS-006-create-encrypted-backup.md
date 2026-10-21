# SYS-006 · Create encrypted backup

> **Design specification 63 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SYS-006` |
| Section | System |
| Feature | Backup and Recovery |
| Source specification | `18-Backup-and-Recovery.md` |
| Prototype | [SYS-006.html](../prototype/screens/SYS-006.html) |
| Rendered reference | [SYS-006.png](../screenshots/SYS-006.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Create a passphrase-protected, authenticated local backup with an explicit include/exclude boundary.

## Users

Admin only

## Permissions

Admin only; audited.

## Entry points

Backups Create backup.

## Navigation

Create → backup history. Cancel → backups.

## Layout regions

- Page header
- Included/excluded card
- Passphrase form
- Destination
- PHI warning
- Backup preview rail
- Process rail

## Components

- Key-values
- Password fields
- Destination picker
- Checkboxes
- Preview
- Warnings

## Data shown

- 184 MB estimate
- 1.2 TB free
- schema v14
- no secrets

## Actions

- Create encrypted backup
- Cancel

## Forms and fields

- Passphrase (required)
- Confirm passphrase
- Destination (required)
- Passphrase-loss acknowledgement

## States

- Ready
- Creating
- Weak passphrase
- Destination unavailable
- Disk full
- Interrupted
- Permission denied

## Offline and data behavior

Local operation; no cloud upload. Temp files must not contain plaintext PHI.

## Keyboard

Passphrase fields labelled; destination picker accessible; progress announced.

## Accessibility

Passphrase guidance; include/exclude lists; no color-only errors.

## Dependencies

BAK-001–006; OFF; audit.

## Open questions / not approved

Passphrase strength policy, destination allowlist, temp-file shredding, large-backup UX.

## Design notes and evidence boundary

No real passphrase is shown. The destination is a fictional preview path.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
