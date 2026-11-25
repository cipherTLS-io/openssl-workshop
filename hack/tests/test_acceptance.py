import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("acceptance", Path(__file__).parents[1] / "acceptance.py")
acceptance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acceptance)


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "hack/acceptance").mkdir(parents=True)
        (self.root / "docs").mkdir()
        (self.root / "docs/PHASES.md").write_text(
            "---\nschema: phases/v1\nphases:\n  - id: M0\n    status: todo\n---\n")
        self.row = {"gate": "hack/acceptance/m0.sh", "tier": "e2e",
                    "requires": [], "manual": False, "skeleton": False}

    def run_gate(self, script, **kwargs):
        (self.root / self.row["gate"]).write_text(script)
        (self.root / "hack/acceptance/phases.json").write_text(json.dumps({"M0": self.row}))
        with contextlib.redirect_stdout(io.StringIO()):
            return acceptance.run(self.root, **kwargs)

    def test_implemented_gate_passes(self):
        self.assertEqual(self.run_gate("exit 0\n"), 0)

    def test_implemented_gate_failure_is_not_a_skeleton(self):
        self.assertEqual(self.run_gate("exit 1\n"), 1)

    def test_pending_skeleton_is_not_product_acceptance(self):
        self.row["skeleton"] = True
        self.assertEqual(self.run_gate("exit 1\n"), 0)
        self.assertEqual(self.run_gate("exit 1\n", phase="M0"), 1)

    def test_green_or_broken_skeleton_is_rejected(self):
        self.row["skeleton"] = True
        self.assertEqual(self.run_gate("exit 0\n"), 1)
        self.assertEqual(self.run_gate("exit 2\n"), 1)

    def test_manual_gate_remains_pending_without_execution(self):
        self.row["manual"] = True
        self.assertEqual(self.run_gate("touch ran\nexit 0\n"), 0)
        self.assertFalse((self.root / "ran").exists())
        self.assertEqual(self.run_gate("exit 0\n", phase="M0"), 1)
        self.assertEqual(self.run_gate("exit 0\n", phase="M0", manual=True), 0)

    def test_capabilities_are_required_for_real_gates(self):
        self.row["requires"] = ["container-runtime"]
        self.assertEqual(self.run_gate("touch ran\nexit 0\n"), 1)
        self.assertFalse((self.root / "ran").exists())
        self.assertEqual(self.run_gate("exit 0\n", capabilities=["container-runtime"]), 0)

    def test_arguments_are_an_argument_vector(self):
        self.row["args"] = ["value with spaces"]
        self.assertEqual(self.run_gate('test "$#" = 1 && test "${1}" = "value with spaces"\n'), 0)

    def test_missing_path_fails_closed(self):
        self.run_gate("exit 0\n")
        (self.root / self.row["gate"]).unlink()
        with self.assertRaises(ValueError):
            acceptance.load_manifest(self.root)

    def test_unknown_ledger_phase_rejected(self):
        self.run_gate("exit 0\n")
        (self.root / "docs/PHASES.md").write_text("---\nschema: phases/v1\nphases:\n  - id: M1\n---\n")
        with self.assertRaises(ValueError):
            acceptance.load_manifest(self.root)

    def test_phase_dependency_is_not_a_host_capability(self):
        self.row["requires"] = ["M1"]
        with self.assertRaises(ValueError):
            self.run_gate("exit 0\n")

    def test_done_milestone_cannot_keep_skeleton(self):
        self.row["skeleton"] = True
        (self.root / "docs/PHASES.md").write_text(
            "---\nschema: phases/v1\nphases:\n  - id: M0\n    status: done\n---\n")
        with self.assertRaises(ValueError):
            self.run_gate("exit 1\n")
