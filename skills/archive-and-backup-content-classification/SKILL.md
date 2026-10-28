---
name: archive-and-backup-content-classification
description: "Decide which compressed or backup artifacts get opened and which are skipped, because an unread archive is a coverage claim nobody has actually tested. Use when archives, database dumps or backup files exist inside the readable boundary"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, archives, coverage]
---

# Archive and Backup Content Classification

> Decide which compressed or backup artifacts get opened and which are skipped, because an unread archive is a coverage claim nobody has actually tested

**Use when:** archives, database dumps or backup files exist inside the readable boundary

**Avoid when:** the boundary excludes archives in writing and no compressed artifact is readable

## Procedure

1. List every archive and backup artifact with its type, size and whether it is tracked.
2. Decide per artifact whether to open it, using the boundary and the size as the constraint, and record the decision.
3. For opened artifacts, extract to a temporary directory outside the tree and scan the contents as a nested surface.
4. Record which members of an archive produced findings and at what depth, since a value two levels deep is still in scope.
5. Delete temporary extractions when finished and record that the deletion happened.
6. Classify artifacts that were not opened as uncovered, with the reason, rather than as clean.

## Signals

- An archive exists and no plan step decides whether to open it
- A backup dump sits in the tree and was counted as scanned because its container was listed
- Temporary extraction directories were left behind after a session
- An artifact was reported clean without ever being opened

## Patterns

**1. Artifact decision**

```text
artifact: data-backup.tgz | type: tarball | decision: open | members scanned: 142 | findings at depth: 2 | temp deleted: yes
```

**2. Unopened label**

```text
unopened artifact -> label uncovered with reason (size, boundary, tool limit); never label it clean
```

**3. Depth record**

```text
record the deepest member scanned so coverage is stated as a measured depth rather than a yes
```

## Pitfalls

- Calling an unopened archive clean because its filename looked harmless
- Leaving extracted copies of sensitive content in a temporary directory
- Reporting coverage over an archive when only its member list was read

## Done when

- Every archive has an open or uncovered decision with a reason and, if opened, a scanned depth
- Temporary extraction is confirmed deleted and recorded

## References

- [CWE-311 - Missing encryption of sensitive data](https://cwe.mitre.org/data/definitions/311.html)
- [OWASP - Data-at-rest handling guidance](https://owasp.org/www-project-top-ten/)
