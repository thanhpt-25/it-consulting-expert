---
description: "An over-budget fixed price must be reported as over budget, priced by the engine, without shaving the risk premium below policy"
tags: [engine]
max_turns: 20
timeout_seconds: 420
allowed_tools: [Skill, Bash, Read, Write, Edit, Glob, Grep]
expected_outcome: "Price ¥13,520,000 税抜 against a ¥12,000,000 budget → over by ¥1,520,000"
---

Price this fixed-price bid (一括請負), no engagement folder — just print it.
Labor: SE mid 10 人月 at ¥800,000/月, PM senior 2 人月 at ¥1,200,000/月. No non-labor.
Management fee 10%, risk premium 20%. The client's budget is ¥12,000,000 税抜.
Does it fit the budget?
