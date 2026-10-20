---
name: feature-inventory
description: "Build or refresh the Neo Child Clinic Desktop feature inventory and Android-to-desktop parity matrix. Use to classify features as implemented, partial, missing, broken, deprecated, or unverified and trace them to screens, services, models, database objects, and tests."
metadata:
  version: "1.0"
  mode: "read-only-by-default"
  scope: "neo-child-clinic-desktop"
---

# Feature Inventory

Produce an evidence-backed catalogue of what the desktop application actually does, what it only appears to do, and how it compares with the Android functional reference. A feature is not implemented because a roadmap, issue, or document names it.

## Invoke when

- You need a current feature list before roadmap, specification, or release work.
- You need an Android-to-desktop parity assessment.
- A stakeholder asks "is this already built?" or "what is missing?"
- Documentation and code disagree about feature completeness.

Do not use this skill to write feature specifications or to implement a feature. Hand off to `feature-specification` or `implementation-planner`.

## Inputs

- Audit report from `project-audit`, or permission to perform the minimum audit needed.
- Absolute desktop project root.
- Optional Android reference root.
- Scope: all features, a domain, or named feature IDs.
- Whether an approved inventory note may be written.

## Before you start

1. Read the root and nested `AGENTS.md` when present, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read the current Knowledge Base index.
2. Confirm Git state and the current commit; record it in the inventory header.
3. Confirm which repository is the desktop project and which is the Android reference. Do not blend their evidence.
4. If the desktop source is absent, produce only an Android reference inventory and mark every desktop status `Unverified`; do not infer parity.

## Evidence standard

- `[VERIFIED]` — observed in current source, schema, configuration, or an executed command. Cite `path:line` or command output.
- `[INFERENCE]` — conclusion from cited evidence; explain the reasoning.
- `[PROPOSED]` — intended future feature; never counts as implemented.
- `[UNKNOWN]` — not enough evidence; name the missing source.

Documentation and navigation labels are discovery aids, not implementation proof. A feature is `Implemented` only when the behavior is present in code and has a traceable entry point. A test file proves a test exists, not that it passes.

## Procedure

1. **Collect candidates.** Read navigation/routes, screens, commands, menus, Wails bindings, Go services, React hooks, domain models, migrations, tests, Android screens, and existing feature notes. Record the source of each candidate.
2. **Deduplicate.** Merge synonyms and screen-level variants under one `FEAT-<AREA>-NNN` ID. Do not reuse or renumber an ID. Keep aliases in the row.
3. **Trace each feature.** For the desktop side, identify the UI entry point, frontend state/data path, Wails binding or API contract, Go service/use case, persistence or Supabase object, and tests. For the Android side, identify the screen/ViewModel, repository/use case, Room entity/DAO, Supabase object, and tests.
4. **Classify status.** Use exactly one:
   - `Implemented` — behavior exists end to end and evidence covers the main path.
   - `Partial` — some paths exist, but a named part is missing or unverified.
   - `Missing` — no implementation evidence in the current repository.
   - `Broken` — implementation exists but a confirmed defect prevents the intended behavior.
   - `Deprecated` — implementation exists but is intentionally superseded or slated for removal.
   - `Unverified` — candidates exist but evidence is insufficient or inaccessible.
5. **Assess parity.** Compare desktop behavior with the Android reference using:
   - `Full` — desktop behavior matches the reference for the stated scope.
   - `Partial` — some behavior matches, with named gaps.
   - `Gap` — reference behavior is absent or materially different.
   - `Desktop-only` — a desktop capability with no Android counterpart.
   - `Unknown` — the reference or desktop evidence is unavailable.
6. **Record evidence quality.** For each row, state `Verified`, `Inferred`, or `Unknown`; do not hide a weak trace behind a confident status.
7. **Summarize counts.** Total features by status, parity gaps by domain, and the highest-risk missing capabilities. Do not turn counts into delivery dates.
8. **Identify unknowns.** List unresolved questions such as missing Android source, inaccessible Supabase project, or a screen that exists but has no reachable route.

## Output contract

Create or update the feature inventory with this structure:

```markdown
# Feature Inventory — <commit> — <YYYY-MM-DD>

## Scope and method
- Desktop root:
- Android reference:
- Sources inspected:
- Exclusions:

## Summary
| Status | Count |
|---|---|
| Implemented | |
| Partial | |
| Missing | |
| Broken | |
| Deprecated | |
| Unverified | |

## Feature catalogue
| ID | Feature | Domain | Status | Desktop evidence | Android counterpart | Parity | Tests | Confidence |
|---|---|---|---|---|---|---|---|---|

## Parity gaps
| FEAT | Gap | Impact | Evidence | Suggested next skill |
|---|---|---|---|---|

## Unknowns
| QUES | Unknown | Why it matters | How to resolve |
|---|---|---|---|

## Evidence appendix
- Source roots:
- Commands run:
```

The companion Android-to-desktop parity matrix uses the same `FEAT` IDs and the parity values above. Do not create separate IDs for the same feature.

## Stop conditions

Stop and report when:

- The desktop and Android repositories cannot be distinguished.
- The desktop source is absent, making desktop classification impossible.
- A feature's intended behavior depends on an unavailable Android reference or live Supabase project.
- The requested scope would require reading production data or secrets.
- A feature's status depends on whether a test passes; run it only if authorized, and otherwise mark it `Unverified`.

## Handoff

- `feature-specification` — turn selected features into detailed specs.
- `product-roadmap` — prioritize parity gaps and desktop-specific work.
- `requirements-traceability` — link feature requirements to code and tests.
- `documentation-sync` — reconcile stale feature claims.
- `bug-and-debt-tracker` — record confirmed broken behavior separately.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Do not modify application code, migrations, SQL, configuration, or tests.
- Do not mark a feature complete because a document, commit message, or issue says so.
- Do not invent Android behavior. If the reference is unavailable, say so.
- Preserve existing feature IDs and notes; add rows rather than rewriting unrelated content.
