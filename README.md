# leaklens

**50 validated data-exposure hunting skills**, plus a `leakplan` CLI that turns a findings summary into a phase-ordered handling plan.

Authorized testing only: every skill describes how to *discover, classify, confirm, harden and report* exposure in systems you own or have written permission to assess. The corpus contains no live credentials and no personal records.

```shell
python -m pip install -e ".[dev]"
leaklens validate          # -> leaklens: 50/50 skills valid
leaklens build             # -> skills/, pack.json, results/
python -m pytest -q        # -> 22 passed
```

## Why this pack exists

Data-exposure hunting is where two failure modes meet: a tool that flags everything, and a reader who stops trusting it. The decisions that separate them — which regions were actually read, whether a candidate's format and context both agree, what a value's reach is as opposed to its class, whether the value exists in history as well as the working tree, how a group of copies collapses into one rotation target — are never written down, so each assessment re-derives them and each report is judged differently.

`leaklens` makes that knowledge checkable. Each of the 50 skills is one self-contained procedure with a stated **use when** and **avoid when**, a numbered procedure, observable **signals**, concrete **patterns**, known **pitfalls** and **done when** criteria. A validator enforces the floor on all of them and the CLI will not report success below 50/50.

## The arc

| Phase | Count | What it covers |
|---|---|---|
| `scope` | 7 | authorized corpus boundary, dataset lineage, data-class ladder, local-only toolchain, synthetic-first rule, read-only evidence, report destination |
| `discover` | 8 | repository surface, high entropy, known formats, assignment shapes, URL credentials, dotfiles, generated artifacts, logs |
| `classify` | 15 | cloud keys, tokens, key material, passwords, connection strings, JWTs, personal and financial data, email corpora, internal hosts, signed URLs, signing and OAuth secrets, archives, exports |
| `confirm` | 9 | two-signal corroboration, false-positive taxonomy, deduplication, precision sampling, never-used verification, staleness, ranking, blind review, remediation readiness |
| `harden` | 7 | rotation before publication, history rewrite, ignore hygiene, commit and pipeline gates, centralized storage, log redaction at source, continuous scan |
| `document` | 4 | evidence pack, redaction for shareable reporting, remediation order by copy, post-closure verification |

## CLI

```shell
leaklens validate --json               # the 50/50 gate, machine-readable
leaklens list --phase classify          # 15 skills
leaklens show rotation-before-publication
leaklens search history rewrite
leaklens build                         # regenerate skills/, pack.json, results/
leaklens leakplan --summary-file examples/demo-summary.json
```

### `leakplan`

`leakplan` is this pack's domain command. It reads a small JSON summary of what you actually found —

```json
{
  "target": "config-tree assessment",
  "classes": ["secret", "personal", "internal"],
  "locations": ["src/**", "config/**", "build/**", "history"],
  "reach": ["tracked", "published"],
  "observed": { "candidates": 418, "accepted": 18, "value_used": false },
  "concerns": ["which findings still exist in tracked history"]
}
```

— flattens it into vocabulary, scores every skill against that vocabulary, and emits a handling plan in phase order. Selection is **phase-stratified**: the first pass takes the best match in each matched phase before any phase gets a second slot, so a small `--top` can never crowd out the later phases of the arc. *Thin coverage* lists phases the summary matched nothing in, computed from matches rather than from the truncated plan.

## The pack holds itself to its own rules

Two tests enforce the corpus's own discipline:

- **Synthetic only** — any credential-shaped value in the corpus must carry a visible marker (`fixture`, `example`, `synthetic`, …), and no private address literal may appear anywhere.
- **Evidence hygiene** — no placeholder tokens, no machine-local paths, canonical `https` references only.

## Layout

```text
src/leaklens/
├─ corpus/        authored skill data — the single source of truth
│  ├─ part1.py    skills 1-15   (scope, discover)
│  ├─ part2.py    skills 16-30  (classify)
│  └─ part3.py    skills 31-50  (confirm, harden, document)
├─ model.py       Skill dataclass + strict dict loading
├─ render.py      deterministic SKILL.md / pack.json / results writer
├─ validate.py    every rule, one place
└─ cli.py         validate / list / show / search / build / leakplan
```

Markdown under `skills/` is **generated**. Edit the corpus, run `leaklens build`, and a test asserts the committed files match a fresh render — the two can never silently disagree.

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — components, data flow, design decisions
- [docs/USAGE.md](docs/USAGE.md) — commands, agent integration, regeneration discipline
- [docs/PROJECT_SPEC.md](docs/PROJECT_SPEC.md) — problem, solution, acceptance tests
- [RESULTS.md](RESULTS.md) — reproducible evidence for every claim above
- [SECURITY.md](SECURITY.md) — authorized-use scope and the reporting path
- [CONTRIBUTING.md](CONTRIBUTING.md) — the quality floor CI enforces

## License

MIT. References link to public specifications and guidance; see each skill's **References** section.