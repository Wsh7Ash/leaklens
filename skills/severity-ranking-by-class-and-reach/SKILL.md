---
name: severity-ranking-by-class-and-reach
description: "Rank findings from two axes at once, what the value is and who can already read it, because either axis alone systematically misorders the work. Use when findings span several classes and locations and need a single priority order"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [confirm, severity, triage]
---

# Severity Ranking by Class and Reach

> Rank findings from two axes at once, what the value is and who can already read it, because either axis alone systematically misorders the work

**Use when:** findings span several classes and locations and need a single priority order

**Avoid when:** the owner supplies a ranking policy that already covers both axes

## Procedure

1. Assign each finding its class from the ladder: internal, personal or secret.
2. Assign each finding its reach: local file, tracked repository, published repository or external destination.
3. Rank on the pair, giving reach the deciding weight when two findings share a class.
4. Record the two inputs beside the rank so a reader can re-derive it rather than accept it.
5. Check the resulting order against the remediation order by copy, since a reachable secret should not sit below a stored personal record.
6. Re-rank after any change in reach, because moving a file changes the priority without changing the value.

## Signals

- Findings are ranked by class alone, putting a stored secret above a published one
- A rank appears in the report with no record of its two inputs
- Reach changed after ranking, such as a file being published mid-assessment
- The ranking order and the remediation order disagree without explanation

## Patterns

**1. Rank matrix**

```text
class \ reach | local | tracked | published
secret | high | critical | critical
personal | medium | high | critical
internal | low | medium | high
```

**2. Input record**

```text
finding E-004 | class: secret | reach: published repository | rank: critical | inputs recorded for re-derivation
```

**3. Re-rank trigger**

```text
a reach change during the assessment triggers an immediate re-rank, noted with the time it happened
```

## Pitfalls

- Ranking purely on class, which buries the published finding under stored ones
- Presenting a rank without its inputs, so nobody can challenge or reproduce it
- Never re-ranking when a file moves from local to published during the work

## Done when

- Every finding records class, reach and the rank derived from both
- The ranking order is reconciled with the remediation order, or the difference is explained

## References

- [OWASP - Risk rating methodology](https://owasp.org/www-community/OWASP_Risk_Rating_Methodology)
- [CVSS - Qualitative severity mapping](https://www.first.org/cvss/)
