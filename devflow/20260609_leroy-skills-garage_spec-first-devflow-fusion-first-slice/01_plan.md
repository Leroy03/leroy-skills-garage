# 01 Plan

- change-id: 20260609-spec-first-devflow-fusion-first-slice
- Objective: land the first executable slice of the spec-first DevFlow plan so future agents can start from real change artifacts instead of chat-only guidance.
- Scope: add specs/ and changes/ structure, add change templates and lifecycle docs, align README/AGENTS/CLAUDE, update planning/governance/memory skills, and add change-aware commands to scripts/devflow.py.
- Out of scope: full L3 archive migration, replacing DevFlow, introducing OpenSpec CLI, or rewriting every skill.
- Dependencies: existing spec-first-devflow-fusion plan, appendix D readiness audit, current scripts/devflow.py.
- Milestones: create artifacts; update skill contracts; add script commands; run validators/help checks.
- Acceptance: change templates exist, lifecycle doc exists, L2/L3 rules mention change-id, devflow.py exposes init-change/validate-change/link-change/archive-change/sync-spec-index, validation evidence is recorded.
- Risk/Rollback: if script changes fail, revert only scripts/devflow.py and keep docs/templates; rollback trigger is devflow help or validation failure after patch.
