import unittest
from decimal import Decimal as Dec

import _helpers  # noqa: F401
import change
import evm
import score
import sla
from common import SierError


class EVM(unittest.TestCase):
    def test_known_values(self):
        r = evm.compute({"bac": 1000, "pv": 500, "ev": 400, "ac": 500})
        self.assertEqual(r["spi"], Dec("0.8"))
        self.assertEqual(r["cpi"], Dec("0.8"))
        self.assertEqual(r["eac"], Dec("1250"))
        self.assertEqual(r["etc"], Dec("750"))
        self.assertEqual(r["tcpi"], Dec("1.2"))
        self.assertEqual(r["rag"]["spi"], "red")      # < 0.85
        self.assertEqual(r["rag"]["tcpi"], "yellow")  # 1.2 is not > 1.2
        self.assertEqual(r["overall"], "red")

    def test_from_tasks(self):
        r = evm.compute({"bac": 300, "tasks": [
            {"planned_value": 100, "planned_pct": 1, "pct_complete": 1, "actual_cost": 90},
            {"planned_value": 200, "planned_pct": 0.5, "pct_complete": 0.25, "actual_cost": 60}]})
        self.assertEqual(r["pv"], Dec("200"))
        self.assertEqual(r["ev"], Dec("150"))
        self.assertEqual(r["ac"], Dec("150"))

    def test_zero_actual_cost_is_safe(self):
        r = evm.compute({"bac": 100, "pv": 10, "ev": 10, "ac": 0})
        self.assertIsNone(r["cpi"])
        self.assertEqual(r["rag"]["cpi"], "n/a")


class Score(unittest.TestCase):
    ALL = {"strategic_fit": 4, "capability_match": 4, "win_probability": 3, "profitability": 3,
           "delivery_risk": 3, "resource_availability": 3}

    def test_dry_run_scores_give_conditional_go(self):
        r = score.compute({"scores": self.ALL})
        self.assertEqual(r["weighted_score"], Dec("3.40"))
        self.assertEqual(r["verdict"], "CONDITIONAL_GO")

    def test_mandatory_gate_overrides_score(self):
        r = score.compute({"scores": {k: 5 for k in self.ALL}, "mandatory": [{"requirement": "ISMS", "met": False}]})
        self.assertEqual(r["score_verdict"], "STRONG_GO")
        self.assertEqual(r["verdict"], "DEFINITE_NO_GO")

    def test_missing_dimension_is_an_error(self):
        with self.assertRaises(SierError):
            score.compute({"scores": {"strategic_fit": 4}})


class ChangeAuthority(unittest.TestCase):
    def test_boundaries_follow_change_request_skill(self):
        a = change.authority
        self.assertEqual(a(Dec(999999), Dec(4), False), "pm")
        self.assertEqual(a(Dec(1000000), Dec(0), False), "director")   # ¥1M is not "< ¥1M"
        self.assertEqual(a(Dec(0), Dec(5), False), "director")
        self.assertEqual(a(Dec(5000000), Dec(15), False), "director")  # ¥1M–¥5M or 5–15 days inclusive
        self.assertEqual(a(Dec(5000001), Dec(0), False), "executive")
        self.assertEqual(a(Dec(0), Dec(16), False), "executive")
        self.assertEqual(a(Dec(0), Dec(0), True), "executive")         # go-live change

    def test_gates(self):
        led = {"baseline": {"cost": 100}, "crs": [{"id": "1", "status": "approved", "cost_delta": 11},
                                                  {"id": "2", "status": "proposed", "cost_delta": 50}]}
        r = change.report(led)
        self.assertEqual(r["cumulative"]["cost"]["gate"], "yellow")   # pending does not count
        led["crs"][1]["status"] = "approved"
        self.assertEqual(change.report(led)["cumulative"]["cost"]["gate"], "red")


class SLA(unittest.TestCase):
    def test_downtime_minutes(self):
        r = sla.compute({"availability_tiers": [{"id": "a", "target": 99.9, "window": "24x7"},
                                                {"id": "b", "target": 99.5, "window": "business_hours"}]})
        self.assertEqual(r["availability"][0]["allowed_downtime_minutes_per_month"], Dec("43.2"))
        self.assertEqual(r["availability"][1]["allowed_downtime_minutes_per_month"], Dec("54.0"))

    def test_fee_and_multi_year_discount(self):
        r = sla.compute({"project_cost": 100000000, "maintenance_rate": 0.15, "contract_years": 3})
        self.assertEqual(r["fee"]["annual_total"], 15000000)
        self.assertEqual(r["fee"]["contract_total"], 42750000)  # 45M × 0.95


if __name__ == "__main__":
    unittest.main()
