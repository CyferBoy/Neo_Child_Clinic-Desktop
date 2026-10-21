---
title: Glossary
doc_status: reference
evidence: project terminology + Phase 0C metadata review + Android source + target architecture
updated: 2026-10-21
---

# Glossary

> **Reference, not implementation.** Definitions describe how terms are used in this vault. Backend terms marked **[reported]** come from the 2026-10-21 metadata exports and are not runtime-certified.

## A–C

| Term | Meaning |
|---|---|
| **ACL (access control list)** | The privileges granted on a database object. A table ACL answers “can this role reach the table?” It does **not** decide which rows pass; RLS does that. |
| **Active staff** | A profile that is not soft-deleted and is marked active. The exported helper path is not safe to assume because of legacy policies; see [Security Model](Security/Security-Model.md). |
| **`anon`** | The PostgreSQL/Supabase role used for unauthenticated requests made with the public client key. It must have no business-table or business-function access in the target model. |
| **`app_metadata`** | Server-controlled Supabase user metadata. The Android client reads the authorization role from `app_metadata.role`; user-editable metadata must not grant a role. |
| **`authenticated`** | The PostgreSQL/Supabase role used after a user signs in. A valid JWT does not by itself make the user staff; active/role checks still apply. |
| **Absence reconciliation** | A proposed sync contract that detects rows missing from an authoritative snapshot, as an alternative to server tombstones. Not approved or implemented. |
| **Audit log** | An append-only, attributable record of sensitive actions. It is a business record, not a debug log. |
| **Clinic ID** | The human-facing patient identifier, separate from the UUID primary key. It must be unique and must not be used as the database identity. |
| **Conflict** | A state where local and remote changes cannot both be applied under the approved rules. Money, stock, clinical notes, and receipts must not use silent last-write-wins. |
| **Cursor** | A stored position used to resume a paged pull. It advances only after the page is committed locally. |

## D–I

| Term | Meaning |
|---|---|
| **Default ACL / default privileges** | The privileges PostgreSQL applies automatically to newly created objects. The export reports broad defaults; the 2026-10-30 Data API change means future tables may not be auto-exposed. Every new object needs explicit review. |
| **`SECURITY DEFINER`** | A PostgreSQL function that runs with its owner's privileges. It must pin `search_path` and revoke execution from roles that should not call it. |
| **Evidence class** | The source category behind a claim: repository source, exported metadata, Android source, verified live configuration, inference, or unknown. |
| **FEFO** | First Expired, First Out. The preferred batch-selection policy; manual selection must still be explicit. |
| **GRANT** | A PostgreSQL privilege assignment. Distinct from RLS: a role needs a grant to reach the object, then a policy to see rows. |
| **Idempotency** | The property that repeating the same operation produces the same business result and does not create a duplicate row, payment, dose movement, or receipt. |
| **IST (`Asia/Kolkata`)** | The clinic's reporting and due-date timezone. Business dates are not the workstation's local day. |
| **JWT** | The signed token presented on Supabase API requests. The desktop must keep it out of renderer storage and logs. |

## L–R

| Term | Meaning |
|---|---|
| **Local working copy** | The proposed SQLite database on the desktop. It is a durable local projection, not a second remote backend. |
| **Minor units** | Integer money representation, for example paise. The desktop should calculate in minor units and convert explicitly at the shared-schema boundary. |
| **Outbox** | A local table of pending writes with stable identity and transaction-group membership. It is committed in the same local transaction as the business change. |
| **PHI** | Protected health information: patient identity, contact details, clinical notes, vaccinations, consultations, reminders, documents, and any combination that can identify a patient. |
| **Policy (RLS policy)** | A PostgreSQL row-security rule attached to a table and role/command. Policies are permissive by default and combine with `OR`; a legacy policy can widen a newer one. |
| **PostgREST** | The HTTP API layer in front of PostgreSQL used by Supabase. Android uses it through supabase-kt. |
| **Publishable key** | The public Supabase client key. It is not a service-role secret, but it still identifies the project and can reach whatever the anon role is permitted to reach. |
| **Realtime** | Supabase's change-publication channel. The export reports publication membership but does not by itself prove Realtime authorization. |
| **RLS (Row Level Security)** | PostgreSQL row filtering by role and predicate. It is separate from table grants and function execution privileges. |
| **Receipt sequence** | The server-side numbering source keyed by financial year. The desktop must read the assigned number back, never compute it locally. |

## S–Z

| Term | Meaning |
|---|---|
| **`service_role`** | The privileged server-side Supabase role that bypasses RLS. It must never be shipped in the desktop client or exposed through Wails. |
| **Soft delete** | Marking a row deleted with flags/timestamps while retaining it for referential and audit purposes. Reads, reports, exports, and sync must filter consistently. |
| **Schema export** | A user-supplied metadata snapshot under `docs/Schemas/`. It is evidence, not a live-schema authority or a connection configuration. |
| **Storage bucket** | Supabase object storage. The Android reference uses `patient-docs`; bucket privacy and policy state are not verified from the export set. |
| **Tombstone** | A server record that a row was deleted. Repository evidence contains no complete tombstone feed; deletion propagation is unresolved. |
| **Transaction group** | A set of outbox rows that represent one business event, for example a vaccination visit plus stock, payment, reminder, and audit intent. A group is acknowledged only when all required members are acknowledged. |
| **`todo_notification_events`** | A table referenced by migrations but absent from the 24-table export. Its live existence is unknown. |
| **`L` evidence** | In the Phase 0C report, the 2026-10-21 metadata export set. |
| **`D` evidence** | In the Phase 0C report, the 2026-10-20 column export. It corroborates column shape, not keys, policies, or runtime access. |
| **Parity** | The same business result across Android and desktop, not an identical screen layout. |
| **P0 / P1 / P2 / P3** | Roadmap priority classes: P0 protects patient safety, money, identity, or security; P1 completes the Phase 1 clinic workflow; P2 is operational completeness; P3 is a future enhancement. |

## Evidence labels used in this vault

| Label | Meaning |
|---|---|
| `[VERIFIED]` | Directly checked in available source/artifacts. |
| `[REPORTED]` | Reported by a metadata export. |
| `[INFERRED]` | Reasoned conclusion, not runtime observation. |
| `[PROPOSED]` | Target design or requirement. |
| `[UNKNOWN]` | Evidence unavailable or conflicting. |
| `[DECISION]` | Explicit project direction or accepted ADR. |

## Related

[[Home]] · [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] · [[Security/Security-Model|Security Model]] · [[Database/Database-Architecture|Database Architecture]] · [[Product/Business-Rules|Business Rules]] · [[Testing/Test-Strategy|Test Strategy]]
