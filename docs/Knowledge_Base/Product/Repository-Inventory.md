---
title: Repository Inventory
doc_status: reference
evidence: filesystem + Git index at the start of the documentation completion pass (2026-10-21)
updated: 2026-10-21
---

# Repository Inventory

> **Two repositories are involved.** The desktop repository contains documentation only. The Android repository is the functional reference and must not be modified by this project. Counts below were checked at the start of the completion pass; documentation edits change the desktop document count.

## Desktop repository

**Path:** `/storage/emulated/0/Neo_Child_Clinic_Desktop`
**Git baseline:** `main` at commit `788995b` at the start of this pass
**Tracked files at that baseline:** 366
**Knowledge Base notes at that baseline:** 68 Markdown files
**Application source:** none

```text
Neo_Child_Clinic_Desktop/
├── README.md                     Project entry point
├── SECURITY.md                   Private reporting and testing boundaries
├── CONTRIBUTING.md               Documentation contribution rules
├── LICENSE                       Apache License 2.0
├── .gitignore                    Local secrets, OS files, docs/Schemas/
├── .opencode/skills/             17 project documentation/audit skills
└── docs/
    ├── Knowledge_Base/           Desktop vault, specifications, audits, ADRs
    ├── Schemas/                  16 local metadata exports; Git-ignored
    └── UI_Design/                Screens, prototype, screenshots, review manifests
```

### What exists

- The [[Home|Knowledge Base]]: product scope, 22 feature specifications, architecture, database/security assessment, testing, roadmap, decisions, audits.
- [UI design evidence](../../UI_Design/) including review and screenshot manifests.
- 17 `.opencode/skills/*/SKILL.md` definitions for audits, specs, database/security documentation, planning, testing, and release documentation.

### What does not exist

`go.mod`, `wails.json`, `package.json`, `src/`, `cmd/`, `internal/`, `frontend/`, `build/`, CI configuration, application tests, packaging configuration, release feed, or an application binary. There is no `AGENTS.md`.

### Local-only evidence

`docs/Schemas/` contains 16 user-supplied metadata exports covering columns, constraints, indexes, policies, ACLs, functions, triggers, relations, roles, and Realtime membership. It is ignored by Git at `.gitignore:14`. The exports contain no project URL, project reference, key, auth setting, or credential.

The older desktop column CSV was removed from the tracked tree in `788995b` and retained locally under `docs/Schemas/`. Git history still contains the earlier file.

## Android reference repository

**Path:** `/data/data/com.termux/files/home/Neo_Child_Clinic`
**Git state:** `main` at `ca4bed406bfd246ad83878fff9a4e178ebc5670f`, clean
**Tracked files:** 583
**Application version:** `0.5.1` (`versionCode` 3) in `gradle/libs.versions.toml`
**Build:** `compileSdk 37`, `minSdk 29`, `targetSdk 35` in `app/build.gradle.kts`
**Main Kotlin files:** 352; 45 `*Screen.kt`; 34 `*ViewModel.kt`
**Local database:** Room version 33, 25 `@Entity` classes across 21 files, 21 DAOs
**Feature packages:** 21 under `app/src/main/java/com/neochildclinic/feature/`
**Tests:** 41 unit files and 8 instrumented files
**SQL migrations:** 23 under `supabase/migrations/`
**Android Knowledge Base:** 37 notes under `docs/Knowledge_Base/`; preserved unchanged

Full architecture and evidence limits are in [Android Reference Architecture](../Architecture/Android-Reference-Architecture.md).

## Verified commands

Only commands actually used for this inventory are listed:

```bash
git status --short --branch
git ls-files | wc -l
git log -1 --oneline
find docs/Knowledge_Base -name '*.md' | wc -l
find docs/Schemas -maxdepth 1 -type f | wc -l
git check-ignore -v docs/Schemas/<file>
```

No build, test, lint, migration, Supabase, or packaging command is asserted because no desktop toolchain exists. Android test results were not re-run in this pass; the existing Android KB records a 2026-10-18 run of 277 unit tests, which is historical reference evidence, not a desktop result.

## Evidence limits

- File counts are point-in-time and will change with documentation edits.
- The Android source is read-only reference evidence; no runtime behaviour, Gradle build, or instrumented test was executed here.
- The schema exports describe reported metadata only. They do not prove the hosted project identity, live policies, grants, Storage, Realtime authorization, or migration ledger.
- The desktop UI design material does not imply implemented screens.

## Related

[[Home]] · [[Architecture/Android-Reference-Architecture|Android Reference Architecture]] · [[Audits/Initial-Audit|Initial Audit]] · [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] · [[Product/Feature-Inventory|Feature Inventory]] · [[Product/Android-Desktop-Parity|Android-Desktop Parity]]
