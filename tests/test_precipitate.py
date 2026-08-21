import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.lesson_candidate import LessonCandidateError, load_lesson_candidate, validate_candidate  # noqa: E402


EXAMPLE = ROOT / "examples" / "lesson-candidate.example.yaml"


class PrecipitateTests(unittest.TestCase):
    def _run(self, *args, check=True):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "precipitate.py"), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if check and result.returncode != 0:
            raise AssertionError(result.stderr or result.stdout)
        return result

    def test_example_candidate_loads(self):
        data = load_lesson_candidate(EXAMPLE)
        self.assertEqual(data["name"], "example-component-health-diagnostic")
        self.assertEqual(data["risk_level"], "L0")

    def test_example_writes_valid_runbook_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "example-component-health-diagnostic.generated.yaml"
            result = self._run("--from", str(EXAMPLE), "--output", str(out), "--force")
            self.assertIn("review_required=true", result.stdout)
            self.assertTrue(out.exists())
            self.assertNotIn("~/.hermes", out.read_text(encoding="utf-8"))
            checked = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "validate_runbook.py"), str(out)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_rejects_private_ip(self):
        ip = ".".join(["10", "0", "0", "8"])
        lesson = f"Restart the node at {ip}"
        errors = validate_candidate(
            {
                "name": "redis-memory-high-diagnostic",
                "title": "Redis memory",
                "category": "redis",
                "lesson": lesson,
                "verification": ["done"],
            },
            f"lesson: {lesson}\n",
        )
        self.assertTrue(any("unsanitized" in item for item in errors))

    def test_rejects_l2(self):
        errors = validate_candidate(
            {
                "name": "mysql-failover",
                "title": "Failover",
                "category": "mysql",
                "risk_level": "L2",
                "lesson": "Promote a replica after approval.",
                "verification": ["replication is healthy"],
            },
            "risk_level: L2\n",
        )
        self.assertTrue(any("L0" in item for item in errors))

    def test_refuses_non_generated_output_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "promoted.yaml"
            result = self._run("--from", str(EXAMPLE), "--output", str(out), "--force", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(".generated.yaml", result.stderr)
            self.assertFalse(out.exists())

    def test_missing_candidate_exits_nonzero(self):
        result = self._run("--from", "/tmp/hermes-ops-kit-missing-lesson.yaml", check=False)
        self.assertNotEqual(result.returncode, 0)

    def test_does_not_import_hermes_home(self):
        source = (ROOT / "scripts" / "precipitate.py").read_text(encoding="utf-8")
        lib = (ROOT / "scripts" / "lib" / "lesson_candidate.py").read_text(encoding="utf-8")
        self.assertNotIn("~/.hermes", source)
        self.assertNotIn("HERMES_HOME", source)
        self.assertNotIn("~/.hermes", lib)

    def test_placeholder_name_is_rejected(self):
        with self.assertRaises(LessonCandidateError):
            load_lesson_candidate(ROOT / "templates" / "lesson-candidate-template.yaml")


if __name__ == "__main__":
    unittest.main()
