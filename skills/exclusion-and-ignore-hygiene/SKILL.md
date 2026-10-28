---
name: exclusion-and-ignore-hygiene
description: "Review every ignore and exclusion rule against what the tree actually contains today, since an exclusion written years ago is the most common reason a scan reports clean. Use when a scan's coverage is in doubt or an exclusion rule predates the current data flows"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [harden, configuration, coverage]
---

# Exclusion and Ignore Hygiene

> Review every ignore and exclusion rule against what the tree actually contains today, since an exclusion written years ago is the most common reason a scan reports clean

**Use when:** a scan's coverage is in doubt or an exclusion rule predates the current data flows

**Avoid when:** exclusions are documented, current and each carries a written reason

## Procedure

1. List every ignore and exclusion rule in effect, with where it is defined and when it was last reviewed.
2. For each rule, list what it currently hides by running the tree against it rather than by reading the pattern.
3. Flag rules that hide regions now containing data, especially build output, exports and local overrides.
4. Replace broad patterns with narrower ones, or keep the broad pattern with a written reason beside it.
5. Re-run the scan with rules adjusted and record the delta in candidates, which shows what the rules were hiding.
6. Add the rule list to the assessment evidence so a later reader can see what was and was not read.

## Signals

- An exclusion rule dates from before a data flow was introduced
- A rule hides a region that a manual spot-check shows contains values
- No one can say when exclusion rules were last reviewed
- Removing a rule produces a large candidate delta nobody expected

## Patterns

**1. Rule review**

```text
rule: build/** | defined: 2023 | hides: 412 files | now contains data: yes | action: narrow to build/**/assets
```

**2. Delta measure**

```text
candidates with rules as-is: 418 | candidates with reviewed rules: 691 | delta 273 was hidden by exclusions
```

**3. Reason rule**

```text
every kept broad rule carries a written reason recorded with the rule, not in a separate document
```

## Pitfalls

- Reading a pattern and assuming you know what it hides without running it against the tree
- Narrowing rules without measuring the delta, so the effect stays unknown
- Documenting reasons elsewhere where nobody reviewing a rule will find them

## Done when

- Every exclusion rule has a current hides-list and a reason or a narrowed pattern
- The candidate delta from reviewing rules is recorded in the evidence

## References

- [OWASP - Configuration review guidance](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE-693 - Protection mechanism failure](https://cwe.mitre.org/data/definitions/693.html)
