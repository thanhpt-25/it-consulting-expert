# Engagement Workspace & Handoff Contract

Every skill and agent in this plugin works on one shared folder per engagement. The folder is the
blackboard: skills never hand each other data through conversation — one writes a file, the next
reads it. This is what lets the presale agents run in parallel, lets a review board read the same
artifacts independently, and lets `sier verify` prove nothing was edited by hand.

## Where it lives

`python3 "${CLAUDE_PLUGIN_ROOT}/sier" init --client "<顧客名>" --project "<案件名>"` creates
`<root>/<client>-<project>/`, where `<root>` is `$SIER_HOME` if set, otherwise `./consulting`
under the current working folder (in Cowork: the connected folder; in Claude Code: the project).

Firm-wide data shared by all engagements lives next to them in `<root>/_firm/`:
`rate-card.json` (your rates) and `calibration.json` (estimate vs actual from closed projects).

## Layout

| Path | Written by | Read by |
|---|---|---|
| `engagement.json` | `engagement-init`, `rfp-notebook` | everyone |
| `00-rfp-brief.json` | **`rfp-notebook` only** | everyone |
| `00-rfp-brief.md` | `sier brief render` (never by hand) | humans |
| `01-go-nogo.json/.md` | `sier score` via `rfp-analysis` | create-proposal, proposal-review |
| `02-architecture.md` | `technical-solution` | effort-estimation, team-composition, proposal-writer |
| `03-estimate.json/.md` | `sier estimate` via `effort-estimation` | team-composition, cost-estimation |
| `04-team.json/.md` | `team-composition` | cost-estimation, vendor-management |
| `05-cost.json/.md` | `sier cost` via `cost-estimation` | create-proposal, maintenance-proposal |
| `06-delivery-plan.md` | `project-delivery` | create-proposal |
| `07-sla.json/.md` | `sier sla` via `maintenance-proposal` | — |
| `inputs/*.json` | the skill that owns each computation | `sier verify` |
| `artifacts/` | create-proposal, presentations, xlsx exports | the client |
| `progress/` | progress-report, change-request | lessons-learned |
| `_state/runs/` | the engine (one audit record per run) | auditors |
| `_state/derived/` | Tier-2 generated analyses (`shared/harness.md`) | reviewers |
| `_state/review/` | proposal-review (one report per persona + `consensus.md`) | bid manager |
| `_state/cr-ledger.json` | `sier cr add` | `sier cr report` |

Numbered files are the presale pipeline in order; `sier status` shows which exist and names the next step.

## The handoff contract — every skill's Step 0

1. **Find the workspace.** Run `python3 "${CLAUDE_PLUGIN_ROOT}/sier" status`. If none exists, run
   `engagement-init` first. For a quick one-off question with no engagement at all, skip the
   workspace and label everything you assume `[Proposed]`.
2. **Read the Brief, not the RFP.** `00-rfp-brief.json` is the canonical extraction. If `sier status`
   says it is missing or **stale** (sources were added after it was generated), run `rfp-notebook`
   first. Do not extract the RFP yourself — two extractions drift.
3. **Ask only for gaps.** `python3 "${CLAUDE_PLUGIN_ROOT}/sier" brief gaps --for <your-skill>` lists the
   open questions that block you. Query NotebookLM only for those, following
   `shared/notebooklm-contract.md`. If nothing blocks you, make **zero** NotebookLM calls.
4. **Write back what you learn.** Add the answer to `00-rfp-brief.json` as a labelled, cited item,
   remove the gap, run `sier brief validate` then `sier brief render`. The next skill gets it free.
5. **Read upstream artifacts from files.** If `03-estimate.json` exists, cost-estimation reads it —
   it does not ask the user for "the effort estimate".
6. **Never type a computed number.** Effort, cost, price, score, EVM, SLA and CR figures come from
   the engine (`shared/engine.md`). Paste its tables; do not retype or "tidy" them.

## Why a file contract instead of conversation

- **Parallel agents** start with empty context and cannot talk to each other. Files are the only
  channel they share.
- **Reproducibility.** A bid reviewed in March must be explainable in September. Inputs, outputs and
  run records make every figure re-derivable.
- **One extraction.** The pre-v2 plugin re-queried NotebookLM ~90 times per engagement and paraphrased
  the same requirement differently in the proposal, the estimate and the review.
