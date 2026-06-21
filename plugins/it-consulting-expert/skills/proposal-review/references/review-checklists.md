# Review Checklists & Scoring Rubrics (レビューチェックリスト)

## Per-Persona Checklists

### 1. Business Strategist Checklist

**Strategic Alignment:**
- [ ] Proposal addresses the client's stated business objectives, not just technical requirements
- [ ] Executive summary leads with business value, not technical features
- [ ] ROI or value proposition is quantified where possible
- [ ] Solution addresses the "why now" — urgency and opportunity cost of inaction
- [ ] Competitive positioning is specific to THIS deal, not generic company strengths

**Commercial Viability:**
- [ ] Gross margin meets company threshold (typical: >15% for fixed price, >25% for T&M)
- [ ] Pricing model appropriate for the scope certainty level
- [ ] Payment terms are cash-flow positive (no >60-day gaps without milestone payments)
- [ ] Follow-on revenue potential identified (maintenance, Phase 2, adjacent projects)
- [ ] Deal size justifies the proposal investment (effort spent on this bid)

**Account Strategy:**
- [ ] Proposal positions us for a long-term relationship, not just this transaction
- [ ] References and case studies are relevant to the client's industry
- [ ] Key differentiators are defensible — not easily claimed by competitors
- [ ] Win themes are consistent across all artifacts (proposal, presentation, Q&A)

---

### 2. Technical Architect Checklist

**Architecture:**
- [ ] Architecture pattern appropriate for scale and complexity requirements [RFP]
- [ ] C4 model views present and consistent (Context → Container → Component)
- [ ] All integration points identified with protocol/format specified
- [ ] Data model or data flow diagram present for data-intensive solutions
- [ ] Deployment architecture addresses stated environment constraints [RFP]

**Technology Choices:**
- [ ] Every technology choice has a stated justification (not just "we know it")
- [ ] Decision matrix documents alternatives considered
- [ ] Technology versions specified (not just "Java" but "Java 21 LTS")
- [ ] Licensing implications considered (cost, restrictions, compliance)
- [ ] Technology maturity appropriate — no bleeding-edge tech for conservative clients

**Non-Functional Requirements:**
- [ ] Performance targets stated with measurement approach
- [ ] Availability/SLA targets achievable with the proposed architecture
- [ ] Security architecture addresses compliance requirements [RFP]
- [ ] Scalability approach defined (horizontal/vertical, auto-scaling triggers)
- [ ] Disaster recovery and backup strategy present
- [ ] Monitoring and observability approach defined

**Feasibility:**
- [ ] No stated requirement is technically impossible or impractical
- [ ] Known technical risks documented with mitigation
- [ ] Proof of concept recommended for high-uncertainty components
- [ ] Team has experience with the proposed technology stack

---

### 3. QCD Controller Checklist

**Quality (品質):**
- [ ] Testing strategy covers unit, integration, system, UAT
- [ ] Test coverage targets defined and measurable
- [ ] Defect density targets stated with industry benchmarks
- [ ] Code review process defined
- [ ] Quality gate criteria specified per phase transition

**Cost (コスト):**
- [ ] Effort estimates based on WBS or Function Points, not gut feeling
- [ ] Rate cards use current market rates for the specified seniority levels
- [ ] Overhead and margin clearly separated from direct costs
- [ ] Contingency/buffer included (10-20% typical)
- [ ] Total cost vs. RFP budget ceiling checked — within range or explained
- [ ] Cost breakdown granularity appropriate for proposal stage

**Delivery (納期):**
- [ ] Timeline accounts for all SIer phases (要件定義 through 移行)
- [ ] Phase duration ratios are within industry norms:
  - Requirements + Design: 30-40% of total
  - Development: 25-35%
  - Testing: 20-30%
  - Migration/Release: 5-10%
- [ ] Critical path identified — what determines the end date?
- [ ] Dependencies on client (approvals, data, access) have scheduled dates
- [ ] Buffer between completion and contractual deadline (≥2 weeks for large projects)

**Balance Check:**
- [ ] The three constraints are balanced — no single one is impossibly tight
- [ ] If one constraint is tight (e.g., aggressive timeline), the others compensate (e.g., more resources)
- [ ] "Fast, good, cheap — pick two" principle visibly applied

---

### 4. Risk & Compliance Officer Checklist

**RFP Compliance:**
- [ ] Every mandatory requirement in the RFP has a corresponding response
- [ ] Compliance matrix is complete — no gaps or "TBD" for mandatory items
- [ ] Submission format requirements met (page count, file format, sections)
- [ ] Mandatory certifications confirmed (ISO, PMS, specific tech certs)
- [ ] Submission deadline achievable with current progress

**Contractual Risk:**
- [ ] Penalty clauses reviewed — exposure capped and proportional
- [ ] Liquidated damages within acceptable limits
- [ ] IP ownership terms clear — work-for-hire vs. license
- [ ] Warranty period and scope defined
- [ ] Termination clauses protect both parties
- [ ] Force majeure clause present and reasonable
- [ ] Limitation of liability capped (typically at contract value)

**Regulatory & Data:**
- [ ] Data residency requirements addressed (Japan data center if required)
- [ ] Privacy law compliance (個人情報保護法, GDPR if applicable)
- [ ] Industry-specific regulations identified and addressed
- [ ] Security standards met (ISO 27001, SOC 2, etc.)
- [ ] Subcontractor data handling agreements planned

**Assumptions & Gaps:**
- [ ] All assumptions documented and labeled [Proposed] or [RFP+]
- [ ] "Not specified in RFP" items explicitly listed
- [ ] Responsibility boundaries clear (what client provides vs. what we provide)
- [ ] Exclusions clearly stated

---

### 5. Client Advocate Checklist

**Evaluation Criteria Alignment:**
- [ ] Every evaluation criterion from the RFP is addressed in the proposal
- [ ] Proposal structure follows the evaluation criteria order (where known)
- [ ] Highest-weighted criteria receive the most attention/detail
- [ ] Scoring aids present — make it easy for evaluators to give us points

**Communication Quality:**
- [ ] Executive summary is compelling in under 2 minutes of reading
- [ ] Client's terminology used throughout (not our internal jargon)
- [ ] RFP requirement IDs referenced consistently
- [ ] [RFP] / [Proposed] / [RFP+] labeling clear and consistent
- [ ] Japanese keigo level appropriate (丁寧語 vs. 尊敬語 vs. 謙譲語)
- [ ] No spelling/grammar errors (especially in Japanese — these signal carelessness)

**Trust Signals:**
- [ ] Evidence of deep RFP reading (specific citations, not generic responses)
- [ ] Understanding of client's business context, not just technical requirements
- [ ] Relevant case studies with quantified outcomes
- [ ] Named key personnel with relevant experience
- [ ] Proactive risk identification (shows maturity, not incompetence)

**Presentation Readiness:**
- [ ] Slide deck hits all evaluation criteria
- [ ] Visual quality professional (consistent design, no clip art)
- [ ] Q&A preparation covers likely client concerns
- [ ] Timing realistic for the allocated presentation slot

---

### 6. Delivery PM Checklist

**Team Feasibility:**
- [ ] Key personnel (PM, Architect, TL) confirmed available for the project dates
- [ ] Team ramp-up plan realistic — not "full team from day one"
- [ ] Skill gaps identified and addressed (training, hiring, partnering)
- [ ] No individual allocated at >100% across concurrent projects
- [ ] Backup plan for key person departure

**Methodology Fit:**
- [ ] Methodology matches client preference from RFP
- [ ] Phase gate criteria are achievable and measurable
- [ ] Governance overhead proportional to project size
  - Small (<10人月): Weekly status meeting sufficient
  - Medium (10-50人月): Bi-weekly steering + weekly operational
  - Large (>50人月): Monthly steering + bi-weekly steering + weekly operational

**Operational Readiness:**
- [ ] Communication plan is realistic (not 15 meetings/week)
- [ ] Tool chain defined (project management, source control, CI/CD, communication)
- [ ] Development environment provisioning timeline reasonable
- [ ] Knowledge transfer from proposal team to delivery team planned
- [ ] Change management process defined BEFORE project start
- [ ] Lessons from similar past projects visibly incorporated

**Vendor Management (if subcontractors involved):**
- [ ] RACI matrix covers all key activities
- [ ] Quality gates for subcontractor deliverables defined
- [ ] Bridge SE allocated for offshore work
- [ ] Single contact point (一窓口) principle enforced
- [ ] Vendor onboarding timeline included in project schedule

---

## Consensus Scoring Rubric

### Score Definitions (1-5 scale)

| Score | Label | Definition |
|-------|-------|-----------|
| 5 | Excellent (優秀) | No critical/major findings. Strengths outweigh minor observations. Ready to submit as-is |
| 4 | Good (良好) | No critical findings. Few major findings with clear fixes. Ready after minor revisions |
| 3 | Adequate (可) | No critical findings but multiple major findings. Needs revision before submission |
| 2 | Weak (要改善) | One or more critical findings. Significant revision required. Submission risky |
| 1 | Inadequate (不可) | Multiple critical findings. Fundamental rework needed. Do not submit |

### Overall Verdict Thresholds

| Overall Score | Verdict | Action |
|--------------|---------|--------|
| ≥ 4.0 | ✅ READY TO SUBMIT | Fix minor items if time permits. Submit with confidence |
| 3.5–3.9 | ⚠️ CONDITIONAL — MINOR REVISION | Fix major items (estimated <1 day effort). Re-verify changed sections |
| 3.0–3.4 | ⚠️ CONDITIONAL — SIGNIFICANT REVISION | Fix major items (estimated 2-3 days). Re-run targeted review after revision |
| 2.0–2.9 | ❌ NOT READY — MAJOR REVISION | Critical issues must be resolved. Full re-review after revision |
| < 2.0 | ❌ NOT READY — FUNDAMENTAL REWORK | Reconsider whether to bid. If proceeding, substantial rework + full re-review |

---

## Debate Facilitation Guide

### When to Trigger Debate

A debate is triggered when:
1. Two or more personas give conflicting severity ratings on the same item (e.g., one says Critical, another says Minor)
2. Two personas recommend contradictory actions (e.g., "add more detail" vs. "reduce scope")
3. A finding from one persona is directly challenged by another's strength assessment
4. The resolution affects the overall verdict (e.g., a single Critical finding pulls score below threshold)

### Debate Resolution Principles

**Evidence hierarchy (strongest to weakest):**
1. RFP citation — what the client explicitly stated
2. Contractual obligation — what we're legally bound to
3. Historical data — what happened in similar past projects
4. Industry benchmark — what's standard practice
5. Expert judgment — what experienced practitioners recommend
6. Theoretical best practice — what frameworks say

When evidence conflicts, higher-numbered evidence yields to lower-numbered.

**Tie-breaking rules:**
- If the debate affects client evaluation criteria → Client Advocate's perspective weights higher
- If the debate affects delivery feasibility → Delivery PM's perspective weights higher
- If the debate affects financial risk → QCD Controller's perspective weights higher
- If all else is equal → the more conservative position wins (downside protection)

### Common Debate Patterns

**"Good enough vs. gold-plated"**
Technical Architect wants comprehensive solution vs. QCD Controller wants minimum viable. Resolution: map the disputed items to evaluation criteria. If the client scores them, include them. If not, mark as "Phase 2 enhancement."

**"Risk tolerance mismatch"**
Risk Officer flags a contractual clause vs. Business Strategist says it's industry standard. Resolution: check precedent in similar past deals. If no precedent, flag for legal review but don't block submission.

**"Scope vs. timeline"**
Client Advocate wants more detail vs. QCD Controller says scope is already over budget. Resolution: identify which details are evaluation criteria (must include) vs. nice-to-have (move to appendix).

---

## Review Session Timing Guide

| Project Size | Review Time | Revision Time | Re-Review Time |
|-------------|------------|---------------|----------------|
| Small proposal (<20 pages) | 2-3 hours | 1 day | 1 hour |
| Medium proposal (20-50 pages) | 4-6 hours | 2-3 days | 2-3 hours |
| Large proposal (50+ pages) | Full day | 3-5 days | Half day |

**Rule of thumb:** Schedule the review at least 1 week before submission deadline to allow time for revision and re-review.

---

## Integration with Other Skills

- **rfp-analysis**: Review board validates that the Go/No-Go assessment was correct
- **create-proposal**: Primary artifact being reviewed
- **effort-estimation**: QCD Controller's primary focus
- **cost-estimation**: Business Strategist and QCD Controller dual-review
- **technical-solution**: Technical Architect's primary focus
- **project-delivery**: Delivery PM's primary focus
- **proposal-presentation**: Client Advocate reviews for evaluation alignment
- **lessons-learned**: Review findings feed into organizational learning
