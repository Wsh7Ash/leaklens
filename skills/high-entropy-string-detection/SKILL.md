---
name: high-entropy-string-detection
description: "Use entropy as a candidate generator rather than as a verdict, because an entropy threshold alone will fill the report with hashes and identifiers nobody can act on. Use when scanning content where the value format is unknown and a broad first pass is needed"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [discover, entropy, detection]
---

# High-Entropy String Detection

> Use entropy as a candidate generator rather than as a verdict, because an entropy threshold alone will fill the report with hashes and identifiers nobody can act on

**Use when:** scanning content where the value format is unknown and a broad first pass is needed

**Avoid when:** every class in scope has a known format, which makes format matching both tighter and cheaper

## Procedure

1. Choose a minimum length and an alphabet for the candidate pass, and record both with the entropy measure you used.
2. Exclude strings that are obviously not secrets: hashes of known length, identifiers with a readable prefix, checksums.
3. Rank candidates by entropy and length so the review order puts the most likely values first.
4. Sample the top, middle and bottom of the ranked list to estimate how much of it is noise before reviewing in full.
5. Record the candidate count and the sample hit rate so the rule's precision is stated rather than assumed.
6. Feed the survivors into classification rather than reporting an entropy hit as a finding on its own.

## Signals

- The candidate list is dominated by hashes, uuids and identifiers
- No sample was taken, so nobody knows the precision of the pass
- The threshold was chosen after looking at the data that it then validated
- Entropy hits are being reported directly as findings without classification

## Patterns

**1. Pass record**

```text
min length: 24 | alphabet: base64/hex | measure: Shannon bits per char >= 4.0 | candidates: 812 | sampled hit rate: 6%
```

**2. Noise exclusions**

```text
drop: sha256-length hex, uuid-shaped, well-known identifier prefixes; record each exclusion with its rule
```

**3. Ranking order**

```text
sort by entropy then length so review starts where a real value is most likely and stops when the sample says the tail is empty
```

## Pitfalls

- Reporting raw entropy hits as findings, which trains readers to ignore the report
- Tuning the threshold against the same content it will be judged on
- Ignoring sample hit rate and reviewing thousands of candidates by hand

## Done when

- Thresholds, alphabet, exclusions and the measured sample hit rate are recorded
- No entropy hit appears in the report without a classification step after it

## References

- [OWASP - Secret detection patterns](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-331 - Insufficient entropy](https://cwe.mitre.org/data/definitions/331.html)
