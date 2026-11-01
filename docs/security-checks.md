# Security checks

The required CI result includes the reusable Security job. Secret scanning checks fetched Git history with Gitleaks 8.30.1 and full redaction. Trivy 0.76.1 scans lockfiles including development dependencies and infrastructure, failing on HIGH/CRITICAL findings. CodeQL security-extended queries cover tracked JavaScript/TypeScript and Python sources; its SARIF gate fails at security-severity 7 or above. Supported language detection is explicit; shell-only and workflow-only repositories have no CodeQL source-language scan. Known additional source languages (Go, Ruby, Java/Kotlin, C/C++, C#, Swift and Rust) fail language detection with an adapter-required message rather than passing silently. Add and verify the relevant build/language adapter before adopting them.

Tool releases are version-pinned and checked against official SHA-256 release manifests before extraction. Workflow actions use full commit SHAs. Dependabot checks Actions weekly and the template TypeScript adapter's npm/pnpm dependencies weekly. Consumers must point the npm directory at their actual application manifest; retain Bun and the existing lockfile in Bun projects.

Scanners do not execute Terraform or install vulnerable packages. No Terraform or image resources currently exist in the scaffold; Trivy infrastructure coverage activates when relevant files are present. For built container images, add a separate image scan of an immutable image digest before deployment; filesystem scanning is not proof that an image was scanned.

## Verification

With the pinned scanners on PATH, run python3 scripts/test_security_scanners.py SANITIZER_SCRIPT, using the sanitizer prepared by the reusable workflow. It generates a random AWS-shaped synthetic string, an old dependency manifest and a public-SSH Terraform example in a temporary folder, verifies detection/nonzero exit status, repairs/removes each example and verifies clean scans. No working credential is used or committed, the vulnerable package is not installed, and Terraform is not applied. The fixture also repeats the synthetic string in a Git commit message and verifies that the published allowlisted report omits it and the author email. The source-template security job repeats these acceptance checks.

Security reports are retained seven days. Raw reports remain in runner temporary storage and are not uploaded. Published Gitleaks reports contain only rule ID, path/lines and commit SHA. Published Trivy reports contain only targets/types, finding IDs, package versions, severity and status; messages, source snippets and author/email metadata are excluded. Never put credentials or personal data in report directories. Tool/database/network failures block the workflow; absence of findings is not proof of complete security.

## Triage and exceptions

For each finding confirm the affected version/resource/path and current code, then fix it and rerun. Do not silence a whole rule or scanner because a fixture failed. A false positive or accepted risk requires a human-reviewed PR recording the exact finding ID/fingerprint and scope, evidence, owner, reason, expiry date and tracking issue. Never allowlist a real leaked credential: revoke/rotate it and follow incident handling; deleting it from the latest commit does not remove it from history.

For Trivy use a narrowly scoped .trivyignore.yaml entry with statement and expired_at, reviewed alongside the exception record. For Gitleaks use an exact fingerprint in .gitleaksignore with a matching dated exception record. Reviewers must reject expired exceptions; the scanner formats differ and Gitleaks fingerprints do not enforce expiry automatically. CodeQL high-severity findings require repair or a separately reviewed change to the precise gate policy; dismissing a UI alert alone does not bypass the SARIF gate. No blanket exception is enabled by this template.

Public PRs are untrusted. Scanners run on hosted Ubuntu with read-only contents access and no inherited credentials. Only the CodeQL job receives security-events write permission to publish findings. No OIDC, deployment environment or self-hosted Mac runner is used. Review changes to workflow/scanner configuration as carefully as application code; local hooks are not enforcement.

CodeQL is enabled here because these platform repositories are public. Private consumers must verify GitHub Code Security entitlement before adopting this workflow; missing entitlement blocks the job rather than silently reporting coverage. Do not claim private CodeQL coverage without a successful analysis.
