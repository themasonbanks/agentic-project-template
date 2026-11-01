from pathlib import Path
import json
import os
import subprocess
import sys
import time


def main():
    root = Path(__file__).resolve().parent.parent
    os.chdir(root)
    stages = ["setup.sh", "check.sh"]
    if (root / "scripts/check-integration.sh").is_file():
        stages.append("check-integration.sh")
    if os.environ.get("GITHUB_EVENT_NAME") == "pull_request" and (root / "scripts/check-e2e.sh").is_file():
        stages.append("check-e2e.sh")
    results = []
    exit_code = 0
    for stage in stages:
        started = time.monotonic()
        result = subprocess.run(["sh", "scripts/" + stage])
        results.append({"stage": stage, "exit_code": result.returncode,
                        "duration_seconds": round(time.monotonic() - started, 3)})
        if result.returncode:
            exit_code = result.returncode if result.returncode > 0 else 1
            break
    reports = root / "test-results"
    reports.mkdir(exist_ok=True)
    (reports / "ci-summary.json").write_text(json.dumps({
        "schema_version": 1, "success": exit_code == 0,
        "expected_stages": stages, "completed_stages": results,
    }, indent=2) + "\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
