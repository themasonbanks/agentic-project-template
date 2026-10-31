# Agentic project template

A language-neutral starting point for independently managed application repositories.
Status: local scaffold for KEB-118; not yet published or proven by adoption.

## Adopt (target: under 30 minutes)

1. Copy this directory into a new application repository without copying credentials.
2. Record the runtime, pinned tool versions, lockfile and architecture in docs/architecture.md.
3. Replace scripts/setup.sh and scripts/check.sh with actual project commands. Setup must install pinned tools and frozen dependencies; checks must validate formatting, lint, types, tests and build where applicable. Document exclusions with reasons.
4. Run sh scripts/ci.sh. It deliberately fails until both adapters are configured.
5. Commit a small change and verify CI runs on a branch push and a PR. Break a real check, confirm failure, repair it and confirm success.
6. Have the owner install GitHub/Linear/CodeRabbit integrations for this repository and configure required checks, human review and no bot bypass. Confirm enforcement on the repository plan.
7. Record elapsed setup time and evidence in docs/adoption-evidence.md.

No database, Docker, cloud resources or application dependencies are installed by this template.
For Stockpot retain Bun, Biome, Turbo and its separate disposable Supabase job; do not replace them with pnpm or an empty generic check.

## Commands

- sh scripts/check.sh: local project checks after dependencies are installed.
- sh scripts/ci.sh: setup followed by project checks in a fresh hosted environment.

The included CI runs checks from this repository. After the shared platform is published and validated, it can call the platform reusable workflow pinned to a reviewed commit SHA. See docs/architecture.md.

## Follow-on work

KEB-119: fast hooks and adapters. KEB-120: complete hosted CI and failure evidence.
KEB-121: security scanners and action pin maintenance. KEB-127: CodeRabbit review tuning.
KEB-124/125: AWS/OIDC/Terraform and deployment. These are not implemented here.
