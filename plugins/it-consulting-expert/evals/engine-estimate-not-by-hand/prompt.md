---
description: "Effort arithmetic must be done by the sier engine, and the recommended figure must be correct"
tags: [engine, smoke]
max_turns: 20
timeout_seconds: 420
allowed_tools: [Skill, Bash, Read, Write, Edit, Glob, Grep]
expected_outcome: "Recommended effort 7.13 人月 (100 人日 base, 10% PM, factors 1.2 × 0.9, × 1.2 recommended, 20 人日/人月)"
---

Quick effort estimate please, no engagement folder needed — just print the result.
WBS: one implementation task W-001 for requirement FR-001, 100 人日, role SE, confidence high.
PM overhead 10%. Factors: technical_complexity 1.2, team_experience 0.9.
What is the recommended 人月 figure for the proposal?
