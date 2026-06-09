# Change Lifecycle Spec

## Purpose

L2/L3 work uses `change-id` as the requirement key and `run-id` as the execution instance key.

## Required Artifacts

For each repository-backed change:

- `changes/<change-id>/proposal.md`
- `changes/<change-id>/design.md`
- `changes/<change-id>/tasks.md`

When delivering or archiving:

- `changes/<change-id>/delivery.md`
- `changes/<change-id>/archive.md`
- optional `changes/<change-id>/spec-delta/*.md`

## Rules

- `change-id` format: `YYYYMMDD-<topic-slug>`.
- `run-id` records state, gate decisions, evidence, and audit events.
- Run artifacts summarize governance state and link to change artifacts.
- Change artifacts hold the requirement, design, task, delivery, and archive body.
- Memory stores stable conclusions only, not change artifact copies.

## Gate Requirements

Before `Reviewed=Approved` for L2/L3 repository-backed work:

- proposal exists and has scope plus success criteria.
- design exists and records the selected option.
- tasks exists and has executable tasks plus verification plan.
- spec delta exists when stable capability contracts change.

