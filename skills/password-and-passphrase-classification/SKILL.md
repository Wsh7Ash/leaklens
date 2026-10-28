---
name: password-and-passphrase-classification
description: "Distinguish a real credential from a placeholder, an example or a test value, and rank the real ones by what the file says they protect. Use when an assignment named like a password or passphrase holds a non-empty literal"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, credentials, passwords]
---

# Password and Passphrase Classification

> Distinguish a real credential from a placeholder, an example or a test value, and rank the real ones by what the file says they protect

**Use when:** an assignment named like a password or passphrase holds a non-empty literal

**Avoid when:** every such assignment holds a documented placeholder or an environment lookup

## Procedure

1. Read the value's context: the key name, the neighbouring configuration and whether the file is tracked or local.
2. Check for placeholder markers in the value itself and in the surrounding file before treating it as live.
3. Look for a companion username or endpoint so you can state what the value protects without repeating the value.
4. Note whether the value looks reused across files, since reuse widens the blast radius of one rotation.
5. Distinguish a real credential from a test value by the environment markers in the file, not by the directory name alone.
6. Classify by what it protects, and record a hash rather than the value in the evidence entry.

## Signals

- A password assignment holds a literal in a tracked configuration file
- The same literal appears under two different key names
- A value marked as an example carries no substitution marker in it at all
- A test directory contains a value with no environment marker anywhere nearby

## Patterns

**1. Classification record**

```text
key: db_password | protects: primary datastore (from companion host field) | tracked: yes | reused at: 1 other path | placeholder markers: none
```

**2. Placeholder set**

```text
placeholder markers: change-me, example, xxxx, <...>, changeme, password; any of these makes the value a finding about hygiene, not exposure
```

**3. Hash substitute**

```text
record sha256 prefix plus length so reuse can be proven across paths without storing any value
```

## Pitfalls

- Treating a documented example value as a live credential and inflating the report
- Recording the value itself in evidence, which recreates the exposure in the ticket
- Missing reuse because each file was read in isolation

## Done when

- Each password finding states what it protects, whether it is tracked, and any reuse found
- Evidence records a hash prefix rather than the value itself

## References

- [OWASP - Password storage guidance](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [CWE-259 - Use of hard-coded password](https://cwe.mitre.org/data/definitions/259.html)
