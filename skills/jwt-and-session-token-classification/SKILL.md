---
name: jwt-and-session-token-classification
description: "Decode the readable parts of a structured token without verifying it, so the report can state subject, scope and expiry while never treating the value as yours to use. Use when a candidate is a structured three-part token or an opaque session identifier"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, jwt, sessions]
---

# JWT and Session Token Classification

> Decode the readable parts of a structured token without verifying it, so the report can state subject, scope and expiry while never treating the value as yours to use

**Use when:** a candidate is a structured three-part token or an opaque session identifier

**Avoid when:** the corpus contains no token-shaped values at all

## Procedure

1. Split the structure into its parts and decode the header and payload without verifying any signature.
2. Record the algorithm declared in the header, the subject or audience claims, the issued-at and expiry times.
3. Never present the token to any endpoint; decoding is local and the value is never used.
4. Note whether the payload contains personal fields, which raises the class of the finding above internal.
5. Check whether the token sits alongside its signing secret in the same file, which is a materially worse combination.
6. Classify by expiry and scope: an expired token is a hygiene finding, an unexpired one with wide scope is a live risk.

## Signals

- A token decodes to an unexpired claim set with a broad scope
- The signing secret appears in the same file as the token
- The header declares a weak or unusual algorithm
- A payload carries personal fields alongside a scope claim

## Patterns

**1. Decoded record**

```text
alg: HS256 | sub: service account | scope: write | exp: 2026-11-02 (still valid) | personal fields: none | co-located secret: no
```

**2. Local-only rule**

```text
decode and read claims locally; never send the token anywhere, and state in the report that it was never used
```

**3. Combination flag**

```text
token plus signing secret in one file is recorded as one finding with a higher rank than either alone
```

## Pitfalls

- Presenting the token to an endpoint to see what it does, which is using the credential
- Reporting an expired token with the same rank as a live one
- Missing that the secret sits three lines below the token in the same file

## Done when

- Each token finding records algorithm, subject, scope, expiry and any co-located secret
- The report states explicitly that no token was presented to any endpoint

## References

- [RFC 7519 - JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519)
- [OWASP - JWT attack surface guidance](https://owasp.org/www-project-web-security-testing-guide/)
