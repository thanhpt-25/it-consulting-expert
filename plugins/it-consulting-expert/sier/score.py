"""Go/No-Go scoring against the canonical rubric in shared/policy.json."""
from __future__ import annotations

from common import D, Findings, SierError, findings_md, md_table, num, pct, policy


def compute(inp: dict) -> dict:
    rub = policy()["rubric"]
    f = Findings()
    dims = rub["dimensions"]
    total_w = sum(D(d["weight"]) for d in dims)
    if total_w != 1:
        raise SierError(f"policy rubric weights sum to {total_w}, not 1.0 — fix shared/policy.json")
    scores = inp.get("scores") or {}
    known = {d["id"] for d in dims}
    for k in scores:
        if k not in known:
            f.error(f"scores: unknown dimension {k!r} (expected {', '.join(sorted(known))})")
    rows, total = [], D(0)
    lo, hi = rub["scale"]["min"], rub["scale"]["max"]
    rationale = inp.get("rationale") or {}
    for d in dims:
        if d["id"] not in scores:
            f.error(f"scores: missing dimension {d['id']} ({d['ja']})")
            continue
        s = D(scores[d["id"]])
        if not (lo <= s <= hi):
            f.error(f"scores.{d['id']} = {s} is outside {lo}–{hi}")
            continue
        w = D(d["weight"])
        total += s * w
        rows.append({"id": d["id"], "en": d["en"], "ja": d["ja"], "score": s, "weight": w, "weighted": s * w,
                     "rationale": rationale.get(d["id"], "")})
        if not rationale.get(d["id"]):
            f.warn(f"no rationale given for {d['en']} — a score without a reason cannot be defended at the bid meeting")
    f.raise_if_errors("Score")

    verdict = next(t for t in sorted(rub["thresholds"], key=lambda t: -t["min"]) if total >= D(t["min"]))
    gate_failures = []
    for i, m in enumerate(inp.get("mandatory") or []):
        met = m.get("met")
        if met not in (True, False, "workaround"):
            raise SierError(f"mandatory[{i}].met must be true, false or \"workaround\"")
        if met is False:
            gate_failures.append(m.get("requirement", f"#{i + 1}"))
        if met == "workaround" and not m.get("evidence"):
            f.warn(f"mandatory requirement {m.get('requirement')!r} relies on a workaround with no evidence recorded")
    final = verdict
    if gate_failures:
        final = next(t for t in rub["thresholds"] if t["verdict"] == "DEFINITE_NO_GO")
        f.warn(f"mandatory gate failed ({', '.join(gate_failures)}) — verdict forced to DEFINITE_NO_GO "
               f"regardless of the {num(total, 2)} score")
    return {"kind": "go_nogo", "rows": rows, "weighted_score": total, "score_verdict": verdict["verdict"],
            "verdict": final["verdict"], "verdict_ja": final["ja"], "action": final["action"],
            "mandatory": inp.get("mandatory") or [], "gate_failures": gate_failures,
            "conditions": inp.get("conditions") or [], "findings": f.as_dict()}


def render(r: dict) -> str:
    rows = [[f"{x['en']} ({x['ja']})", num(x["score"], 0), pct(x["weight"], 0), num(x["weighted"], 2), x["rationale"]]
            for x in r["rows"]]
    rows.append(["**Total**", "", "**100%**", f"**{num(r['weighted_score'], 2)} / 5.00**", ""])
    out = ["# Go/No-Go Assessment (案件評価)", "",
           f"## Verdict: **{r['verdict']}** ({r['verdict_ja']})", "", r["action"], "",
           "> Computed by `sier score` against the rubric in shared/policy.json.", "",
           md_table(["Dimension", "Score", "Weight", "Weighted", "Rationale"], rows, "lrrrl"), ""]
    if r["mandatory"]:
        icon = {True: "✅ met", False: "❌ NOT met", "workaround": "⚠️ workaround"}
        out += ["## Mandatory qualifications (必須要件)", "",
                md_table(["Requirement", "Status", "Evidence / gap"],
                         [[m.get("requirement"), icon[m.get("met")], m.get("evidence", "")] for m in r["mandatory"]]), ""]
    if r["conditions"]:
        out += ["## Conditions for GO", ""] + [f"{i + 1}. {c}" for i, c in enumerate(r["conditions"])] + [""]
    out += ["## Findings", "", findings_md(r["findings"]), ""]
    return "\n".join(out)
