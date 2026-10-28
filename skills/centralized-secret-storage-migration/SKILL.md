---
name: centralized-secret-storage-migration
description: "Move values out of files into a store with access control and audit, then verify none remain, because removing a value is only half the fix. Use when values live in files and configuration because no store exists to hold them"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [harden, secrets-management, migration]
---

# Centralized Secret Storage Migration

> Move values out of files into a store with access control and audit, then verify none remain, because removing a value is only half the fix

**Use when:** values live in files and configuration because no store exists to hold them

**Avoid when:** a store is already in use and files reference it without embedding values

## Procedure

1. List every value found, its locations and its owning application, from the deduplicated group list.
2. Stand up or select the store and confirm it has access control, audit logging and per-environment separation.
3. Move each value to the store and change the reading code to fetch it, keeping one change per value so it can be reviewed.
4. After each move, re-run the scan against that location to confirm the value is absent from the file.
5. Handle rotation for values that must change once they are out of the file, since the move exposed them to the file's readers.
6. Record the migration with the re-scan result per location and the store entry each value now lives under.

## Signals

- Values are moved to a store while the file still contains the literal
- The store has no per-environment separation, so one key serves all environments
- No re-scan confirms the file no longer holds the value
- Files were edited in bulk, making each change hard to review or roll back

## Patterns

**1. Migration row**

```text
value group: E-004 | store entry: prod/payments/api_key | file updated: yes | re-scan: absent | rotation: required, scheduled
```

**2. One-at-a-time rule**

```text
one value per change so a failure is attributable and a rollback is small
```

**3. Store requirements**

```text
access control, audit log, per-environment separation, rotation support; each confirmed rather than assumed
```

## Pitfalls

- Moving a value into a store while leaving the original in place, which now has two copies
- Migrating in one bulk edit that nobody can review
- Skipping rotation on the grounds that the value is now safely stored

## Done when

- Each migrated value records its store entry, the file update and a re-scan showing absence
- Rotation status is recorded per value rather than assumed complete

## References

- [OWASP - Secrets management cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [NIST SP 800-57 - Key storage guidance](https://csrc.nist.gov/pubs/sp/800/57/r5/final)
