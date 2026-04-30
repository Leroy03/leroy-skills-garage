# Skills Contract Template

本模板用于给核心技能补齐最小治理字段，保持轻量且单一职责。

## 使用原则

- 只补结构，不重写原能力语义。
- 每个 skill 只做自己的事，避免跨角色重复。
- 优先可验证与可交接，不引入额外流程负担。

## 推荐章节（直接复制到 SKILL.md）

```md
## Contract

- `inputs_required`
  - ...
- `outputs_required`
  - ...
- `evidence_files`
  - ...（若不适用可写“无硬性文件”）

## Fallback

- 输入不足时如何降级处理：
  - ...
- 执行失败时如何返回：
  - ...

## Handoff

- 默认交接到：
  - ...
- 失败/阻断时回交流程：
  - ...
```

## 字段说明（最小集）

- `inputs_required`：启动 skill 需要的最小输入。
- `outputs_required`：skill 必须产出的结果键。
- `evidence_files`：可审计的证据文件（如 `test_result.json`）。
- `Fallback`：信息不足或失败时的可执行降级策略。
- `Handoff`：下一步交给哪个 skill，及何种条件交接。

## 轻量边界建议

- 决策型 skill（如 router）：可不要求硬性证据文件。
- 执行型 skill（如 coder/test）：建议要求证据文件。
- 治理型 skill（如 marshal/gate）：必须有门禁结论与交接方向。
