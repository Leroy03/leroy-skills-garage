#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal DevFlow run helper aligned with skills/inject/devflow-marshal-context.md section 9."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ARTIFACT_MAP = {
    "plan": "01_plan.md",
    "review": "02_review.md",
    "dispatch": "03_dispatch.md",
    "delivery": "04_delivery.md",
    "postmortem": "05_postmortem.md",
}

# Protocol states (plus Rejected for gate failure).
STATUSES = frozenset(
    {
        "Draft",
        "Planned",
        "Reviewed",
        "Rejected",
        "Dispatched",
        "Running",
        "Delivered",
        "Archived",
    }
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _slug(s: str, max_len: int = 48) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", s, flags=re.I)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s:
        s = "topic"
    return s[:max_len].rstrip("-")


def devflow_root() -> Path:
    p = os.environ.get("DEVFLOW_ROOT", "").strip()
    base = Path(p).resolve() if p else (Path.cwd() / "devflow")
    base.mkdir(parents=True, exist_ok=True)
    return base


def find_run_dir(run_id: str) -> Path:
    root = devflow_root()
    direct = root / run_id
    if direct.is_dir() and (direct / "run.json").is_file():
        return direct
    for child in root.iterdir():
        if not child.is_dir():
            continue
        rj = child / "run.json"
        if not rj.is_file():
            continue
        try:
            data = json.loads(rj.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("run_id") == run_id:
            return child
    raise SystemExit(f"run not found: {run_id!r} under {root}")


def cmd_create_run(args: argparse.Namespace) -> None:
    root = devflow_root()
    d = date.today().strftime("%Y%m%d")
    rp = _slug(args.project, 32)
    rt = _slug(args.topic, 40)
    run_id = f"{d}_{rp}_{rt}"
    run_dir = root / run_id
    n = 2
    while run_dir.exists():
        run_id = f"{d}_{rp}_{rt}-{n}"
        run_dir = root / run_id
        n += 1
    run_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_id": run_id,
        "project": args.project,
        "topic": args.topic,
        "status": "Draft",
        "created_at": _utc_now_iso(),
        "updated_at": _utc_now_iso(),
        "path": str(run_dir.resolve()),
    }
    (run_dir / "run.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    audit_line = {
        "ts": _utc_now_iso(),
        "actor": "devflow.py",
        "from_status": None,
        "to_status": "Draft",
        "note": "create-run",
    }
    (run_dir / "run.json.audit").write_text(
        json.dumps(audit_line, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(run_id)
    print(str(run_dir.resolve()))


def cmd_get_run(args: argparse.Namespace) -> None:
    run_dir = find_run_dir(args.run_id)
    data = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_write_artifact(args: argparse.Namespace) -> None:
    art = args.artifact.lower()
    if art not in ARTIFACT_MAP:
        raise SystemExit(f"unknown artifact: {args.artifact!r}; expected one of {sorted(ARTIFACT_MAP)}")
    run_dir = find_run_dir(args.run_id)
    name = ARTIFACT_MAP[art]
    try:
        body = sys.stdin.buffer.read().decode("utf-8")
    except UnicodeDecodeError as e:
        raise SystemExit(f"stdin must be valid UTF-8: {e}") from e
    if body and not body.endswith("\n"):
        body += "\n"
    (run_dir / name).write_text(body, encoding="utf-8")
    print(f"wrote {run_dir / name}")


def cmd_update_status(args: argparse.Namespace) -> None:
    if args.status not in STATUSES:
        raise SystemExit(f"invalid status {args.status!r}; expected one of {sorted(STATUSES)}")
    run_dir = find_run_dir(args.run_id)
    rj = run_dir / "run.json"
    data: dict[str, Any] = json.loads(rj.read_text(encoding="utf-8"))
    old = data.get("status")
    data["status"] = args.status
    data["updated_at"] = _utc_now_iso()
    rj.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit_path = run_dir / "run.json.audit"
    audit_line = {
        "ts": _utc_now_iso(),
        "actor": args.actor,
        "from_status": old,
        "to_status": args.status,
        "note": args.note,
    }
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(audit_line, ensure_ascii=False) + "\n")
    print("ok")


def cmd_validate_run(args: argparse.Namespace) -> None:
    run_dir = find_run_dir(args.run_id)
    rj = run_dir / "run.json"
    data = json.loads(rj.read_text(encoding="utf-8"))
    status = data.get("status", "")
    errors: list[str] = []
    if status == "Planned" and not (run_dir / "01_plan.md").is_file():
        errors.append("status Planned but 01_plan.md missing")
    if status == "Reviewed":
        p = run_dir / "02_review.md"
        if not p.is_file():
            errors.append("status Reviewed but 02_review.md missing")
        else:
            txt = p.read_text(encoding="utf-8", errors="replace")
            if "PASS" not in txt and "FAIL" not in txt:
                errors.append("02_review.md should mention PASS or FAIL")
    if status == "Dispatched" and not (run_dir / "03_dispatch.md").is_file():
        errors.append("status Dispatched but 03_dispatch.md missing")
    if status == "Running":
        for fname in ("03_dispatch.md", "04_delivery.md"):
            if not (run_dir / fname).is_file():
                errors.append(f"status Running but {fname} missing")
    if status == "Delivered":
        for fname in ("03_dispatch.md", "04_delivery.md"):
            if not (run_dir / fname).is_file():
                errors.append(f"status Delivered but {fname} missing")
    if status == "Archived":
        for fname in ("03_dispatch.md", "04_delivery.md", "05_postmortem.md"):
            if not (run_dir / fname).is_file():
                errors.append(f"status Archived but {fname} missing")
    if errors:
        raise SystemExit("validate failed:\n- " + "\n- ".join(errors))
    print("validate ok")


def main() -> None:
    p = argparse.ArgumentParser(description="DevFlow Marshal minimal run tooling")
    sub = p.add_subparsers(dest="cmd", required=True)

    c1 = sub.add_parser("create-run", help="Create run directory and run.json")
    c1.add_argument("--project", required=True)
    c1.add_argument("--topic", required=True)
    c1.set_defaults(func=cmd_create_run)

    c2 = sub.add_parser("get-run", help="Print run.json as JSON")
    c2.add_argument("--run-id", required=True)
    c2.set_defaults(func=cmd_get_run)

    c3 = sub.add_parser("write-artifact", help="Write stdin to artifact file")
    c3.add_argument("--run-id", required=True)
    c3.add_argument(
        "--artifact",
        required=True,
        choices=sorted(ARTIFACT_MAP.keys()),
    )
    c3.set_defaults(func=cmd_write_artifact)

    c4 = sub.add_parser("update-status", help="Update status and append audit line")
    c4.add_argument("--run-id", required=True)
    c4.add_argument("--status", required=True)
    c4.add_argument("--actor", required=True)
    c4.add_argument("--note", default="", help="Audit note")
    c4.set_defaults(func=cmd_update_status)

    c5 = sub.add_parser("validate-run", help="Minimal consistency checks")
    c5.add_argument("--run-id", required=True)
    c5.set_defaults(func=cmd_validate_run)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
