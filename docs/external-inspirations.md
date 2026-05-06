# External Inspirations

本仓库当前主要吸收了两个外部项目的思路：

- `obra/superpowers`
- `forrestchang/andrej-karpathy-skills`
- `ruvnet/ruflo`
- `mattpocock/skills`
- `harness`（方法论层）
- `hermes agent`（任务编排层）

## 共同点

- 都强调“不要直接冲进实现”，要先澄清任务与成功标准
- 都反对 ad-hoc 工作方式，提倡可复用流程
- 都强调验证优先，不能只凭“感觉做完了”
- 都把复杂度控制视为一等公民

## 主要差异

### Superpowers
- 强在 workflow 编排
- 强在技能触发、TDD、调试、review、并行 agent、branch/worktree 等工程动作
- 适合完整开发流水线
- 风险是照搬后流程容易偏重

### Karpathy Guidelines
- 强在行为约束
- 重点解决：乱猜、过度设计、越界改动、没有成功标准
- 非常轻量，适合做全局默认 guardrails
- 风险是只有约束，没有完整 workflow 编排

### Ruflo
- 强在插件化组织、能力清单、状态页、验证脚本和运行预算
- 适合参考其“轻安装 vs 全量运行时”的分层思路
- 风险是全量照搬会把 skills 仓库拖成重型 agent 平台
- 本仓库只吸收结构治理能力，不引入 swarm、自学习、联邦通信等运行时平台能力

### Matt Pocock Skills
- 强在“小 skill、可组合、真实工程反馈回路”而非重流程主导
- 重点能力包括：前置澄清（grilling）、共享领域语言（`CONTEXT.md`）、ADR 沉淀、`tdd` 与 `diagnose` 的工程循环
- 适合参考其“先对齐再编码、先反馈再扩张”的节奏控制
- 风险是若全量照搬其命令体系，会与现有 `entry-router + DevFlow Marshal` 重叠

### Harness（方法论参考）
- 强在“验证驱动 + 可重复执行”的工程闭环思维（而非单点技巧）
- 适合吸收为：明确输入输出 contract、稳定检查命令、失败可复现
- 风险是若把 harness 设计成重平台，会与本仓库“轻量 skill 组合”目标冲突

### Hermes Agent（编排参考）
- 强在任务路由、阶段化执行与多角色协作的编排视角
- 适合吸收为：先分流再执行、阶段停点、失败回退与重试策略
- 风险是照搬后可能把个人流程拉向多 agent 重编排，增加维护负担

## 本仓库的融合策略

### 入口层
- 引入 `entry-router`
- 所有非 trivial 任务先做 `⚪/🟢/🟡/🔴` 分流
- 目标：先选最轻可行流程，而不是默认重治理

### 约束层
- 引入 `karpathy-guidelines`
- 作为实现、调试、评审、优化前的默认护栏
- 目标：减少乱猜、过度工程化与无关改动

### 验证层
- 引入 `verification-before-completion`
- 在声明“完成”前要求最小证据
- 借鉴 Ruflo 的状态页与 verify 脚本，补充 `scripts/validate_skills.py` 与 `docs/STATUS.md`
- 目标：把验证闭环做轻，但不缺席
- 结合 Matt 的反馈回路思想，引入 `tdd-lite` 作为“高风险才启用”的轻量测试先行机制

### 治理层
- 保留 `DevFlow Marshal`
- 只让 `🟡/🔴` 进入明显流程化路径
- 目标：把审计能力集中在高风险场景，而不是污染全部请求
- 吸收 Hermes 的阶段化思想，但保持单人可执行，不引入复杂多代理依赖

## 不照搬的部分

- 不直接复制 `superpowers` 的全套 slash commands
- 不默认要求 worktree / subagent / TDD 全量流程
- 不把所有实现都强制升级成多阶段审批
- 不引入 Ruflo 的全量 MCP server、swarm、后台 worker、自学习记忆和跨机器联邦
- 不直接复制 Matt 的完整命令生态（如 `grill-with-docs`、`triage`、`to-prd` 等）
- 不强制每个项目都维护完整 `CONTEXT.md + docs/adr` 文档体系
- 不引入 Harness/Hermes 的重运行时或平台级控制面，只保留方法论与最小落地规则

## 结果目标

- `⚪/🟢`：像 Karpathy，一样克制、简单、明确
- `🟡/🔴`：借 Superpowers 的 workflow 能力，但由分级控制复杂度
- 高风险实现：吸收 Matt 的测试反馈哲学，用 `tdd-lite` 做最小必要保护

## Matt 技术痕迹盘点（当前状态）

### 已融入
- `tdd` 思想的轻量化落地：`skills/tdd-lite/SKILL.md`
- “小 skill、可组合、不过度流程化”的总方向：`entry-router` 的轻重分级
- 将验证作为完成前硬步骤：`verification-before-completion`

### 部分融入
- 共享领域语言思路已有对应能力，但未采用 Matt 的原生命名与模板：
  - `knowledge-keeper`
  - `context-builder`
  - `permanent-memory`

### 尚未明显融入
- grilling 双技能（`grill-me` / `grill-with-docs`）的专门入口
- `diagnose` 风格的标准化排查循环（目前主要由 `bug-hunter` 覆盖）
- `to-prd` / `triage` 这类 issue-first 交付链路

## Harness / Hermes 痕迹盘点（当前状态）

### 代码与文档直接痕迹
- 当前仓库未检索到 `harness`、`hermes` 关键字的直接引用记录（无显式命名痕迹）。

### 可能的间接吸收
- Harness 风格：`scripts/validate_skills.py`、`skills/*` 的 Contract/Fallback/Handoff 结构
- Hermes 风格：`entry-router` 的分流与停点、`DevFlow Marshal` 的阶段状态机

### 建议补位（保持轻量）
- 在 `README.md` 或本文件新增“术语映射”小节：说明 Harness/Hermes 思想在本仓库对应到哪些 skills
- 若后续新增相关 skill，优先使用 `*-lite` 形式，避免重编排

## 三省六部逻辑（治理映射）

本仓库已具备“三省六部”的可落地雏形，建议统一按以下映射执行：

### 三省（决策与门禁）
- **中书省（起草方案）**：`requirement-analyst`、`solution-designer`、`task-planner`
- **门下省（审议封驳）**：`ai-output-auditor`、`qa-gatekeeper`、`skill-contract-checker`
- **尚书省（执行统筹）**：`DevFlow Marshal`、`delivery-tracker`

### 六部（执行职能）
- **吏部（任务组织）**：`entry-router`、`context-builder`
- **户部（证据与资产）**：`test-evidence-packager`、`knowledge-keeper`、`permanent-memory`
- **礼部（规范与约束）**：`karpathy-guidelines`、`verification-before-completion`
- **兵部（故障与风险）**：`bug-hunter`、`code-reviewer`
- **刑部（质量门禁）**：`qa-gatekeeper`、`skill-contract-checker`
- **工部（实现与优化）**：`pragmatic-coder`、`code-optimizer`、`tdd-lite`

### 落地规则（轻量版）
- `⚪/🟢`：以“六部直办”为主，必要时最小门禁，不引入完整审议流程。
- `🟡`：必须经过“中书拟案 -> 门下审议 -> 尚书统筹”，默认停在 `Reviewed=Approved`。
- `🔴`：执行完整状态机，并保留审计与封存证据。
- 若用户明确提及“正式/立案/归档/走流程”，一律按 `🔴`。
