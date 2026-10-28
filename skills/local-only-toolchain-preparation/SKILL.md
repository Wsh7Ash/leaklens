---
name: local-only-toolchain-preparation
description: "Prepare a scanning chain that never uploads content anywhere, because a tool that phones home with your repository has already caused the incident you are assessing. Use when any tool, model or service will read in-scope content and its network behaviour has not been confirmed"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [scope, tooling, data-handling]
---

# Local-Only Toolchain Preparation

> Prepare a scanning chain that never uploads content anywhere, because a tool that phones home with your repository has already caused the incident you are assessing

**Use when:** any tool, model or service will read in-scope content and its network behaviour has not been confirmed

**Avoid when:** the owner already supplies an air-gapped toolchain with a documented network policy

## Procedure

1. List every tool that will read in-scope content and record whether it transmits anything, including telemetry and crash reporting.
2. Disable telemetry and auto-update on each tool where an option exists, and record which options you set.
3. Confirm that no tool sends content to a hosted model or service; local execution is the requirement, not a preference.
4. Verify the exclusion and ignore files so caches and previous output do not get re-read as new findings.
5. Run a dry pass over a harmless file and inspect the tool's own logs or network counters for any outbound attempt.
6. Record the prepared toolchain with versions and settings beside the evidence, so the run can be reproduced exactly.

## Signals

- A tool has default telemetry enabled and no documented way to disable it
- A model-backed helper would send file contents to a hosted endpoint
- No one has checked whether the runner has outbound network access at all
- Cache directories from a previous run are about to be re-read as fresh findings

## Patterns

**1. Toolchain record**

```text
tool | version | network | telemetry | settings applied
scanner-x | 2.3 | disabled at OS level | off | --no-telemetry
helper-y | 1.1 | blocked by firewall rule | off | local model only
```

**2. Dry pass**

```text
run against one known-harmless file, then inspect egress counters; any outbound attempt stops the session and is reported as a toolchain defect
```

**3. Exclusion list**

```text
exclude caches, previous results and vendored dependencies before the first pass so re-reads never masquerade as new findings
```

## Pitfalls

- Letting an AI helper summarize repository content through a hosted API the owner never approved
- Re-running against a cache from a previous session and reporting duplicates as new
- Assuming a tool is offline because it has no obvious upload button

## Done when

- Every tool reading in-scope content has a recorded network posture and the settings applied
- A dry pass shows no outbound attempt, and exclusions are set before the first real run

## References

- [OWASP - Secure development toolchain guidance](https://owasp.org/www-project-application-security-verification-standard/)
- [NIST SP 800-53 - Monitoring and boundary protection](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
