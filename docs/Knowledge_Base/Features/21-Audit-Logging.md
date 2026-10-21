---
title: Audit Logging
feature_id: AUD
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 21. Audit Logging

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/audit/`, `core/logger/AuditLogger.kt`, `supabase/migrations/*audit*`.

**Requirement IDs:** `AUD-001`, `AUD-002`, `AUD-003`, `AUD-004`, `AUD-005`

## 1. Purpose and scope

Record an append-only, attributable history of sensitive actions and provide an admin review surface without exposing or allowing mutation of audit records.

### User stories

- As an admin, I can review who changed a patient, payment, stock item, role, or backup.
- As a staff member, my sensitive actions are attributable without clinical content being written to logs.

## 2. Actors

- Admin (review)
- All staff (implicit writer)

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Emit audit intent inside a business transaction.
2. Sync audit rows append-only.
3. View paged/filtered audit by patient/entity/actor/date.
4. Export a redacted audit extract if approved.
5. Investigate a failed/duplicate audit write.

## 5. UI states

| State | Expected behavior |
|---|---|
| Loading | Audit table skeleton. |
| Empty | No events for filter. |
| Ready | Paged table with filters. |
| Permission denied | Admin only. |
| Error | Do not show a false empty history. |
| Export | Redaction preview. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `AUD-001` | Audit records are append-only; no client update/delete path exists. | P0 |
| `AUD-002` | Actor identity comes from the authenticated session/server, not a renderer string. | P0 |
| `AUD-003` | Sensitive create/update/delete, payment, stock, staff, backup/restore, and sync-resolution actions are audited. | P0 |
| `AUD-004` | Audit reads are paged, access-controlled, and redacted for export. | P1 |
| `AUD-005` | A failed audit write is visible and does not silently allow an unaudited sensitive action. | P0 |

## 7. Validation and business rules

### Validation

- Actor, action, entity, timestamp required.
- No update/delete operations.
- Filter values validated.
- Export redaction checked.

### Business rules

- Audit is a business record, not a debug log.
- No PHI in general logs; audit payload minimization per policy.
- Failed audit on a sensitive action blocks or flags the action.
- Audit rows are not silently overwritten by sync.

## 8. Permissions

- Read/export: admin.
- Write: system on behalf of authenticated actor.

## 9. Offline and data behavior

- Audit intent stored locally with the business transaction.
- Append-only sync; conflicts require investigation.

## 10. Errors and recovery

- Audit insert failure -> transaction rollback or explicit repair state.
- Duplicate -> idempotent by event ID.
- Unauthorized read -> 403.
- Export failure -> no partial file.

## 11. Edge cases

- Actor deactivated later.
- Entity deleted.
- Clock skew.
- Duplicate event.
- Large history.
- Audit payload contains sensitive value.

## 12. Acceptance criteria

- [ ] No UI/API update/delete audit path.
- [ ] Actor matches session.
- [ ] Sensitive action produces an audit row.
- [ ] Audit failure blocks/flags action.
- [ ] Export is redacted and access-controlled.

## 13. Test notes

- Integration: append-only/actor/failure.
- Security: direct update/delete attempt.
- E2E: filter/read/export.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-AUD-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/16-Local-Persistence-and-Offline-Operation|Local Persistence]]
- [[Features/17-Supabase-Sync|Sync]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

`audit_logs`; local audit/outbox state for offline actions.

## 15. Open questions

- Which fields are audit-safe?
- Retention period?
- Who can export?
- How are legacy permissive policies fixed?

## 16. Related

- [[Security/Security-Model|Security Model]]
- [[Audits/Risk-Register|Risk Register]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
