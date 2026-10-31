# Application infrastructure boundary

Placeholder only. No Terraform resources, state backend or deployment is provisioned.
KEB-124 defines encrypted versioned state, locking and restricted GitHub OIDC roles.
KEB-125 adds modules, separate dev/prod state, previews, teardown and human production approval.
Never copy state files, provider credentials or production secrets into a template.
