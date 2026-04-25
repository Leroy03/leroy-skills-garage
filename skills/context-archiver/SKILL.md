---
name: "context-archiver"
description: "沉淀本次需求/问题的关键信息：结论、决策理由、改动点与验证方式，便于复用与追溯。"
version: "1.0.0"
dependencies:
  - knowledge-keeper
---

# Context-Archiver（上下文沉淀）

## 目标
把一次协作的“关键信息”沉淀成一条可复用记录：下次遇到同类问题能快速定位并复用方案。

## 适用场景
- Bug 修复完成后：记录根因、改动点、验证方式与回归范围
- 功能实现完成后：记录需求、关键取舍、影响范围与验证方式
- 优化/重构完成后：记录问题点、最小改动方案与效果（如可量化）
- 显式调用：`$context-archiver`

## 不做
- 维护“知识图谱/智能推荐/存储结构/ADR”体系化建设
- 自动生成或强制落盘大量文档
- 代替 `permanent-memory` 维护跨任务长期稳定知识

## 输入
- title：一句话标题（必填）
- type：feature | bugfix | optimization | review（必填）
- summary：一句话结论（必填）
- details：关键细节（选填，建议 5–10 行以内）
  - root_cause：根因（如有）
  - decision：关键取舍与理由（如有）
  - changes：改动文件与要点（file + 简述）
  - verification：如何验证与回归范围
  - risks：风险与回滚点（如有）

## 输出（默认 JSON）
```json
{
  "title": "string",
  "type": "feature|bugfix|optimization|review",
  "summary": "string",
  "changes": [{"file": "string", "note": "string"}],
  "verification": ["string"],
  "risks": [{"risk": "string", "mitigation": "string"}]
}
```

## 与 permanent-memory 的边界
- `context-archiver`：记录本次任务的结论、改动点、验证与风险
- `permanent-memory`：只沉淀跨任务稳定复用的约定、接口、命令、回滚策略
- 当一条结论满足“下次大概率还会复用”时，再升级写入 `memory/永久记忆库.md`

## 调用方式
- `$context-archiver` + 标题 +（可选）上述细节
