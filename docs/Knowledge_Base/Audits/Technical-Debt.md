---
title: Technical Debt
doc_status: baseline
evidence: Android KB + desktop audit
updated: 2026-10-20
---

# Technical Debt

> This register separates **inherited backend/reference debt** from **desktop delivery debt**. The desktop has no code, so it has no implementation debt yet; it has unbuilt foundations and inherited constraints.

## Register

| ID | Debt | Type | Evidence | Interest / risk | Repayment | Status |
|---|---|---|---|---|---|---|
| TD-001 | No reproducible baseline schema | Inherited | Only 9 creates for 24 tables | Cannot rebuild, test, or recover confidently | Baseline migration + reset test | Open |
| TD-002 | RLS is broad/single-clinic and partly unverified | Inherited | NSC-001/002/005/013 | PHI over-access, false confidence | Role-scoped policies + live tests | Open |
| TD-003 | Sync is last-write-wins with weak conflict/tombstone handling | Inherited | Android sync findings | Resurrected deletes, duplicate/lost updates | Outbox, tombstones, explicit conflicts | Open |
| TD-004 | Stock arithmetic exists in client and trigger paths | Inherited | Inventory findings; trigger double-apply | Stock corruption | One ledger path, server reconciliation | Open |
| TD-005 | Business dates are text | Inherited | Schema/type snapshot | Sort/timezone defects | Typed boundary + IST rules | Open |
| TD-006 | Money uses floating point | Inherited | Schema/reference models | Rounding, duplicate totals | Integer minor units in desktop; boundary conversion | Open |
| TD-007 | Soft delete is inconsistent across tables | Inherited | Migration reconciliation | Leaks, resurrected rows, report errors | Central tombstone/filter policy | Open |
| TD-008 | Backup restore is destructive and untested | Inherited | Android KB | Data loss | Automated round-trip/interruption tests | Open |
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

[[Audits/Risk-Register|Risk Register]] · [[Audits/Initial-Audit|Initial Audit]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Roadmap/Phase-1-Implementation-Plan|Phase 1 Implementation Plan]]
