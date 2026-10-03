"""Effort estimation: WBS roll-up or Function Points, adjustment factors, three-point range.

Order of operations (documented so a reviewer can reproduce it by hand):
    base        = Σ WBS item days            (or FP core days + FP extra phases + any WBS items)
    pm          = base × pm_overhead
    subtotal    = base + pm
    adjusted    = subtotal × Π(adjustment factors)
    range       = adjusted × {optimistic, most_likely, pessimistic}
    recommended = adjusted × recommended multiplier          (policy; the proposal figure)
    pert_mean   = adjusted × (O + 4M + P) / 6                (shown for comparison, not used)
"""
from __future__ import annotations

from typing import Any

from common import (D, Findings, SierError, findings_md, md_table, num, pct, policy, product, q)

CONFIDENCE = ("high", "medium", "low")
LABELS = ("RFP", "Proposed", "RFP+")


def _phase_index(pol: dict) -> dict:
    idx = {}
    for p in pol["phases"]:
        idx[p["id"]] = p
        idx[p["ja"]] = p
        idx[p["en"].lower()] = p
    return idx


def _fp(fp: dict, pol: dict, f: Findings) -> dict:
    fpp = pol["function_points"]
    weights = fpp["weights"]
    counts = fp.get("counts") or {}
    ufp = D(0)
    rows = []
    for ftype, levels in counts.items():
        if ftype not in weights:
            f.error(f"fp.counts: unknown function type {ftype!r} (expected {', '.join(weights)})")
            continue
        for level, n in (levels or {}).items():
            if level not in weights[ftype]:
                f.error(f"fp.counts.{ftype}: unknown complexity {level!r} (expected low/avg/high)")
                continue
            n = D(n)
            if n < 0:
                f.error(f"fp.counts.{ftype}.{level}: negative count")
                continue
            w = D(weights[ftype][level])
            ufp += n * w
            if n:
                rows.append({"type": ftype, "complexity": level, "count": n, "weight": w, "fp": n * w})
    vcfg = fpp["vaf"]
    if "gsc" in fp:
        gsc = fp["gsc"]
        if not isinstance(gsc, list) or len(gsc) != vcfg["gsc_count"]:
            f.error(f"fp.gsc must be a list of {vcfg['gsc_count']} ratings")
            gsc = [0] * vcfg["gsc_count"]
        for i, g in enumerate(gsc):
            if not (0 <= D(g) <= vcfg["gsc_max"]):
                f.error(f"fp.gsc[{i}] must be 0–{vcfg['gsc_max']}")
        tdi = sum(D(g) for g in gsc)
        vaf = D(vcfg["base"]) + D(vcfg["per_point"]) * tdi
    elif "vaf" in fp:
        vaf, tdi = D(fp["vaf"]), None
        lo = D(vcfg["base"])
        hi = lo + D(vcfg["per_point"]) * vcfg["gsc_count"] * vcfg["gsc_max"]
        if not (lo <= vaf <= hi):
            f.error(f"fp.vaf {vaf} is outside the possible range {lo}–{hi}")
    else:
        vaf, tdi = D(1), None
        f.warn("fp: no gsc or vaf given — using VAF 1.00 (unadjusted)")
    if "hours_per_fp" not in fp:
        f.error("fp.hours_per_fp is required (see effort-estimation/references/function-point-guide.md)")
        hpf = D(0)
    else:
        hpf = D(fp["hours_per_fp"])
    afp = ufp * vaf
    hours = afp * hpf
    core_days = hours / D(pol["hours_per_day"])
    shares = fp.get("extra_phase_shares", fpp["extra_phase_shares"])
    extra = {k: core_days * D(v) for k, v in shares.items()}
    return {"rows": rows, "ufp": ufp, "tdi": tdi, "vaf": vaf, "afp": afp, "hours_per_fp": hpf,
            "core_hours": hours, "core_days": core_days, "extra_phase_days": extra}


def compute(inp: dict, calibration: dict | None = None) -> dict:
    pol = policy()["estimation"]
    tp = pol["three_point"]
    f = Findings()
    method = inp.get("method", "wbs")
    if method not in ("wbs", "fp"):
        raise SierError("method must be 'wbs' or 'fp'")
    days_per_mm = D(inp.get("days_per_mm", pol["days_per_mm"]))
    pm_overhead = D(inp.get("pm_overhead", pol["pm_overhead"]["default"]))
    lo, hi = (D(x) for x in pol["pm_overhead"]["range"])
    if not (lo <= pm_overhead <= hi):
        f.warn(f"pm_overhead {pct(pm_overhead)} is outside the policy range {pct(lo)}–{pct(hi)}")

    # -- adjustment factors
    factors = inp.get("factors") or {}
    fdefs = {k: v for k, v in pol["factors"].items() if not k.startswith("_")}
    for name, val in factors.items():
        if name not in fdefs:
            f.error(f"factors: unknown factor {name!r} (known: {', '.join(fdefs)})")
            continue
        v = D(val)
        b0, b1 = (D(x) for x in fdefs[name]["bounds"])
        if v != 1 and not (b0 <= v <= b1):
            f.error(f"factors.{name} = {v} is outside its bounds {b0}–{b1}")
    factor_product = product(factors.values()) if factors else D(1)

    # -- WBS items
    pidx = _phase_index(pol)
    items = inp.get("items") or []
    seen, phase_days, role_days, conf_days = set(), {}, {}, {c: D(0) for c in CONFIDENCE}
    untraced, proposed, oversized = [], 0, []
    max_task = D(pol["max_task_days"])
    item_rows = []
    for i, it in enumerate(items):
        where = f"items[{i}]"
        iid = it.get("id")
        if not iid:
            f.error(f"{where}: missing id")
        elif iid in seen:
            f.error(f"{where}: duplicate id {iid}")
        seen.add(iid)
        try:
            days = D(it.get("days"))
        except SierError:
            f.error(f"{where} ({iid}): days must be a number")
            continue
        if days <= 0:
            f.error(f"{where} ({iid}): days must be positive")
            continue
        ph = pidx.get(str(it.get("phase", "")).strip()) or pidx.get(str(it.get("phase", "")).strip().lower())
        if not ph:
            f.error(f"{where} ({iid}): unknown phase {it.get('phase')!r}")
            continue
        role = it.get("role") or "UNASSIGNED"
        if role == "UNASSIGNED":
            f.warn(f"{where} ({iid}): no role — cost reconciliation will not be able to price it")
        conf = it.get("confidence", "medium")
        if conf not in CONFIDENCE:
            f.error(f"{where} ({iid}): confidence must be high/medium/low")
            conf = "medium"
        label = it.get("label", "RFP")
        if label not in LABELS:
            f.error(f"{where} ({iid}): label must be RFP / Proposed / RFP+")
        if label == "Proposed":
            proposed += 1
        elif not it.get("req"):
            untraced.append(iid)
        if days > max_task:
            oversized.append(iid)
        phase_days[ph["id"]] = phase_days.get(ph["id"], D(0)) + days
        role_days[role] = role_days.get(role, D(0)) + days
        conf_days[conf] += days
        item_rows.append({"id": iid, "req": it.get("req"), "phase": ph["id"], "task": it.get("task", ""),
                          "days": days, "role": role, "confidence": conf, "label": label})
    if untraced:
        f.warn(f"{len(untraced)} item(s) labelled RFP/RFP+ have no RFP requirement id: {', '.join(untraced[:10])}"
               + (" …" if len(untraced) > 10 else "") + " — trace them or label them Proposed")
    if oversized:
        f.warn(f"{len(oversized)} task(s) exceed {max_task} man-days and should be split: {', '.join(oversized[:10])}")

    # -- FP core
    fp_result = None
    if method == "fp":
        if not inp.get("fp"):
            raise SierError("method 'fp' needs an 'fp' block with counts and hours_per_fp")
        fp_result = _fp(inp["fp"], pol, f)
        phase_days["fp_core"] = phase_days.get("fp_core", D(0)) + fp_result["core_days"]
        for k, v in fp_result["extra_phase_days"].items():
            phase_days[k] = phase_days.get(k, D(0)) + v
        if "deployment" not in phase_days:
            f.warn("FP covers design, build and unit test only; no 移行・リリース (deployment) effort is included — add WBS items for it")
    elif not items:
        raise SierError("method 'wbs' needs at least one item")

    f.raise_if_errors("Estimate")

    base = sum(phase_days.values(), D(0))
    if base <= 0:
        raise SierError("Total base effort is zero")
    pm_days = base * pm_overhead
    subtotal = base + pm_days
    adjusted = subtotal * factor_product
    rec_mult = D(tp["recommended"])
    cal = None
    if calibration and calibration.get("n"):
        cal = dict(calibration)
        cal["applied"] = bool(inp.get("apply_calibration"))
        if cal["applied"]:
            rec_mult *= D(cal["factor"])
    totals_days = {
        "base": base, "pm": pm_days, "subtotal": subtotal, "adjusted": adjusted,
        "optimistic": adjusted * D(tp["optimistic"]),
        "most_likely": adjusted * D(tp["most_likely"]),
        "pessimistic": adjusted * D(tp["pessimistic"]),
        "pert_mean": adjusted * (D(tp["optimistic"]) + 4 * D(tp["most_likely"]) + D(tp["pessimistic"])) / 6,
        "recommended": adjusted * rec_mult,
    }
    if cal:
        totals_days["calibrated_recommended"] = adjusted * D(tp["recommended"]) * D(cal["factor"])

    # -- phase distribution check (WBS only; FP has its own split)
    phases = []
    pdefs = {p["id"]: p for p in pol["phases"]}
    for pid, days in phase_days.items():
        share = days / base
        pdef = pdefs.get(pid)
        rng = pdef["range"] if pdef else None
        in_range = None
        if rng and method == "wbs":
            in_range = D(rng[0]) <= share <= D(rng[1])
            if not in_range:
                f.warn(f"phase {pdef['ja']} is {pct(share)} of base effort; typical range is {pct(rng[0])}–{pct(rng[1])}")
        phases.append({"id": pid, "ja": pdef["ja"] if pdef else "設計・製造・単体テスト (FP)",
                       "days": days, "mm": days / days_per_mm, "share": share, "range": rng, "in_range": in_range})
    order = {p["id"]: i for i, p in enumerate(pol["phases"])}
    order["fp_core"] = 1.5
    phases.sort(key=lambda p: order.get(p["id"], 99))
    if method == "wbs":
        for p in pol["phases"]:
            if p["id"] not in phase_days:
                f.warn(f"no effort in phase {p['ja']} — is it really out of scope?")

    # -- role allocation of the recommended figure (feeds cost reconciliation)
    roles = []
    role_days_all = dict(role_days)
    role_days_all["PM"] = role_days_all.get("PM", D(0)) + pm_days
    if method == "fp":
        role_days_all["UNALLOCATED (FP)"] = fp_result["core_days"] + sum(fp_result["extra_phase_days"].values(), D(0))
    for role, days in sorted(role_days_all.items(), key=lambda kv: -kv[1]):
        share = days / subtotal
        roles.append({"role": role, "base_days": days, "share": share,
                      "recommended_mm": totals_days["recommended"] * share / days_per_mm})

    result = {
        "kind": "estimate",
        "method": method,
        "project_type": inp.get("project_type"),
        "params": {"days_per_mm": days_per_mm, "pm_overhead": pm_overhead, "factors": factors,
                   "factor_product": factor_product, "three_point": tp},
        "phases": phases,
        "roles": roles,
        "items": item_rows,
        "fp": fp_result,
        "totals_days": totals_days,
        "totals_mm": {k: v / days_per_mm for k, v in totals_days.items()},
        "recommended_mm": totals_days["recommended"] / days_per_mm,
        "recommended_days": totals_days["recommended"],
        "traceability": {"items": len(item_rows), "traced": len(item_rows) - len(untraced) - proposed,
                         "proposed": proposed, "untraced": untraced},
        "confidence_days": conf_days,
        "calibration": cal,
        "findings": f.as_dict(),
    }
    return _rounded(result)


def _rounded(obj: Any) -> Any:
    """Round Decimals for storage: 4 dp keeps verify comparisons stable without float noise."""
    if isinstance(obj, dict):
        return {k: _rounded(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_rounded(v) for v in obj]
    if isinstance(obj, type(D(0))):
        return q(obj, 4)
    return obj


def render(r: dict) -> str:
    t, m = r["totals_days"], r["totals_mm"]
    p = r["params"]
    out = [f"# Effort Estimate (工数見積) — method: {r['method'].upper()}", "",
           "> Computed by `sier estimate`. Do not edit numbers here; edit `inputs/estimate.json` and re-run.", ""]
    if r.get("fp"):
        fp = r["fp"]
        out += ["## Function Points", "",
                md_table(["Type", "Complexity", "Count", "Weight", "FP"],
                         [[x["type"], x["complexity"], num(x["count"], 0), num(x["weight"], 0), num(x["fp"], 0)]
                          for x in fp["rows"]], "llrrr"), "",
                md_table(["Metric", "Value"], [
                    ["Unadjusted FP (UFP)", num(fp["ufp"], 0)],
                    ["Total degree of influence (TDI)", num(fp["tdi"], 0) if fp["tdi"] is not None else "—"],
                    ["Value adjustment factor (VAF)", num(fp["vaf"], 2)],
                    ["Adjusted FP (AFP)", num(fp["afp"], 2)],
                    ["Hours per FP", num(fp["hours_per_fp"], 1)],
                    ["Core effort (design + build + UT)", f"{num(fp['core_hours'], 0)} h = {num(fp['core_days'], 1)} 人日"],
                ], "lr"), ""]
    out += ["## Effort by phase (フェーズ別工数)", "",
            md_table(["Phase", "人日", "人月", "Share", "Typical range"],
                     [[ph["ja"], num(ph["days"], 1), num(ph["mm"], 2), pct(ph["share"]),
                       (f"{pct(ph['range'][0], 0)}–{pct(ph['range'][1], 0)}" + ("" if ph["in_range"] in (None, True) else " ⚠️"))
                       if ph["range"] else "—"] for ph in r["phases"]], "lrrrl"), "",
            "## Roll-up (積算)", "",
            md_table(["Step", "人日", "人月", "How"], [
                ["Base", num(t["base"], 1), num(m["base"], 2), "Σ items" + (" + FP" if r.get("fp") else "")],
                [f"PM overhead ({pct(p['pm_overhead'])})", num(t["pm"], 1), num(m["pm"], 2), "base × overhead"],
                ["Subtotal", num(t["subtotal"], 1), num(m["subtotal"], 2), "base + PM"],
                [f"Adjusted (× {num(p['factor_product'], 4)})", num(t["adjusted"], 1), num(m["adjusted"], 2), "subtotal × Π factors"],
            ], "lrrl"), ""]
    if p["factors"]:
        out += ["### Adjustment factors (調整係数)", "",
                md_table(["Factor", "Multiplier"], [[k, num(v, 2)] for k, v in p["factors"].items()]
                         + [["**Combined (product)**", f"**{num(p['factor_product'], 4)}**"]], "lr"), ""]
    tp = p["three_point"]
    out += ["## Range (三点見積)", "",
            md_table(["Scenario", "Multiplier", "人日", "人月"], [
                ["Optimistic (楽観)", f"× {tp['optimistic']}", num(t["optimistic"], 1), num(m["optimistic"], 2)],
                ["Most likely (最頻)", f"× {tp['most_likely']}", num(t["most_likely"], 1), num(m["most_likely"], 2)],
                ["Pessimistic (悲観)", f"× {tp['pessimistic']}", num(t["pessimistic"], 1), num(m["pessimistic"], 2)],
                ["PERT mean (for comparison)", "(O+4M+P)/6", num(t["pert_mean"], 1), num(m["pert_mean"], 2)],
                ["**Recommended for the proposal**", f"× {tp['recommended']}"
                 + (" × calibration" if (r.get("calibration") or {}).get("applied") else ""),
                 f"**{num(t['recommended'], 1)}**", f"**{num(m['recommended'], 2)}**"],
            ], "lrrr"), ""]
    cal = r.get("calibration")
    if cal:
        out += [f"> **Your track record:** {cal['n']} closed `{cal.get('project_type')}` project(s) ran a median "
                f"**× {num(cal['factor'], 2)}** of their initial estimate. Calibrated recommendation: "
                f"**{num(m['calibrated_recommended'], 2)} 人月** "
                + ("(applied above)." if cal["applied"] else "(shown for information; set `apply_calibration: true` to use it)."), ""]
    if r["roles"]:
        out += ["## Allocation by role (ロール別配分 — feeds cost reconciliation)", "",
                md_table(["Role", "Base 人日", "Share", "Recommended 人月"],
                         [[x["role"], num(x["base_days"], 1), pct(x["share"]), num(x["recommended_mm"], 2)]
                          for x in r["roles"]], "lrrr"), ""]
    tr = r["traceability"]
    cd = r["confidence_days"]
    out += ["## Traceability & confidence (トレーサビリティ・確度)", "",
            f"- WBS items: {tr['items']} — traced to an RFP requirement: {tr['traced']}, "
            f"labelled Proposed: {tr['proposed']}, untraced: {len(tr['untraced'])}",
            f"- Effort by confidence: high {num(cd['high'], 1)} / medium {num(cd['medium'], 1)} / low {num(cd['low'], 1)} 人日",
            "", "## Findings", "", findings_md(r["findings"]), ""]
    return "\n".join(out)
