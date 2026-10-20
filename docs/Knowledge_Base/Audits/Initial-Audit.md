---
title: Initial Audit
doc_status: baseline
evidence: filesystem + Android repository + Android KB + two supplied CSV snapshots + shared-backend investigation
updated: 2026-10-20
---

# Initial Audit

> **Audit date:** 2026-10-20. **Desktop source:** absent. **Application source changes:** none. This audit is read-only with respect to application code.

## Scope

- Desktop project at `/storage/emulated/0/Neo_Child_Clinic_Desktop`.
- Android reference at `/data/data/com.termux/files/home/Neo_Child_Clinic` (`main`, `ca4bed4`, clean worktree, 583 tracked files).
- Existing Android Knowledge Base (37 Markdown notes).
- Supabase migrations (23 SQL files) and two public column snapshots: the desktop CSV (24 tables, 416 columns) and the older tracked Android-repo CSV (23 tables, 361 columns). Neither contains connection, auth, policy, or credential fields.
- Installed OpenCode skills (17 `SKILL.md` files).
- Existing configuration, tests, and documentation conventions.

## Method

1. Enumerated files, Git state, branches, and documentation.
2. Searched for Go, Wails, React, TypeScript, package, test, and CI files in both project locations.
3. Read Android source for roles, auth, patient/vaccination/inventory/finance/reminder/sync/backup flows.
4. Read the existing KB's verified notes and confirmed findings.
5. Parsed both supplied table-column CSV snapshots and compared them with migration SQL and Android source.
6. Checked the Android repo's test file counts and migration counts.
7. Did not run the Android app, Gradle tests, live Supabase queries, or any desktop build.

## Verified environment facts

| Fact | Value |
|---|---|
| Desktop project files | 17 skills + 1 user CSV; no app source |
| Desktop Git repository | None |
| Desktop `AGENTS.md` | None |
| Android branch / HEAD | `main` / `ca4bed406bfd246ad83878fff9a4e178ebc5670f` |
| Android worktree | Clean, 583 tracked files |
| Android main Kotlin files | 352 |
| Android unit test files | 41 |
| Android instrumented test files | 8 |
| Supabase migrations | 23 SQL files |
| Existing Android KB notes | 37 Markdown files |
| Desktop column snapshot (user-supplied) | 24 tables, 416 columns |
| Android KB validator | Existing script; not re-run before writing this note |
| Live Supabase access | Not available |
| Desktop tests run | 0 (no suite) |
| Android tests run | 0 in this pass |

## Findings

| ID | Severity | Finding | Evidence | Disposition |
|---|---|---|---|---|
| AUD-001 | **Blocker** | No desktop implementation exists | Filesystem search found only skills and CSV | Document as Missing; do not fabricate parity |
| AUD-002 | **High** | Desktop project is not a Git repository and has no `AGENTS.md` | `.git` absent; no instruction file | Establish before code; no source changes in this pass |
| AUD-003 | **High** | Live Supabase schema, grants, policies, and data are unavailable | No project credentials/connection | Mark live claims `[UNKNOWN]`; require verification gate |
| AUD-004 | **High** | Repository cannot reproduce a clean database from zero | Only 9 `CREATE TABLE` statements for 24 snapshot tables | Baseline schema + migration reconciliation before release |
| AUD-005 | **Medium** | Existing Android KB is stale relative to HEAD | Home cites `f8e5d8a`; HEAD `ca4bed4`; counts differ (351/43/22 vs 352/41+8/23) | Do not overwrite Android KB; note drift and link |
| AUD-006 | **Medium** | Proposed desktop KB paths would collide with Android note names | `Home`, `Architecture Map`, `Feature Roadmap`, etc. | Created a separate desktop vault; preserved Android vault |
| AUD-007 | **Medium** | User-supplied CSV is untracked and provenance is unstated | File exists at project root; no commit/metadata | Preserve; label as user-supplied, not authoritative |
| AUD-008 | **High** | Android reference has confirmed defects in stock, sync, statistics, and backup | Existing KB confirmed findings | Treat as anti-patterns; require desktop tests |
| AUD-009 | **High** | No desktop tests or test harness; Android tests not re-run | 0 desktop files; 41+8 Android test files but no execution | Test strategy and Phase 0 CI gate |
| AUD-010 | **High** | No desktop toolchain, dependency manifest, or build | No `go.mod`, `wails.json`, `package.json` | Phase 0 setup |
| AUD-011 | **Medium** | No desktop packaging, signing, print, or update path | No build/dist/update files | Phase 0/1 release workstream |
| AUD-012 | **High** | Privacy retention, backup format, and local encryption are undecided | No ADR/policy | Decision gate before PHI storage |
| AUD-013 | **Medium** | Table evidence sets disagree | `todo_notification_events` is referenced by migration but absent from both CSVs; `sync_queue`, `widget_due_cache`, `inventory_deductions`, and `backup_history` are local-only Room entities | Keep local-only tables local; verify `todo_notification_events` live |
| AUD-014 | **Low** | Android KB page counts and test totals are inconsistent internally | Home/Testing/Feature Roadmap dates and counts differ | Note as documentation debt; do not silently edit |
| AUD-015 | **Medium** | Supplied column CSV may be incomplete | Ordinal gaps (for example `patients` 9 -> 12) despite the reported column count | Treat as partial; require live catalog before baseline |

## What is genuinely strong in the reference

- Clear feature package separation and a substantial domain/test surface.
- Offline-first write intent with a local queue and explicit sign-out guard.
- Server-side receipt numbering with an immutable sequence.
- A detailed existing Knowledge Base with source citations and confirmed findings.
- A real RLS/role migration effort and security register, even where gaps remain.
- A versioned, encrypted backup container with a safety-backup concept.

## What cannot be concluded

- That any desktop feature works.
- That any live RLS policy is correct.
- That the Android test suite currently passes.
- That the supplied CSV is current or complete; ordinal gaps suggest omitted columns.
- That the desktop would connect to the same Supabase project as Android; the actual URL/project identity and key are absent from the worktree.
- That either CSV proves authentication, RLS, Storage, Realtime, or RPC configuration; neither contains those fields.
- That the Android app's workflows are free of the known defects.
- That a clean clone can reproduce production.

## Recommended next gate

Before feature implementation:
1. Create the desktop repository, `AGENTS.md`, branch protection, and CI.
2. Obtain approved access to the **existing** Supabase project and capture the real schema/grants/policies read-only. Do not create a new project or separate database; see [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]].
3. Reconcile the baseline migration against that evidence and prove the approved verification path works.
4. Approve local persistence, encryption, auth/session, sync, and backup ADRs.
5. Run the existing Android test suite or explicitly accept that its results are historical.
6. Re-run documentation validation and link checks.

## Related

[[Audits/Risk-Register|Risk Register]] · [[Audits/Technical-Debt|Technical Debt]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Testing/Test-Strategy|Test Strategy]]
