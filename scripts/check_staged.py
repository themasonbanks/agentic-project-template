import os
from pathlib import Path
import subprocess
import sys


def git(*args):
    return subprocess.check_output(["git", *args])


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("pnpm", "bun", "shell"):
        raise SystemExit("Usage: check_staged.py pnpm|bun|shell")
    adapter = sys.argv[1]
    os.chdir(os.fsdecode(git("rev-parse", "--show-toplevel").strip()))
    paths = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
    for raw in filter(None, paths.split(b"\0")):
        path = os.fsdecode(raw)
        suffix = Path(path).suffix.lower()
        commands = []
        code = suffix in (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts")
        data = suffix in (".json", ".jsonc", ".css", ".md", ".yml", ".yaml")
        if adapter == "pnpm":
            if code or data:
                commands.append(["pnpm", "exec", "prettier", "--check", "--stdin-filepath", path])
            if code:
                commands.append(["pnpm", "exec", "eslint", "--max-warnings=0", "--stdin", "--stdin-filename", path])
        elif adapter == "bun" and (code or suffix in (".json", ".jsonc", ".css")):
            commands.append(["./node_modules/.bin/biome", "check", "--stdin-file-path=" + path])
        elif adapter == "shell" and suffix == ".sh":
            commands.append(["sh", "-n"])
        if commands:
            mode = git("ls-files", "--stage", "--", path).split(b" ", 1)[0]
            if mode not in (b"100644", b"100755"):
                raise SystemExit("Unsupported staged file mode: " + path)
            content = git("show", ":" + path)
            for command in commands:
                print("Checking staged " + path, flush=True)
                subprocess.run(command, input=content, check=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
