import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.lib.env_map import load_env_map, extract_environment_names, get_environment


EXAMPLE = '''
version: "0.2"

environments:
  dev:
    type: k8s
    kubeconfig: "~/.kube/config-dev"
    components:
      longhorn:
        mode: disabled
        disabled_reason: "optional storage backend"
      mysql:
        mode: auto
    inspection:
      include:
        - k8s_nodes_ready
        - pod_abnormal
        - longhorn_health
      exclude:
        - pod_abnormal
  test:
    type: k8s
    kubeconfig: "~/.kube/config-test"
    inspection:
      include:
        - warning_events
        - pvc_status
      exclude:
        - argocd_sync
rules:
  - "Never store credential values"
'''


class EnvMapLoaderTests(unittest.TestCase):
    def test_extract_environment_names(self):
        self.assertEqual(extract_environment_names(EXAMPLE), ["dev", "test"])

    def test_load_env_map_and_get_environment(self):
        with TemporaryDirectory() as td:
            path = Path(td) / "env-map.yaml"
            path.write_text(EXAMPLE, encoding="utf-8")
            env_map = load_env_map(str(path))
            test_env = get_environment(env_map, "test")
            self.assertEqual(test_env.name, "test")
            self.assertEqual(test_env.kubeconfig, "~/.kube/config-test")
            self.assertEqual(test_env.inspection_include, ["warning_events", "pvc_status"])
            self.assertEqual(test_env.inspection_exclude, ["argocd_sync"])
            self.assertEqual(test_env.disabled_components, {})
            dev_env = get_environment(env_map, "dev")
            self.assertEqual(dev_env.inspection_exclude, ["pod_abnormal"])
            self.assertEqual(dev_env.disabled_components["longhorn"], "optional storage backend")
            self.assertNotIn("mysql", dev_env.disabled_components)
            self.assertTrue(dev_env.has_inspection_include)
            self.assertTrue(test_env.has_inspection_include)

    def test_example_env_map_honors_disabled_components(self):
        env_map = load_env_map(str(Path(__file__).resolve().parents[1] / "config" / "env-map.example.yaml"))
        dev = get_environment(env_map, "dev")
        self.assertIn("longhorn", dev.disabled_components)
        self.assertIn("retired_mongodb", dev.disabled_components)
        self.assertEqual(dev.inspection_exclude, [])
        self.assertNotIn("mysql", dev.disabled_components)

    def test_disabled_reason_before_mode(self):
        text = '''
version: "0.2"
environments:
  test:
    type: k8s
    kubeconfig: "~/.kube/config-test"
    components:
      longhorn:
        disabled_reason: "reason first"
        mode: disabled
    inspection:
      include:
        - longhorn_health
'''
        with TemporaryDirectory() as td:
            path = Path(td) / "env-map.yaml"
            path.write_text(text, encoding="utf-8")
            env_map = load_env_map(str(path))
            test_env = get_environment(env_map, "test")
            self.assertEqual(test_env.disabled_components["longhorn"], "reason first")

    def test_empty_include_is_present_not_missing(self):
        text = '''
version: "0.2"
environments:
  test:
    type: k8s
    kubeconfig: "~/.kube/config-test"
    inspection:
      include: []
      exclude: []
'''
        with TemporaryDirectory() as td:
            path = Path(td) / "env-map.yaml"
            path.write_text(text, encoding="utf-8")
            env_map = load_env_map(str(path))
            test_env = get_environment(env_map, "test")
            self.assertTrue(test_env.has_inspection_include)
            self.assertEqual(test_env.inspection_include, [])
            self.assertEqual(test_env.inspection_exclude, [])

    def test_missing_include_is_not_present(self):
        text = '''
version: "0.2"
environments:
  test:
    type: k8s
    kubeconfig: "~/.kube/config-test"
'''
        with TemporaryDirectory() as td:
            path = Path(td) / "env-map.yaml"
            path.write_text(text, encoding="utf-8")
            env_map = load_env_map(str(path))
            test_env = get_environment(env_map, "test")
            self.assertFalse(test_env.has_inspection_include)
            self.assertEqual(test_env.inspection_include, [])

    def test_get_missing_environment_returns_none(self):
        with TemporaryDirectory() as td:
            path = Path(td) / "env-map.yaml"
            path.write_text(EXAMPLE, encoding="utf-8")
            env_map = load_env_map(str(path))
            self.assertIsNone(get_environment(env_map, "prod"))


if __name__ == "__main__":
    unittest.main()
