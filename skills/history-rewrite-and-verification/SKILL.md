---
name: history-rewrite-and-verification
description: "Remove a value from history deliberately and then prove it is gone, because removing a file from the working tree changes nothing about what a clone still receives. Use when a live value was found in tracked history and remains retrievable from a clone"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [harden, history, git]
---

# History Rewrite and Verification

> Remove a value from history deliberately and then prove it is gone, because removing a file from the working tree changes nothing about what a clone still receives

**Use when:** a live value was found in tracked history and remains retrievable from a clone

**Avoid when:** the value never entered history or the repository has no shared history to rewrite

## Procedure

1. Confirm from the finding record that the value exists in history, not only in the working tree.
2. Notify collaborators that history will be rewritten and agree a window, since clones will need re-cloning.
3. Choose the rewrite scope: one file, one path or every occurrence, based on the deduplicated group's location list.
4. Perform the rewrite and then re-scan history for the value hash to confirm absence rather than trusting the tool's report.
5. Expire any cached copies: run clones, mirrors, artifact storage and any service that indexed the old history.
6. Record the rewrite, the verification scan and the caches cleared, each with a date.

## Signals

- A value was deleted from the tree and the issue was closed without a history check
- A rewrite was performed but no independent re-scan confirmed the value is gone
- A mirror or CI cache still serves the pre-rewrite history
- No window was agreed, so collaborators lost work when their clones diverged

## Patterns

**1. Verification scan**

```text
re-scan history by value hash -> zero matches; the zero is the evidence, recorded with the date and the scan scope
```

**2. Cache list**

```text
caches to clear: local clones, remote mirrors, CI caches, indexed search, artifact storage; each marked done or not applicable
```

**3. Window note**

```text
rewrite window announced at <time>; collaborators re-cloned by <time>; recorded so fallout is visible
```

## Pitfalls

- Deleting a file and declaring the exposure resolved while history still serves it
- Trusting a rewrite tool's success message without an independent hash scan
- Leaving mirrors and caches in place, which keep serving the value after the rewrite

## Done when

- An independent re-scan of history returns zero matches for the value hash
- Every cache and mirror is recorded as cleared or not applicable with a date

## References

- [CWE-527 - Version control information exposure](https://cwe.mitre.org/data/definitions/527.html)
- [OWASP - Repository hygiene guidance](https://owasp.org/www-project-web-security-testing-guide/)
