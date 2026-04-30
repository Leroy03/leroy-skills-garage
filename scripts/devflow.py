#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal DevFlow run helper aligned with inject/devflow-marshal-context.md section 9."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
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

DEFAULT_PROJECT_CONFIG: dict[str, Any] = {
    "version": 1,
    "collaboration_profile": "global-default",
    "testing": {
        "required_for_levels": ["L2", "L3"],
        "venv": {"enabled": True, "path": ".venv"},
        "commands": ["python -m pytest -q"],
        "coverage": {"enabled": False, "min_percent": 0},
        "extra_evidence": [],
    },
    "gates": {
        "reviewed_requires": ["01_plan.md", "02_review.md", "test_result.json"],
        "delivered_requires": ["03_dispatch.md", "04_delivery.md", "regression_scope.md"],
        "archived_requires": ["05_postmortem.md"],
    },
    "skill_contract": {
        "enabled": True,
        "require_fields": ["inputs_required", "outputs_required", "evidence_files"],
    },
}

PROJECT_TEMPLATE_FILES: dict[str, str] = {
    "devflow.templates/01_plan.md": "# 01 Plan\n\n- Objective:\n- Scope:\n- Risks:\n- Rollback:\n- Acceptance:\n",
    "devflow.templates/02_review.md": "# 02 Review\n\n- Verdict: PASS | FAIL\n- Findings:\n- Required fixes:\n",
    "devflow.templates/03_dispatch.md": "# 03 Dispatch\n\n- Owner:\n- Milestones:\n- Execution notes:\n",
    "devflow.templates/04_delivery.md": "# 04 Delivery\n\n- Changed files:\n- Verification evidence:\n- Residual risks:\n",
    "devflow.templates/05_postmortem.md": "# 05 Postmortem\n\n- What happened:\n- Root cause:\n- Follow-ups:\n",
    "devflow.templates/regression_scope.md": "# Regression Scope\n\n- P0:\n- P1:\n- P2:\n",
}


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


def _project_config_path(project_root: Path) -> Path:
    return project_root / "devflow.project.yaml"


def _adhoc_dir(project_root: Path) -> Path:
    base = devflow_root() / "quick" / _slug(project_root.name, 32)
    base.mkdir(parents=True, exist_ok=True)
    return base


def _load_project_config(project_root: Path) -> dict[str, Any]:
    path = _project_config_path(project_root)
    if not path.is_file():
        return json.loads(json.dumps(DEFAULT_PROJECT_CONFIG))
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if stripped.startswith("{"):
        data = json.loads(text)
    else:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise SystemExit(
                f"{path} uses YAML syntax; install PyYAML or switch to JSON-compatible YAML content"
            ) from exc
        loaded = yaml.safe_load(text)
        data = loaded if isinstance(loaded, dict) else {}
    merged = json.loads(json.dumps(DEFAULT_PROJECT_CONFIG))
    _merge_missing(merged, data)
    return merged


def _merge_missing(base: dict[str, Any], incoming: dict[str, Any]) -> None:
    for key, value in incoming.items():
        if key not in base:
            base[key] = value
            continue
        if isinstance(base[key], dict) and isinstance(value, dict):
            _merge_missing(base[key], value)
        else:
            base[key] = value


def _ensure_venv(project_root: Path, cfg: dict[str, Any]) -> str:
    testing = cfg.get("testing", {})
    venv_cfg = testing.get("venv", {})
    enabled = bool(venv_cfg.get("enabled", False))
    if not enabled:
        return sys.executable
    venv_path = project_root / str(venv_cfg.get("path", ".venv"))
    if os.name == "nt":
        venv_python = venv_path / "Scripts" / "python.exe"
    else:
        venv_python = venv_path / "bin" / "python"
    if not venv_python.is_file():
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True, cwd=str(project_root))
    return str(venv_python)


def _replace_python(cmd: str, python_exec: str) -> str:
    tokens = shlex.split(cmd, posix=False)
    if not tokens:
        return cmd
    if tokens[0].lower() == "python":
        tokens[0] = python_exec
        return subprocess.list2cmdline(tokens)
    return cmd


def _extract_missing_module(stderr_text: str) -> str | None:
    m = re.search(r"No module named ['\"]?([a-zA-Z0-9_\.]+)['\"]?", stderr_text)
    if not m:
        return None
    return m.group(1)


def _auto_install_package(python_exec: str, project_root: Path, package_name: str) -> None:
    subprocess.run(
        [python_exec, "-m", "pip", "install", package_name],
        check=True,
        cwd=str(project_root),
    )


def _parse_auto_install_whitelist(raw: str) -> set[str]:
    items = [x.strip().lower() for x in raw.split(",")]
    return {x for x in items if x}


def _install_package_with_result(python_exec: str, project_root: Path, package_name: str) -> tuple[bool, str]:
    proc = subprocess.run(
        [python_exec, "-m", "pip", "install", package_name],
        check=False,
        cwd=str(project_root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    snippet = (proc.stdout + "\n" + proc.stderr).strip()[-2000:]
    return proc.returncode == 0, snippet


def _append_event(run_dir: Path, event: dict[str, Any]) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    payload = {"ts": _utc_now_iso(), **event}
    with (run_dir / "event.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _write_gate_report(run_dir: Path, gate_name: str, status: str, reasons: list[str], details: dict[str, Any]) -> Path:
    payload = {
        "ts": _utc_now_iso(),
        "gate_name": gate_name,
        "status": status,
        "reasons": reasons,
        "details": details,
    }
    reports_dir = run_dir / "gate_reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{gate_name}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Keep a compatibility pointer for legacy readers.
    (run_dir / "gate_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


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
    _append_event(
        run_dir,
        {
            "command": "create-run",
            "status": "success",
            "run_id": run_id,
        },
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
    _append_event(
        run_dir,
        {
            "command": "update-status",
            "status": "success",
            "run_id": args.run_id,
            "from_status": old,
            "to_status": args.status,
        },
    )
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
    review_or_later = {"Reviewed", "Dispatched", "Running", "Delivered", "Archived"}
    if args.strict_level == "standard" and status in review_or_later:
        test_result = _load_json_if_exists(run_dir / "test_result.json")
        if not test_result:
            errors.append("review+ gate requires test_result.json")
        else:
            overall = test_result.get("summary", {}).get("overall_status")
            if overall != "passed":
                errors.append(f"review+ gate requires tests passed, got: {overall!r}")

        contract = _load_json_if_exists(run_dir / "contract_report.json")
        if not contract:
            errors.append("review+ gate requires contract_report.json")
        else:
            contract_status = contract.get("summary", {}).get("status")
            if contract_status != "passed":
                errors.append(f"review+ gate requires contract passed, got: {contract_status!r}")
    gate_status = "passed" if not errors else "failed"
    gate_path = _write_gate_report(
        run_dir,
        "validate-run",
        gate_status,
        errors,
        {"run_id": args.run_id, "status": status},
    )
    _append_event(
        run_dir,
        {
            "command": "validate-run",
            "status": gate_status,
            "run_id": args.run_id,
            "artifact": str(gate_path),
            "error_count": len(errors),
        },
    )
    if errors:
        raise SystemExit("validate failed:\n- " + "\n- ".join(errors))
    print("validate ok")


def cmd_init_project(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    project_root.mkdir(parents=True, exist_ok=True)
    created = 0
    skipped = 0
    cfg_path = _project_config_path(project_root)
    if cfg_path.exists() and not args.force:
        skipped += 1
    else:
        # Write JSON text to .yaml path so parsing works without PyYAML dependency.
        cfg_text = json.dumps(DEFAULT_PROJECT_CONFIG, ensure_ascii=False, indent=2) + "\n"
        cfg_path.write_text(cfg_text, encoding="utf-8")
        created += 1
    for rel, content in PROJECT_TEMPLATE_FILES.items():
        path = project_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not args.force:
            skipped += 1
            continue
        path.write_text(content, encoding="utf-8")
        created += 1
    print(json.dumps({"project_root": str(project_root), "created_count": created, "skipped_count": skipped}, ensure_ascii=False))


def cmd_sync_project(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    cfg_path = _project_config_path(project_root)
    if not cfg_path.is_file():
        raise SystemExit(f"config not found: {cfg_path}")
    text = cfg_path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if stripped.startswith("{"):
        current = json.loads(text)
        is_json = True
    else:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise SystemExit("sync-project for YAML requires PyYAML") from exc
        loaded = yaml.safe_load(text)
        current = loaded if isinstance(loaded, dict) else {}
        is_json = False
    before_version = current.get("version")
    merged = json.loads(json.dumps(DEFAULT_PROJECT_CONFIG))
    added_fields: list[str] = []
    _merge_and_track(merged, current, "", added_fields)
    merged["version"] = args.target_version if args.target_version is not None else merged.get("version", 1)
    after_version = merged.get("version")
    if not args.dry_run:
        if is_json:
            cfg_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            import yaml  # type: ignore

            cfg_path.write_text(yaml.safe_dump(merged, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "project_root": str(project_root),
                "before_version": before_version,
                "after_version": after_version,
                "added_fields": sorted(set(added_fields)),
                "dry_run": args.dry_run,
            },
            ensure_ascii=False,
        )
    )


def _merge_and_track(base: dict[str, Any], current: dict[str, Any], prefix: str, added_fields: list[str]) -> None:
    for key, value in current.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if key not in base:
            base[key] = value
            continue
        if isinstance(base[key], dict) and isinstance(value, dict):
            _merge_and_track(base[key], value, full_key, added_fields)
        else:
            base[key] = value
    for key in base.keys():
        if key not in current:
            full_key = f"{prefix}.{key}" if prefix else key
            added_fields.append(full_key)


def cmd_collect_evidence(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    cfg = _load_project_config(project_root)
    python_exec = _ensure_venv(project_root, cfg)
    commands = cfg.get("testing", {}).get("commands", [])
    if not isinstance(commands, list) or not commands:
        raise SystemExit("testing.commands is empty in devflow.project.yaml")
    run_dir = find_run_dir(args.run_id) if args.run_id else None
    module_to_package = {
        "pytest": "pytest",
        "pytest_cov": "pytest-cov",
        "coverage": "coverage",
    }
    auto_whitelist = _parse_auto_install_whitelist(args.auto_install_whitelist)
    dependency_actions: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    total_start = datetime.now(timezone.utc)
    for idx, cmd in enumerate(commands, start=1):
        if not isinstance(cmd, str):
            continue
        cmd_run = _replace_python(cmd, python_exec)
        started = datetime.now(timezone.utc)
        proc = subprocess.run(
            cmd_run,
            shell=True,
            cwd=str(project_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if (
            args.auto_install_missing
            and proc.returncode != 0
            and " -m " in cmd_run
        ):
            missing_module = _extract_missing_module(proc.stderr)
            if missing_module:
                package_name = module_to_package.get(missing_module, missing_module)
                if package_name.lower() in auto_whitelist:
                    installed, install_output = _install_package_with_result(python_exec, project_root, package_name)
                    dependency_actions.append(
                        {
                            "action": "auto_install",
                            "module": missing_module,
                            "package": package_name,
                            "status": "success" if installed else "failed",
                            "output_snippet": install_output,
                        }
                    )
                    if installed:
                        proc = subprocess.run(
                            cmd_run,
                            shell=True,
                            cwd=str(project_root),
                            capture_output=True,
                            text=True,
                            encoding="utf-8",
                            errors="replace",
                        )
                else:
                    dependency_actions.append(
                        {
                            "action": "auto_install_skipped",
                            "module": missing_module,
                            "package": package_name,
                            "status": "skipped_not_in_whitelist",
                            "output_snippet": "",
                        }
                    )
        ended = datetime.now(timezone.utc)
        duration_ms = int((ended - started).total_seconds() * 1000)
        item = {
            "id": f"cmd-{idx}",
            "command": cmd_run,
            "start_at": started.replace(microsecond=0).isoformat(),
            "end_at": ended.replace(microsecond=0).isoformat(),
            "duration_ms": duration_ms,
            "exit_code": proc.returncode,
            "status": "passed" if proc.returncode == 0 else "failed",
            "stdout_snippet": proc.stdout[-4000:],
            "stderr_snippet": proc.stderr[-4000:],
            "artifacts": [],
        }
        results.append(item)
        if args.stop_on_fail and proc.returncode != 0:
            break
    passed = sum(1 for x in results if x["status"] == "passed")
    failed = sum(1 for x in results if x["status"] == "failed")
    total_end = datetime.now(timezone.utc)
    payload = {
        "schema_version": "1.0",
        "project": project_root.name,
        "run_id": args.run_id,
        "level": args.level,
        "generated_at": total_end.replace(microsecond=0).isoformat(),
        "environment": {
            "os": os.name,
            "python": python_exec,
            "venv_path": cfg.get("testing", {}).get("venv", {}).get("path", ".venv"),
            "cwd": str(project_root),
        },
        "summary": {
            "total_commands": len(results),
            "passed": passed,
            "failed": failed,
            "duration_ms": int((total_end - total_start).total_seconds() * 1000),
            "overall_status": "passed" if failed == 0 else "failed",
        },
        "commands": results,
        "dependency_actions": dependency_actions,
        "coverage": {
            "enabled": bool(cfg.get("testing", {}).get("coverage", {}).get("enabled", False)),
            "overall_percent": None,
            "threshold_percent": cfg.get("testing", {}).get("coverage", {}).get("min_percent", 0),
            "status": "skipped",
        },
        "quality_gates": {"review_gate": "skipped", "delivery_gate": "skipped", "reasons": []},
    }
    output_path = Path(args.output).resolve() if args.output else (
        (run_dir / "test_result.json") if run_dir else (_adhoc_dir(project_root) / "test_result.json")
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    event_dir = run_dir if run_dir else _adhoc_dir(project_root)
    _append_event(
        event_dir,
        {
            "command": "collect-evidence",
            "status": payload["summary"]["overall_status"],
            "run_id": args.run_id,
            "level": args.level,
            "output": str(output_path),
            "total_commands": len(results),
            "failed": failed,
            "dependency_actions": len(dependency_actions),
        },
    )
    print(
        json.dumps(
            {"output": str(output_path), "total_commands": len(results), "passed": passed, "failed": failed},
            ensure_ascii=False,
        )
    )


def cmd_validate_skill_contract(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    cfg = _load_project_config(project_root)
    contract_cfg = cfg.get("skill_contract", {})
    if not contract_cfg.get("enabled", True):
        print(json.dumps({"enabled": False, "status": "skipped"}, ensure_ascii=False))
        return
    required_fields = contract_cfg.get("require_fields", [])
    run_dir = find_run_dir(args.run_id) if args.run_id else _adhoc_dir(project_root)
    run_dir.mkdir(parents=True, exist_ok=True)
    report_items = []
    missing_total: list[str] = []
    for skill in args.skill:
        record_path = run_dir / "skill_contract" / f"{skill}.json"
        record_path.parent.mkdir(parents=True, exist_ok=True)
        item_missing: list[str] = []
        evidence_missing: list[str] = []
        data: dict[str, Any] = {}
        if record_path.is_file():
            try:
                data = json.loads(record_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                item_missing.append("invalid_json")
        else:
            if args.init_missing:
                data = {
                    "inputs_required": [],
                    "outputs_required": [],
                    "evidence_files": [],
                }
                record_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            else:
                item_missing.append("contract_file_missing")
        for field in required_fields:
            if field not in data:
                item_missing.append(field)
        for evidence in data.get("evidence_files", []):
            p = Path(evidence)
            if not p.is_absolute():
                p = run_dir / evidence
            if not p.exists():
                evidence_missing.append(str(evidence))
        report_items.append(
            {
                "skill": skill,
                "contract_file": str(record_path),
                "missing_fields": sorted(set(item_missing)),
                "missing_evidence": sorted(set(evidence_missing)),
                "status": "passed" if not item_missing and not evidence_missing else "failed",
            }
        )
        if item_missing or evidence_missing:
            missing_total.append(skill)
    report = {
        "generated_at": _utc_now_iso(),
        "required_fields": required_fields,
        "skills": report_items,
        "summary": {
            "total": len(report_items),
            "failed": len(missing_total),
            "passed": len(report_items) - len(missing_total),
            "status": "passed" if not missing_total else "failed",
        },
    }
    report_path = run_dir / "contract_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    missing_reasons = [f"skill contract failed: {x}" for x in missing_total]
    gate_path = _write_gate_report(
        run_dir,
        "validate-skill-contract",
        report["summary"]["status"],
        missing_reasons,
        {"run_id": args.run_id, "skills": args.skill, "report": str(report_path)},
    )
    _append_event(
        run_dir,
        {
            "command": "validate-skill-contract",
            "status": report["summary"]["status"],
            "run_id": args.run_id,
            "artifact": str(report_path),
            "gate_report": str(gate_path),
            "failed": report["summary"]["failed"],
        },
    )
    print(json.dumps({"output": str(report_path), "status": report["summary"]["status"]}, ensure_ascii=False))
    if args.strict and missing_total:
        raise SystemExit("validate-skill-contract failed in strict mode")


def cmd_df_init(args: argparse.Namespace) -> None:
    init_args = argparse.Namespace(project_root=args.project_root, force=args.force)
    cmd_init_project(init_args)


def cmd_df_quick(args: argparse.Namespace) -> None:
    collect_args = argparse.Namespace(
        project_root=args.project_root,
        run_id=args.run_id,
        level=args.level,
        stop_on_fail=True,
        auto_install_missing=args.auto_install_missing,
        auto_install_whitelist=args.auto_install_whitelist,
        output=args.output,
    )
    cmd_collect_evidence(collect_args)
    if args.run_id:
        validate_args = argparse.Namespace(run_id=args.run_id, strict_level="minimal")
        cmd_validate_run(validate_args)


def cmd_df_gate(args: argparse.Namespace) -> None:
    if args.skill:
        contract_args = argparse.Namespace(
            project_root=args.project_root,
            run_id=args.run_id,
            skill=args.skill,
            strict=True,
            init_missing=args.init_missing,
        )
        cmd_validate_skill_contract(contract_args)
    validate_args = argparse.Namespace(run_id=args.run_id, strict_level="standard")
    cmd_validate_run(validate_args)


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
    c5.add_argument(
        "--strict-level",
        choices=("minimal", "standard"),
        default="standard",
        help="Validation strictness: minimal checks artifact presence only; standard also checks test/contract gates",
    )
    c5.set_defaults(func=cmd_validate_run)

    c6 = sub.add_parser("init-project", help="Initialize devflow.project.yaml and template docs")
    c6.add_argument("--project-root", default=".")
    c6.add_argument("--force", action="store_true")
    c6.set_defaults(func=cmd_init_project)

    c7 = sub.add_parser("sync-project", help="Sync config schema and fill missing fields")
    c7.add_argument("--project-root", default=".")
    c7.add_argument("--target-version", type=int)
    c7.add_argument("--dry-run", action="store_true")
    c7.set_defaults(func=cmd_sync_project)

    c8 = sub.add_parser("collect-evidence", help="Run test commands and write test_result.json")
    c8.add_argument("--project-root", default=".")
    c8.add_argument("--run-id")
    c8.add_argument("--level", default="L2")
    c8.add_argument("--stop-on-fail", action="store_true")
    c8.add_argument("--auto-install-missing", action="store_true")
    c8.add_argument(
        "--auto-install-whitelist",
        default="pytest,pytest-cov,coverage",
        help="Comma-separated pip package whitelist for auto install",
    )
    c8.add_argument("--output")
    c8.set_defaults(func=cmd_collect_evidence)

    c9 = sub.add_parser("validate-skill-contract", help="Validate skill contract outputs and evidence")
    c9.add_argument("--project-root", default=".")
    c9.add_argument("--run-id")
    c9.add_argument("--skill", action="append", required=True)
    c9.add_argument("--strict", action="store_true")
    c9.add_argument("--init-missing", action="store_true", help="Create missing skill contract files with empty template")
    c9.set_defaults(func=cmd_validate_skill_contract)

    c10 = sub.add_parser("df-init", help="Shortcut: initialize devflow project templates")
    c10.add_argument("--project-root", default=".")
    c10.add_argument("--force", action="store_true")
    c10.set_defaults(func=cmd_df_init)

    c11 = sub.add_parser("df-quick", help="Shortcut: collect evidence and optional minimal run validation")
    c11.add_argument("--project-root", default=".")
    c11.add_argument("--run-id")
    c11.add_argument("--level", default="L2")
    c11.add_argument("--auto-install-missing", action="store_true")
    c11.add_argument(
        "--auto-install-whitelist",
        default="pytest,pytest-cov,coverage",
        help="Comma-separated pip package whitelist for auto install",
    )
    c11.add_argument("--output")
    c11.set_defaults(func=cmd_df_quick)

    c12 = sub.add_parser("df-gate", help="Shortcut: strict contract check and standard run gate")
    c12.add_argument("--project-root", default=".")
    c12.add_argument("--run-id", required=True)
    c12.add_argument("--skill", action="append", help="Skill name to validate contract; can pass multiple")
    c12.add_argument("--init-missing", action="store_true", help="Create missing skill contract files before check")
    c12.set_defaults(func=cmd_df_gate)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
