# Security Policy

> **Scope:** the Neo Child Clinic Desktop documentation repository and the shared Supabase backend it describes. No desktop application has been released. Live Supabase verification and production remediation are deferred by the project owner to a later phase.

## Reporting a security issue

Do **not** open a public issue, discussion, or pull request containing:

- patient information or any data that could identify a patient;
- credentials, tokens, project URLs, publishable/secret keys, or connection strings;
- an exploit against a live clinic system;
- database rows, screenshots containing PHI, or unredacted logs.

Report privately to the repository owner through an existing private channel. If GitHub private vulnerability reporting is enabled for this repository, use the repository's **Security** tab. The repository does not publish a security email address or a response-time SLA; do not invent one.

Include only what is necessary:

1. the affected document, component, or reported backend control;
2. the evidence class (repository source, exported metadata, or live configuration);
3. a minimal, redacted reproduction;
4. potential impact;
5. any suggested containment that does not require accessing production.

## Authorized testing boundaries

- Do not test the shared Supabase project, clinic accounts, Storage, functions, or Realtime without explicit written authorization.
- Do not run SQL, issue PostgREST requests, or exercise the exported anon path as part of documentation review.
- Do not use real patient data. Synthetic data and approved test accounts are required for any later verification.
- Do not attempt denial of service, credential stuffing, social engineering, or persistence.
- The proposed `supabase/tests/rls_role_test.sql` is non-read-only and must not be run without separate approval.

## What is already known

The current assessment is recorded in the [Security Model](docs/Knowledge_Base/Security/Security-Model.md), [Phase 0C Schema Export Review](docs/Knowledge_Base/Audits/Phase-0C-Schema-Export-Review.md), and [Risk Register](docs/Knowledge_Base/Audits/Risk-Register.md).

The highest-priority exported finding is a possible unauthenticated path to clinical and inventory tables through legacy `{public}` policies and `get_my_role()`'s `'nurse'` fallback. It is **observed in an export**, not verified against live configuration. Treat it as a possible exposure until it is confirmed or disproved; do not describe it as a confirmed production breach.

## Handling sensitive evidence

- Keep the user-supplied exports under `docs/Schemas/`; they are Git-ignored.
- Redact project identity, keys, tokens, URLs, and patient data before quoting an export.
- Store credentials only in an approved secret manager, never in this repository.
- Delete temporary files that contain PHI or credentials after use.

## Remediation expectations

Security remediation is not authorized in the documentation phase. Any future change to grants, RLS policies, functions, triggers, or Storage must be reviewed as a migration, tested with synthetic data, and verified with `anon`, non-staff authenticated, active staff, and deactivated-account roles. Follow the [Security Model](docs/Knowledge_Base/Security/Security-Model.md) and [Phase 1 Implementation Plan](docs/Knowledge_Base/Roadmap/Phase-1-Implementation-Plan.md).

## Disclosure

Do not publish details of an unverified exposure or patient data. Coordinate disclosure with the clinic owner after containment and verification. This policy does not create a legal or regulatory compliance certification.
