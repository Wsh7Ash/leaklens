---
name: repository-surface-enumeration
description: "Map every place in a repository that can carry a value: source, configuration, fixtures, generated output and history, so a scan does not quietly skip the class most likely to hold one. Use when a repository is in scope and no one has listed which of its regions are readable and which contain data"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [discover, inventory, repository]
---

# Repository Surface Enumeration

> Map every place in a repository that can carry a value: source, configuration, fixtures, generated output and history, so a scan does not quietly skip the class most likely to hold one

**Use when:** a repository is in scope and no one has listed which of its regions are readable and which contain data

**Avoid when:** the owner supplies a manifest stating each region's contents and data class

## Procedure

1. List the regions that exist: tracked source, untracked local files, generated output, vendored dependencies, archives and history.
2. Classify each region by likelihood of holding values: configuration and fixtures high, vendored code low but large.
3. Check whether generated output is scanned at all, since build directories are frequently excluded by an old ignore rule.
4. Note archives and bundles, because a compressed copy will never match a pattern that reads plain text.
5. Include commit history in the plan, since a removed value usually still exists there.
6. Write the surface as a table of region, class, scanned or not and the reason for any skip.

## Signals

- An ignore rule excludes build output from an era when it contained no data
- Archives are present but the tool reads only plain text
- History is not part of the scan plan even though values were removed last quarter
- Untracked local files exist that no plan step covers

## Patterns

**1. Surface row**

```text
region | class | scanned | reason
tracked source | internal | yes | -
build output | internal | no | ignore rule from 2023
archives | unknown | no | tool reads plain text only
history | internal | planned | remediation check
```

**2. Skip discipline**

```text
every unscanned region carries a written reason; an unscanned region with no reason is a gap, not a decision
```

**3. Archive note**

```text
list archive formats present and state whether they were expanded or deliberately skipped
```

## Pitfalls

- Accepting an inherited ignore rule without checking what it excludes today
- Reporting coverage over tracked files while archives and history went unread
- Scanning vendored dependencies so noisily that real findings are buried

## Done when

- A surface table covers every region with class, scanned status and reason for any skip
- Archives and history each have an explicit decision recorded

## References

- [OWASP - Source code analysis guidance](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-527 - Version control information exposure](https://cwe.mitre.org/data/definitions/527.html)
