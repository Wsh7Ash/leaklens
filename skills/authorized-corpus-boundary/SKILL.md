---
name: authorized-corpus-boundary
description: "Write down exactly which repositories, paths, artifacts and data classes the exposure assessment may read, before the first file is opened. Use when a data-exposure assessment is about to start and no written list states which trees, artifacts or datasets are in scope"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [scope, authorization, rules-of-engagement]
---

# Authorized Corpus Boundary

> Write down exactly which repositories, paths, artifacts and data classes the exposure assessment may read, before the first file is opened

**Use when:** a data-exposure assessment is about to start and no written list states which trees, artifacts or datasets are in scope

**Avoid when:** the owner already publishes a machine-readable list of readable trees with an explicit exclusion list

## Procedure

1. Collect the written authorization, the ownership statement and any path list into one place and note the versions you used.
2. List every in-scope tree, repository, artifact location and environment exactly as written, without normalizing or guessing wildcards.
3. Record explicit exclusions too, since a subtree excluded by name is the most common way an assessment reads something it may not.
4. State the data classes you expect to encounter and which of them you are cleared to read versus only to detect the presence of.
5. Write the boundary as a short pre-flight checklist you re-read before the first read of every session, not as a note recalled from memory.
6. Save the boundary text beside the evidence so a reviewer can prove every recorded path fell inside the permitted set.

## Signals

- Authorization names a repository but is silent on generated output and build directories
- A subtree is excluded in prose while a glob in the same document includes it
- No one can say whether reading a backup artifact is permitted
- A previous session recorded paths you cannot find in any current document

## Patterns

**1. Boundary record**

```text
scope:
  trees: [src/**, config/**, docs/**]
  excluded: [vendor/**, third_party/**]
  artifacts: [build output read allowed]
  classes: [detect only: personal, secret]
  network: forbidden
```

**2. Pre-flight echo**

```text
Before session start, restate: readable trees, exclusions, classes detect-only, and the network ban. Any element you cannot quote from the document is a gap to resolve, not a permission to assume.
```

**3. Evidence binding**

```text
Store boundary.md beside evidence/ so each recorded finding carries a document version it can be checked against during review.
```

## Pitfalls

- Reading a wildcard as permission for every subtree when the document lists specific paths only
- Scanning build output that the owner never opened up for assessment
- Treating an old approval as current after the repository changed hands or gained new data

## Done when

- A written boundary table names readable trees, exclusions, data classes and the network ban
- Every later evidence entry carries the document version that justified reading it

## References

- [OWASP - Sensitive data exposure guidance](https://owasp.org/www-project-top-ten/)
- [NIST SP 800-53 - PII and information handling](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
