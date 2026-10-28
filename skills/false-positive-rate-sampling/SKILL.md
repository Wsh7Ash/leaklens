---
name: false-positive-rate-sampling
description: "Measure what proportion of your report is noise by sampling, so precision is a number in the report rather than a feeling about the tool. Use when a run produced a large candidate set and nobody has measured how much of it is real"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [confirm, precision, measurement]
---

# False-Positive Rate Sampling

> Measure what proportion of your report is noise by sampling, so precision is a number in the report rather than a feeling about the tool

**Use when:** a run produced a large candidate set and nobody has measured how much of it is real

**Avoid when:** the candidate set is small enough to review exhaustively, which removes the need to sample

## Procedure

1. Define the sample: a random selection from the accepted set, with the sample size recorded.
2. Review each sampled entry against the two-signal rule and classify it real or false.
3. Compute the real proportion and state it with the sample size, so a reader can judge the margin.
4. Repeat for a second sample if the first is small enough that the result is unstable.
5. Extrapolate to the full set only as an estimate, and label it an estimate with its sample basis.
6. Feed the false entries found into the taxonomy so the measurement improves the rules.

## Signals

- No sample was taken and the report implies all entries are real
- A sample of three entries was used to claim a precision figure
- Extrapolation is presented as a count rather than as an estimate
- False entries found during sampling were not fed back into any rule

## Patterns

**1. Sampling record**

```text
sample size: 30 random from 418 accepted | real: 26 | precision: 87% +/- margin | rule version: v7
```

**2. Extrapolation label**

```text
estimate: roughly 54 real findings in 418, based on a sample of 30; stated as an estimate, never as a count
```

**3. Feedback loop**

```text
each false entry found in sampling is added to the taxonomy with a group name, then rules are re-run against fixtures
```

## Pitfalls

- Quoting a precision number without its sample size, which makes it meaningless
- Sampling only the top of the ranked list, where precision is highest by construction
- Finding false positives during sampling and adjusting nothing afterwards

## Done when

- A precision figure with its sample size and rule version appears in the report
- False entries found during sampling are recorded in the taxonomy with a rule change

## References

- [OWASP - Measurement and verification guidance](https://owasp.org/www-project-application-security-verification-standard/)
- [NIST - Measurement discipline considerations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
