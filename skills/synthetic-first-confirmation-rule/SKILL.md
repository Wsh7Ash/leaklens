---
name: synthetic-first-confirmation-rule
description: "Confirm every detection technique against a planted synthetic value first, so the technique is proven before it ever touches a real record. Use when a detection rule is being introduced or changed and its false-positive behaviour is unmeasured"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [scope, validation, method]
---

# Synthetic First Confirmation Rule

> Confirm every detection technique against a planted synthetic value first, so the technique is proven before it ever touches a real record

**Use when:** a detection rule is being introduced or changed and its false-positive behaviour is unmeasured

**Avoid when:** a golden corpus of synthetic fixtures already covers each class and the rule passes against it

## Procedure

1. Create synthetic fixtures for each class: a fake cloud key, a fake token, a fake personal record, each clearly marked.
2. Plant them in a temporary tree you own, never in the repository under assessment.
3. Run the rule against the fixtures and require a hit on every one before the rule is used for real content.
4. Introduce near-miss fixtures, such as an identifier that resembles a token, and require the rule to stay quiet.
5. Record the fixture set with the rule version so a later rule change can be measured against the same corpus.
6. Only after both hit and quiet behave as expected, run the rule against in-scope content.

## Signals

- A rule was written and applied directly to production content without a fixture test
- Near-miss fixtures produce hits, which means every real finding will need manual clearing
- The fixture set exists in someone's shell history rather than in a file
- A rule change shipped with no re-run against the corpus

## Patterns

**1. Fixture row**

```text
class | fixture | expected | observed
cloud-key | AKIA...fixture | hit | hit
token | ghp_fixture | hit | hit
near-miss | order_reference_123 | quiet | hit  <- rule too broad
```

**2. Two-sided test**

```text
every rule needs both a hit requirement and a quiet requirement; only the hit side leaves precision unmeasured
```

**3. Version binding**

```text
store the fixture set with a rule version so a later change is measured against the identical corpus
```

## Pitfalls

- Tuning a rule against real content until it stops firing, which is how a real secret gets tuned out
- Testing only the positive case and accepting a rule that flags half the repository
- Keeping fixtures in an ad-hoc location so they are unavailable when the rule changes

## Done when

- A fixture set with hit and quiet expectations exists per class and passes before real content is scanned
- The fixture set is stored with the rule version that last passed against it

## References

- [OWASP - Verification and testing guidance](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE-546 - Suspicious comment and pattern checking](https://cwe.mitre.org/data/definitions/546.html)
