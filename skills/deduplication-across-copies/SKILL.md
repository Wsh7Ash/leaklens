---
name: deduplication-across-copies
description: "Collapse one value found in many locations into a single finding with N rotation targets, so the report counts exposures rather than file lines. Use when the same value or the same logical secret appears in more than one file or region"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [confirm, deduplication, reporting]
---

# Deduplication Across Copies

> Collapse one value found in many locations into a single finding with N rotation targets, so the report counts exposures rather than file lines

**Use when:** the same value or the same logical secret appears in more than one file or region

**Avoid when:** each finding is already unique by value and location

## Procedure

1. Group findings by a stable identity: the value hash, or the logical secret when a value was assembled differently in two places.
2. For each group record every location, separating tracked files, artifacts, history and logs.
3. Pick a canonical finding entry and cross-reference the other locations inside it rather than repeating the detail.
4. Count locations as rotation targets, since each one must be handled for the rotation to be complete.
5. Record how the copies were matched, so a reader can tell value identity from logical identity.
6. Re-check after remediation that every location in the group has been handled, not only the canonical one.

## Signals

- One value appears in source, a log and an artifact and is reported as three unrelated findings
- Two locations hold the same secret assembled differently, so a literal match misses one
- Rotation was completed on the canonical location while another copy remained
- The report counts file lines rather than distinct exposures

## Patterns

**1. Group entry**

```text
identity: sha256 3f2a... | locations: 3 (src/client.py:18, log/app.log:902, build/bundle.js) | canonical: src/client.py:18 | rotation targets: 3
```

**2. Match basis**

```text
basis: value hash | logical match: same secret assembled at runtime in two files, matched by lookup name
```

**3. Close-out rule**

```text
the finding closes only when every listed location is verified handled; one outstanding location keeps it open
```

## Pitfalls

- Reporting duplicates as separate findings, which makes the exposure look larger and the fix incomplete
- Matching only on literal value and missing a copy assembled differently
- Closing a finding after the canonical location was fixed while other copies remain

## Done when

- Each group has one canonical entry with all locations cross-referenced as rotation targets
- The match basis, value or logical, is recorded per group

## References

- [NIST SP 800-53 - Information consistency controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [OWASP - Secrets management guidance](https://owasp.org/www-project-web-security-testing-guide/)
