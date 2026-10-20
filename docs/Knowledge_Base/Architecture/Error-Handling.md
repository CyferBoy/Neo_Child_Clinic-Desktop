---
title: Error Handling
doc_status: proposed
evidence: Android error-handling reference + target architecture
updated: 2026-10-20
---

# Error Handling

> **Proposed only.** No desktop error boundary, error code registry, or retry policy exists.

## Goals

- The user knows whether the action was saved locally, saved remotely, rejected, or needs attention.
- No failure is swallowed.
- No raw database, HTTP, stack trace, token, or PHI reaches the UI or logs.
- Retries are safe and bounded.
- Support can diagnose without accessing patient data.

## Error taxonomy

| Class | Examples | User action | Retry |
|---|---|---|---|
| Validation | Missing field, invalid amount, expiry in past | Fix highlighted field | No automatic retry |
| Conflict | Duplicate clinic ID, stale version, receipt collision | Review and resolve | No blind retry |
| Permission | RLS denial, inactive account, role mismatch | Contact admin / re-authenticate | No |
| Auth | Expired/revoked session | Sign in again | Once after refresh |
| Offline | No network, DNS, timeout | Continue working locally | Automatic with backoff |
| Server transient | 429, 500, 502, 503, 504 | Show pending, retry | Yes, bounded |
| Server permanent | 400, 422, schema mismatch | Surface record and diagnostic | No |
| Local storage | Disk full, DB corrupt, migration failed | Stop writes, preserve data, recovery flow | No |
| Print/export | No printer, permission, malformed template | Retry/choose printer | Yes |
| Update | Signature failure, download failure, unsupported version | Abort update, keep current version | Yes for download only |
| Unknown | Unclassified | Safe generic message + correlation ID | No automatic |

## Stable error envelope

```json
{
  "code": "INV_STOCK_INSUFFICIENT",
  "message": "The selected batch does not have enough doses.",
  "retryable": false,
  "correlationId": "opaque-id"
}
```

Rules:
- `message` is safe for the user.
- `code` is stable and documented.
- `correlationId` links to a redacted Go log entry.
- No `details` field with raw server output unless explicitly sanitized.

## UI patterns

- **Inline:** field errors and cross-field rules.
- **Banner:** offline, sync degraded, update available.
- **Dialog:** destructive confirmation, conflict resolution, restore preview.
- **Sync center:** per-record failures with retry, export, and support reference.
- **Fatal screen:** local DB unrecoverable, migration failed, incompatible schema; offer backup/export and exit safely.
- **Error boundary:** renderer crash shows a recovery screen without losing unsaved form data where possible.

## Logging

- Structured JSON with timestamp, level, component, error code, correlation ID, app version, OS, and redacted context.
- Never log names, phone numbers, addresses, DOB, clinical notes, payment references, tokens, or full payloads.
- Log the operation and entity ID, not the entity content.
- Rotate logs; cap size; allow a redacted diagnostic export.
- Audit logs are separate and append-only.

## Retry policy

- Transient network/5xx: exponential backoff with jitter, capped attempts, visible pending state.
- 401: refresh once; then pause and re-authenticate.
- 403: no retry; permission path.
- 409: conflict path, not retry.
- 429: honor `Retry-After` if present; otherwise backoff.
- Duplicate/already-exists: reconcile identity before treating as success.
- User-initiated retry bypasses backoff but still uses idempotency.

## Requirements

| ID | Requirement |
|---|---|
| ERR-001 | Every user-visible failure has a stable code, safe message, and correlation ID. |
| ERR-002 | No raw SQL, HTTP body, stack trace, token, or PHI is displayed or logged. |
| ERR-003 | Retries are idempotent and bounded; non-retryable classes do not loop. |
| ERR-004 | A local write is never reported as cloud-saved before acknowledgement. |
| ERR-005 | A fatal local storage error stops writes and offers a safe recovery path. |

## Acceptance

- Simulate 401, 403, 409, 429, 500, timeout, and duplicate responses; each maps to the intended UI.
- Kill the network mid-write; the UI says saved locally, and sync resumes.
- Force a DB migration failure; the app refuses to write and preserves the old data.
- Search logs for a patient name after a full workflow; no match.
- A printer failure does not lose the payment or receipt state.

## Open questions

- What is the retention period for redacted logs?
- Is a crash-reporting service allowed, and under what data-processing agreement?
- Should support be able to export a redacted diagnostic bundle without admin approval?

## Related

[[Architecture/Frontend-Architecture|Frontend Architecture]] · [[Architecture/Offline-and-Sync-Design|Offline and Sync Design]] · [[Security/Privacy-and-Backup|Privacy and Backup]] · [[Features/16-Local-Persistence-and-Offline-Operation|Local Persistence]]
