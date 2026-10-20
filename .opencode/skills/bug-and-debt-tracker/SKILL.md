---
name: bug-and-debt-tracker
description: "Maintain a deduplicated Neo Child Clinic Desktop register of verified defects, risks, technical debt, and unresolved questions. Use to record evidence, severity, impact, reproduction, affected modules, and next actions while separating confirmed defects from suspected issues."
metadata:
  version: "1.0"
  mode: "docs-write-after-approval"
  scope: "neo-child-clinic-desktop"
---

# Bug and Technical-Debt Tracker

Keep one trustworthy register of what is broken, what might be broken, what is structurally costly, and what remains unknown. Do not let duplicates, unverified reports, or fixed-but-unproven items inflate or hide the picture.

## Invoke when

- A defect, risk, debt item, or open question is found during audit, review, testing, or implementation.
- You need to triage a bug report.
- You need to deduplicate or reconcile an existing register.
- You need a summary of open quality risks for a roadmap or release.

Do not use this skill to fix the code or to claim a fix. Hand off remediation to `implementation-planner` and verification to `test-strategy-planner`.

## Inputs

- Existing bug/debt register, audit reports, security findings, test results, and code evidence.
- A candidate report: symptom, reproduction, affected area, environment, and evidence.
- Whether an approved register note may be updated.
- The Android reference register, if cross-referencing an inherited issue.

## Before you start

1. Read the root and nested `AGENTS.md`, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read, the register, the hypotheses/unknowns note, and the documentation maintenance guide.
2. Record the current commit and date.
3. Search for duplicates by symptom, root cause, affected symbol, and reproduction before assigning a new ID.
4. Preserve existing IDs. Never renumber, reuse, or delete an ID, even when an item is fixed or refuted.

## Evidence standard

- `[VERIFIED]` — reproduced, or proven by reading the cited code/schema and tracing the failure path. Cite `path:line` plus the reproduction or static evidence.
- `[INFERENCE]` — a plausible defect or risk derived from cited evidence; label it suspected.
- `[PROPOSED]` — a suggested fix or mitigation; not a confirmed defect.
- `[UNKNOWN]` — not enough evidence. Keep it as a question or suspected issue.

A commit message, issue comment, or prior audit does not prove a fix. A fix requires evidence against the original reproduction. Do not paste secrets or real patient data into the register.

## Procedure

1. **Triage the candidate.** Determine whether it is a `Defect`, `Risk`, `Debt`, or `Question`. A defect has observable wrong behavior; a risk is a possible future harm; debt is a structural cost; a question is unresolved.
2. **Check duplicates.** Search the register and related notes. If duplicate, link the existing ID and add new evidence instead of creating a second item. If the same root cause produces multiple symptoms, keep one canonical item and list the symptoms.
3. **Assign an ID.** Use `BUG-<AREA>-NNN`, `RISK-<AREA>-NNN`, `DEBT-<AREA>-NNN`, or `QUES-<AREA>-NNN`. Areas are three-letter uppercase domains. Never reuse Android `NCC-*` or `NSC-*` IDs; cross-reference them in prose.
4. **Write the card.** Include title, type, status, severity, confidence, affected version/commit, environment, impact, reproduction, evidence, root cause (or hypothesis), affected modules, workaround, suggested next action, regression test, owner, and links.
5. **Set severity.** `Critical` = patient safety, data loss/corruption, financial integrity, auth bypass, or release blocker. `High` = major workflow broken or serious privacy/security exposure. `Medium` = degraded workflow with workaround or material maintainability risk. `Low` = minor UX/code quality. `Info` = observation.
6. **Set confidence and status.** Defect statuses: `Suspected`, `Confirmed`, `Investigating`, `Fixed`, `Verified Fixed`, `Won't Fix`, `Duplicate`, `Refuted`. Risk/debt statuses: `Open`, `Accepted`, `Mitigated`, `Resolved`. A defect becomes `Confirmed` only with a reproduction or a complete static proof; `Verified Fixed` only with evidence against the original reproduction.
7. **Record the fix evidence format.** Example: "Verified Fixed 2026-01-15 — `TestName` fails before the change and passes after; command and output attached." Not acceptable: "fixed in commit abc123."
8. **Reconcile the summary.** Keep counts consistent with detail rows. Do not let a fixed item disappear from history. Note open critical/high items that block a phase or release.
9. **Update links.** Link the item to the relevant feature, requirement, test, architecture note, ADR, or release. If a product decision closes an item as `Won't Fix`, record the decision and owner.
10. **Report changes.** List new IDs, status changes, duplicates merged, and items needing verification.

## Output contract

```markdown
# Bug and Technical-Debt Register — <commit> — <YYYY-MM-DD>

## Summary
| Type | Open | Confirmed | Fixed / Resolved | Accepted | Total |
|---|---|---|---|---|---|

## Register
### BUG-<AREA>-NNN — <title>
- Type: Defect
- Status: Suspected | Confirmed | Investigating | Fixed | Verified Fixed | Won't Fix | Duplicate | Refuted
- Severity: Critical | High | Medium | Low | Info
- Confidence: Confirmed | Probable | Suspected | Unverified
- Affected: version / commit / modules
- Impact:
- Reproduction:
- Evidence:
- Root cause:
- Workaround:
- Suggested next action:
- Regression test:
- Owner:
- Links: REQ / FEAT / TEST / ADR / release

### RISK-<AREA>-NNN — <title>
- Status: Open | Accepted | Mitigated | Resolved
- ...

### DEBT-<AREA>-NNN — <title>
- Status: Open | Accepted | Mitigated | Resolved
- ...

### QUES-<AREA>-NNN — <question>
- Status: Open | Resolved
- ...
```

## Stop conditions

Stop and report when:

- The report cannot be reproduced and static tracing is inconclusive; record it as `Suspected`, not `Confirmed`.
- An existing ID conflicts or would need renumbering.
- The item depends on production data or a live service you cannot safely inspect.
- A requested status change lacks evidence.
- The register is being used to hide or delete historical items.

## Handoff

- `test-strategy-planner` — design the regression or reproduction test.
- `implementation-planner` — sequence approved fixes.
- `security-review` — validate security impact.
- `documentation-sync` — correct stale bug or debt claims.
- `release-documenter` — list known issues and verified fixes.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Do not modify application code, migrations, SQL policies, configuration, or tests.
- Do not mark a defect fixed without evidence against the original reproduction.
- Do not merge distinct root causes into one item or split one root cause into duplicates.
- Do not paste secrets, credentials, or identifiable patient data.
- Preserve IDs, history, and user changes.
