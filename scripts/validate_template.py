from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class TemplateChecks(unittest.TestCase):
    def test_shell_syntax(self):
        for script in (ROOT / "scripts").glob("*.sh"):
            with self.subTest(script=script.name):
                subprocess.run(["sh", "-n", str(script)], check=True)

    def test_unconfigured_application_fails(self):
        for name in ("setup.sh", "check.sh", "ci.sh"):
            with self.subTest(script=name):
                result = subprocess.run(
                    ["sh", str(ROOT / "scripts" / name)],
                    cwd=ROOT, capture_output=True, text=True,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Configure scripts/", result.stderr)

    def test_configured_runner_preserves_order_and_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            scripts = project / "scripts"
            scripts.mkdir()
            shutil.copyfile(ROOT / "scripts/ci.sh", scripts / "ci.sh")
            (scripts / "setup.sh").write_text(
                "set -eu\nprintf 'setup\\n' >> sequence\n"
            )
            (scripts / "check.sh").write_text(
                "set -eu\nprintf 'check\\n' >> sequence\n"
            )
            subprocess.run(["sh", str(scripts / "ci.sh")], cwd=ROOT, check=True)
            self.assertEqual((project / "sequence").read_text(), "setup\ncheck\n")
            (project / "sequence").unlink()
            (scripts / "setup.sh").write_text("exit 7\n")
            failed = subprocess.run(["sh", str(scripts / "ci.sh")], cwd=ROOT)
            self.assertEqual(failed.returncode, 7)
            self.assertFalse((project / "sequence").exists())
            (scripts / "setup.sh").write_text("exit 0\n")
            (scripts / "check.sh").write_text("exit 9\n")
            failed = subprocess.run(["sh", str(scripts / "ci.sh")], cwd=ROOT)
            self.assertEqual(failed.returncode, 9)


if __name__ == "__main__":
    unittest.main()
