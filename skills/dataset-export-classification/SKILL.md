---
name: dataset-export-classification
description: "Classify exported datasets by contents, ownership and destination, because an export is the copy most likely to leave the organization entirely. Use when export files, data dumps or report extracts exist inside the readable boundary"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, exports, lineage]
---

# Dataset Export Classification

> Classify exported datasets by contents, ownership and destination, because an export is the copy most likely to leave the organization entirely

**Use when:** export files, data dumps or report extracts exist inside the readable boundary

**Avoid when:** no export artifact exists or the boundary excludes them in writing

## Procedure

1. List every export artifact with its format, row count and the date it appears to have been produced.
2. Read the header row only to classify the fields present, without reading data rows.
3. Assign each field a class from the ladder and record the class summary, not the values.
4. Trace where the export came from using naming, dates and any manifest alongside it.
5. Determine, from local evidence only, whether the destination of that copy is inside or outside the organization.
6. Classify by field classes and destination together, with retention and ownership where they are known.

## Signals

- An export contains personal-class fields with no manifest and no owner
- A file's date suggests it predates a retention change and was never refreshed
- The destination of the copy cannot be determined from anything in the tree
- A header row alone was enough to classify but the file was read in full anyway

## Patterns

**1. Export record**

```text
artifact: report-q3.csv | rows: 1580 | fields: id, email, plan | classes: personal | owner: unknown | destination: unknown | retention: none
```

**2. Header-only rule**

```text
read the header row to classify fields and stop; data rows are never opened when the ladder marks the class detect-only
```

**3. Destination rank**

```text
destination outside the organization outranks internal storage for the same fields; rank on destination first
```

## Pitfalls

- Reading data rows to be thorough when the header alone answers the classification question
- Reporting an export without saying where its copy went
- Assuming a recent file date means the content was reviewed

## Done when

- Each export records format, row count, field classes, owner, destination and retention
- Classification comes from the header row, with data rows left unopened

## References

- [NIST SP 800-53 - Information export controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [OWASP - Sensitive data discovery](https://owasp.org/www-project-web-security-testing-guide/)
