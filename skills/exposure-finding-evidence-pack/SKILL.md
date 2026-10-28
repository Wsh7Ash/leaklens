---
name: exposure-finding-evidence-pack
description: "Assemble a report where every exposure claim carries its location, class, reach, rank and confirmation basis without ever containing the value itself. Use when findings are ready to be written up for the owning team or the destination agreed in scope"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [document, evidence, reporting]
---

# Exposure Finding Evidence Pack

> Assemble a report where every exposure claim carries its location, class, reach, rank and confirmation basis without ever containing the value itself

**Use when:** findings are ready to be written up for the owning team or the destination agreed in scope

**Avoid when:** the finding has already been reported and only a closing note remains

## Procedure

1. State the finding in one sentence naming location, class and reach, without adjectives.
2. Attach the confirmation basis: format evidence, context evidence and the explicit statement that no network use occurred.
3. Include class, reach and rank with both rank inputs, so a reader can re-derive the priority.
4. List the group's locations as rotation targets, so remediation has its full scope.
5. Record the staleness verdict with the assessment date it was made on.
6. Attach the boundary and rule versions that permitted the read and produced the detection.

## Signals

- A report claims an exposure without saying where it was read from
- Rank appears without its class and reach inputs
- Confirmation basis is absent, so a reader cannot tell how the claim was established
- Only one location is listed for a value that appears in three

## Patterns

**1. Claim skeleton**

```text
claim: <class> value at <location>, reach <reach>, rank <rank>
basis: format + context, no network use
locations: <N rotation targets>
staleness: <verdict> as of <date>
```

**2. Evidence line**

```text
E-004 | src/client.py:18 | class: secret | reach: tracked | sha256: 3f2a... | rule v7 | boundary v3 | no network use
```

**3. Value-free rule**

```text
the pack contains hashes, paths and field names; a reviewer can act on every entry without ever seeing a value
```

## Pitfalls

- Including a value for context, which re-creates the exposure in the ticket
- Omitting the group locations, so remediation covers one file of three
- Presenting a rank without its inputs, which makes it impossible to challenge

## Done when

- Every claim carries location, class, reach, rank inputs, confirmation basis and staleness
- The pack contains no value, only hashes, paths and field names

## References

- [NIST SP 800-61 - Incident documentation](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
- [OWASP - Reporting security findings](https://owasp.org/www-project-web-security-testing-guide/)
