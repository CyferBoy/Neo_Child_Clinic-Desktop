---
title: Frontend Architecture
doc_status: proposed
evidence: React + TypeScript project direction + Android UX reference
updated: 2026-10-20
---

# Frontend Architecture

> **Proposed only.** No React application exists. The goal is a desktop-native, keyboard-efficient, offline-aware UI that never becomes an independent source of authorization or data truth.

## Stack and boundaries

- React + TypeScript, built by the chosen Wails frontend pipeline.
- All reads and writes go through typed Wails bindings. The renderer does not call Supabase, open the local database, or read arbitrary files.
- The renderer may cache view state and form drafts in memory, but the local database remains the durable working copy.
- No PHI in `localStorage`, `sessionStorage`, URL query strings, analytics, or crash breadcrumbs.

## Module structure

```text
src/
  app/                 shell, routes, providers, error boundary
  features/
    auth/
    patients/
    vaccinations/
    consultations/
    inventory/
    waste/
    borrowed/
    reminders/
    personal-reminders/
    finance/
    receipts/
    dashboard/
    reports/
    audit/
    settings/
    staff/
    updates/
  components/          design system, tables, forms, dialogs
  lib/                 bindings, formatting, validation, result types
  styles/
```

Each feature owns its screens, view models/hooks, validation messages, tests, and typed binding contracts. Cross-feature imports go through public module entry points, not deep paths.

## Routing and guards

- Routes are declarative and map to feature entry points.
- A route guard is a **usability** control. The Go service and RLS must enforce authorization independently.
- Deep links must not expose PHI. Use opaque internal IDs, not names or phone numbers, in URLs.
- Unsaved-change navigation requires confirmation.
- The sync center and offline banner are global, not per-screen.

## State model

| State | Owner | Rules |
|---|---|---|
| Session identity and role | Go; renderer receives a minimal view | Never trust a role copied into the renderer |
| Server data | Local DB via Go queries | Renderer subscribes to query results; no silent background mutation |
| Form draft | Renderer memory | Lost on explicit discard; recoverable drafts require a documented local store |
| Sync status | Go sync service | Pending/failed/conflicted counts are visible |
| UI preferences | Local settings store | No PHI; validated on load |
| Secrets | OS keychain, Go only | Never in renderer state |

## Screen patterns

### List screens
- Server-side or local-query pagination; no unbounded `SELECT *`.
- Search by name, clinic ID, phone; debounce; show result count.
- Empty, loading, error, offline, and permission-denied states.
- Bulk actions only where the domain allows and with explicit confirmation.

### Detail screens
- Stable header with patient identity and clinic ID.
- Tabs or sections for history, vaccinations, consultations, payments, notes, documents, audit.
- Every mutation shows a pending sync state until acknowledged.
- Destructive actions require a reason and are soft-deleted where the domain requires it.

### Forms
- Inline validation on blur and on submit; first error focused.
- Required fields are marked and explained.
- Numeric fields use locale-aware display but integer minor units in transport.
- Dates use a date picker and explicit IST label; no ambiguous free text.
- Save is disabled only for invalid/duplicate submission, not for offline.

### Tables
- Keyboard navigation, sticky header, column visibility, and accessible row actions.
- Money right-aligned with fixed decimal places.
- Dates formatted consistently; raw ISO values available in detail/export.
- No color-only status; include text and icon.

## Offline UX

- Global indicator: online, offline, syncing, attention required.
- A write succeeds locally and shows "Saved on this device — waiting to sync" rather than a false "Saved to cloud".
- Failed sync opens a resolution view with the affected record, error category, retry, and export/diagnostic action.
- Do not block navigation on a background retry.
- Sign-out with unacknowledged writes requires explicit confirmation, matching the Android safety intent.

## Money, dates, and identity

`[PROPOSED]` Use integer minor units for money end-to-end. The Android reference stores `Double`; the desktop should not introduce floating-point calculations in new code. If the shared schema requires numeric, convert at the boundary with explicit rounding rules.

`[PROPOSED]` Use typed date/time values in Go and ISO-8601 at boundaries. Display in IST. Do not sort formatted date strings.

`[PROPOSED]` Use UUIDs for entity IDs and a separate human-facing clinic ID for patients. Never use a display name as a key.

## Accessibility and desktop behavior

- Full keyboard operation for registration, search, vaccination, payment, and receipt.
- Visible focus, semantic labels, error announcements, and minimum contrast.
- Respect OS font scaling and reduced motion.
- Single-instance behavior by default; second launch focuses the existing window.
- Window size/position persisted without PHI.
- No custom title bar content that leaks patient identity.

## Error handling

Use a discriminated result type:
```ts
type Result<T> =
  | { ok: true; value: T }
  | { ok: false; code: string; message: string; retryable: boolean; details?: unknown };
```
`details` must be safe for display. Raw server errors, SQL, tokens, and PHI stay in redacted Go logs.

## Testing

- Component tests for forms, validation, tables, and permission-aware rendering.
- Contract tests for every binding.
- Integration tests against a temporary local SQLite database.
- E2E tests for critical workflows with a fake backend or an approved test harness; a test harness must never become a second production backend.
- Accessibility checks in CI for core screens.

## Open questions

- Which router, form, table, and state libraries are approved?
- Is a design system shared with Android, or is desktop a new visual language?
- Which languages/locales are required?
- Is offline draft recovery required for long consultation notes?
- Is touch-screen use expected at the front desk?

## Related

[[Architecture/System-Architecture|System Architecture]] · [[Architecture/Go-Backend-Architecture|Go Backend Architecture]] · [[Architecture/Error-Handling|Error Handling]] · [[Testing/Test-Strategy|Test Strategy]]
