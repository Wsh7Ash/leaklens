---
name: format-plus-context-corroboration
description: "Require a format match and a surrounding context signal before calling a candidate real, because either alone produces a report full of noise or one full of misses. Use when candidates have been generated and each must be judged as a real value or a false positive"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [confirm, precision, detection]
---

# Format Plus Context Corroboration

> Require a format match and a surrounding context signal before calling a candidate real, because either alone produces a report full of noise or one full of misses

**Use when:** candidates have been generated and each must be judged as a real value or a false positive

**Avoid when:** a candidate already has an independent confirmation that does not rely on its shape

## Procedure

1. For each candidate record the format evidence: prefix, length and alphabet that matched.
2. Record the context evidence: the key name it sits under, the file region and the surrounding code's use of it.
3. Accept as a real value only when at least one format signal and one context signal agree.
4. Log candidates rejected by this rule with the reason, so a later reader can see what was excluded and why.
5. Sample the rejected set to check that real values are not being discarded by an over-strict context rule.
6. Record precision for the rule as accepted over reviewed, so the rule's quality is a stated number.

## Signals

- A candidate matches format but sits under a key named example or sample
- A strong key name holds a value whose shape does not match any known format
- The rejected set was never sampled, so over-strict exclusion would go unnoticed
- No precision figure exists for a rule that determines what reaches the report

## Patterns

**1. Two-signal rule**

```text
accept only when format evidence and context evidence both hold; record both signals per candidate
```

**2. Rejection log**

```text
candidate #214 | format match: yes | context: key name 'example_password' | verdict: rejected | sampled later: clean
```

**3. Precision figure**

```text
accepted 18 of 61 reviewed -> precision 30%; stated with the rule version that produced it
```

## Pitfalls

- Accepting on format alone and filling the report with hashes and identifiers
- Accepting on key name alone and reporting every example value in the documentation
- Never sampling the rejected set, which is how a real secret gets tuned away

## Done when

- Every accepted candidate records both format and context evidence
- A precision figure with the rule version is recorded and the rejected set has been sampled

## References

- [OWASP - Secret detection accuracy](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-798 - Use of hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)
