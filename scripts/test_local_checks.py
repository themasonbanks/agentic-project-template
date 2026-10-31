from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def run(args, cwd, success=True):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if success != (result.returncode == 0):
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout + result.stderr


def main():
    adapter = ROOT / "adapters/pnpm-typescript"
    with tempfile.TemporaryDirectory(prefix="local-checks-") as directory:
        project = Path(directory)
        shutil.copytree(adapter, project, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("node_modules", "dist"))
        (project / "node_modules").symlink_to(adapter / "node_modules", target_is_directory=True)
        (project / "scripts").mkdir()
        shutil.copyfile(ROOT / "scripts/check_staged.py", project / "scripts/check_staged.py")
        shutil.copyfile(ROOT / "lefthook.yml", project / "lefthook.yml")
        run(["git", "init", "-b", "main"], project)
        run(["git", "config", "user.name", "Hook verification"], project)
        run(["git", "config", "user.email", "hooks@example.invalid"], project)
        run(["git", "add", "."], project)
        run(["git", "commit", "-m", "Initial fixture"], project)
        run(["pnpm", "exec", "prettier", ".", "--write"], project)
        run(["pnpm", "check"], project)
        run(["pnpm", "hooks:install"], project)
        source = project / "src/greet.ts"
        valid = source.read_text()
        source.write_text(valid + "const unused = 1;\n")
        run(["git", "add", "src/greet.ts"], project)
        source.write_text(valid)
        rejected = run(["git", "commit", "-m", "Invalid staged lint"], project, False)
        assert "no-unused-vars" in rejected, rejected
        assert source.read_text() == valid
        assert "unused" in run(["git", "show", ":src/greet.ts"], project)
        source.write_text(valid)
        run(["git", "add", "src/greet.ts"], project)
        spaced = project / "src/name with spaces.ts"
        spaced.write_text(valid)
        run(["git", "add", str(spaced.relative_to(project))], project)
        spaced.write_text(valid + "const unstaged = 1;\n")
        run(["git", "commit", "-m", "Valid staged content"], project)
        assert "unstaged" in spaced.read_text()
        spaced.write_text(valid)
        source.write_text(valid.replace("Hello,", "Wrong,"))
        regression = run(["pnpm", "check"], project, False)
        assert "<failure" in (project / "test-results/unit.xml").read_text(), regression
        source.write_text(valid)
        run(["pnpm", "check"], project)
        print("PASS: real Lefthook commit rejection, staged-only content, spaces, preserved edits, full-check test regression and repair")


if __name__ == "__main__":
    main()
