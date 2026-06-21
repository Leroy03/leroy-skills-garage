# Archive

- change-id: 20260621-workflow-capability-layer
- archived_at: 2026-06-21
- final_status: Archived

## Final Outcome

The repository now has a validated workflow recipe layer and a capability provider layer integrated with `entry-router`, DevFlow tooling, skill packages, tests, and documentation.

## Stable Decisions

- Workflow recipes compose skills but do not replace skill contracts or DevFlow gates.
- Workflow and capability files use JSON-compatible YAML to avoid a new parser dependency.
- Capability providers are ordered and resolved by the first available read-only probe.
- Capability diagnosis never installs dependencies or accesses credentials.
- Optional semantic providers such as CodeGraph must retain a built-in fallback.

## Reusable Knowledge

- Validate recipes with `python scripts/devflow.py validate-workflow --all`.
- Diagnose providers with `python scripts/devflow.py doctor-capabilities --strict`.
- Resolve one provider with `python scripts/devflow.py resolve-capability --name <name>`.
- Run all repository evidence commands through `python scripts/devflow.py collect-evidence` with `devflow.project.yaml`.

## Spec Updates

- Added `specs/workflow-composition/spec.md`.
- Added `specs/capability-routing/spec.md`.

## Memory Candidates

Only list stable conclusions that may belong in permanent memory. Do not copy the full proposal, design, or tasks.

- The specs and README already provide the stable source of truth; no duplicate permanent-memory entry is required.

## References

- `changes/20260621-workflow-capability-layer/delivery.md`
- `devflow/20260621_leroy-skills-garage_workflow-capability-layer/test_result.json`
- `devflow/20260621_leroy-skills-garage_workflow-capability-layer/contract_report.json`

