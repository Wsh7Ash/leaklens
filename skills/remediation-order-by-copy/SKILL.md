---
name: remediation-order-by-copy
description: "Sequence the fix across every copy of a value, from the most reachable to the least, so the exposure stops widening while slower copies are still being cleaned. Use when a value exists in several locations and the fix must be sequenced"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [document, remediation, sequencing]
---

# Remediation Order by Copy

> Sequence the fix across every copy of a value, from the most reachable to the least, so the exposure stops widening while slower copies are still being cleaned

**Use when:** a value exists in several locations and the fix must be sequenced

**Avoid when:** each value has exactly one location, which removes the ordering question

## Procedure

1. List all copies of each value from the deduplicated group, including history, artifacts and logs.
2. Order copies by reach: published first, then tracked, then local, then retained logs and history.
3. Rotate or remove in that order, so the copies an external reader could reach are handled first.
4. Re-scan each location after it is handled, and record the result rather than moving on by assumption.
5. Handle history and caches last but schedule them explicitly, since they are the steps most often forgotten.
6. Write the sequence into the report so the owning team sees the order and the reason for it.

## Signals

- A local file was fixed while a published copy remained reachable
- History and caches were never scheduled and survive after the report closes
- No re-scan confirms each copy was actually cleaned
- The order was chosen by file convenience rather than by reach

## Patterns

**1. Sequence**

```text
1 published repo  2 tracked files  3 build artifacts  4 local overrides  5 logs with retention  6 history and mirrors
```

**2. Per-copy close**

```text
each copy: handled at <time>, re-scan result <absent/present>; a present result keeps the group open
```

**3. Reason line**

```text
order follows reach so the exposure stops widening first; written into the report with the ordering rule
```

## Pitfalls

- Fixing the easiest file first and leaving the published copy live for days
- Never scheduling history and mirrors, which keep serving the old value
- Marking a copy handled without a re-scan showing it is actually clean

## Done when

- Every copy appears in a reach-ordered sequence with a per-copy re-scan result
- History and mirrors are scheduled explicitly rather than left implicit

## References

- [NIST SP 800-40 - Remediation sequencing](https://csrc.nist.gov/pubs/sp/800/40/r4/final)
- [OWASP - Remediation guidance](https://owasp.org/www-project-web-security-testing-guide/)
