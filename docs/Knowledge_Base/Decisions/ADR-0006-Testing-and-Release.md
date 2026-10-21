---
title: ADR-0006 Testing and Release
doc_status: proposed
evidence: audit + release risk
updated: 2026-10-21
---

# ADR-0006 — Testing and Release

**Status:** Proposed — awaiting approval.

## Context

The desktop handles PHI, money, and stock. The Android reference has confirmed defects that survived because critical orchestrators and destructive paths lacked tests. The desktop has no test suite or release process yet.

## Decision

Adopt a layered test strategy and evidence-gated release:
- Go domain unit tests and repository integration tests.
- Contract tests for every Wails binding.
- RLS/API tests against the existing Supabase project through an approved non-destructive path.
- React component and E2E tests for critical workflows.
- Sync chaos, backup/restore, print, update, and accessibility gates.
- CI required on every change.
- Signed builds, versioned release feed, rollback artifact, and a completed release checklist.
- No release with an open P0/P1 data-integrity or security finding.

## Alternatives considered

| Alternative | Assessment |
|---|---|
| Manual testing only | Cannot prove replay/RLS/restore safety |
| Unit tests only | Misses integration and destructive paths |
| Test against production | Unacceptable PHI/security risk |
| Unsigned auto-update | Supply-chain risk |
| Release on compile success | Repeats known failure mode |

## Consequences

Positive:
- Evidence for high-risk changes.
- Replay/restore/RLS defects caught before clinic impact.
- Rollback is possible.

Negative / risks:
- Shared-backend verification access and test-data cleanup effort.
- Test maintenance.
- Slower releases, intentionally.

## Validation

- CI blocks on failing P0 tests.
- RLS suite runs with multiple roles.
- Backup restore and update rollback are rehearsed.
- Release checklist has attached evidence and named sign-off.

## Open questions

- Which CI provider?
- Who owns access to the existing Supabase project and its test data?
- Is a separate test harness permitted, or must all verification use the existing project? If permitted, how is it isolated from the desktop backend?
- Which signing/notarization requirements apply per OS?
- What is the pilot rollback window?

## Related

[[Testing/Test-Strategy|Test Strategy]] · [[Testing/Test-Case-Catalog|Test Case Catalog]] · [[Releases/Release-Checklist|Release Checklist]] · [[Decisions/ADR-0010-Backup-and-Restore|ADR-0010]] · [[Roadmap/Phase-1-Implementation-Plan|Phase 1 Plan]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
