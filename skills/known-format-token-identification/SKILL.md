---
name: known-format-token-identification
description: "Match the documented prefixes and lengths of well-known credentials first, because a format match is cheap, precise and far easier to rank than an entropy hit. Use when scanning content for credentials issued by platforms that publish a recognisable format"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [discover, detection, tokens]
---

# Known-Format Token Identification

> Match the documented prefixes and lengths of well-known credentials first, because a format match is cheap, precise and far easier to rank than an entropy hit

**Use when:** scanning content for credentials issued by platforms that publish a recognisable format

**Avoid when:** the secrets in scope are self-generated values with no published format at all

## Procedure

1. List the platforms whose credentials could appear in this corpus and look up each documented prefix and length.
2. Encode those formats as rules with the fixture set from the synthetic-first step, and require every fixture to hit.
3. Run the format pass before the entropy pass so precise candidates are reviewed first.
4. Handle prefixes that overlap with ordinary words by requiring an exact prefix match plus a length bound.
5. Record a hit with its platform, the path and line, and the rule version, never the value.
6. Note formats you looked for and did not find, so absence is a recorded result rather than an omission.

## Signals

- A format rule fires on ordinary prose because the prefix check has no length bound
- Credentials from a platform in use across the company are absent from the rule list
- A rule passes without ever having been tested against a planted fixture
- Overlapping prefixes produce a large false-positive group in comments and docs

## Patterns

**1. Format rule**

```text
platform: version-control token | prefix: ghp_ | length: 36..44 | fixture: ghp_fixture0000000000000000000000 | expected: hit
```

**2. Review order**

```text
format hits first, then entropy survivors, then structural matches; the order is chosen by precision, not by ease of writing the rule
```

**3. Absence record**

```text
formats checked and not found: <list>; recorded so a later reader knows they were searched for
```

## Pitfalls

- Writing format rules from memory and getting a length or prefix subtly wrong
- Reporting a prefix hit in prose where a length bound would have excluded it
- Never recording which formats were searched, so absence is indistinguishable from not looking

## Done when

- Every platform rule has a fixture that hits and a length bound that keeps prose quiet
- Formats searched but not found are listed as a recorded result

## References

- [OWASP - Secrets in source code](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-798 - Use of hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)
