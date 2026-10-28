---
name: oauth-client-credential-classification
description: "Classify application credentials separately from user tokens, since a client secret acts as the application itself and its rotation path runs through every grant it holds. Use when a candidate resembles an application client identifier or its secret"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, oauth, credentials]
---

# OAuth Client Credential Classification

> Classify application credentials separately from user tokens, since a client secret acts as the application itself and its rotation path runs through every grant it holds

**Use when:** a candidate resembles an application client identifier or its secret

**Avoid when:** the corpus contains no application credentials of any kind

## Procedure

1. Separate the client identifier, which is often public, from the client secret, which never is.
2. Record which identity provider is in use and which flow the credential belongs to, from configuration context.
3. Check for redirect URIs configured alongside, since a permissive redirect list compounds the finding.
4. Note whether the credential appears in a tracked file, an artifact or history.
5. List the rotation path: provider console, application configuration, every environment and any stored grant.
6. Classify the secret as secret and the identifier as internal, and report them as two related entries.

## Signals

- A client secret sits in a tracked configuration file
- A redirect URI list includes a wildcard or a broad pattern
- The client identifier is reported with the same rank as the secret
- Rotation requires a provider console step nobody has access to

## Patterns

**1. Pair record**

```text
idp: major provider | flow: authorization code | client id: public, tracked (expected) | client secret: present, tracked (finding) | redirect list: 1 exact URI
```

**2. Two entries**

```text
identifier -> internal entry; secret -> secret entry; both cross-referenced so a reader sees them together
```

**3. Rotation path**

```text
steps: provider console, app config, environments, stored grants; each step has an owner or is marked blocked
```

## Pitfalls

- Reporting the client identifier as a credential, which is wrong and wastes reviewer time
- Fixing the file while the provider-side secret remains unchanged
- Overlooking a permissive redirect URI that makes the credential easier to exercise

## Done when

- Client identifier and secret are reported as separate cross-referenced entries
- The rotation path is listed with an owner or an explicit blocker per step

## References

- [RFC 6749 - OAuth 2.0 client credentials](https://www.rfc-editor.org/rfc/rfc6749)
- [OWASP - OAuth security guidance](https://owasp.org/www-project-web-security-testing-guide/)
