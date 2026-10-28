# Changelog

All notable changes to `leaklens` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [1.0.0] - 2026-10-28

### Added

- Initial release: 50 unique data-exposure hunting skills across six phases
  (`scope`, `discover`, `classify`, `confirm`, `harden`, `document`).
- Validator with structural, strength and hygiene rules; `50/50 skills valid`
  gate with `--json` output for CI.
- Deterministic renderer and `build` command writing `skills/`,
  `pack.json` (SHA-256 per skill) and `results/`.
- CLI: `validate`, `list`, `show`, `search`, `build`, `leakplan`.
- `leakplan` — findings summary to phase-ordered handling plan, with
  phase-stratified selection and match-derived thin-coverage reporting.
- Example summary `examples/demo-summary.json`.
- Test suite (22 tests) covering corpus shape, rules, regeneration, drift,
  the corpus's own evidence-hygiene rules, every CLI command and leakplan's
  selection semantics.
- CI workflow, docs (`ARCHITECTURE`, `USAGE`, `PROJECT_SPEC`), `SECURITY.md`.

### Design notes

- `missing_phases` is derived from matched skills, not from the plan truncated
  by `--top`, so a covered phase can never be reported as uncovered.
- Selection draws matches round-robin across `PHASE_ORDER` before any phase
  receives a second slot, so `--top 6` still covers all six phases when the
  summary matches them.
- Two tests hold the corpus to the rules it prescribes: any credential-shaped
  value must carry a visible synthetic marker, and no private address literal
  or machine-local path may appear anywhere.