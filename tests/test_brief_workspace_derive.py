import json
import os
import unittest
from pathlib import Path

import _helpers
from _helpers import TempWorkspace, fixture

import brief
import derive
import workspace
from common import SierError


class Brief(unittest.TestCase):
    def setUp(self):
        self.b = fixture("abc-manufacturing", "00-rfp-brief.json")

    def test_fixture_is_valid(self):
        f = brief.validate(self.b)
        self.assertEqual(f.errors, [])

    def test_rfp_label_without_citation_is_an_error(self):
        self.b["functional_requirements"][0]["citation"] = ""
        self.assertTrue(any("no citation" in e for e in brief.validate(self.b).errors))

    def test_assumption_cannot_be_rfp(self):
        self.b["assumptions"] = [{"text": "x", "label": "RFP", "citation": "p1"}]
        self.assertTrue(any("assumption cannot be labelled RFP" in e for e in brief.validate(self.b).errors))

    def test_duplicate_and_malformed_ids(self):
        self.b["functional_requirements"].append(dict(self.b["functional_requirements"][0]))
        self.b["integrations"][0]["id"] = "INT1"
        errs = " ".join(brief.validate(self.b).errors)
        self.assertIn("duplicate id FR-001", errs)
        self.assertIn("INT1", errs)

    def test_gaps_for_skill(self):
        self.assertEqual([g["id"] for g in brief.gaps_for(self.b, "cost-estimation")], ["Q-002"])
        with self.assertRaises(SierError):
            brief.gaps_for(self.b, "not-a-skill")

    def test_render_contains_sections_and_readiness(self):
        md = brief.render(self.b)
        for s in ("## 1. Project Overview", "FR-005", "¥200,000,000", "## 9. Downstream readiness"):
            self.assertIn(s, md)


class Workspace(unittest.TestCase):
    def test_init_layout_and_duplicate_refusal(self):
        with TempWorkspace() as ws:
            for sub in workspace.SUBDIRS:
                self.assertTrue((ws / sub).is_dir(), sub)
            self.assertTrue((ws.parent / "_firm").is_dir())
            with self.assertRaises(SierError):
                workspace.init("Test Client", "Test Project", root=ws.parent, slug="t")

    def test_find_walks_up_from_subfolder(self):
        with TempWorkspace() as ws:
            cwd = os.getcwd()
            try:
                os.chdir(ws / "artifacts")
                self.assertEqual(workspace.find(), ws.resolve())
            finally:
                os.chdir(cwd)

    def test_stale_brief_detection(self):
        eng = {"brief": {"generated_at": "2026-07-01"}, "sources_updated_at": "2026-07-05"}
        self.assertTrue(workspace.brief_is_stale(eng))
        eng["sources_updated_at"] = "2026-06-30"
        self.assertFalse(workspace.brief_is_stale(eng))

    def test_slugify_keeps_japanese(self):
        self.assertEqual(workspace.slugify("ABC製造", "CRM / 移行"), "ABC製造-CRM-移行")


class Derive(unittest.TestCase):
    def _script(self, ws, name, body):
        p = ws / "_state" / "derived" / name
        p.write_text(body, encoding="utf-8")
        return p

    def test_guardrails(self):
        with TempWorkspace() as ws:
            with self.assertRaisesRegex(SierError, "no `assert`"):
                derive.run(ws, self._script(ws, "a.py", "print('{}')"))
            with self.assertRaisesRegex(SierError, "Tier-1"):
                derive.run(ws, self._script(ws, "b.py", "import json\nassert True\nprint(json.dumps({'x': {'verdict': 1}}))"))
            with self.assertRaisesRegex(SierError, "must live in"):
                outside = ws / "c.py"
                outside.write_text("assert True\nprint('{}')")
                derive.run(ws, outside)
            ok = derive.run(ws, self._script(ws, "d.py", "import json\nassert 1 + 1 == 2\nprint(json.dumps({'p80': 3}))"))
            rec = json.loads(Path(ok["output_path"]).read_text())
            self.assertEqual(rec["output"], {"p80": 3})
            self.assertEqual(len(rec["script_sha256"]), 64)

    def test_failing_script_reports_stderr(self):
        with TempWorkspace() as ws:
            with self.assertRaisesRegex(SierError, "ZeroDivisionError"):
                derive.run(ws, self._script(ws, "e.py", "assert True\n1/0"))


if __name__ == "__main__":
    unittest.main()
