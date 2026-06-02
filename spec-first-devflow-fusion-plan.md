# 附录 D：上下文完备性与接手准备度审计

本文件是 [spec-first-devflow-fusion-plan.md](/D:/leroy-skills-garage-main/docs/spec-first-devflow-fusion-plan.md) 的从属附录。  
本文件只回答一个问题：

**在缺失额外口头上下文的情况下，只给新 agent 本仓库和计划书体系，能否稳定继续执行迭代更新。**

## 1. 审计结论

当前结论：

- 可以独立理解方向
- 可以启动第一轮实施
- 还不能保证多轮迭代都无歧义

原因不是总方向不清，而是“未来对象已被计划书定义，但部分关键资产尚未真实落盘”。

## 2. 能独立接手的部分

以下上下文已经具备，可支撑新 agent 判断整体方向：

- 总目标已定义：
  - `change/spec` 主轴
  - `DevFlow` 治理
  - `skills` 执行
  - `memory` 沉淀
- `change-id` 上位、`run-id` 降级的主决策已定义
- 分阶段实施顺序已定义
- 必改文件清单已定义
- 风险与缓解方案已定义
- 总计划书与附录关系已定义

## 3. 已具备的仓库内落点

以下对象已经存在，因此新 agent 能对照真实文件开展工作：

- [README.md](/D:/leroy-skills-garage-main/README.md)
- [AGENTS.md](/D:/leroy-skills-garage-main/AGENTS.md)
- [CLAUDE.md](/D:/leroy-skills-garage-main/CLAUDE.md)
- [skills/entry-router/SKILL.md](/D:/leroy-skills-garage-main/skills/entry-router/SKILL.md)
- [skills/DevFlow Marshal/SKILL.md](</D:/leroy-skills-garage-main/skills/DevFlow Marshal/SKILL.md>)
- [skills/requirement-analyst/SKILL.md](/D:/leroy-skills-garage-main/skills/requirement-analyst/SKILL.md)
- [skills/solution-designer/SKILL.md](/D:/leroy-skills-garage-main/skills/solution-designer/SKILL.md)
- [skills/task-planner/SKILL.md](/D:/leroy-skills-garage-main/skills/task-planner/SKILL.md)
- [skills/requirement-locator/SKILL.md](/D:/leroy-skills-garage-main/skills/requirement-locator/SKILL.md)
- [skills/memory-sync-gate/SKILL.md](/D:/leroy-skills-garage-main/skills/memory-sync-gate/SKILL.md)
- [inject/devflow-marshal-context.md](/D:/leroy-skills-garage-main/inject/devflow-marshal-context.md)
- [scripts/devflow.py](/D:/leroy-skills-garage-main/scripts/devflow.py)

## 4. 仍然缺失的关键上下文

以下内容在计划书中被提到，但当前还不是仓库内真实资产：

- [docs/change-lifecycle.md](/D:/leroy-skills-garage-main/docs/change-lifecycle.md)
- `specs/`
- `changes/`
- `changes/templates/proposal.template.md`
- `changes/templates/design.template.md`
- `changes/templates/tasks.template.md`
- `changes/templates/delivery.template.md`
- `changes/templates/archive.template.md`
- `changes/templates/spec-delta.template.md`

这意味着：

- 新 agent 知道要建哪些对象
- 但还拿不到这些对象的第一版真实模板
- 因此第二轮以后容易出现各自发挥

## 5. 目前最可能出现的接手歧义

### 5.1 `proposal/design/tasks` 最小合格内容不统一

问题：

- 计划书说要产出这些文件
- 但模板还没落盘

结果：

- 不同 agent 会写出不同结构

### 5.2 `change lifecycle` 步骤粒度不统一

问题：

- 总计划书定义了方向
- 但没有独立的操作手册说明“建 change -> 绑定 run -> review -> archive”的最小路径

结果：

- agent 可能知道要做，但不知道从哪一步开始最标准

### 5.3 planning skills 与模板目标还未完全对齐

问题：

- 计划书要求这些 skill 输出到 `changes/`
- 但 skill 文档本身还没改

结果：

- 新 agent 可能继续沿用 chat-only 结果

### 5.4 memory 边界虽有原则，但还未完全转成硬门禁

问题：

- 文档说 memory 不该复制 change 正文
- 但实际 gate 规则和模板仍未落盘

结果：

- 仍可能发生“把 change 正文抄进 memory”

## 6. 以“独立接手”为目标的最小补全项

要达到“只有本仓库和计划书，也能独立推进”的标准，最少需要补齐以下资产：

### P0：必须补

- `changes/templates/proposal.template.md`
- `changes/templates/design.template.md`
- `changes/templates/tasks.template.md`
- `docs/change-lifecycle.md`

### P1：强烈建议补

- `changes/templates/delivery.template.md`
- `changes/templates/archive.template.md`
- `changes/templates/spec-delta.template.md`
- `specs/change-lifecycle/spec.md`

### P2：后续增强

- `specs/memory-boundary/spec.md`
- `specs/skill-contract/spec.md`
- `specs/governance-lifecycle/spec.md`

## 7. 接手准备度评级

### 当前评级：B-

解释：

- A：可在无口头背景下持续多轮稳定迭代
- B：可独立起步，但第二轮后会因模板与 lifecycle 缺失而产生分歧
- C：方向不清或主决策未定

当前属于 B-，原因：

- 总方向明确
- 对象边界明确
- 但最小 change 模板与 lifecycle 还未落盘

## 8. 对新 Agent 的接手规则

如果新 agent 只拿到项目与计划书，默认按以下顺序行动：

1. 先读总计划书
2. 再读附录 A、B、C、D
3. 检查 `specs/`、`changes/`、`changes/templates/` 是否存在
4. 若不存在，优先执行“文档与模板补全”任务，而不是直接改 `devflow.py`
5. 若模板已存在，再开始 planning skills 改造

## 9. 审计结论的使用方式

本附录的用途不是替代总计划书，而是帮助任何接手者先判断：

- 当前是否已经具备足够上下文
- 若还不具备，第一步该补什么
- 哪些缺口不补，会导致后续多 agent 漂移

## 10. 完成定义

当以下条件满足时，可认为“文档接手准备度”达标：

1. 总计划书与附录全部已落盘并互相登记
2. `change lifecycle` 已有独立文档
3. `changes/templates/*` 已存在
4. planning skills 已改到与模板一致
5. 新 agent 不需要额外口头解释即可启动并进入第二轮

