# Change Lifecycle

This document defines the lightest standard path for spec-first DevFlow work.

## Object Model

- `change-id`: the requirement key for a bounded feature, fix, optimization, or governance change.
- `run-id`: one execution instance for a change, used for status, audit, evidence, and gate reports.
- `spec`: a stable capability contract under `specs/`.

## Directory Layout

```text
changes/
  templates/
  <change-id>/
    proposal.md
    design.md
    tasks.md
    delivery.md
    archive.md
    spec-delta/
      <capability>.md
specs/
  <capability>/
    spec.md
```

## Minimal Path

1. Create a change with `YYYYMMDD-<topic-slug>`.
2. Copy or generate `proposal.md`, `design.md`, and `tasks.md` from `changes/templates/`.
3. Create a DevFlow run only when governance or evidence tracking is needed.
4. Link the run to the change.
5. Review the change artifacts before `Reviewed=Approved`.
6. Execute the work and record evidence on the run.
7. Write `delivery.md` for the change.
8. Archive only after stable conclusions and memory candidates are separated.

## Artifact Ownership

- `proposal.md`: problem, scope, goals, success criteria, and acceptance baseline.
- `design.md`: options, selected approach, affected files/modules, compatibility, rollback.
- `tasks.md`: executable tasks, dependencies, milestones, verification plan, done criteria.
- `delivery.md`: implementation summary, changed files, evidence, deviations, residual risks.
- `archive.md`: final outcome, stable decisions, reusable knowledge, spec updates.
- `spec-delta/*.md`: changes to long-lived capability contracts.

## Run Artifact Boundary

Run documents should summarize governance state and link to change artifacts. They should not duplicate full proposal, design, or task bodies.

## Memory Boundary

Memory may receive stable conclusions, commands, rollback lessons, or reusable contracts. It must not receive full copies of change artifacts.

