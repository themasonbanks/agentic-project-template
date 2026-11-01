from pathlib import Path
import json
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class RunnerTests(unittest.TestCase):
    def exercise(self, event="push", failure=None):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            scripts = project / "scripts"
            scripts.mkdir()
            shutil.copyfile(ROOT / "scripts/run_ci.py", scripts / "run_ci.py")
            for name in ("setup.sh", "check.sh", "check-integration.sh", "check-e2e.sh"):
                status = 7 if name == failure else 0
                (scripts / name).write_text("exit " + str(status) + "\n")
            env = dict(os.environ, GITHUB_EVENT_NAME=event)
            result = subprocess.run(["python3", str(scripts / "run_ci.py")], cwd=ROOT, env=env)
            report = json.loads((project / "test-results/ci-summary.json").read_text())
            return result.returncode, report

    def test_push_runs_integration_but_not_e2e(self):
        code, report = self.exercise()
        self.assertEqual(code, 0)
        self.assertTrue(report["success"])
        self.assertEqual([item["stage"] for item in report["completed_stages"]],
                         ["setup.sh", "check.sh", "check-integration.sh"])

    def test_pr_runs_e2e(self):
        code, report = self.exercise("pull_request")
        self.assertEqual(code, 0)
        self.assertEqual(report["completed_stages"][-1]["stage"], "check-e2e.sh")

    def test_each_stage_failure_stops_and_remains_reported(self):
        for failure in ("setup.sh", "check.sh", "check-integration.sh", "check-e2e.sh"):
            with self.subTest(failure=failure):
                code, report = self.exercise("pull_request", failure)
                self.assertEqual(code, 7)
                self.assertFalse(report["success"])
                self.assertEqual(report["completed_stages"][-1]["stage"], failure)
                self.assertEqual(report["completed_stages"][-1]["exit_code"], 7)


if __name__ == "__main__":
    unittest.main()
