# Prioritize

- Create an ADR on generate, deploy and destroy workflow user experience.
- Github `destroy` workflow is slimmed down. Logic lives `_services/` directory with a single entry points for steps. This should be blocked by ADR on deploy / destroy workflows.
- Generate scripts run on local. Update documentation. Remove workflow
- `ansible-lint` is a workflow on PRs with config
- Fix label script for workflows

  
**Search codebase for `TODO: COOL:` for inline tags.**


# Complete

- Workflows do not checkout branch that they are not on.
- Github `deploy` workflow is slimmed down. Logic lives `_services/` directory with a single entry points for steps.
- Create generate workflow for Phish.
- Create deploy workflow for Phish.

