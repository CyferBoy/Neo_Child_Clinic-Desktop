---
name: release-documenter
description: "Prepare Neo Child Clinic Desktop changelogs, release notes, version checklists, migration notes, known issues, and release verification plans from Git history and verified implementation evidence. Use to ensure no unimplemented or unverified feature is claimed as released."
metadata:
  version: "1.0"
  mode: "docs-write-after-approval"
  scope: "neo-child-clinic-desktop"
---

# Release Documenter

Produce release documentation that a maintainer can defend: what changed, what was verified, what must be checked before shipping, what could break, and what remains known-broken. Git history is a starting point, not proof of user-visible behavior.

## Invoke when

- Preparing a version, tag, or release candidate.
- Writing or updating a changelog or user-facing release notes.
- Building a release checklist, migration note, or known-issues section.
- Auditing whether a claimed feature is actually in a release.

Do not use this skill to tag, publish, sign, deploy, or modify application code. Hand off operational release actions to the maintainer.

## Inputs

- Target version and the exact commit/tag range.
- Git history and merged pull requests for the range.
- Roadmap, feature inventory, requirements traceability, bug/debt register, and test strategy.
- Migration list, release checklist, and known issues.
- Whether release notes may be written and where.

## Before you start

1. Read the root and nested `AGENTS.md`, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read, the release checklist, changelog conventions, and previous release notes.
2. Record the target commit, previous release tag, branch, and date.
3. Confirm the version number from the actual project manifest or release process. Do not invent it.
4. Confirm which environments were used for verification. Do not imply a hosted migration or production test occurred without evidence.

## Evidence standard

- `[VERIFIED]` — a change is present in the release range and its behavior is supported by code plus an observed test/check, or an owner-confirmed release fact.
- `[INFERENCE]` — a user-facing description derived from the diff or code; label it and avoid overstating.
- `[PROPOSED]` — a planned release item or note; not released.
- `[UNKNOWN]` — no evidence or no observed verification.

A merged commit does not automatically mean a feature is complete, enabled, or safe to announce. Do not claim unimplemented, unverified, or behind-a-flag behavior as released.

## Procedure

1. **Establish the release range.** List commits between the previous tag and the target commit. Include merge commits only for context; inspect the actual changes.
2. **Classify changes.** Group into features, fixes, security, performance, database/migrations, documentation, and maintenance. Link each item to `FEAT`, `BUG`, `REQ`, or `ADR` where available.
3. **Verify claims.** For each user-visible item, inspect the code and the verification evidence. If a test was run, record the command and observed result. If not, mark the item `Unverified` and keep it out of release claims.
4. **Write the changelog.** Use a consistent format such as Keep a Changelog: Added, Changed, Fixed, Security, Deprecated, Removed. Include only items in the release range. Do not include internal speculation.
5. **Write release notes for users.** Explain outcomes, not internal file names. Note behavior changes, required actions, compatibility with Android/shared backend, and known limitations.
6. **Write migration notes.** List schema/RLS/RPC/storage changes, ordering, backfill, rollback, and client compatibility. Never state that a migration was applied unless observed.
7. **Build the release checklist.** Cover version manifest, build reproducibility, tests, database migrations, RLS verification, signing, installer/update channel, backup/restore, docs, known issues, and rollback. Mark each item `Not Run`, `Passed`, `Failed`, `Blocked`, or `Not Applicable` only from observed evidence.
8. **List known issues.** Pull open confirmed defects, accepted risks, and limitations from the register. Separate release blockers from acceptable known issues.
9. **Write the verification plan.** Define exact commands/checks and the expected result. Do not execute unless authorized.
10. **Set release status.** `Draft`, `Ready`, `Released`, or `Blocked`. Only a human owner can authorize `Released`.

## Output contract

```markdown
# Release <version> — <commit/tag> — <YYYY-MM-DD>

## Status
- Status: Draft | Ready | Released | Blocked
- Previous release:
- Target commit:
- Owner:

## Changelog
### Added
### Changed
### Fixed
### Security
### Deprecated
### Removed

## User-facing release notes
## Compatibility
- Desktop:
- Android / shared backend:
- Database / migrations:

## Migration notes
| Object | Change | Order | Backfill | Rollback | Applied? |
|---|---|---|---|---|---|

## Release checklist
| Check | Command / method | Expected | Observed | Status |
|---|---|---|---|---|

## Known issues
| ID | Severity | Issue | Impact | Workaround |
|---|---|---|---|---|

## Verification plan
| Check | Method | Required? | Evidence |
|---|---|---|---|

## Rollback plan
## Open questions
```

Statuses: `Draft`, `Ready`, `Released`, `Blocked`. Verification statuses: `Not Run`, `Passed`, `Failed`, `Blocked`, `Not Applicable`. Use `REL-<version>` for the release record if needed.

## Stop conditions

Stop and report when:

- The version or tag range is unclear.
- The working tree contains uncommitted changes that are not part of the release.
- A release claim has no implementation or verification evidence.
- Migrations or RLS changes have not been reviewed.
- Signing, update, or migration steps cannot be verified.
- A human owner has not authorized the release status.

## Handoff

- `documentation-sync` — reconcile release docs with code after publication.
- `bug-and-debt-tracker` — confirm known issues and blockers.
- `test-strategy-planner` — execute the verification plan when authorized.
- `knowledge-base-manager` — index the release note and update cross-links.
- `implementation-planner` — address release blockers.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Do not tag, sign, publish, deploy, or modify application code, migrations, SQL policies, or configuration.
- Do not claim a feature is released because it is merged, planned, or documented.
- Do not invent dates, version numbers, test results, or migration status.
- Do not include secrets, credentials, or real patient data in release notes.
- Preserve prior release notes; append or correct with evidence.
