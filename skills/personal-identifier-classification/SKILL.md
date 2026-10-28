---
name: personal-identifier-classification
description: "Detect and classify values that identify a person, recording presence and structure rather than the identifier itself. Use when the corpus may contain personal data and the ladder marks that class detect-only"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, personal-data, privacy]
---

# Personal Identifier Classification

> Detect and classify values that identify a person, recording presence and structure rather than the identifier itself

**Use when:** the corpus may contain personal data and the ladder marks that class detect-only

**Avoid when:** the ladder explicitly permits reading personal values and the owner has confirmed it in writing

## Procedure

1. Confirm from the ladder that this class is detect-only before running any detection at all.
2. Detect by structure rather than by content: field names, formats and surrounding labels.
3. Record the path, the field name, the structure detected and a hash of the value, never the value.
4. Count occurrences per file rather than listing each one, so the report states volume without reproducing records.
5. Note whether the file is tracked, published or exported, since location decides the urgency.
6. Classify severity by publication state, not by the sensitivity of the field alone.

## Signals

- A tracked file contains a column of personal identifiers in plain text
- A fixtures directory holds what look like real records rather than synthetic ones
- A document or export includes personal fields with no publication restriction
- A detection ran against values the ladder marked detect-only

## Patterns

**1. Presence record**

```text
path: data/seed.csv | field: national_id | structure matches: yes | occurrences: 412 | tracked: yes | hash of first: 7be1...
```

**2. Count-not-copy rule**

```text
report counts and structure; the value never appears in evidence, a ticket or a chat message
```

**3. Publication rank**

```text
published or exported outranks merely stored; rank the finding by where the copy lives
```

## Pitfalls

- Pasting an example record into the report so a reader can see what was found
- Listing every occurrence individually, which turns the report into a second copy of the dataset
- Ranking by field sensitivity while ignoring that the file is already public

## Done when

- Each personal-data finding records structure, count, path and publication state with no value
- The report cites the ladder's detect-only rule as the reason values are absent

## References

- [OWASP - Sensitive data exposure](https://owasp.org/www-project-top-ten/)
- [NIST SP 800-53 - PII processing and transparency](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
