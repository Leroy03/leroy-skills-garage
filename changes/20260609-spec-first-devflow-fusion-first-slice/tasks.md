# Tasks

- change-id: 20260609-spec-first-devflow-fusion-first-slice
- status: Draft
- design: ./design.md

## Task List

- [x] T1: add change templates.
- [x] T2: add change lifecycle documentation and spec.
- [x] T3: align README/AGENTS/CLAUDE.
- [x] T4: align planning, governance, and memory skill contracts.
- [x] T5: add change-aware `devflow.py` commands.
- [x] T6: validate script and command path.

## Dependencies

- Existing DevFlow script and governance docs.

## Milestones

- M1:
  - output: `changes/templates/*`, `docs/change-lifecycle.md`, `specs/change-lifecycle/spec.md`
  - acceptance: files exist and are referenced by docs.
- M2:
  - output: updated skill contracts and governance protocol.
  - acceptance: L2/L3 change-id rules are explicit.
- M3:
  - output: change-aware `devflow.py` commands.
  - acceptance: CLI help lists commands and validation succeeds.

## Verification Plan

- [x] `python -m py_compile .\scripts\devflow.py`
- [x] `python .\scripts\devflow.py --help`
- [x] `python .\scripts\devflow.py init-change --change-id 20260609-spec-first-devflow-fusion-first-slice`
- [x] `python .\scripts\devflow.py validate-change --change-id 20260609-spec-first-devflow-fusion-first-slice`
- [x] `python .\scripts\devflow.py link-change --run-id 20260609_leroy-skills-garage_spec-first-devflow-fusion-first-slice --change-id 20260609-spec-first-devflow-fusion-first-slice`
- [x] `python .\scripts\devflow.py sync-spec-index`

## Risk Controls

- Keep old run commands untouched.
- Add change commands as additive functionality.
- Keep templates lightweight.

## Done Criteria

- [x] New repository assets exist.
- [x] Governance and planning docs point to change artifacts.
- [x] Tooling supports init/validate/link/index.
- [x] Validation evidence is available.

