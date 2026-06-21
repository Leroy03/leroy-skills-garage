# Delivery

- change-id: 20260621-workflow-capability-layer
- run-id: 20260621_leroy-skills-garage_workflow-capability-layer
- status: Delivered
- delivered_at: 2026-06-21

## Implementation Summary

Added a declarative workflow recipe layer and an ordered capability provider registry. `entry-router` can now recommend workflows and declare required capabilities; `capability-router` resolves those requirements without installing dependencies.

## Changed Files

- `workflows/*.yaml`
- `capabilities/providers.yaml`
- `skills/capability-router/SKILL.md`
- `skills/entry-router/SKILL.md`
- `skills/DevFlow Marshal/SKILL.md`
- `skills.packages.json`
- `specs/workflow-composition/spec.md`
- `specs/capability-routing/spec.md`
- `scripts/devflow.py`
- `tests/test_devflow_workflow_capabilities.py`
- `devflow.project.yaml`
- `README.md`, DevFlow docs/protocol, and generated indexes

## Verification Evidence

- `python -m py_compile scripts/devflow.py`: passed.
- `python -m unittest discover -s tests -p "test_*.py" -v`: 6 passed.
- `python scripts/validate_skills.py`: 29 skills, 5 packages, 0 errors.
- `python scripts/devflow.py validate-workflow --all`: 4 workflows passed.
- `python scripts/devflow.py doctor-capabilities --strict`: 4 capabilities resolved.
- `repository_search`: CodeGraph CLI/project index unavailable, correctly fell back to `ripgrep`.
- DevFlow `collect-evidence`: 4 commands passed, 0 failed.
- Skill contract validation: passed.

## Deviations From Design / Tasks

- None. The implementation stayed within read-only `command/path/always` probes and added no dependencies.

## Residual Risks

- Command presence does not prove semantic health; future provider adapters may add security-reviewed active probes.
- Workflow recipes are declarative and validated but not automatically executed.

## Follow-ups

- Add an optional CodeGraph adapter using the provider contract.
- Evaluate `frontend-flow` and `context-budget-manager` as separate changes.

