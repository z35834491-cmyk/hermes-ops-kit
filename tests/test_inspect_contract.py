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
        data = json.loads(result.stdout)
        for item in data["checks"]:
            self.assertIn("duration_seconds", item)
            self.assertGreaterEqual(item["duration_seconds"], 0)

    def test_exclude_and_disabled_components_are_skipped(self):
        fixture = """
version: "0.2"
environments:
  test:
    type: k8s
    kubeconfig: "~/.kube/config-test"
    components:
      longhorn:
        mode: disabled
        disabled_reason: "not used in this fixture"
      elasticsearch:
        mode: auto
    inspection:
      include:
        - k8s_nodes_ready
        - longhorn_health
        - elasticsearch_health
      exclude:
        - elasticsearch_health
"""
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "env-map.yaml"
            path.write_text(fixture, encoding="utf-8")
            result = self._inspect(
                "test",
                "--config",
                str(path),
                "--catalog",
                "config/check-catalog.yaml",
                "--plan",
                "--json",
            )
            data = json.loads(result.stdout)
            by_id = {item["id"]: item for item in data["checks"]}
            self.assertEqual(by_id["elasticsearch_health"]["status"], "skipped")
            self.assertIn("excluded by inspection.exclude", by_id["elasticsearch_health"]["evidence"])
            self.assertEqual(by_id["longhorn_health"]["status"], "skipped")
            self.assertIn("component longhorn is disabled", by_id["longhorn_health"]["evidence"])
            self.assertEqual(by_id["k8s_nodes_ready"]["status"], "skipped")
            self.assertIn("plan-only", by_id["k8s_nodes_ready"]["evidence"])
            self.assertIn("duration_seconds", by_id["k8s_nodes_ready"])
            self.assertGreaterEqual(by_id["k8s_nodes_ready"]["duration_seconds"], 0)

    def test_empty_include_does_not_dispatch_catalog(self):
        fixture = """
version: "0.2"
environments:
  test:
    type: k8s
    kubeconfig: "~/.kube/config-test"
    inspection:
      include: []
"""
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "env-map.yaml"
            path.write_text(fixture, encoding="utf-8")
            result = self._inspect(
                "test",
                "--config",
                str(path),
                "--catalog",
                "config/check-catalog.yaml",
                "--plan",
                "--json",
            )
            data = json.loads(result.stdout)
            ids = [item["id"] for item in data["checks"]]
            self.assertEqual(ids, ["env_map_contract"])


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
