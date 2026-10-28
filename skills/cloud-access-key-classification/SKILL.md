---
name: cloud-access-key-classification
description: "Separate a cloud access key identifier from the secret half of the pair, because only one half is unusable on its own and the two demand different responses. Use when a candidate matches a cloud provider key format or an assignment named like an access key"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, cloud, credentials]
---

# Cloud Access Key Classification

> Separate a cloud access key identifier from the secret half of the pair, because only one half is unusable on its own and the two demand different responses

**Use when:** a candidate matches a cloud provider key format or an assignment named like an access key

**Avoid when:** the corpus contains no cloud provider credentials of any kind

## Procedure

1. Identify which half you have: the public identifier that pairs with a secret, or the secret value itself.
2. Record the provider, the identifier prefix, the path and line, and the region the file belongs to.
3. Check whether the paired secret appears anywhere in the corpus, since an identifier alone still narrows an attack surface.
4. Determine whether the key is active, disabled or merely a placeholder, using only non-network means such as configuration or documentation.
5. Note whether the key appears in tracked history, which decides whether a rewrite is needed after rotation.
6. Classify severity by half: identifier as internal, secret as secret, and state which one you found.

## Signals

- A key identifier appears without its secret half anywhere in the corpus
- Both halves appear together in the same file
- The key looks like a legacy format that predates the current rotation policy
- The identifier appears in tracked history after being removed from the working tree

## Patterns

**1. Half record**

```text
half: identifier | provider: cloud | prefix: AKIA | path: config/settings.py:42 | paired secret found: no
```

**2. Severity by half**

```text
identifier alone -> internal, useful for attribution; secret alone or both -> secret, rotation required before publication
```

**3. History flag**

```text
identifier removed from tree but present in history -> rewrite flagged as a separate remediation item
```

## Pitfalls

- Reporting an identifier as a full credential and inflating the severity
- Rotating only the half you found while the pair remains valid elsewhere
- Leaving history untouched after removing a secret from the working tree

## Done when

- Each key finding states which half was found, the provider and whether a paired secret exists
- History presence is recorded per finding as a separate remediation item

## References

- [OWASP - Cloud security misconfiguration guidance](https://owasp.org/www-project-cloud-security/)
- [CWE-798 - Use of hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)
