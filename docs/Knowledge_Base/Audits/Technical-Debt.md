---
title: Technical Debt
doc_status: baseline
evidence: Android KB + desktop audit + Phase 0C Supabase metadata exports (no SQL executed)
updated: 2026-10-21
---

# Technical Debt

> This register separates **inherited backend/reference debt** from **desktop delivery debt**. The desktop has no code, so it has no implementation debt yet; it has unbuilt foundations and inherited constraints.

## Register

| ID | Debt | Type | Evidence | Interest / risk | Repayment | Status |
|---|---|---|---|---|---|---|
| TD-001 | No reproducible baseline schema | Inherited | Only 9 creates for 24 tables; 15 baseline tables; six live-only columns; one missing migration (`todo_notification_events`) | Cannot rebuild, test, or recover confidently | Baseline migration + reset test | Open |
| TD-002 | RLS/grants are broad and not runtime-verified | Inherited | NSC-001/002/005/013; Phase 0C: 10 anon-reachable tables, `reminders` true, 22 full anon/auth ACLs, 21 anon-executable functions | PHI exposure, false confidence | Role-scoped policies, explicit grants, anon/non-staff negative tests | Open |
| TD-003 | Deletion/absence reconciliation is undefined; conflict semantics are partly unverified | Inherited | NCC-023/025/038 | Resurrected deletes, duplicate/lost updates | Approved deletion contract, outbox, explicit conflicts | Open |
| TD-004 | Stock arithmetic exists in client and trigger paths; live database is pre-fix | Inherited | Phase 0C: two stock triggers and old `update_batch_stock()` remain; `20261017` not applied and guard fails; NCC-027/030 open | Double-applied/corrupt stock | One ledger path, corrected trigger, server reconciliation | Open |
| TD-005 | Business dates are text | Inherited | Schema/type snapshot | Sort/timezone defects | Typed boundary + IST rules | Open |
| TD-006 | Money uses floating point in the Android client | Inherited | Shared schema is `numeric`; Android maps to `Double` | Rounding, duplicate totals | Integer minor units in desktop; boundary conversion | Open |
| TD-007 | Soft delete is inconsistent across tables | Inherited | Migration reconciliation; NCC-023 | Leaks, resurrected rows, report errors | Central soft-delete/filter policy plus deletion/absence reconciliation | Open |
| TD-008 | Backup restore is destructive and lacks an end-to-end test | Inherited | Android KB; NCC-037 fixed; crypto/validator unit tests exist | Data loss | Automated round-trip/interruption tests | Open |
| TD-009 | No desktop repository/instructions/CI | Desktop delivery | AUD-002/AUD-009/AUD-010 | Rework, uncontrolled changes | Phase 0 setup | Open |
| TD-010 | No desktop local schema/encryption decision | Desktop delivery | No ADR | Rework, PHI exposure | ADR-0002 + prototype | Open |
| TD-011 | No desktop sync contract | Desktop delivery | No ADR | Duplicate writes, unrecoverable conflicts | ADR-0003 + contract tests | Open |
| TD-012 | No packaging/signing/update/printing design | Desktop delivery | No files | Unsafe release, PHI leakage | ADR/release workstream | Open |
| TD-013 | Existing KB drifts from HEAD | Documentation | Home cites older commit; counts differ | Wrong decisions from stale facts | Docs-as-code + link checks | Open |
| TD-014 | No observability/redaction design | Desktop delivery | No logging config | PHI leakage, unsupportable failures | Error/logging spec + review | Open |
| TD-015 | No accessibility/keyboard acceptance | Desktop delivery | No UI code | Front-desk inefficiency, exclusion | Accessibility tests in DoD | Open |

## Debt policy

- New debt requires an owner, evidence, and a repayment trigger.
- Debt touching patient safety, money, stock, auth, or PHI cannot be accepted silently.
- A temporary workaround must have a removal condition and a test.
- Do not "fix" inherited schema debt in production without a migration review and backup.

## Related

[[Audits/Risk-Register|Risk Register]] · [[Audits/Initial-Audit|Initial Audit]] · [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] · [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]] · [[Database/Schema-Reconciliation|Schema Reconciliation]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Roadmap/Phase-1-Implementation-Plan|Phase 1 Implementation Plan]]
