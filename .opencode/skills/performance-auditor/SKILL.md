---
name: performance-auditor
description: "Investigate Neo Child Clinic Desktop performance: slow screens, database access, rendering, repeated requests, caching, startup, and synchronization. Use to inspect or measure before making claims and to define measurable acceptance criteria."
metadata:
  version: "1.0"
  mode: "read-only"
  scope: "neo-child-clinic-desktop"
---

# Performance Auditor

Find performance problems with evidence, not intuition. Inspect code paths and, when safe and authorized, measure the actual behavior. Every recommendation should come with a measurable acceptance criterion.

## Invoke when

- A screen, startup, query, search, report, or sync operation feels slow.
- You need to validate a suspected N+1, repeated request, or unnecessary payload.
- You need performance acceptance criteria for a feature or release.
- A cache or synchronization change may affect latency or resource use.

Do not use this skill to optimize code or to run production load tests. Hand off approved changes to `implementation-planner`.

## Inputs

- Scenario, user role, dataset size, and environment.
- Desktop root, query/schema, cache, and sync code.
- Baseline commit/tag and expected behavior.
- Permission to run local benchmarks or profiling. Default: permission denied.
- Whether a report may be written.

## Before you start

1. Read the root and nested `AGENTS.md`, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read and any performance, architecture, and data-flow notes.
2. Record the commit, build type, OS, hardware/VM, dataset, and network conditions. A result without an environment is not comparable.
3. Confirm the test environment. Never measure against production or a shared service without explicit owner approval and a safe plan.
4. Establish a baseline before changing anything. Since this skill is read-only, no optimization is applied here.

## Evidence standard

- `[VERIFIED]` — measured in a stated environment, or directly observed in an executed query/profile. Include the method, sample size, and result.
- `[INFERENCE]` — a likely bottleneck derived from code inspection; state the reasoning and the measurement needed.
- `[PROPOSED]` — a recommended optimization or target; not proof of a problem.
- `[UNKNOWN]` — no safe measurement or environment available.

Do not call something "slow" without a baseline, threshold, or user-reported scenario. Do not call something "fast" without evidence.

## Procedure

1. **Define the scenario.** User action, screen/flow, data volume, role, offline/online state, and expected frequency. Write the user-visible outcome, not just a function name.
2. **Establish a baseline.** Use local profiling, Go benchmarks, frontend performance tooling, query plans, or timing instrumentation as appropriate. Record p50/p95 and the measurement method. If measurement is not possible, say so and rely on code inspection only.
3. **Inspect the render path.** Look for unnecessary re-renders, unstable dependencies, large lists without virtualization, expensive formatting on every render, and blocking work on the UI thread.
4. **Inspect data access.** Look for repeated fetches, N+1 queries, full-table reads, unbounded lists, over-wide payloads, missing pagination, queries without supporting indexes, and chatty Wails/Supabase round trips. Use `EXPLAIN` only on a safe local/staging database.
5. **Inspect caching.** Record cache keys, TTL, invalidation, duplication, stale reads, and whether cache hits avoid work. Do not assume a cache helps without measuring.
6. **Inspect startup.** Trace initialization order, eager work, auth/session restoration, local database opening/migration, sync startup, and update checks. Separate time-to-first-window from time-to-usable.
7. **Inspect synchronization.** Measure push/pull batch sizes, retry storms, repeated reconciliation, conflict resolution cost, and behavior on a large offline backlog. Do not create artificial conflicts against shared data.
8. **Identify bottlenecks.** For each, state the evidence, affected users, expected impact, and confidence. Separate measured bottlenecks from code-smell hypotheses.
9. **Recommend changes.** Prefer the smallest change that addresses the measured cause. Include a measurable acceptance criterion, for example: "p95 search response under 300 ms for 10,000 patients on the reference laptop" or "one query per screen load instead of N+1."
10. **Plan regression measurement.** Define the benchmark, dataset, command, and threshold that would prove the fix and catch regressions.

## Output contract

```markdown
# Performance Audit — <scenario> — <commit> — <YYYY-MM-DD>

## Scenario and environment
- User action:
- Role:
- Build:
- OS / hardware:
- Dataset:
- Network:
- Baseline commit:

## Method
- Measured / inspected:
- Tools:
- Sample size:
- Limitations:

## Baseline measurements
| Metric | p50 | p95 | Max | Method |
|---|---|---|---|---|

## Findings
| ID | Finding | Type (measured / inferred) | Evidence | Impact | Confidence |
|---|---|---|---|---|---|

## Render path
## Data access
## Cache behavior
## Startup
## Synchronization
## Recommendations and acceptance criteria
| Recommendation | Expected effect | Acceptance criterion | Measurement plan |
|---|---|---|---|

## Regression plan
## Unknowns
```

Use `PERF-<AREA>-NNN` for performance findings, `RISK-PERF-NNN` for risks, and `QUES-PERF-NNN` for unknowns. Severity uses `Critical`, `High`, `Medium`, `Low`, `Info`.

## Stop conditions

Stop and report when:

- No safe environment exists for measurement.
- The only available target is production or a shared service.
- The dataset or hardware is not representative and results would be misleading.
- Profiling would require patient data or secrets.
- A performance claim is requested without a baseline or threshold.

## Handoff

- `data-flow-auditor` — trace the full data path behind a bottleneck.
- `implementation-planner` — sequence approved optimizations.
- `test-strategy-planner` — add performance regression checks.
- `bug-and-debt-tracker` — register measured regressions or accepted debt.
- `release-documenter` — include only measured, verified performance changes.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Read-only. Do not modify code, queries, indexes, cache settings, or configuration.
- Do not run stress, saturation, or load tests against shared or production systems.
- Do not present code inspection as a measurement.
- Do not optimize before establishing the baseline.
- Preserve every pre-existing user change; never reset, clean, or rewrite the worktree.
