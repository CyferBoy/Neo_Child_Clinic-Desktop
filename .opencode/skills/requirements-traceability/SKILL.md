---
name: requirements-traceability
description: "Assign stable requirement IDs and link Neo Child Clinic Desktop requirements to specifications, source symbols, tests, and documentation. Use to build a requirements traceability matrix and report requirements without implementation evidence and code without a documented requirement."
metadata:
  version: "1.0"
  mode: "docs-write-after-approval"
  scope: "neo-child-clinic-desktop"
---

# Requirements Traceability

Keep requirements and implementation connected. Every requirement should point to a specification, code, and tests; every significant behavior should point back to a requirement. Report gaps without changing code.

## Invoke when

- A Phase 1 or feature specification is approved.
- You need to know whether a requirement is implemented or tested.
- You need to find undocumented code or orphan requirements.
- Before a release, audit, or implementation plan.

Do not use this skill to test behavior or fix gaps. Hand off to `test-strategy-planner`, `bug-and-debt-tracker`, or `implementation-planner`.

## Inputs

- Approved specifications, roadmap, feature inventory, and acceptance criteria.
- Desktop root and test inventory.
- Existing requirement ID registry or traceability matrix.
- Whether an approved matrix note may be written.

## Before you start

1. Read the root and nested `AGENTS.md`, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read, the documentation index, and any existing requirement registry.
2. Record the commit and date. Traceability is a snapshot, not a permanent truth.
3. Locate all ID sources. Do not create a second ID scheme if one exists; adopt it. If none exists, use the project convention below.
4. Confirm that test results, if referenced, have an observed source. A test file is not a passing test.

## Evidence standard

- `[VERIFIED]` — requirement, implementation symbol, or test exists and was inspected. Cite `path:line` or test name.
- `[INFERENCE]` — a code-to-requirement mapping inferred from naming or behavior; state the reasoning.
- `[PROPOSED]` — a requirement or mapping not yet approved.
- `[UNKNOWN]` — no evidence; state what is missing.

A requirement is not implemented because a document says so. A test proves a check exists, not that it passes.

## Procedure

1. **Build the requirement registry.** Read specs and approved roadmap items. Normalize each requirement to one stable `REQ-<AREA>-NNN`. Preserve existing IDs; never renumber or reuse. Record source, owner, priority, and status.
2. **Build the feature map.** Link each requirement to one or more `FEAT-<AREA>-NNN` entries. Flag requirements with no feature and features with no requirements.
3. **Map implementation.** For each requirement, find the smallest responsible code path: UI action, Wails binding, Go service/use case, domain rule, repository, schema object, or RPC. Cite symbols and paths. If no code path exists, mark `Missing`.
4. **Map tests.** Link existing unit, integration, database/RLS, IPC, UI, sync, and regression tests by exact name/path. If no test exists, mark `Untested`. Do not mark `Tested` unless the test was executed and passed, or label it `Test exists; result unverified`.
5. **Map documentation.** Link specs, architecture notes, ADRs, schema notes, and release notes. Flag claims that describe behavior not covered by a requirement.
6. **Find gaps in both directions.**
   - Requirement without implementation.
   - Requirement without test.
   - Requirement without documentation.
   - Implementation with no documented requirement.
   - Test with no linked requirement.
   - Conflicting or duplicate requirements.
7. **Assess coverage.** Report counts by status and by domain. Do not turn coverage into release approval.
8. **Recommend next actions.** For each gap, recommend `specify`, `implement`, `test`, `document`, `deprecate`, or `investigate`. Do not execute.
9. **Maintain the matrix.** Add rows; never delete historical IDs. Mark superseded requirements with `Deprecated` and link the replacement.

## Output contract

```markdown
# Requirements Traceability — <commit> — <YYYY-MM-DD>

## Scope and sources
- Specifications:
- Roadmap:
- Code roots:
- Test roots:
- Documentation:

## Summary
| Status | Count |
|---|---|
| Proposed | |
| Approved | |
| In Progress | |
| Implemented | |
| Verified | |
| Missing | |
| Untested | |
| Deprecated | |
| Unverified | |

## Traceability matrix
| REQ | Requirement | Priority | FEAT | Specification | Implementation evidence | Test evidence | Documentation | Status |
|---|---|---|---|---|---|---|---|---|

## Requirements without implementation
| REQ | Gap | Expected area | Next action |
|---|---|---|---|

## Implementation without a requirement
| Path / symbol | Behavior | Suggested REQ or deprecation | Evidence |
|---|---|---|---|

## Tests without a requirement
| Test | Covers | Suggested REQ | Evidence |
|---|---|---|---|

## Conflicts and duplicates
| ID | Conflict | Evidence | Decision needed |
|---|---|---|---|

## Coverage by domain
| Domain | Requirements | Implemented | Verified | Missing | Untested |
|---|---|---|---|---|---|

## Recommended next actions
```

Use `REQ-<AREA>-NNN`, `FEAT-<AREA>-NNN`, `TEST-<AREA>-NNN`, `BUG-<AREA>-NNN`, `RISK-<AREA>-NNN`, and `QUES-<AREA>-NNN`. Status values: `Proposed`, `Approved`, `In Progress`, `Implemented`, `Verified`, `Missing`, `Untested`, `Deprecated`, `Unverified`.

## Stop conditions

Stop and report when:

- No approved specification or requirement source exists.
- IDs conflict or an existing registry cannot be reconciled.
- Code or test sources are unavailable.
- A test result is required to determine status but was not observed.
- Mapping would require guessing clinical, financial, or authorization behavior.

## Handoff

- `test-strategy-planner` — close test gaps.
- `documentation-sync` — correct documentation claims.
- `implementation-planner` — plan implementation for missing requirements.
- `bug-and-debt-tracker` — register confirmed defects or debt found while tracing.
- `release-documenter` — confirm only verified requirements are release claims.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Do not modify application code, migrations, SQL policies, configuration, or tests.
- Do not reuse, renumber, or delete requirement IDs.
- Do not claim test coverage or passing status without observed evidence.
- Preserve existing matrices and user changes; add rows and corrections rather than rewriting unrelated content.
