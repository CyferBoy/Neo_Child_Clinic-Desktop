---
title: ADR-0002 Local Persistence
doc_status: proposed
evidence: offline-first requirement + Android Room reference
updated: 2026-10-20
---

# ADR-0002 — Local Persistence

**Status:** Proposed.

## Context

The desktop must read and write clinical data offline. It needs durable transactions, a sync outbox, migrations, and a recovery story. The local store is PHI and must be protected.

## Decision

Use **SQLite** as the local working database, accessed only by Go, with:
- WAL mode, foreign keys, busy timeout, and a single writer.
- Embedded, versioned migrations.
- Explicit transactions for business events and outbox rows.
- A separate local schema from PostgreSQL, with typed mapping at the boundary.
- Encryption at rest using an approved mechanism; key protected by the OS keychain.

The exact SQLite driver and encryption library remain open.

## Alternatives considered

| Alternative | Assessment |
|---|---|
| Embedded key-value store | Weak relational queries/transactions for clinical joins |
| JSON files | No transactional integrity; corruption risk |
| In-memory only | Fails offline durability |
| Direct remote-only | Fails offline requirement |
| Full PostgreSQL locally | Heavy operational burden for a desktop app |

## Consequences

Positive:
- Mature transactions, indexes, and migrations.
- Works offline and on modest hardware.
- Easy backup snapshot and test fixtures.

Negative / risks:
- Schema duplication with PostgreSQL.
- Encryption/key recovery complexity.
- Concurrent multi-process access must be prevented or designed.
- Local migration failure can block the app.

## Validation

- Kill the process during a transaction; committed data survives, partial data does not.
- Run 10 migrations forward on a populated DB; no data loss.
- Simulate disk full/corruption; app stops safely and offers recovery.
- Verify no plaintext PHI in the DB file or temp files.

## Open questions

- SQLite driver and encryption approach.
- Key derivation/recovery and whether the DB key is per-device or per-user.
- Local schema versioning and downgrade policy.
- Portable vs per-user install.

## Related

[[Architecture/Go-Backend-Architecture|Go Backend]] · [[Architecture/Offline-and-Sync-Design|Offline and Sync]] · [[Security/Privacy-and-Backup|Privacy and Backup]]
