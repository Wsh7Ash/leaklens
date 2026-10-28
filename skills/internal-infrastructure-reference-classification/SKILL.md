---
name: internal-infrastructure-reference-classification
description: "Classify internal hostnames, addresses and service names found in public or shared files, because infrastructure detail is its own disclosure even with no credential attached. Use when the corpus contains hostnames, IP literals, service names or internal URLs"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, infrastructure, disclosure]
---

# Internal Infrastructure Reference Classification

> Classify internal hostnames, addresses and service names found in public or shared files, because infrastructure detail is its own disclosure even with no credential attached

**Use when:** the corpus contains hostnames, IP literals, service names or internal URLs

**Avoid when:** the tree is internal-only and its readership already includes everyone who could use the detail

## Procedure

1. Extract hostnames, address literals, port numbers and service names into a counted list per file.
2. Split them into categories: public-facing, internal naming scheme, and placeholder such as localhost or example.
3. Record which files are tracked, published or mirrored outside the organization, since that decides exposure.
4. Note whether the reference includes an environment label such as staging or a region, which adds detail.
5. Check for an accompanying credential, because infrastructure detail plus a credential is one combined finding.
6. Classify by reader reach: public file outranks internal documentation, even for the same hostname.

## Signals

- A public documentation file names an internal hostname and its port
- An address literal appears with an environment label beside it
- An internal service name appears in an example that was copied into a public repository
- A credential and a host appear in the same file

## Patterns

**1. Reference record**

```text
host: db-replica-2.internal | port: 5432 | env label: prod | file: README.md | tracked: yes | published: yes
```

**2. Reader-reach rank**

```text
published outside the org > public repo > internal doc > local file; rank by who can actually read the file
```

**3. Combined flag**

```text
host plus credential in one file -> one combined finding ranked above either alone, with both components described
```

## Pitfalls

- Reporting internal hostnames as critical when only internal readers can see them
- Splitting a host and credential into two findings, which understates the combination
- Ignoring that a public README was copied into other repositories years ago

## Done when

- Each reference finding records host, category, environment label and reader reach
- Any co-located credential is recorded as a combined finding rather than a separate one

## References

- [CWE-200 - Exposure of sensitive information](https://cwe.mitre.org/data/definitions/200.html)
- [OWASP - Information disclosure guidance](https://owasp.org/www-project-web-security-testing-guide/)
