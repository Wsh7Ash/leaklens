---
name: value-never-used-verification
description: "Confirm a finding from local evidence alone and state in the report that the value was never presented anywhere, because using the credential to prove it exists changes the incident. Use when a real value has been found and the temptation to test it exists"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [confirm, ethics, method]
---

# Value Never Used Verification

> Confirm a finding from local evidence alone and state in the report that the value was never presented anywhere, because using the credential to prove it exists changes the incident

**Use when:** a real value has been found and the temptation to test it exists

**Avoid when:** the owner explicitly commissions an active test and provides a controlled environment for it

## Procedure

1. Confirm the finding from format, context and location evidence, all of which are local operations.
2. Record explicitly in the evidence entry that the value was not presented to any endpoint.
3. Where liveness matters, use only non-network evidence such as configuration, dates or companion metadata.
4. If an active test were ever commissioned, record that commissioning separately from the finding itself.
5. State the confirmation basis in the report so a reviewer knows exactly how the claim was established.
6. Keep the value out of every artifact produced, since confirmation never requires writing it down.

## Signals

- Someone suggests trying the value against an endpoint to see if it works
- A report claims a credential is live without saying how that was established
- A value appears in a shell history from being typed during a test
- An active test was performed without a written commission

## Patterns

**1. Confirmation basis**

```text
basis: format match + key context + tracked location; network use: none; stated explicitly in the report entry
```

**2. Liveness substitute**

```text
judge from local evidence: config names the service, dates show recent use, companion metadata identifies the purpose
```

**3. Commission record**

```text
if an active test is commissioned: record who commissioned it, the environment and the date, as a separate entry
```

## Pitfalls

- Testing a credential against a live service to strengthen a report, which turns exposure into use
- Leaving the value in shell history while testing, which creates a second copy
- Writing that a credential is live without stating the evidence that supports it

## Done when

- Every real-value finding records a confirmation basis and an explicit no-network-use statement
- Any active test is documented as separately commissioned with owner, environment and date

## References

- [NIST - Evidence-based assessment practice](https://csrc.nist.gov/publications/detail/sp/800-86/final)
- [OWASP - Ethical testing boundaries](https://owasp.org/www-project-web-security-testing-guide/)
