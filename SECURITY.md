# Security Policy

## Authorized use only

`leaklens` is a knowledge corpus and planning tool for **authorized** security work: assessing trees, repositories and artifacts you own, or whose owners have explicitly permitted you to read them. The software itself performs **no network requests** — it renders, validates and plans locally from a JSON summary you supply.

The skills describe data-exposure **assessment** methodology: how to establish a boundary, what to discover, how to classify a candidate by structure and reach, how to confirm it from local evidence without ever using it, and how to harden and report what you found. They contain no weaponized exploit material.

## What this corpus deliberately does not contain

- No live credentials, tokens, keys or personal records. Any credential-shaped value in the corpus carries a visible synthetic marker and is asserted as such by a test.
- No private address literals and no machine-local paths anywhere in the corpus.
- No instructions for using a credential you find, for accessing a system without authorization, or for exfiltrating data.
- No scanner and no automation. The package reads nothing it was not pointed at and contacts nothing.

## Scope discipline is built into the corpus

The opening skills exist to keep an assessment bounded and honest:

1. `authorized-corpus-boundary` — readable trees, exclusions and detect-only classes are written down before the first file is opened.
2. `data-class-ladder-definition` — the ladder carries a handling column, so "detect-only" means no value is ever read or recorded.
3. `synthetic-first-confirmation-rule` — every rule proves itself against planted fixtures, including near-miss fixtures, before it touches real content.
4. `value-never-used-verification` — findings are confirmed from local evidence alone, and every finding records that no network use occurred.

`leakplan` always emits `scope` first for this reason: a plan that begins with discovery rather than a permission is a plan that has already skipped its most important step.

## Reporting a vulnerability in this project

If you find a defect in `leaklens` itself — for example, a validation bypass that lets a malformed skill pass the 50/50 gate — please open a private security advisory on the repository or contact the maintainer through GitHub. Do not publish exploit details before a fix is available.

## Scope of this project's own testing

All tests run locally against the checked-in corpus and the checked-in example summary. No test sends traffic anywhere; `leakplan` reads one JSON file and scores text. Continuous integration runs the same local gates: validation, unit tests and an artifact-sync check.