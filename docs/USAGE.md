# Usage

## Setup

```shell
python -m pip install -e ".[dev]"
leaklens validate      # must print: leaklens: 50/50 skills valid
python -m pytest -q    # 22 passed
```

Python 3.10+, no runtime dependencies.

## Day-to-day commands

| Command | What it does |
|---|---|
| `leaklens validate` | Runs every corpus rule **and** checks `skills/**/SKILL.md` on disk against a fresh render. Exit 0 only at 50/50. |
| `leaklens validate --skip-files` | Validates the authored corpus without touching generated files (useful mid-edit). |
| `leaklens validate --json` | Machine-readable report: checked, valid, passed, floors, issues. |
| `leaklens list` | All 50 skills with their phase. |
| `leaklens list --phase classify` | Narrow to one phase (15 skills). |
| `leaklens list --tag personal-data` | Narrow to one tag. |
| `leaklens show <slug>` | Print one rendered `SKILL.md`. |
| `leaklens search <terms...>` | Rank skills by keyword across slug, title, summary, tags and steps. |
| `leaklens build` | Regenerate `skills/`, `pack.json`, `results/catalog.md` and `results/validation.json`. |

## Turning a findings summary into a handling plan

```shell
leaklens leakplan --summary-file examples/demo-summary.json
leaklens leakplan --summary-file examples/demo-summary.json --top 6 --json
```

```text
# Handling plan - config-tree assessment
Classes: 3   Locations: 4   Reach: 2   Skills matched: 50 of 50   Plan steps: 12   Phases covered: 6/6

Classes found: secret, personal, internal
Locations: src/**, config/**, build/**, history
Reach: tracked, published

## scope
...
```

Summary keys consumed as vocabulary: `classes`, `locations`, `reach`, `tools`, `observed`, `concerns`, `keywords`. Anything else in the file is ignored rather than guessed at.

- **`--top N`** caps plan length; selection is round-robin across phases, so every matched phase gets a slot before any phase gets a second.
- **Thin coverage** lists phases where the summary matched *no* skill at all. It is computed from matches, never from the truncated plan.

## Loading skills into agents

Every skill is a standalone file with YAML front-matter:

```text
skills/rotation-before-publication/SKILL.md
```

**Claude Code** — point `skills` at this repository in `.claude/settings.json`, or copy the directory you want into the project's skills folder:

```json
{ "skills": { "paths": ["../leaklens/skills"] } }
```

**opencode** — add the directory to `opencode.json`:

```json
{ "skill": [{ "path": "../leaklens/skills" }] }
```

Any runtime that loads `SKILL.md` files works the same way; front-matter carries `name`, `description`, `pack`, `version`, `category` and `tags`.

## Regeneration discipline

`skills/**` and `pack.json` are **generated**. Never hand-edit them — a drift test will fail.

```shell
# 1. edit the corpus in src/leaklens/corpus/part1..3.py
# 2. regenerate and check the gate
leaklens build
leaklens validate      # must print 50/50
python -m pytest -q
```

CI runs the same sequence and then `git diff --exit-code -- skills pack.json results`, so a corpus edit committed without a rebuild fails the build.