# Project architecture

Complete before adoption:

- Product boundary and Linear project:
- Runtime/tool versions and package manager:
- Source layout and domain invariants:
- Setup/check/build commands and justified exclusions:
- Required CI status names and owner:
- Data classification, secret references and disposable test services:
- Deployment target, approval and rollback owner:

## Shared platform interface

The platform workflow checks out the calling application, then invokes sh scripts/ci.sh.
That script installs the application's tools/dependencies and runs its checks.
Keep credentialed deployments in separate approved jobs. Do not pass secrets to quality checks.
Pin cross-repository reusable workflow references to a reviewed platform commit SHA:
OWNER/agentic-platform/.github/workflows/project-checks.yml@FULL_COMMIT_SHA.
Verify private repository Actions access before adoption.

References:
https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
https://docs.coderabbit.ai/reference/configuration

## Review and merge ownership

For a solo author, require a PR and passing checks, then manually review and merge.
Required approving reviews remain zero because authors cannot approve their own PRs.
To enforce independent human approval, add another eligible reviewer and require their approval.
An empty bypass list prevents bypass of required checks; it does not prevent a bot
with sufficient repository permissions from merging a passing PR.
