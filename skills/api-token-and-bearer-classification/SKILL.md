---
name: api-token-and-bearer-classification
description: "Classify bearer-style tokens by issuer, scope and expiry, so the report can say what a reader of the file could actually do with the value. Use when a candidate matches a published token format or sits inside an authorization header construction"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, tokens, authorization]
---

# API Token and Bearer Classification

> Classify bearer-style tokens by issuer, scope and expiry, so the report can say what a reader of the file could actually do with the value

**Use when:** a candidate matches a published token format or sits inside an authorization header construction

**Avoid when:** the corpus holds no token-format values and no header construction of any kind

## Procedure

1. Identify the issuer from the prefix and record it, since scope conventions differ by platform.
2. Record where it sits: source file, configuration, log, fixture or history, because location changes the fix.
3. Look for scope or permission indicators nearby in code or configuration to estimate what the token could do.
4. Note any expiry metadata associated with the token, and whether a value with no expiry path is in use.
5. Check whether the same value appears in more than one location, since each copy is a separate rotation target.
6. Classify by estimated capability, not by length, and state the estimate as an estimate.

## Signals

- A token sits in a tracked file with no expiry handling anywhere in the code
- The same value appears in a source file and in a log
- Scope indicators suggest a permission set wider than the component needs
- A fixture directory contains what looks like a live token rather than a marked test value

## Patterns

**1. Token record**

```text
issuer: code-hosting | prefix: ghp_ | location: src/client.py:18 + log/app.log:902 | scope hint: repo write | expiry: none found
```

**2. Capability note**

```text
state what the file's own code does with the token; that is the floor of what a reader of the file could do
```

**3. Copy count**

```text
one value, N locations -> N rotation targets, each listed separately so none is missed during rotation
```

## Pitfalls

- Reporting a token without tracing what the code does with it, which leaves severity unarguable
- Missing a second copy in a log and rotating only the source location
- Treating a fixture token as live without checking the surrounding markers

## Done when

- Each token finding records issuer, location list, scope hint and expiry status
- Rotation targets are enumerated as one entry per location

## References

- [OWASP - Broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [CWE-798 - Use of hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)
