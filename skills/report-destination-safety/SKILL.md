---
name: report-destination-safety
description: "Decide where findings may be written before writing any, because the destination determines whether your report becomes a second copy of every secret it names. Use when findings will be shared and the destination, its retention and its audience have not been agreed"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [scope, reporting, handling]
---

# Report Destination Safety

> Decide where findings may be written before writing any, because the destination determines whether your report becomes a second copy of every secret it names

**Use when:** findings will be shared and the destination, its retention and its audience have not been agreed

**Avoid when:** the owner supplies a private channel with stated retention and an audience you have confirmed

## Procedure

1. Name the destination for findings: private repository, internal ticket, encrypted channel or in-person, with its retention rule.
2. Confirm who can read that destination, since an internal audience and a vendor audience change what you may include.
3. Check whether the destination indexes content for search, which turns a redacted report into a discoverable one if redaction slips.
4. Agree what happens after closure: deletion, archival or retention, with a date attached to each.
5. Record the destination and its rules beside the boundary document so every later finding inherits them.
6. Before first write, send one synthetic entry to the destination and inspect exactly what was stored and where.

## Signals

- Findings are headed for a public repository by default
- A ticket system retains deleted attachments
- A shared document is indexed by an enterprise search nobody remembered
- No one can say what happens to findings after closure

## Patterns

**1. Destination record**

```text
channel: internal ticket | audience: security + owning team | retention: 90 days post-closure | indexed: yes | search: redacted only
```

**2. Test write**

```text
send one synthetic finding first, then inspect what was stored, indexed and retained; that observation is the basis for the decision
```

**3. Closure rule**

```text
on closure: raw captures deleted at date X, report retained to date Y, both recorded when the finding is opened
```

## Pitfalls

- Defaulting to a public issue tracker because it is the most convenient place to write
- Assuming a deletion in a ticket system also removes attachments and search copies
- Letting an enterprise search index a report containing partially redacted values

## Done when

- A destination record names audience, retention, indexing behaviour and closure handling
- A synthetic test write has been inspected before any real finding is recorded

## References

- [OWASP - Information disclosure guidance](https://owasp.org/www-project-web-security-testing-guide/)
- [ISO 27002 - Information handling controls](https://www.iso.org/standard/75652.html)
