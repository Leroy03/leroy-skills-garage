# Spec-First + DevFlow 融合改造计划书

## 1. 文档目标

本计划书用于指导 `D:\leroy-skills-garage-main` 从当前的 `run-first governance` 结构，演进为 `spec/change first + DevFlow governance + skills execution + memory distillation` 的统一架构。

目标不是“把 OpenSpec 原样搬进来”，而是吸收其最有价值的部分：

- 把功能改动定义为仓库内长期可追踪的 `spec/change artifacts`
- 让 `DevFlow Marshal + devflow.py` 从“run 文书中心”收敛为“治理与门禁中心”
- 让 `skills` 成为围绕 `change/spec` 运作的执行与路由层
- 让 `memory` 只沉淀长期稳定知识，不再承载一次性 change 正文

本计划书的受众：

- 新加入的 agent
- 后续维护本仓库的人
- 需要按统一架构继续扩展 skills / devflow / spec 体系的人

本计划书的使用方式：

- 先阅读第 2-6 节确认目标架构与边界
- 再按第 7-12 节执行改造
- 任何新 agent 接手时，默认以本计划书为总方向文档

## 1.1 文档控制规则

本文件是本次改造的唯一总计划书。

允许存在多个附录或子文档，但必须满足以下规则：

- 总方向、主决策、阶段顺序、完成定义，只能以本文件为准
- 子文档只能展开说明，不能自行改写主方向
- 若子文档与本文件冲突，以本文件为准
- 任何新 agent 首先阅读本文件，再按需阅读附录

## 1.2 附录索引

以下文档是本总计划书的从属附录：

- [spec-first-devflow-appendix-a-architecture.md](/D:/leroy-skills-garage-main/docs/spec-first-devflow-appendix-a-architecture.md)
- [spec-first-devflow-appendix-b-rollout.md](/D:/leroy-skills-garage-main/docs/spec-first-devflow-appendix-b-rollout.md)
- [spec-first-devflow-appendix-c-devflow-script-design.md](/D:/leroy-skills-garage-main/docs/spec-first-devflow-appendix-c-devflow-script-design.md)
- [spec-first-devflow-appendix-d-context-readiness.md](/D:/leroy-skills-garage-main/docs/spec-first-devflow-appendix-d-context-readiness.md)

使用约定：

- 看方向与边界：先看本文件第 3-6 节，再看附录 A
- 看实际执行顺序：先看本文件第 7-11 节，再看附录 B
- 看 `devflow.py` 如何改：先看本文件第 7、8、9 节，再看附录 C
- 看“只有项目和计划书能否独立推进”：先看本文件第 13 节，再看附录 D

## 2. 当前状态总结

### 2.1 当前主结构

当前仓库已具备四类核心资产：

- `skills/`
  - skill 定义与协作协议
- `scripts/devflow.py`
  - run 创建、状态流转、artifact 写入、evidence 收集、contract 校验
- `DevFlow Marshal`
  - L0/L1/L2/L3 分级、审议门禁、状态机
- `memory/`
  - context / permanent-memory / memory-sync-gate 等沉淀路径

### 2.2 当前优势

- 已有明确分级与治理骨架
- 已有 `validate-run` / `collect-evidence` / `validate-skill-contract`
- 已有 package / validator / status 页面
- 已有 memory 分层意识
- 已有 UTF-8 / contract / handoff 等工程化约束

### 2.3 当前核心问题

当前结构更偏 `run-first`，表现为：

- `run_id` 更像主对象
- `01_plan.md` ~ `05_postmortem.md` 承担了大量正文职责
- 对“这次功能改动本身”的规格资产沉淀较弱
- planning / governance / archive 的文书边界不够彻底
- memory 与 change 正文之间未来容易重复

### 2.4 本次改造的根本判断

后续架构应改为：

- `change/spec` 是需求与改动的主对象
- `run` 是执行实例与审计对象
- `DevFlow` 是治理对象
- `skills` 是执行对象
- `memory` 是长期知识对象

## 3. 目标架构

### 3.1 目标一句话

将仓库升级为：

`Spec/Change 主轴 + DevFlow 治理层 + Skills 执行层 + Memory 沉淀层`

### 3.2 目标分层

#### A. Spec / Change 层

职责：

- 定义“要改什么”
- 记录“为什么改”
- 记录“怎么设计”
- 记录“任务怎么拆”
- 记录“规格如何变化”

建议目录：

```text
specs/
  <capability>/
    spec.md

changes/
  <change-id>/
    proposal.md
    design.md
    tasks.md
    delivery.md
    archive.md
    spec-delta/
      <capability>.md
```

#### B. Governance 层

职责：

- 判定分级
- 控制状态机
- 控制审议门禁
- 验证 change artifacts 是否完整
- 记录审计与 gate 报告

主要组件：

- `skills/entry-router`
- `skills/DevFlow Marshal`
- `scripts/devflow.py`

#### C. Skills 层

职责：

- 分析需求
- 产出 proposal / design / tasks
- 定位代码
- 实施变更
- 收集测试证据
- 校验 contract

#### D. Memory 层

职责：

- 沉淀长期稳定知识
- 记录这次执行摘要
- 做 archive 前完整性检查

主要组件：

- `context-archiver`
- `permanent-memory`
- `knowledge-keeper`
- `memory-sync-gate`

### 3.3 目标对象模型

#### `change-id`

定义：

- 需求主键
- 一次有边界的功能改动或架构改造

职责：

- 挂载 proposal / design / tasks / spec-delta / archive

#### `run-id`

定义：

- 执行实例主键
- 某次对一个 change 的实际执行过程

职责：

- 挂载状态流转
- 挂载测试证据
- 挂载 gate 报告
- 挂载审计事件

### 3.4 核心关系

推荐关系：

- `1 change` 对 `1..n runs`
- `1 run` 对 `1 active change`

强约束：

- L2/L3 工作必须绑定 `change-id`
- 没有 `change-id` 的 L2/L3 不允许进入最终 gate
- `run_id` 不再承载正文主文书

## 4. 边界重画

### 4.1 变更正文归谁

今后这些内容只放在 `changes/<change-id>/`：

- 需求摘要
- 方案选型
- 设计说明
- 任务拆解
- 规格变化
- 最终 archive 摘要

禁止重复放在：

- `01_plan.md`
- `02_review.md`
- `04_delivery.md`
- `memory/` 的长期文档里

### 4.2 治理文书归谁

今后 `DevFlow` 文书只负责：

- 本轮是否允许继续
- 是否通过 review gate
- 本轮执行状态
- 本轮 evidence 和 gate 结果
- 本轮偏差与阻塞点

也就是说：

- `01_plan.md` 只写治理级 plan 摘要，并引用 `proposal.md` / `design.md`
- `02_review.md` 只写 gate verdict，并引用 `tasks.md` / `spec-delta`
- `03_dispatch.md` 只写执行授权与 handoff
- `04_delivery.md` 只写本次执行与验证摘要
- `05_postmortem.md` 只写治理层复盘

### 4.3 memory 归谁

今后 memory 只收：

- 长期稳定规则
- 可复用接口约定
- 常见坑与回滚经验
- 通用验证命令

memory 不收：

- 某个 change 的完整 proposal/design/tasks 正文
- 任何一次性需求文书副本

## 5. 非目标

以下事项不在本次改造的首轮范围内：

- 不直接引入 OpenSpec 官方 CLI
- 不直接复制 OpenSpec 命令体系
- 不引入新的重型后台 runtime
- 不把仓库改成多 agent 平台
- 不推翻现有 `DevFlow Marshal`
- 不一次性重写所有 skill 内容

## 6. 总体改造策略

### 6.1 总策略

采用“三阶段收敛法”：

1. 先建立 `change/spec` 主轴
2. 再让 `DevFlow` 接管对 `change` 的治理
3. 最后清理重复文书并完成 memory 边界收束

### 6.2 为什么不一步到位

原因：

- 当前 `devflow.py` 已经可用
- 当前 skill contract 已有用户心智
- 一步重构会破坏现有运行路径
- 风险最大的是“架构看起来干净，但过程不可落地”

## 7. 分阶段实施计划

## 阶段 0：基线冻结与对齐

### 目标

- 先冻结当前规则，避免边改边漂移
- 明确这次改造以本计划书为唯一总方向

### 任务

1. 建立本计划书为总纲文档
2. 在 `README.md` 中增加新架构方向声明
3. 在 `AGENTS.md` / `CLAUDE.md` 中补充：
   - `change-id` 将成为 L2/L3 主键
   - `run` 将降级为执行实例

### 产出

- 本文档
- `README.md` 架构声明
- `AGENTS.md` / `CLAUDE.md` 规则补充

### 验收

- 新 agent 只读仓库文档即可知道改造方向

## 阶段 1：建立 Spec / Change 主轴

### 目标

- 让仓库具备稳定的 `specs/` 与 `changes/` 目录约定

### 任务

1. 新增目录结构

```text
specs/
changes/
changes/templates/
```

2. 新增 change 文书模板

- `proposal.template.md`
- `design.template.md`
- `tasks.template.md`
- `delivery.template.md`
- `archive.template.md`
- `spec-delta.template.md`

3. 约定 `change-id` 生成规则

建议：

- `YYYYMMDD-<topic-slug>`

示例：

- `20260602-spec-first-devflow-fusion`

4. 在 `README.md` 中新增 “如何发起一个 change”

### 需要修改的文件

- `README.md`
- 新增 `specs/`
- 新增 `changes/`
- 可能新增 `docs/change-lifecycle.md`

### 风险

- 仅建目录但没有 skill 接入，形成空壳

### 风险控制

- 阶段 1 完成后，必须立刻进入阶段 2

## 阶段 2：让 Planning Skills 产出 Change Artifacts

### 目标

- 让 planning 类 skills 不再主要产出聊天内文本
- 改为产出 `changes/<change-id>/...` 正文

### 需要改造的 skills

#### `requirement-analyst`

当前职责：

- 分析自然语言需求

新职责：

- 产出 `proposal.md` 的需求边界部分
- 明确 `in_scope` / `out_of_scope`
- 输出 acceptance baseline

#### `solution-designer`

当前职责：

- 输出方案选项与 tradeoff

新职责：

- 产出 `design.md`
- 维护 `recommended_option`
- 记录 architecture tradeoff

#### `task-planner`

当前职责：

- 输出 WBS

新职责：

- 产出或更新 `tasks.md`
- 将任务拆解结果挂到 `change-id`

#### `requirement-locator`

当前职责：

- 定位相关代码

新职责：

- 补充 `design.md` / `tasks.md` 的 affected files / modules

### 关键 contract 变化

planning skills 的默认输出目标从：

- `01_plan.md`
- 聊天内文字总结

改为：

- `changes/<change-id>/proposal.md`
- `changes/<change-id>/design.md`
- `changes/<change-id>/tasks.md`

### 风险

- agent 仍然沿用旧习惯，只在 chat 中给结果

### 风险控制

- 修改 skill 文档中的 Required Output
- 新增模板与示例
- 后续 gate 中把 change artifacts 完整性设为必检

## 阶段 3：重构 DevFlow 为 Change-Aware Governance

### 目标

- 让 `DevFlow Marshal + devflow.py` 认识 `change-id`
- 让 run 降级为执行实例

### 需要修改的核心对象

#### `skills/DevFlow Marshal/SKILL.md`

新增规则：

- `L2/L3` 默认必须绑定 `change-id`
- `Reviewed=Approved` 前必须检查：
  - `proposal.md`
  - `design.md`
  - `tasks.md`
  - 必要时 `spec-delta`

#### `inject/devflow-marshal-context.md`

新增协议：

- `change-id` 是主对象
- `run_id` 是执行实例
- `run` 对应的文书以引用 `change artifacts` 为主

#### `skills/entry-router/SKILL.md`

新增字段建议：

- `artifact_mode: chat_only | repo_change`
- `change_required: yes | no`

规则建议：

- `L0/L1` 可 `chat_only`
- `L2/L3` 默认 `repo_change`

### `devflow.py` 需要新增的能力

建议新增命令：

- `init-change`
  - 初始化 `changes/<change-id>/`
- `validate-change`
  - 校验 change artifact 完整性
- `link-change`
  - 把 `run_id` 绑定到 `change-id`
- `archive-change`
  - 完成归档
- `sync-spec-index`
  - 更新 spec/change 索引

### `run.json` 建议新增字段

```json
{
  "run_id": "...",
  "change_id": "...",
  "change_path": "...",
  "artifact_mode": "repo_change",
  "status": "Draft"
}
```

### 风险

- 旧 run 结构与新结构并存
- `validate-run` 与 `validate-change` 可能出现双重逻辑

### 风险控制

- 初期允许兼容模式
- 明确 `validate-run` 管执行一致性
- 明确 `validate-change` 管规格资产一致性

## 阶段 4：收缩 Run 文书，消除正文重复

### 目标

- 让 run 文书不再承担正文主内容

### 需要做的事

1. 缩减 `01_plan.md`

改为只包含：

- `change-id`
- 本轮目标
- 当前 gate 前提
- 当前假设
- 下一步

不再重复写：

- 完整 scope
- 完整 design
- 完整 tasks

2. 缩减 `02_review.md`

改为只包含：

- 审核对象引用
- PASS / FAIL
- blocker
- rework 指令

3. 缩减 `04_delivery.md`

改为只包含：

- 本次执行摘要
- evidence 链接
- 与 design/tasks 的偏差

4. 缩减 `05_postmortem.md`

改为只包含：

- 治理复盘
- 过程复盘
- 标准化建议

### 废弃或弱化原则

以下内容今后不应再以 run 文书为主载体：

- 完整需求正文
- 完整设计正文
- 完整任务正文

## 阶段 5：建立 Stable Spec 体系

### 目标

- 把仓库里长期稳定的能力规则，从 skill prose 中抽出为 `specs/`

### 适合先抽出的 spec

建议优先抽这些：

- `governance-lifecycle`
- `skill-contract`
- `test-evidence`
- `memory-boundary`
- `change-lifecycle`

### 为什么要做这步

因为很多规则不是“一次 change 的设计”，而是仓库长期稳定契约。  
这些内容只放在 `SKILL.md` 中不够显式，不利于外部 agent 快速对齐。

### 风险

- `specs/` 与 `skills/` 再次重复

### 风险控制

- `specs/` 只放稳定契约
- `skills/` 只放执行入口与使用规则

## 阶段 6：重构 Memory 边界

### 目标

- 防止 change 文书与 memory 重复

### 边界规则

#### `context-archiver`

保留：

- 本次执行摘要
- 改动概览
- 验证方式

不保留：

- 完整 proposal/design/tasks 副本

#### `permanent-memory`

保留：

- 长期稳定约定
- 命令
- 常见坑
- 回滚策略

不保留：

- 某次 change 全量文书

#### `memory-sync-gate`

新增检查：

- 此 change 是否已 archive
- 是否有应进入 permanent-memory 的稳定结论
- 是否错误复制了一次性正文到 memory

### 风险

- 记忆层继续被当成“文书备份区”

### 风险控制

- 在 skill contract 中明确禁止

## 阶段 7：验证、迁移与切换

### 目标

- 让新架构真正可执行

### 验证项

1. 用一个真实 L2 任务跑通
2. 用一个真实 L3 任务跑通
3. 验证：
   - change 建立
   - planning artifacts 产出
   - run 绑定 change
   - evidence 收集
   - contract 校验
   - archive 与 memory gate

### 迁移策略

建议分三档：

#### 档 1：兼容期

- 老 run 流程继续可用
- 新 L2/L3 推荐使用 change

#### 档 2：默认期

- 新 L2/L3 强制使用 change
- 老 run 文书保留兼容读取

#### 档 3：收敛期

- run 文书彻底摘要化
- change 成为唯一正文主层

## 8. 需要修改的文件清单

### 8.1 高优先级

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `skills/entry-router/SKILL.md`
- `skills/DevFlow Marshal/SKILL.md`
- `skills/requirement-analyst/SKILL.md`
- `skills/solution-designer/SKILL.md`
- `skills/task-planner/SKILL.md`
- `skills/requirement-locator/SKILL.md`
- `skills/memory-sync-gate/SKILL.md`
- `inject/devflow-marshal-context.md`
- `scripts/devflow.py`

### 8.2 新增目录 / 文件

- `specs/`
- `changes/`
- `changes/templates/proposal.template.md`
- `changes/templates/design.template.md`
- `changes/templates/tasks.template.md`
- `changes/templates/delivery.template.md`
- `changes/templates/archive.template.md`
- `changes/templates/spec-delta.template.md`
- `docs/change-lifecycle.md`
- `docs/spec-first-devflow-fusion-plan.md`

### 8.3 次优先级

- `docs/devflow-run-tooling.md`
- `docs/external-inspirations.md`
- `docs/indexes/*`
- `scripts/update_knowledge_index.py`
- `scripts/validate_skills.py`
- `skills.packages.json`

## 9. 关键设计决策

## 决策 1：保留 DevFlow，不替换为 OpenSpec

理由：

- 当前仓库已有可用治理底座
- 直接替换成本高
- 用户心智已经围绕 DevFlow 建立

结论：

- 保留 `DevFlow Marshal + devflow.py`
- 吸收的是 `spec/change artifact` 思想

## 决策 2：`change-id` 上位，`run_id` 降级

理由：

- change 更适合作为需求主键
- run 更适合作为执行实例

结论：

- 新架构以 `change-id` 为主
- `run_id` 继续存在，但不再做正文主轴

## 决策 3：规划文书与治理文书分离

理由：

- 避免 proposal/design/tasks 与 plan/review/delivery 重复

结论：

- `changes/` 承担正文
- `run` 文书承担治理摘要

## 决策 4：memory 不做 change 仓库备份

理由：

- 否则 memory 会快速失真

结论：

- memory 只保留稳定结论

## 10. 主要风险与缓解方案

## 风险 1：架构变重，agent 不愿走

表现：

- 新流程太繁琐
- L2/L3 任务被绕过

缓解：

- L0/L1 不强制 change
- L2/L3 才强制
- 模板要轻
- 命令要能一键初始化

## 风险 2：run 和 change 双主键打架

表现：

- 不知道看哪个对象
- gate 不知道审哪个对象

缓解：

- 明确 `change-id` 是需求主键
- `run_id` 是执行实例主键
- 所有 gate 先看 change，再看 run

## 风险 3：文书重复

表现：

- `proposal.md` 和 `01_plan.md` 都写完整计划

缓解：

- 政策上禁止正文重复
- 缩减 run 文书模板
- validator 增加重复边界规则

## 风险 4：memory 被污染

表现：

- change 文书被复制进长期记忆

缓解：

- memory gate 加强校验
- permanent-memory 明确只收 stable conclusions

## 风险 5：迁移过程中旧流程断裂

表现：

- 旧任务无法继续
- 老文档无法解释

缓解：

- 设置兼容期
- `validate-run` 保留旧结构兼容
- 分阶段切换

## 11. 推荐实施顺序

推荐按以下顺序落地：

1. 建立 `changes/` / `specs/` 目录与模板
2. 修改 `README.md` / `AGENTS.md` / `CLAUDE.md`
3. 改 `requirement-analyst` / `solution-designer` / `task-planner`
4. 改 `entry-router` / `DevFlow Marshal`
5. 给 `devflow.py` 增加 `change-aware` 命令
6. 缩减 run 文书模板
7. 修改 memory 相关 skills
8. 更新 validator / knowledge index / status surface
9. 用真实 L2/L3 任务验收

## 12. 对新 Agent 的执行指令

任何新 agent 接手该项目时，默认遵循以下规则：

1. 不把 OpenSpec 当作外来整包引入目标。
2. 本仓库的目标架构是：
   - `change/spec` 主轴
   - `DevFlow` 治理
   - `skills` 执行
   - `memory` 沉淀
3. L2/L3 改造默认以 `change-id` 为主键。
4. 不再新增以 `run` 为中心的正文文书。
5. 任何 planning 类输出，应优先落到 `changes/<change-id>/...`。
6. 任何 governance 类输出，应只做 gate / 状态 / 摘要，不复制正文。
7. 任何 memory 类输出，只沉淀稳定结论，不复制 change 正文。
8. 如果出现重复，优先删掉 run 文书中的正文，而不是删 change artifacts。
9. 如果出现对象冲突，优先保留 `change-id` 主轴。
10. 若要增加新脚本能力，优先扩展 `scripts/devflow.py`，不要并行造第二套治理脚本。

## 13. 完成定义

当以下条件全部满足时，可认为本次融合改造完成：

1. 仓库存在稳定的 `specs/` 与 `changes/` 结构
2. `L2/L3` 默认要求 `change-id`
3. planning skills 默认产出 `proposal/design/tasks`
4. `DevFlow Marshal` 能对 `change artifacts` 做 gate
5. `devflow.py` 支持 change-aware 命令
6. run 文书不再承载正文主内容
7. memory 不再重复收录 change 正文
8. 至少一个真实 L2 和一个真实 L3 任务跑通全链路

## 13.1 文档接手完成定义

当以下条件满足时，可认为“只依赖本仓库和本计划书体系，新 agent 也能独立接手并继续迭代”：

1. 总计划书与附录索引完整，且没有未登记的关键从属文档
2. 目标目录 `specs/`、`changes/`、`changes/templates/` 已真实存在
3. `change lifecycle` 操作文档已落盘
4. planning skills 的目标输出与模板目录一致
5. `DevFlow Marshal` 与 `devflow.py` 已明确 `change-id` / `run-id` 边界
6. memory 边界文档已说明哪些内容禁止复制
7. 新 agent 不需要额外口头解释即可判断“下一步先补什么”

## 14. 建议首批实施任务

建议首批只做以下子项目：

### 子项目 A：目录与模板落地

- 新建 `specs/` / `changes/`
- 建 change 模板

### 子项目 B：planning skills 改造

- 改 `requirement-analyst`
- 改 `solution-designer`
- 改 `task-planner`

### 子项目 C：DevFlow 接管 change

- 改 `DevFlow Marshal`
- 改 `entry-router`
- 改 `devflow.py`

### 子项目 D：memory 边界收敛

- 改 `memory-sync-gate`
- 更新 `context-archiver` / `permanent-memory` 说明

## 15. 对后续文档拆分的要求

如果后续继续细化文档，必须遵守以下拆分原则：

1. 总计划书永远只有这一份。
2. 任何新附录必须在本文件 `1.2 附录索引` 中登记。
3. 新附录只允许细化以下内容：
   - 目录结构与对象模型
   - 分阶段任务与实施步骤
   - 脚本命令与数据结构设计
   - skill contract 细化
   - 验证矩阵与迁移清单
   - 文档完备性与接手准备度审计
4. 新附录不得自行定义新的总目标、新主键或新的治理主轴。
5. 若需要推翻本文件主决策，必须直接修改本文件，而不是绕过本文件新增“替代版计划”。

---

## 附录 A：推荐的新目录树

```text
docs/
  spec-first-devflow-fusion-plan.md
  change-lifecycle.md

specs/
  governance-lifecycle/
    spec.md
  skill-contract/
    spec.md
  test-evidence/
    spec.md
  memory-boundary/
    spec.md

changes/
  templates/
    proposal.template.md
    design.template.md
    tasks.template.md
    delivery.template.md
    archive.template.md
    spec-delta.template.md
  20260602-spec-first-devflow-fusion/
    proposal.md
    design.md
    tasks.md
    delivery.md
    archive.md
    spec-delta/
      governance-lifecycle.md

skills/
scripts/
memory/
```

## 附录 B：推荐的模板职责

### proposal.md

- 背景
- 问题定义
- in_scope / out_of_scope
- success criteria

### design.md

- 方案选项
- 选型理由
- 新对象模型
- 边界与兼容策略

### tasks.md

- 原子任务
- 依赖关系
- 验收标准
- 风险与回滚

### delivery.md

- 本次执行摘要
- 关键变更
- 验证结果
- 未完成项

### archive.md

- 最终结论
- 稳定规则
- 后续可复用项
