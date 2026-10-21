---
title: Application Updates
feature_id: UPD
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 22. Application Updates

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `feature/update/`, `AppUpdateManager.kt`, `supabase/functions/notify-update/`.

**Requirement IDs:** `UPD-001`, `UPD-002`, `UPD-003`, `UPD-004`, `UPD-005`

## 1. Purpose and scope

Check for, verify, install, and roll back desktop updates safely without interrupting clinical work or exposing the update channel to tampering.

### User stories

- As a staff member, I can defer an update until my current work is safe.
- As an admin, I can verify a signed update and recover from a failed release.

## 2. Actors

- All staff
- Admin (deployment)

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Check for an update manually or on a schedule.
2. Show version/release notes and compatibility.
3. Download and verify signature/checksum.
4. Install with explicit consent when safe.
5. Roll back to the previous version if needed.

## 5. UI states

| State | Expected behavior |
|---|---|
| Checking | Non-blocking progress. |
| Up to date | Version/date. |
| Available | Version, notes, size, compatibility. |
| Downloading | Progress/cancel. |
| Verifying | Signature check. |
| Ready to install | Consent; warn about restart. |
| Failed | Current version intact; retry/support. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `UPD-001` | Updates are signed and verified before installation. | P0 |
| `UPD-002` | Version checks prevent accidental downgrade and unsupported OS installs. | P0 |
| `UPD-003` | An update never interrupts an active local transaction or unsynced write. | P0 |
| `UPD-004` | A failed/tampered update leaves the current version intact. | P0 |
| `UPD-005` | Rollback to the previous installed version is possible. | P1 |

## 7. Validation and business rules

### Validation

- Signature valid.
- Version monotonic.
- OS/architecture supported.
- Enough disk.
- No active write/unsynced state without safe handoff.

### Business rules

- No unsigned update.
- No silent install during clinical work.
- No PHI in update telemetry.
- Rollback artifact retained.
- Changelog reviewed before rollout.

## 8. Permissions

- All users may check; admin controls deployment channel/policy.
- Installing may require admin on managed devices.

## 9. Offline and data behavior

- Check fails gracefully; current version works.
- Downloaded update can wait.

## 10. Errors and recovery

- Bad signature -> abort/delete.
- Partial download -> retry.
- Disk full -> abort.
- Downgrade -> block.
- Active sync -> defer.

## 11. Edge cases

- Update during offline work.
- Proxy/firewall.
- Multiple OS users.
- Rollback with a newer DB schema.
- Unsupported OS.

## 12. Acceptance criteria

- [ ] Tampered update rejected.
- [ ] Version monotonic.
- [ ] Current version intact on failure.
- [ ] No update during an active transaction.
- [ ] Rollback restores previous build.

## 13. Test notes

- Harness: signature/version/disk/partial.
- E2E: defer during sync.
- Manual: install/rollback on each OS.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-UPD-*`). No test is implemented or executed.

## 14. Dependencies

- [[Releases/Release-Checklist|Release Checklist]]
- [[Decisions/ADR-0006-Testing-and-Release|ADR-0006]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

No business table. Update manifest/version metadata and the application binary only.

## 15. Open questions

- Update feed/provider?
- Signing/notarization per OS?
- Admin-controlled vs user-initiated?
- Rollback window?

## 16. Related

- [[Security/Security-Model|Security Model]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
