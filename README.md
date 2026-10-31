# Agentic project template

A language-neutral starting point for independently managed application repositories.
Status: published private scaffold for KEB-118; hosted adoption is verified for a prepared POSIX shell sample; see docs/adoption-evidence.md for timing and limitations.

## Adopt (target: under 30 minutes)

1. Use GitHub’s Use this template → Create a new repository. Wait until the generated default branch contains its initial commit before cloning. For a local copy, copy tracked files only; exclude .git, local environment files and credentials.
2. Record the runtime, pinned tool versions, lockfile and architecture in docs/architecture.md.
3. Replace scripts/setup.sh and scripts/check.sh with actual project commands. Setup must install pinned tools and frozen dependencies; checks must validate formatting, lint, types, tests and build where applicable. Document exclusions with reasons.
4. Run sh scripts/ci.sh. It deliberately fails until both adapters are configured.
5. Commit a small change and verify CI runs on a branch push and a PR. Break a real check, confirm failure, repair it and confirm success.
6. Have the owner approve GitHub/Linear/CodeRabbit access and enforce required checks with no bot bypass. Use the exact check name shown on the PR (currently Project checks / Project checks). For solo authors, require PRs and manual human merge but zero approving reviews: authors cannot approve their own PRs. Independent approval needs a second eligible human. Required checks alone do not enforce human-only merging; bot permissions must match that policy. Confirm enforcement on the repository plan.
7. Record elapsed setup time and evidence in docs/adoption-evidence.md.

No database, Docker, cloud resources or application dependencies are installed by this template.
For Stockpot retain Bun, Biome, Turbo and its separate disposable Supabase job; do not replace them with pnpm or an empty generic check.

## Commands

- sh scripts/check.sh: local project checks after dependencies are installed.
- sh scripts/ci.sh: setup followed by project checks in a fresh hosted environment.

The included CI calls the shared platform workflow pinned to a commit SHA; it runs checks from this repository. Owner-scoped private workflow access is enabled. See docs/architecture.md.

## Follow-on work

KEB-119: fast hooks and adapters. KEB-120: complete hosted CI and failure evidence.
KEB-121: security scanners and action pin maintenance. KEB-127: CodeRabbit review tuning.
KEB-124/125: AWS/OIDC/Terraform and deployment. These are not implemented here.

## Template repository CI

This source repository runs Template validation: shell/YAML syntax, rejection of unconfigured application adapters, and runner success/error propagation. Run it locally with `python3 scripts/validate_template.py` and parse configuration YAML with Ruby's standard YAML library.

Repository identity selects the job in .github/workflows/ci.yml. Every generated or forked application has a different repository name and runs the shared Project checks job instead. An unconfigured application still fails. If you rename or transfer the source template, update both repository comparisons. Application owners may remove the template-only job and validator during adoption.
