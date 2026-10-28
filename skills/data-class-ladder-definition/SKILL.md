---
name: data-class-ladder-definition
description: "Agree the ladder of data classes and what each one permits, so a detection is judged against a stated rule instead of against whoever reads the report. Use when findings will be ranked and no agreed ladder defines what separates public from personal from secret"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [scope, classification, policy]
---

# Data Class Ladder Definition

> Agree the ladder of data classes and what each one permits, so a detection is judged against a stated rule instead of against whoever reads the report

**Use when:** findings will be ranked and no agreed ladder defines what separates public from personal from secret

**Avoid when:** the organization already publishes a classification policy with handling rules per class

## Procedure

1. Adopt or write a short ladder: public, internal, personal, secret, and state what each class means in one sentence.
2. Define the handling rule for each class, particularly whether detection alone is permitted or whether reading a value is allowed.
3. Record which classes are detect-only for this engagement, since that single decision shapes every later confirmation step.
4. Agree how a value straddling two classes is ranked, because most real findings sit between them.
5. Note the retention rule for evidence per class, so a captured value has a defined lifetime from the moment it is written.
6. Store the ladder beside the boundary document and reference it from every finding you record.

## Signals

- Two readers rank the same finding differently with no policy to settle it
- A class is defined but no handling rule says what you may do with it
- Evidence retention differs per finding only because individuals decided differently
- A straddling value has no defined ranking and gets argued each time

## Patterns

**1. Ladder definition**

```text
public: fine to publish
internal: harms nobody outside if exposed, still not published
personal: identifies or contacts a person
secret: grants access if used; detect-only in this engagement
```

**2. Handling column**

```text
class | read value | record value | retain
detect-only: detect yes, record no, retain no
personal: detect yes, record hash only, retain until report
```

**3. Straddle rule**

```text
a token inside a personal record ranks as the higher of the two classes and inherits the stricter handling rule
```

## Pitfalls

- Publishing a secret value in a report that a ticket system will retain forever
- Defining classes with no handling column, so every reader improvises
- Ranking a straddling value by the lower class because that keeps the report short

## Done when

- A ladder with a handling column and a retention rule is written and referenced by findings
- The straddle rule is stated, and at least one finding cites it

## References

- [NIST SP 800-60 - Information categorization](https://csrc.nist.gov/pubs/sp/800/60/v1r1/final)
- [OWASP - Sensitive data discovery](https://owasp.org/www-project-web-security-testing-guide/)
