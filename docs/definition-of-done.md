# Delivery criteria

A project change is ready for review when its Linear acceptance criteria are implemented,
relevant automated tests pass, lint and all workspace type checks pass, and an independent
review has no unresolved blocking findings. Record any unavailable checks explicitly.

Where applicable, schema changes need migrations tested on a disposable local database,
authorisation coverage for permitted and denied access, and generated types matching
the migrated schema. Stockpot uses local Supabase for this. Never point destructive
test or reset commands at a shared or production database.

Mobile changes need light/dark, accessibility, and relevant native simulator/device
checks. Browser previews do not establish secure-storage or deep-link behaviour.

Use the PR template to connect implementation to issue criteria and document rollback.
Separate implemented, tested, reviewed, merged, and deployed states. Do not mark a
Linear issue Done while required evidence or integration remains outstanding.

The reusable CI job appears as Project checks / Project checks on hosted runs; verify
the exact status context on the adoption PR. Applications may add database jobs. Making
these mandatory for merging requires repository branch-protection configuration;
adding a workflow alone does not enforce that policy.
