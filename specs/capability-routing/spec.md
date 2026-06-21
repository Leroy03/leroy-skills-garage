# Capability Routing Spec

## Purpose

Capabilities describe what a workflow needs. Providers describe ordered local implementations. This keeps optional tools out of core routing logic.

## Registry

The registry lives at `capabilities/providers.yaml` and uses JSON-compatible YAML.

Supported read-only probes:

- `command`: provider is available when the command exists on `PATH`; an optional `path` field adds a required project/absolute path guard.
- `path`: provider is available when the project-relative or absolute path exists.
- `always`: built-in provider is always available.

## Selection

- Providers are checked in declaration order.
- The first available provider is selected.
- Diagnosis never installs software, reads credentials, or performs authenticated/network actions.
- Missing optional providers are reported with reasons.
- A required unresolved capability fails `resolve-capability` with a non-zero exit code.

## Integration

- `entry-router` declares `required_capabilities` and `recommended_workflow`.
- `capability-router` resolves providers before an execution skill starts.
- Future adapters may add CodeGraph, Agent-Reach, or Headroom providers without changing workflow recipes.
