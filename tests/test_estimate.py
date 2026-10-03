import unittest
from decimal import Decimal as Dec

import _helpers  # noqa: F401
import estimate
from common import SierError


def wbs(items, **kw):
    return {"method": "wbs", "items": items, **kw}


def item(i, phase="implementation", days=5, **kw):
    return {"id": f"W-{i:03d}", "req": "FR-001", "phase": phase, "days": days, "role": "SE", **kw}


class FunctionPoints(unittest.TestCase):
    def test_guide_worked_example(self):
        # function-point-guide.md: UFP 59, VAF 1.05, 10 h/FP -> ~620 h, ~3.9 人月
        r = estimate.compute({"method": "fp", "pm_overhead": 0.10, "fp": {
            "counts": {"EI": {"avg": 1, "high": 2}, "EO": {"avg": 1, "high": 1}, "EQ": {"low": 1, "avg": 1},
                       "ILF": {"avg": 1, "low": 1}, "EIF": {"avg": 1}},
            "vaf": 1.05, "hours_per_fp": 10, "extra_phase_shares": {}}})
        self.assertEqual(r["fp"]["ufp"], Dec("59"))
        self.assertEqual(r["fp"]["afp"], Dec("61.95"))
        self.assertEqual(r["fp"]["core_hours"], Dec("619.5"))
        self.assertAlmostEqual(float(r["totals_mm"]["base"]), 3.87, places=2)

    def test_gsc_drives_vaf(self):
        r = estimate.compute({"method": "fp", "fp": {"counts": {"ILF": {"avg": 10}}, "gsc": [3] * 14, "hours_per_fp": 8}})
        self.assertEqual(r["fp"]["vaf"], Dec("1.07"))  # 0.65 + 0.01 * 42

    def test_fp_warns_about_missing_deployment(self):
        r = estimate.compute({"method": "fp", "fp": {"counts": {"EI": {"low": 5}}, "hours_per_fp": 8}})
        self.assertTrue(any("移行" in w for w in r["findings"]["warnings"]))

    def test_vaf_out_of_range_rejected(self):
        with self.assertRaises(SierError):
            estimate.compute({"method": "fp", "fp": {"counts": {"EI": {"low": 1}}, "vaf": 1.5, "hours_per_fp": 8}})


class WBS(unittest.TestCase):
    def test_rollup_order_of_operations(self):
        r = estimate.compute(wbs([item(1, days=100)], pm_overhead=0.10,
                                 factors={"technical_complexity": 1.2, "team_experience": 0.9}))
        t = r["totals_days"]
        self.assertEqual(t["base"], Dec("100"))
        self.assertEqual(t["pm"], Dec("10"))
        self.assertEqual(t["subtotal"], Dec("110"))
        self.assertEqual(r["params"]["factor_product"], Dec("1.08"))
        self.assertEqual(t["adjusted"], Dec("118.8"))
        self.assertEqual(t["recommended"], Dec("142.56"))     # × 1.2
        self.assertEqual(t["pessimistic"], Dec("178.2"))      # × 1.5
        self.assertEqual(r["recommended_mm"], Dec("7.128"))   # / 20

    def test_factor_out_of_bounds_is_an_error(self):
        with self.assertRaises(SierError):
            estimate.compute(wbs([item(1)], factors={"team_experience": 2.0}))

    def test_unknown_factor_is_an_error(self):
        with self.assertRaises(SierError):
            estimate.compute(wbs([item(1)], factors={"vibes": 1.1}))

    def test_duplicate_id_and_unknown_phase(self):
        with self.assertRaises(SierError) as cm:
            estimate.compute(wbs([item(1), item(1), item(2, phase="nonsense")]))
        self.assertIn("duplicate id", str(cm.exception))
        self.assertIn("unknown phase", str(cm.exception))

    def test_japanese_phase_names_accepted(self):
        r = estimate.compute(wbs([item(1, phase="製造"), item(2, phase="要件定義")]))
        self.assertEqual({p["id"] for p in r["phases"]}, {"implementation", "requirements"})

    def test_untraced_and_oversized_warnings(self):
        r = estimate.compute(wbs([{"id": "W-1", "phase": "製造", "days": 12, "role": "PG"},
                                  {"id": "W-2", "phase": "製造", "days": 3, "role": "PG", "label": "Proposed"}]))
        w = " ".join(r["findings"]["warnings"])
        self.assertIn("no RFP requirement id: W-1", w)
        self.assertIn("exceed 5 man-days", w)
        self.assertEqual(r["traceability"]["proposed"], 1)

    def test_role_allocation_sums_to_recommended(self):
        r = estimate.compute(wbs([item(1, days=40), {**item(2, days=60), "role": "PG"}], pm_overhead=0.12))
        total = sum(x["recommended_mm"] for x in r["roles"])
        self.assertAlmostEqual(float(total), float(r["recommended_mm"]), places=3)

    def test_calibration_is_informational_unless_applied(self):
        cal = {"project_type": "x", "n": 3, "factor": 1.3}
        a = estimate.compute(wbs([item(1, days=100)]), calibration=cal)
        b = estimate.compute(wbs([item(1, days=100)], apply_calibration=True), calibration=cal)
        self.assertEqual(b["recommended_mm"], (a["recommended_mm"] * Dec("1.3")).quantize(Dec("0.0001")))
        self.assertIn("calibrated_recommended", a["totals_days"])


if __name__ == "__main__":
    unittest.main()
