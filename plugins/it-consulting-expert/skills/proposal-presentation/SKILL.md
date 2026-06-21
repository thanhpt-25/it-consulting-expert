---
name: proposal-presentation
description: >
  Generate proposal defense presentation materials for Japanese bidding processes.
  Use this skill when the user asks to "create a presentation for the proposal",
  "提案プレゼン資料を作成", "prepare for the proposal defense", "make slides for
  the bid", "プレゼン準備", "pitch deck for the proposal", or needs presentation
  materials to accompany a consulting proposal. Also trigger for "提案説明会",
  "proposal pitch", "client presentation", "見積説明資料", and any request to
  create slides or talking points for presenting a proposal to the client.
  This skill should run AFTER create-proposal — it converts the full proposal
  into a focused presentation.
metadata:
  version: "0.1.0"
---

# Proposal Presentation (提案プレゼン資料)

Generate presentation materials for Japanese proposal defense meetings (提案説明会). In Japanese SIer bidding, the presentation is often where bids are won or lost — a technically superior proposal can lose to a better-presented one.

## Why This Matters

Japanese enterprise procurement typically involves a formal presentation where vendors have 15-30 minutes to present, followed by 15-30 minutes of Q&A. The evaluation committee scores both the document and the presentation. Your slides must hit every evaluation criterion while telling a compelling story.

## Workflow

### Step 0: Connect to NotebookLM

Query the RFP for presentation-critical information:

```bash
notebooklm ask "What is the proposal presentation format — time limit, number of attendees, presentation date, any format requirements?" --json
notebooklm ask "What are the evaluation criteria and their weights for this proposal?" --json
notebooklm ask "Who are the key decision-makers and what are their likely concerns — technical, business, or political?" --json
```

### Step 1: Gather Inputs

- **The completed proposal** (from `create-proposal` skill)
- **Presentation time limit** (default: 20 minutes if not specified)
- **Audience**: CIO-level, department heads, technical evaluators, procurement
- **Language**: Japanese, English, or bilingual
- **Format**: .pptx (using the `pptx` skill)

### Step 2: Presentation Structure

Follow this structure optimized for Japanese enterprise presentations:

**Slide 1: Title (表紙)**
- Proposal title, client name (御中), your company name and logo
- Date, presenter name and title
- 秘密保持 (Confidential) mark

**Slide 2: Agenda (本日のご説明内容)**
- Numbered list of sections, aligned to evaluation criteria order
- Time allocation per section

**Slide 3: Executive Summary (ご提案の概要)**
- ONE slide: problem → solution → outcome → investment
- This is the most important slide — if they remember nothing else, they remember this
- Keep to 4-5 bullet points maximum

**Slides 4-5: Understanding of Client Needs (お客様の課題認識)**
- Demonstrate you understood the RFP deeply
- Restate the client's problem in THEIR language (from RFP citations)
- Show empathy for their pain points — don't just list requirements
- This is where you prove "we read your RFP carefully, not just skimmed it"

**Slides 6-8: Proposed Solution (ご提案内容)**
- Solution architecture diagram (simple, max 7-8 components)
- Key features mapped to client's stated requirements
- Technology stack with ONE-LINE justification per choice
- Differentiation point (差別化ポイント) — what makes your approach unique

**Slide 9: Project Approach (プロジェクトアプローチ)**
- Methodology choice and rationale (1 slide)
- Phase overview with timeline bar
- Quality assurance highlights

**Slide 10: Team Structure (プロジェクト体制)**
- Organization chart — keep simple, show only key roles
- Highlight key member qualifications relevant to THIS project
- If possible, name the PM and TL (clients want to know WHO, not just roles)

**Slide 11: Schedule (スケジュール)**
- Gantt chart or timeline visual
- Key milestones aligned to RFP deadlines
- Go/No-Go gate points

**Slide 12: Cost Summary (費用概要)**
- Summary table only — NOT the detailed breakdown
- Total by phase or year
- Payment schedule
- Note: detailed cost breakdown is in the proposal document

**Slide 13: Our Strengths / Why Us (弊社の強み)**
- 3-4 differentiators directly relevant to THIS project
- Past project examples (similar scale, industry, technology)
- Client testimonials or statistics if available
- DO NOT make this generic — every point must connect to the RFP

**Slide 14: Risk Management (リスクと対策)**
- Top 3-5 risks only (not the full register)
- For each: risk → our mitigation → why client can feel confident
- Frame positively: "We've anticipated X and prepared Y"

**Slide 15: Next Steps (今後のステップ)**
- Proposed timeline from proposal acceptance to project kickoff
- Key decisions needed from the client
- Contact information

**Appendix Slides (参考資料):**
- Detailed architecture diagrams
- Company profile
- Relevant case studies
- Team member detailed profiles

### Step 3: Design Principles for Japanese Enterprise Presentations

**Layout:**
- White or very light gray background — dark backgrounds feel informal in Japanese enterprise
- Consistent header bar with section title
- Page numbers on every slide
- Company logo in footer (small)
- Maximum 6-7 lines of text per slide

**Typography:**
- Title: 24-28pt bold
- Body: 16-20pt
- Japanese: Meiryo or Yu Gothic
- English: Calibri or Arial

**Visuals:**
- Use diagrams over text wherever possible
- Consistent color scheme (2-3 colors maximum)
- Architecture diagrams should be simple enough to explain in 60 seconds
- Avoid clip art — use clean icons or no imagery at all

**Tone:**
- Formal keigo throughout
- Client-centric: "お客様の〜" not "弊社の〜"
- Confident but not arrogant: "実現いたします" not "できます"
- Numbers and evidence over adjectives

### Step 4: Q&A Preparation (想定質問集)

Generate a Q&A preparation document with anticipated questions:

**Technical Questions:**
- "Why did you choose [Technology X] over [Technology Y]?"
- "How do you handle [specific NFR from RFP]?"
- "What's your experience with [integration point from RFP]?"

**Commercial Questions:**
- "Can you reduce the cost by X%?"
- "What if we reduce scope to Phase 1 only?"
- "What are the payment terms flexibility?"

**Delivery Questions:**
- "What if key team members leave?"
- "How do you handle scope changes?"
- "What's your escalation process?"

**Competitive Questions:**
- "How are you different from [competitor]?"
- "Why should we choose you over the incumbent?"

For each question, prepare a 30-second answer and a 2-minute detailed answer.

### Step 5: Output

Generate using the `pptx` skill:
1. Main presentation deck (.pptx)
2. Q&A preparation document (.docx) — internal document, not shared with client

## Key Principles

- **Evaluation criteria are your outline**: Structure the presentation to hit every scoring criterion in order
- **Rule of 3**: Three differentiators, three key risks, three next steps — humans remember threes
- **Show, don't tell**: A 30-second demo or architecture walkthrough beats 5 minutes of text slides
- **Rehearse timing**: Japanese presentations must end ON TIME. Running over signals poor project management
- **Anticipate the "real" question**: Behind every technical question is a trust question. Answer both
- **Client's language**: Use terminology from the RFP, not your internal jargon

For presentation format guidelines, read `references/presentation-guide.md`.
