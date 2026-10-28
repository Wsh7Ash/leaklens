---
name: payment-and-financial-record-classification
description: "Detect financial record fragments by structure and field name, and rank them by how far the copy has travelled from the system of record. Use when the corpus may contain transaction, card, bank or invoice data"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, financial, personal-data]
---

# Payment and Financial Record Classification

> Detect financial record fragments by structure and field name, and rank them by how far the copy has travelled from the system of record

**Use when:** the corpus may contain transaction, card, bank or invoice data

**Avoid when:** the owner confirms in writing that no financial data exists in any readable tree

## Procedure

1. Detect by structure and field naming rather than reading values, consistent with the ladder's handling rule.
2. Record the path, the field names detected and a count per file, with a hash rather than any value.
3. Distinguish full records from truncated or masked ones, since a masked fragment ranks far lower.
4. Note whether the copy is a production export, a fixture or a test artifact, using local markers only.
5. Trace whether the copy has a documented owner and retention, since an unowned export is the urgent case.
6. Classify by completeness and location together: masked and internal is low, full and published is critical.

## Signals

- A tracked export contains unmasked financial fields
- A fixture directory contains records whose structure matches production exactly
- A copy exists with no owner and no retention date
- Only a masked fragment is present but it was reported as a full record

## Patterns

**1. Completeness record**

```text
path: exports/q3.csv | fields: card_number, expiry | masked: no | occurrences: 1580 | owner: unknown | retention: none
```

**2. Masking check**

```text
record whether values are fully present, partially masked or tokenized; this single field often decides the rank
```

**3. Owner rule**

```text
an export with no owner and no retention is ranked above a full record whose owner and retention are documented
```

## Pitfalls

- Recording an unmasked value so the reader understands the finding
- Ranking a masked fragment as a full record because the field name looks alarming
- Reporting a production export as a fixture because it lives beside test data

## Done when

- Each financial finding records completeness, count, location, owner and retention with no values
- The rank is justified from completeness and publication state together

## References

- [PCI DSS - Requirements for stored cardholder data](https://www.pcisecuritystandards.org/)
- [NIST SP 800-53 - Information retention controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
