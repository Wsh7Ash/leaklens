---
name: near-miss-false-positive-taxonomy
description: "Name the categories of thing your rules mistake for secrets, because a labelled false positive can be excluded systematically while an unlabelled one keeps coming back. Use when the same kinds of non-secret keep appearing as candidates across runs"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [confirm, false-positives, precision]
---

# Near-Miss False-Positive Taxonomy

> Name the categories of thing your rules mistake for secrets, because a labelled false positive can be excluded systematically while an unlabelled one keeps coming back

**Use when:** the same kinds of non-secret keep appearing as candidates across runs

**Avoid when:** the candidate set is already small enough that every rejection is judged individually

## Procedure

1. Group rejected candidates by why they were rejected rather than reviewing them one at a time.
2. Name each group concretely: content hashes, identifiers with readable prefixes, encoded fixtures, base64 data blobs.
3. Write one exclusion rule per group and record which group each rule targets.
4. Re-run against the fixture corpus to confirm each new exclusion still leaves real fixtures hitting.
5. Track group counts over time so a growing group is visible rather than absorbed into a total.
6. Keep one catch-all group for anything no rule explains, and review it before it grows large.

## Signals

- The same rejection reason is written out by hand many times in one run
- An exclusion rule was added that stopped a real fixture from hitting
- Group counts are never tracked, so a growing noise class is invisible
- Everything unexplained is discarded without a catch-all review

## Patterns

**1. Group table**

```text
group | count this run | exclusion rule | fixture still hits
content hashes | 412 | length plus alphabet | yes
readable identifiers | 188 | prefix allow-list | yes
base64 blobs | 61 | entropy floor | yes
```

**2. Rule-to-group binding**

```text
every exclusion rule names the group it targets, so removing a rule later is a safe, scoped change
```

**3. Catch-all review**

```text
unexplained rejections are counted and sampled before each run; a growing catch-all means a new group is forming
```

## Pitfalls

- Writing one broad exclusion that silently removes a class of real findings
- Never re-running fixtures after adding an exclusion, which is how precision is bought with recall
- Letting the catch-all become a dumping ground where real values disappear

## Done when

- Rejected candidates are grouped by reason with a named exclusion rule per group
- Every exclusion rule is confirmed to leave its fixtures hitting

## References

- [OWASP - Verification methodology](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE-546 - Suspicious pattern evaluation](https://cwe.mitre.org/data/definitions/546.html)
