# it-consulting-expert — v1.3.0 → v2.0.0 Upgrade Plan

## Status — 2026-10-03

| Phase | State | Where |
|---|---|---|
| **P0** Correctness | ✅ Done | commit `aa8ee58` (rebuilt from the Mac branch, identical content) |
| **P1** Engagement workspace | ✅ Done | `d5cd013` — `engagement-init`, handoff contract, Brief schema, all Step 0s |
| **P2** Deterministic engine | ✅ Done | `3555276` — `sier`, `shared/policy.json`, 60 tests |
| **P3** Review board as agents | ✅ Done | `825b5f5` — 8 review agents, `proposal-review` fan-out |
| **P3b** Presale agent team | ✅ Done | `825b5f5` — 6 presale agents, `presale-team` skill |
| **P3c** Tier-2 harness | ✅ Done | `825b5f5` — `sier derive`, `shared/harness.md` |
| **P4** Output quality | 🟡 Partial | xlsx/drawio routing done; branded templates need company assets |
| **P5** Learning loop | ✅ Done | `sier calibrate` + `sier ratecard`; lessons-learned writes, effort-estimation reads |
| **P6** Automation | ⬜ Not started | `engagement-init` offers deadline reminders; nothing installed |
| **P7** Evals + CI | ✅ Done | `11ea5e2` — 20 eval cases (20/20 on one run each), GitHub Actions |
| **P8** Japanese legal depth | ⬜ Not started | needs counsel; see 取適法 note below |

Shipped as **2.0.0** on branch `feat/v2` (8 commits on top of `master`). Not yet pushed — see the delivery note.

### What the build changed in this plan

Facts checked against docs or live runs that overturned something written above:

1. **No `bin/` directory.** Cowork and claude.ai refuse to install a plugin that ships `bin/`. The engine is
   invoked as `python3 "${CLAUDE_PLUGIN_ROOT}/sier" <cmd>` instead of `sier-*` commands on PATH.
2. **Agents must be flat.** A sub-folder agent (`agents/review/x.md`) did not load on Claude Code 2.1.288
   despite the docs. Agents are `agents/review-*.md` and `agents/presale-*.md`.
3. **Sub-agents can nest** (up to three levels). The bid manager still runs in the main conversation — so the
   Go/No-Go and budget gates stay visible — not because nesting is impossible.
4. **The presale DAG was wrong.** Staffing cannot run in parallel with the estimator; the team is sized from
   the estimate. Real parallelism: estimator ∥ writer draft (W2), and the review board (W6). The bid manager
   is a skill (`presale-team`), so the team is 6 agents, not 7.
5. **JSON, not YAML.** Policy, engagement and Brief files are JSON so the engine needs nothing beyond the
   Python standard library. `scoring-rubric.yaml` became part of `shared/policy.json`.
6. **One CLI with sub-commands** rather than per-skill scripts: one package, one test suite, one `verify`.
7. **下請法 → 取適法.** The law P8 would have cited was replaced on 2026-01-01 (中小受託取引適正化法:
   手形 ban, employee-count coverage test, duty to consult on price; 60-day payment and written terms
   continue). `vendor-management` now flags this; P8 must be written against the new law.

### Verified by live runs (claude -p in the build workspace)

- `skills:` preloading in plugin agents works with scoped and bare names; `${CLAUDE_PLUGIN_ROOT}` is
  substituted in agent bodies.
- `review-qcd` on the ABC fixture used `_state/verify.md` instead of redoing arithmetic, flagged the
  over-budget price, and found a role-level mismatch (QA 20 vs 37.5 人月) hidden by a matching total. That
  check is now in the engine with a regression test.
- `presale-estimator` on a fresh workspace wrote `inputs/estimate.json`, ran the engine, traced every
  `FR-*`, raised the open EDI gap, and passed `sier verify`.
- Eval suite: 20/20 cases on one run each ($2.45). CI runs 3 runs with the baseline.

### Open questions for you

- **Cap on the combined adjustment factor?** Each factor is bounded, but six of them compounded to ×1.67 in
  the live estimator run. Should `policy.json` cap the product (e.g. ×1.5) or require a justification above
  a threshold?
- **Rate card.** `sier ratecard init` writes market midpoints; the engine warns until real rates replace them.
- **Contract value vs computed price** for the post-award baseline when they differ after negotiation.

---

**Audit date:** 2026-09-15
**Audited artifacts:** `plugins/it-consulting-expert/` @ `cc01ecf` (GitHub: `thanhpt-25/it-consulting-expert`) + the installed synced copy
**Scope:** 16 skills, 38 files, 283 KB, 0 scripts, 0 assets, 0 agents, 0 commands, 0 evals

---

## 1. What exists today

| Layer | Present | Notes |
|---|---|---|
| Skills | 16 | All prose-only `SKILL.md` + 1–2 `references/*.md` each |
| Scripts | **0** | Every calculation is done by the model in prose |
| Assets (templates) | **0** | No `.docx` / `.pptx` / `.xlsx` template |
| Sub-agents | **0** | The 6-persona review board is prose, not real fan-out |
| Slash commands | **0** | — |
| Eval suite | **0** | `dry-run-results.md` is a hand-written transcript, not runnable |
| External deps | 1 hard | `notebooklm` CLI, called 140× for `ask` alone |

Size distribution is inverted against value: the money-critical skills are the thinnest.

| Skill | Lines | Comment |
|---|---:|---|
| rfp-notebook | 496 | Fat |
| proposal-review | 340 | Fat |
| design-presentation | 325 | Fat |
| lessons-learned / maintenance-proposal | 240 | OK |
| vendor-management / create-proposal | 209–222 | OK |
| rfp-analysis / proposal-presentation | 185–192 | OK |
| progress-report | 160 | Thin |
| project-delivery | 124 | **Thin — fixed-price critical** |
| cost-estimation | 122 | **Thin — money** |
| effort-estimation | 119 | **Thin — money** |
| technical-solution | 114 | **Thin** |
| team-composition | 108 | **Thin — money** |

---

## 2. Defects found (fix before adding anything)

### D1 — Broken NotebookLM CLI syntax (blocking)
Every grounded query is written as:
```bash
notebooklm ask "..." --json -n <notebook_id>
```
The `notebooklm` skill's own contract states `-n` applies to `wait` / `download`; other commands take `--notebook <id>`. There are **140 `ask` calls** across the plugin using the wrong flag. Either they error, or they silently fall back to whatever `notebooklm use` last set — which the CLI docs explicitly warn is a shared global (`~/.notebooklm/context.json`) that parallel agents clobber.

### D2 — Redundant extraction, no cache contract
`rfp-notebook` runs 26 queries to build the "canonical" RFP Brief. Then every downstream skill still opens with its own `Step 0: Connect to NotebookLM` and its own query block:

| Skill | Own queries |
|---|---:|
| rfp-notebook | 26 |
| create-proposal | 11 |
| rfp-analysis | 9 |
| effort-estimation | 7 |
| team-composition | 6 |
| cost-estimation | 5 |
| technical-solution, project-delivery, change-request, vendor-management, maintenance-proposal, lessons-learned, proposal-presentation | 3–6 each |

**~90 round-trips per engagement**, with no defined path where the Brief lives, no schema, and no "if the Brief exists, read it instead" branch. The README says downstream skills consume the Brief; no `SKILL.md` implements that. Consequence: slow, expensive, and the same requirement gets paraphrased differently in the proposal, the estimate, and the review.

### D3 — All arithmetic is prose arithmetic
Not one number in this plugin is computed reproducibly. The model is asked to do, by hand:
- WBS roll-up across 7 phases + 10–15% PM overhead
- Function Point counting (EI/EO/EQ/ILF/EIF) and conversion
- 5 multiplicative adjustment factors (0.7–1.5× each, compounding)
- 3-point → P75 (`base × 1.2`)
- Labor Σ(rate × 人月) + management fee 10% + risk buffer 15–25%
- Budget-fit delta vs. RFP ceiling
- EVM: SPI, CPI, EAC, ETC
- Weighted 6-dimension Go/No-Go score
- Cumulative CR deviation % vs. baseline (with 🟡10% / 🔴20% gates)
- Maintenance price as 15–20% of project cost; SLA availability tiers

For a firm submitting **一括請負** bids, an arithmetic slip is a margin loss you can't renegotiate. This is the single largest quality gap.

### D4 — The scoring rubric is not single-sourced
`rfp-analysis/SKILL.md`: Strategic 15 / Capability 25 / Win 25 / **Profitability 15 / Delivery Risk 10 / Resource Availability 10**
`dry-run-results.md`: Strategic 15 / Capability 25 / Win 25 / **Commercial Viability 20 / Risk Profile 15** — different dimension set, no Resource dimension.
Two sources of truth already disagree at 16 skills. At 20+ this compounds.

### D5 — Version drift
`plugin.json` = `1.3.0`; `marketplace.json` = `1.2.0`. Per-skill `metadata.version` is `0.1.0` or `0.2.0` with no relation to either and no changelog. `README.md` (33 KB, the best documentation in the project) exists **only in the installed copy — it is not in the git repo.**

### D6 — No `allowed-tools` declared
Zero skills declare frontmatter `allowed-tools`. Skills that shell out to `notebooklm` on every invocation should declare `Bash`, and the dependency should be visible at the manifest level.

### D7 — Single fragile channel, no fallback
`notebooklm` is an unofficial API requiring browser OAuth. When it is unauthenticated, rate-limited, or the notebook isn't set up, every skill hard-stops at Step 0 — even though the RFP PDF is usually sitting right there and the `pdf` skill can read it.

### D8 — The review board cannot actually be independent
`proposal-review` claims "Independent Reviews — each persona reviews all artifacts alone (prevents groupthink)." Run in a single context, all six personas share one attention window and each sees the previous persona's verdict. The anti-groupthink property the skill advertises is **structurally unachievable as written**.

### D9 — Trigger-phrase collisions
"proposal" appears as a trigger across `create-proposal`, `proposal-presentation`, `design-presentation`, `proposal-review`, `maintenance-proposal`. "見積" spans `cost-estimation`, `effort-estimation`, `create-proposal`, `proposal-presentation`. Nothing tests or disambiguates routing.

### D10 — The learning loop is described but not wired
`lessons-learned` produces "estimation accuracy assessment with calibration factors for future projects." Nothing writes them anywhere. `effort-estimation` and `cost-estimation` never read them. `cost-estimation` says "use the user's actual rates" — there is nowhere to store a rate card.

### D11 — Japanese legal/market depth is missing where liability lives
`vendor-management` (協力会社/オフショア) has no **下請法** content (60-day payment rule, mandatory 発注書, prohibited 買いたたき / 減額), no **偽装請負** risk guidance (the 請負 vs 準委任 vs 派遣 distinction that determines whether your offshore structure is legal), and `create-proposal` §11 Terms has no **契約不適合責任** (post-2020 Civil Code — replaced 瑕疵担保), no 印紙税 on 請負契約, no reference to the IPA/経産省 モデル取引・契約書.

---

## 3. Capabilities available but unused

| Capability | Where it belongs |
|---|---|
| **Sub-agents (`Agent`)** | Real fan-out for the 6-persona review board (fixes D8) |
| **Artifacts** | Live shareable engagement dashboard; compliance-matrix coverage %; the proposal itself as a reviewable page |
| **`xlsx` skill** | The natural home for 見積書 / WBS / EVM — currently everything is forced into `.docx` |
| **`drawio` skill** | 体制図, C4 architecture, multi-vendor org charts — currently ASCII/mermaid only |
| **`design` canvas skill** | `design-presentation` hand-writes HTML instead of using the canvas |
| **Scheduled tasks** | Friday 週次進捗報告 draft; RFP deadline T-14/T-7/T-3 alerts |
| **Gmail / Drive / Calendar** | Submission delivery, deadline calendar, client-facing distribution |
| **Microsoft Learn MCP** | Azure architecture grounding in `technical-solution` |
| **Memory** | Firm rate card, calibration factors, client/engagement history |
| **`pdf` skill** | The NotebookLM fallback (D7) |

---

## 4. Target architecture — v2.0.0

```
plugins/it-consulting-expert/
├── .claude-plugin/plugin.json          v2.0.0, allowed-tools, declared deps
├── CHANGELOG.md                        NEW
├── README.md                           MOVED INTO GIT
├── agents/                             NEW — real subagent definitions
│   ├── presale/                        → it-consulting-expert:presale:*
│   │   ├── bid-manager.md              提案リーダー (orchestrator)
│   │   ├── rfp-analyst.md              RFP 分析・要件抽出
│   │   ├── solution-architect.md       ソリューションアーキテクト
│   │   ├── estimator.md                見積担当 (effort + FP)
│   │   ├── cost-controller.md          原価・価格担当
│   │   ├── staffing-planner.md         要員・体制担当
│   │   └── proposal-writer.md          提案書ライター
│   └── review/                         → it-consulting-expert:review:*
│       ├── business.md                 事業戦略
│       ├── architect.md                技術アーキテクト
│       ├── qcd.md                      品質・コスト・納期
│       ├── risk.md                     リスク・コンプライアンス
│       ├── client.md                   顧客視点
│       ├── pm.md                       デリバリーPM
│       ├── security.md                 NEW optional persona
│       └── legal-ja.md                 NEW optional persona
├── bin/                                NEW — added to PATH by the plugin
│   ├── sier-estimate                   wraps estimate.py
│   ├── sier-cost                       wraps cost_model.py
│   └── sier-evm                        wraps evm.py
├── commands/                           NEW
│   ├── engagement-new.md               /engagement-new <client> <project>
│   ├── engagement-status.md            /engagement-status
│   └── rfp-brief.md                    /rfp-brief  (re-extract / refresh)
├── skills/
│   ├── _shared/                        NEW — single source of truth
│   │   ├── engagement-workspace.md     file layout + handoff contract
│   │   ├── grounding.md                [RFP]/[Proposed]/[RFP+] + citations
│   │   ├── notebooklm-contract.md      correct CLI + 3-step fallback ladder
│   │   ├── scoring-rubric.yaml         THE Go/No-Go weights (fixes D4)
│   │   ├── ja-sier-conventions.md      keigo, 人月, 税抜/税込, 千円単位
│   │   └── legal-compliance-ja.md      下請法 / 偽装請負 / 契約不適合責任 / 印紙
│   ├── engagement-init/                NEW — replaces 16 ad-hoc "Step 0"s
│   ├── rfp-notebook/scripts/extract.py         batched + cached + schema-validated
│   ├── rfp-analysis/scripts/score.py           reads scoring-rubric.yaml
│   ├── effort-estimation/scripts/estimate.py   WBS + FP + 3-point + factors
│   ├── cost-estimation/scripts/cost_model.py   labor/non-labor, pricing, TCO, fit
│   ├── progress-report/scripts/evm.py          SPI/CPI/EAC/ETC/TCPI + RAG
│   ├── change-request/scripts/cr_ledger.py     cumulative baseline deviation
│   ├── maintenance-proposal/scripts/sla_calc.py
│   └── assets/
│       ├── proposal-template.docx      表紙 + 社判 + Meiryo/Yu Gothic styles
│       ├── estimate-workbook.xlsx      WBS / 見積内訳 / 要員計画 sheets
│       └── deck-template.pptx          16:9 Japanese enterprise
└── evals/                              NEW
    ├── triggering.yaml                 16 positive + 16 negative routing cases
    └── scenarios/abc-manufacturing/    from dry-run-results.md, made runnable
```

### The engagement workspace (the structural keystone)

```
~/consulting/<client>-<project>/
├── engagement.yaml        notebook_id, currency, rate_card, deadlines, baseline
├── 00-rfp-brief.md        schema'd — the ONLY extraction output
├── 01-go-nogo.md
├── 02-estimate.json       machine-readable, produced by estimate.py
├── 03-cost.json
├── artifacts/             proposal.docx, deck.pptx, estimate.xlsx
└── _state/
    ├── cr-ledger.json     cumulative change tracking
    └── review/            per-persona subagent outputs
```

**Handoff contract** — every skill's Step 0 becomes:
1. Read `engagement.yaml`. If absent → invoke `engagement-init`.
2. If `00-rfp-brief.md` exists and is newer than the newest NotebookLM source → **use it, do not query**.
3. Query NotebookLM only for fields the Brief marks as gaps.

The Brief becomes a **schema**, not prose — YAML frontmatter + typed requirement rows (`FR-001 | text | MoSCoW | citation`) so `estimate.py` and `score.py` can read it directly.

---

## 4b. Presale agent team & computation harness — feasibility

**Both confirmed supported.** Verified against `code.claude.com/docs/en/plugins-reference` and `/sub-agents`, 2026-09-15.

### What the platform actually gives us

| Capability | Status | Consequence for this plugin |
|---|---|---|
| Plugin `agents/` directory | ✅ Supported, auto-loaded | Presale team + review board ship *inside* the plugin |
| Scoped + subfoldered names | ✅ `agents/review/security.md` → `it-consulting-expert:review:security` | Clean namespacing for two distinct teams |
| Parallel subagents | ✅ 20 concurrent by default (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) | 6-persona review fans out in one wave |
| Fresh isolated context per subagent | ✅ No conversation history inherited | **This is what makes review independence real** (fixes D8) |
| `skills: [...]` preload | ✅ | Each agent boots with exactly its own skill — estimator gets `effort-estimation`, nothing else |
| `model:` per agent | ✅ `opus`/`sonnet`/`haiku`/`fable`/`inherit` | Model tiering → cost control |
| `tools:` / `disallowedTools:` | ✅ | Reviewers become structurally read-only |
| `effort:`, `maxTurns:` | ✅ | Bound runaway cost per agent |
| `bin/` on PATH | ✅ | Ship `sier-estimate` etc. as real CLI commands |
| Bundled `scripts/` per skill | ✅ (the `docx` skill you depend on already does this) | Deterministic layer is proven in this exact runtime |
| Plugin `.mcp.json` | ✅ | — |
| `hooks` / `mcpServers` / `permissionMode` **inside a plugin agent** | ❌ Ignored for security | See constraint C3 below |

### Why a presale team ≠ the review board

The review board is the easy case: six read-only tasks, mutually independent, and independence *is* the goal. Pure fan-out.

A presale team is the hard case, because the work is **dependent**:

```
architecture → estimate → cost → proposal
                 ↑          ↑
            staffing ───────┘
```

Naive parallel fan-out fails here. Sub-agents start with **fresh context** and cannot talk to each other — only the orchestrator sees all their returns. So the coordination substrate must be **files, not conversation**. That is precisely what the Phase 1 engagement workspace provides:

> **The workspace is the blackboard.** Every agent's contract is "read these files → write this file." `engagement.yaml` + the schema'd RFP Brief + typed JSON artifacts are what one agent hands the next.

This makes **P1 a hard prerequisite for the agent team**, not a nice-to-have.

### Execution DAG

| Wave | Agents | Reads | Writes | Parallel |
|---|---|---|---|---|
| W0 | `rfp-analyst` | RFP sources | `00-rfp-brief.md` | — |
| W1 | `solution-architect` | Brief | `02-architecture.md` | — |
| W2 | `estimator`, `staffing-planner` | Brief + arch | `03-estimate.json`, `04-team.json` | ✅ ×2 |
| W3 | `cost-controller` | estimate + team | `05-cost.json` | — |
| W4 | `proposal-writer` | all of the above | `artifacts/proposal.docx` | — |
| W5 | 6–8 review personas | artifacts only | `_state/review/*.md` | ✅ ×6–8 |
| W6 | `bid-manager` (main context) | review reports | conflict resolution + verdict | — |

Wall-clock wins land in W2 and W5. W6 stays in the main context deliberately — mediation needs to see every report at once, which is exactly what a subagent cannot do.

### Cost control via model tiering

| Agent | Model | Rationale |
|---|---|---|
| `solution-architect`, `proposal-writer`, `bid-manager` | `opus` | Judgement and prose quality |
| `estimator`, `cost-controller`, `staffing-planner` | `sonnet` | Numbers come from scripts, not the model |
| `rfp-analyst`, review personas | `sonnet` | Extraction and checklist work |
| Mechanical validators | `haiku` | Format/compliance sweeps |

Pair with `maxTurns` and `effort` caps per agent. Without tiering, a full presale run on Opus × 13 invocations is the dominant cost of the plugin.

### Honest constraints

- **C1 — Cold start tax.** Each subagent re-reads the Brief; an 8-persona review on a full artifact set multiplies read cost. Mitigation: the Brief is schema'd and compact, and each agent receives only the artifacts it needs.
- **C2 — No negotiation.** Agents cannot argue with each other. Design so disagreement surfaces as a *file diff* the orchestrator adjudicates, never as an expected conversation.
- **C3 — Plugin agents get no MCP / hooks.** Fine for NotebookLM (a CLI reached via `Bash`), but a presale agent cannot itself use Google Drive/Gmail MCP. Keep connector work in the main context, or copy the agent to `~/.claude/agents/`.
- **C4 — Non-determinism.** Same input, subtly different prose. This is exactly why the harness matters more than the team:

> **Agents buy throughput and independence. Scripts buy reproducibility. Never confuse the two — and never let an agent own a contractual number.**

### The harness — three tiers

**Tier 1 — Bundled deterministic scripts (recommended, ~90% of the need).**
Versioned Python in `skills/*/scripts/` plus `bin/` wrappers. Fixed, reviewable, unit-testable, byte-identical output for identical input. Owns every contractual number: WBS roll-up, FP, adjustment factors, P75, labor Σ, fee + buffer, budget fit, EVM, Go/No-Go score, CR deviation, SLA credits. This is what makes a 一括請負 figure defensible in a 見積説明.

**Tier 2 — Model-generated code, executed, then reconciled (the real "harness").**
For questions whose *shape* comes from the RFP and cannot be pre-scripted: Monte Carlo on schedule risk with client-specific correlations, a bespoke migration-volume model, sensitivity analysis on the cost drivers this client weights. Pattern:

1. Model writes a short script to `_state/derived/<name>.py`
2. Executes it; stdout captured to `<name>.json`
3. **Script is kept next to its output** — every derived number is auditable and re-runnable
4. Script must carry self-checks: assertions, unit consistency, cross-total reconciliation
5. **Hard rule:** Tier-2 output may never restate a headline number that a Tier-1 script owns. Generated code answers *new* questions; bundled code owns the contract.

**Tier 3 — Self-modifying skills: don't.**
A plugin rewriting its own `SKILL.md` or scripts at runtime is technically possible and a reproducibility disaster — you lose the ability to reconstruct why a past bid said what it said. The controlled form: the model *proposes* a script, and promotion into the plugin goes through a PR with a human reviewer. `_calibration.yaml` evolves the same way.

**Tier 4 — The validation harness (the safety net).**
`claude plugin eval` for routing, plus a numeric regression fixture: the ABC Manufacturing scenario with asserted totals. Any change to a script or a rubric that moves a number fails CI loudly.

---

## 5. Phased plan

| Phase | Theme | Effort | Risk | Unblocks |
|---|---|---|---|---|
| **P0** | Correctness fixes | 0.5 d | none | everything |
| **P1** | Engagement workspace = agent blackboard | 2 d | med | P2, P3, P3b, P5 |
| **P2** | Deterministic calculation layer (harness Tier 1) | 3 d | low | credibility |
| **P3** | Review board as real subagents | 1.5 d | low | — |
| **P3b** | **Presale agent team (7 agents + DAG + tiering)** | 2.5 d | med | needs P1, P2 |
| **P3c** | **Tier-2 generated-code harness + guardrails** | 1.5 d | med | needs P2 |
| **P4** | Output quality (templates, xlsx, drawio, artifacts) | 2.5 d | low | — |
| **P5** | Learning loop (calibration + rate card + memory) | 1.5 d | low | needs P1, P2 |
| **P6** | Automation & delivery (schedules, Gmail/Drive/Cal) | 1 d | low | needs P1 |
| **P7** | Eval + numeric regression harness (Tier 4) | 1.5 d | low | safe iteration |
| **P8** | Japanese legal/market depth | 2 d + counsel | med | — |

**Total ≈ 19.5 engineering days.** P0 → P1 → P2 remains the critical path; P3b and P3c are what turn the plugin from a prompt library into a presale factory, and both depend on it.

---

### Phase 0 — Correctness (do first, ship alone)
1. Replace all 140 `ask ... -n <id>` with `--notebook <id>`; drop reliance on `notebooklm use` entirely (documented as unsafe for parallel agents).
2. Single-source the Go/No-Go rubric into `_shared/scoring-rubric.yaml`; make `rfp-analysis/SKILL.md` and `dry-run-results.md` both reference it.
3. `plugin.json` = `marketplace.json` = `2.0.0`; add `CHANGELOG.md`; delete per-skill `metadata.version` (it tracks nothing).
4. Add `allowed-tools` to all 16 frontmatters.
5. Commit `README.md` to the repo.
6. Add the NotebookLM fallback ladder to `_shared/notebooklm-contract.md`: `notebooklm` CLI → `notebooklm-web` (browser) → direct `Read` of the RFP PDF via the `pdf` skill. **No skill hard-stops at Step 0 again.**

**Definition of done:** a full engagement runs end-to-end with `notebooklm` uninstalled.

---

### Phase 1 — Engagement workspace
1. New skill `engagement-init` (triggers: "新規案件", "start an engagement", "set up this RFP").
2. Define `engagement.yaml` and the RFP Brief schema in `_shared/engagement-workspace.md`.
3. Rewrite all 16 `Step 0` sections to the 3-step handoff contract above.
4. `rfp-notebook` becomes the sole NotebookLM caller.

**Definition of done:** NotebookLM query count per engagement drops from ~90 to ≤30 and is identical on a re-run.

---

### Phase 2 — Deterministic calculation
Six scripts, each JSON-in / JSON-out with schema validation. Each `SKILL.md` gains a hard rule: *"Do not perform this arithmetic in prose. Call the script and present its output."*

| Script | Replaces prose math for |
|---|---|
| `estimate.py` | WBS roll-up, FP counting, phase %, 5 adjustment factors, 3-point → P75 |
| `cost_model.py` | labor Σ, non-labor, mgmt fee, risk buffer, 3 pricing models, budget fit, 3/5-yr TCO |
| `evm.py` | PV/EV/AC → SPI, CPI, EAC, ETC, TCPI + RAG thresholds |
| `score.py` | weighted Go/No-Go + mandatory-qualification gate |
| `cr_ledger.py` | cumulative CR deviation vs. baseline + 🟡10%/🔴20% gates |
| `sla_calc.py` | availability tiers → allowed downtime, SLA credits, maintenance % of project cost |

Each writes both a Markdown table (for the document) and JSON (for the next skill).

**Definition of done:** every number in a generated proposal traces to a script run recorded in `_state/`.

---

### Phase 3b — Presale agent team
1. Write the 7 `agents/presale/*.md` definitions. Each declares: `skills:` (its one skill), `model:` per the tiering table, `tools:` narrowed to what it needs, `maxTurns` + `effort` caps, and an explicit **input/output file contract**.
2. `bid-manager` orchestrates the W0→W6 DAG; waves W2 and W5 dispatch in parallel.
3. New slash command `/presale-run` — one command takes an engagement from Brief to reviewed proposal.
4. Every agent writes a run record to `_state/runs/` (agent, model, inputs, outputs, script calls) so a bid is reconstructible months later.
5. Reviewers get `disallowedTools: Write, Edit` — read-only by construction, not by instruction.

### Phase 3c — Tier-2 generated-code harness
1. `_shared/harness.md` defines the contract: where generated scripts live (`_state/derived/`), mandatory self-checks, the reconciliation rule against Tier 1, and the prohibition on restating contractual numbers.
2. `estimate.py` and `cost_model.py` expose a stable JSON schema so generated code consumes them rather than recomputing.
3. Add `--verify` mode to Tier-1 scripts: re-derive totals by an independent path and fail on mismatch.
4. Promotion path: a generated script that proves useful across 3+ engagements becomes a PR into `skills/*/scripts/`.

### Phase 3 — Real review board
1. Convert the 6 personas into `agents/*.md` definitions with narrow tool sets (`Read`, `Grep`, `Glob` only).
2. `proposal-review` fans out with the `Agent` tool — **one subagent per persona, each given only the artifacts**, never another persona's output. Independence becomes structural rather than aspirational.
3. Conflict detection + structured debate + mediation run in the main context, over the six returned reports.
4. Add `reviewer-security` and `reviewer-legal-ja` as opt-in personas.
5. Persist each report to `_state/review/` so revision tracking re-reviews only changed artifacts.

---

### Phase 4 — Output quality
1. `assets/proposal-template.docx` — 表紙, 社判 placement, Yu Gothic/Meiryo styles, heading numbering, 見積 number formatting (¥, 千円単位, 税抜/税込).
2. `assets/estimate-workbook.xlsx` — route 見積 / WBS / 要員計画 to `xlsx` instead of forcing `.docx`.
3. `technical-solution` + `team-composition` + `vendor-management` → `drawio` for C4 diagrams and 体制図.
4. `design-presentation` → use the `design` canvas skill rather than hand-written HTML.
5. New: publish a per-engagement **Artifact dashboard** — compliance-matrix coverage %, budget fit, review verdict, deadline countdown — one shareable link for the bid team.

---

### Phase 5 — Learning loop
1. `lessons-learned` writes `~/consulting/_calibration.yaml`: per-project-type estimate-vs-actual ratios, defect-origin distribution, realized margin.
2. `effort-estimation` and `cost-estimation` read it and show *"your last 4 CRM migrations ran 1.29× the initial estimate"* alongside the raw number.
3. Firm rate card stored once in `~/consulting/_rate-card.yaml`; `cost-estimation` stops asking every time.
4. Client/engagement history to memory so a repeat client's context carries across sessions.

---

### Phase 6 — Automation & delivery
1. Scheduled task: Friday 15:00 JST → draft 週次進捗報告 from the workspace state, leave for review.
2. Scheduled task: RFP deadline T-14 / T-7 / T-3 alerts from `engagement.yaml`.
3. Calendar: 提案説明会 and phase-gate reviews created from the delivery plan.
4. Drive/Gmail: package `artifacts/` and stage the submission mail (draft only, never auto-send).

---

### Phase 7 — Eval harness
1. `evals/triggering.yaml` — for each of 16 skills, 3 positive phrases (JA + EN) and 3 negative phrases drawn from its nearest sibling. Directly targets D9.
2. `evals/scenarios/abc-manufacturing/` — convert the existing `dry-run-results.md` into a fixture with assertions (compliance matrix covers 100% of FRs; total within RFP ceiling; every number present in `_state/`).
3. Run `claude plugin eval` in CI on every PR.

---

### Phase 8 — Japanese legal/market depth
New `_shared/legal-compliance-ja.md`, consumed by `vendor-management`, `create-proposal` §11, `maintenance-proposal`:
- **下請法** — 60-day payment, mandatory 発注書 (3条書面), 買いたたき/減額/受領拒否 prohibitions, 5条書類 retention
- **偽装請負** — 請負 / 準委任 / 労働者派遣 boundary tests; indicators that make an offshore or 協力会社 structure non-compliant
- **契約不適合責任** — post-2020 Civil Code; notice periods, remedies, how to scope it in a 一括請負 proposal
- **印紙税** — 請負契約 stamp duty bands
- IPA / 経産省 モデル取引・契約書 and 見積り指標 as citable anchors

> Mark this section advisory, not legal advice, and route it past your counsel before it reaches a client document.

---

## 6. Recommended sequencing

```
P0 ──▶ P1 ──▶ P2 ──┬──▶ P3b ──▶ P3c
       │           ├──▶ P5
       │           └──▶ P4
       ├──▶ P6
       └──▶ P3 ────────▶ P3b
P7 ──── runs alongside from the end of P0
P8 ──── independent, gated on counsel review
```

| Release | Contents | Theme |
|---|---|---|
| **v1.3.1** | P0 | Pure bug fix, no behaviour change — ship today |
| **v2.0.0** | P0 + P1 + P2 | Grounded, reproducible numbers |
| **v2.1.0** | P3 + P3b + P3c | **Presale agent team + harness** |
| **v2.2.0** | P4 + P7 | Output quality + regression safety |
| **v2.3.0** | P5 + P6 | Learning loop + automation |
| **v2.4.0** | P8 | Japanese legal depth (counsel-gated) |

---

## 7. Success metrics

| Metric | Today | v2.0 target |
|---|---|---|
| NotebookLM queries / engagement | ~90 | ≤30 |
| Numbers computed reproducibly | 0% | 100% |
| Skills that hard-stop without NotebookLM | 16 | 0 |
| Review personas with genuine independence | 0 / 6 | 6 / 6 |
| Sources of truth for the Go/No-Go rubric | 2 | 1 |
| Automated eval cases | 0 | 96+ |
| Re-run of the same engagement → identical numbers | no | yes |
| Presale agents shipped in the plugin | 0 | 7 + 8 reviewers |
| Wall-clock for a full presale cycle | sequential | 2 parallel waves |
| Derived numbers with a re-runnable script beside them | 0% | 100% |
