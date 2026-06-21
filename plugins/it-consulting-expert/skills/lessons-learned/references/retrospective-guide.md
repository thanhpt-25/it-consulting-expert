# Retrospective Facilitation Guide (振り返り実施ガイド)

## Session Planning

### Recommended Format

| Project Size | Duration | Participants | Format |
|-------------|----------|-------------|--------|
| Small (< 5人月) | 2 hours | Full team | Single session |
| Medium (5-30人月) | Half day | Full team + key stakeholders | Single session + follow-up |
| Large (30-100人月) | Full day | Team leads → then all-hands | Two-tier: leads first, then full team |
| Very Large (100人月+) | 2 days | Sub-team sessions → combined | Multiple sessions with synthesis |

### Preparation Checklist

- [ ] Schedule 1-2 weeks after go-live (not during crunch)
- [ ] Book room with whiteboard/post-its (or virtual equivalent)
- [ ] Distribute pre-work questionnaire 3 days before
- [ ] Prepare planned vs. actual data (effort, schedule, cost, quality)
- [ ] Gather change request log
- [ ] Compile defect statistics
- [ ] Collect client feedback (formal and informal)
- [ ] Invite ALL participants — including subcontractors
- [ ] Assign a facilitator (ideally NOT the PM — they're too close)

### Pre-Work Questionnaire

Send to all participants before the session:

```
【振り返り事前アンケート】

プロジェクト名: ___________
回答者: ___________

1. このプロジェクトで最もうまくいったことは何ですか？(2-3個)

2. 最も困難だったことは何ですか？(2-3個)

3. 次の同様のプロジェクトで変えたいことは何ですか？(2-3個)

4. 見積の精度について、どの工程が最もずれましたか？
   なぜだと思いますか？

5. クライアントとのコミュニケーションで改善すべき点はありましたか？

6. ツールやプロセスで不足していたものはありますか？

7. その他、共有したいことがあれば自由に記述してください。
```

## Facilitation Techniques

### KPT Session Flow (3 hours)

**1. Opening (15 min)**
- Ground rules: blameless, constructive, specific
- Review project overview and key metrics
- Set expectations: "We're here to learn, not to blame"

**2. Individual Reflection (15 min)**
- Silent writing: each person writes Keep/Problem/Try on sticky notes
- One idea per note, as specific as possible

**3. Keep — Sharing (30 min)**
- Round robin: each person shares their Keep items
- Group similar items
- Vote on top 3-5 to formalize as best practices

**4. Problem — Sharing (45 min)**
- Round robin: each person shares their Problem items
- Group by theme
- For top problems: use "5 Whys" to find root cause
- Vote on top 5-7 most impactful problems

**5. Break (15 min)**

**6. Try — Solution Generation (45 min)**
- For each top Problem, brainstorm concrete Try items
- Each Try must have: action, owner, timeline, and "applies to" scope
- Vote on top 5-10 Try items to commit to

**7. Action Planning (15 min)**
- Assign owners and deadlines
- Decide tracking mechanism
- Schedule follow-up check (30 days)

**8. Closing (10 min)**
- Thank participants
- Preview next steps
- Positive ending: "What are you most proud of from this project?"

### 5 Whys Technique for Root Cause Analysis

Example:
- **Problem**: Integration testing took 3 weeks longer than planned
- **Why 1?** Many integration defects were found late
- **Why 2?** Interface specifications were ambiguous
- **Why 3?** External system specifications weren't available during design phase
- **Why 4?** We didn't request them early enough from the client
- **Why 5?** Our kickoff checklist doesn't include "request all external system specifications"
- **Root Cause**: Incomplete kickoff checklist
- **Action**: Add "external system specification request" to project kickoff checklist

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Blame game | People stop sharing | Enforce blameless rule, focus on process |
| PM dominates | Other voices suppressed | Use neutral facilitator |
| Too general | "Communication was bad" — not actionable | Push for specifics: who, what, when, impact |
| No follow-up | Actions never tracked | Schedule 30-day check, assign owners |
| Only negatives | Demoralizing, misses best practices | Start with Keep, celebrate wins |
| Skipping it | "Too busy" — lessons lost | Make it mandatory, block calendar in advance |
| Too late | Memories faded after 2+ months | Schedule during project planning, not after |

## Estimation Calibration Framework

Use historical data to improve future estimates:

### Tracking Sheet

| Project | Type | Est. Effort | Actual Effort | Ratio | Notes |
|---------|------|------------|---------------|-------|-------|
| Project A | Web app, medium | 30人月 | 38人月 | 1.27 | Scope creep in testing |
| Project B | Migration, large | 50人月 | 45人月 | 0.90 | Over-estimated data migration |
| Project C | API integration | 15人月 | 22人月 | 1.47 | External system delays |

### Calibration Factor by Project Type

After 5+ projects of each type, calculate average ratio:

| Project Type | Avg Ratio | Recommended Buffer |
|-------------|-----------|-------------------|
| New web application | 1.25 | +25% over base estimate |
| System migration | 1.15 | +15% |
| API/Integration | 1.35 | +35% |
| Infrastructure | 1.10 | +10% |

Apply these as organizational adjustment factors in the `effort-estimation` skill.

## Integration with Other Skills

- **create-proposal**: Original baseline data comes from the proposal
- **effort-estimation**: Calibration data feeds back into estimation accuracy
- **progress-report**: Cumulative project data provides the actual metrics
- **change-request**: CR log shows scope evolution over the project
- **vendor-management**: Subcontractor performance data feeds into vendor scorecard
