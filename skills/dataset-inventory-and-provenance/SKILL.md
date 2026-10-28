---
name: dataset-inventory-and-provenance
description: "Build a list of where data actually comes from and where it is copied, because an exposure is only actionable once every copy of the record is known. Use when the assessment covers a system whose data reaches more than one store, artifact or third party"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [scope, inventory, lineage]
---

# Dataset Inventory and Provenance

> Build a list of where data actually comes from and where it is copied, because an exposure is only actionable once every copy of the record is known

**Use when:** the assessment covers a system whose data reaches more than one store, artifact or third party

**Avoid when:** one authoritative store exists and the owner can account for every derived copy

## Procedure

1. Enumerate the sources that produce records: application database, object storage, logs, exports, third-party syncs and build artifacts.
2. For each source record what it holds, roughly how many records, and whether it contains personal or secret classes.
3. Trace where each source is copied to: warehouses, backups, analytics pipelines, support tooling and developer workstations.
4. Mark each copy as authoritative, derived or incidental, since each class implies a different remediation path.
5. Note any copy whose owner is unknown and carry it into the discover phase as an open question.
6. Write the inventory as a table with source, contents, class, copies and owner, and mark unconfirmed cells as unknown.

## Signals

- A warehouse table mirrors production data with no recorded owner
- A support export leaves the system and nobody can say where the file went
- Backups exist for one store but no one has considered the log pipeline
- A third-party sync was configured by a former team member

## Patterns

**1. Lineage row**

```text
source | contents | class | copies | owner
primary db | accounts | personal | warehouse, backup | data-team
app logs | request traces | internal | log store | platform
exports | reports | personal | drive folder | unknown
```

**2. Copy class**

```text
authoritative (the record lives here) | derived (computed from it) | incidental (a by-product); each class changes who fixes a leak
```

**3. Unknown rule**

```text
any cell you could not confirm is written as unknown and carried forward rather than dropped from the inventory
```

## Pitfalls

- Inventorying only the primary store while the log pipeline holds the same records
- Assuming a derived copy is harmless because it was computed rather than copied
- Omitting third-party syncs, which are usually where the data class widens

## Done when

- Every source has a row with contents, class, copies and owner, and unknown cells are listed
- At least one derived or incidental copy is traced to its destination with an owner named

## References

- [OWASP - Data-centric security guidance](https://owasp.org/www-project-top-ten/)
- [NIST SP 800-53 - System boundary documentation](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
