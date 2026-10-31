# Adoption evidence — 31 October 2026

## Scope

Private consumer: https://github.com/themasonbanks/agentic-harness-validation/pull/1
Generated using GitHub template mode from agentic-project-template. Application: dependency-free POSIX shell greeting command. No cloud resources, database, environment files or credentials were copied. Application files were prepared locally before repository creation.

## Results

- Local syntax and behavioural tests passed; deliberately wrong greeting failed; repair passed.
- Broken commit: cd20f94e4c53de07b76ebe672c6f8b717a27641b.
- Failing branch run: https://github.com/themasonbanks/agentic-harness-validation/actions/runs/41241882995
- Failing PR run: https://github.com/themasonbanks/agentic-harness-validation/actions/runs/41241886417
- Repaired commit: fc8fe12233c26085957a0556463384bbbea0f695.
- Passing branch run: https://github.com/themasonbanks/agentic-harness-validation/actions/runs/41241973611
- Passing PR run: https://github.com/themasonbanks/agentic-harness-validation/actions/runs/41241977713
- Shared workflow: agentic-platform at 85791b3f7e02156e480718756e33b2e28c4a7017.
- Independent read-only review: no blocking findings; guidance findings corrected on the template PR.

The failed log confirmed configured adapters ran and exited 1 on the application checks, rather than stopping at an unconfigured placeholder. Hosted check name: Project checks / Project checks.

## Timing and limitations

Repository created at 21:02:37 UTC; repaired PR run completed at 21:06:09 UTC: 3 minutes 32 seconds including CI queues and a template-generation history repair. This interval excludes preparing the sample locally, account permissions and preceding review work. Automated local copy/configuration/check execution took 0.13 seconds; that is not manual setup time. The under-30-minute result applies only to this prepared shell sample. Full-app/manual setup time is unmeasured.

GitHub template generation was asynchronous: an immediate clone saw the empty repository before its initial commit. Work was reapplied on a branch based on the finished generated main commit. Consumers should wait until the generated default branch is populated before cloning.

No deployment, merge or production change occurred. The validation repository's branch rules, Linear linking and CodeRabbit configuration were not acceptance-tested; Stockpot integration evidence is tracked separately in KEB-117. Full security scanning, action upgrades, hooks and comprehensive CI remain follow-on work.
