---
title: Threat Model
doc_status: proposed
evidence: target architecture + Android security register
updated: 2026-10-20
---

# Threat Model

> **Proposed.** No desktop threat model has been validated against a running application. This document identifies the threats the Phase 1 design must address.
>
> **Backend constraint:** the desktop uses the same existing Supabase project/schema as Android under [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]. No new project, separate database, direct PostgreSQL access, or service-role key in the client is permitted.

## Scope

In scope: desktop client, local database, Wails IPC, Supabase Auth/PostgREST/Storage/Edge Functions, backup/export, printing, updates, and staff workflows.

Out of scope for this pass: Supabase platform compromise, clinic network hardware, Android client internals, legal compliance certification, and physical security beyond reasonable workstation controls.

## Actors

| Actor | Capability | Motivation |
|---|---|---|
| Legitimate staff | Valid account, role-limited | Care delivery; accidental misuse |
| Departing/former staff | Stale credentials or device access | Retaliation, data theft |
| Malicious insider | Valid low-privilege account | Curiosity, fraud, data sale |
| Opportunistic thief | Stolen laptop/backup | Data theft |
| Network attacker | Clinic Wi-Fi or upstream | Interception, injection |
| Malicious renderer content | XSS or compromised dependency | Token/data access, IPC abuse |
| Supply-chain attacker | Update/build dependency | Code execution |
| Automated attacker | Credential stuffing, API abuse | Account takeover, DoS |

## STRIDE summary

| Threat | Example | Mitigation | Residual |
|---|---|---|---|
| Spoofing | Stolen refresh token used on another device | Keychain, revocation, device registration, re-auth for sensitive actions | Token theft on a fully compromised OS |
| Tampering | Modified local DB or outbox payload | Local encryption/integrity, validation, server authority, idempotency | Root/admin malware |
| Repudiation | Staff denies a payment/stock adjustment | Append-only audit with authenticated actor, server timestamps | Shared OS account |
| Information disclosure | PHI in logs, backup, printer spool | Redaction, encryption, access control, retention | Shoulder surfing, OS-level capture |
| Denial of service | Sync flood, rate limits, disk full | Bounded queues, backoff, quotas, disk checks | Upstream outage |
| Elevation of privilege | UI guard bypass or permissive RLS | RLS verification, server checks, least privilege | Legacy policies not found |
| XSS / renderer compromise | Malicious patient note rendered as HTML | Escape by default, sanitize rich text, CSP, no `dangerouslySetInnerHTML` | Dependency compromise |
| Malicious update | Fake binary/update feed | Signed manifest and binary, pinned key, rollback | Signing key compromise |

## Priority threats

### T-01 Stolen laptop with a signed-in session
Impact: full clinic data exposure.
Controls: OS disk encryption, app lock, short idle timeout, encrypted local DB, keychain-bound key, remote revocation, clear caches on lock.
Verification: attempt offline access after lock/logout; inspect local files for plaintext PHI.

### T-02 Over-broad staff access
Impact: insider privacy breach, fraudulent edits.
Controls: RLS verification, least-privilege roles, audit review, no shared accounts, sensitive-action re-auth.
Verification: run the same query as nurse, receptionist, doctor, inventory manager, and deactivated user.

### T-03 Token theft through the renderer
Impact: account takeover and data exfiltration.
Controls: tokens only in Go/keychain, no Supabase calls from renderer, CSP, dependency review, no PHI in URLs.
Verification: inspect renderer storage, network calls, and crash reports for tokens.

### T-04 Sync replay or duplicate writes
Impact: duplicate payments, stock corruption, duplicate receipts.
Controls: stable IDs, idempotency keys, transaction groups, server uniqueness, duplicate reconciliation.
Verification: replay outbox batches, simulate timeout-after-commit, compare row counts and amounts.

### T-05 Malicious or malformed server data
Impact: renderer XSS, crash, data corruption.
Controls: runtime schema validation, escaping, allowlisted fields, no HTML rendering of notes, schema-drift stop.
Verification: inject unexpected fields/types through an approved test account/data set on the existing project; app rejects safely. Do not mutate production data.

### T-06 Backup theft
Impact: full clinic export.
Controls: strong passphrase KDF, authenticated encryption, no plaintext temp files, access-controlled storage, retention.
Verification: attempt to open without passphrase; inspect temp directories.

### T-07 Printer/export leakage
Impact: PHI left in spool or shared folders.
Controls: explicit action, preview, redaction options, secure spool guidance, no auto-export.
Verification: inspect spool/temp after print/export; test cancel/failure paths.

### T-08 Compromised update
Impact: arbitrary code execution with clinic data access.
Controls: signed manifest/artifact, pinned key, version monotonicity, rollback, no update during writes.
Verification: tamper with manifest/binary; app refuses.

### T-09 Destructive restore
Impact: data loss or cross-account contamination.
Controls: preview, safety snapshot, passphrase, explicit confirmation, account/clinic binding, transaction, post-restore reconciliation.
Verification: interrupt restore; previous DB remains intact.

## Abuse cases

- A receptionist attempts to open the audit screen by editing a route.
- A deactivated user restores an old refresh token.
- A staff member exports all patients to a personal drive.
- A malicious note contains `<script>` or a `javascript:` link.
- A batch quantity is edited directly in the local DB.
- A sync retry creates a second payment.
- An update binary is replaced on a shared drive.

## Security acceptance

- All priority threats have a test or a documented compensating control.
- RLS verification evidence is attached to the release.
- No critical/high finding remains open without an approved exception.
- The threat model is reviewed when auth, sync, backup, printing, or update design changes.

## Open questions

- Is the workstation shared between staff? If so, app lock and session switching need stronger controls.
- Are USB exports allowed? Under what policy?
- Is remote wipe/revocation required?
- What logging is permitted under the clinic's privacy obligations?

## Related

[[Security/Security-Model|Security Model]] · [[Security/Privacy-and-Backup|Privacy and Backup]] · [[Audits/Risk-Register|Risk Register]] · [[Testing/Test-Strategy|Test Strategy]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
