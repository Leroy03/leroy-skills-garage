---
name: "code-reviewer"
description: "代码评审：正确性、可维护性、性能与安全性审查，输出可执行的修改建议。"
collaboration_protocol: ".trae/skills/collaboration-protocol.yaml"
version: "1.0.0"
dependencies:
  - context-builder
---

# Code-Reviewer（代码评审）

## 目标
对指定代码做评审，给出问题清单与可执行建议，避免泛泛而谈。

## 适用场景
- 评审一段改动/一组文件/一个模块
- 上线前安全审计或风险点梳理
- 显式调用：`$code-reviewer`

## 不做
- 直接实现改动（交给 pragmatic-coder）
- 做大规模重构方案（交给 code-optimizer）

## 输入
- files：要评审的文件（或 PR diff/关键片段）
- context：来自 context-builder 的上下文（依赖、影响面、回归点）
- focus：可选，指定评审重点（正确性/性能/安全/可维护性）

## 输出
- overall_score：0–100
- issues：按严重级别输出（critical/high/medium/low），每条包含 location + 描述 + 建议
- strengths：做得好的点（可选）
- recommendations：按优先级排序的修复建议（可选）

## 评审维度（默认）
- 正确性：空值/边界/异常路径/并发与事务
- 安全性：敏感信息、鉴权遗漏、注入风险、反序列化风险
- 性能：N+1、全表扫描、循环 IO、无界集合增长
- 可维护性：重复逻辑、职责过重、命名与分层是否清晰

## 调用方式
- `$code-reviewer` + 文件/改动范围 +（可选）评审重点
