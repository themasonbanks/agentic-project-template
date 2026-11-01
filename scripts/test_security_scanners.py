from pathlib import Path
import json
import secrets
import string
import subprocess
import tempfile
import sys


def scan(command, report, expected):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != expected:
        raise AssertionError("Scanner returned unexpected status: " + str(result.returncode) + " " + result.stderr[-1500:])
    return json.loads(report.read_text())


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: test_security_scanners.py SANITIZER_SCRIPT")
    with tempfile.TemporaryDirectory(prefix="scanner-verification-") as directory:
        root = Path(directory)
        sample = root / "sample"
        sample.mkdir()
        report = root / "report.json"
        fake = "AKIA" + "".join(secrets.SystemRandom().sample(string.ascii_uppercase + "234567", 16))
        key = sample / "example.txt"
        key.write_text('aws_access_key_id = "' + fake + '"\n')
        command = ["gitleaks", "dir", str(sample), "--redact", "--report-format", "json", "--report-path", str(report), "--no-banner"]
        findings = scan(command, report, 1)
        assert any(item["RuleID"] == "aws-access-token" for item in findings)
        assert fake not in report.read_text()
        subprocess.run(["git", "init", "-b", "main"], cwd=sample, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Scanner fixture"], cwd=sample, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=sample, check=True)
        subprocess.run(["git", "add", "."], cwd=sample, check=True)
        subprocess.run(["git", "commit", "-m", "Synthetic fixture " + fake], cwd=sample, check=True, capture_output=True)
        history = root / "gitleaks-raw.json"
        scan(["gitleaks", "git", str(sample), "--redact", "--report-format", "json", "--report-path", str(history), "--no-banner"], history, 1)
        published = root / "published"
        subprocess.run(["python3", sys.argv[1], str(root), str(published)], check=True)
        public_report = (published / "gitleaks.json").read_text()
        assert fake not in public_report
        assert "fixture@example.invalid" not in public_report
        assert all(set(item) <= {"RuleID", "File", "StartLine", "EndLine", "Commit"} for item in json.loads(public_report))
        key.write_text("No credentials are present.\n")
        scan(command, report, 0)
        requirements = sample / "requirements.txt"
        requirements.write_text("Django==1.2\n")
        command = ["trivy", "fs", "--scanners", "vuln", "--include-dev-deps", "--severity", "HIGH,CRITICAL", "--exit-code", "1", "--format", "json", "--output", str(report), str(sample)]
        findings = scan(command, report, 1)
        assert any(v["PkgName"].lower() == "django" for result in findings.get("Results", []) for v in result.get("Vulnerabilities", []))
        requirements.unlink()
        scan(command, report, 0)
        terraform = sample / "main.tf"
        terraform.write_text('resource "aws_security_group" "example" {\n  name = "example"\n  ingress {\n    from_port = 22\n    to_port = 22\n    protocol = "tcp"\n    cidr_blocks = ["0.0.0.0/0"]\n  }\n}\n')
        command = ["trivy", "fs", "--scanners", "misconfig", "--severity", "HIGH,CRITICAL", "--exit-code", "1", "--format", "json", "--output", str(report), str(sample)]
        findings = scan(command, report, 1)
        assert any(v.get("Status") == "FAIL" for result in findings.get("Results", []) for v in result.get("Misconfigurations", []))
        terraform.unlink()
        scan(command, report, 0)
        print("PASS: synthetic secret, vulnerable dependency and public SSH rule detected; clean repairs pass")


if __name__ == "__main__":
    main()
