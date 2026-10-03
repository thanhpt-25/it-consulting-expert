"""Maintenance & SLA arithmetic: allowed downtime, annual fee, multi-year totals, service credits."""
from __future__ import annotations

from common import D, Findings, SierError, findings_md, md_table, num, pct, policy, round_yen, yen


def window_hours(window: str, pol: dict) -> D:
    if window == "24x7":
        return D(pol["month_hours_24x7"])
    if window == "business_hours":
        return D(pol["business_hours_per_day"]) * D(pol["business_days_per_month"])
    raise SierError(f"unknown measurement window {window!r} (use 24x7 or business_hours)")


def compute(inp: dict) -> dict:
    pol = policy()["maintenance"]
    com = policy()["commercial"]
    f = Findings()
    tiers = inp.get("availability_tiers") or pol["availability_tiers"]
    avail = []
    for t in tiers:
        target = D(t["target"])
        if not (0 < target < 100):
            raise SierError(f"availability target {target} must be a percentage between 0 and 100")
        hours = window_hours(t.get("window", "24x7"), pol)
        down_h = hours * (100 - target) / 100
        avail.append({"id": t.get("id"), "target": target, "window": t.get("window", "24x7"),
                      "window_hours_per_month": hours, "allowed_downtime_minutes_per_month": down_h * 60,
                      "allowed_downtime_hours_per_month": down_h})
        claimed = t.get("claimed_downtime_minutes")
        if claimed is not None and abs(D(claimed) - down_h * 60) > D(1):
            f.warn(f"{t.get('id')}: document claims ~{num(claimed, 0)} min/month allowed downtime, "
                   f"but {target}% over a {t.get('window')} window ({num(hours, 0)} h) allows {num(down_h * 60, 1)} min")

    fee = None
    if inp.get("project_cost") is not None:
        pc = D(inp["project_cost"])
        lo, hi = (D(x) for x in com["maintenance_rate"]["range"])
        rate = D(inp.get("maintenance_rate", com["maintenance_rate"]["default"]))
        if not (lo <= rate <= hi):
            f.warn(f"maintenance rate {pct(rate)} is outside the guideline {pct(lo)}–{pct(hi)} of project cost")
        annual = pc * rate
        uplift = D(0)
        if inp.get("support_24x7"):
            ulo, uhi = (D(x) for x in pol["uplift_24x7"]["range"])
            uplift = D(inp.get("uplift_24x7", ulo))
            if not (ulo <= uplift <= uhi):
                f.warn(f"24/7 uplift {pct(uplift)} is outside the guideline {pct(ulo)}–{pct(uhi)}")
        annual_total = round_yen(annual * (1 + uplift))
        years = int(inp.get("contract_years", 1))
        disc = D(pol["multi_year_discount"].get(str(years), 0))
        contract_total = round_yen(D(annual_total) * years * (1 - disc))
        fee = {"project_cost": pc, "rate": rate, "annual_base": round_yen(annual), "uplift_24x7": uplift,
               "annual_total": annual_total, "monthly": round_yen(D(annual_total) / 12), "contract_years": years,
               "multi_year_discount": disc, "contract_total": contract_total,
               "range_annual": [round_yen(pc * lo), round_yen(pc * hi)]}

    credits = None
    if inp.get("credits"):
        c = inp["credits"]
        measured = D(c["measured_availability"])
        monthly_fee = D(c.get("monthly_fee", fee["monthly"] if fee else 0))
        applicable = [t for t in sorted(c["tiers"], key=lambda t: D(t["below"])) if measured < D(t["below"])]
        credit_pct = D(applicable[0]["credit_pct"]) if applicable else D(0)
        credits = {"measured": measured, "monthly_fee": monthly_fee, "credit_pct": credit_pct,
                   "credit_amount": round_yen(monthly_fee * credit_pct / 100)}
    return {"kind": "sla", "availability": avail, "fee": fee, "credits": credits, "findings": f.as_dict()}


def render(r: dict) -> str:
    out = ["# Maintenance & SLA (保守・SLA)", "",
           "> Computed by `sier sla`. Policy from shared/policy.json (maintenance, commercial.maintenance_rate).", "",
           "## Availability (可用性)", "",
           md_table(["Tier", "Target", "Window", "Hours/month", "Allowed downtime/month"],
                    [[a["id"], f"{a['target']}%", a["window"].replace("_", " "), num(a["window_hours_per_month"], 0),
                      f"{num(a['allowed_downtime_minutes_per_month'], 1)} min ({num(a['allowed_downtime_hours_per_month'], 2)} h)"]
                     for a in r["availability"]], "lrlrr"), ""]
    fee = r.get("fee")
    if fee:
        rows = [["Project cost", yen(fee["project_cost"])],
                [f"Annual base ({pct(fee['rate'])})", yen(fee["annual_base"])],
                ["Guideline range (annual)", f"{yen(fee['range_annual'][0])} – {yen(fee['range_annual'][1])}"]]
        if fee["uplift_24x7"]:
            rows.append([f"24/7 uplift (+{pct(fee['uplift_24x7'])})", ""])
        rows += [["**Annual fee**", f"**{yen(fee['annual_total'])}**"], ["Monthly", yen(fee["monthly"])],
                 [f"Contract total ({fee['contract_years']} yr, −{pct(fee['multi_year_discount'], 0)})",
                  f"**{yen(fee['contract_total'])}**"]]
        out += ["## Fee (保守費用)", "", md_table(["Item", "Amount"], rows, "lr"), ""]
    c = r.get("credits")
    if c:
        out += ["## Service credit (サービスクレジット)", "",
                f"Measured {c['measured']}% → credit {num(c['credit_pct'], 0)}% of {yen(c['monthly_fee'])} = **{yen(c['credit_amount'])}**", ""]
    out += ["## Findings", "", findings_md(r["findings"]), ""]
    return "\n".join(out)
