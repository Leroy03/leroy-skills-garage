# Tasks

- change-id: 20260621-workflow-capability-layer
- status: Planned
- design: ./design.md

## Task List

- [x] T1: define workflow and capability schemas/specs.
- [x] T2: add bundled workflows and provider registry.
- [x] T3: add capability-router and entry-router contract fields.
- [x] T4: implement DevFlow validation/doctor/resolution commands.
- [x] T5: add standard-library unit tests.
- [x] T6: update README, indexes, delivery artifacts, and run evidence.

## Dependencies

- T1 precedes T2-T4.
- T2-T4 precede T5.
- Validation precedes delivery and commit.

## Milestones

- M1:
  - output: specs, registries, skill contracts.
  - acceptance: files parse and references resolve.
- M2:
  - output: DevFlow CLI commands and tests.
  - acceptance: all unit and repository validators pass.
- M3:
  - output: docs, indexes, delivery evidence, commit.
  - acceptance: clean committed worktree.

## Verification Plan

- [x] Python compile check.
- [x] Unit tests.
- [x] Skill validator.
- [x] Workflow validator for all recipes.
- [x] Capability doctor and resolution smoke tests.
- [x] Change and run gates.

## Risk Controls

- No dependency installation.
- No credential/network probes.
- Read-only capability diagnosis.
- Existing command behavior covered by smoke checks.

## Done Criteria

- [x] Success criteria pass.
- [x] Delivery evidence is written to change and run artifacts.
- [x] Changes are committed.

