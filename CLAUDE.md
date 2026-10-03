# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a **Claude Code plugin marketplace**, not an application. The product is the
`it-consulting-expert` plugin — a full-lifecycle IT consulting expert for Japanese SIer engagements.
It ships three kinds of artifact:

- **Skills** (`plugins/it-consulting-expert/skills/*/SKILL.md`) — 18 Markdown skills with YAML frontmatter (`name`, `description` with trigger phrases).
- **Agents** (`plugins/it-consulting-expert/agents/*.md`) — 14 subagents: a `presale-*` team and a `review-*` board.
- **`sier`** (`plugins/it-consulting-expert/sier/`) — a Python calculation engine, **standard library only**, run as `python3 "${CLAUDE_PLUGIN_ROOT}/sier" <command>`.

Two manifests must stay in sync and both are validated in CI: `plugins/it-consulting-expert/.claude-plugin/plugin.json` and the marketplace root `.claude-plugin/marketplace.json`.

The authoritative product/usage reference is `README.md`. The deeper contracts live in `plugins/it-consulting-expert/shared/`: `engine.md` (command reference), `harness.md` (when code may be written), `engagement-workspace.md` (the file blackboard), `brief-schema.md`, `notebooklm-contract.md`.

## Commands

All commands assume repo root. Nothing to build or install — the engine is pure stdlib Python 3.9+.

```bash
# Engine tests (60 unit + regression tests)
python3 -m unittest discover -s tests -t tests            # all
python3 -m unittest discover -s tests -t tests -v         # verbose (as CI runs it)
python3 -m unittest tests.test_cost                        # one module
python3 -m unittest tests.test_cli_and_regression.RegressionABC.test_dry_run_pricing_arithmetic  # one test

# Run the engine directly during development (CLAUDE_PLUGIN_ROOT is the plugin dir)
python3 plugins/it-consulting-expert/sier <command> [options]
python3 plugins/it-consulting-expert/sier --help

# Manifest validation (both must pass --strict)
claude plugin validate plugins/it-consulting-expert --strict
claude plugin validate .claude-plugin/marketplace.json --strict

# Plugin evals (routing + engine-use; costs money, needs ANTHROPIC_API_KEY)
cd plugins/it-consulting-expert && claude plugin eval . --tag smoke --runs 1 --ablation none --allow-tools Bash Write Edit
```

CI (`.github/workflows/ci.yml`) runs the unittest suite on Python 3.9 and 3.12 and both manifest validations on every push/PR. Evals run only on manual `workflow_dispatch`.

## The `sier` engine

`sier/__main__.py` is an `argparse` CLI that dispatches each subcommand to a per-domain module. Modules import each other **flat** (the entry point does `sys.path.insert(0, sier/)`), so inside the engine and in tests you import `cost`, `estimate`, `score` — never `sier.cost`.

| Module | Owns |
|---|---|
| `estimate.py` | WBS / function-point effort, adjustment factors, three-point range, recommended 人月 |
| `cost.py` | Labor/non-labor, fees, risk premium, 税抜/税込, budget fit, estimate↔team↔cost reconciliation |
| `score.py` | Go/No-Go rubric + mandatory-qualification gate |
| `evm.py` | SPI/CPI/EAC/ETC/VAC/TCPI |
| `sla.py` | Downtime per tier, maintenance fee, service credits |
| `change.py` | Change-request ledger, cumulative deviation gates |
| `brief.py` | RFP Brief validate / render / gaps |
| `firm.py` | Firm-wide rate card and calibration |
| `derive.py` | Tier-2 generated-script runner (guardrails) |
| `workspace.py` | The engagement workspace: `init`, `find`, `status`, `record_run`, the `PIPELINE` order |
| `common.py` | Shared helpers: `load_json`/`dump_json`, `md_table`, `SierError`, Decimal money handling, policy hashing |

Each compute module exposes a pure `compute(inputs, ...)` returning a result dict and a `render(result)` returning Markdown. The CLI layer adds workspace I/O and audit records.

### Engine invariants — do not break these

- **Money is `Decimal`.** Never introduce float arithmetic into contractual numbers. Tests assert exact `Decimal` values.
- **Every policy number lives in `shared/policy.json`** — rubric weights, phase ranges, factor bounds, fees, premiums, EVM thresholds, CR gates, SLA windows. Change behavior there, not scattered through code; tests and the regression fixture follow it.
- **`sier verify` recomputes every stored artifact from its saved `inputs/` file** and cross-checks estimate↔team↔cost↔budget. Keeping an artifact's input in `inputs/` is how a hand-edited number is detected. Don't add an engine output that isn't reproducible from a saved input.
- **Exit codes are contractual:** `0` ok · `1` verification mismatch / real problem (e.g. over budget) · `2` input/validation error · `3` warnings under `--strict`. Preserve them.

### Regression fixture

`tests/fixtures/abc-manufacturing/` encodes the original dry run and pins what the engine found wrong with it (adjustment factors multiply to 1.20 not 1.07; correct estimate 175.79 人月; policy price ¥233.25M, over the ¥200M budget). `tests/test_cli_and_regression.py` asserts these claims — treat failures there as a signal the engine's arithmetic changed, not as tests to loosen.

## How the pieces work together (the big picture)

1. **One workspace per engagement** (`consulting/<slug>/`, or `$SIER_HOME`) is a shared file blackboard. Skills and agents hand work to each other by reading/writing numbered files (`00-rfp-brief.json` → `06-delivery-plan.md`). `workspace.PIPELINE` defines the dependency order that drives `sier status` and the presale agent DAG.
2. **The RFP is extracted once.** Only the `rfp-notebook` skill writes `00-rfp-brief.json` (from NotebookLM, cited). Every other skill reads the Brief and queries NotebookLM only for gaps (`sier brief gaps --for <skill>`). Always pass `--notebook <id>`; never rely on `notebooklm use`.
3. **The model never does contractual arithmetic.** Effort, cost, price, tax, score, EVM, SLA and CR gates come from the engine (Tier 1). Tier 2 (`sier derive run`) is for engagement-specific questions the engine can't pre-build — sandboxed scripts in `_state/derived/` that must self-assert and may not re-emit engine-owned keys (see `harness.contractual_keys` in `policy.json`). Tier 3: **no skill, agent, or runtime step edits `SKILL.md`, the engine, or `policy.json`** — policy/engine changes go through a PR with a test so past bids stay explainable.
4. **Grounding labels** `[RFP]` / `[Proposed]` / `[RFP+]` tag every fact in output; RFP facts carry citations. These rules apply across all skills (see README "Grounding Rules").

## Evals

`plugins/it-consulting-expert/evals/` has one directory per case (mostly `trigger-<skill>` routing checks, plus engine-use and over-budget checks). Each case is a `prompt.md` plus a `graders/` directory. See `evals/README.md`.

## Conventions

- Keep the plugin version aligned across `plugin.json`, `marketplace.json`, `README.md`, and `CHANGELOG.md` when bumping.
- The engine is deliberately dependency-free; don't add third-party packages to it.
- Formal document output defaults to Japanese (keigo); bilingual throughout.
