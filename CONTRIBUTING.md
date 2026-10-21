# Contributing to Neo Child Clinic Desktop

> **Current phase: documentation and architecture review.** This repository has no Go/Wails/React application source, package manifest, build, or desktop test suite. Do not add implementation code as part of documentation work.

## Before changing anything

1. Read the [Knowledge Base entry](docs/Knowledge_Base/README.md), [Home](docs/Knowledge_Base/Home.md), and the latest [Documentation Completion Report](docs/Knowledge_Base/Audits/Documentation-Completion-Report.md).
2. Run `git status` and preserve unrelated working-tree changes. The Obsidian files under `docs/Knowledge_Base/.obsidian/` are local UI state and should not be committed unless a separate decision explicitly approves it.
3. Do not modify the Android reference repository at `/data/data/com.termux/files/home/Neo_Child_Clinic`.
4. Do not connect to Supabase, execute SQL or HTTP requests, alter grants/policies/triggers, or change production data.
5. Do not commit credentials, tokens, project URLs, patient data, or the user-supplied exports under `docs/Schemas/`. That directory is intentionally ignored.

## What belongs here

- Documentation that can be supported by the repository, Android source, migration evidence, user-supplied schema exports, or an explicit project decision.
- Proposed architecture, requirements, test plans, and decision records clearly labelled as proposed.
- Corrections that remove a stale or contradictory claim and cite the supporting evidence.

What does not belong here:

- Application code, dependencies, lockfiles, migrations, or database objects.
- Invented commands, URLs, releases, licence terms, delivery dates, or completed-feature claims.
- A parallel remote backend, a second Supabase project, or a duplicate remote schema.
- Security remediation presented as applied when it was only recommended.

## Evidence standard

Use the same labels as [Home](docs/Knowledge_Base/Home.md):

| Label | Meaning |
|---|---|
| `[VERIFIED]` | Directly checked in the available source, filesystem, migration, or artifact. |
| `[REPORTED]` | Reported by a metadata export; not a runtime observation. |
| `[INFERRED]` | A reasoned conclusion from evidence, not a runtime observation. |
| `[PROPOSED]` | Target design or requirement; not implemented or approved for implementation. |
| `[UNKNOWN]` | Evidence unavailable, conflicting, or not inspected. |
| `[DECISION]` | Explicit project direction or an accepted ADR. Only ADR-0008 is accepted at this baseline. |

Security findings additionally use the status vocabulary in the [Security Model](docs/Knowledge_Base/Security/Security-Model.md): **Confirmed in repository source**, **Observed in an export**, **Verified against live configuration**, **Potential risk requiring verification**, **Deferred by user**, and **Resolved with evidence**. Do not describe an exported policy as a confirmed production exposure.

## Documentation workflow

1. Search for an existing note before creating a new one. Update it instead of duplicating it.
2. Keep the frontmatter fields `title`, `doc_status`, `evidence`, and `updated` on Knowledge Base notes.
3. Use Obsidian-compatible relative wikilinks such as `[[Features/04-Patient-Management|Patient Management]]`.
4. Add a source path and symbol for significant technical claims, for example `core/sync/SyncUploader.kt`.
5. Link every new note from [Home](docs/Knowledge_Base/Home.md) or the appropriate index.
6. Separate verified Android behaviour, reported backend metadata, proposed desktop behaviour, and unknowns.
7. State `Not run` or `Not implemented` where that is the truth. A plan is not a test result.

## Validation before handoff

- Check Markdown and Obsidian links, including new files and index entries.
- Check frontmatter, heading structure, code fences, and Mermaid fences.
- Search edited notes for contradictory counts or stale commit references.
- Confirm no credentials, tokens, URLs, patient identifiers, or ignored exports are staged.
- Inspect `git diff --stat` and the full diff for accidental application, migration, or `.obsidian` changes.
- Re-read [Documentation Validation](docs/Knowledge_Base/Audits/Documentation-Validation.md) and the latest completion report before claiming a documentation phase is complete.

## Security reporting

Do not open a public issue containing a vulnerability, PHI, credentials, or reproduction data. Follow [SECURITY.md](SECURITY.md).

## Commits and review

- Keep changes scoped and explain the evidence behind them.
- Do not claim that CI, branch protection, packaging, or tests exist until they do.
- Documentation changes are reviewed against the architecture and security gates in the [Desktop Roadmap](docs/Knowledge_Base/Roadmap/Desktop-Roadmap.md).
- Implementation remains blocked until the Phase 0C items in the [Risk Register](docs/Knowledge_Base/Audits/Risk-Register.md) are closed or formally risk-accepted.

## License

Contributions to this repository are accepted under the [Apache License 2.0](LICENSE).
