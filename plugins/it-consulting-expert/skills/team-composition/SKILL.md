---
name: team-composition
description: >
  Propose team structures and staffing plans for IT consulting projects, grounded
  in customer RFP/RFQ from NotebookLM. Use this skill when the user asks to
  "propose a team", "plan staffing", "define team structure", "体制図を作成",
  "create an org chart", "what team do I need", "how many developers", or needs
  to determine roles, seniority mix, and resource allocation for a software,
  infrastructure, or transformation project. Also trigger for "resource plan",
  "staffing", "人員計画", "チーム構成".
---

# Team Composition Planner

Design optimal team structures for IT consulting engagements, **grounded in RFP/RFQ requirements from NotebookLM**.

## Grounding

This skill reads the engagement's RFP Brief (`00-rfp-brief.json`) and never invents client requirements. Facts carry `[RFP]` / `[RFP+]` / `[Proposed]` labels as defined in `${CLAUDE_PLUGIN_ROOT}/shared/brief-schema.md`.

## Workflow

### Step 0: Load the engagement (Brief first — NotebookLM only for gaps)

Follow the handoff contract in `${CLAUDE_PLUGIN_ROOT}/shared/engagement-workspace.md`:

1. **Find the workspace:** `python3 "${CLAUDE_PLUGIN_ROOT}/sier" status`. None → run `engagement-init` first.
   (For a one-off question with no engagement, skip the workspace and label every assumption `[Proposed]`.)
2. **Read `00-rfp-brief.json`.** If `sier status` says it is missing or **stale**, run `rfp-notebook` first —
   do not extract the RFP yourself.
3. **From the Brief this skill needs:** `team_process.staffing`, `team_process.methodology`, `timeline`, `evaluation.mandatory_qualifications` (certifications).
4. **Upstream files:** `03-estimate.json` → `roles` (recommended 人月 per role) and `02-architecture.md`.
5. **Gaps only:** `python3 "${CLAUDE_PLUGIN_ROOT}/sier" brief gaps --for team-composition`. If it reports no gaps, make
   **no** NotebookLM calls. Otherwise query only for those gaps, per `${CLAUDE_PLUGIN_ROOT}/shared/notebooklm-contract.md`
   (`--notebook <notebook_id> --json`, fallback ladder if NotebookLM is unreachable).
6. **Write back** each answer into `00-rfp-brief.json` as a labelled, cited item, remove the gap, then run
   `sier brief validate` and `sier brief render` so the next skill gets it free.

**Gap queries** — starting points when the Brief is missing one of the fields above:

```bash
notebooklm ask "What team structure, staffing requirements, or role specifications does the client define?" --json --notebook <notebook_id>
notebooklm ask "Does the client require specific certifications, clearances, or experience levels?" --json --notebook <notebook_id>
notebooklm ask "What is the expected delivery model — onsite, offshore, nearshore, or hybrid?" --json --notebook <notebook_id>
notebooklm ask "Does the client provide their own team members? What roles does the client fill vs. what the vendor must provide?" --json --notebook <notebook_id>
notebooklm ask "What is the project scope, scale, and timeline that should drive team sizing?" --json --notebook <notebook_id>
notebooklm ask "Are there any technology stack requirements that affect team skill needs?" --json --notebook <notebook_id>
```

### Step 1: Gather Additional Context from User

After extracting from the RFP, ask only for what's missing:
- **Budget constraints** affecting team size
- **Your company's available resources** and their skill profiles
- **Preferred offshore/nearshore partners** if applicable

### Step 2: Define Roles

Select roles that match the RFP's requirements. Read `references/role-catalog.md` for the full catalog.

**Core roles for most projects:**

| Role | Japanese Title | Responsibility |
|------|---------------|----------------|
| Project Manager | プロジェクトマネージャー (PM) | Overall delivery, client communication, risk management |
| Technical Lead | テクニカルリード (TL) | Architecture decisions, code quality, technical mentoring |
| Business Analyst | ビジネスアナリスト (BA) | Requirements gathering, process modeling, stakeholder alignment |
| System Engineer | システムエンジニア (SE) | Design and development |
| Programmer | プログラマー (PG) | Implementation, unit testing |
| QA Engineer | テストエンジニア (QA) | Test planning, execution, automation |
| Infrastructure Engineer | インフラエンジニア | Server, network, cloud, CI/CD setup |
| UX/UI Designer | UX/UIデザイナー | User research, wireframes, visual design |

If the RFP mandates specific roles not in this list, include them. If the RFP excludes roles you'd normally recommend, note the omission as a risk.

### Step 3: Determine Team Size

**Start from RFP constraints.** If the RFP states team size or budget, work within those bounds. Otherwise, apply these heuristics:

- Small (1-3 months, 1-2 features): 3-5 members
- Medium (3-6 months, moderate scope): 5-10 members
- Large (6-12+ months, enterprise): 10-25 members
- Enterprise program: multiple teams, 25+ with PMO

**Seniority mix guidelines:**
- Senior (7+ years): 20-30%
- Mid-level (3-7 years): 40-50%
- Junior (0-3 years): 20-30%

**Ramp-up pattern:**
- Phase 1 (requirements/design): small core — PM, TL, BA, 1-2 SE
- Phase 2 (development): full team ramp-up
- Phase 3 (testing): add QA, reduce some developers
- Phase 4 (deployment/transition): scale down to core team

### Step 4: Output Format

**Organization Chart (体制図)** — visual hierarchy using mermaid or text tree

**Staffing Table:**
| Role | Count | Seniority | Allocation (%) | Duration | Skills Required | RFP Source |
|------|-------|-----------|----------------|----------|-----------------|------------|

The **RFP Source** column is important — it traces each role back to the RFP requirement that drives it, or marks it as "Proposed" if it's your recommendation.

**Monthly Resource Histogram** — person-months per role across timeline

**Ramp-Up/Down Schedule** — when each role joins and leaves

## Key Principles

- **RFP compliance first**: If the RFP says "5 senior Java developers onsite," your plan includes exactly that — then add your recommendations on top
- **Right-size the team**: Overstaffing wastes budget; understaffing risks delays
- **Skills over headcount**: One strong senior outperforms three juniors on complex work
- **Client integration**: If the client provides team members, plan collaboration roles
- **Buffer**: Include 10-15% buffer capacity for unplanned work

For the full role catalog, read `references/role-catalog.md`.
