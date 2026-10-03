# Changelog

All notable changes to the `it-consulting-expert` plugin.
Format follows [Keep a Changelog](https://keepachangelog.com/); versioning is semver.

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
