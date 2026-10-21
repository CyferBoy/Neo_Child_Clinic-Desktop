# SYS-002 · Resolve sync conflict

> **Design specification 59 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SYS-002` |
| Section | System |
| Feature | Supabase Synchronization |
| Source specification | `17-Supabase-Sync.md` |
| Prototype | [SYS-002.html](../prototype/screens/SYS-002.html) |
| Rendered reference | [SYS-002.png](../screenshots/SYS-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Compare local and server versions of a high-risk stock conflict and resolve deliberately, with audit and no last-write-wins.

## Users

Admin (proposed), with domain input

## Permissions

Admin review; stock/money/clinical conflicts never auto-resolve.

## Entry points

Sync center conflict row; audit event linked conflict.

## Navigation

Resolve and reapply; discard local; cancel; open audit.

## Layout regions

- Page header
- Conflict summary strip
- Danger alert
- Local vs server cards
- Comparison table
- Resolution choice
- Why-blocked rail

## Components

- Comparison cards
- Diff table
- Resolution cards
- Reason field
- Warning alerts

## Data shown

- PCV-2411
- Local −2 · server −1
- v18 → v19
- Physical count not verified

## Actions

- Resolve & reapply
- Discard local
- Cancel
- Open audit event

## Forms and fields

- Resolution choice (required)
- Resolution note (required)

## States

- Unresolved
- Resolving
- Reapply conflict
- Discarded
- Permission denied
- Server changed again

## Offline and data behavior

Conflict resolution requires a current server version; cannot be done offline.

## Keyboard

Choice cards keyboard selectable; destructive/discard separated; reason required.

## Accessibility

Both sides labelled; interpretation text; no color-only conflict; table headers.

## Dependencies

SYS-001; INV; audit; sync conflict engine.

## Open questions / not approved

Exact resolution math, admin authority, physical-count verification, reapply semantics, receipt conflicts.

## Design notes and evidence boundary

The UI deliberately avoids a simple 'Keep mine/Keep theirs' timestamp choice.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
