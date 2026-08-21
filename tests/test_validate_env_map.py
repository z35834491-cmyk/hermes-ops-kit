import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_env_map import validate  # noqa: E402


class ValidateEnvMapTests(unittest.TestCase):
    def test_example_aligns_with_catalog(self):
        ok, errors, warnings, envs = validate(
            ROOT / "config" / "env-map.example.yaml",
            catalog_path=ROOT / "config" / "check-catalog.yaml",
        )
        self.assertTrue(ok)
        self.assertEqual(errors, [])
        self.assertIn("test", envs)
        self.assertEqual(warnings, [])

    def test_unknown_include_is_error(self):
        text = """
version: "0.2"
environments:
  test:
    type: k8s
    kubeconfig: "~/.kube/config-test"
    inspection:
      include:
        - pvc_usage
"""
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "env-map.yaml"
            path.write_text(text, encoding="utf-8")
            ok, errors, _warnings, _envs = validate(
                path,
                catalog_path=ROOT / "config" / "check-catalog.yaml",
            )
            self.assertFalse(ok)
            self.assertTrue(any("unknown check: pvc_usage" in item for item in errors))

    def test_unknown_exclude_is_error(self):
        text = """
version: "0.2"
environments:
  test:
    type: k8s
    kubeconfig: "~/.kube/config-test"
    inspection:
      include:
        - pvc_status
      exclude:
        - node_disk
"""
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "env-map.yaml"
            path.write_text(text, encoding="utf-8")
            ok, errors, _warnings, _envs = validate(
                path,
                catalog_path=ROOT / "config" / "check-catalog.yaml",
            )
            self.assertFalse(ok)
            self.assertTrue(any("unknown check: node_disk" in item for item in errors))

    def test_disabled_include_is_warning(self):
        text = """
version: "0.2"
environments:
  test:
    type: k8s
    kubeconfig: "~/.kube/config-test"
    components:
      longhorn:
        mode: disabled
        disabled_reason: "not used"
    inspection:
      include:
        - longhorn_health
"""
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "env-map.yaml"
            path.write_text(text, encoding="utf-8")
            ok, errors, warnings, _envs = validate(
                path,
                catalog_path=ROOT / "config" / "check-catalog.yaml",
            )
            self.assertTrue(ok)
            self.assertEqual(errors, [])
            self.assertTrue(any("longhorn_health" in item and "disabled" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
