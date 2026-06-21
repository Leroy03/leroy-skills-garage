# Proposal

- change-id: 20260621-workflow-capability-layer
- status: Planned
- owner: Codex
- created_at: 2026-06-21

## Background

The repository has a mature skill router, package manifest, change lifecycle, and DevFlow governance tooling. It does not yet have a reusable command/workflow layer or a capability registry that can select and diagnose optional tool providers.

## Problem

- Skill chains are described in prose but are not machine-validatable workflow recipes.
- `entry-router` can recommend skills but cannot declare concrete capability requirements or provider fallback.
- Optional tools such as CodeGraph cannot be integrated without hard-coding them into individual skills.
- There is no standard doctor command that proves a capability provider is actually usable.

## Goals

- Add JSON-compatible YAML workflow recipes for common delivery paths.
- Add a capability provider registry with ordered fallback.
- Add `validate-workflow`, `doctor-capabilities`, and `resolve-capability` commands to `scripts/devflow.py`.
- Extend `entry-router` with workflow and capability outputs.
- Add stable specs, documentation, tests, and indexes.

## In Scope

- `workflows/implement.yaml`, `debug.yaml`, `ship.yaml`, and `archive.yaml`.
- `capabilities/providers.yaml` with deterministic local probes.
- A new `capability-router` skill.
- DevFlow CLI validation and diagnosis commands.
- Unit tests using Python standard library only.

## Out of Scope

- Installing CodeGraph, Agent-Reach, Headroom, or any external runtime.
- Network, browser-login, cookie, or credential probes.
- Replacing `entry-router`, DevFlow Marshal, or existing skill packages.
- A general workflow execution engine; this change validates and resolves recipes only.

## Success Criteria

- [x] All bundled workflow recipes pass `validate-workflow`.
- [x] `doctor-capabilities` reports provider availability without installing dependencies.
- [x] `resolve-capability` selects the first available provider or exits non-zero when required and unavailable.
- [x] Existing skill validation remains green.
- [x] Unit tests pass without new dependencies.

## Acceptance Baseline

- [x] `python -m unittest discover -s tests -p "test_*.py" -v`
- [x] `python scripts/validate_skills.py`
- [x] `python scripts/devflow.py validate-workflow --all`
- [x] `python scripts/devflow.py doctor-capabilities`
- [x] `python scripts/devflow.py resolve-capability --name repository_search`

## Dependencies

- Python standard library.
- Existing `scripts/devflow.py`, skill inventory, and change lifecycle.

## Risks

- Workflow recipes may duplicate skill prose; recipes therefore contain orchestration metadata only.
- Provider probes may become platform-specific; this slice restricts probes to `command`, `path`, and `always`.
- A doctor command may be mistaken for an installer; it explicitly performs read-only detection only.

## References

- `docs/change-lifecycle.md`
- `skills/entry-router/SKILL.md`
- `skills.packages.json`

