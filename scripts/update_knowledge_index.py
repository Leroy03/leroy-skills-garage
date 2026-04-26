#!/usr/bin/env python3
"""Generate lightweight repository knowledge indexes for skill consumption."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "documents"
IGNORE_DIRS = {".git", ".venv", "__pycache__", "node_modules"}


def iter_tree(base: Path, depth: int = 2) -> list[str]:
    lines: list[str] = []

    def walk(path: Path, prefix: str, current_depth: int) -> None:
        if current_depth > depth:
            return
        children = sorted(
            [
                child
                for child in path.iterdir()
                if child.name not in IGNORE_DIRS
            ],
            key=lambda p: (p.is_file(), p.name.lower()),
        )
        for child in children:
            marker = "/" if child.is_dir() else ""
            lines.append(f"{prefix}- `{child.relative_to(ROOT).as_posix()}{marker}`")
            if child.is_dir():
                walk(child, prefix + "  ", current_depth + 1)

    walk(base, "", 1)
    return lines


def collect_skill_entries() -> list[str]:
    entries: list[str] = []
    for skill_file in sorted(ROOT.glob("skills/*/SKILL.md"), key=lambda p: p.parent.name.lower()):
        skill_dir = skill_file.parent
        entries.append(f"## `{skill_dir.name}`")
        entries.append(f"- 路径：`{skill_file.relative_to(ROOT).as_posix()}`")
        first_lines = skill_file.read_text(encoding="utf-8").splitlines()
        description = ""
        for index, line in enumerate(first_lines):
            if not line.startswith("description:"):
                continue
            value = line.replace("description:", "", 1).strip()
            if value in {">", ">-", "|", "|-"}:
                folded: list[str] = []
                for extra in first_lines[index + 1 :]:
                    if not extra.startswith("  "):
                        break
                    folded.append(extra.strip())
                description = " ".join(folded).strip()
            else:
                description = value.strip('"')
            break
        if description:
            entries.append(f"- {description}")
        entries.append("")
    return entries


def collect_support_entries() -> list[str]:
    lines = [
        "## 支撑资源",
        "- DevFlow 协议：`skills/inject/devflow-marshal-context.md`",
        "- DevFlow 工具：`scripts/devflow.py`",
        "- DevFlow 文档：`skills/docs/devflow-run-tooling.md`、`skills/docs/devflow-marshal-subagent-scope.md`",
        "- 记忆库：`skills/memory/永久记忆库.md`、`skills/memory/永久记忆库_INDEX.md`",
        "- 协作协议：`skills/collaboration-protocol.yaml`",
        "",
    ]
    return lines


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    tree_content = "\n".join(
        [
            "# 文件树索引",
            "",
            "该索引用于帮助 `knowledge-keeper`、`context-builder` 等 skills 快速了解仓库结构。",
            "",
            *iter_tree(ROOT),
        ]
    )
    write(DOCS_DIR / "00-文件树索引.md", tree_content)

    knowledge_content = "\n".join(
        [
            "# 知识库索引",
            "",
            "该索引汇总当前仓库中的 skills 与支撑文档入口。",
            "",
            *collect_skill_entries(),
            *collect_support_entries(),
        ]
    )
    write(DOCS_DIR / "01-知识库索引.md", knowledge_content)


if __name__ == "__main__":
    main()
