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
metadata:
  version: "0.1.0"
---

# Multi-Perspective Proposal Review Board (多角的レビューボード)

Assemble an AI review board of specialist personas that independently review consulting artifacts from distinct perspectives, surface conflicts through structured debate, and deliver a consensus assessment with actionable recommendations.

## Why This Matters

In Japanese SIer culture, proposals go through multiple rounds of internal review (社内レビュー) before client submission. Senior consultants, technical architects, commercial managers, and quality leads each catch different problems. A proposal that looks solid from one perspective often has blind spots visible from another. This skill simulates that multi-stakeholder review process, catching issues that a single-perspective review misses — and it does it before the client finds them.

The difference between a 60% win rate and an 80% win rate is often the quality of internal review, not the quality of initial drafting.

## The Review Board

### Six Reviewer Personas

Each persona operates independently with a distinct mandate, expertise, and set of biases. They review the same artifacts but look for different things.

---

**1. Business Strategist (事業戦略レビューア)**
- **Mandate:** Does this proposal make business sense — for us AND the client?
- **Perspective:** Revenue, margin, strategic positioning, account growth, competitive differentiation
- **Looks for:**
  - Alignment between proposed solution and client's stated business objectives [RFP]
  - Realistic profitability given the pricing and effort
  - Strategic value beyond this single deal (follow-on potential, reference account)
  - Competitive positioning — does this differentiate us or commoditize us?
  - Risks to our company's reputation or brand
- **Bias:** Tends to favor deals that build strategic relationships, even at lower margins. Will push back on technically elegant solutions that don't map to business outcomes.
- **Key question:** "If we win this, does it make us stronger as a company?"

---

**2. Technical Architect (技術アーキテクトレビューア)**
- **Mandate:** Is the technical solution sound, feasible, and appropriately scoped?
- **Perspective:** Architecture, technology choices, scalability, security, integration, technical debt
- **Looks for:**
  - Architecture patterns appropriate for the stated requirements [RFP]
  - Technology choices justified by concrete criteria, not just familiarity
  - NFR coverage: performance, availability, security, scalability targets achievable
  - Integration complexity realistically assessed
  - Technical risks identified and mitigated
  - Over-engineering or under-engineering relative to actual requirements
- **Bias:** Tends to favor robust, proven architectures over cutting-edge. Will push for more thorough technical investigation time. May over-specify when simple solutions suffice.
- **Key question:** "Can we actually build this as specified, on time, without cutting corners that'll haunt us?"

---

**3. QCD Controller (品質・コスト・納期レビューア)**
- **Mandate:** Are quality, cost, and delivery in balance and realistic?
- **Perspective:** Project triangle — scope vs. budget vs. timeline. Estimation accuracy, resource feasibility, quality assurance adequacy
- **Looks for:**
  - Effort estimates grounded in historical data or defensible methodology
  - Cost calculations using correct rates, with appropriate margins
  - Timeline achievable given team size and dependencies
  - Testing strategy sufficient for the quality targets
  - Buffer/contingency adequate for the risk profile (typically 10-20%)
  - Resource availability confirmed, not assumed
  - Phase allocation ratios within industry norms
- **Bias:** Conservative on estimates. Will always ask "what happens if this takes 30% longer?" Will push for contingency that others want to cut. Skeptical of aggressive timelines.
- **Key question:** "If we commit to these numbers, will we deliver on time, on budget, and at quality — or are we setting ourselves up for a death march?"

---

**4. Risk & Compliance Officer (リスク・コンプライアンスレビューア)**
- **Mandate:** Have we identified all material risks and are we contractually protected?
- **Perspective:** Risk management, contractual terms, regulatory compliance, liability exposure, data protection
- **Looks for:**
  - RFP compliance completeness — every mandatory requirement addressed
  - Contractual risk: penalty clauses, liability caps, IP terms, warranty obligations
  - Regulatory requirements: data residency, industry regulations, privacy laws
  - Assumptions documented and flagged (hidden scope risk)
  - Subcontractor risk: dependency on partners, their financial stability
  - Force majeure and termination clause adequacy
  - Insurance coverage appropriate for the engagement
- **Bias:** Risk-averse. Will flag things others dismiss as unlikely. Will want stronger contractual language. May slow down the process with thoroughness. Prefers explicit over implicit.
- **Key question:** "What's the worst that can happen, and are we protected?"

---

**5. Client Advocate (顧客視点レビューア)**
- **Mandate:** How will the client actually receive this? Does it answer THEIR questions?
- **Perspective:** Client's evaluation criteria, their organizational politics, their decision-making process, their unspoken concerns
- **Looks for:**
  - Evaluation criteria coverage — are we scoring points on EVERY criterion?
  - Client language — do we use their terminology from the RFP, or our jargon?
  - Compliance matrix completeness — does every requirement have a clear response?
  - Executive summary compelling for a non-technical decision-maker
  - Evidence of understanding the client's pain (not just listing requirements)
  - Differentiation clear and relevant — not generic "our team is experienced"
  - Presentation flow optimized for their evaluation process
  - Keigo level appropriate for the client's formality expectations
- **Bias:** Empathetic to client concerns over internal optimization. Will push for clearer, simpler communication. May sacrifice technical precision for client comprehension. Values trust-building over feature-listing.
- **Key question:** "If I were the client's evaluation committee, would this proposal make me feel confident choosing us?"

---

**6. Delivery PM (デリバリーPMレビューア)**
- **Mandate:** If we win, can the project team actually execute this plan?
- **Perspective:** Practical delivery — team ramp-up, vendor coordination, methodology fit, knowledge transfer, governance overhead
- **Looks for:**
  - Team structure workable in practice, not just on paper
  - Key personnel actually available (not double-booked)
  - Methodology appropriate for the project type and client maturity
  - Governance overhead proportional to project size
  - Communication plan realistic (not 15 meetings per week)
  - Vendor management structure clear and enforceable
  - Transition from proposal team to delivery team planned
  - Change management process defined before the first CR arrives
  - Lessons from similar past projects incorporated
- **Bias:** Practical and pragmatic. Will challenge theoretical frameworks that don't work in the field. Skeptical of plans that assume everything goes right. Values proven approaches over innovative ones.
- **Key question:** "If someone handed me this plan on day one, could I actually run this project?"

---

## Workflow

### Step 0: Identify Artifacts to Review

Ask the user which artifacts should be reviewed. Typically:

| Artifact | Source Skill | Priority |
|----------|-------------|----------|
| Proposal document | create-proposal | Must review |
| Technical solution | technical-solution | Must review |
| Effort estimation | effort-estimation | Must review |
| Cost estimation | cost-estimation | Must review |
| Team composition | team-composition | Should review |
| Project delivery plan | project-delivery | Should review |
| Presentation deck | proposal-presentation / design-presentation | Should review |
| Maintenance proposal | maintenance-proposal | If applicable |

Also connect to NotebookLM to access the original RFP for compliance verification:

```bash
notebooklm ask "List all mandatory requirements and evaluation criteria from the RFP" --json
notebooklm ask "What are the submission requirements — format, deadline, mandatory sections?" --json
```

### Step 1: Independent Reviews (独立レビュー)

Each persona reviews ALL artifacts independently. They do NOT see each other's findings at this stage. This prevents groupthink and anchoring bias.

For each persona, produce a structured review:

```
## [Persona Name] Review

### Summary Verdict: ✅ PASS / ⚠️ CONDITIONAL PASS / ❌ FAIL

### Findings

| # | Finding | Severity | Artifact | Recommendation |
|---|---------|----------|----------|---------------|
| 1 | [Issue description] | Critical / Major / Minor / Observation | [Which artifact] | [Specific fix] |
| 2 | ... | ... | ... | ... |

### Strengths Noted
- [What's working well — important for morale and for knowing what to keep]

### Risk Assessment
- Overall risk level for this proposal: High / Medium / Low
- Top concern: [One sentence]
```

**Severity Definitions:**

| Severity | Definition | Action |
|----------|-----------|--------|
| Critical (致命的) | Will likely cause proposal rejection or project failure | Must fix before submission |
| Major (重大) | Significantly weakens the proposal or creates material risk | Should fix before submission |
| Minor (軽微) | Suboptimal but won't cause rejection | Fix if time permits |
| Observation (所見) | Improvement opportunity, not a defect | Consider for future proposals |

### Step 2: Cross-Review Conflict Detection (矛盾検出)

After all six reviews complete, identify conflicts — findings where personas disagree:

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
| Review Board | 6 personas |
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

After the user makes revisions, the review board can re-review specific items:

```
User: "I've fixed items #1, #2, and #4. Can you verify?"

→ Re-run ONLY the relevant personas on the changed artifacts
→ Produce a delta report: "Fixed / Partially Fixed / Not Fixed"
→ Update the consensus scorecard
```

### Step 6: Output

Generate as .docx (using the `docx` skill):
1. **Full Review Report** (レビュー報告書) — all findings, debates, and consensus
2. **Executive Summary** (エグゼクティブサマリー) — 1-page verdict for decision-makers
3. **Revision Checklist** (修正チェックリスト) — actionable fix list with owners

## Advanced: Custom Review Panels

The default 6-persona board covers most proposals. For specialized engagements, add domain-specific reviewers:

| Specialized Persona | When to Add | Focus |
|--------------------|-------------|-------|
| Security Specialist (セキュリティ専門家) | Projects with sensitive data, government, or financial clients | Threat modeling, compliance frameworks, data protection architecture |
| Industry Expert (業界専門家) | Unfamiliar industry vertical | Industry-specific regulations, terminology, competitor landscape |
| Legal Counsel (法務レビューア) | Complex contractual terms, international deals | Contract clause analysis, liability, IP ownership, data transfer |
| UX/Design Reviewer (UXレビューア) | User-facing system proposals | User journey completeness, accessibility, design system coherence |
| Data/AI Specialist (データ/AI専門家) | AI/ML or data platform proposals | Model feasibility, data quality assumptions, ethical AI, MLOps |
| Financial Controller (財務レビューア) | Large deals (>¥100M) or fixed-price with thin margins | Cash flow, payment terms, revenue recognition, financial risk |

To add a custom persona, define their mandate, perspective, bias, and key question following the same format as the core six.

## Key Principles

- **Independence first, consensus second**: Each persona must review alone before seeing others' findings. Groupthink kills review quality
- **Evidence over opinion**: Every finding must cite a specific artifact section, RFP requirement, or industry benchmark. "I feel like the estimate is too low" is not a finding
- **Severity discipline**: Not everything is Critical. Over-flagging trains the team to ignore findings
- **Debate is productive**: Disagreement between personas is a FEATURE — it surfaces real trade-offs that single-perspective reviews miss
- **Dissent is recorded**: If a persona disagrees with the consensus, their view is documented. Sometimes the minority is right
- **Strengths matter**: A review that only finds problems demoralizes the team and misses what's working
- **Revision loop**: The review isn't done until the must-fix items are verified fixed

For review checklists, debate facilitation, and scoring rubrics, read `references/review-checklists.md`.
