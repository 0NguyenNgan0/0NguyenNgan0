"""Exercise the public CLI, saved report, and blend-weight routing contract."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    return subprocess.run([sys.executable, "-m", "recommender", *args],
                          cwd=ROOT, capture_output=True, text=True)


class CliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        baseline = run_cli("--seed", "42", "--k", "10")
        if baseline.returncode:
            raise RuntimeError(baseline.stderr)
        cls.baseline = json.loads(baseline.stdout)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "report.json"
            changed = run_cli("--seed", "42", "--k", "10", "--als-weight", "0.3",
                              "--output", str(output))
            if changed.returncode:
                raise RuntimeError(changed.stderr)
            cls.changed = json.loads(changed.stdout)
            cls.saved = json.loads(output.read_text(encoding="utf-8"))

    def test_report_records_weight_and_saved_output_matches_stdout(self):
        self.assertEqual(self.baseline["configuration"]["als_weight"], 0.6)
        self.assertEqual(self.changed["configuration"]["als_weight"], 0.3)
        self.assertEqual(self.changed, self.saved)

    def test_weight_changes_warm_hybrid_only_on_fixed_fixture(self):
        before, after = self.baseline["methods"], self.changed["methods"]
        for method in ("popularity", "als", "content"):
            self.assertEqual(before[method], after[method])
        for cohort in ("sparse", "new"):
            self.assertEqual(before["hybrid"]["by_cohort"][cohort],
                             after["hybrid"]["by_cohort"][cohort])
        self.assertNotEqual(before["hybrid"]["by_cohort"]["warm"],
                            after["hybrid"]["by_cohort"]["warm"])

    def test_invalid_weight_exits_cleanly_without_report(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            for value in ("-0.1", "1.1", "nan", "inf", "-inf", "abc"):
                with self.subTest(value=value):
                    result = run_cli(f"--als-weight={value}", "--output", str(output))
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("must be a finite number between 0 and 1", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(result.stdout, "")
                    self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
