---
name: proposal-review
description: >
  Conduct multi-perspective review of IT consulting artifacts using an AI review
  board. Use this skill when the user asks to "review the proposal", "提案レビュー",
  "quality check the deliverables", "成果物レビュー", "review from multiple
  perspectives", "多角的レビュー", "get a second opinion on the proposal",
  "proposal quality gate", "品質ゲートレビュー", "review board",
  "レビューボード", "final check before submission", "提出前最終確認", or needs
  a structured multi-viewpoint assessment of consulting deliverables. Also trigger
  for "peer review", "cross-check the proposal", "red team the proposal",
  "devil's advocate review", "提案品質チェック", "QCD review", and any request
  to evaluate proposal artifacts from business, technical, quality, cost, or
  client perspectives before client submission.
---

# Multi-Perspective Proposal Review Board (多角的レビューボード)

Assemble an AI review board of specialist personas that independently review consulting artifacts from distinct perspectives, surface conflicts through structured debate, and deliver a consensus assessment with actionable recommendations.

## Why This Matters

In Japanese SIer culture, proposals go through multiple rounds of internal review (社内レビュー) before client submission. Senior consultants, technical architects, commercial managers, and quality leads each catch different problems. A proposal that looks solid from one perspective often has blind spots visible from another. This skill simulates that multi-stakeholder review process, catching issues that a single-perspective review misses — and it does it before the client finds them.

The difference between a 60% win rate and an 80% win rate is often the quality of internal review, not the quality of initial drafting.

## The Review Board

Each reviewer is a separate agent. Independence is structural: every reviewer runs in its own fresh
context, reads the same artifacts, and never sees another reviewer's report. (Before v2.1 the six personas
ran one after another in a single conversation, so each one read its predecessors' verdicts — the
"independent review" this skill promised was not possible. Running them as agents fixes that.)

| Agent (`subagent_type`) | Persona | Scorecard dimension | Key question |
|---|---|---|---|
| `it-consulting-expert:review-business` | Business Strategist (事業戦略) | Business Alignment | Does winning this make us stronger? |
| `it-consulting-expert:review-architect` | Technical Architect (技術アーキテクト) | Technical Soundness | Can we build this as specified? |
| `it-consulting-expert:review-qcd` | QCD Controller (品質・コスト・納期) | QCD Balance | On time, on budget, at quality? |
| `it-consulting-expert:review-risk` | Risk & Compliance (リスク・コンプライアンス) | Risk & Compliance | What's the worst case, and are we protected? |
| `it-consulting-expert:review-client` | Client Advocate (顧客視点) | Client Readiness | Would the client feel confident choosing us? |
| `it-consulting-expert:review-delivery` | Delivery PM (デリバリーPM) | Delivery Feasibility | Could I run this from day one? |
| `it-consulting-expert:review-security` | Security Specialist — optional | Security | What would an attacker or auditor find? |
| `it-consulting-expert:review-legal-ja` | Legal Counsel (Japan) — optional | Legal | What do the contract and the law say if it fails? |

Each agent file holds that persona's mandate, perspective, bias, checklist pointer and report format.
Add Security for sensitive data, government or financial clients; add Legal for large fixed-price deals,
unusual terms or multi-vendor structures. The reviewers are read-only (`Read`, `Grep`, `Glob`).

## Workflow

### Step 0: Prepare the evidence

1. `python3 "${CLAUDE_PLUGIN_ROOT}/sier" status` to find the workspace.
2. **Run `python3 "${CLAUDE_PLUGIN_ROOT}/sier" verify`.** It recomputes every engine artifact from its
   inputs and cross-checks estimate ↔ team ↔ cost ↔ budget, writing `_state/verify.md`. Reviewers judge
   the numbers; the engine has already proved the arithmetic. A FAIL here is itself a Critical finding.
3. Decide scope with the user if it isn't obvious: which artifacts (default — everything in the pipeline
   that exists), and which optional reviewers.

Artifacts usually in scope: `artifacts/proposal.docx` (or `proposal-draft.md`), `02-architecture.md`,
`03-estimate.md`, `04-team.md`, `05-cost.md`, `06-delivery-plan.md`, `01-go-nogo.md`, presentation decks,
`07-sla.md` for maintenance bids. Client requirements come from `00-rfp-brief.json` — no NotebookLM
queries are needed here.

### Step 1: Independent reviews — dispatch all reviewers at once

Issue **one Agent call per reviewer, all in the same message**, so they run in parallel. Each prompt:

```
Workspace: <absolute path>
Artifacts in scope: <list of relative paths>
Engine verification: _state/verify.md (<PASS | FAIL — n problems>)
Client: <name> — language of findings: <ja | en>
Review independently and return your report in the format your instructions define.
```

The prompt must not mention other reviewers' views, earlier review rounds, or what you expect them to find.

When the reports come back, save each one **verbatim** to `_state/review/<persona>.md`
(`business.md`, `architect.md`, …) before reading across them. That file is the record of what each
reviewer said independently.

**If agents are unavailable on this surface:** run the personas one at a time in this conversation by
reading each `agents/review-*.md` file from `${CLAUDE_PLUGIN_ROOT}`, writing each report to
`_state/review/` before starting the next, and never re-reading earlier reports during later ones. State
in the consensus report that the reviews were sequential and therefore not fully independent.

### Step 2: Cross-Review Conflict Detection (矛盾検出)

After every reviewer has reported, read across the saved reports and identify conflicts — findings where personas disagree:

**Conflict Types:**

| Type | Example | Resolution Method |
|------|---------|-------------------|
| Priority conflict | Business says "accept lower margin for strategic value" vs. QCD says "margin too thin" | Weighted debate |
| Feasibility conflict | Technical says "architecture is solid" vs. Delivery PM says "team can't build this in time" | Evidence-based resolution |
| Scope conflict | Client Advocate says "add more detail" vs. QCD says "scope is already too large" | Client criteria arbitration |
| Risk tolerance conflict | Risk Officer flags a clause vs. Business says "standard in this industry" | Precedent and data review |

### Step 3: Structured Debate (構造化討論)

For each conflict, facilitate a structured debate between the disagreeing personas:

**Debate Format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEBATE #[N]: [Topic]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POSITION A: [Persona Name]
"[Their argument — 2-3 sentences max, with evidence]"
Evidence: [Data point, RFP citation, or industry benchmark]

POSITION B: [Persona Name]
"[Their counter-argument — 2-3 sentences max, with evidence]"
Evidence: [Data point, RFP citation, or industry benchmark]

REBUTTAL A: [One sentence response to Position B]

REBUTTAL B: [One sentence response to Position A]

MEDIATOR ANALYSIS:
- Position A strength: [What's valid about this view]
- Position B strength: [What's valid about this view]
- Key trade-off: [What we're actually choosing between]

RESOLUTION: [Specific decision]
Rationale: [Why this resolution, referencing both positions]
Confidence: High / Medium / Low
Dissent noted: [If any persona still disagrees, record it]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Debate Rules:**
- Arguments must reference evidence (RFP citations, benchmarks, historical data)
- No ad hominem — critique the position, not the persona
- Each persona gets exactly one argument + one rebuttal
- The mediator (neutral facilitator) synthesizes and proposes resolution
- Resolution must be actionable — not "consider further" but "do X specifically"
- Dissenting views are recorded, not suppressed

### Step 4: Consensus Report (合意レビュー報告書)

Produce the final consolidated review:

**Header:**
| Field | Value |
|-------|-------|
| Review Date | YYYY/MM/DD |
| Artifacts Reviewed | [List] |
| Review Board | <n> reviewers (agents, independent) |
| Overall Verdict | ✅ READY / ⚠️ CONDITIONAL / ❌ NOT READY |

**1. Executive Summary (総括)**
3-5 sentences: overall assessment, top strengths, and critical gaps. Written for a senior executive who will decide whether to submit.

**2. Consensus Scorecard (合意スコアカード)**

| Dimension | Score (1-5) | Status | Key Finding |
|-----------|------------|--------|-------------|
| Business Alignment | X.X | 🟢/🟡/🔴 | [One line] |
| Technical Soundness | X.X | 🟢/🟡/🔴 | [One line] |
| QCD Balance | X.X | 🟢/🟡/🔴 | [One line] |
| Risk & Compliance | X.X | 🟢/🟡/🔴 | [One line] |
| Client Readiness | X.X | 🟢/🟡/🔴 | [One line] |
| Delivery Feasibility | X.X | 🟢/🟡/🔴 | [One line] |
| **Overall** | **X.X** | | |

Scoring: 🟢 ≥ 4.0 | 🟡 3.0–3.9 | 🔴 < 3.0

**3. Must-Fix Items (必須修正事項)**
Critical and Major findings that ALL personas agree must be addressed before submission. Sorted by impact.

| # | Finding | Severity | Owner | Deadline | Personas Agreed |
|---|---------|----------|-------|----------|----------------|
| 1 | | Critical | | | All 6 / 5 of 6 |

**4. Debate Resolutions (討論結果)**
Summary of each conflict that was debated, the resolution reached, and any recorded dissent.

**5. Strengths to Preserve (維持すべき強み)**
Things the review board identified as strong — don't accidentally weaken these during revision.

**6. Should-Fix Items (推奨修正事項)**
Minor findings that would strengthen the proposal if time permits. Prioritized.

**7. Observations for Future (今後の改善提案)**
Patterns noticed that don't affect this proposal but should inform future ones. Feed into `lessons-learned`.

### Step 5: Revision Tracking (修正追跡)

After the user fixes items, re-run `sier verify`, then re-dispatch **only the reviewers whose findings
were addressed**, on the changed artifacts, telling them which finding ids to check. Produce a delta
report (Fixed / Partially fixed / Not fixed) and update the scorecard. Keep earlier rounds in
`_state/review/round-<n>/`.

### Step 6: Output

Save the consensus report as `_state/review/consensus.md` (this is what `sier status` looks for), then
generate .docx with the `docx` skill:
1. **Full Review Report** (レビュー報告書) — all findings, debates and consensus
2. **Executive Summary** (エグゼクティブサマリー) — one-page verdict for decision-makers
3. **Revision Checklist** (修正チェックリスト) — fixes with owners

Patterns worth keeping for future bids go to `lessons-learned`.

## Custom reviewers

Beyond the two optional agents, add a specialist (Industry Expert, UX, Data/AI, Financial Controller)
by copying an `agents/review-*.md` file in the plugin, changing its mandate, lens and dimension, and
dispatching it alongside the others. Until such an agent exists, a custom persona can run in this
conversation — note that it was not independent.

## Key Principles

- **Independence first, consensus second**: Reviewers are separate agents that never see each other's reports; mediation happens only after all have reported
- **Evidence over opinion**: Every finding must cite a specific artifact section, RFP requirement, or industry benchmark. "I feel like the estimate is too low" is not a finding
- **Severity discipline**: Not everything is Critical. Over-flagging trains the team to ignore findings
- **Debate is productive**: Disagreement between personas is a FEATURE — it surfaces real trade-offs that single-perspective reviews miss
- **Dissent is recorded**: If a persona disagrees with the consensus, their view is documented. Sometimes the minority is right
- **Strengths matter**: A review that only finds problems demoralizes the team and misses what's working
- **Revision loop**: The review isn't done until the must-fix items are verified fixed

For review checklists, debate facilitation, and scoring rubrics, read `references/review-checklists.md`.
