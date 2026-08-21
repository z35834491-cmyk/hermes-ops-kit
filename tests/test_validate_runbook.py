import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


class ValidateRunbookTests(unittest.TestCase):
    def setUp(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from validate_runbook import parse_runbook, validate_runbook
        self.parse_runbook = parse_runbook
        self.validate_runbook = validate_runbook

    def test_example_runbooks_pass(self):
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_runbook.py"), str(ROOT / "examples" / "runbooks")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_l0_change_mode_is_error(self):
        text = """
name: bad-runbook
title: Bad
category: k8s
risk_level: L0
requires_approval: false
mode: change
inputs:
  - name: env
    required: true
    description: Environment name from env-map.
verification:
  - done
"""
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "runbooks"
            path.mkdir()
            file_path = path / "bad-runbook.yaml"
            file_path.write_text(text, encoding="utf-8")
            data = self.parse_runbook(text)
            errors = self.validate_runbook(file_path, data)
            self.assertTrue(any("read-only" in item for item in errors))

    def test_filename_must_match_name(self):
        text = """
name: other-name
title: Bad
category: k8s
risk_level: L0
requires_approval: false
mode: read-only
inputs:
  - name: env
    required: true
    description: Environment name from env-map.
verification:
  - done
"""
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "runbooks"
            path.mkdir()
            file_path = path / "mismatch.yaml"
            file_path.write_text(text, encoding="utf-8")
            data = self.parse_runbook(text)
            errors = self.validate_runbook(file_path, data)
            self.assertTrue(any("filename stem" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
