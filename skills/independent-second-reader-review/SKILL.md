---
name: independent-second-reader-review
description: "Have a second person re-derive a sample of your classifications without seeing your reasoning, because agreement on the easy cases proves nothing about the hard ones. Use when the finding set is large enough that a single reader's judgement drives the whole report"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [confirm, review, precision]
---

# Independent Second Reader Review

> Have a second person re-derive a sample of your classifications without seeing your reasoning, because agreement on the easy cases proves nothing about the hard ones

**Use when:** the finding set is large enough that a single reader's judgement drives the whole report

**Avoid when:** the finding set is a handful of entries reviewed jointly as they were found

## Procedure

1. Select a sample covering every class and both high- and low-confidence findings, with the sample size recorded.
2. Give the second reader the evidence entries without your classification or rank.
3. Have them classify and rank each entry independently using the same ladder.
4. Compare and record agreement as a proportion, naming each disagreement with both readings.
5. Resolve disagreements by referring to the ladder text rather than by preference, and amend the ladder if it was ambiguous.
6. Feed each ambiguity found back into the ladder so the next run starts from a clearer rule.

## Signals

- Only the obvious findings were reviewed, so agreement says nothing about the hard ones
- The second reader saw your reasoning first, which anchors their judgement
- Disagreements were resolved by deferring to the original author
- An ambiguity found during review was never written back into the ladder

## Patterns

**1. Review record**

```text
sample: 18 of 418, spanning all classes | agreement: 14/18 (78%) | disagreements: 4, each with both readings
```

**2. Blind rule**

```text
the second reader receives evidence only, never the classification; seeing your rank first turns review into confirmation
```

**3. Ladder feedback**

```text
disagreement caused by ambiguous ladder text -> the ladder text changes in the same change that resolves the finding
```

## Pitfalls

- Reviewing only the easy findings and reporting a high agreement figure
- Settling a disagreement by deferring to the first reader rather than to the ladder
- Finding an ambiguity and leaving it for the next assessment to rediscover

## Done when

- A blind sample spanning all classes has an agreement figure with each disagreement recorded
- Ambiguities found are written back into the ladder text

## References

- [NIST - Quality review considerations](https://csrc.nist.gov/publications/detail/sp/800-86/final)
- [OWASP - Verification methodology](https://owasp.org/www-project-application-security-verification-standard/)
