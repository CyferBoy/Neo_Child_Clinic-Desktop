---
name: implementation-planner
description: "Convert an approved Neo Child Clinic Desktop feature specification into small, ordered, reviewable implementation tasks. Use after explicit approval to plan dependencies, affected files and modules, database changes, tests, rollback, and documentation updates without executing the plan."
metadata:
  version: "1.0"
  mode: "planning-only"
  scope: "neo-child-clinic-desktop"
---

# Implementation Planner

Turn an approved specification into a plan a reviewer can trust: small tasks, explicit dependencies, safe migration order, test gates, rollback, and documentation updates. The plan is not permission to implement.

## Invoke when

- A feature specification and its requirements are approved.
- A confirmed defect has an approved fix scope.
- A schema or contract change has passed impact analysis.
- You need a reviewable sequence before any code changes.

Do not use this skill if the specification is still `Proposed`, if key decisions are unresolved, or if the user has not approved implementation. Do not write code, migrations, or tests while planning.

## Inputs

- Approved `FEAT-<AREA>-NNN` specification and `REQ-<AREA>-NNN` requirements.
- Change-impact report, architecture, schema, and data-flow notes.
- Test strategy and bug/debt register.
- Repository root, current commit, and known constraints.
- Explicit approval boundary: planning only, or planning plus later execution.

## Before you start

1. Read the root and nested `AGENTS.md`, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read, the spec, the impact analysis, and the existing implementation.
2. Record the commit and date.
3. Confirm the spec status is `Approved` and all blocking `QUES` items are resolved. If not, stop.
4. Confirm the write scope: no application code should be changed during planning.

## Evidence standard

- `[VERIFIED]` — an affected file, symbol, schema object, or test exists. Cite it.
- `[INFERENCE]` — an expected touch point derived from the code map; mark it for confirmation during implementation.
- `[PROPOSED]` — the task, sequence, or design. This is the normal state of a plan.
- `[UNKNOWN]` — missing decision or evidence; make it a blocking task or question.

## Procedure

1. **Restate the approved outcome.** Include the feature, scope, non-goals, acceptance criteria, and explicit constraints. If the spec and impact analysis disagree, stop.
2. **Choose a delivery shape.** Prefer vertical slices that deliver testable behavior, or a safe expand/contract sequence for shared schema changes. Avoid a big-bang cutover.
3. **Decompose into small tasks.** Each task should be reviewable on its own, have one primary purpose, and leave the system working. Use `TASK-<AREA>-NNN`.
4. **For each task, record:**
   - Goal and acceptance evidence.
   - Dependencies and blockers.
   - Expected files/modules/symbols (verify during implementation; do not guess silently).
   - Contracts, schema, RLS, migration, or sync changes.
   - Tests to add or update.
   - Documentation to update.
   - Rollback or feature-flag plan.
   - Estimated risk, not invented effort.
5. **Order safely.** Typical order: additive schema/contract, compatibility layer, backend/domain logic, Wails binding, frontend integration, migration/backfill, switch behavior, tests, docs, cleanup. Adapt to the impact analysis.
6. **Plan data safety.** Back up or export before destructive changes; use expand/contract; preserve Android compatibility when the backend is shared; define how to recover from a failed backfill or sync queue.
7. **Plan verification gates.** Each task needs a gate: unit test, integration test, RLS test, IPC contract test, UI test, sync test, manual check, or documentation validation. State what must be observed before the next task.
8. **Plan documentation.** Identify the spec, architecture, schema, ADR, index, release note, and traceability updates.
9. **Review the whole plan.** Check for missing tasks, circular dependencies, unowned decisions, and verification gaps. Confirm no task silently includes unrelated refactoring.
10. **Stop at the approval gate.** Present the plan and ask for explicit approval before execution. Do not start task one.

## Output contract

```markdown
# Implementation Plan — FEAT-<AREA>-NNN — <commit> — <YYYY-MM-DD>

## Approval
- Spec status:
- Approved by:
- Scope:
- Non-goals:
- Execution authorized: no

## Outcome and acceptance criteria
## Constraints and assumptions
## Task sequence
| TASK | Goal | Depends on | Files / modules | Data / schema | Tests | Docs | Rollback | Risk |
|---|---|---|---|---|---|---|---|---|

## Detailed tasks
### TASK-<AREA>-NNN — <title>
- Goal:
- Acceptance evidence:
- Dependencies:
- Expected touch points:
- Data / migration:
- Tests:
- Documentation:
- Rollback:
- Risks / unknowns:

## Database and migration plan
## Contract and compatibility plan
## Test and verification gates
## Documentation updates
## Rollback and recovery
## Open decisions
| QUES | Decision | Owner | Blocking? |
|---|---|---|---|

## Execution checklist (not yet run)
- [ ] Approval recorded
- [ ] Branch/worktree confirmed
- [ ] Baseline tests observed
- [ ] Migration/backup plan approved
- [ ] ...
```

Use `TASK-<AREA>-NNN` for tasks, `REQ-<AREA>-NNN`/`FEAT-<AREA>-NNN` for links, and `RISK-<AREA>-NNN` for risks.

## Stop conditions

Stop and report when:

- The specification is not approved or has unresolved blocking decisions.
- The impact analysis is missing for a schema, RLS, IPC, or sync change.
- A task would require a destructive migration without a backup and rollback plan.
- The change would break Android compatibility and no compatibility plan exists.
- Execution approval has not been given.
- The plan would require modifying unrelated code or user changes.

## Handoff

- `test-strategy-planner` — finalize the test matrix and regression checks.
- `change-impact-analyzer` — resolve newly discovered impact.
- `release-documenter` — prepare release notes after verified delivery.
- `documentation-sync` — update docs after implementation evidence exists.
- `bug-and-debt-tracker` — register issues found during planning.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Do not implement, edit source, create migrations, change SQL policies, or run tests as part of planning.
- Do not invent estimates, dates, or completed tasks.
- Do not hide unresolved decisions inside a task description.
- Preserve user changes and the existing Git state.
