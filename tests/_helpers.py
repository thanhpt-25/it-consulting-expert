"""Test helpers: put the sier engine on sys.path and provide fixture/workspace utilities."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "plugins" / "it-consulting-expert"
ENGINE = PLUGIN / "sier"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(ENGINE))


def fixture(*parts):
    return json.loads((FIXTURES.joinpath(*parts)).read_text(encoding="utf-8"))


class TempWorkspace:
    """Context manager: a throwaway engagement workspace."""

    def __enter__(self):
        import workspace
        self.root = Path(tempfile.mkdtemp(prefix="sier-test-"))
        self.ws = workspace.init("Test Client", "Test Project", root=self.root, slug="t")
        return self.ws

    def __exit__(self, *exc):
        shutil.rmtree(self.root, ignore_errors=True)
