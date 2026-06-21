# Design

- change-id: 20260621-workflow-capability-layer
- status: Planned
- proposal: ./proposal.md

## Summary

Add a declarative workflow and capability layer below `entry-router` and above concrete tools. Workflows compose existing skills; capabilities select ordered providers through read-only probes.

## Options

### Option A

- approach: JSON-compatible YAML registries plus additive DevFlow CLI commands.
- cost: small, no new runtime dependency.
- risk: intentionally limited probe and workflow semantics.

### Option B

- approach: install external plugin managers and capability runtimes directly.
- cost: high operational and security overhead.
- risk: couples core governance to fast-changing third-party tools.

## Recommended Option

Option A. It preserves the current governance model and creates stable extension points for later CodeGraph, Agent-Reach, or Headroom adapters.

## Object Model / Interfaces

- Workflow: `name`, `version`, `level`, `description`, `skills`, `outputs`, `required_capabilities`, `next_workflows`.
- Capability: name mapped to ordered provider objects.
- Provider: `name`, `probe`, optional `command`, `path`, `args`, and `description`.
- `validate-workflow`: structural and cross-reference validation.
- `doctor-capabilities`: reports all provider probes and selected provider.
- `resolve-capability`: emits one selected provider for agent/router consumption.

## Affected Files / Modules

- `workflows/*.yaml`
- `capabilities/providers.yaml`
- `skills/capability-router/SKILL.md`
- `skills/entry-router/SKILL.md`
- `skills.packages.json`
- `specs/workflow-composition/spec.md`
- `specs/capability-routing/spec.md`
- `scripts/devflow.py`
- `tests/test_devflow_workflow_capabilities.py`
- `README.md` and generated indexes

## Compatibility

- Existing DevFlow commands and workflow prose remain valid.
- Registries use JSON syntax in `.yaml` files so PyYAML is not required.
- Missing optional providers are reported, not installed and not treated as a global failure.

## Rollback Strategy

Remove the new registries, skill, specs, tests, CLI subcommands, and entry-router fields. Existing DevFlow behavior remains unchanged because all changes are additive.

## Open Questions

- Future slice: whether workflow recipes should become executable or remain declarative routing contracts.
- Future slice: whether remote probes require a separate security-approved adapter.

