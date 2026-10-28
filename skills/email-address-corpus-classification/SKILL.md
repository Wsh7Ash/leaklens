---
name: email-address-corpus-classification
description: "Detect email addresses at volume and classify them by whether they are synthetic, role-based, employee or customer addresses, since only one of those is a privacy finding. Use when the corpus may contain email addresses in source, fixtures, logs or exports"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, personal-data, contacts]
---

# Email Address Corpus Classification

> Detect email addresses at volume and classify them by whether they are synthetic, role-based, employee or customer addresses, since only one of those is a privacy finding

**Use when:** the corpus may contain email addresses in source, fixtures, logs or exports

**Avoid when:** the owner confirms all addresses present are synthetic test data

## Procedure

1. Detect addresses by structure and record counts per file rather than listing each address.
2. Separate known synthetic domains and fixtures from addresses on real domains using local markers and domain lists.
3. Classify remaining addresses as role-based, employee-like or customer-like based on the surrounding field and file.
4. Check whether the addresses appear in a tracked and possibly published file, since location drives the rank.
5. Note whether addresses co-occur with other personal fields, which raises the class from contact detail to a record.
6. Record counts and classification per file with a hash sample, never an address.

## Signals

- A tracked file contains addresses on a real domain with no synthetic markers
- Addresses co-occur with other personal fields in the same row
- A fixture directory contains addresses that match production structure exactly
- A log records full addresses where a hash or truncation would do

## Patterns

**1. Count record**

```text
path: docs/examples.md | addresses: 23 | synthetic domain: 21 | real domain: 2 | co-located personal fields: no
```

**2. Domain split**

```text
synthetic domains and marked fixtures are excluded with the rule that excluded them; real-domain hits are kept and counted
```

**3. Co-occurrence flag**

```text
addresses plus another personal field in one row -> rank as a record, not as a contact detail
```

## Pitfalls

- Listing every address in the report, which reproduces the list you were asked to detect
- Treating a synthetic domain as real and inflating the count
- Missing co-occurring fields, which is what separates a contact detail from a record

## Done when

- Each file yields a count split by synthetic and real with the exclusion rule recorded
- Co-occurrence with other personal fields is flagged per file

## References

- [NIST SP 800-53 - Personally identifiable information handling](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [OWASP - Information disclosure guidance](https://owasp.org/www-project-web-security-testing-guide/)
