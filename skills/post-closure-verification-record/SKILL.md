---
name: post-closure-verification-record
description: "Re-scan after the fix and record the result as dated evidence, so closure is a measured outcome rather than an assertion by whoever closed the ticket. Use when a finding has been fixed and is about to be closed"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [document, verification, closure]
---

# Post-Closure Verification Record

> Re-scan after the fix and record the result as dated evidence, so closure is a measured outcome rather than an assertion by whoever closed the ticket

**Use when:** a finding has been fixed and is about to be closed

**Avoid when:** the fix is still in progress and closure is not yet being considered

## Procedure

1. Re-run the same rule version against every location listed in the group after the fix lands.
2. Record the result per location as absent or present with the date and the rule version used.
3. Confirm the fixture corpus still passes, so an absence result is not explained by a weakened rule.
4. Check history and caches where those were in scope, since a clean working tree proves nothing about them.
5. Attach the verification record to the finding and close only when every location returns absent.
6. Keep the record past closure for the retention period, since it is the only proof the exposure ended.

## Signals

- A finding was closed on the strength of a fix commit with no re-scan
- The rule version used for verification differs from the one that found the issue
- A fixture miss went unnoticed, so an absence result may just be a weaker rule
- History was never re-checked after the working tree was cleaned

## Patterns

**1. Closure record**

```text
group E-004 | locations: 3 | re-scan 2026-10-28 rule v7: absent everywhere | fixtures: 4 of 4 hit | history: zero matches
```

**2. Rule parity**

```text
verify with the same rule version that produced the finding, or record why a different one was used
```

**3. Fixture guard**

```text
a passing fixture run in the same job proves absence means absence rather than a rule that stopped matching
```

## Pitfalls

- Closing on a commit hash instead of on evidence that the value is gone
- Re-scanning with a modified rule that no longer matches the original pattern
- Skipping history, so the value remains available from a clone after closure

## Done when

- Every location in the group returns absent on re-scan with the date and rule version recorded
- The fixture run passes in the same verification job, guarding the absence result

## References

- [NIST SP 800-53 - Assessment and monitoring records](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [OWASP - Verification methodology](https://owasp.org/www-project-application-security-verification-standard/)
