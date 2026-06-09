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
- `ruvnet/ruflo`：提供插件分层、能力清单、状态页、验证脚本与运行预算的工程化参考
- 本仓库的融合思路：`Karpathy` 负责约束执行风格，`Superpowers` 负责补强关键 workflow，`Ruflo` 负责启发可验证的包级组织，而 `DevFlow` 负责按 `⚪/🟢/🟡/🔴` 控制流程重量

## 模型兼容结论

- 当前这套分层方向是对的，符合主流 coding agent 的工作习惯：先分流，再约束，再执行，再验证
- 但若只保留 `⚪/🟢/🟡/🔴` 和中文层名，对 `Cursor`、`Codex`、`Claude Code` 这类模型不够稳
- 主流模型更吃“显式 level + 显式判定轴 + 明确停点”，不太吃隐喻式命名
- 因此本仓库现在改为双轨表示：对人保留原层名，对模型增加 `L0/L1/L2/L3`

## 分层兼容映射

| 人类层名 | 模型层名 | alias | 适用场景 |
| --- | --- | --- | --- |
| `⚪ 口谕` | `L0` | `direct` | 问答、解释、纯说明、只读判断 |
| `🟢 快奏` | `L1` | `minimal` | 单文件、小范围、低风险执行 |
| `🟡 常奏` | `L2` | `planned` | 多文件、需轻规划、需评审 |
| `🔴 正奏` | `L3` | `formal` | 正式项目、高风险、跨系统、需审计 |

## Spec-First DevFlow 主轴

本仓库按 `Spec/Change 主轴 + DevFlow 治理层 + Skills 执行层 + Memory 沉淀层` 演进。

- `change-id` 是 L2/L3 的需求主键，格式为 `YYYYMMDD-<topic-slug>`。
- `run-id` 是执行实例主键，只负责状态、审计、证据和 gate 报告。
- 需求、设计、任务正文放在 `changes/<change-id>/`。
- DevFlow run 文书只写治理摘要、review 结论和 evidence 引用，不复制完整正文。
- 长期稳定能力契约放在 `specs/<capability>/spec.md`。
- memory 只沉淀稳定结论，不保存一次性 change 正文副本。

发起一个 change 的最小路径：

1. 创建 `changes/<change-id>/`。
2. 从 `changes/templates/` 复制 `proposal.md`、`design.md`、`tasks.md`。
3. 需要治理追踪时创建 run，并把 run 绑定到 `change-id`。
4. 在 `Reviewed=Approved` 前检查 proposal/design/tasks，必要时检查 `spec-delta/`。
5. 交付后写 `delivery.md`，归档时写 `archive.md` 并筛选 memory candidates。

操作细节见 `docs/change-lifecycle.md`。

## 工作流改造进展

当前已经完成第一轮 `spec-first-devflow` 可执行切片：

| 领域 | 当前状态 | 证据 |
| --- | --- | --- |
| Change / Spec 主轴 | 已落地 `changes/`、`changes/templates/`、`specs/` | `changes/templates/*`、`specs/change-lifecycle/spec.md` |
| Change 生命周期 | 已有最小操作手册 | `docs/change-lifecycle.md` |
| 总计划落盘 | 已把融合计划放入 docs 入口 | `docs/spec-first-devflow-fusion-plan.md` |
| DevFlow 工具 | 已支持 change-aware 命令 | `init-change`、`validate-change`、`link-change`、`archive-change`、`sync-spec-index` |
| Run / Change 绑定 | 已用真实 L2 切片跑通 | `devflow/20260609_leroy-skills-garage_spec-first-devflow-fusion-first-slice/` |
| Spec / Change 索引 | 已可刷新索引 | `docs/indexes/02-spec-change-index.md` |
| Planning skills 对齐 | 已默认指向 `changes/<change-id>/proposal.md`、`design.md`、`tasks.md` | `requirement-analyst`、`solution-designer`、`task-planner`、`requirement-locator` |
| Governance skills 对齐 | 已要求 L2/L3 gate 前检查 change artifacts | `entry-router`、`DevFlow Marshal`、`inject/devflow-marshal-context.md` |
| Memory 边界 | 已禁止把 change 正文复制进 memory | `context-archiver`、`permanent-memory`、`memory-sync-gate` |

本轮验证证据：

- `python -m py_compile .\scripts\devflow.py`
- `python .\scripts\devflow.py --help`
- `python .\scripts\devflow.py validate-change --change-id 20260609-spec-first-devflow-fusion-first-slice`
- `python .\scripts\devflow.py validate-run --run-id 20260609_leroy-skills-garage_spec-first-devflow-fusion-first-slice --strict-level minimal`
- `python .\scripts\validate_skills.py`

已知状态：

- `validate-change` 与 DevFlow minimal run gate 已通过。
- 4 个高度重叠的 PUA 风格 skills 已合并为 `high-pressure-pua`，并补齐 `Contract/Fallback/Handoff`。
- `python .\scripts\validate_skills.py` 已通过。
- 下一阶段建议扩展 `specs/governance-lifecycle`、`specs/skill-contract`、`specs/test-evidence`、`specs/memory-boundary`。

## 分级判定轴

- `scope`：只读 / 单文件 / 多文件 / 跨系统
- `risk`：low / medium / high
- `ambiguity`：low / medium / high
- `governance`：none / review_needed / formal_required
- 建议：模型先判定四个轴，再落到 `L0-L3`，最后再映射到 `⚪/🟢/🟡/🔴`


## Ruflo 借鉴边界

- 借鉴：插件包分层、能力 manifest、状态页、验证脚本、预算/安全字段。
- 不借鉴：全量 swarm、后台 worker、自学习运行时、联邦通信、重型 MCP 平台化。
- 合并原则：先让现有 skills 可枚举、可校验、可路由，再考虑新增能力。

## 能力包

能力包定义在 `skills.packages.json`，用于把 flat skills 组织成可验证的最小包：

- `core-flow`：入口分流、执行护栏、最小实现、完成前验证。
- `planning-flow`：方案、任务拆解、上下文和需求定位。
- `quality-gates`：测试证据、合同检查、回归矩阵、代码评审与交付门禁。
- `governance-flow`：DevFlow 状态机、正式编排、记忆门禁和沉淀。
- `implementation-specialists`：调试、优化、TDD、知识维护和日报总结。

运行 `python scripts/validate_skills.py --write-status docs/STATUS.md` 可刷新当前能力状态。

## 完整 Skills 介绍

### Core Flow

日常默认入口，用于最小流程下完成路由、约束、实现与完成前验证。

| Skill | 作用 | 典型触发 | 主要产出 |
| --- | --- | --- | --- |
| `entry-router` | 判断 `L0/L1/L2/L3`、是否需要 `grill-lite`、是否需要 `change-id` | 所有非闲聊任务入口 | level、grade、推荐链路、required checks、artifact mode |
| `grill-lite` | 在需求模糊时先问 5-8 个关键问题 | 验收不清、范围不清、用户说“优化一下” | 澄清答案、假设、stop point |
| `karpathy-guidelines` | 约束执行风格，防止乱猜、过度工程、越界改动 | 编码、调试、优化、评审前 | 简化后的执行原则与风险提醒 |
| `pragmatic-coder` | 做最小、清晰、可验证的实现 | 边界明确的改动 | 代码改动、验证说明 |
| `verification-before-completion` | 完成前要求证据与 `completion_decision` | 宣告完成前 | verification evidence、completion_decision |

### Planning Flow

用于 L2 及以上的需求分析、方案选择、任务拆解与代码落点定位。Spec-first 后默认写入 `changes/<change-id>/`。

| Skill | 作用 | 典型触发 | L2/L3 默认产物 |
| --- | --- | --- | --- |
| `requirement-analyst` | 分析自然语言需求，明确范围、验收、风险与测试建议 | 需求分析、拆任务、列验收 | `changes/<change-id>/proposal.md` |
| `solution-designer` | 给出 2-3 个方案、权衡与推荐路径 | 方案选择、技术选型、需求不清 | `changes/<change-id>/design.md` |
| `task-planner` | 把方案转成 WBS、里程碑、验收与验证计划 | 已有方案，需要执行计划 | `changes/<change-id>/tasks.md` |
| `context-builder` | 构建任务上下文、影响面、依赖、测试面 | 改动前需要理解代码和风险 | context map、impact scope、regression points |
| `requirement-locator` | 从需求定位代码入口、修改点与影响面 | “这功能在哪”“应该改哪里” | affected files/modules，补入 design/tasks |

### Quality Gates

用于把“我觉得完成了”变成可审计证据，覆盖测试、contract、回归、评审与交付门禁。

| Skill | 作用 | 典型触发 | 主要产出 |
| --- | --- | --- | --- |
| `test-evidence-packager` | 执行测试命令并生成标准测试证据 | L2/L3 gate、交付前 | `test_result.json` |
| `skill-contract-checker` | 检查 skill 输出是否满足 contract | L2/L3 gate、流程审查 | `contract_report.json`、gate report |
| `qa-gatekeeper` | 定义测试矩阵、回归范围、发布质量门禁 | 发布前、风险较高改动 | QA gate verdict、测试矩阵 |
| `regression-matrix-builder` | 根据改动范围建立回归测试矩阵 | 核心路径改动、防回归 | P0/P1/P2 regression scope |
| `code-reviewer` | 审查正确性、安全、性能与可维护性 | PR 前、关键改动后 | findings、风险、修复建议 |
| `ai-output-auditor` | 审校 AI 生成内容的一致性、事实与风险 | 方案、代码、文案需要二次审计 | audit verdict、问题清单 |
| `delivery-tracker` | 交付前检查验证路径、回滚与剩余风险 | 准备交付或发布 | delivery checklist、rollback note |

### Governance Flow

用于正式治理、跨阶段编排、状态机、封存与记忆边界控制。

| Skill | 作用 | 典型触发 | 主要产出 |
| --- | --- | --- | --- |
| `devflow-marshal` / `DevFlow Marshal` | DevFlow 治理入口，负责分级、状态机、review gate 与文书纪律 | 走流程、立案、归档、正式治理 | run 状态、gate decision、artifact discipline |
| `dev-flow-orchestrator` | 编排端到端需求到交付流程 | 跨阶段、跨角色、多步骤任务 | workflow plan、handoff |
| `memory-sync-gate` | Delivered 到 Archived 前检查沉淀完整性与边界 | 正式归档、重大改动封存 | memory gate verdict |
| `context-archiver` | 沉淀单次任务摘要、改动、验证、风险 | Bug/功能/优化完成后 | archive record |
| `permanent-memory` | 写入跨任务稳定复用的长期知识 | 约定、接口、命令、回滚策略稳定后 | `memory/永久记忆库.md` 与索引 |

### Implementation Specialists

用于执行阶段的专项能力，按实际问题选择，不要求每次全跑。

| Skill | 作用 | 典型触发 | 主要产出 |
| --- | --- | --- | --- |
| `bug-hunter` | 复现、定位根因、提出修复方案 | Bug 排查、异常定位 | root cause、fix plan |
| `code-optimizer` | 针对明确目标做最小优化或重构 | 性能、可读性、维护性目标明确 | scoped refactor、before/after rationale |
| `tdd-lite` | 为高风险核心逻辑补轻量测试先行 | 核心逻辑、防回归 | minimal tests、red/green evidence |
| `knowledge-keeper` | 维护稳定入口、命令、索引与仓库约定 | 更新索引、沉淀入口信息 | docs/indexes、lookup hints |
| `daily-qa-work-summary` | 汇总当天 Q&A 与完成工作 | 日报、交接、工作回顾 | numbered work summary |

### High-Pressure PUA Skill

这是“防摆烂/防空转”的风格化督促技能，只在代理明显重复失败、想空口收工、拒绝查证或用户明确要求加压时使用。首次尝试且仍在有效推进时不要触发。

| Skill | 模式 | 风格 | 使用边界 |
| --- | --- | --- |
| `high-pressure-pua` | `bahamut` | 巴哈资深网友嘴炮感 | 阻止装懂、基础没做完就乱冲 |
| `high-pressure-pua` | `dcard` | Dcard 阴阳怪气拆台感 | 阻止云判断、重复空转 |
| `high-pressure-pua` | `ptt` | PTT 酸民反串感 | 阻止硬拗同一路线、空口收工 |
| `high-pressure-pua` | `kaobei` | 台湾靠北黑特感 | 阻止装忙、甩锅、不验证 |

原本 4 个高度重叠的 PUA skills 已收敛为一个 skill，统一使用相同 trigger、recovery loop、delivery contract，并通过 `mode` 切换语气。

## 推荐使用链路

### L0 / ⚪ 口谕

- 适用：快问快答、解释、微调、一次性说明
- 处理：主对话直接回答，必要时少量只读工具
- 通常不启用：文书、run 管理、正式治理

### L1 / 🟢 快奏

- 适用：单点修复、小改动、边界明确的实现
- 推荐链路：`entry-router` -> `karpathy-guidelines` -> `knowledge-keeper`（可选） -> `context-builder`（可选） -> `tdd-lite`（高风险时） -> `pragmatic-coder` -> `verification-before-completion`
- 验证：小范围测试、日志检查、诊断检查

### L2 / 🟡 常奏

- 适用：多文件但边界清楚、有轻量规划与评审需求
- 推荐链路：`entry-router` -> `karpathy-guidelines` -> `solution-designer`（如需） -> `task-planner` -> `context-builder` -> `tdd-lite`（核心逻辑时） -> `pragmatic-coder` -> `code-reviewer` / `qa-gatekeeper` -> `verification-before-completion`
- 工具化：可用 `python .\scripts\devflow.py` 维护最小 run 与文书
- 默认停点：`Reviewed=Approved`

### L3 / 🔴 正奏

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
| 问答、解释、一次性说明 | `L0 / ⚪` | 直接回答 |
| 单文件修复、边界明确的小实现 | `L1 / 🟢` | `entry-router` -> `karpathy-guidelines` -> `pragmatic-coder` -> `verification-before-completion` |
| 可复现 Bug 且需防回归 | `L1/L2 / 🟢/🟡` | `entry-router` -> `karpathy-guidelines` -> `bug-hunter` -> `tdd-lite` -> `pragmatic-coder` -> `verification-before-completion` |
| 多文件实现、有轻量规划需求 | `L2 / 🟡` | `entry-router` -> `karpathy-guidelines` -> `task-planner` -> `context-builder` -> `pragmatic-coder` -> `code-reviewer` |
| 核心逻辑重构、需要行为保护 | `L2 / 🟡` | `entry-router` -> `karpathy-guidelines` -> `context-builder` -> `tdd-lite` -> `code-optimizer` -> `verification-before-completion` |
| 正式项目、跨系统集成、需审计追溯 | `L3 / 🔴` | `entry-router` -> `karpathy-guidelines` -> `DevFlow Marshal` -> 全流程治理 |

## 对主流模型的建议

- `Cursor`：更适合 `L0-L2`，偏好明确文件范围、明确验收、少量强制流程
- `Codex`：更适合显式目标、显式约束、显式验证；`L0-L3` 都能用，但不要依赖隐喻术语
- `Claude Code`：对长流程容忍度更高，适合 `L2-L3`，但同样建议先给 level 和 stop point
- 通用建议：永远不要只说“按快奏处理”，最好写成“按 `L1 / 🟢 快奏` 处理，单文件、低风险、验证后结束”

## 支撑资产

- 协作协议：`skills/collaboration-protocol.yaml`
- 知识索引脚本：`scripts/update_knowledge_index.py`
- 知识索引输出：`docs/indexes/00-文件树索引.md`、`docs/indexes/01-知识库索引.md`
- DevFlow 协议：`inject/devflow-marshal-context.md`
- DevFlow 工具说明：`docs/devflow-run-tooling.md`
- DevFlow 职责映射：`docs/devflow-marshal-subagent-scope.md`
- Spec-first DevFlow 总计划：`docs/spec-first-devflow-fusion-plan.md`
- Change lifecycle：`docs/change-lifecycle.md`
- 外部灵感整合：`docs/external-inspirations.md`
- 永久记忆库：`memory/永久记忆库.md`、`memory/永久记忆库_INDEX.md`

## 设计原则

- 清晰优先于聪明
- 最小可行流程优先于仪式化膨胀
- 先分级，再进流程
- 先约束行为，再扩大执行
- 文本与代码文件默认使用 UTF-8（no BOM）
- 能力新增前先更新 `skills.packages.json` 与 `scripts/validate_skills.py` 的验证预期
- 结构化 handoff 优先于自由发挥
- 稳定知识回仓优先于每次重新搜索
- 先修一致性，再加新 skill
