---
name: "bug-hunter"
description: "专业 Debug：日志分析、复现路径、根因定位、修复方案。只专注定位问题并提出解决方案。"
collaboration_protocol: ".trae/skills/collaboration-protocol.yaml"
version: "1.0.0"
dependencies:
  - knowledge-keeper
  - context-builder
  - pragmatic-coder
---

# Bug-Hunter（问题定位）

## 目标
基于现象、日志与代码，定位根因并给出 2–3 个修复方案（含推荐与风险）。

## 适用场景
- 报错/异常/堆栈/日志定位（如 NPE、超时、SQL 异常、序列化异常）
- 功能不符合预期且可描述复现路径
- 显式调用：`$bug-hunter`

## 不做
- 需求方案设计（交给 solution-designer）
- 优化/重构（交给 code-optimizer）

## 需要的输入（信息越全越快）
- 现象：期望 vs 实际
- 日志/堆栈：完整异常堆栈、关键 error 日志（脱敏）
- 复现步骤：触发条件、入参、环境（dev/test/prod）

## 输出
- root_cause：文件/行号/原因（如果能定位到）
- solutions：2–3 个修复方案（影响面、风险、回滚点）
- verification_plan：怎么验证 + 需要回归哪些路径

## 常见定位切入点（本仓库）
- Controller/Service/Mapper 分层调用链
- MyBatis SQL 与 Mapper.xml 映射
- 配置差异：`config/**`、`src/main/resources/config/**` 的 profile

## 调用方式
- `$bug-hunter` + 现象描述 +（可选）日志/堆栈/复现步骤
