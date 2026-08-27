# Lumen Nation Build Plan

## Current state

The existing Lumen Nation core is a Flask + SQLite application.

Existing functionality includes:

- users
- profiles
- timeline
- issues
- resources
- connections
- chat
- local assistant
- issue/resource matching

## Implementation order

1. Preserve existing backend behavior.
2. Normalize database access.
3. Add validation boundaries.
4. Add authentication.
5. Add authorization.
6. Add privacy/data classification.
7. Add evidence/provenance.
8. Add counsel orchestration.
9. Add crisis-safety workflow.
10. Add messaging.
11. Add identity verification.
12. Add client application.
13. Add automated security tests.
14. Build release APK.
15. Conduct controlled beta.
16. Perform release audit.

## Security principle

The client is untrusted.

AI output is untrusted.

External content is untrusted.

User identity does not equal user authority.

Verification does not equal truth.

Popularity does not equal evidence.

## Crisis principle

Lumen may provide supportive information and navigation.

Lumen must not falsely represent AI as a human.

A high-risk interaction must provide an appropriate path toward
real human assistance.

Any escalation mechanism must be explicit, narrow, auditable,
and privacy-preserving.

## Identity principle

Identity verification is an optional verification signal.

It must not be converted into:

- credibility score;
- social rank;
- access class;
- political classification;
- economic class;
- presumed truthfulness.

## Legal-information principle

Lumen should distinguish:

- what a law says;
- what rights a source recognizes;
- what rights a user claims;
- what jurisdiction applies;
- what remains uncertain.

The system should not silently convert legal information into
legal advice or a claim of guaranteed legal outcome.
