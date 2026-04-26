# leroy-skills-garage

一组围绕“需求到交付”主流程组织的 skills 仓库，目标是让方案、拆解、编码、评审、测试、交付与沉淀形成低歧义、可复用的协作链路。

## 仓库目标

- 让 skill 边界清晰：知道谁负责什么、谁不负责什么
- 让 handoff 可复用：输出尽量结构化，减少口语交接损耗
- 让流程可分级：简单任务轻处理，复杂任务再启用治理与文书
- 让知识可沉淀：把稳定约定、入口、命令与复盘放回仓库

## 外部灵感

- `superpowers`：提供完整 workflow、TDD、调试、review、并行执行等工程技能编排
- `andrej-karpathy-skills`：提供轻量但高价值的执行护栏，重点防止乱猜、过度工程和越界修改
- 本仓库的融合思路：`Karpathy` 负责约束执行风格，`Superpowers` 负责补强关键 workflow，而 `DevFlow` 负责按 `⚪/🟢/🟡/🔴` 控制流程重量

## 技能地图

### 方案与规划

- `entry-router`：入口分流，先判断该走哪种轻重流程
- `solution-designer`：需求澄清、方案对比、推荐方案
- `task-planner`：把方案转成 WBS、里程碑、验收与风险
- `dev-flow-orchestrator`：面向跨阶段、跨角色的端到端流程编排
- `DevFlow Marshal`：治理入口，负责分级、状态机、门禁与文书纪律

### 上下文与知识

- `knowledge-keeper`：维护稳定入口、文档、命令与仓库约定索引
- `context-builder`：把任务转成核心文件、依赖、影响面与回归点
- `context-archiver`：沉淀本次任务的结论、改动与验证方式
- `permanent-memory`：沉淀跨任务长期复用的稳定知识

### 实作与分析

- `karpathy-guidelines`：全局执行护栏，防止乱猜、过度设计与越界改动
- `pragmatic-coder`：最小改动、够用即可、可验证的务实实现
- `tdd-lite`：轻量测试先行，只在高风险改动时补最小保护测试
- `bug-hunter`：问题定位、根因分析、修复方案
- `code-reviewer`：正确性、安全、性能与可维护性评审
- `code-optimizer`：针对明确目标做最小优化或重构
- `verification-before-completion`：完成前验证，要求证据而不是口头完成

### 质量与交付

- `qa-gatekeeper`：测试矩阵、回归范围、发布门禁
- `ai-output-auditor`：对 AI 生成结果做事实、一致性与风险审校
- `delivery-tracker`：交付前检查、验证路径与回滚方案

## 推荐使用链路

### ⚪ 口谕

- 适用：快问快答、解释、微调、一次性说明
- 处理：主对话直接回答，必要时少量只读工具
- 通常不启用：文书、run 管理、正式治理

### 🟢 快奏

- 适用：单点修复、小改动、边界明确的实现
- 推荐链路：`entry-router` -> `karpathy-guidelines` -> `knowledge-keeper`（可选） -> `context-builder`（可选） -> `tdd-lite`（高风险时） -> `pragmatic-coder` -> `verification-before-completion`
- 验证：小范围测试、日志检查、诊断检查

### 🟡 常奏

- 适用：多文件但边界清楚、有轻量规划与评审需求
- 推荐链路：`entry-router` -> `karpathy-guidelines` -> `solution-designer`（如需） -> `task-planner` -> `context-builder` -> `tdd-lite`（核心逻辑时） -> `pragmatic-coder` -> `code-reviewer` / `qa-gatekeeper` -> `verification-before-completion`
- 工具化：可用 `python .\scripts\devflow.py` 维护最小 run 与文书
- 默认停点：`Reviewed=Approved`

### 🔴 正奏

- 适用：正式需求、高风险改动、跨系统集成、需要审计追溯
- 推荐链路：`entry-router` -> `karpathy-guidelines` -> `DevFlow Marshal` -> `dev-flow-orchestrator` -> `solution-designer` -> `task-planner` -> `context-builder` -> `pragmatic-coder` -> `code-reviewer` -> `qa-gatekeeper` -> `delivery-tracker` -> `context-archiver` / `permanent-memory`
- 工具化：使用 `scripts/devflow.py` 全流程维护状态与文书

## 覆盖矩阵

| 阶段 | 主技能 | 补充技能 |
| --- | --- | --- |
| 入口分流 | `entry-router` | `DevFlow Marshal` |
| 需求澄清 | `solution-designer` | `knowledge-keeper`、`karpathy-guidelines` |
| 任务拆解 | `task-planner` | `dev-flow-orchestrator` |
| 上下文构建 | `context-builder` | `knowledge-keeper` |
| 编码实现 | `pragmatic-coder` | `bug-hunter`、`code-optimizer`、`karpathy-guidelines`、`tdd-lite` |
| 代码评审 | `code-reviewer` | `ai-output-auditor`、`karpathy-guidelines` |
| 测试与门禁 | `qa-gatekeeper` | `code-reviewer`、`verification-before-completion` |
| 发布与交付 | `delivery-tracker` | `DevFlow Marshal` |
| 经验沉淀 | `context-archiver` | `permanent-memory` |

## 任务到分级

| 任务类型 | 建议分级 | 默认链路 |
| --- | --- | --- |
| 问答、解释、一次性说明 | `⚪` | 直接回答 |
| 单文件修复、边界明确的小实现 | `🟢` | `entry-router` -> `karpathy-guidelines` -> `pragmatic-coder` -> `verification-before-completion` |
| 可复现 Bug 且需防回归 | `🟢/🟡` | `entry-router` -> `karpathy-guidelines` -> `bug-hunter` -> `tdd-lite` -> `pragmatic-coder` -> `verification-before-completion` |
| 多文件实现、有轻量规划需求 | `🟡` | `entry-router` -> `karpathy-guidelines` -> `task-planner` -> `context-builder` -> `pragmatic-coder` -> `code-reviewer` |
| 核心逻辑重构、需要行为保护 | `🟡` | `entry-router` -> `karpathy-guidelines` -> `context-builder` -> `tdd-lite` -> `code-optimizer` -> `verification-before-completion` |
| 正式项目、跨系统集成、需审计追溯 | `🔴` | `entry-router` -> `karpathy-guidelines` -> `DevFlow Marshal` -> 全流程治理 |

## 支撑资产

- 协作协议：`skills/collaboration-protocol.yaml`
- 知识索引脚本：`scripts/update_knowledge_index.py`
- 知识索引输出：`documents/00-文件树索引.md`、`documents/01-知识库索引.md`
- DevFlow 协议：`skills/inject/devflow-marshal-context.md`
- DevFlow 工具说明：`skills/docs/devflow-run-tooling.md`
- DevFlow 职责映射：`skills/docs/devflow-marshal-subagent-scope.md`
- 外部灵感整合：`skills/docs/external-inspirations.md`
- 永久记忆库：`skills/memory/永久记忆库.md`、`skills/memory/永久记忆库_INDEX.md`

## 设计原则

- 清晰优先于聪明
- 最小可行流程优先于仪式化膨胀
- 先分级，再进流程
- 先约束行为，再扩大执行
- 结构化 handoff 优先于自由发挥
- 稳定知识回仓优先于每次重新搜索
- 先修一致性，再加新 skill
