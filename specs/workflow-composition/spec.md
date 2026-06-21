# Workflow Composition Spec

## Purpose

Workflow recipes compose existing skills into reusable paths without duplicating skill instructions or replacing DevFlow governance.

## Format

Workflow files live under `workflows/*.yaml` and use JSON-compatible YAML so the standard library can parse them.

Required fields:

- `name`: unique slug matching the file name.
- `version`: positive integer.
- `level`: `L0`, `L1`, `L2`, or `L3`.
- `description`: concise workflow purpose.
- `skills`: ordered list of existing skill names.
- `required_capabilities`: capability names from `capabilities/providers.yaml`.
- `outputs`: observable workflow outputs.
- `next_workflows`: valid workflow names suggested after completion.

## Rules

- Recipes contain orchestration metadata only; skill behavior remains in `skills/*/SKILL.md`.
- Recipes do not bypass `entry-router`, review gates, or `change-id` requirements.
- `L2/L3` recipes use repository-backed change artifacts.
- Suggested next workflows are advisory and must be re-routed for the current request.

## Validation

Run `python scripts/devflow.py validate-workflow --all` before delivery when workflow files change.
