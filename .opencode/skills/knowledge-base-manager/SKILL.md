---
name: knowledge-base-manager
description: "Maintain the Neo Child Clinic Obsidian Knowledge Base safely. Use to search for duplicate or conflicting notes, create or update approved notes, preserve frontmatter and wikilinks, maintain the index and cross-links, and validate the vault without reorganizing it wholesale."
metadata:
  version: "1.0"
  mode: "docs-write-after-approval"
  scope: "neo-child-clinic-desktop"
---

# Knowledge Base Manager

Maintain the project's Obsidian vault as a curated, evidence-backed knowledge base. The vault may contain Android reference material, desktop documentation, or both. Never reorganize the whole vault, bulk-rewrite notes, or create a parallel documentation system without approval.

## Invoke when

- A requested document must be created, updated, linked, or indexed.
- You need to find whether a note already covers a topic before writing a new one.
- Links, frontmatter, or indexing need repair.
- A documentation change must be scoped to specific notes.

Do not use this skill to reconcile many stale claims across the codebase; use `documentation-sync` first, then apply approved edits here.

## Inputs

- Absolute vault path. Discover it; do not assume. A vault normally contains `.obsidian/`.
- Requested note title, purpose, scope, and evidence sources.
- Whether the request is create, update, index, link repair, or template work.
- Explicit approval for any write, and the exact destination.

## Before you start

1. Read the root and nested `AGENTS.md`, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read, the vault index (often `Home.md`), the documentation maintenance guide, and any template notes.
2. Record the current Git status and commit. If the vault is outside Git, record that.
3. Determine whether the requested note is Android-reference material, desktop-specific material, or shared. Do not mix them without an explicit namespace decision.
4. If no vault exists, stop and propose a location and structure. Do not create one until approved.

## Evidence standard

- `[VERIFIED]` — cited from current source, schema, configuration, or an executed command using `path:line`.
- `[INFERENCE]` — derived from cited evidence; state the reasoning.
- `[PROPOSED]` — target design or recommendation; label it clearly.
- `[UNKNOWN]` — missing evidence; name the source that would resolve it.

A claim without a citation is a hypothesis. Put hypotheses in the vault's designated hypotheses note rather than presenting them as facts. Do not paste secrets, tokens, or personal data into notes.

## Procedure

1. **Locate the vault and its conventions.** Read the index, maintenance guide, recent notes, and templates. Record frontmatter fields, tag style, wikilink style, heading conventions, and the validator command if one exists.
2. **Search before creating.** Search titles, aliases, headings, tags, and body text for the topic and its synonyms. Also search the Android and desktop namespaces separately. Report any duplicate, near-duplicate, or contradictory note.
3. **Decide create vs update.** Prefer updating an existing canonical note. Create a new note only when the topic is distinct and the index has a sensible place for it. If two notes conflict, report the conflict and ask which is authoritative; do not merge silently.
4. **Propose the change.** State the destination path, note title, frontmatter, sections to add or change, inbound links, and index update. For bulk changes or moves, stop for explicit approval.
5. **Write targeted content.** Preserve existing wording and structure where possible. Use `[[Note Name]]` wikilinks that resolve by note name. Do not use short heading anchors; the project validator does not resolve fragments, and Obsidian requires the full heading text. Link to evidence rather than duplicating large source excerpts.
6. **Record provenance.** Add or preserve a header with scope, commit, date, and evidence rules. Mark proposed architecture separately from verified implementation.
7. **Maintain the index.** Add one clear entry to the appropriate index or map-of-content note. Do not regenerate the whole index unless approved. Ensure the new note has an inbound link and at least one useful outbound link.
8. **Validate.** If a project validator exists, run it exactly as documented and report the observed result. If none exists, manually check wikilinks, Markdown links, Mermaid fences, required headings, and duplicate titles; state that validation was manual.
9. **Report.** List files created or changed, index updates, links added, unresolved duplicates, and validation output. Do not claim a validator passed unless it was run.

## Output contract

A Knowledge Base change report:

```markdown
# Knowledge Base Change — <YYYY-MM-DD>

## Request
## Vault and conventions
- Vault:
- Index:
- Frontmatter:
- Link style:
- Validator:

## Duplicate / conflict search
| Candidate | Path | Relationship | Decision |
|---|---|---|---|

## Files changed
| Path | Action | Sections | Evidence |
|---|---|---|---|

## Index and links
- Index entry:
- New inbound links:
- New outbound links:

## Validation
- Command:
- Observed result:
- Manual checks:

## Unresolved
```

Use documentation status values `Current`, `Stale`, `Missing`, `Contradictory`, `Unverified` when reporting note health. Use `DOC-<AREA>-NNN` for tracked documentation discrepancies.

## Stop conditions

Stop and report when:

- No vault is present.
- The requested note duplicates or contradicts an existing note, and no authoritative version is identified.
- The request requires moving, renaming, or deleting many notes.
- The change would overwrite uncommitted user work.
- The validator fails for reasons outside the requested change.
- A note would contain a secret, credential, or identifiable patient data.

## Handoff

- `documentation-sync` — produce a discrepancy report across the vault.
- `architecture-documenter` — author architecture notes and ADRs.
- `api-database-documenter` — author schema and API notes.
- `release-documenter` — author release notes and checklists.
- `documentation-sync` — re-check links and claims after edits.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Never reorganize the entire vault without approval.
- Never delete a note to silence an orphan or broken-link warning; link it or report it.
- Never bulk-search-and-replace across the vault.
- Never overwrite an audit report; append a reconciliation.
- Do not modify application code, migrations, SQL policies, or configuration while managing documentation.
