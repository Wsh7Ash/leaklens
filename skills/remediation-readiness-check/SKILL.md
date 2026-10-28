---
name: remediation-readiness-check
description: "Verify before reporting that every finding has an owner, a destination and a stated fix, so the report hands over work rather than observations. Use when the finding set is complete and about to be handed to the owning team"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [confirm, handover, remediation]
---

# Remediation Readiness Check

> Verify before reporting that every finding has an owner, a destination and a stated fix, so the report hands over work rather than observations

**Use when:** the finding set is complete and about to be handed to the owning team

**Avoid when:** findings are delivered to an audience that supplies their own owners and fixes

## Procedure

1. Attach an owner to every finding, or mark it unowned and escalate, because an unowned finding does not get fixed.
2. State the fix for each: rotate, remove, redact, restrict reach, or accept with a reason.
3. Confirm each fix names its target locations from the deduplicated group, not only the canonical file.
4. Check that reach-reducing steps, such as unpublishing, are included where reach drove the rank.
5. Record the expected verification for each fix, so closure has a defined test rather than a claim.
6. List findings that cannot yet be fixed with the blocker, since an unfixable finding needs a decision, not a status.

## Signals

- A finding has no owner and no stated fix
- The fix names one location while the group holds three
- A reach-driven rank has no reach-reducing step attached
- Closure has no defined verification, only an assertion that it was done

## Patterns

**1. Readiness row**

```text
finding | owner | fix | targets | verification
E-004 | platform | rotate + unpublish | 3 locations | new value absent from re-scan
```

**2. Fix classes**

```text
rotate (value changes) | remove (file changes) | redact (report changes) | restrict reach (location changes) | accept with reason
```

**3. Blocked list**

```text
blocked finding | blocker | who can unblock | needed decision; listed so it is escalated rather than left in a backlog
```

## Pitfalls

- Handing over observations and calling the assessment complete
- Rotating the canonical location while two group locations keep the old value
- Letting a blocked finding sit in the list without naming who can unblock it

## Done when

- Every finding has an owner, a fix class, its full target list and a defined verification
- Blocked findings name their blocker and the person who can unblock them

## References

- [OWASP - Remediation guidance](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST SP 800-40 - Patch and configuration management](https://csrc.nist.gov/pubs/sp/800/40/r4/final)
