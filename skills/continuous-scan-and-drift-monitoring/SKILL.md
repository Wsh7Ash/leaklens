---
name: continuous-scan-and-drift-monitoring
description: "Run the same detection on a schedule against the same fixture corpus, so a regression is caught by a monitor instead of by the next assessment a year later. Use when the assessment is closing and nothing will currently run the detection again"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [harden, monitoring, regression]
---

# Continuous Scan and Drift Monitoring

> Run the same detection on a schedule against the same fixture corpus, so a regression is caught by a monitor instead of by the next assessment a year later

**Use when:** the assessment is closing and nothing will currently run the detection again

**Avoid when:** a scheduled scan already runs with a fixture corpus and an alert on regression

## Procedure

1. Schedule the scan against the tracked tree on a cadence, plus an artifact region scan where those exist.
2. Run the fixture corpus in the same job so a rule regression is visible as a fixture miss, not as a silent pass.
3. Define the alert: new findings, fixture misses, or a coverage region becoming unreadable.
4. Record the baseline finding count so a later run can be compared against something.
5. Assign the alert to an owner, since an unowned alert becomes noise within a week.
6. Review the cadence against how fast values reach the tree, and shorten it if the interval outlives the risk.

## Signals

- No scheduled scan exists and the next assessment is the only check
- Fixtures are not part of the job, so a rule regression produces no signal
- An alert has no owner and no one reads it
- The scan interval is longer than the rate at which values reach the tree

## Patterns

**1. Schedule record**

```text
cadence: daily tracked scan + weekly artifact scan | fixtures: in every job | baseline: 0 findings | owner: platform
```

**2. Fixture signal**

```text
a fixture miss alerts on its own; it means the rule got weaker and the scan would otherwise look cleaner than reality
```

**3. Baseline compare**

```text
compare against the recorded baseline so a new finding stands out instead of blending into a total nobody remembers
```

## Pitfalls

- Scheduling a scan without fixtures, so a weakening rule looks like an improvement
- Owning the alert personally rather than as a team, so it dies when people move
- Choosing a cadence by convenience without reference to how fast values arrive

## Done when

- A scheduled job runs the scan with the fixture corpus and has a named owner
- A baseline finding count is recorded for comparison on later runs

## References

- [NIST SP 800-53 - Continuous monitoring controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [OWASP - Security regression testing](https://owasp.org/www-project-application-security-verification-standard/)
