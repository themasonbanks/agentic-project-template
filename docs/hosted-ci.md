# Hosted checks

Both branch pushes and pull requests run on hosted Ubuntu. The workflow groups runs by workflow, event type, source repository and branch, cancelling older work within that group. Push and PR runs are separate because PRs can have extra E2E coverage; a push must never cancel that coverage. Full local/unit checks may run for both events; expensive browser tests run only for PRs. Fork branches with the same name use different source repository keys.

## Stable required check

Require the `CI` status in an active default-branch ruleset with no bot bypass. It succeeds only when the selected source-template or application job succeeds; a skipped, failed or cancelled selected job fails the overall result. App job skips in the source repository and template job skips in consumers are expected. Use `CI`, not an optional job name, as the required check.

The platform, template and validation repositories are now public with active main rulesets requiring CI, up-to-date PRs and no bypass. A failing validation PR was confirmed BLOCKED, then CLEAN after repair. Private adopters still need a plan that supports protected branches; do not treat a passing workflow as branch protection.

## Application contract

Copy scripts/run_ci.py when upgrading to the new pinned shared workflow. It requires Python 3 on the hosted runner, executes setup.sh then check.sh, and records duration/status in test-results/ci-summary.json. Setup installs the project's pinned runtime/package manager and uses the committed lockfile with frozen installation. check.sh runs formatting, lint, types, unit tests and build where applicable. The pnpm TypeScript adapter emits JUnit and LCOV reports from its unit tests. Preserve Bun and its lockfile in existing Bun projects.

Optional scripts/check-integration.sh runs after application checks. Optional scripts/check-e2e.sh runs only on pull_request events, after integration checks. Projects with browser UI should install pinned Playwright dependencies in setup, start their preview/test server with readiness checks, write traces/reports to test-results or playwright-report and clean up services on exit. No browser UI exists in the shell/TypeScript fixtures, so Playwright is not installed or claimed as tested here. Schema and native-mobile checks remain application-specific.

Existing consumers remain pinned to their older workflow. Upgrading requires both the reviewed platform commit SHA and scripts/run_ci.py; do not silently update one without the other.

## Artifacts and permissions

The reusable job uploads only test-results, coverage and playwright-report directories, including on failure but not cancellation. Reports are retained for seven days; hidden files are excluded. Redact reports and traces before writing them: these directories must not contain tokens, personal data, environment dumps, full prompts or source archives. The summary records stage names, timings and exit codes, not command output. In the source template, the TypeScript fixture's JUnit/LCOV files are uploaded separately.

Quality jobs have read-only contents permission, no persisted checkout credentials, no inherited secrets, no deployment environment, no OIDC write permission and no personal-Mac runner. Deployment credentials belong in separate, human-approved workflows; never use pull_request_target to execute untrusted PR code with secrets.

## Verification

Run python3 scripts/test_ci_runner.py locally to verify failure reporting, execution order and optional-stage gating. CI also runs the existing real-hook acceptance tests and template checks. Hosted acceptance must demonstrate broken/repair status and downloadable reports. Required-before-merge enforcement was verified on the public validation repository; new adopters must configure and verify their own rules.
