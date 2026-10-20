---
title: Desktop Shell and Navigation
feature_id: PLAT
doc_status: proposed
desktop_status: Missing
android_status: Unverified
evidence: Android source + Knowledge Base
updated: 2026-10-20
---

# 01. Desktop Shell and Navigation

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Unverified. Evidence: `app/Navigation.kt`, `app/NavigationDashboardGraph.kt`, `feature/dashboard/presentation/component/AppDrawer.kt`.

**Requirement IDs:** `PLAT-001`, `PLAT-002`, `PLAT-003`, `PLAT-004`, `PLAT-005`, `PLAT-006`

## 1. Purpose and scope

Provide the signed-in desktop frame: single-instance window, navigation, global search entry, sync/offline status, update prompts, and safe session transitions.

## 2. Actors

- All staff

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Launch the app; restore a valid session or show sign-in.
2. Navigate via a persistent sidebar and keyboard shortcuts.
3. Open global patient search without leaving the current context.
4. See online/offline/sync-attention state at all times.
5. Sign out or switch account with an unsynced-write warning.
6. Receive a non-blocking update prompt.

## 5. UI states

| State | Expected behavior |
|---|---|
| Launching | Splash with no PHI; restore session/local DB; timeout to a recoverable error. |
| Signed out | Sign-in screen only; no clinical navigation. |
| Ready | Sidebar, workspace, status bar, and role-appropriate actions. |
| Offline | Cached data remains usable; local writes allowed; server-only actions explained. |
| Sync attention | Persistent badge and sync-center link; no modal trap. |
| Update available | Non-blocking prompt with version and release notes. |
| Fatal | Recovery screen with diagnostic export and safe exit. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `PLAT-001` | The app runs as a single-instance desktop shell with a signed-in and signed-out state. | P0 |
| `PLAT-002` | Navigation guards hide unavailable routes and re-check authorization on the server side. | P0 |
| `PLAT-003` | A global status surface shows online, offline, syncing, and attention-required states. | P0 |
| `PLAT-004` | Core navigation and search are fully keyboard operable and accessible. | P1 |
| `PLAT-005` | Window title, notification previews, and crash recovery do not expose PHI by default. | P0 |
| `PLAT-006` | A renderer crash or fatal local-storage error shows a safe recovery screen. | P1 |

## 7. Validation and business rules

### Validation

- No PHI in the OS window title.
- Deep links use opaque IDs.
- Unsaved changes require confirmation before navigation.

### Business rules

- UI guards are usability only; Go and RLS enforce access.
- One running instance by default; a second launch focuses the existing window.
- Offline state never blocks local clinical writes.
- Update prompts never interrupt an in-flight local transaction.

## 8. Permissions

- The visible menu is role-aware but not authoritative.
- Admin-only routes remain inaccessible to other roles even by direct binding call.

## 9. Offline and data behavior

- Shell and cached routes load offline.
- Server-only actions are disabled with a reason, not a silent failure.
- Sync status remains visible.

## 10. Errors and recovery

- Renderer crash -> error boundary with recovery.
- Local DB failure -> stop writes and offer export/exit.
- Second-instance failure -> focus existing or explain.

## 11. Edge cases

- Multiple monitors and display scaling.
- OS sleep/resume with an expired token.
- Deep link to a deleted patient.
- Second launch while the first is updating.
- High-contrast/OS font scaling.

## 12. Acceptance criteria

- [ ] Clean launch reaches sign-in without PHI.
- [ ] Offline banner appears within one second of network loss.
- [ ] A nurse cannot open staff management by URL or binding call.
- [ ] Sign-out with pending writes requires confirmation.
- [ ] Keyboard-only user can reach patient search and a patient record.

## 13. Test notes

- Component: route guards, status bar, keyboard nav.
- E2E: launch, sign-in, offline banner, sign-out warning.
- Security: direct binding call as a non-admin.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

## 14. Dependencies

- [[Features/02-Authentication-and-Session|Authentication]]
- [[Features/16-Local-Persistence-and-Offline-Operation|Local Persistence]]
- [[Features/17-Supabase-Sync|Sync]]

## 15. Open questions

- Is multi-window support required?
- Which OSes and architectures are targets?
- Is a global command palette in Phase 1?

## 16. Related

- [[Architecture/Frontend-Architecture|Frontend Architecture]]
- [[Product/Personas-and-Roles|Personas and Roles]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
