---
name: test-strategy-planner
description: "Plan Go unit, React/TypeScript, integration, database/RLS, Wails IPC, UI, synchronization, and regression tests for Neo Child Clinic Desktop. Use to cover financial calculations, inventory reconciliation, partial returns, reminders, soft deletion, timezones, offline recovery, and authorization without claiming unobserved results."
metadata:
  version: "1.0"
  mode: "read-only-planning"
  scope: "neo-child-clinic-desktop"
---

# Test Strategy Planner

Plan how the desktop application will be proven correct, layer by layer, with special attention to clinical, inventory, financial, reminder, synchronization, and authorization behavior. A plan is not a test result.

## Invoke when

- A feature specification or implementation plan needs test coverage.
- A defect needs a regression test.
- You need a testing strategy, test matrix, environment plan, or release verification plan.
- Existing tests do not cover a high-risk path.

Do not use this skill to write production code or to assert that a test passed. Test execution is a separate, explicitly authorized action.

## Inputs

- Approved specifications, acceptance criteria, and `REQ`/`FEAT` IDs.
- Architecture, data-flow, schema, and security notes.
- Bug/debt register and requirements traceability matrix.
- Desktop root, test directories, build files, and CI configuration.
- Available environments: local, local Supabase, staging. Never assume production access.

## Before you start

1. Read the root and nested `AGENTS.md` when present, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read the test conventions and existing test layout.
2. Record the commit and date.
3. Discover the actual test commands from build files, package scripts, `Makefile`, CI, README, or Wails configuration. Do not invent commands.
4. Inspect what already exists before proposing new suites. Do not duplicate an existing test under a new name.

## Evidence standard

- `[VERIFIED]` — a test file, command, or observed result was inspected. Cite `path:line` or the exact command/output.
- `[INFERENCE]` — a coverage gap or risk derived from cited code; state the reasoning.
- `[PROPOSED]` — a planned test or acceptance criterion.
- `[UNKNOWN]` — environment, fixture, or result unavailable.

Never write "passing", "green", or "verified" unless you executed the test and observed the result. Report the command, environment, timestamp, and relevant output. A test that was skipped, not run, or blocked is not a pass.

## Procedure

1. **Map risks to layers.** For each requirement or confirmed defect, decide the cheapest layer that can prove it: Go unit/domain, React component/hook, Wails IPC contract, integration with a real local database, Supabase/Postgres/RLS, UI end-to-end, sync/offline, or regression.
2. **Inventory existing tests.** List suites, test names, layer, fixtures, and known gaps. Link tests to requirements. Do not count a test as coverage if it asserts nothing meaningful.
3. **Design the test matrix.** For each `TEST-<AREA>-NNN`, record the requirement, layer, setup, action, oracle, environment, data, priority, and whether it is new or existing.
4. **Cover critical domains explicitly.**
   - **Financial:** rounding, currency, discounts, payments, refunds, partial returns, receipts, idempotency, and reconciliation.
   - **Inventory:** batch selection/FEFO, expiry, stock deduction, negative-stock guard, adjustments, partial returns, waste, and ledger-versus-shelf reconciliation.
   - **Vaccination reminders:** schedule calculation, multiple doses, cancellation, timezone/DST, duplicate suppression, retry, and notification permission behavior.
   - **Deletion:** soft delete, tombstones or absence reconciliation, restore, and exclusion from lists, statistics, and sync.
   - **Synchronization:** offline write, queue ordering, retry/backoff, conflict resolution, duplicate delivery, interrupted sync, and recovery after restart.
   - **Authorization:** role matrix, UI guard versus server enforcement, RLS for each operation, `SECURITY DEFINER` functions, storage policies, and Wails IPC argument validation.
   - **Time:** UTC storage versus local display, date-only vaccination dates, clinic timezone, DST boundaries, and clock skew.
5. **Design test data and fixtures.** Include multi-tenant/clinic isolation, multiple roles, expired and near-expiry batches, partial payments, duplicate patients, and concurrent edits. Keep fixtures synthetic and free of real patient data.
6. **Define environments.** Local unit tests, isolated local database, local Supabase stack, staging. State what each can and cannot prove. Never plan destructive tests against production.
7. **Plan regression coverage.** Every confirmed defect gets a test that fails against the original reproduction and passes after the fix. Record the exact reproduction and oracle.
8. **Plan execution and evidence.** List commands, order, expected artifacts, and who may run them. Mark execution unauthorized until approved.
9. **Report gaps.** Separate missing tests, weak oracles, flaky tests, untestable code, and environment blockers. Recommend refactoring only as a proposal.

## Output contract

```markdown
# Test Strategy — <scope> — <commit> — <YYYY-MM-DD>

## Scope and risk summary
## Existing coverage
| Suite / test | Layer | Requirements | Evidence | Assessment |
|---|---|---|---|---|

## Test matrix
| TEST | Requirement | Layer | Scenario | Oracle | Environment | Priority | New / existing |
|---|---|---|---|---|---|---|---|

## Critical-domain coverage
### Financial
### Inventory and partial returns
### Reminders and time
### Deletion and restore
### Offline and synchronization
### Authorization and RLS
### Wails IPC

## Test data and fixtures
## Environments and commands
| Environment | Command | Proves | Limits |
|---|---|---|---|

## Regression plan
| BUG | Reproduction | Regression test | Expected failure / pass evidence |
|---|---|---|---|

## Execution record
| TEST | Command | Environment | Result | Observed output |
|---|---|---|---|---|

## Gaps and blockers
```

Use `TEST-<AREA>-NNN` for planned or existing tests and `REQ-<AREA>-NNN`/`BUG-<AREA>-NNN` for links. Status values: `Planned`, `Existing`, `Blocked`, `Passed`, `Failed`, `Skipped`, `Not Run`, `Unverified`. Only `Passed` or `Failed` may be used after observed execution.

## Stop conditions

Stop and report when:

- No test command can be discovered.
- The required environment is unavailable or would require production access.
- A test would mutate shared data or require real patient data.
- The acceptance criteria are too vague to define an oracle.
- A test result is requested but execution was not authorized or observed.

## Handoff

- `implementation-planner` — add test tasks to the approved plan.
- `bug-and-debt-tracker` — register defects found during test design or execution.
- `requirements-traceability` — link tests to requirements.
- `release-documenter` — record only observed verification.
- `performance-auditor` — add measurable performance tests where relevant.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Do not write production code, migrations, or tests unless the task explicitly authorizes test-file changes.
- Do not run destructive, load, or production tests.
- Do not fabricate pass/fail results or coverage percentages.
- Preserve user changes and existing tests; add rather than overwrite, unless a replacement is approved.
