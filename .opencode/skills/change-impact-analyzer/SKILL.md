---
name: change-impact-analyzer
description: "Analyze the impact of a proposed Neo Child Clinic Desktop change across React/TypeScript, Wails contracts, Go services, local storage, Supabase schema and RLS, shared Android compatibility, tests, and documentation. Use before implementation to recommend a minimal safe sequence."
metadata:
  version: "1.0"
  mode: "read-only"
  scope: "neo-child-clinic-desktop"
---

# Change Impact Analyzer

For a proposed change, find everything that can break: callers, contracts, persisted data, RLS, synchronization, Android clients sharing the backend, tests, and documentation. The result is an impact map and a minimal implementation sequence, not an implementation.

## Invoke when

- A feature or bug fix is being considered but not yet approved.
- A schema, RLS, RPC, Wails binding, or shared contract may change.
- You need to know whether a change is additive, breaking, or requires a migration.
- You need a reviewable sequence before handing work to `implementation-planner`.

Do not use this skill to edit code, write migrations, or execute a plan.

## Inputs

- The proposed change, stated as a behavior and acceptance criteria.
- Target `FEAT-<AREA>-NNN`, `REQ-<AREA>-NNN`, or `BUG-<AREA>-NNN` if one exists.
- Desktop root, Supabase artifacts, and optional Android reference root.
- Known constraints: offline support, backward compatibility, release timing, data volume.

## Before you start

1. Read the root and nested `AGENTS.md`, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read and the current architecture, schema, and sync documentation.
2. Record the current commit and Git state.
3. Restate the change in one paragraph and list explicit non-goals. If the intended behavior is ambiguous, stop and ask.
4. Confirm whether the backend is shared with Android. If it is, Android compatibility is in scope even when only desktop changes.

## Evidence standard

- `[VERIFIED]` — current code, schema, test, or configuration proves the dependency. Cite `path:line` or the schema object.
- `[INFERENCE]` — a dependency derived from naming, data shape, or call graph; state the reasoning.
- `[PROPOSED]` — the recommended implementation approach. Never present it as existing behavior.
- `[UNKNOWN]` — cannot be established without a missing repository, live schema, or owner decision.

## Procedure

1. **Locate the current behavior.** Find the implementation of the behavior being changed and every entry point that reaches it. Search by symbol, route, Wails binding, SQL object, and test name.
2. **Map inbound dependencies.** Identify screens, hooks, components, commands, background jobs, and external callers that depend on the current behavior or contract.
3. **Map outbound dependencies.** Identify the Go services, domain rules, repositories, local tables, Supabase tables/RPCs, storage objects, sync descriptors, and Android consumers affected by the change.
4. **Check contract compatibility.** For each Wails binding, JSON payload, Go type, SQL function, table column, enum, or event, state whether the change is additive, behavior-changing, or breaking. Note versioning and mixed-version risks.
5. **Check data and migration impact.** Determine whether existing local rows, remote rows, queued sync operations, backups, or cached values need backfill, transformation, or invalidation. Prefer expand/contract sequencing over destructive changes. Identify rollback limits.
6. **Check authorization and RLS impact.** Identify policies, grants, helper functions, triggers, and service-role paths that must change or be re-tested. A desktop-only UI change can still alter what data is requested.
7. **Check offline and sync impact.** Identify queue format changes, conflict resolution changes, idempotency, tombstones, ordering, clock/timezone assumptions, and behavior for clients that have not updated.
8. **Check tests and observability.** List existing tests that should fail or need updating, missing regression tests, fixtures, RLS tests, and the logs/metrics needed to verify the change.
9. **Check documentation.** Identify notes, ADRs, schema references, API contracts, release notes, and index links that would become stale.
10. **Assess risk.** For each impact, assign `Critical`, `High`, `Medium`, `Low`, or `Info`, with a confidence label. Distinguish confirmed dependencies from suspected ones.
11. **Recommend a minimal sequence.** Order steps to keep the system working at each point: additive schema/contract, compatibility layer, data backfill, behavior switch, cleanup, tests, docs. Include rollback or feature-flag points.
12. **List open decisions.** Do not choose product behavior silently.

## Output contract

```markdown
# Change Impact — <change> — <commit> — <YYYY-MM-DD>

## Proposed change
- Behavior:
- Acceptance criteria:
- Non-goals:
- Shared with Android: yes / no / unknown

## Impact map
| ID | Area | Affected module / object | Change type | Severity | Confidence | Evidence |
|---|---|---|---|---|---|---|

## Contract compatibility
| Contract | Current | Proposed | Additive / Breaking | Consumers | Notes |
|---|---|---|---|---|---|

## Data and migration impact
| Store / object | Impact | Backfill needed | Rollback | Evidence |
|---|---|---|---|---|

## Authorization and RLS impact
## Offline and sync impact
## Test impact
| Test / suite | Why affected | Action |
|---|---|---|

## Documentation impact
| Note / section | Why affected | Action |
|---|---|---|

## Minimal implementation sequence
1. ...
2. ...

## Rollback and recovery
## Open decisions
| QUES | Decision needed | Owner | Blocking? |
|---|---|---|---|
```

Use `IMPACT-<AREA>-NNN` for impact rows, `RISK-<AREA>-NNN` for risks, and `QUES-<AREA>-NNN` for unresolved questions. Do not reuse Android `NCC-*` or `NSC-*` IDs.

## Stop conditions

Stop and report when:

- The proposed behavior or acceptance criteria are ambiguous.
- The current implementation cannot be located.
- The change requires a destructive migration with no rollback or backup plan.
- Shared Android compatibility cannot be assessed because the Android reference or live schema is unavailable.
- The analysis would require modifying code, data, or production configuration.

## Handoff

- `implementation-planner` — convert the sequence into approved tasks.
- `feature-specification` — resolve missing behavior and acceptance criteria.
- `test-strategy-planner` — design regression coverage for the affected areas.
- `api-database-documenter` — update schema and contract documentation after approval.
- `security-review` — review RLS, IPC, or auth changes.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Read-only. Do not edit source, migrations, policies, configuration, tests, or documentation.
- Do not run migrations, backfills, or destructive queries.
- Do not assume a change is safe because it is "only UI"; trace the data and authorization path.
- Preserve existing IDs and user changes; never clean or reset the worktree.
