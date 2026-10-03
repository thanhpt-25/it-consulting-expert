"""Firm-wide data shared across engagements: the rate card and the estimation calibration record.

Both live in <root>/_firm/ next to the engagements, so they travel with the consultant's files
and survive plugin updates.
"""
from __future__ import annotations

from pathlib import Path
from statistics import mean, median

from common import D, SierError, dump_json, load_json, md_table, num, today

RATE_CARD = "rate-card.json"
CALIBRATION = "calibration.json"

# Midpoints of the Japanese market bands in cost-estimation/references/rate-cards.md (monthly, JPY).
# Marked benchmark_only so `sier cost` warns until the firm replaces them with its own rates.
BENCHMARK_RATES = {
    "PM":     {"senior": 1350000, "expert": 2000000},
    "TL":     {"senior": 1150000, "expert": 1550000},
    "BA":     {"mid": 800000, "senior": 1050000, "expert": 1350000},
    "SE":     {"junior": 575000, "mid": 750000, "senior": 975000, "expert": 1250000},
    "PG":     {"junior": 475000, "mid": 625000, "senior": 800000},
    "QA":     {"junior": 475000, "mid": 650000, "senior": 875000},
    "INFRA":  {"junior": 600000, "mid": 825000, "senior": 1125000, "expert": 1450000},
    "DEVOPS": {"mid": 800000, "senior": 1050000, "expert": 1350000},
    "SEC":    {"mid": 900000, "senior": 1200000, "expert": 1600000},
    "UX":     {"junior": 525000, "mid": 700000, "senior": 950000},
    "AIML":   {"mid": 900000, "senior": 1200000, "expert": 1700000},
    "DBA":    {"mid": 800000, "senior": 1050000, "expert": 1350000},
    "SM":     {"mid": 800000, "senior": 1000000},
}


def ratecard_init(firm: Path, force: bool = False) -> Path:
    p = firm / RATE_CARD
    if p.exists() and not force:
        raise SierError(f"{p} already exists — edit it, or pass --force to overwrite it with benchmarks")
    dump_json({
        "currency": "JPY", "unit": "monthly",
        "source": "Market benchmark midpoints (rate-cards.md) — REPLACE WITH YOUR FIRM'S RATES",
        "benchmark_only": True, "updated": today().isoformat(), "rates": BENCHMARK_RATES,
    }, p)
    return p


def ratecard_load(firm: Path) -> dict | None:
    p = firm / RATE_CARD
    return load_json(p) if p.exists() else None


def calibration_load(firm: Path) -> dict:
    p = firm / CALIBRATION
    return load_json(p) if p.exists() else {"records": []}


def calibration_add(firm: Path, rec: dict) -> dict:
    for k in ("project", "project_type", "estimated_mm", "actual_mm"):
        if rec.get(k) in (None, ""):
            raise SierError(f"calibration record needs {k}")
    if D(rec["estimated_mm"]) <= 0 or D(rec["actual_mm"]) <= 0:
        raise SierError("estimated_mm and actual_mm must be positive")
    data = calibration_load(firm)
    data["records"] = [r for r in data["records"] if r.get("project") != rec["project"]] + [rec]
    dump_json(data, firm / CALIBRATION)
    return data


def calibration_factor(firm: Path, project_type: str | None) -> dict | None:
    """Median actual/estimated effort ratio for a project type. None when there is no history."""
    if not project_type:
        return None
    recs = [r for r in calibration_load(firm)["records"] if r.get("project_type") == project_type]
    if not recs:
        return None
    ratios = [float(D(r["actual_mm"]) / D(r["estimated_mm"])) for r in recs]
    return {"project_type": project_type, "n": len(recs), "factor": round(median(ratios), 4),
            "mean": round(mean(ratios), 4), "ratios": [round(x, 4) for x in ratios],
            "projects": [r["project"] for r in recs]}


def calibration_render(firm: Path) -> str:
    data = calibration_load(firm)
    if not data["records"]:
        return "No calibration records yet. `lessons-learned` adds one per closed project."
    types = sorted({r["project_type"] for r in data["records"]})
    rows = []
    for t in types:
        c = calibration_factor(firm, t)
        rows.append([t, c["n"], f"× {num(c['factor'], 2)}", f"× {num(c['mean'], 2)}", ", ".join(c["projects"])])
    detail = [[r["project"], r["project_type"], num(r["estimated_mm"], 1), num(r["actual_mm"], 1),
               f"× {num(D(r['actual_mm']) / D(r['estimated_mm']), 2)}"] for r in data["records"]]
    return "\n".join(["# Estimation calibration (見積精度の実績)", "",
                      md_table(["Project type", "n", "Median actual/estimate", "Mean", "Projects"], rows, "lrrrl"), "",
                      md_table(["Project", "Type", "Estimated 人月", "Actual 人月", "Ratio"], detail, "llrrr"), ""])
