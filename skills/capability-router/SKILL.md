---
name: capability-router
description: Resolves workflow capability requirements to ordered available providers and reports missing provider diagnostics. Use after entry-router selects a workflow or before an execution skill needs an optional tool.
---

# Capability Router

## Goal

Translate abstract requirements such as `repository_search` or `test_execution` into a concrete available provider without hard-coding tools into planning and execution skills.

## Inputs

- `required_capabilities`
- `project_root`
- `provider_preferences` (optional)

## Outputs

- `resolved_providers`
- `unresolved_capabilities`
- `diagnostics`
- `fallbacks_used`

## Workflow

1. Read `capabilities/providers.yaml`.
2. Run `python scripts/devflow.py doctor-capabilities` or resolve only required capabilities.
3. Select the first available provider unless a valid preference is supplied.
4. Report fallback use explicitly.
5. Stop before execution when a required capability has no available provider.

## Guardrails

- Do not install dependencies automatically.
- Do not request or inspect credentials during diagnosis.
- Do not perform network or authenticated probes unless a future security-reviewed provider explicitly allows it.
- A missing optional provider is not a workflow failure when a fallback is available.

## Contract

- `inputs_required`
  - `required_capabilities`
  - `project_root`
- `outputs_required`
  - `resolved_providers`
  - `unresolved_capabilities`
  - `diagnostics`
  - `fallbacks_used`
- `evidence_files`
  - `capabilities/providers.yaml`
  - capability doctor output or run gate report when L2/L3

## Fallback

- If the registry is missing or invalid, report the configuration error and return control to `entry-router`.
- If a required capability is unresolved, stop execution and provide the failed probes.

## Handoff

- Resolved providers: hand off to the selected workflow's first execution skill.
- Missing repository context capability: hand off to `context-builder` with built-in file tools if available.
- L2/L3 provider failure: hand off to `DevFlow Marshal` as a blocker.
