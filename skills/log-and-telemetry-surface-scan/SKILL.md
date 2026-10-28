---
name: log-and-telemetry-surface-scan
description: "Sweep logs, traces and telemetry as their own region, because this is where a value appears even when every source file was written carefully. Use when log files, traces or telemetry exports are inside the readable boundary"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [discover, logs, telemetry]
---

# Log and Telemetry Surface Scan

> Sweep logs, traces and telemetry as their own region, because this is where a value appears even when every source file was written carefully

**Use when:** log files, traces or telemetry exports are inside the readable boundary

**Avoid when:** log content is excluded from the assessment in writing and no log data is readable

## Procedure

1. List the telemetry sources in scope: application logs, access logs, traces, crash dumps and analytics events.
2. Sample across time rather than reading only the newest file, since the interesting line usually predates the current policy.
3. Look for full request and response bodies, authorization headers and query strings recorded verbatim.
4. Check whether structured logging serializes objects wholesale, which captures fields nobody intended to log.
5. Record the sources read with the sample window, so coverage over time is stated.
6. Pass hits to classification with the source recorded, because log remediation differs from code remediation.

## Signals

- A structured log line serializes an entire object including its credential field
- Authorization headers appear verbatim in an access log
- Only the newest log file was read while the interesting events are older
- A crash dump contains request state including a token

## Patterns

**1. Source row**

```text
source | window read | finding class
app.log | 2026-10-01..28 | token in structured field
access.log | 2026-10-20..28 | authorization header verbatim
crash.dmp | not read, reason: binary dump out of boundary
```

**2. Structural check**

```text
look for whole-object serialization and interpolation of request context; both capture fields the author never meant to log
```

**3. Time coverage**

```text
record the sample window explicitly; a scan of only recent files cannot support a claim about older exposure
```

## Pitfalls

- Reading only the newest file and concluding the pipeline is clean
- Reporting a value in logs without tracing where it was logged from
- Treating a log finding as a code finding and fixing the wrong layer

## Done when

- Telemetry sources are listed with the sample window read and any skip reason
- At least one structured or header finding is traced to the code that emitted it

## References

- [OWASP - Logging cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [CWE-532 - Insertion of sensitive information into log file](https://cwe.mitre.org/data/definitions/532.html)
