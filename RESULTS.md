# Results

Reproducible evidence for the claims in `README.md`.

## Environment

- OS: Windows (MSYS2 shell)
- Python: 3.14.3 (`requires-python >= 3.10`)
- Runtime dependencies: none (standard library only)
- Dev dependency: `pytest`
- Network: none required at any point — the package performs no network requests

## Validation performed

### 1. Corpus gate — PASS

```shell
$ PYTHONPATH=src python -m leaklens validate
leaklens: 50/50 skills valid
  ok  steps>=6 signals>=4 patterns>=3 pitfalls>=3 words>=180 refs canonical https
```

Exit code 0. With generated files included (the default), this also byte-compares every `skills/**/SKILL.md` against a fresh render.

### 2. Test suite — PASS (22 tests)

```shell
$ PYTHONPATH=src python -m pytest -q
......................                                                   [100%]
22 passed
```

Covered: pack declares and delivers 50; slugs and titles unique; every skill passes every rule; all six phases populated and balanced; word floor holds on the weakest skill; no placeholder or machine-local path tokens; **the corpus obeys its own evidence rules** (any credential-shaped value carries a visible synthetic marker, no private address literals anywhere); committed `SKILL.md` files match the render; `pack.json` hashes match file bytes; build is byte-idempotent in a temp directory; drift is detected; `validate --json` reports 50/50; `list`/`show`/`search` behave as documented; `leakplan` orders phases, covers all six with `--top 12` and with `--top 6`, rejects a missing summary, reports every phase as thin coverage for a summary that matches nothing, and aggregates vocabulary across summary keys; `results/validation.json` and `results/catalog.md` are consistent with the corpus.

### 3. Build and artifact sync — PASS

```shell
$ PYTHONPATH=src python -m leaklens build
built 50 skills -> .../leaklens/skills
$ PYTHONPATH=src python -m leaklens validate
leaklens: 50/50 skills valid
```

Regenerating twice produces byte-identical output; `test_build_is_idempotent` asserts this against a clean temp directory.

### 4. Phase distribution — as specified

| Phase | Skills |
|---|---|
| scope | 7 |
| discover | 8 |
| classify | 15 |
| confirm | 9 |
| harden | 7 |
| document | 4 |
| **total** | **50** |

`leaklens list --phase classify` returns 15; every other phase filter returns its count above.

### 5. `leakplan` on the checked-in example — PASS

```shell
$ PYTHONPATH=src python -m leaklens leakplan --summary-file examples/demo-summary.json
# Handling plan - config-tree assessment
Classes: 3   Locations: 4   Reach: 2   Skills matched: 50 of 50   Plan steps: 12   Phases covered: 6/6

Classes found: secret, personal, internal
Locations: src/**, config/**, build/**, history
Reach: tracked, published

## scope
...
```

Observed behaviour: 50 of 50 skills matched the summary vocabulary; the plan contains 12 steps spread across **all 6 phases** despite `--top 12`; `missing_phases` is empty because every phase matched. With `--top 6` the plan still covers 6/6 phases.

For a summary whose vocabulary matches nothing (`{"keywords": ["qqqqqq", "zzzzzz"]}`), `skills_matched` is 0, `plan_steps` is 0 and `missing_phases` lists all six phases — confirming thin coverage is derived from matches rather than from the truncated plan.

### 6. Cross-pack uniqueness — PASS

Against sibling packs `edgescout` (50) and `hookproof` (50): **0 slug overlap, 0 title overlap** across all three corpora (150 skills).

## Commands executed

```shell
python -m leaklens validate --json
python -m leaklens validate
python -m leaklens build
python -m leaklens list --phase classify
python -m leaklens search history rewrite
python -m leaklens leakplan --summary-file examples/demo-summary.json
python -m pytest -q
```

## Known limitations

- **`leakplan` is vocabulary matching, not a remediation engine.** It scores observed tokens against skill text. It will not tell you which finding matters most, only which skills relate to the summary you described and which phases you matched nothing in.
- **Thin coverage is only as good as the summary.** A summary that omits a class or a location will not surface the phase for it.
- **The pack does not scan.** Nothing here reads a repository, detects a secret or contacts a provider. Every discovery and classification step still has to be executed by the tester under the boundary they established.
- **Ranking is a matrix, not a model.** Severity comes from class crossed with reach as the corpus describes; there is no scoring model beyond it, and the report must carry both inputs for a reader to re-derive the rank.
- Tests were run on Python 3.14 locally. CI additionally covers 3.10, 3.12 and 3.13.

## Generated artifacts

| Path | What it is |
|---|---|
| `skills/**/SKILL.md` | 50 rendered skills, byte-identical to the corpus |
| `pack.json` | manifest with SHA-256 per skill file |
| `results/catalog.md` | generated skill catalog table |
| `results/validation.json` | machine-readable gate report (`passed: true`) |
| `examples/demo-summary.json` | the example summary used above |