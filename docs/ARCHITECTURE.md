# Architecture

## Goals

1. **One source of truth.** Skills are authored as Python data; Markdown files are generated. A test asserts committed files match a fresh render, so the two can never disagree.
2. **Validation is a first-class gate.** Every quality floor lives in `validate.py` and is enforced by both the CLI and the test suite.
3. **No runtime dependencies.** Standard library only, so the pack runs anywhere Python 3.10+ exists.

## Components

```text
src/leaklens/
├─ corpus/           authored skill data (source of truth)
│  ├─ __init__.py    PACK metadata, PHASE_ORDER + loads part1..part3
│  ├─ part1.py       skills 1-15   (scope, discover)
│  ├─ part2.py       skills 16-30  (classify)
│  └─ part3.py       skills 31-50  (confirm, harden, document)
├─ model.py          Skill dataclass + strict dict loading
├─ render.py         deterministic SKILL.md + pack.json + results writer
├─ validate.py       every rule, one place
└─ cli.py            validate / list / show / search / build / leakplan
```

### Data flow

```text
part1..part3 (dicts)
      │  skill_from_dict()  -- shape check, rejects missing/empty fields
      ▼
   Skill (frozen dataclass)
      │
      ├─ validate_pack()  ─▶ Issue list ─▶ CLI exit code (0 only at 50/50)
      └─ render_skill()   ─▶ skills/<slug>/SKILL.md  (byte-deterministic)

summary.json ─▶ summary_vocabulary() ─▶ build_leakplan()
                                         │  phase-stratified selection
                                         ▼
                      phase-ordered plan + thin-coverage phase list
```

### The leakplan command

`leakplan` is leaklens's domain command and separates this pack from a document library. It consumes a small summary of what the assessment *found* — classes, locations, reach, tools, observed counts and free-text concerns — and flattens it into lowercase tokens. Every skill is scored by counting how many of those tokens appear in its slug, title, summary, tags and steps.

Selection is **phase-stratified**: matches are bucketed by phase, sorted by score, and drawn round-robin in `PHASE_ORDER`. Round 0 takes the best match from every matched phase, round 1 the second-best, and so on until `--top` is reached. Two consequences:

- a small `--top` (even `top=6`) still yields one step from every phase the summary matched;
- ordering inside the output still follows the arc, so the plan reads scope → discover → classify → confirm → harden → document.

`missing_phases` is computed from **matched** skills, not from the truncated plan. Reporting "no matched skill in these phases" for a phase that matched but was cut by `--top` would be a false statement — and a pack whose entire subject is honest reporting cannot ship a tool that misreports its own coverage.

### Design decisions

- **`leakplan` stays vocabulary matching.** It encodes "what did you find → what should you do next", not a remediation engine. Judgement about which observation matters belongs to the reader; the CLI's job is to surface phases that would otherwise be skipped.
- **Scope precedes everything.** `PHASE_ORDER` puts `scope` first because a plan that begins with discovery rather than permission has already skipped its most important step.
- **Class and reach are separate axes.** The corpus treats *what the value is* and *who can already read it* as independent inputs to a rank, and `severity-ranking-by-class-and-reach` encodes the matrix. A pack that merged them would lose the axis that usually decides the order.
- **Phases are data, not code.** `PHASE_ORDER` lives in `corpus/__init__.py` next to `PACK`, so renderer, validator, CLI and tests all read one tuple.
- **Generated files are never hand-edited.** `validate` byte-compares every `skills/**/SKILL.md` against a fresh render, which is why CI can run `build` followed by `git diff --exit-code`.
- **The pack enforces its own rules.** Two tests assert the corpus contains no private address literals, no machine-local paths, and that any credential-shaped value carries a visible synthetic marker. A rule the corpus itself violates is a rule readers will not trust.

## Test surface

`tests/test_corpus.py` covers corpus shape (counts, uniqueness, phase balance), every validation rule, regeneration equality, drift detection, the evidence-hygiene rules, every CLI subcommand including `leakplan`'s stratified selection and thin-coverage semantics, and the integrity of the committed `pack.json` hashes and `results/` reports.