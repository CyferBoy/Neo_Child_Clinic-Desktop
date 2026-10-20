---
name: data-flow-auditor
description: "Trace Neo Child Clinic Desktop data flows from React/TypeScript through Wails and Go to local storage and Supabase, including cache, synchronization, retries, conflicts, and error handling. Use to document observed behavior and find duplicate queries, N+1 requests, and unnecessary data loading."
metadata:
  version: "1.0"
  mode: "read-only"
  scope: "neo-child-clinic-desktop"
---

# Data-Flow Auditor

Trace how data actually moves through the desktop application: frontend action or render, Wails binding, Go handler/service, repository or query, local database/cache, Supabase/Postgres, and the response path back to the UI. Document the observed path, not the intended architecture.

## Invoke when

- A screen is slow, shows stale data, loses writes, or behaves differently offline.
- You need data-flow diagrams, cache strategy, sync design, or error-handling documentation.
- You need to check whether a change affects local storage, Supabase, or synchronization.
- You suspect duplicate requests, N+1 access, or unnecessary payloads.

Do not use this skill to fix a flow or performance issue. Hand off to `performance-auditor`, `bug-and-debt-tracker`, or `implementation-planner`.

## Inputs

- Audit report or a verified map of the project.
- One or more flows to trace, ideally named by `FEAT-<AREA>-NNN` or a user action.
- Desktop root, and optional Supabase project artifacts and Android reference root.
- Whether a flow document may be written to an approved Knowledge Base path.

## Before you start

1. Read the root and nested `AGENTS.md` when present, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read the documentation index.
2. Record the current commit and Git status.
3. Locate the actual frontend entry point, Wails bindings, Go handlers, repositories, local database layer, Supabase client, and synchronization code. Do not assume paths from the intended stack.
4. If Go or frontend sources are absent, stop at the available layer and mark the remainder `Unverified`.

## Evidence standard

- `[VERIFIED]` — observed in source or runtime output with `path:line` or command evidence.
- `[INFERENCE]` — derived from cited code; state the reasoning and the assumptions.
- `[PROPOSED]` — a recommended flow or fix; label it separately.
- `[UNKNOWN]` — not observable. Name the missing source, environment, or runtime fact.

Distinguish **intended behavior** (comments, docs, specifications, product copy) from **observed implementation** (executed code path). Never present one as the other.

## Procedure

1. **Select and bound the flow.** State the trigger, actor, input, expected output, and explicit exclusions. Example: "record a vaccination payment and deduct stock."
2. **Map the forward path.** Trace from the UI event or render to the Wails method, Go handler/service, domain logic, repository, local write, Supabase request/RPC, and response. Record symbols and `path:line`.
3. **Map the return path.** Trace query results, cache reads, state updates, invalidation, refetch, and UI rendering. Note where the UI can show stale or partial data.
4. **Inspect transactions and ordering.** Note transaction boundaries, batching, ordering guarantees, idempotency keys, and whether partial failures can leave local and remote state inconsistent.
5. **Inspect local storage and cache.** For each cache or local table, record key, scope, lifetime/TTL, invalidation, source of truth, encryption, and behavior on logout or account change.
6. **Inspect synchronization.** Record triggers, queue/outbox design, push/pull direction, retry and backoff, conflict detection and resolution, tombstones or absence reconciliation, deletion semantics, clock/timezone assumptions, and recovery after offline startup.
7. **Inspect error handling.** Record where errors are caught, translated, logged, surfaced, retried, or swallowed. Note user-visible states and whether a failed write can be recovered without data loss.
8. **Inspect access efficiency.** Look for duplicate calls on one render, N+1 queries, repeated full-table loads, unbounded lists, over-wide payloads, and avoidable round trips. Label findings `[VERIFIED]` only when the call path is visible; otherwise `[INFERENCE]`. Do not claim a performance regression without measurement; use `performance-auditor` for that.
9. **Draw the flow.** Use one Mermaid `sequenceDiagram` for the normal path and, only if needed, a separate `flowchart` for sync/retry. Mark unverified edges with `⚠️`. Keep one idea per diagram.
10. **Record findings and unknowns.** Use `RISK-<AREA>-NNN` or `BUG-<AREA>-NNN` for actionable findings; cite the exact code path and impact.

## Output contract

```markdown
# Data Flow — <flow name> — <commit> — <YYYY-MM-DD>

## Trigger and expected outcome
## Scope and exclusions
## Observed path
| Step | Layer | Symbol / path:line | Input | Output | Notes |
|---|---|---|---|---|---|

## Diagram
```mermaid
sequenceDiagram
    ...
```

## Local storage and cache
| Store / cache | Key and scope | TTL / invalidation | Encrypted | Source of truth |
|---|---|---|---|---|

## Synchronization and conflict handling
| Concern | Observed behavior | Evidence | Status |
|---|---|---|---|

## Error and recovery behavior
| Failure | Detection | User-visible result | Recovery | Evidence |
|---|---|---|---|---|

## Efficiency observations
| ID | Observation | Evidence | Classification |
|---|---|---|---|

## Intended vs observed
| Claim | Source | Observed implementation | Verdict |
|---|---|---|---|

## Unknowns
```

Use `Current`, `Stale`, `Missing`, `Contradictory`, or `Unverified` when the output is a documentation comparison rather than a code finding.

## Stop conditions

Stop and report when:

- The required layer is absent or inaccessible.
- The flow depends on a live Supabase project, production data, or credentials you do not have.
- A performance claim would require running against production or a shared environment.
- The intended behavior is ambiguous and no product owner or reference behavior resolves it.
- Tracing would require exposing secrets or personal data.

## Handoff

- `architecture-documenter` — place verified flows in the system architecture.
- `api-database-documenter` — document schemas, RPCs, and contracts used by the flow.
- `security-review` — assess auth, RLS, IPC, and local-data boundaries.
- `performance-auditor` — measure suspected inefficiencies.
- `bug-and-debt-tracker` — register confirmed defects and debt.
- `documentation-sync` — reconcile flow docs with code.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Read-only. Do not change code, queries, migrations, cache settings, or configuration.
- Do not run destructive requests, mutate production data, or force sync conflicts to observe behavior.
- Do not infer a database object from a client model; verify it in migrations or the live schema.
- Preserve existing diagrams and notes; add targeted corrections rather than rewriting unrelated content.
