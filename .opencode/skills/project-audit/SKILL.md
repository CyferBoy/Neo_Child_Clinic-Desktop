---
name: project-audit
description: "Audit the Neo Child Clinic Desktop repository before documentation, planning, or implementation. Use for repository structure, dependencies, build configuration, code organization, documentation, Git state, and evidence-backed unknowns; strictly read-only."
metadata:
  version: "1.0"
  mode: "read-only"
  scope: "neo-child-clinic-desktop"
---

# Project Audit

Establish ground truth about the repository before anyone documents, plans, or changes it. An audit is read-only: it records what exists, what does not, and what cannot be verified. It never fixes, reformats, installs, migrates, or cleans anything.

## Invoke when

- Starting work in an unfamiliar checkout or after a large change.
- Before feature inventory, architecture documentation, roadmap, specifications, or implementation planning.
- When a claim about the stack, build, dependencies, tests, or Git state needs evidence.
- When the desktop repository may be confused with the Android reference repository.

Do not use this skill to implement, refactor, or update documentation. Use `documentation-sync` or `knowledge-base-manager` for approved documentation work.

## Inputs

- Absolute path to the project root.
- Optional absolute path to the Android reference repository.
- Audit scope: full repository, or named subsystems.
- Whether a report may be written, and to which approved path. Default: return the report in conversation and write nothing.

## Before you start

1. Read the root and nested `AGENTS.md` when present, plus `opencode.json`/`opencode.jsonc` when present, and any instructions they reference. Project instructions override this skill where they are stricter.
2. Confirm the project root with `pwd`, `git rev-parse --show-toplevel` (if Git), and the location of the expected manifests. If the directory is the Android reference rather than the desktop project, say so and stop the desktop-specific audit.
3. Capture Git state without changing it: `git status --short --branch`, `git diff --stat`, `git diff --cached --stat`, `git ls-files --others --exclude-standard`, `git stash list`, `git log -1 --format='%H%n%ad%n%s' --date=iso-strict`, `git remote -v`, and recent tags. If there is no Git repository, record that fact.
4. Never run `git reset`, `git clean`, `git checkout`, `git restore`, `git stash`, or any command that rewrites user work.

## Evidence standard

- `[VERIFIED]` — directly observed in current source, configuration, Git output, or a command you actually ran. Cite `path:line`, commit SHA, or the exact command and observed result.
- `[INFERENCE]` — a conclusion derived from cited evidence. State the reasoning.
- `[PROPOSED]` — a recommendation or target design. It is not evidence that anything exists.
- `[UNKNOWN]` — evidence is missing or inaccessible. State what would resolve it and who can provide it.

A statement without a citation is a hypothesis, not a finding. Use ISO-8601 dates and UTC timestamps for command results. Do not paste secrets, tokens, keys, or personal data into the report; cite only the file and line where a secret-like value appears.

## Procedure

1. **Record the audit frame.** Date, auditor, absolute root, branch, commit, dirty/clean state, scope, and excluded paths. Note whether the desktop application sources are present.
2. **Map the repository.** List top-level directories and their purpose. Identify application source, generated output, vendored dependencies, migrations, tests, scripts, documentation, CI, packaging, and build artifacts. Do not assume a Go/Wails/React layout; verify it from manifests such as `go.mod`, `wails.json`, `package.json`, `tsconfig.json`, `vite.config.*`, `supabase/config.toml`, and migrations.
3. **Identify entry points and boundaries.** Locate desktop entry point, Wails application setup, frontend mount point, Go service registration, Wails bindings, authentication bootstrap, local database initialization, sync startup, and update mechanism. Record only what is present.
4. **Audit build and release configuration.** Find documented build/test commands in README, `Makefile`, task files, package scripts, CI workflows, and Wails configuration. Note required toolchain versions. If a safe, local, non-destructive command can be run and the user authorized execution, run it once and record the exact command, exit status, and relevant output. Otherwise mark it `[UNKNOWN]` and do not claim it works.
5. **Audit dependencies.** List direct dependencies, versions, lockfiles, and whether they are committed. Note obviously unmaintained, duplicated, or unpinned dependencies only as observations unless a security review establishes impact. Do not run an installer or update a lockfile.
6. **Map code organization.** Summarize frontend, Go backend, shared contracts, domain logic, data access, local storage, Supabase access, synchronization, background jobs, and tests. For each, give representative paths and symbols. Note generated code and do not treat it as hand-written evidence.
7. **Audit documentation.** Find READMEs, `AGENTS.md`, `docs/`, the Knowledge Base, architecture notes, ADRs, and release notes. Record the vault path, index note, frontmatter conventions, link style, and whether a documentation validator exists. Do not edit any note.
8. **Locate the Android reference.** If present, record its absolute path and the directories that define screens, domain logic, Room schema, Supabase migrations, and tests. The Android app is a functional reference, not proof of desktop implementation. If absent, record the limitation.
9. **Assess test posture.** Count test files by layer, identify the commands that run them, and note whether results are recorded. Do not run destructive or environment-dependent tests during an audit; if tests are run with authorization, report only observed output.
10. **Collect findings and unknowns.** Separate verified facts, evidence-backed risks, proposed follow-ups, and missing information. Every finding must identify its evidence, affected module, and impact.
11. **Recommend the next skill.** Choose based on the question: `feature-inventory`, `architecture-documenter`, `data-flow-auditor`, `security-review`, `api-database-documenter`, or `documentation-sync`.

## Output contract

Return an audit report with these sections:

```markdown
# Repository Audit — <project> — <YYYY-MM-DD>

## Frame
- Root:
- Branch / commit:
- Worktree state:
- Scope:
- Excluded:

## Verified facts
| Area | Fact | Evidence |
|---|---|---|

## Repository map
| Path | Purpose | Evidence |
|---|---|---|

## Build, dependencies, and tests
| Item | Observation | Evidence / command | Status |
|---|---|---|---|

## Code map
| Layer | Paths / symbols | Responsibility | Evidence |
|---|---|---|---|

## Documentation and Knowledge Base
- Vault:
- Index:
- Conventions:
- Validator:
- Gaps:

## Android reference
- Location:
- Available sources:
- Not inspected:

## Risks and observations
| ID | Severity | Observation | Evidence | Impact |
|---|---|---|---|---|

## Unknowns
| ID | Unknown | Why it matters | How to resolve |
|---|---|---|---|

## Recommended next action
```

Use `RISK-<AREA>-NNN` for audit risks and `QUES-<AREA>-NNN` for unknowns when an ID helps tracking. Severity is one of `Critical`, `High`, `Medium`, `Low`, `Info`.

## Stop conditions

Stop and report, rather than guessing, when:

- The root is not the desktop project, or the desktop sources are absent.
- The repository contains uncommitted user changes that would be disturbed by a requested command.
- A build or test requires production credentials, live data, network mutations, or writes outside the repository.
- A requested command is destructive or would alter Git state.
- Access is denied or a required toolchain is unavailable.
- A secret or personal data is found; do not copy it. Report its location and recommend rotation or removal through the proper owner.

## Handoff

- `feature-inventory` — classify and compare capabilities.
- `architecture-documenter` — build verified architecture notes and ADRs.
- `data-flow-auditor` — trace frontend-to-database flows.
- `security-review` — assess trust boundaries and RLS.
- `documentation-sync` — reconcile existing docs with current code.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Audit only. Do not modify application code, migrations, SQL policies, configuration, production data, or existing documentation.
- Do not install dependencies, generate lockfiles, apply migrations, or start long-running services unless explicitly authorized and safe.
- Preserve every pre-existing user change. Never clean or reset the worktree.
- Do not claim a fact because a README, issue, roadmap, or prior audit says so. Re-check the current source.
