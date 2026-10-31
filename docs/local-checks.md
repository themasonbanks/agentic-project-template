# Local checks and commit hooks

## pnpm / TypeScript

Use the files under adapters/pnpm-typescript as a starting application, or merge the scripts/configuration into an existing pnpm project. Do not overwrite an existing manifest, lockfile or lint rules. The supplied fixture pins its dependencies and pnpm 12.16.1; verification uses Node 26.13.0. Node's built-in test runner imports TypeScript with erasable syntax; projects using enums or transformed syntax should use their existing test runner instead.

At the application root, retain scripts/check_staged.py and lefthook.yml. Copy adapter files including .gitignore, .prettierignore, pnpm-workspace.yaml and pnpm-lock.yaml, then run:

```sh
pnpm install --frozen-lockfile
pnpm check
pnpm hooks:install
```

Activation is per clone, after reviewing the configuration and existing hooks. Inspect `git config --get core.hooksPath` and .git/hooks before installing; reconcile existing hooks rather than overwriting them. Lefthook dependency builds are explicitly disabled in pnpm-workspace.yaml to avoid automatic hook installation. The optional platform binary supplies the executable; activation remains explicit.

`pnpm check` runs format validation, ESLint, TypeScript, unit tests and build sequentially. A failed step stops execution. It excludes E2E and external database services. For hosted checks, configure scripts/setup.sh to install the pinned runtime/pnpm and run frozen dependency installation, and scripts/check.sh to run `pnpm check`.

The pre-commit hook checks indexed file contents through stdin, not the working file. Prettier and ESLint validate JS/TS; Prettier also validates JSON, JSONC, CSS, Markdown and YAML. Deleted files and unsupported extensions are skipped. Lint configuration/plugins come from the working tree; this is not a complete staged filesystem snapshot. Review configuration changes alongside code. Files are not formatted, staged, stashed or rewritten automatically. Format/fix manually and stage the intended changes before retrying. Each staged file invokes its tools separately; benchmark large commits before expanding scope.

## Existing Bun / Biome projects

Keep Bun, Biome and the existing lockfile. Change the lefthook command to `python3 scripts/check_staged.py bun`. It invokes the already installed ./node_modules/.bin/biome for staged JS/TS, JSON/JSONC and CSS; it never installs tools. Install Lefthook as an exact dev dependency using the project's existing package manager, then explicitly run its install command.

For Stockpot a full check should combine its existing format:check, lint, typecheck and unit scripts using Bun. Build only applications with a defined, appropriate build task. Keep disposable Supabase and native device checks separate. Stockpot itself has not been changed by this template task; the Bun/Biome adapter needs validation there before adoption.

## Non-Node fallback

Python 3 and Git are sufficient for `python3 scripts/check_staged.py shell`, which checks indexed .sh files with POSIX `sh -n`. It is syntax validation, not ShellCheck or a substitute for behavioural tests. Configure scripts/check.sh with the language's full tests/builds.

If Lefthook is unavailable, create an executable local .git/hooks/pre-commit (or integrate into an existing hook) containing:

```sh
#!/bin/sh
exec python3 scripts/check_staged.py shell
```

Check core.hooksPath first; its directory takes precedence over .git/hooks. Do not overwrite existing hooks. If no hook manager/interpreter can run, invoke the staged checker manually and rely on required hosted checks until local tools are available; report that hooks are inactive.

## Limits and verification

Hooks are local feedback, not security enforcement. They can be bypassed or absent in another clone; required hosted checks must rerun the full checks. Do not grant a bot merge permission based on a hook result.

Source-template maintainers run `python3 scripts/test_local_checks.py` after installing the adapter's frozen dependencies. The disposable Git fixture installs the actual Lefthook hook, rejects invalid staged lint, preserves valid/invalid partial staging and spaces, and demonstrates full-check test failure and repair. The source workflow repeats it on hosted Ubuntu.

Sources: https://lefthook.dev/configuration/run/ ; https://prettier.io/docs/cli ; https://eslint.org/docs/latest/use/command-line-interface ; https://pnpm.io/settings/build
