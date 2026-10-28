---
name: read-only-evidence-capture
description: "Capture enough of a detection to prove it later while never copying the sensitive value itself, so the assessment cannot become the second copy of a leak. Use when a detection must be recorded in a report, a ticket or a shared document"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [scope, evidence, redaction]
---

# Read-Only Evidence Capture

> Capture enough of a detection to prove it later while never copying the sensitive value itself, so the assessment cannot become the second copy of a leak

**Use when:** a detection must be recorded in a report, a ticket or a shared document

**Avoid when:** the finding is a path with no value attached, such as a file missing an exclusion rule

## Procedure

1. Record the path, the line or offset, the class assigned by the rule and a hash or prefix of the value, never the value itself.
2. For personal records, record presence and a hash of a non-identifying region rather than any identifying field.
3. Keep the raw capture in a file excluded from version control with a defined deletion date from the retention rule.
4. Number each evidence entry and link it to the boundary version and the rule version that produced it.
5. Verify before sharing that the evidence file contains no value that would grant access or identify a person.
6. Delete transient captures once the report is filed, keeping only what the disclosure record requires.

## Signals

- A report or ticket contains a complete credential because it was pasted for context
- A raw scan output file sits in a tracked directory
- Evidence has no deletion date and will outlive its purpose
- An evidence entry cannot be tied to the rule version that produced it

## Patterns

**1. Evidence line**

```text
E-014 | path: config/settings.py | line: 42 | class: cloud-key | sha256: 3f2a... | rule v7 | boundary v3
```

**2. Value substitute**

```text
prefix 4 chars plus a hash proves sameness and allows later rotation checks without ever storing the secret
```

**3. Retention note**

```text
raw capture deleted on <date>; report entry retained; both dates recorded when the entry is written
```

## Pitfalls

- Pasting a value into a ticket that a vendor portal will retain permanently
- Keeping raw outputs in the repository, which recreates the exposure being assessed
- Omitting the rule version, so a later reader cannot tell which rule produced the line

## Done when

- No archived evidence contains a usable credential or an identifying personal field
- Every evidence entry carries a number, a rule version and a boundary version

## References

- [NIST SP 800-53 - Audit record content](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [OWASP - Sensitive data in logs](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
