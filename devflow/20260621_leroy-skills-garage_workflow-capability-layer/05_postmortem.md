# 05 Postmortem

- change-id: 20260621-workflow-capability-layer
- Outcome: delivered and verified without new dependencies.
- What worked: JSON-compatible YAML kept parsing deterministic; provider fallback selected ripgrep when CodeGraph was absent; standard-library integration tests covered success and failure paths.
- Misses: the first standard Running gate correctly failed because 04_delivery.md had not yet been written; the artifact was added before delivery.
- Stable lesson: workflow composition and capability resolution should remain declarative, additive, and independently validated.
- Follow-ups: optional CodeGraph adapter; frontend-flow; context-budget-manager.
