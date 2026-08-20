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
    inspection:
      include:
        - k8s_nodes_ready
        - pod_abnormal
  test:
    type: k8s
    kubeconfig: "~/.kube/config-test"
    inspection:
      include:
        - warning_events
        - pvc_status
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

    def test_get_missing_environment_returns_none(self):
        with TemporaryDirectory() as td:
            path = Path(td) / "env-map.yaml"
            path.write_text(EXAMPLE, encoding="utf-8")
            env_map = load_env_map(str(path))
            self.assertIsNone(get_environment(env_map, "prod"))


if __name__ == "__main__":
    unittest.main()
