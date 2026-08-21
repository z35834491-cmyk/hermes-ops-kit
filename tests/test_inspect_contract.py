import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


class InspectContractTests(unittest.TestCase):
    def _inspect(self, *args, check=True):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "inspect.py"), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if check and result.returncode != 0:
            raise AssertionError(result.stderr or result.stdout)
        return result

    def test_all_target_stamps_env_and_unique_id_env_pairs(self):
        result = self._inspect(
            "all",
            "--config",
            "config/env-map.example.yaml",
            "--plan",
            "--json",
        )
        data = json.loads(result.stdout)
        pairs = [(item["id"], item.get("env")) for item in data["checks"]]
        self.assertTrue(all(item.get("env") for item in data["checks"]))
        self.assertEqual(len(pairs), len(set(pairs)))
        self.assertIn("duration_seconds", data)
        self.assertGreaterEqual(data["duration_seconds"], 0)

    def test_missing_config_exits_nonzero(self):
        result = self._inspect("test", "--config", "/tmp/hermes-ops-kit-missing-env-map.yaml", "--json", check=False)
        self.assertNotEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "warning")

    def test_example_target_exits_zero(self):
        result = self._inspect("test", "--config", "config/env-map.example.yaml", "--plan", "--json")
        self.assertEqual(result.returncode, 0)


class OnboardContractTests(unittest.TestCase):
    def test_generated_include_exists_in_catalog(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        from lib.check_catalog import load_check_catalog
        from lib.env_map import load_env_map

        with TemporaryDirectory() as tmp:
            output = Path(tmp) / "generated.yaml"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "onboard.py"),
                    "--env",
                    "test",
                    "--output",
                    str(output),
                    "--force",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            catalog = load_check_catalog(str(ROOT / "config" / "check-catalog.yaml"))
            env_map = load_env_map(str(output))
            include = env_map.environments["test"].inspection_include
            missing = [item for item in include if item not in catalog.checks]
            self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
