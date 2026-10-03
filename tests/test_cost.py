import unittest
from decimal import Decimal as Dec

import _helpers  # noqa: F401
import cost
from common import SierError

CARD = {"source": "test", "rates": {"SE": {"mid": 800000}, "PM": {"senior": 1200000}}}


def base(**kw):
    return {"labor": [{"role": "SE", "seniority": "mid", "mm": 10}, {"role": "PM", "seniority": "senior", "mm": 2}],
            **kw}


class Pricing(unittest.TestCase):
    def test_fixed_price_fee_and_premium_on_subtotal(self):
        r = cost.compute(base(mgmt_fee_rate=0.10, pricing={"model": "fixed", "risk_premium": 0.20}), rate_card=CARD)
        self.assertEqual(r["labor_total"], Dec("10400000"))
        self.assertEqual(r["mgmt_fee"], 1040000)
        self.assertEqual(r["risk_premium"], 2080000)       # 20% of subtotal, not of subtotal+fee
        self.assertEqual(r["price_tax_excluded"], 13520000)
        self.assertEqual(r["tax"], 1352000)
        self.assertEqual(r["price_tax_included"], 14872000)

    def test_tm_has_no_risk_premium(self):
        r = cost.compute(base(pricing={"model": "tm", "risk_premium": 0.2}), rate_card=CARD)
        self.assertEqual(r["risk_premium"], 0)
        self.assertTrue(any("ignored for T&M" in w for w in r["findings"]["warnings"]))

    def test_hybrid_premium_only_on_fixed_share_of_labor(self):
        r = cost.compute(base(pricing={"model": "hybrid", "fixed_share": 0.5, "risk_premium": 0.2}), rate_card=CARD)
        self.assertEqual(r["risk_premium"], 1040000)  # 10.4M × 0.5 × 0.2

    def test_premium_below_policy_floor_warns(self):
        r = cost.compute(base(pricing={"model": "fixed", "risk_premium": 0.06}), rate_card=CARD)
        self.assertTrue(any("less contingency than policy" in w for w in r["findings"]["warnings"]))

    def test_rounding_to_thousand_yen(self):
        r = cost.compute({"labor": [{"role": "X", "rate": 333333, "mm": 1}], "round_to": 1000,
                          "mgmt_fee_rate": 0.10, "pricing": {"model": "tm"}})
        self.assertEqual(r["price_tax_excluded"] % 1000, 0)
        self.assertEqual(r["price_tax_excluded"], 367000)   # 333,333 + 33,333 = 366,666 -> 367,000

    def test_missing_rate_is_an_error(self):
        with self.assertRaises(SierError):
            cost.compute({"labor": [{"role": "QA", "seniority": "mid", "mm": 1}]}, rate_card=CARD)


class Checks(unittest.TestCase):
    def test_budget_over_within_and_well_under(self):
        over = cost.compute(base(budget={"amount": 10000000, "basis": "tax_excluded"}), rate_card=CARD)
        self.assertEqual(over["budget_fit"]["status"], "over")
        within = cost.compute(base(budget={"amount": 14000000, "basis": "tax_excluded"}), rate_card=CARD)
        self.assertEqual(within["budget_fit"]["status"], "within")
        under = cost.compute(base(budget={"amount": 40000000, "basis": "tax_excluded"}), rate_card=CARD)
        self.assertEqual(under["budget_fit"]["status"], "well_under")

    def test_budget_tax_included_basis_compares_tax_included_price(self):
        r = cost.compute(base(budget={"amount": 15000000, "basis": "tax_included"}), rate_card=CARD)
        self.assertEqual(r["budget_fit"]["compared_price"], r["price_tax_included"])

    def test_reconciliation_against_estimate(self):
        bad = cost.compute(base(), rate_card=CARD, estimate={"recommended_mm": 9})
        self.assertFalse(bad["reconciliation"]["within_tolerance"])
        good = cost.compute(base(), rate_card=CARD, estimate={"recommended_mm": 12.3})
        self.assertTrue(good["reconciliation"]["within_tolerance"])

    def test_client_provided_lines_are_not_priced(self):
        r = cost.compute(base(non_labor=[{"item": "AWS", "monthly": 100000, "months": 12, "provided_by": "client"},
                                         {"item": "tools", "one_time": 50000}]), rate_card=CARD)
        self.assertEqual(r["non_labor_total"], Dec("50000"))
        self.assertEqual(len(r["client_provided"]), 1)

    def test_payment_schedule_sums_exactly(self):
        r = cost.compute(base(payment_schedule=[{"milestone": "a", "pct": 33}, {"milestone": "b", "pct": 33},
                                                {"milestone": "c", "pct": 34}]), rate_card=CARD)
        self.assertEqual(sum(x["amount_tax_included"] for x in r["payment_schedule"]), r["price_tax_included"])
        with self.assertRaises(SierError):
            cost.compute(base(payment_schedule=[{"pct": 50}, {"pct": 40}]), rate_card=CARD)

    def test_benchmark_rate_card_warns(self):
        r = cost.compute(base(), rate_card={**CARD, "benchmark_only": True})
        self.assertTrue(any("benchmark" in w for w in r["findings"]["warnings"]))


if __name__ == "__main__":
    unittest.main()
