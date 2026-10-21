# SYS-004 · Application update

> **Design specification 61 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SYS-004` |
| Section | System |
| Feature | Application Updates |
| Source specification | `22-Application-Updates.md` |
| Prototype | [SYS-004.html](../prototype/screens/SYS-004.html) |
| Rendered reference | [SYS-004.png](../screenshots/SYS-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Show a signed update, release notes and install readiness without interrupting active clinical work or unsynced writes.

## Users

All staff may check; admin deployment policy

## Permissions

Install may require admin; no unsigned/silent install.

## Entry points

Settings/about/updates; scheduled check notification.

## Navigation

Check again; install when safe; rollback details.

## Layout regions

- Page header
- Version card
- Release notes
- Install readiness
- Rollback card
- Policy and current install rails

## Components

- Version summary
- Readiness checklist
- Warnings
- Actions
- Policy list

## Data shown

- Current 0.1.0-preview
- New 0.2.0
- 84.2 MB
- 3 pending writes
- signature verified

## Actions

- Check for updates
- Install update (blocked)
- View rollback details

## Forms and fields



## States

- Checking
- Up to date
- Update available
- Downloading
- Signature invalid
- Blocked by unsynced writes
- Installing
- Failed
- Rollback available

## Offline and data behavior

Check fails gracefully; current version continues. Downloaded update waits.

## Keyboard

Install blocked state explained; actions labelled; release notes readable.

## Accessibility

Status textual; checks list; no countdown auto-install.

## Dependencies

UPD-001–005; sync; local transaction; installer.

## Open questions / not approved

Update channel policy, admin install rights, signature implementation, rollback procedure, telemetry scope.

## Design notes and evidence boundary

This preview cannot install anything; the block is intentional.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
