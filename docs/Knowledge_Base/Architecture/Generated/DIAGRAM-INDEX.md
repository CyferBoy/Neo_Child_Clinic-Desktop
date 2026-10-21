# Diagram Index

Flat index of every diagram in the generated suite. Evidence classes: `ANDROID-SOURCE` (verified at ca4bed4, reference only), `DESKTOP-PROPOSED` (planned, NOT implemented), `SCHEMA-EXPORT` (export-reported, not live-verified), `MIXED` (mixed or unknown).

## Structural

| Diagram | UML type | Evidence | Renderer | Summary |
|---|---|---|---|---|
| [System Context — Desktop & Shared Backend](structural/system-context.html) | System Context (non-UML) | `DESKTOP-PROPOSED` | Archify | Staff actors, the proposed desktop shell, and the shared Supabase project. |
| [Application Architecture — Desktop Layers](structural/application-architecture.html) | Component (layered) | `DESKTOP-PROPOSED` | Archify | React renderer → Wails bindings → services → repositories → SQLite + sync. |
| [Deployment — Desktop Runtime](structural/deployment-desktop.html) | Deployment | `DESKTOP-PROPOSED` | Archify | Single Wails process, webview, local SQLite file, shared Supabase. |
| [Android Reference Components](structural/component-android-reference.html) | Component | `ANDROID-SOURCE` | Archify | Verified app/core/data/domain/feature module structure at ca4bed4. |
| [Build & Packaging (Android reference)](structural/build-packaging-android.html) | Activity (build) | `ANDROID-SOURCE` | Archify | Gradle pipeline; no desktop build, signing, or CI exists. |
| [Class Diagram — Android Reference Model](structural/class-android-reference.svg) | Class | `ANDROID-SOURCE` | Supplementary SVG | Representative Room entities, DAOs, repositories, and services. |
| [Class Diagram — Desktop Proposed Layering](structural/class-desktop-proposed.svg) | Class | `DESKTOP-PROPOSED` | Supplementary SVG | Planned Go + React classes mirroring Android contracts; not implemented. |
| [Package Diagram — Android Modules](structural/package-android-reference.svg) | Package | `ANDROID-SOURCE` | Supplementary SVG | Verified Gradle module and package layout at ca4bed4. |
| [Package Diagram — Desktop Proposed Modules](structural/package-desktop-proposed.svg) | Package | `DESKTOP-PROPOSED` | Supplementary SVG | Planned Go module layout; no go.mod/wails.json exists yet. |
| [Object Diagram — Sync Queue Snapshot](structural/object-sync-queue-snapshot.svg) | Object | `ANDROID-SOURCE` | Supplementary SVG | Instance view of sync_queue rows during one vaccination upload. |
| [Composite Structure — Desktop Process](structural/composite-desktop-process.svg) | Composite Structure | `DESKTOP-PROPOSED` | Supplementary SVG | Internal parts and ports of the single Wails process. |

## Behavioral

| Diagram | UML type | Evidence | Renderer | Summary |
|---|---|---|---|---|
| [Authentication & Authorization Flow](behavioral/auth-authorization-flow.html) | Activity (auth) | `MIXED / UNKNOWN` | Archify | Sign-in, JWT role claim, RLS gate. Live enforcement UNKNOWN. |
| [Error Handling & Recovery](behavioral/error-recovery-flow.html) | Activity (error) | `DESKTOP-PROPOSED` | Archify | Fail-closed taxonomy with bounded retry; desktop code does not exist. |
| [Use Case — Roles & Clinic Use Cases](behavioral/use-case-clinic-roles.svg) | Use Case | `MIXED / UNKNOWN` | Supplementary SVG | Five roles and the core use cases; authorization is server-enforced. |
| [Communication — Vaccination Write](behavioral/communication-vaccination-write.svg) | Communication | `ANDROID-SOURCE` | Supplementary SVG | Numbered message links for one vaccination record. |
| [Interaction Overview — Consultation](behavioral/interaction-overview-consultation.svg) | Interaction Overview | `ANDROID-SOURCE` | Supplementary SVG | Frame overview where each box references a detailed interaction. |
| [Timing — Sync Retry Backoff](behavioral/timing-sync-retry.svg) | Timing | `ANDROID-SOURCE` | Supplementary SVG | Duration-constrained state changes under a transient 5xx. |
| [Protocol State Machine — Sync Item](behavioral/protocol-state-sync-item.svg) | Protocol State Machine | `ANDROID-SOURCE` | Supplementary SVG | Signatures and guards constraining accepted events per state. |
| [Sequence — Login & Session](behavioral/sequence-login-session.html) | Sequence | `ANDROID-SOURCE` | Archify | Verified Android login and bounded startup session restore. |
| [Sequence — Vaccination & Receipt](behavioral/sequence-vaccination-write.html) | Sequence | `MIXED / UNKNOWN` | Archify | Local commit, queued sync, server-assigned receipt number. |
| [Sequence — Sync Push/Conflict/Pull](behavioral/sequence-sync-push-pull.html) | Sequence | `ANDROID-SOURCE` | Archify | Last-write-wins reconciliation, single-flight, bounded retry. |
| [Sequence — Receipt Numbering](behavioral/sequence-receipt-numbering.html) | Sequence | `SCHEMA-EXPORT` | Archify | Server-side receipt assignment and counter locking (export-reported). |
| [Sequence — Borrow & Return](behavioral/sequence-borrow-return.html) | Sequence | `ANDROID-SOURCE` | Archify | Return path with outstanding-quantity cap and derived status. |
| [Sequence — Backup & Safe Restore](behavioral/sequence-backup-restore.html) | Sequence | `ANDROID-SOURCE` | Archify | Export and restore with a staged safety snapshot. |
| [Sequence — Dashboard Refresh](behavioral/sequence-dashboard-refresh.html) | Sequence | `ANDROID-SOURCE` | Archify | Pull-then-render refresh with single-flight guard and debounced realtime. |
| [State Machine — Sync Queue Item](behavioral/state-sync-queue.html) | State Machine | `ANDROID-SOURCE` | Archify | PENDING → SYNCING → SYNCED / FAILED with requeue recovery. |
| [State Machine — Vaccination Reminder](behavioral/state-reminder.html) | State Machine | `ANDROID-SOURCE` | Archify | ACTIVE / COMPLETED / DISMISSED / EXTERNAL with a duplicate guard. |
| [State Machine — Personal Reminder](behavioral/state-personal-reminder.html) | State Machine | `ANDROID-SOURCE` | Archify | PENDING → READY → COMPLETED with cancel and reverse side-paths. |
| [State Machine — Borrow Record](behavioral/state-borrow-record.html) | State Machine | `ANDROID-SOURCE` | Archify | Derived BORROWED / PARTIALLY_RETURNED / RETURNED status. |
| [State Machine — Inventory Batch](behavioral/state-inventory-batch.html) | State Machine | `ANDROID-SOURCE` | Archify | Batch stock lifecycle and the history-based deletion guard. |
| [State Machine — Financial Transaction](behavioral/state-finance-record.html) | State Machine | `ANDROID-SOURCE` | Archify | Append-only finance row with ambiguous-link failure. |
| [State Machine — Session Readiness](behavioral/state-session-readiness.html) | State Machine | `ANDROID-SOURCE` | Archify | USABLE / RETRY_LATER / LOGGED_OUT gating a sync group. |

## Data & Flows

| Diagram | UML type | Evidence | Renderer | Summary |
|---|---|---|---|---|
| [Data Flow — Offline Capture & Sync](data-and-flows/dataflow-offline-sync.html) | Data Flow (DFD) | `MIXED / UNKNOWN` | Archify | Local-first write, queue, push, authority, pull. RLS UNKNOWN. |
| [Data Flow — Offline Registration](data-and-flows/dataflow-patient-registration-offline.html) | Data Flow (DFD) | `DESKTOP-PROPOSED` | Archify | Planned desktop offline registration path mirroring Android. |
| [ERD — Core Clinical Schema](data-and-flows/erd-core-clinical.svg) | Entity Relationship (ERD) | `SCHEMA-EXPORT` | Supplementary SVG | patients, visits, vaccination_items, consultations, notes. |
| [ERD — Inventory & Stock Schema](data-and-flows/erd-inventory.svg) | Entity Relationship (ERD) | `SCHEMA-EXPORT` | Supplementary SVG | vaccines, batches, transactions, waste, borrow/return ledger. |
| [ERD — Finance & Receipt Schema](data-and-flows/erd-finance.svg) | Entity Relationship (ERD) | `SCHEMA-EXPORT` | Supplementary SVG | finance_transactions, expenses, receipt_sequences, reminders. |

## Feature Workflows

| Diagram | UML type | Evidence | Renderer | Summary |
|---|---|---|---|---|
| [Activity — Record a Vaccination](features/activity-vaccination-record.html) | Activity | `ANDROID-SOURCE` | Archify | One transaction across visit, items, income, stock, and queue. |
| [Activity — Inventory Decrement](features/activity-inventory-decrement.html) | Activity | `ANDROID-SOURCE` | Archify | FEFO decrement with reconciliation ledger and duplicate risk. |
| [Activity — Borrow / Partial / Full Return](features/activity-borrow-return.html) | Activity | `ANDROID-SOURCE` | Archify | Borrow lifecycle with outstanding-quantity guard rails. |
| [Activity — Create a Patient](features/activity-patient-create.html) | Activity | `ANDROID-SOURCE` | Archify | Clinic-id generation, uniqueness check, insert, and enqueue in one tx. |
| [Activity — Record a Consultation](features/activity-consultation-record.html) | Activity | `ANDROID-SOURCE` | Archify | Slot revalidation and an optional edit/no-change branch. |
| [Activity — Batch Selection & Expiry](features/activity-batch-expiry.html) | Activity | `ANDROID-SOURCE` | Archify | FEFO selection and expiry rules enforced at UI and repository. |
| [Activity — Due Vaccinations & Reminders](features/activity-due-reminders.html) | Activity | `ANDROID-SOURCE` | Archify | Reminder pipeline; due dates are entered, not computed. |
| [Activity — Dashboard Statistics](features/activity-dashboard-stats.html) | Activity | `ANDROID-SOURCE` | Archify | Local-first aggregation; no dashboard query reaches the network. |
| [Activity — Staff & Role Management](features/activity-staff-roles.html) | Activity | `ANDROID-SOURCE` | Archify | Client gating is UX only; the Edge Function is the real boundary. |
| [Activity — Backup & Restore](features/activity-backup-restore.html) | Activity | `ANDROID-SOURCE` | Archify | Fail-closed backup and staged-safety restore; ADR-0010 pending. |

**Total: 47 diagrams** (33 Archify-rendered HTML + 14 supplementary SVG).
