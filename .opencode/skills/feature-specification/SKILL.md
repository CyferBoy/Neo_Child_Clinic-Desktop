---
name: feature-specification
description: "Write detailed Neo Child Clinic Desktop feature specifications covering purpose, users, requirements, workflows, UI states, permissions, data changes, validation, errors, offline behavior, acceptance criteria, and tests. Use for normal, edge, failure, and recovery cases with explicit dependencies and open decisions."
metadata:
  version: "1.0"
  mode: "docs-write-after-approval"
  scope: "neo-child-clinic-desktop"
---

# Feature Specification

Turn an approved feature or parity gap into an implementation-ready specification. Describe intended behavior precisely enough to test, without pretending the feature exists or choosing unresolved product decisions silently.

## Invoke when

- A feature or parity gap is approved for specification.
- A bug fix needs a defined intended behavior and acceptance criteria.
- Implementation planning needs unambiguous requirements and edge cases.
- A feature note must be updated after a product decision.

Do not use this skill to write code, migrations, tests, or implementation tasks. Hand off to `implementation-planner` and `test-strategy-planner`.

## Inputs

- `FEAT-<AREA>-NNN` and its inventory/parity evidence.
- Target phase and `REQ` IDs from the roadmap, if assigned.
- Android reference behavior when parity is in scope.
- Product owner decisions, constraints, and non-goals.
- Whether a specification note may be written and where.

## Before you start

1. Read the root and nested `AGENTS.md`, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read, the feature inventory, roadmap, architecture, schema, and related specs.
2. Record the commit/date and the evidence sources for the intended behavior.
3. Confirm the feature is in scope and the product owner is available for unresolved decisions.
4. If the Android reference is the only source of behavior, describe it as reference input, not as a desktop fact.

## Evidence standard

- `[VERIFIED]` — behavior proven in current desktop implementation or an authoritative source with `path:line`.
- `[REFERENCE]` — verified Android behavior used as parity input. State the Android source path.
- `[PROPOSED]` — intended desktop behavior, requirement, or design. This is the normal state of a new spec.
- `[UNKNOWN]` — undecided or unverified. Record an owner and a decision needed.

Do not invent clinical rules, financial calculations, stock rules, role names, table names, endpoints, or error codes. If a rule is not established, mark it unknown.

## Procedure

1. **Frame the feature.** State purpose, user problem, target users/roles, `FEAT` ID, scope, non-goals, and the phase/requirement links.
2. **Define functional requirements.** Assign stable `REQ-<AREA>-NNN` IDs. Give each a priority (`Must`, `Should`, `Could`, `Won't`), a testable statement, and its evidence/status. Do not reuse IDs.
3. **Describe workflows.** Cover the normal path, alternate paths, edge cases, failure paths, and recovery. Include entry points, preconditions, postconditions, and state transitions.
4. **Define UI states.** Explicitly cover loading, empty, first use, error, offline, partial data, permission denied, long content, success, and destructive confirmation where relevant.
5. **Define permissions.** Map each action to roles and authorization checks. State which checks are UI-only and which must be enforced by Go/Supabase RLS. Do not invent roles.
6. **Define data changes.** List reads/writes, local tables, Supabase tables/RPCs, cache keys, and storage objects. Mark proposed schema changes clearly. Include migration/backfill implications.
7. **Define validation.** Field-level and cross-field rules, ranges, required values, duplicate handling, date/timezone rules, and server-side enforcement. Separate client convenience validation from authoritative validation.
8. **Define domain rules.** For financial features, cover rounding, currency, payments, refunds, discounts, and receipts. For inventory, cover batches, FEFO, expiry, negative stock, partial returns, adjustments, and reconciliation. For reminders, cover schedule calculation, timezone/DST, cancellation, and idempotency. For deletion, cover soft delete, tombstones, and restore.
9. **Define offline and sync behavior.** What works offline, what queues, what is optimistic, what blocks, how conflicts resolve, what happens on retry, and how the user recovers.
10. **Define error handling.** Error classes, user-visible messages, retry policy, logging without sensitive data, and recovery. Avoid silent failure.
11. **Write acceptance criteria.** Use `Given / When / Then` for each `REQ`. Include negative and recovery cases. Make them executable or reviewable.
12. **Define test coverage.** Map requirements to Go unit, React component, integration, database/RLS, IPC, UI, and sync tests. Do not claim tests exist or pass.
13. **List dependencies and open decisions.** Include schema migrations, Android compatibility, shared contracts, design assets, legal/privacy review, and owners.

## Output contract

```markdown
# FEAT-<AREA>-NNN — <Feature> — <status>

## Metadata
- Feature:
- Phase / roadmap:
- Requirements:
- Owner:
- Evidence date / commit:

## Purpose and problem
## Users and roles
## Scope
### In scope
### Non-goals

## Functional requirements
| REQ | Priority | Requirement | Evidence | Status |
|---|---|---|---|---|

## Workflows
### Normal path
### Alternate paths
### Edge cases
### Failure and recovery

## UI states
| State | Expected behavior | Copy / action | Evidence |
|---|---|---|---|

## Permissions
| Action | Role | UI check | Server / RLS check | Evidence |
|---|---|---|---|---|

## Data changes
| Store / object | Read / write | Change | Migration / backfill | Evidence |
|---|---|---|---|---|

## Validation rules
## Domain rules
### Financial
### Inventory
### Reminders / time
### Deletion / restore

## Offline and synchronization behavior
## Error handling and recovery
## Acceptance criteria
### REQ-... 
- Given ...
- When ...
- Then ...

## Test plan
| Requirement | Layer | Test intent | Existing test? |
|---|---|---|---|

## Dependencies
## Open decisions
| QUES | Decision needed | Owner | Blocks implementation? |
|---|---|---|---|

## Evidence and related notes
```

Use `REQ-<AREA>-NNN`, `FEAT-<AREA>-NNN`, `QUES-<AREA>-NNN`, and `TEST-<AREA>-NNN`. Use status values `Proposed`, `Approved`, `In Progress`, `Implemented`, `Verified`, `Deferred`, or `Rejected`.

## Stop conditions

Stop and report when:

- The feature lacks an owner, scope, or acceptance criteria.
- A clinical, financial, inventory, authorization, or deletion rule is unresolved.
- The data model or API contract needed for the spec is unknown.
- The spec would require inventing a table, policy, endpoint, or role.
- The requested behavior conflicts with verified Android compatibility or security constraints.

## Handoff

- `implementation-planner` — convert the approved spec into tasks.
- `test-strategy-planner` — design coverage from the acceptance criteria.
- `requirements-traceability` — link requirements to code and tests.
- `change-impact-analyzer` — assess a proposed schema or contract change.
- `knowledge-base-manager` — index and cross-link the approved note.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Do not modify code, migrations, SQL policies, configuration, or tests.
- Do not present proposed behavior as implemented.
- Do not silently choose product behavior; record open decisions.
- Preserve existing IDs, notes, and user changes.
