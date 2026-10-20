---
title: Go Backend Architecture
doc_status: proposed
evidence: Go + Wails project direction + Android repository patterns
updated: 2026-10-20
---

# Go Backend Architecture

> **Proposed only.** There is no `go.mod`, Go package, Wails binding, or database driver in the desktop project.

## Responsibilities

The Go process is the trusted desktop application core. It owns:
- Wails binding methods and input validation.
- Use-case orchestration and local transactions.
- Local database migrations and queries.
- Supabase Auth session handling and HTTPS calls to the **existing** project.
- Sync outbox, pull cursor, retries, and conflict classification.
- Audit intent and append-only records.
- OS keychain, printing, file export, and update verification.

The renderer is a presentation client. It must not receive database handles, service-role keys, refresh tokens, or unrestricted filesystem APIs. The desktop must not open a direct PostgreSQL connection or create a second database; see [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]].

## Proposed package layout

```text
cmd/clinic-desktop/        main, Wails bootstrap, single-instance
internal/app/              use cases and binding contracts
internal/domain/           pure rules: money, dates, stock, due dates, merge
internal/infra/localdb/    SQLite, migrations, repositories, transactions
internal/infra/supabase/   auth, PostgREST, storage, edge functions
internal/sync/             outbox, puller, retry, conflict handling
internal/security/         keychain, session, redaction, permissions
internal/printing/         receipt rendering and OS print adapter
internal/update/           signed manifest, verification, rollback
internal/observability/    structured logs, redacted diagnostics
```

Packages depend inward. Domain has no Wails, SQL, HTTP, or OS imports.

## Binding contract rules

1. Every method has a typed request and typed result.
2. Every request is validated for required fields, length, range, and cross-field consistency.
3. Mutating methods accept an idempotency key or derive one from a stable business identity.
4. Methods accept a `context.Context` for cancellation and timeouts.
5. Errors are mapped to stable codes; raw SQL/HTTP errors never cross the boundary.
6. Authorization is checked against the current session and, where relevant, the server; the renderer's claimed role is not trusted.
7. Methods return the locally committed state and a sync status; they do not block indefinitely on the network.

## Local database

`[PROPOSED]` SQLite with:
- WAL mode, foreign keys, busy timeout, and one writer goroutine.
- Versioned migrations embedded in the binary.
- Explicit transactions for visit creation, stock movement, payment, receipt link, and outbox insert.
- `PRAGMA integrity_check` at startup or scheduled maintenance.
- Backup/export path that uses a consistent snapshot, not a raw copy of an open WAL database.

The local schema is **not** assumed to be identical to PostgreSQL. It mirrors the working set and sync metadata. Differences must be documented and migrated.

## Supabase access

- Use Supabase Auth for sign-in, refresh, and revocation.
- Call PostgREST with the user's access token; do not embed a service-role key.
- Use Edge Functions only for operations that require server-side secrets, such as staff administration and push notifications.
- Pin the API surface and validate response shapes.
- Treat 401/403 differently: refresh/re-authenticate versus show a permission error.
- Never log Authorization headers, refresh tokens, or full request bodies containing PHI.

## Receipt numbers

Receipt numbers are assigned by PostgreSQL (`receipt_sequences` + `neo_next_receipt_number` / `neo_assign_receipt_number`). The desktop must upload a blank receipt number for a new visit and read the assigned value back. It must not compute or reuse a number locally. A local placeholder must be clearly labeled and never printed as a final receipt.

## Sync worker

```text
commit local transaction
  -> enqueue outbox row(s) with transaction_group_id
  -> return success to UI with "pending sync"
  -> worker claims a batch atomically
  -> uploads in dependency order
  -> marks acknowledged only after server confirmation
  -> pulls changes after a cursor
  -> resolves/queues conflicts
```

The worker is single-flight per entity group, backs off with jitter, and never drops a failed row silently. A transaction group is acknowledged only when all required members are acknowledged, or the group is explicitly marked repairable with a visible error.

## Logging and diagnostics

- Structured logs with correlation IDs, not free-text patient details.
- Redact names, phone numbers, addresses, clinical notes, tokens, and full payloads.
- Provide an exportable diagnostic bundle that contains counts, versions, error codes, and redacted metadata.
- Audit logs are business records, not debug logs; keep them separate.

## Testing

- Pure domain unit tests for money, dates, stock, due dates, and merge rules.
- Repository tests against an in-memory or temporary SQLite database.
- Contract tests against the existing Supabase project through an approved non-destructive verification path; a separate test harness requires explicit approval and must not become the desktop backend.
- Sync tests with fault injection: timeout, 409, 429, 500, duplicate response, partial group, token expiry.
- Race tests for one writer and concurrent UI reads.
- Backup/restore round-trip and corrupted-file tests.

## Open questions

- SQLite driver and encryption approach.
- Wails v2 versus v3 and binding generation workflow.
- Whether the Go process owns printing or delegates to an OS helper.
- How local schema migrations are rolled back after a failed upgrade.
- Whether the app supports a portable mode or only per-user installation.

## Related

[[Architecture/System-Architecture|System Architecture]] · [[Architecture/Offline-and-Sync-Design|Offline and Sync Design]] · [[Decisions/ADR-0002-Local-Persistence|ADR-0002]] · [[Decisions/ADR-0005-Wails-Boundary|ADR-0005]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]]
