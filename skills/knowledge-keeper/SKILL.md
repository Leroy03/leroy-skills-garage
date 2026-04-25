---
name: "knowledge-keeper"
description: "Maintains reusable project knowledge indexes and lookup hints. Invoke when another skill needs stable entry points, related files, commands, or repo conventions."
---

# Knowledge-Keeper（知识索引与检索）

## 目标
为其他 skills 提供稳定、可复用的仓库知识入口，避免每次都从零扫描代码。

## 适用场景
- 需要快速确认模块入口、相关文件、常用命令、流程文档位置
- `context-builder`、`bug-hunter`、`context-archiver` 需要先拿到稳定线索
- 显式调用：`$knowledge-keeper`

## 不做
- 不直接输出实现代码
- 不代替详细设计、任务拆解或代码评审
- 不把一次性临时线索当成长期事实写入索引

## 输入
- target：文件/模块/功能/问题描述（至少一个）
- intent：lookup | summarize | handoff（可选）
- hints：已知路径、关键词、命令（可选）

## 输出（优先 JSON）
```json
{
  "target": "string",
  "entry_points": ["string"],
  "related_files": ["string"],
  "commands": ["string"],
  "docs": ["string"],
  "conventions": ["string"],
  "confidence": "high|medium|low"
}
```

## 知识来源优先级
1. `.trae/documents/01-知识库索引.md`
2. `.trae/documents/00-文件树索引.md`
3. `README.md`、`docs/**`、`memory/**`
4. 必要时再回到代码搜索

## 维护规则
- 只沉淀稳定入口、稳定命令、稳定约定
- 索引失效时，先更新索引再继续下游工作
- 如果没有足够证据，明确标记 `confidence=low`

## 索引刷新
- 使用：`python .\.trae\scripts\update_knowledge_index.py`
- 刷新后应更新 `.trae/documents/00-文件树索引.md`
- 刷新后应更新 `.trae/documents/01-知识库索引.md`
