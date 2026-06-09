# Proposal

- change-id: 20260609-spec-first-devflow-fusion-first-slice
- status: Draft
- owner:
- created_at: 2026-06-09

## Background

`spec-first-devflow-fusion-plan` requires the repository to move from run-first governance toward a change/spec first model.

## Problem

Appendix D identified that the repository had enough direction to start, but lacked real `changes/`, `specs/`, templates, and lifecycle guidance. Without those assets, later agents would keep producing chat-only planning outputs.

## Goals

- Create the first usable change/spec directory structure.
- Provide lightweight templates for proposal, design, tasks, delivery, archive, and spec delta.
- Align daily routing, planning skills, governance, and memory boundaries with `change-id`.
- Add minimal change-aware commands to `scripts/devflow.py`.

## In Scope

- Documentation and skill contract updates.
- `devflow.py` support for init/validate/link/archive/sync change operations.
- Validation of the new command path.

## Out of Scope

- Importing OpenSpec CLI.
- Replacing DevFlow Marshal.
- Full L3 archive migration.
- Rewriting all skills.

## Success Criteria

- [x] `changes/` and `specs/` exist with templates/specs.
- [x] L2/L3 rules mention `change-id` and change artifacts.
- [x] `devflow.py` exposes change-aware commands.
- [x] New commands are directly validated.

## Acceptance Baseline

- `python -m py_compile .\scripts\devflow.py`
- `python .\scripts\devflow.py --help`
- `python .\scripts\devflow.py validate-change --change-id 20260609-spec-first-devflow-fusion-first-slice`

## Dependencies

- `spec-first-devflow-fusion-plan,md`
- `spec-first-devflow-fusion-plan.md`
- Existing `scripts/devflow.py`

## Risks

- Run and change artifacts may duplicate content unless skill and governance boundaries are explicit.
- Existing agents may continue using chat-only planning unless contracts point to `changes/<change-id>/`.

## References

- `docs/change-lifecycle.md`
- `specs/change-lifecycle/spec.md`

