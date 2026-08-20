import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.lib.check_catalog import get_check, load_check_catalog


CATALOG = '''
version: "0.1"

checks:
  k8s_nodes_ready:
    component: k8s
    risk_level: L0
    mode: read-only
    requires_approval: false
    checker: k8s
    title: K8s nodes readiness
  high_restart:
    component: k8s
    risk_level: L0
    mode: read-only
    requires_approval: false
    checker: k8s
    title: High restart pods
    threshold: 10
'''


class CheckCatalogLoaderTests(unittest.TestCase):
    def test_load_check_catalog(self):
        with TemporaryDirectory() as td:
            path = Path(td) / "check-catalog.yaml"
            path.write_text(CATALOG, encoding="utf-8")
            catalog = load_check_catalog(str(path))
            self.assertEqual(sorted(catalog.checks.keys()), ["high_restart", "k8s_nodes_ready"])
            self.assertEqual(catalog.checks["k8s_nodes_ready"].checker, "k8s")
            self.assertEqual(catalog.checks["high_restart"].settings["threshold"], "10")

    def test_get_missing_check_returns_none(self):
        with TemporaryDirectory() as td:
            path = Path(td) / "check-catalog.yaml"
            path.write_text(CATALOG, encoding="utf-8")
            catalog = load_check_catalog(str(path))
            self.assertIsNone(get_check(catalog, "missing"))


if __name__ == "__main__":
    unittest.main()
