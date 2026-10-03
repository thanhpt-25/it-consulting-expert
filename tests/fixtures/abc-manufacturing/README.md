# Fixture: ABC Manufacturing CRM migration

The simulated engagement from `dry-run-results.md`, turned into engine inputs so its numbers
can be recomputed and regression-tested.

| File | What it reproduces |
|---|---|
| `00-rfp-brief.json` | The simulated RFP's key requirements as a schema-valid Brief |
| `go-nogo.json` | Skill 1 scoring (canonical 6-dimension rubric) |
| `estimate.json` | Skill 4: the seven phase totals (106 人月), PM 15%, and the four adjustment factors the dry run listed |
| `cost-as-dry-run.json` | Skill 5 exactly as the dry run priced it: no management fee, 6% risk premium |
| `cost-policy.json` | The same labor and non-labor priced under shared/policy.json (10% fee, 15% risk premium) |
| `sla.json` | Skill 13: availability tiers and the annual maintenance fee |

What the engine finds (asserted in `tests/test_regression_abc.py`):

- The four factors multiply to **1.20175**, not the 1.07 the dry run printed — and neither was applied to its 132 人月 total.
- Computed correctly (base 106 + PM 15.9, × 1.20175, × 1.2 recommended) the estimate is **175.79 人月**.
  The dry run's team plan of 178 人月 reconciles with that figure within 1.3% — so the team plan was right
  and the printed estimate total was the error.
- As the dry run priced it, the bid is ¥197,796,000 (6% of ¥186.6M is ¥11,196,000, not the ¥11.4M printed).
  The 6% premium is below the 15–25% fixed-price policy floor and no management fee was charged.
- Priced to policy, the bid is **¥233,250,000 — ¥33.25M (16.6%) over** the ¥200M budget.
- 15% annual maintenance on the as-priced bid is ¥29,669,400, not ¥30,000,000.
