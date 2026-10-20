---
name: product-roadmap
description: "Maintain the Neo Child Clinic Desktop product vision, scope, phased roadmap, milestones, dependencies, priorities, risks, and acceptance criteria. Use to separate verified Android functionality, required desktop parity, desktop-specific improvements, and future ideas without inventing dates or completion."
metadata:
  version: "1.0"
  mode: "docs-write-after-approval"
  scope: "neo-child-clinic-desktop"
---

# Product Roadmap

Turn verified feature and defect evidence into a prioritised, honest roadmap. The roadmap describes intended outcomes and constraints; it does not assert that anything is built, and it does not invent delivery dates.

## Invoke when

- You need a product vision, scope, release phases, or Phase 1 requirements.
- You need to prioritise parity work against desktop-specific improvements and future ideas.
- Stakeholders need a dependency-aware sequence without fabricated estimates.
- A roadmap claim must be checked against implementation evidence.

Do not use this skill to write detailed feature behavior; use `feature-specification`. Do not use it to schedule implementation tasks; use `implementation-planner`.

## Inputs

- Feature inventory and Android-to-desktop parity matrix.
- Bug and technical-debt register, security findings, and architecture constraints.
- Stakeholder priorities and any real deadlines or release constraints.
- Desktop root and optional Android reference root.
- Whether an approved roadmap note may be written.

## Before you start

1. Read the root and nested `AGENTS.md`, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read, the product/KB index, and any existing vision or roadmap notes.
2. Record the evidence date and commit. A roadmap built on stale inventory is marked as such.
3. Identify who owns product priority. If no owner is available, mark prioritisation as `[UNKNOWN]` rather than inventing it.
4. Do not reuse Android roadmap stages as desktop commitments. They are reference material only.

## Evidence standard

- `[VERIFIED]` — capability or constraint proven by current implementation evidence or an owner decision.
- `[INFERENCE]` — a dependency or priority derived from cited evidence; state the reasoning.
- `[PROPOSED]` — a recommended phase, scope, or priority. This is the normal status for roadmap items.
- `[UNKNOWN]` — missing owner input, effort data, or implementation evidence.

Completion requires implementation evidence. A checked roadmap item without a code/test citation is a documentation defect.

## Procedure

1. **State the vision and scope.** One paragraph on the product's purpose, the clinical/financial outcomes it must protect, the users it serves, and explicit non-goals. Separate verified facts from proposed direction.
2. **Classify the work.** Use four buckets:
   - `Android reference` — behavior verified in the Android app, used as input.
   - `Desktop parity` — required to match the reference on desktop; still proposed until built.
   - `Desktop-specific` — improvements or capabilities that only make sense on desktop.
   - `Future / exploratory` — not committed; may be rejected.
3. **Define phases.** Use phases or releases, not calendar promises. A typical shape is discovery/foundation, parity-critical, operational completeness, hardening, and future work. Adapt to evidence; do not copy a template blindly.
4. **Prioritise explicitly.** Rank by patient safety, financial and inventory integrity, security/privacy, data-loss risk, workflow blocking, dependency order, and user impact. If effort is unknown, say so. Never invent story points or dates.
5. **Define Phase 1 requirements.** For the first phase, list `REQ-<AREA>-NNN` requirements with priority (`Must`, `Should`, `Could`, `Won't`), acceptance criteria, dependencies, and evidence status. Link each to a `FEAT` and, where relevant, a `BUG` or `RISK`.
6. **Map milestones and acceptance.** A milestone is a verifiable outcome, not a date. State the evidence that would prove it: a passing test, a verified flow, an RLS check, a migration applied in a safe environment, or an approved document.
7. **Record dependencies and risks.** Include shared-backend compatibility with Android, schema migrations, auth/RLS, offline sync, update/release infrastructure, and missing reference sources.
8. **Maintain status.** Use `Proposed`, `Approved`, `In Progress`, `Implemented`, `Verified`, `Deferred`, or `Rejected`. Do not mark `Implemented` without implementation evidence; do not mark `Verified` without observed verification.
9. **Reconcile with the inventory.** Every roadmap item links to a feature or explicitly states why it is new. Every critical parity gap should appear in a phase or be explicitly deferred with a reason.

## Output contract

```markdown
# Product Roadmap — <commit> — <YYYY-MM-DD>

## Vision
## Scope
### In scope
### Non-goals
## Users and outcomes
## Evidence base
- Feature inventory:
- Parity matrix:
- Bug/debt register:
- Security review:

## Classification
| FEAT | Capability | Android reference | Desktop parity | Desktop-specific | Future | Status | Evidence |
|---|---|---|---|---|---|---|---|

## Phases
### Phase 1 — <outcome>
| REQ | Requirement | Priority | FEAT | Dependencies | Acceptance evidence | Status |
|---|---|---|---|---|---|---|

### Phase 2 — <outcome>
...

## Milestones
| Milestone | Verifiable outcome | Depends on | Status |
|---|---|---|---|

## Prioritisation rationale
## Risks and dependencies
| RISK | Risk | Impact | Mitigation | Owner |
|---|---|---|---|---|

## Deferred / rejected
| Item | Reason | Revisit condition |
|---|---|---|

## Open decisions
```

Use `REQ-<AREA>-NNN` for requirements, `FEAT-<AREA>-NNN` for features, `RISK-<AREA>-NNN` for risks, and `QUES-<AREA>-NNN` for open questions. No dates or estimates unless supplied by an accountable owner and labelled as a constraint, not a forecast.

## Stop conditions

Stop and report when:

- The feature inventory or parity matrix is missing or stale.
- No product owner can confirm priorities or scope.
- A requested date or estimate has no stated basis.
- Roadmap items conflict with verified architecture, security, or shared-backend constraints.
- Marking an item complete would require evidence that does not exist.

## Handoff

- `feature-specification` — specify approved Phase 1 features.
- `requirements-traceability` — link roadmap requirements to code, tests, and docs.
- `implementation-planner` — sequence approved work.
- `release-documenter` — produce release notes only from verified delivery.
- `bug-and-debt-tracker` — register risks that block a phase.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Do not invent delivery dates, estimates, completed milestones, or stakeholder priorities.
- Do not present Android functionality as desktop functionality.
- Do not modify application code, migrations, SQL policies, or configuration.
- Preserve existing roadmap notes; make targeted, evidence-backed changes.
