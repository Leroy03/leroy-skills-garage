# Design

- change-id: 20260609-spec-first-devflow-fusion-first-slice
- status: Draft
- proposal: ./proposal.md

## Summary

Implement the first slice as a lightweight repository-native extension: keep DevFlow as the governance layer, add change artifacts as the planning layer, and extend the existing script rather than adding another tool.

## Options

### Option A

- approach: documentation/templates first, script extension second.
- cost: low.
- risk: leaves deeper migration for later.

### Option B

- approach: rewrite DevFlow around changes immediately.
- cost: high.
- risk: breaks existing run workflow and increases migration risk.

## Recommended Option

Option A. It matches appendix D's P0/P1 readiness gap and keeps the existing run workflow compatible.

## Object Model / Interfaces

- `change-id`: requirement key, stored under `changes/<change-id>/`.
- `run-id`: execution instance, stored under `devflow/<run-id>/`.
- `spec`: stable capability contract under `specs/<capability>/spec.md`.
- `devflow.py` commands: `init-change`, `validate-change`, `link-change`, `archive-change`, `sync-spec-index`.

## Affected Files / Modules

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/change-lifecycle.md`
- `docs/devflow-run-tooling.md`
- `skills/*/SKILL.md` for planning, governance, and memory boundaries
- `inject/devflow-marshal-context.md`
- `scripts/devflow.py`

## Compatibility

Existing run-first commands remain available. Change-aware commands add fields to `run.json` only when `link-change` is used.

## Rollback Strategy

If script validation fails, revert the `scripts/devflow.py` changes and keep docs/templates as guidance-only assets.

## Open Questions

- When should the repository move from compatibility period to default mandatory `change-id` for all new L2/L3 runs?

