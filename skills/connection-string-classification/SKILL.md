---
name: connection-string-classification
description: "Parse connection strings into their parts, because one string usually carries a host, a user, a credential and a database name, and each part is a separate fact to report. Use when the corpus contains connection strings for databases, caches, queues or services"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, connection-strings, databases]
---

# Connection String Classification

> Parse connection strings into their parts, because one string usually carries a host, a user, a credential and a database name, and each part is a separate fact to report

**Use when:** the corpus contains connection strings for databases, caches, queues or services

**Avoid when:** no connection-string shaped values exist anywhere in the readable tree

## Procedure

1. Identify every connection-string shape present: URL form, key-value form and driver-specific forms.
2. Parse each into components and record the host, database name, user and whether a credential component is present.
3. Classify the credential component separately from the host, since a host is usually internal while the credential is secret.
4. Check whether the string is assembled from parts at runtime, in which case record the parts rather than a literal.
5. Note whether the host points at an internal or production endpoint, which determines who must be told.
6. Record the string with its credential component redacted and a hash of it so reuse across files can still be detected.

## Signals

- A connection string embeds user and password before the host
- A string points at a production datastore from a development configuration file
- The string is assembled at runtime from environment lookups, so no literal exists
- The same credential appears in two strings for the same datastore

## Patterns

**1. Parsed record**

```text
scheme: postgres | host: internal-db.internal | db: app | user: app_rw | credential present: yes | sha256: 9c1d...
```

**2. Component split**

```text
host -> infrastructure reference (internal class); credential -> secret; user -> internal; each reported separately
```

**3. Assembly case**

```text
runtime-assembled string -> record the lookup names and the file, and mark the value as living in the store rather than in the file
```

## Pitfalls

- Reporting a whole connection string as one finding, which both over- and under-states it
- Redacting inconsistently so the same credential cannot be matched across two findings
- Missing that an internal host in a public file is its own information disclosure

## Done when

- Each connection string yields separate entries for host, user and credential with a hash for reuse checks
- Runtime-assembled strings are labelled as references with the lookup source recorded

## References

- [CWE-312 - Cleartext storage of sensitive information](https://cwe.mitre.org/data/definitions/312.html)
- [OWASP - Database security guidance](https://owasp.org/www-project-web-security-testing-guide/)
