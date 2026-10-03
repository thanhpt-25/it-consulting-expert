# Eval suite

Run from the plugin root (`plugins/it-consulting-expert`). Evals call the model with your own
credentials and count against your usage.

| Cases | What they check |
|---|---|
| `trigger-*` (18) | Each skill fires on a realistic request (JA or EN). Six collision cases also assert the sibling that shares vocabulary does **not** fire (effort ↔ cost, the four "proposal" skills ↔ create-proposal). |
| `engine-estimate-not-by-hand` | The estimate is computed by `sier estimate` and the recommended figure is right (7.13 人月). |
| `cost-over-budget-surfaced` | The price comes from `sier cost`, is right (¥13,520,000), and over-budget is reported honestly. |

```bash
# cheap smoke run (~5 cases, 1 run each, no baseline arm)
claude plugin eval . --tag smoke --runs 1 --ablation none --allow-tools Bash Write Edit --trust-plugin

# routing only
claude plugin eval . --tag trigger --runs 2

# full suite with the no-plugin baseline (the default) — most expensive
claude plugin eval . --allow-tools Bash Write Edit --threshold 0.8
```

The engine cases need `--allow-tools Bash Write Edit`; without it they cannot run `sier` and will fail.
Results land in `evals/results/` (git-ignored).
