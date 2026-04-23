---
name: "pragmatic-coder"
description: "从简编码：清晰 > 聪明，够用 > 完美，最小改动且可验证。"
collaboration_protocol: ".trae/skills/collaboration-protocol.yaml"
version: "1.0.0"
dependencies:
  - context-builder
---

# Pragmatic-Coder（务实编码）

## 目标
在不引入新复杂度的前提下完成需求实现或修复：改动小、逻辑清晰、可验证、可回滚。

## 适用场景
- 用户明确要“实现/新增功能/修复并改代码”
- workflow 已给出任务清单或修复方案
- 显式调用：`$pragmatic-coder`

## 不做
- 为了“优雅”做大改或大规模抽象
- 引入新框架/新中间件解决局部问题
- 发散式补齐所有未来扩展点

## 输入
- task：要做的具体改动（功能点/修复点）
- context：来自 context-builder 的上下文（核心文件、依赖、回归点）
- constraints：兼容性/性能/禁止改动点（可选）

## 输出
- 变更的文件与关键改动点
- 最小验证步骤（如何跑/看什么日志/回归哪些路径）

## 实现约束（默认）
- 优先复用现有分层与写法（Controller/Service/Mapper/DTO/Entity）
- 日志不输出敏感信息（密码、token、sessionid 等）
- 只在需要时新增测试，优先沿用现有测试框架与项目脚手架

## 调用方式
- `$pragmatic-coder` + 任务描述 +（可选）目标文件/模块 + 约束
