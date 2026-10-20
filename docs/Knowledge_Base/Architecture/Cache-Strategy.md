---
title: Cache Strategy
doc_status: proposed
evidence: Android caching reference + confirmed stale-cache defect
updated: 2026-10-20
---

# Cache Strategy

> **Proposed only.** There is no desktop cache implementation.

## Principle

The local database is the durable working copy. A cache may accelerate reads, but it must not become a second, less-correct source of truth. No cache may serve a value that contradicts an unacknowledged local write.

## Layers

| Layer | Contents | Lifetime | Invalidation |
|---|---|---|---|
| Renderer query cache | Read models for active screens | Screen/session | Local DB change notifications; explicit refetch |
| Go read cache | Small lookup sets (roles, vaccine catalog labels) | Short TTL | Versioned key; write-through invalidation |
| Local database | Working copy and outbox | Durable | Transactional writes and pull |
| HTTP cache | No PHI responses | Avoid | Not used for patient data |
| OS/keychain | Tokens and keys | Session/device | Logout, revocation, key rotation |

## Rules

1. **Writes update the local DB first.** Never update a renderer cache as if the write succeeded before the local transaction commits.
2. **Invalidate on committed change.** A patient edit, vaccination, payment, or stock movement invalidates every read model that depends on it.
3. **No long-lived PHI in memory.** Clear patient detail caches on sign-out, lock, and after a configurable idle period.
4. **No cross-account cache.** A different user session must not see the previous user's data.
5. **No cache-only authorization.** A cached role or permission is for rendering; Go/RLS decides.
6. **No stale history.** Editing a vaccination must invalidate the patient timeline, not only the patient row.
7. **Bounded size.** Use LRU limits and metrics; do not cache unbounded lists.
8. **Explicit stale state.** If a read is from a stale snapshot, label it and offer refresh.

## Anti-pattern from the reference

The Android `PatientCache` is invalidated on `patients` table changes, but not on vaccination edits, so a cached patient can hold stale history for up to five minutes. The desktop must key cache entries by all dependent entity versions or invalidate on the broader clinical event.

## Proposed read model keys

- `patient:{id}:v{version}`
- `patient-list:{queryHash}:v{patientsVersion}`
- `inventory:{vaccineId}:v{stockVersion}`
- `due-list:{date}:v{reminderVersion}`
- `dashboard:{date}:v{aggregateVersion}`

A monotonic local `data_version` per aggregate is simpler and safer than time-based expiry for clinical reads.

## Offline behavior

- Cached reads remain available offline.
- A cache miss reads the local database.
- A local database miss may show an empty state, but must not silently fetch and claim freshness while offline.
- Background refresh failures do not erase existing data.

## Security

- Do not cache PHI in browser storage, service workers, or unencrypted temp files.
- Do not include PHI in cache keys written to logs.
- Clear caches on logout and account switch.
- Protect diagnostic dumps from containing cached patient data.

## Acceptance

- Edit a vaccination; open the patient timeline; the new item and stock state are visible immediately.
- Switch users; no previous user's patient appears.
- Go offline; cached lists remain readable; a write still commits locally.
- Kill the app; reopen; the local DB is the source, not a stale memory cache.
- Corrupt/clear the renderer cache; the app recovers from the local DB.

## Open questions

- Is a renderer query library approved, or is a hand-rolled read model preferred?
- What idle timeout should clear PHI from memory?
- Are aggregate dashboard caches worth the complexity in Phase 1?

## Related

[[Architecture/Offline-and-Sync-Design|Offline and Sync Design]] · [[Architecture/Frontend-Architecture|Frontend Architecture]] · [[Features/16-Local-Persistence-and-Offline-Operation|Local Persistence]]
