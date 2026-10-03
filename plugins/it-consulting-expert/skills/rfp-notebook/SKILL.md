---
name: rfp-notebook
description: >
  Set up and manage NotebookLM notebooks for IT consulting engagements. Use this
  skill when the user asks to "set up a notebook for an RFP", "RFPのノートブックを
  作成", "upload RFP to NotebookLM", "RFP資料をアップロード", "extract requirements
  from the RFP", "要件を抽出", "create engagement notebook", "案件ノートブック作成",
  "add amendment to notebook", "追加資料をノートブックに追加", "which notebook has
  the RFP", "RFPはどのノートブックにありますか", "prepare notebook for proposal",
  "提案準備のノートブック設定", "run RFP extraction", "RFP分析を実行", "briefing
  from RFP", "RFPブリーフィング作成", or any request to create, manage, or query
  NotebookLM notebooks for consulting engagements. Also trigger for "notebooklm
  setup", "notebook管理", "source management", "ソース管理", and requests to
  produce a structured RFP brief from uploaded documents.
---
# RFP Notebook Manager (RFP ノートブック管理)

Load the client's RFP/RFQ into NotebookLM, extract it once, systematically, and write the result as
the engagement's **RFP Brief** (`00-rfp-brief.json`). This skill is the **only** one that extracts
from the RFP. Every other skill reads the Brief and queries NotebookLM only for gaps the Brief
records — that is what keeps the proposal, the estimate and the review describing the same project.

Contracts this skill follows:
- Workspace and handoff: `${CLAUDE_PLUGIN_ROOT}/shared/engagement-workspace.md`
- Brief schema and labels: `${CLAUDE_PLUGIN_ROOT}/shared/brief-schema.md`
- NotebookLM flags and fallback ladder: `${CLAUDE_PLUGIN_ROOT}/shared/notebooklm-contract.md`

## Step 1: Workspace and notebook

1. `python3 "${CLAUDE_PLUGIN_ROOT}/sier" status` — no workspace → run `engagement-init` first.
2. Find or create the notebook. Never use `notebooklm use`; pass `--notebook` on every command.
   ```bash
   notebooklm list --json
   notebooklm create "RFP - [Client] - [Project]" --json     # only if none exists
   ```
   | Pattern | Example | When |
   |---------|---------|------|
   | `RFP - [Client] - [Project]` | `RFP - NTT Data - 基幹系統刷新` | Standard engagement |
   | `RFQ - [Client] - [Project]` | `RFQ - MUFG - クラウド移行` | Quote request |

   One notebook per engagement — never mix RFPs.
3. Write the id into `engagement.json` → `notebook_id`.

## Step 2: Load every source before extracting

Upload the RFP plus **all** appendices, Q&A responses, amendments and current-system documents —
extraction quality depends on completeness.

```bash
notebooklm source add ./RFP.pdf --notebook <notebook_id> --json
notebooklm source add ./appendix-a.pdf --notebook <notebook_id> --json
notebooklm source wait <source_id> -n <notebook_id> --timeout 600
notebooklm source list --notebook <notebook_id> --json
```

Proceed only when every source is `"status": "ready"`. Then set `engagement.json` →
`sources_updated_at` to today. `sier status` uses it to flag a Brief that predates its sources.

**If NotebookLM is unreachable**, do not stop: follow the fallback ladder. At tier 3, read the files
directly (`pdf` / `docx` skills or `Read`) and cite by section and page (`RFP §4.1 p.18`). Record the
tier in the Brief's `source_tier` — downstream readers need to know.

## Step 3: Run the standard extraction (26 queries)

Run all of them, each with `--json` so answers come back with `references[].cited_text`. Follow-ups
for thin answers are in `references/extraction-catalog.md`.

#### 3.1 Project Overview (案件概要)

```bash
notebooklm ask "What is the project name, objective, and background? Why is the client undertaking this project now?" --json --notebook <notebook_id>
notebooklm ask "What is the project scope? What is explicitly in-scope and out-of-scope?" --json --notebook <notebook_id>
notebooklm ask "What are the key success criteria or KPIs the client defines for this project?" --json --notebook <notebook_id>
```

#### 3.2 Requirements (要件)

```bash
notebooklm ask "List all functional requirements mentioned in the RFP, organized by business area or module" --json --notebook <notebook_id>
notebooklm ask "List all non-functional requirements: performance targets, security requirements, availability SLA, scalability needs, and accessibility standards" --json --notebook <notebook_id>
notebooklm ask "What are the mandatory technology constraints, platform requirements, or integration standards?" --json --notebook <notebook_id>
notebooklm ask "What data migration or conversion requirements are specified?" --json --notebook <notebook_id>
```

#### 3.3 Timeline & Milestones (スケジュール)

```bash
notebooklm ask "What is the overall project timeline? Start date, end date, and any intermediate deadlines?" --json --notebook <notebook_id>
notebooklm ask "What are the key milestones, phase gates, or checkpoint dates the client expects?" --json --notebook <notebook_id>
notebooklm ask "What is the proposal submission deadline and format requirements?" --json --notebook <notebook_id>
```

#### 3.4 Budget & Commercial (予算・商務)

```bash
notebooklm ask "Is there a stated budget range, budget ceiling, or budget constraints?" --json --notebook <notebook_id>
notebooklm ask "What pricing model does the client prefer: fixed price, time and materials, or other?" --json --notebook <notebook_id>
notebooklm ask "What payment terms, invoicing schedule, or financial conditions are specified?" --json --notebook <notebook_id>
```

#### 3.5 Technical Environment (技術環境)

```bash
notebooklm ask "Describe the client's current IT systems, infrastructure, and technology stack mentioned in the document" --json --notebook <notebook_id>
notebooklm ask "What integrations with existing systems are required? List each system and the integration type" --json --notebook <notebook_id>
notebooklm ask "What security, compliance, or regulatory requirements are mentioned? Include industry-specific regulations" --json --notebook <notebook_id>
notebooklm ask "What are the hosting, deployment, or infrastructure requirements (on-premises, cloud, hybrid)?" --json --notebook <notebook_id>
```

#### 3.6 Team & Process (体制・プロセス)

```bash
notebooklm ask "What team structure, roles, or staffing requirements does the client specify or prefer?" --json --notebook <notebook_id>
notebooklm ask "Does the client prefer a specific development methodology (waterfall, agile, hybrid)? What governance is expected?" --json --notebook <notebook_id>
notebooklm ask "What reporting, communication, or meeting cadence does the client expect?" --json --notebook <notebook_id>
```

#### 3.7 Evaluation & Submission (評価・提出)

```bash
notebooklm ask "What evaluation criteria will the client use to assess proposals? List with weights if provided" --json --notebook <notebook_id>
notebooklm ask "What are the mandatory submission requirements: format, page count, sections, copies, delivery method?" --json --notebook <notebook_id>
notebooklm ask "Are there mandatory qualifications, certifications, or references required from the vendor?" --json --notebook <notebook_id>
```

#### 3.8 Risks & Constraints (リスク・制約)

```bash
notebooklm ask "What risks, constraints, or assumptions does the RFP mention or imply?" --json --notebook <notebook_id>
notebooklm ask "Are there penalty clauses, liquidated damages, or SLA breach consequences specified?" --json --notebook <notebook_id>
notebooklm ask "What are the contract terms for IP ownership, warranty, and liability?" --json --notebook <notebook_id>
```

## Step 4: Write the Brief as JSON

Map every answer into `00-rfp-brief.json` in the workspace, following
`${CLAUDE_PLUGIN_ROOT}/shared/brief-schema.md`:

- **Requirements become rows with ids** — `FR-001…`, `NFR-001…`, `INT-001…`. Effort estimates, the
  compliance matrix and the review board all trace to these ids, so number them once, here.
- **Every fact gets a label.** `RFP` and `RFP+` need a citation — the `cited_text` NotebookLM returned
  (tier 1–2) or section/page (tier 3). If you cannot cite it, it is `Proposed` or it is a gap.
- **Budget is a number or null.** `{"amount": 200000000, "basis": "tax_excluded", …}`. Never turn
  "around 2億" into a number without saying so in the text; never invent a basis.
- **Silence is a gap, not a guess.** Anything a downstream skill needs and the RFP doesn't say becomes
  a `gaps[]` entry with the question to ask the client and `blocks: [skills]`.

Then validate and render — the Markdown is generated, never written by hand:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/sier" brief validate
python3 "${CLAUDE_PLUGIN_ROOT}/sier" brief render
```

Fix every validation error before handing over. `render` also records `generated_at` and
`source_tier` in `engagement.json` and adds a downstream-readiness table to the Markdown.

## Step 5: Amendments and Q&A rounds (追加資料管理)

1. Add the new source and wait for it (Step 2), then update `sources_updated_at`. From this moment
   `sier status` reports the Brief as **stale** to every skill.
2. Run delta queries only:
   ```bash
   notebooklm ask "What changes does the latest amendment make to the original RFP requirements?" --json --notebook <notebook_id>
   notebooklm ask "Does the amendment change the timeline, budget, or evaluation criteria?" --json --notebook <notebook_id>
   notebooklm ask "Are there new requirements added or existing requirements removed by this amendment?" --json --notebook <notebook_id>
   ```
3. Update the Brief JSON: change items in place (keep ids stable — never renumber), add new ids for new
   requirements, close gaps the Q&A answered. Set `generated_at` to today; validate and render.
4. Report the impact:
   | Section | Was | Now | Affected artifacts |
   |---|---|---|---|
   Downstream artifacts computed before the change (`03-estimate`, `05-cost`, …) must be re-run;
   `sier verify` will fail until they are.

## Step 6: Several engagements

`notebooklm list --json` shows notebooks; `ls ./consulting/*/engagement.json` (or under `$SIER_HOME`)
shows workspaces. Run `sier status --ws <folder>` on each for a one-line state. Switch by working in
the other folder — never by `notebooklm use`.

## Output

- `00-rfp-brief.json` — canonical; `00-rfp-brief.md` — rendered for people
- The gaps list (Brief §8) — questions to send the client before the Q&A deadline
- `engagement.json` updated with notebook id, sources date, brief date and tier

## Key principles

- **One extraction.** Downstream skills trust the Brief. If the Brief is wrong, everything is wrong —
  so it is validated, cited and versioned.
- **Gaps are features.** What the RFP doesn't say is as valuable as what it does.
- **Stable ids.** Amendments edit items; they never renumber requirements other artifacts trace to.
- **State the tier.** A Brief read straight from a PDF is valid work, but it says so.
