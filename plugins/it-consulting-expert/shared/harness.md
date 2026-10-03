# The computation harness — when to write code, and the rules for it

Numbers in a Japanese SIer bid are commitments. A 一括請負 price that is off by an arithmetic slip is a
margin you cannot renegotiate. This plugin therefore never lets a model do contractual arithmetic in
prose. There are three tiers.

## Tier 1 — the engine owns every contractual number

`python3 "${CLAUDE_PLUGIN_ROOT}/sier" …` (see `shared/engine.md`): effort, cost, price, tax, budget fit,
Go/No-Go score, EVM, SLA downtime and fees, change-request gates. Versioned, unit-tested, and
`sier verify` re-derives every stored result from its saved input. **If the engine computes it, you call
the engine.** You never retype, round or "tidy" its output.

## Tier 2 — generated code for questions the engine doesn't cover

Some questions take their shape from the RFP and can't be pre-built: a Monte Carlo of schedule risk with
this client's dependencies, a data-migration volume model, sensitivity of the price to the two cost
drivers this client weights, a comparison of three vendors' offshore rates. For these, write a short
Python script instead of reasoning through numbers in prose.

### Rules — enforced by `sier derive run`

1. **Location.** The script lives in `<workspace>/_state/derived/<name>.py`. It stays there next to its
   output, so every derived number can be re-run and audited months later.
2. **Self-checks.** It contains at least one `assert` that would catch a wrong result — totals that must
   reconcile, percentiles that must be ordered, shares that must sum to 1. No assert, no run.
3. **Output.** It prints exactly one JSON object to stdout. `sier derive run` saves it as
   `<name>.out.json` with the script's SHA-256, so a later edit to the script shows as stale.
4. **No restating contractual numbers.** The output may not contain keys the engine owns
   (`price_tax_excluded`, `grand_total`, `recommended_mm`, `verdict`, `eac`, … — the full list is
   `harness.contractual_keys` in `shared/policy.json`). Read those values *from* `03-estimate.json` /
   `05-cost.json` if you need them as inputs; never re-emit them. Generated code answers new questions; it
   doesn't produce a second version of the price.
5. **Inputs from files.** Read engine artifacts and the Brief from the workspace; don't paste numbers into
   the script by hand.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/sier" derive run _state/derived/schedule_mc.py
python3 "${CLAUDE_PLUGIN_ROOT}/sier" derive list
```

### Example

```python
"""P50/P80 of phase effort under triangular uncertainty (Tier-2)."""
import json, random
random.seed(42)                                     # reproducible
est = json.load(open("03-estimate.json"))
phases = [p["mm"] for p in est["phases"]]
runs = sorted(sum(m * random.triangular(0.85, 1.6, 1.0) for m in phases) for _ in range(5000))
p50, p80 = runs[len(runs) // 2], runs[int(len(runs) * 0.8)]
assert p50 <= p80
assert abs(sum(phases) - est["totals_mm"]["base"]) < 0.01   # reconciles with the engine
print(json.dumps({"base_phase_mm": round(sum(phases), 2), "p50_phase_mm": round(p50, 2), "p80_phase_mm": round(p80, 2)}))
```

When you present a Tier-2 result, say so: "derived analysis (`_state/derived/schedule_mc.py`), not part of
the contractual estimate."

## Tier 3 — the plugin never rewrites itself at runtime

No skill or agent edits `SKILL.md` files, the engine, or `shared/policy.json` during an engagement. If a
derived script proves useful on several engagements, propose it as an engine command through a pull
request with a test — a human reviews it, and every past bid stays explainable by the version that
produced it. The same goes for policy changes (fee rates, factor bounds): change `policy.json` in the
repository, never in a workspace.
