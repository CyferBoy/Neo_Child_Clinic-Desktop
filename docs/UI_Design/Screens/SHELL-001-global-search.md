# SHELL-001 · Global search

> **Design specification 6 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SHELL-001` |
| Section | Shell |
| Feature | Desktop Shell and Navigation |
| Source specification | `01-Desktop-Shell-and-Navigation.md` |
| Prototype | [SHELL-001.html](../prototype/screens/SHELL-001.html) |
| Rendered reference | [SHELL-001.png](../screenshots/SHELL-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Find a patient, batch, receipt or permitted action from anywhere in the app using bounded, permission-aware results.

## Users

All staff

## Permissions

Results respect role and clinic scope; no all-patient scan in the renderer.

## Entry points

Top-bar search, Ctrl/Cmd+K, or empty-state search.

## Navigation

Open result → permitted destination. Escape → prior screen.

## Layout regions

- Dashboard context behind a scrim
- Centered command palette
- Search field
- Grouped results and quick actions

## Components

- Command palette
- Search input
- Result rows
- Keyboard hints

## Data shown

- Fictional patient names, clinic IDs, ages, masked phones
- Batch and receipt groups are present but empty in this sample

## Actions

- Open patient
- Start vaccination
- Register patient

## Forms and fields

- Global search (bounded query, minimum 2 characters)

## States

- Idle
- Searching
- Results
- No results
- Permission hidden
- Offline local results

## Offline and data behavior

Searches the encrypted local index; stale remote-only results are marked.

## Keyboard

Ctrl/Cmd+K opens; ↑/↓ moves; Enter opens; Escape closes; Tab does not leave the palette.

## Accessibility

Combobox/listbox semantics, announced result count, no reliance on color for status, visible focus.

## Dependencies

PLAT-003; PAT-003; local search index.

## Open questions / not approved

Search ranking and whether batches/receipts are in Phase 1 global search remain unresolved.

## Design notes and evidence boundary

Phone values are fictional. Result cap and pagination must be enforced in implementation.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
