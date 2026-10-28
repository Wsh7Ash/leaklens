# Project Spec — leaklens

## Name

`leaklens`

## Category

`data-tool`

## Target user

Engineers and authorized testers doing data-exposure assessment over repositories, configuration, artifacts and logs they are permitted to read.

## Problem

Exposure hunting fails in two directions at once: a tool flags everything and the reader stops trusting it, or a tool is tuned until it stops flagging the thing that mattered. The decisions that separate the two are never written down anywhere the next person can find them: which regions were actually read and which an inherited ignore rule hid, whether a candidate's format *and* context both agree, whether a finding's rank should come from what the value is or from who can already read it, whether the value survives in history after the file was cleaned, and how a value found in three locations becomes one rotation target with three targets instead of three unrelated findings. Every assessment re-derives them, and agents have no structured skill files to load.

## Solution

A corpus of 50 unique, validated data-exposure skills organised into six phases (`scope`, `discover`, `classify`, `confirm`, `harden`, `document`), a validator that enforces quality floors, and a `leakplan` CLI that turns a findings summary into a phase-ordered handling plan with honest thin-coverage reporting.

## Core workflow

```text
author/edit corpus  ->  build  ->  skills/ + pack.json + results/
                                    |
                                    v
                          validate (50/50 gate)  ->  pytest  ->  CI
                                    |
                                    v
                       leakplan --summary-file summary.json -> ordered plan
```

## Must-have features

- 50 unique skills with unique slugs and titles across the six phases.
- Validator with structural, strength and hygiene rules; exit `0` only at 50/50.
- Deterministic renderer; committed files proven in sync by tests.
- `leakplan` producing a phase-ordered plan from a JSON summary, with thin coverage derived from matches rather than from the truncated plan.
- The corpus must satisfy its own evidence rules: no live-looking credential values, no private address literals, no machine-local paths.

## Nice-to-have (explicitly out of scope for v1)

- A scanner. The pack makes **no** network requests and reads no files it was not pointed at.
- Automated rotation against a provider API.
- A ranking model beyond the class-by-reach matrix the corpus describes.

## Acceptance tests

1. `validate` exits 0 and reports 50/50.
2. `pytest -q` passes 22 tests, including regeneration equality, drift detection and the corpus's own evidence-hygiene rules.
3. `leakplan` — round-trips the checked-in example summary, covers all 6 phases with `--top 6`, and reports every phase as thin coverage for a summary that matches nothing.
4. A generated build lands byte-identically in a clean temp directory.

## Authorized-use constraint

This is a defensive and methodology pack. Skills describe discovery over authorized trees, classification by structure, confirmation from local evidence, hardening and reporting. The corpus contains no live credentials, no personal records and no weaponized payload; `SECURITY.md` states the boundary and the reporting path.