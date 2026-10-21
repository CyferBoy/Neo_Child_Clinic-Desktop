# Neo Child Clinic Desktop — UI/UX Design Package

**Status:** design-only proposal. No production UI, backend, database, auth, API or business rule was implemented or changed.

This package defines a complete desktop design direction, screen set, component system, workflow model and implementation backlog for the Neo Child Clinic Desktop application. It is grounded in the existing Knowledge Base and the 22 Phase 1 module specifications. The repository contains **no desktop source code**; every desktop capability described here is a design proposal, not an implemented feature.

## What is in this package

| Artifact | Location | Count |
|---|---|---|
| Screen specifications | [`Screens/`](Screens/) | 68 |
| Standalone HTML prototype | [`prototype/screens/`](prototype/screens/) | 68 pages |
| Gallery and index | [`prototype/index.html`](prototype/index.html) | 1 |
| Prototype preview guide | [`prototype/README.md`](prototype/README.md) | — |
| Rendered PNG references | [`screenshots/`](screenshots/) | 73 |
| Screen inventory | [`Screen-Inventory.md`](Screen-Inventory.md) | 68 rows |
| Design system | [`Design-System.md`](Design-System.md) | — |
| Navigation and workflows | [`Navigation-and-Workflows.md`](Navigation-and-Workflows.md) | — |
| Component catalogue | [`Component-Catalog.md`](Component-Catalog.md) | — |
| State and error model | [`States-and-Errors.md`](States-and-Errors.md) | — |
| Accessibility | [`Accessibility.md`](Accessibility.md) | — |
| Traceability | [`Design-Traceability.md`](Design-Traceability.md) | — |
| Implementation backlog | [`Implementation-Backlog.md`](Implementation-Backlog.md) | — |
| Validation record | [`Validation.md`](Validation.md) | — |
| Screenshot review | [`Screenshot-Review.md`](Screenshot-Review.md) | 68 screens / 73 images |
| Review workflow and manifest | [`review/`](review/) | 8 batches, max 10 images each |
| Repository/requirements audit | [`Repository-and-Requirements-Audit.md`](Repository-and-Requirements-Audit.md) | — |

The 73 screenshots are 68 light-theme screens at 1366×768 plus five reference variants:

- `AUTH-001-wide.png` at 1920×1080
- `DASH-001-wide.png` at 1920×1080
- `DASH-001-dark.png`
- `PAT-001-dark.png`
- `SET-001-dark.png`

The dark and wide images are rendered from the same HTML as the light pages. They are not separate mockups.

## Design direction

**Calm Clinical Precision.** A light-first, data-dense clinical workspace built around deep teal, warm apricot accents, clear status semantics and compact but readable tables. Dark variants preserve the same semantic colours rather than inventing a different visual language.

The design targets the two documented desktop sizes:

- **1366×768** — primary reference and the size used for every base screenshot.
- **1920×1080** — wide reference for authentication and dashboard, with the same shell and content rules.

## How to review the prototype

1. Open [`prototype/index.html`](prototype/index.html) in a browser. It links to all 68 pages. For exact direct-file and local-server commands, see [`prototype/README.md`](prototype/README.md).
2. Open any page under [`prototype/screens/`](prototype/screens/). Pages are static HTML and use only local assets, local fonts and local fictional data.
3. Use the theme control in the shell to inspect light/dark behaviour where implemented.
4. Use the search field or `Ctrl/Cmd+K` to focus the global search affordance.
5. Compare the page with its specification under [`Screens/`](Screens/) and its PNG under [`screenshots/`](screenshots/).

No page calls a production service, opens a database, sends a network request, or uses a real patient record.

## Screenshot review

The rendered screenshots are reviewed in isolated batches of **at most 10 images per AI request**. The workflow, batch files, prompts, manifest and request-size audit live in [`review/`](review/README.md). Results and any screens needing attention are in [`Screenshot-Review.md`](Screenshot-Review.md).

The manifest records every screen ID, its screenshot path(s), batch, review status, verdict and concise finding. A screen with dark or wide variants counts every image toward its batch limit and is never split across batches. No batch inherits images from another batch.

## Evidence boundary

- **Repository:** the design package is the only untracked change under `docs/UI_Design/`.
- **Desktop implementation:** none. All 22 Phase 1 desktop modules are `Missing` in the Knowledge Base.
- **Android reference:** source exists, but was not executed in this pass. Android claims are not runtime verification.
- **Backend:** ADR-0008 (reuse the existing Supabase project and schema) is accepted. No connection was made and no project identifier or secret is included.
- **Decisions:** ADR-0001–ADR-0007 and D1–D14 remain unapproved. The design does not silently settle unresolved policy.
- **Data:** all names, identifiers, amounts, stock counts, clinical text and timestamps are fictional.

## Approval gate

This is a design proposal. **Do not implement production UI from this package without explicit user approval.** Before implementation, the open decisions listed in [`Implementation-Backlog.md`](Implementation-Backlog.md) and the Phase 0B blockers in the Knowledge Base must be resolved or explicitly accepted.

## Related Knowledge Base documents

- [`Product Scope`](../Knowledge_Base/Product/Product-Scope.md)
- [`Feature Inventory`](../Knowledge_Base/Product/Feature-Inventory.md)
- [`Android-Desktop Parity`](../Knowledge_Base/Product/Android-Desktop-Parity.md)
- [`Personas and Roles`](../Knowledge_Base/Product/Personas-and-Roles.md)
- [`Frontend Architecture`](../Knowledge_Base/Architecture/Frontend-Architecture.md)
- [`Risk Register`](../Knowledge_Base/Audits/Risk-Register.md)
- [`ADR-0008`](../Knowledge_Base/Decisions/ADR-0008-Shared-Supabase-Backend.md)
