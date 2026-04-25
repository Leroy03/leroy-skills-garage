---
name: "context-builder"
description: "智能构建任务上下文：相关文件、依赖关系、测试覆盖、影响分析。为其他 skills 提供可执行的上下文。"
collaboration_protocol: ".trae/skills/collaboration-protocol.yaml"
version: "1.0.0"
dependencies:
  - knowledge-keeper
---

# Context-Builder（上下文构建）

## 目标
把“要改什么”转成“需要看的文件 + 影响范围 + 回归点”，用于安全地写代码、修 Bug、做评审或优化。

## 持久上下文优先（减少 token/耗时）
- 优先读取项目内索引，而不是每次从头扫描：
  - `.trae/documents/00-文件树索引.md`（目录与模块线索）
  - `.trae/documents/01-知识库索引.md`（文档/API/表/配置/工具索引）
- 先尝试从 `knowledge-keeper` 拿 `entry_points` / `related_files` / `commands`
- 当索引明显过期、缺失或无法覆盖任务时，再扩大到代码搜索/依赖分析
- 更新索引：`python .\.trae\scripts\update_knowledge_index.py`

## 适用场景
- 写代码前需要确认入口/依赖/影响面
- 排查问题需要定位调用链与相关配置
- 评审/优化需要掌握模块结构与测试情况
- 显式调用：`$context-builder <文件/类/功能>`

## 不做
- 直接输出实现代码（交给 pragmatic-coder）
- 给优化/重构方案（交给 code-optimizer）
- 代替 `knowledge-keeper` 长期维护知识索引

## 输入
- target：文件路径/类名/方法名/模块名/功能描述（至少一个）
- task_type：implement | debug | optimize | review（可选）
- hints：来自 knowledge-keeper 的 entry/related_files（可选）

## 输出（优先 JSON）
```json
{
  "target": "string",
  "core_files": ["string"],
  "dependencies": { "upstream": ["string"], "downstream": ["string"] },
  "test_files": ["string"],
  "impact_scope": "low|medium|high",
  "risk_level": "low|medium|high",
  "suggestions": ["string"]
}
```

## 构建要点（贴近本仓库）
- 分层链路：Controller -> Service -> Mapper -> XML/DB
- 配置联动：`config/**`、`src/main/resources/config/**`、以及相关 `@Value/@ConfigurationProperties`
- 前端调用（如涉及）：`src/main/resources/static/**` 里对后端接口的引用
- 测试：优先找 `src/test/**` 下的单测/集成测配置（如 application-unit-test.yaml）

## 调用方式
- `$context-builder` + 目标（文件/类/功能）+（可选）线索/约束
