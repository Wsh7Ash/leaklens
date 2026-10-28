---
name: rotation-before-publication
description: "Rotate every live value before any report that could be read more widely than intended, because publication is irreversible while rotation is not. Use when a report naming live values is about to move to a destination with a wider audience"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [harden, rotation, disclosure]
---

# Rotation Before Publication

> Rotate every live value before any report that could be read more widely than intended, because publication is irreversible while rotation is not

**Use when:** a report naming live values is about to move to a destination with a wider audience

**Avoid when:** the finding set contains only internal references and no live values

## Procedure

1. Identify which findings carry live values rather than internal references, using the class and reach record.
2. Sequence rotation ahead of publication, starting with the highest-ranked reachable values.
3. Confirm each rotation through the defined verification, which for a value is usually a re-scan showing absence.
4. Check that every group location was updated, not only the canonical file, before treating a rotation as done.
5. Only after rotations verify does the report move to the agreed destination.
6. Record the order performed and the verification result for each, so the sequence can be audited.

## Signals

- A report is being shared while live values it names are still valid
- Rotation was performed on one location while other group locations still hold the value
- No verification step exists, so a rotation is a claim rather than a result
- Publication preceded rotation because the deadline was closer than the fix

## Patterns

**1. Sequence record**

```text
1. rank reachable live values  2. rotate each  3. verify by re-scan  4. confirm all group locations  5. publish report
```

**2. Verification**

```text
for a value: re-scan shows the value absent everywhere it appeared; for a file: re-read shows redaction applied
```

**3. Order evidence**

```text
rotation timestamps precede publication timestamp; both recorded so the order is provable
```

## Pitfalls

- Publishing first and rotating afterwards because the report was already written
- Calling a rotation complete when only the canonical location was changed
- Recording no verification, so nobody can tell later whether the value actually died

## Done when

- Every live finding rotates and verifies before the report reaches a wider audience
- Rotation and publication timestamps are recorded in the order they occurred

## References

- [NIST SP 800-57 - Key rotation](https://csrc.nist.gov/pubs/sp/800/57/r5/final)
- [OWASP - Coordinated disclosure guidance](https://owasp.org/www-project-vulnerability-disclosure/)
