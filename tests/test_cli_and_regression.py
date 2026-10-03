"""End-to-end through the CLI, and regression assertions for the ABC Manufacturing dry run."""
import contextlib
import io
import json
import shutil
import unittest
from decimal import Decimal as Dec

import _helpers
from _helpers import FIXTURES, TempWorkspace, fixture

import importlib.util
import cost
import estimate
import sla

_spec = importlib.util.spec_from_file_location("sier_cli", _helpers.ENGINE / "__main__.py")
cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cli)

ABC = FIXTURES / "abc-manufacturing"


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main([str(a) for a in argv])
    return code, out.getvalue(), err.getvalue()


class RegressionABC(unittest.TestCase):
    """Each assertion pins a claim made in tests/fixtures/abc-manufacturing/README.md."""

    def test_factor_product_is_not_1_07(self):
        r = estimate.compute(fixture("abc-manufacturing", "estimate.json"))
        self.assertEqual(r["params"]["factor_product"], Dec("1.2018"))  # 1.20175 at 4 dp
        self.assertEqual(r["totals_mm"]["base"], Dec("106"))
        self.assertEqual(r["totals_mm"]["subtotal"], Dec("121.9"))

    def test_correct_estimate_reconciles_with_team_plan(self):
        r = estimate.compute(fixture("abc-manufacturing", "estimate.json"))
        self.assertEqual(r["recommended_mm"], Dec("175.7920"))  # 121.9 × 1.20175 × 1.2 = 175.79199
        c = cost.compute(fixture("abc-manufacturing", "cost-policy.json"), estimate=r)
        self.assertEqual(c["labor_mm"], Dec("178"))
        self.assertTrue(c["reconciliation"]["within_tolerance"])

    def test_matching_total_hides_role_shortfall(self):
        # Found by the review-qcd agent in a live run, then made deterministic: QA 20 vs ~37.5 人月.
        r = estimate.compute(fixture("abc-manufacturing", "estimate.json"))
        c = cost.compute(fixture("abc-manufacturing", "cost-policy.json"), estimate=r)
        qa = next(x for x in c["reconciliation"]["by_role"] if x["role"] == "QA")
        self.assertTrue(qa["flag"])
        self.assertLess(qa["team_mm"], qa["estimate_mm"])
        self.assertTrue(any("short against the estimate's role allocation" in w and "QA" in w
                            for w in c["findings"]["warnings"]))

    def test_dry_run_pricing_arithmetic(self):
        c = cost.compute(fixture("abc-manufacturing", "cost-as-dry-run.json"))
        self.assertEqual(c["labor_total"], Dec("169600000"))
        self.assertEqual(c["cost_subtotal"], Dec("186600000"))
        self.assertEqual(c["risk_premium"], 11196000)       # dry run printed 11,400,000
        self.assertEqual(c["price_tax_excluded"], 197796000)
        w = " ".join(c["findings"]["warnings"])
        self.assertIn("less contingency than policy", w)
        self.assertIn("management fee 0.0%", w)

    def test_policy_pricing_is_over_budget(self):
        c = cost.compute(fixture("abc-manufacturing", "cost-policy.json"),
                         brief_budget=fixture("abc-manufacturing", "00-rfp-brief.json")["commercial"]["budget"])
        self.assertEqual(c["price_tax_excluded"], 233250000)
        self.assertEqual(c["budget_fit"]["status"], "over")
        self.assertEqual(c["budget_fit"]["delta"], Dec("33250000"))

    def test_maintenance_fee_and_downtime_claim(self):
        r = sla.compute(fixture("abc-manufacturing", "sla.json"))
        self.assertEqual(r["fee"]["annual_total"], 29669400)   # dry run printed 30,000,000
        self.assertTrue(any("allows 54.0 min" in w for w in r["findings"]["warnings"]))


class CLIPipeline(unittest.TestCase):
    def test_full_pipeline_then_verify_then_tamper(self):
        with TempWorkspace() as ws:
            shutil.copy(ABC / "00-rfp-brief.json", ws / "00-rfp-brief.json")
            self.assertEqual(run("brief", "render", "--ws", ws)[0], 0)
            eng = json.loads((ws / "engagement.json").read_text())
            self.assertEqual(eng["brief"]["source_tier"], 3)
            self.assertEqual(run("score", "--in", ABC / "go-nogo.json", "--ws", ws)[0], 0)
            self.assertEqual(run("estimate", "--in", ABC / "estimate.json", "--ws", ws)[0], 0)
            self.assertEqual(run("cost", "--in", ABC / "cost-policy.json", "--ws", ws)[0], 0)
            for f in ("01-go-nogo.json", "03-estimate.md", "05-cost.json", "inputs/cost.json"):
                self.assertTrue((ws / f).exists(), f)
            self.assertGreaterEqual(len(list((ws / "_state" / "runs").glob("*.json"))), 4)

            code, out, _ = run("verify", "--ws", ws)
            self.assertEqual(code, 1)                      # over budget is a real problem
            self.assertIn("recomputed from inputs: identical", out)
            self.assertIn("| Budget fit | ❌ | over |", out)

            md = ws / "05-cost.md"
            md.write_text(md.read_text().replace("¥233,250,000", "¥199,800,000"))
            code, out, _ = run("verify", "--ws", ws)
            self.assertIn("edited by hand", out)

    def test_strict_exit_code_on_warnings(self):
        code, _, _ = run("cost", "--in", ABC / "cost-as-dry-run.json", "--no-ws", "--strict")
        self.assertEqual(code, 3)

    def test_bad_input_exit_code(self):
        code, _, err = run("estimate", "--in", "/nonexistent.json", "--no-ws")
        self.assertEqual(code, 2)
        self.assertIn("File not found", err)


if __name__ == "__main__":
    unittest.main()
