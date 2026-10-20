---
name: documentation-sync
description: "Compare Neo Child Clinic documentation against current code, schema, configuration, and tests. Use to find stale claims, missing documentation, contradictions, and broken links, produce a discrepancy report first, and update only explicitly approved documentation."
metadata:
  version: "1.0"
  mode: "read-only-until-approved"
  scope: "neo-child-clinic-desktop"
---

# Documentation Sync

Find where documentation and the repository disagree. Produce a discrepancy report with evidence before changing any note. Then, only after explicit approval, apply the smallest targeted edits and validate them.

## Invoke when

- Code, schema, configuration, or release behavior changed and docs may be stale.
- A note makes a claim that needs verification.
- The Knowledge Base has broken links, orphan notes, or contradictory pages.
- Before a release or after a large merge.

Do not use this skill to design missing architecture or write new feature specifications. Use `architecture-documenter` or `feature-specification` for new content.

## Inputs

- Absolute project root and Knowledge Base path.
- Scope: whole vault, changed files, a branch diff, or named notes.
- Baseline commit/tag or diff range.
- Whether edits are approved, and the exact files that may be changed.

## Before you start

1. Read the root and nested `AGENTS.md`, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read, the documentation maintenance guide, the index, and the vault validator instructions.
2. Record the baseline commit, branch, date, and Git status.
3. Establish the comparison set. For a diff-based pass, use the actual changed files; do not scan the entire vault unless requested.
4. If the vault has uncommitted user changes, preserve them and work around them; do not overwrite.

## Evidence standard

- `[VERIFIED]` — the claim and the current source/schema/configuration/test were both inspected. Cite the note location and the code `path:line`.
- `[INFERENCE]` — the discrepancy is derived indirectly; state the reasoning.
- `[PROPOSED]` — a suggested correction, not yet applied.
- `[UNKNOWN]` — the code or environment needed to adjudicate is unavailable.

Documentation is not evidence of implementation. A migration is evidence of schema only for the migration's scope; it does not prove the hosted database has it applied.

## Procedure

1. **Build the documentation inventory.** List notes, their scope, last verified commit/date if stated, and the code areas they claim to describe.
2. **Extract falsifiable claims.** Identify statements about files, symbols, routes, tables, columns, policies, commands, tests, versions, and behavior. Ignore purely aspirational statements that are clearly labelled.
3. **Verify each claim.** Compare with current source, migrations, configuration, tests, and Git history. Record the exact evidence and whether the claim is current, stale, missing, contradictory, or unverified.
4. **Check links and structure.** Resolve wikilinks and relative Markdown links. Check that notes are reachable from the index. Do not use short heading anchors; the project validator may not resolve them. Note orphans without deleting anything.
5. **Check diagrams.** Validate Mermaid fences and labels. Flag diagrams that show proposed or removed components as if they are current.
6. **Produce the discrepancy report first.** Do not edit yet. Group by severity and by note. Include the proposed minimum correction and the evidence needed.
7. **Wait for approval.** The user must approve the exact notes or the report's edit set. Approval to "fix docs" does not authorize a vault-wide rewrite.
8. **Apply targeted edits only.** Preserve tone, structure, and valid links. Update the verification header/date where the vault convention requires it. Do not delete a note to fix an orphan.
9. **Validate.** Run the documented validator (for example, a project script) and report the exact command and observed output. If no validator exists, perform and report a manual link/Mermaid/heading check.
10. **Report the delta.** List changed files, claims resolved, unresolved discrepancies, and any new unknown.

## Output contract

```markdown
# Documentation Sync — <scope> — <commit> — <YYYY-MM-DD>

## Baseline
- Commit / branch:
- Vault:
- Scope:
- Validator:

## Discrepancy report
| ID | Note | Claim | Current evidence | Classification | Severity | Proposed correction |
|---|---|---|---|---|---|---|

## Link and structure report
| Note / link | Problem | Target exists? | Action |
|---|---|---|---|

## Approved edits
- Approved by:
- Files:

## Changes applied
| Path | Change | Evidence |
|---|---|---|

## Validation
- Command:
- Observed result:
- Manual checks:

## Remaining unknowns
```

Use `DOC-<AREA>-NNN` for tracked discrepancies. Classification is exactly one of `Current`, `Stale`, `Missing`, `Contradictory`, `Unverified`, or `Broken link`. Severity uses `Critical`, `High`, `Medium`, `Low`, `Info`.

## Stop conditions

Stop and report when:

- No stable baseline or commit can be established.
- The vault contains conflicts that require a product or architecture decision.
- The proposed fix would require rewriting or reorganizing many notes.
- The validator is unavailable and the user requires automated validation.
- Documentation conflicts with code and the owner cannot say which is authoritative.
- A change would expose secrets or patient data.

## Handoff

- `knowledge-base-manager` — apply approved note and index changes.
- `architecture-documenter` — resolve missing architecture content.
- `api-database-documenter` — resolve schema or policy discrepancies.
- `requirements-traceability` — reconcile requirement coverage.
- `release-documenter` — update release-facing docs from verified changes.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Report before editing. Never change documentation without explicit approval.
- Never rewrite the whole vault, bulk-replace text, or delete notes to silence warnings.
- Never modify application code, migrations, SQL policies, or configuration.
- Do not mark a claim current based on a commit message, issue, or roadmap; verify the source.
