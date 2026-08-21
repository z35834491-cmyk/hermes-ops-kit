import unittest

from scripts.checkers import k8s


class K8sCheckerTests(unittest.TestCase):
    def test_plan_mode_does_not_execute(self):
        calls = []
        result = k8s.run(
            "k8s_nodes_ready",
            "test",
            {"kubeconfig": "example-kubeconfig"},
            {"title": "K8s nodes readiness"},
            execute=False,
            runner=lambda *_: calls.append("called"),
        )
        self.assertEqual(result.status, "skipped")
        self.assertEqual(calls, [])
        self.assertIn("plan-only", result.evidence)

    def test_execute_without_runner_does_not_call_cluster(self):
        result = k8s.run(
            "k8s_nodes_ready",
            "test",
            {"kubeconfig": "example-kubeconfig"},
            {"title": "K8s nodes readiness"},
            execute=True,
        )
        self.assertEqual(result.status, "skipped")
        self.assertIn("does not execute kubectl", result.evidence)

    def test_nodes_ready_parses_kubectl_output(self):
        def runner(cmd, timeout=30):
            return "node-a Ready\nnode-b NotReady\n"

        result = k8s.run(
            "k8s_nodes_ready",
            "test",
            {"kubeconfig": "example-kubeconfig"},
            {"title": "K8s nodes readiness"},
            execute=True,
            runner=runner,
        )
        self.assertEqual(result.status, "warning")
        self.assertIn("1/2 Ready", result.evidence)
        self.assertIn("node-b", result.evidence)

    def test_pod_abnormal_detects_not_ready_pod(self):
        def runner(cmd, timeout=30):
            return "ns-a pod-ok 1/1 Running 0\nns-a pod-bad 0/1 Running 3\nns-b job-x 0/1 Completed 0\n"

        result = k8s.run(
            "pod_abnormal",
            "test",
            {"kubeconfig": "example-kubeconfig"},
            {"title": "Abnormal pods"},
            execute=True,
            runner=runner,
        )
        self.assertEqual(result.status, "warning")
        self.assertIn("pod-bad", result.evidence)
        self.assertNotIn("job-x", result.evidence)

    def test_warning_events_detects_recent_warnings(self):
        def runner(cmd, timeout=30):
            return "ns-a 10m Warning FailedScheduling pod-a 0/3 nodes are available\nns-b 2m Normal Pulled pod-b image pulled\n"

        result = k8s.run(
            "warning_events",
            "test",
            {"kubeconfig": "example-kubeconfig"},
            {"title": "Warning events"},
            execute=True,
            runner=runner,
        )
        self.assertEqual(result.status, "warning")
        self.assertIn("FailedScheduling", result.evidence)
        self.assertNotIn("Pulled", result.evidence)

    def test_pvc_status_detects_non_bound_pvc(self):
        def runner(cmd, timeout=30):
            return "ns-a data-a Bound pvc-1 10Gi RWO standard 1d\nns-b data-b Pending pvc-2 20Gi RWO standard 1h\n"

        result = k8s.run(
            "pvc_status",
            "test",
            {"kubeconfig": "example-kubeconfig"},
            {"title": "PVC status"},
            execute=True,
            runner=runner,
        )
        self.assertEqual(result.status, "warning")
        self.assertIn("data-b", result.evidence)
        self.assertNotIn("data-a Bound", result.evidence)

    def test_high_restart_detects_pods_above_threshold(self):
        def runner(cmd, timeout=30):
            return "ns-a pod-ok 1/1 Running 2\nns-a pod-hot 1/1 Running 12\nns-b pod-bad 0/1 CrashLoopBackOff 20\n"

        result = k8s.run(
            "high_restart",
            "test",
            {"kubeconfig": "example-kubeconfig"},
            {"title": "High restart pods", "threshold": "10"},
            execute=True,
            runner=runner,
        )
        self.assertEqual(result.status, "warning")
        self.assertIn("pod-hot", result.evidence)
        self.assertIn("pod-bad", result.evidence)
        self.assertNotIn("pod-ok", result.evidence)

    def test_node_resource_top_detects_high_memory(self):
        def runner(cmd, timeout=30):
            return "node-a 100m 5% 1000Mi 40%\nnode-b 900m 50% 7000Mi 91%\n"

        result = k8s.run(
            "node_resource_top",
            "test",
            {"kubeconfig": "example-kubeconfig"},
            {"title": "Node resource top", "memory_threshold_percent": "85"},
            execute=True,
            runner=runner,
        )
        self.assertEqual(result.status, "warning")
        self.assertIn("node-b", result.evidence)
        self.assertIn("91%", result.evidence)

    def test_argocd_sync_detects_out_of_sync_apps(self):
        def runner(cmd, timeout=30):
            return "argocd app-a Synced Healthy\nargocd app-b OutOfSync Degraded\n"

        result = k8s.run(
            "argocd_sync",
            "test",
            {"kubeconfig": "example-kubeconfig"},
            {"title": "ArgoCD sync"},
            execute=True,
            runner=runner,
        )
        self.assertEqual(result.status, "warning")
        self.assertIn("app-b", result.evidence)
        self.assertNotIn("app-a Synced", result.evidence)

    def test_longhorn_health_detects_unhealthy_volumes(self):
        def runner(cmd, timeout=30):
            return "vol-a healthy attached\nvol-b degraded attached\n"

        result = k8s.run(
            "longhorn_health",
            "test",
            {"kubeconfig": "example-kubeconfig"},
            {"title": "Longhorn health"},
            execute=True,
            runner=runner,
        )
        self.assertEqual(result.status, "warning")
        self.assertIn("vol-b", result.evidence)
        self.assertNotIn("vol-a healthy", result.evidence)


if __name__ == "__main__":
    unittest.main()
