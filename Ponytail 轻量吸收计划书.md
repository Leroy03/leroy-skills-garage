# Ponytail 轻量吸收计划书

## 背景

本计划用于指导后续把 `DietrichGebert/ponytail` 的有效思想吸收到本仓库 skills 体系中。目标不是安装或复制 Ponytail 的完整运行时，而是在现有 `entry-router + karpathy-guidelines + pragmatic-coder + verification-before-completion` 链路中补一个更具体的“复杂度最小化”检查能力。

参考来源：

- `DietrichGebert/ponytail` README：<https://github.com/DietrichGebert/ponytail/blob/main/README.md>
- `DietrichGebert/ponytail` AGENTS：<https://github.com/DietrichGebert/ponytail/blob/main/AGENTS.md>
- Agentic benchmark 说明：<https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-06-18-agentic.md>

## 分析结论

Ponytail 的可取点不在于多一套 agent 平台，而在于把“少写代码”变成可执行顺序：

1. 先判断是否真的需要改。
2. 再找仓库已有实现或配置。
3. 再优先用标准库、平台原生能力、已安装依赖。
4. 最后才写最小实现。
5. 不用“少写代码”牺牲安全、错误处理、可访问性和验证。

这比当前 `karpathy-guidelines` 的“不要过度工程”更具体，但它与现有多个 skill 有重叠：

- `karpathy-guidelines`：已有反乱猜、反过度设计、最小实现原则。
- `pragmatic-coder`：已有最小改动、复用现有分层、完成后验证。
- `code-reviewer`：已有简洁性、可维护性、性能、安全评审。
- `code-optimizer`：已有明确收益下的最小优化。

因此不应新增一个重型流程，也不应把 Ponytail 的 hooks、模式切换、benchmark 命令整套接入。本仓库更适合新增一个轻量 skill，作为实现前和评审时的复杂度检查尺。

## 目标

新增一个轻量 skill：`complexity-minimizer`。

二元验收目标：

- 当任务涉及实现、修复、重构或评审时，agent 能用该 skill 判断是否可以少写代码、少引依赖、少加抽象。
- 新增后仓库结构校验通过，且没有引入额外运行时依赖。

## 范围

### In Scope

- 新增 `skills/complexity-minimizer/SKILL.md`。
- 在 `skills.packages.json` 的 `implementation-specialists` 中登记该 skill。
- 在 `README.md` 的技能地图中补一行定位说明。
- 在 `docs/external-inspirations.md` 中补 Ponytail 的吸收边界。
- 运行索引脚本刷新 `docs/indexes/*`。
- 运行 skills 校验脚本验证结构。

### Out of Scope

- 不安装 Ponytail npm 包或外部插件。
- 不引入 Ponytail hooks、host adapter、mode persistence。
- 不复制 benchmark 框架或展示命令。
- 不新增依赖。
- 不改 DevFlow 状态机。
- 不重写 `karpathy-guidelines`、`pragmatic-coder`、`code-reviewer` 的主体语义。

## 新 Skill 定位

建议名称：`complexity-minimizer`

建议 frontmatter：

```yaml
---
name: "complexity-minimizer"
description: "在实现、修复、重构或评审前检查是否能少写代码：优先复用现有实现、标准库、平台原生能力和已安装依赖，避免不必要抽象、依赖和配置膨胀。"
---
```

职责：

- 负责判断“是否能用更少代码完成同一目标”。
- 负责输出最小实现阶梯和禁止膨胀项。
- 负责在 review 场景指出可删除、可复用、可降级的复杂度。

不负责：

- 不替代 `code-reviewer` 做完整正确性、安全、性能评审。
- 不替代 `pragmatic-coder` 直接改代码。
- 不替代 `code-optimizer` 做性能优化方案。
- 不以少写代码为理由跳过验证、错误处理、安全边界和可访问性要求。

## 建议内容结构

`skills/complexity-minimizer/SKILL.md` 建议控制在 120 行以内，只放核心规则。

推荐章节：

- `目标`
- `何时调用`
- `复杂度最小化阶梯`
- `不可牺牲项`
- `输出要求`
- `Contract`
- `Fallback`
- `Handoff`

核心阶梯建议写成：

1. `no_change`：是否不需要改代码，只需配置、文档或说明。
2. `reuse_existing`：是否已有函数、组件、脚本、测试夹具可复用。
3. `use_platform`：是否可用标准库、框架内置能力、数据库/CLI 原生命令。
4. `use_installed_dependency`：是否已有依赖能直接覆盖需求。
5. `write_small_code`：才写最小代码，不新增未来扩展点。

输出建议：

- `decision`：`no_change | reuse_existing | use_platform | use_installed_dependency | write_small_code`
- `reasoning`：为什么选择该层级。
- `reuse_targets`：可复用的文件、函数、命令或依赖。
- `scope_limits`：明确不做什么。
- `must_keep`：安全、验证、错误处理、可访问性等不可牺牲项。
- `handoff`：下一步交给哪个 skill。

## WBS

| 步骤 | 文件 | 动作 | 产物 | 依赖 |
| --- | --- | --- | --- | --- |
| 1 | `skills/complexity-minimizer/SKILL.md` | 新增轻量 skill | 可触发的 SKILL.md | 本计划 |
| 2 | `skills.packages.json` | 加入 `implementation-specialists` | 包校验可识别 | 步骤 1 |
| 3 | `README.md` | 技能地图补定位 | 用户可理解入口 | 步骤 1 |
| 4 | `docs/external-inspirations.md` | 记录 Ponytail 吸收边界 | 外部灵感可追溯 | 步骤 1 |
| 5 | `docs/indexes/*` | 运行索引脚本刷新 | 索引包含新 skill | 步骤 1 |
| 6 | 校验命令 | 运行结构校验 | 通过或列出错误 | 步骤 1-5 |

## 推荐修改细节

### 1. 新增 `skills/complexity-minimizer/SKILL.md`

必须满足：

- frontmatter 有 `name` 和 `description`。
- 包含 `## Contract`、`## Fallback`、`## Handoff`。
- 使用 UTF-8 without BOM。
- 不包含额外 README、CHANGELOG、QUICK_REFERENCE。

### 2. 更新 `skills.packages.json`

只在 `implementation-specialists.skills` 追加：

```json
"complexity-minimizer"
```

不新增 package，避免能力包膨胀。

### 3. 更新 `README.md`

在“实作与分析”区域补一行：

```md
- `complexity-minimizer`：实现或评审前检查是否能复用现有实现、标准库、平台原生能力或已安装依赖，避免不必要代码和抽象。
```

### 4. 更新 `docs/external-inspirations.md`

新增 Ponytail 小节，建议包含：

- 借鉴：复杂度最小化阶梯、先复用后新写、不可牺牲安全与验证。
- 不借鉴：hooks、mode runtime、benchmark 命令、外部插件安装。
- 落地：映射到 `complexity-minimizer`，由 `entry-router` 后按需触发。

### 5. 刷新索引

执行：

```powershell
python scripts/update_knowledge_index.py
```

预期变更：

- `docs/indexes/00-文件树索引.md`
- `docs/indexes/01-知识库索引.md`

### 6. 验证

执行：

```powershell
python scripts/validate_skills.py --pack implementation-specialists
python scripts/validate_skills.py
```

通过条件：

- 无 UTF-8 BOM。
- 新 skill frontmatter 通过。
- 新 skill 包含 `Contract/Fallback/Handoff`。
- `implementation-specialists` 无 unknown skills。

## 验收标准

- `skills/complexity-minimizer/SKILL.md` 存在，且职责边界不超过本计划。
- `skills.packages.json` 只更新现有 `implementation-specialists` 包，不新增包。
- `README.md` 和 `docs/external-inspirations.md` 只补必要说明，不重写旧章节。
- 索引刷新后能在知识库索引中看到 `complexity-minimizer`。
- 两条验证命令通过。

## 风险与约束

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 与 `karpathy-guidelines` 重复 | skill 边界变模糊 | 让 `karpathy-guidelines` 保持通用护栏，`complexity-minimizer` 只管少写代码阶梯 |
| 与 `code-reviewer` 重复 | review 输出变散 | 明确它只输出复杂度问题，不做完整评审 |
| 过度吸收 Ponytail | 仓库膨胀 | 禁止 hooks、runtime、benchmark 命令和新增依赖 |
| 少写代码被误用 | 安全和验证被弱化 | 在 skill 中列 `must_keep`：安全、错误处理、验证、可访问性 |

## 后续执行停点

建议一次只做到以下停点：

1. 新增 skill 和最小文档更新。
2. 刷新索引。
3. 校验通过。
4. 停止，不继续扩展 hooks、命令、benchmark 或自动路由。

若后续真实使用中发现该 skill 经常被调用，再考虑下一轮小改：

- 在 `entry-router` 的 L1/L2 推荐链中按条件提及它。
- 在 `code-reviewer` 的简洁性维度中增加 handoff。
- 增加 1 个示例输入输出，但不超过 40 行。

## completion_decision

当前计划只建议做最小新增，不建议引入外部运行时。后续可按本文件执行一轮 L1/L2 之间的小改，完成后以 `validate_skills.py` 结果作为验收证据。
