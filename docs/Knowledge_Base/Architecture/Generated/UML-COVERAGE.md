# UML & Diagram Coverage Matrix

Every standard UML 2.5 diagram type plus the supplementary types the suite addresses. Archify natively renders architecture, workflow, sequence, dataflow, and lifecycle; the remaining types are produced by a local SVG generator so coverage is honest rather than claimed. Live Supabase security behavior is marked UNKNOWN because the live project is never exercised in this documentation-only pass.

| Diagram type | Status | Renderer | Notes |
|---|---|---|---|
| Class | Implemented | SVG | Android reference + desktop proposed class models. |
| Object | Implemented | SVG | Sync-queue instance snapshot. |
| Package | Implemented | SVG | Android modules + desktop proposed modules. |
| Component | Implemented | Archify + SVG | Layered desktop architecture (Archify) + Android reference. |
| Composite Structure | Implemented | SVG | Desktop process internal parts and ports. |
| Deployment | Implemented | Archify | Single Wails process, webview, SQLite, shared Supabase. |
| Profile | Inapplicable | — | UML profiles/stereotypes have no meaning for this documentation set; the desktop is a greenfield app, not a UML-extensible platform. |
| Use Case | Implemented | SVG | Five clinic roles and core use cases. |
| Activity | Implemented | Archify | 10 feature workflows + auth, error, and build flows. |
| State Machine (behavioral) | Implemented | Archify | 7 lifecycle diagrams (sync, reminders, borrow, batch, finance, session). |
| Protocol State Machine | Implemented | SVG | Sync-item protocol signatures and guards. |
| Sequence | Implemented | Archify | 7 sequence diagrams (login, vaccination, sync, receipt, borrow, backup, refresh). |
| Communication | Implemented | SVG | Vaccination write message links. |
| Interaction Overview | Implemented | SVG | Consultation flow frame overview. |
| Timing | Implemented | SVG | Sync retry backoff duration model. |
| System Context (non-UML) | Implemented | Archify | Actors, desktop shell, shared Supabase. |
| Data Flow Diagram / DFD (non-UML) | Implemented | Archify | Offline capture/sync and offline registration. |
| Entity Relationship / ERD (non-UML) | Implemented | SVG | Core clinical, inventory, and finance domains from the schema export. |
| Model (UML 2.5) | Inapplicable | — | A model-containment diagram adds no information beyond the package and component views. |
| Information Item (UML 2.5) | Inapplicable | — | Information-item diagrams are superseded by the sequence and data-flow views already produced. |
| Macro (build/packaging pipeline) | Implemented (Android only) | Archify | Android Gradle pipeline; the desktop build is BLOCKED — no go.mod, wails.json, or CI exists. |
| Decision / ADR view | Documented elsewhere | — | 10 ADRs (ADR-0008 accepted; 9 pending incl. ADR-0010 backup/encryption) live in the Knowledge Base, not as a diagram. |
| Live security / RLS enforcement | Blocked (UNKNOWN) | — | Requires exercising the live Supabase project, which is out of scope; exports report {public} policies on 10 core tables and anon-executable functions. |

**Summary:** 23 diagram types tracked — 18 implemented, 3 documented as inapplicable, 1 blocked/unknown, 1 tracked elsewhere.

The suite ships 33 Archify-rendered HTML diagrams and 14 supplementary SVG diagrams (47 total). See [DIAGRAM-INDEX.md](DIAGRAM-INDEX.md) for the flat list and [index.html](index.html) for the interactive, filterable catalog.
