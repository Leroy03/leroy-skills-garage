from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVFLOW = ROOT / "scripts" / "devflow.py"


def run_devflow(*args: str, project_root: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DEVFLOW), *args, "--project-root", str(project_root)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


class WorkflowCapabilityCliTests(unittest.TestCase):
    def test_bundled_workflows_validate(self) -> None:
        result = run_devflow("validate-workflow", "--all")
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["status"], "passed")
        self.assertEqual(payload["summary"]["workflow_count"], 4)

    def test_doctor_selects_available_providers(self) -> None:
        result = run_devflow("doctor-capabilities", "--strict")
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["unresolved_count"], 0)
        selected = {item["capability"]: item["selected_provider"] for item in payload["capabilities"]}
        self.assertIn(selected["repository_search"], {"codegraph-cli", "ripgrep"})
        self.assertEqual(selected["devflow_governance"], "project-devflow")

    def test_resolve_capability_returns_first_available_provider(self) -> None:
        result = run_devflow("resolve-capability", "--name", "repository_search")
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "available")
        self.assertIn(payload["selected_provider"], {"codegraph-cli", "ripgrep"})

    def test_invalid_workflow_fails_with_actionable_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "workflows").mkdir()
            (project / "capabilities").mkdir()
            (project / "workflows" / "broken.yaml").write_text(
                json.dumps({"name": "broken", "version": 1}), encoding="utf-8"
            )
            (project / "capabilities" / "providers.yaml").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "capabilities": {
                            "example": {
                                "providers": [{"name": "built-in", "probe": "always"}]
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            result = run_devflow("validate-workflow", "--all", project_root=project)
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["summary"]["status"], "failed")
            self.assertTrue(
                any("missing required field" in error for error in payload["workflows"][0]["errors"])
            )

    def test_strict_doctor_fails_for_unresolved_provider(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "capabilities").mkdir()
            (project / "capabilities" / "providers.yaml").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "capabilities": {
                            "missing": {
                                "providers": [
                                    {
                                        "name": "missing-command",
                                        "probe": "command",
                                        "command": "definitely-not-a-real-command-leroy",
                                    }
                                ]
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            result = run_devflow("doctor-capabilities", "--strict", project_root=project)
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["summary"]["unresolved_count"], 1)

    def test_command_provider_can_require_project_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "capabilities").mkdir()
            (project / "capabilities" / "providers.yaml").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "capabilities": {
                            "indexed_search": {
                                "providers": [
                                    {
                                        "name": "runtime-with-index",
                                        "probe": "command",
                                        "command": Path(sys.executable).name,
                                        "path": ".required-index",
                                    }
                                ]
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            result = run_devflow("doctor-capabilities", "--strict", project_root=project)
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            reason = payload["capabilities"][0]["providers"][0]["reason"]
            self.assertIn("required path not found", reason)


if __name__ == "__main__":
    unittest.main()
