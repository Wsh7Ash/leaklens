---
name: temporal-staleness-assessment
description: "Establish how old a finding is and whether it is still reachable, because an expired credential in history and a credential used this morning demand entirely different responses. Use when a finding's age and continued validity have not been established from local evidence"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [confirm, staleness, triage]
---

# Temporal Staleness Assessment

> Establish how old a finding is and whether it is still reachable, because an expired credential in history and a credential used this morning demand entirely different responses

**Use when:** a finding's age and continued validity have not been established from local evidence

**Avoid when:** the owner supplies current status for every credential the corpus could contain

## Procedure

1. Read file dates, commit dates and any embedded timestamps to establish when the value was written.
2. Look for evidence of later removal, such as a rotation note, a change entry or an absent companion.
3. Determine validity from local evidence only: expiry fields, rotation records or configuration that supersedes it.
4. Rank stale and current findings separately, since a reader of the report triages them differently.
5. Record the assessment date beside every staleness verdict, because validity is time-dependent.
6. Flag findings where staleness could not be determined rather than assuming either way.

## Signals

- A finding carries no date, so a reader cannot tell whether it is current
- History holds a value that a later commit appears to have rotated
- Staleness could not be determined and the report implies it is live
- An expired value and a current one appear in the same priority band

## Patterns

**1. Staleness record**

```text
written: 2025-08-14 | last seen in history: 2026-02-02 | rotation evidence: none found | verdict: unknown, not assumed
```

**2. Date basis**

```text
verdict: current | stale | unknown; basis: embedded expiry, rotation note, or file and commit dates
```

**3. Rank split**

```text
current findings triage first; stale ones are batched; unknown ones go to the owner for a status answer
```

## Pitfalls

- Assuming an old value is dead because it is old, when nobody has checked
- Presenting an unknown staleness verdict as though it were current
- Ranking without the assessment date, which makes the claim stale the moment it is written

## Done when

- Each finding carries a staleness verdict with its basis and the assessment date
- Unknown verdicts are listed for owner confirmation rather than assumed either way

## References

- [NIST SP 800-53 - Currency of information controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [CWE-672 - Operation on a resource after expiration](https://cwe.mitre.org/data/definitions/672.html)
