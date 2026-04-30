---
name: "requirement-locator"
description: "根据用户的需求/问题快速定位代码中的相关功能与修改位置。用户要求“定位功能/查找应该改哪里/给出代码链接与入口”时调用。"
---

# 需求分析定位

## 目标
从自然语言需求或问题出发，快速在代码库中定位相关功能的入口、关键实现与应修改的位置，并给出可点击的代码链接与最小改动建议。

## 适用场景（触发条件）
- 用户问：“这个功能在哪里实现？”
- 用户要求：“帮我找应该改哪段代码？”
- 新增/优化一个能力，需要找到合适的落点（控制器/服务/任务/SQL）。

## 输入
- 需求/问题描述（必填）
- 关键词或万得代码/接口路径（可选）
- 目标模块或目录范围（可选）

## 输出
- 入口文件与关键实现的短清单（含理由）
- 推荐的修改位置（函数/类/方法）与影响面
- 可点击的代码链接（file:///absolute/path#Lx-Ly）
- 最小改动建议与下一步动作

## 工作流程
1. 语义解析需求，抽取领域关键词、端点、类名线索
2. 高层级检索控制器/服务/调度任务/SQL脚本，形成候选
3. 追踪调用链，识别读写路径与边界（事务、缓存、外部依赖）
4. 生成入口与关键点清单，标注推荐修改点与理由
5. 输出代码链接与下一步实施建议（保持最小改动原则）

## 返回格式（示例）
- 入口：Controller/Service/Task/SQL
- 代码链接：如 [HoldingReportTask](file:///d:/Wind.Fund.FullStackStrategy/release/src/src/main/java/cn/com/wind/fund/fullstackstrategy/ems/core/schedule/HoldingReportTask.java#L1-L120)
- 推荐修改点：方法名/行区间
- 影响面：事务边界/并发/幂等/日志/测试
- 下一步：实现步骤与验证方式

## 使用示例
输入：“持仓日报重复生成如何处理？”
输出：定位到定时任务与唯一键策略，给出幂等实现建议与代码链接。

## 常见问题
- 检索范围太广：可提供目录范围缩小搜索
- 结果不准确：补充更多业务关键词或具体调用示例
- 链接打不开：需在本 IDE 内点击 file:/// 链接

## Contract

- `inputs_required`
  - `requirement_or_question`
  - `keywords`（可选）
  - `target_scope`（可选）
- `outputs_required`
  - `entry_points`
  - `candidate_change_points`
  - `impact_scope`
  - `next_actions`
- `evidence_files`
  - 无硬性文件（定位型 skill）

## Fallback

- 若定位不唯一：输出 Top-N 候选并附置信度与排查顺序。

## Handoff

- 默认交接：`context-builder`（补上下文）或 `pragmatic-coder`（执行改动）。
