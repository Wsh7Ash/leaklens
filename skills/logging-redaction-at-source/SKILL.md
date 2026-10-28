---
name: logging-redaction-at-source
description: "Redact values where they are written rather than where they are found, because a log that has already shipped retains every copy you failed to stop. Use when a value was found in logs, traces or telemetry and the emitting code is under your control"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [harden, logging, redaction]
---

# Logging Redaction at Source

> Redact values where they are written rather than where they are found, because a log that has already shipped retains every copy you failed to stop

**Use when:** a value was found in logs, traces or telemetry and the emitting code is under your control

**Avoid when:** the emitting component is a third party you cannot modify and only retention can be changed

## Procedure

1. Trace each logged value back to the exact statement or serializer that produced it.
2. Redact at the emitting statement by allow-listing fields, or by masking values whose key matches a sensitive name.
3. Prefer structural redaction over pattern replacement, since a pattern misses values it has never seen.
4. Verify with a fixture: emit a synthetic sensitive value and confirm the log output does not contain it.
5. Address retention for the copies already written, since fixing the source does not touch existing log files.
6. Record the emitting statement changed, the fixture result and the retention action for existing copies.

## Signals

- A structured log serializes a whole object, capturing fields the author never named
- Redaction is done by pattern, so a new value format slips through
- The source was fixed while existing log files still hold the values
- No fixture proves the redaction actually removes the value

## Patterns

**1. Emit record**

```text
statement: app.log:118 serializer=whole object | fix: allow-list of fields | fixture: synthetic value absent from output: yes
```

**2. Allow-list over deny-list**

```text
log the fields you mean to log; a deny-list of sensitive keys fails on the key name you did not anticipate
```

**3. Retention pairing**

```text
source fix plus retention action on existing files, both recorded, because only the pair closes the exposure
```

## Pitfalls

- Fixing the source and leaving months of log files holding the values
- Redacting by pattern and declaring the pipeline clean when a new format will bypass it
- Writing a redaction test that never proves the value is absent from output

## Done when

- Each emitting statement is changed with a fixture proving absence from output
- A retention action for existing copies is recorded alongside the source fix

## References

- [OWASP - Logging cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [CWE-532 - Insertion of sensitive information into log file](https://cwe.mitre.org/data/definitions/532.html)
