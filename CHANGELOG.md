# Changelog

All notable changes to the `it-consulting-expert` plugin.
Format follows [Keep a Changelog](https://keepachangelog.com/); versioning is semver.

## [2.0.0] — 2026-10-03

The plugin stops being a prompt library and becomes a presale system: one workspace, one extraction,
numbers from code, agents with contracts, and tests that prove it.

### Added
- **`sier` calculation engine** (`sier/`, Python stdlib, 3.7+): `init`, `status`, `brief`, `score`,
  `estimate`, `cost`, `evm`, `sla`, `cr`, `calibrate`, `ratecard`, `derive`, `verify`, `runs`. Every
  computed artifact keeps its input in `inputs/` and an audit record in `_state/runs/`.
- **`sier verify`** recomputes every artifact from its saved input and cross-checks estimate ↔ team ↔ cost
  ↔ budget; it fails on hand edits and stale dependencies.
- **`shared/policy.json`** — the single source of truth for every policy number (replaces
  `shared/scoring-rubric.yaml`).
- **Engagement workspace** and handoff contract (`shared/engagement-workspace.md`); RFP Brief schema
  (`shared/brief-schema.md`); engine reference (`shared/engine.md`); harness rules (`shared/harness.md`).
- **Skills:** `engagement-init` (create/resume a workspace, deadlines, baseline, rate card) and
  `presale-team` (bid manager: runs the agent team wave by wave with Go/No-Go and budget gates).
- **14 agents:** presale team — `presale-rfp-analyst`, `presale-architect`, `presale-estimator`,
  `presale-staffing`, `presale-cost`, `presale-writer`; review board — `review-business`,
  `review-architect`, `review-qcd`, `review-risk`, `review-client`, `review-delivery`, `review-security`,
  `review-legal-ja`. Model-tiered (opus for architecture and writing, sonnet otherwise) with turn caps.
- **Per-role reconciliation** of the team plan against the estimate — found by the `review-qcd` agent in a
  live run (team matched in total but QA was 20 vs 37.5 人月), then made deterministic.
- **Tests:** 60 unit/regression tests (`tests/`); ABC Manufacturing regression fixture; 20 plugin eval
  cases (`evals/`) for routing, sibling collisions and engine use; GitHub Actions CI.

### Changed
- `rfp-notebook` is the only skill that extracts the RFP; it writes `00-rfp-brief.json` (validated,
  cited, with gaps that name the skills they block) and records the fallback tier.
- Every other skill reads the Brief and queries NotebookLM only for gaps it records. Unconditional
  queries per engagement: ~90 → 26.
- Effort, cost, Go/No-Go, EVM, SLA, change-request and calibration arithmetic moved from prose into the
  engine; the skills now prepare inputs and present engine output.
- `proposal-review` dispatches reviewers as parallel agents with separate contexts — the independence the
  skill always claimed is now structural — after running `sier verify`.
- `create-proposal` writes from workspace artifacts and checks compliance-matrix coverage against Brief ids;
  end-to-end runs moved to `presale-team`.
- `team-composition` writes `04-team.json` in the shape `cost-estimation` prices.
- Per-skill `metadata.version` removed; `plugin.json` and this file are the version of record.

### Fixed
- `maintenance-proposal` stated "~3.6 hours" allowed downtime for 99.5% measured over business hours; the
  correct figure is ~54 minutes (3.6 h is the 24/7 figure).
- `dry-run-results.md` was arithmetically wrong in several places (factor product 1.20 printed as 1.07 and
  never applied; 6% premium mis-computed and below policy; priced to policy the bid is over budget). The
  document now carries a banner; the corrected figures are pinned by tests.

### Notes
- No `bin/` directory on purpose: Cowork and claude.ai refuse to install plugins that ship one.
- Agents live flat in `agents/` with `presale-`/`review-` prefixes: a sub-folder agent did not load on
  Claude Code 2.1.288 although the docs describe sub-folder support.
- `vendor-management` now flags that 下請法 was replaced by 取適法 on 2026-01-01; full legal guidance
  (P8) remains out of scope pending counsel review.

### Not yet done (from docs/upgrade-plan-v2.md)
- P4 branded `.docx`/`.pptx`/`.xlsx` templates (needs your company assets).
- P6 scheduled tasks (deadline alerts, weekly report drafts) — offered by `engagement-init`, not installed.
- P8 Japanese legal reference (取適法, 偽装請負, 契約不適合責任, 印紙税) — needs counsel.
- `allowed-tools` declarations — still deferred until the eval suite has run at full strength.

## [1.3.1] — 2026-09-15

Correctness release. No new capability, no change to any skill's intended behaviour.

### Fixed
- **NotebookLM CLI targeting (151 call sites across 18 files).** Every `ask`, `source add`,
  `source list` and `status` invocation now passes `--notebook <notebook_id>`.
  Previously 38 calls used `-n`, which that CLI accepts only on
  `artifact wait` / `source wait` / `research wait|status` / `download *`, and 102 `ask`
  calls passed no notebook at all, silently depending on the global context written by
  `notebooklm use`. That file is shared and concurrent agents overwrite it, so a query
  could resolve against another engagement's notebook. The 4 legitimate `source wait -n`
  uses are unchanged.
- **Misleading guidance** in `create-proposal/references/notebooklm-integration.md` that
  presented `-n` and `--notebook` as interchangeable.
- **Conflicting Go/No-Go rubrics.** `dry-run-results.md` scored 5 dimensions
  (Strategic 15 / Capability 25 / Win 25 / Commercial 20 / Risk 15) while `rfp-analysis`
  scored 6 (… / Profitability 15 / Delivery Risk 10 / Resource Availability 10).
  The worked example now uses the canonical 6 dimensions; its weighted total is unchanged
  at 3.40 and the Conditional GO verdict stands.
- **Version drift.** `marketplace.json` and `plugin.json` both read 1.2.0 while the
  published plugin was 1.3.0 — the repo was not the source of truth. Both now read 1.3.1
  and carry the same description.

### Added
- `shared/scoring-rubric.yaml` — single source of truth for Go/No-Go weights, thresholds
  and the mandatory-qualification gate.
- `shared/notebooklm-contract.md` — flag rules, the ban on relying on `notebooklm use`,
  and a 4-tier fallback ladder so no skill hard-stops when NotebookLM is unreachable.
