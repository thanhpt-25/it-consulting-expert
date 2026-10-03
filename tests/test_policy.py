"""The policy file is the single source of truth — check it is internally consistent."""
import re
import unittest
from decimal import Decimal as Dec

import _helpers
from common import policy


class Policy(unittest.TestCase):
    def test_rubric_weights_sum_to_one(self):
        self.assertEqual(sum(Dec(str(d["weight"])) for d in policy()["rubric"]["dimensions"]), 1)

    def test_thresholds_descend(self):
        mins = [t["min"] for t in policy()["rubric"]["thresholds"]]
        self.assertEqual(mins, sorted(mins, reverse=True))

    def test_phase_ranges_can_sum_to_100(self):
        ph = policy()["estimation"]["phases"]
        self.assertLessEqual(sum(p["range"][0] for p in ph), 1.0)
        self.assertGreaterEqual(sum(p["range"][1] for p in ph), 1.0)

    def test_three_point_ordered(self):
        tp = policy()["estimation"]["three_point"]
        self.assertTrue(tp["optimistic"] < tp["most_likely"] <= tp["recommended"] < tp["pessimistic"])

    def test_no_skill_hardcodes_rubric_weights(self):
        """Weights live in policy.json only. A SKILL.md that restates them will drift (defect D4)."""
        pat = re.compile(r"Strategic Fit[^\n]*?\b15%")
        for p in (_helpers.PLUGIN / "skills").rglob("SKILL.md"):
            self.assertIsNone(pat.search(p.read_text(encoding="utf-8")), f"{p} restates rubric weights")


if __name__ == "__main__":
    unittest.main()
