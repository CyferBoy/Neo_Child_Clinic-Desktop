# SYS-003 · Local data & recovery

> **Design specification 60 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SYS-003` |
| Section | System |
| Feature | Local Persistence and Offline Operation |
| Source specification | `16-Local-Persistence-and-Offline-Operation.md` |
| Prototype | [SYS-003.html](../prototype/screens/SYS-003.html) |
| Rendered reference | [SYS-003.png](../screenshots/SYS-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Expose local database health, encryption, schema, disk and recovery posture without raw data access.

## Users

Admin/support with approved procedure; all staff may see health

## Permissions

No raw DB access from renderer. Destructive recovery admin-only.

## Entry points

Sync center Open local data; system health.

## Navigation

Run integrity check; backup; restore; migration history.

## Layout regions

- Page header
- Four health metrics
- Database details
- Recovery card
- Warning
- Checks rail
- Related system pages

## Components

- Metric cards
- Key-values
- Status checks
- Actions
- Warnings

## Data shown

- SQLCipher
- schema v14
- 184 MB
- 2.4 GB free
- integrity passed

## Actions

- Run integrity check
- Create backup
- Open migration history
- Restore a backup

## Forms and fields



## States

- Healthy
- Checking
- Migration failed
- Disk full
- Corrupt
- Keychain locked
- Unsupported schema

## Offline and data behavior

This page is local. Recovery operations must not claim success without verification.

## Keyboard

Actions reachable; progress text; no raw paths exposed in this preview.

## Accessibility

Health checks text; pass/fail not color-only; disk values labelled.

## Dependencies

OFF-001–006; BAK; local core; keychain; audit.

## Open questions / not approved

Idle/lock policy, support access, corruption repair procedure, migration rollback UX, path disclosure policy.

## Design notes and evidence boundary

No destructive reset is offered here; final policy is unresolved.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
