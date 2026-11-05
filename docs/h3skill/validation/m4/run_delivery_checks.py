#!/usr/bin/env python3
"""Reproduce M4 packaging, official format and standalone CLI checks.

Only this module's validation/m4 outputs are written. Runtime tools are read-only.
These checks do not inspect media, solve physics, compile prompts or invoke H3.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIVERY = HERE.parents[1]
SKILL = DELIVERY / "h3-action-performance"
LOGS = HERE / "logs"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    started = datetime.now(timezone.utc).isoformat()
    LOGS.mkdir(parents=True, exist_ok=True)
    results = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

    def run(label, argv, cwd, json_report=False):
        proc = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=60)
        (LOGS / (label + ".stdout.txt")).write_text(proc.stdout, encoding="utf-8")
        (LOGS / (label + ".stderr.txt")).write_text(proc.stderr, encoding="utf-8")
        row = {"check": label, "argv": [str(x) for x in argv], "cwd": str(cwd),
               "exit_code": proc.returncode, "passed": proc.returncode == 0}
        report = None
        if json_report:
            try:
                report = json.loads(proc.stdout)
            except ValueError as exc:
                row.update(passed=False, report_error=str(exc))
        results.append(row)
        return report

    # The unmodified Anthropic validator is a development-only dependency.
    run("anthropic-format", [sys.executable, str(DELIVERY / "_standards/anthropics-quick-validate.py"), str(SKILL)], DELIVERY)
    imports = set()
    for path in (SKILL / "scripts").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                imports.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module.split(".")[0] if node.module else "<relative>")
    external = sorted(imports - sys.stdlib_module_names - {"__future__"})
    results.append({"check": "runtime_imports_are_standard_library", "passed": not external,
                    "imports": sorted(imports), "external_imports": external})

    # Copy only the installable directory: no parent docs, tests or sibling skills.
    with tempfile.TemporaryDirectory(prefix="m4-standalone-") as name:
        standalone = Path(name) / SKILL.name
        shutil.copytree(SKILL, standalone, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        script = standalone / "scripts/m4_contract.py"
        prefix = [sys.executable, str(script)]
        run("portable-help", prefix + ["--help"], standalone)
        for suffix in ("", "-1", "-2", "-3"):
            filename = "request-m4" + suffix + ".json"
            run("portable-route-" + filename[:-5], prefix + ["route", "assets/" + filename], standalone, True)
        for n in (1, 2, 3):
            run(f"portable-check-proposal-m4-{n}", prefix + ["check", f"assets/proposal-m4-{n}.json",
                "--request", f"assets/request-m4-{n}.json"], standalone, True)
        run("portable-check-batch", prefix + ["check", "assets/proposal-batch.json", "--requests", "assets/requests.json"], standalone, True)
        run("portable-check-empty-state", prefix + ["check", "assets/state-empty.json"], standalone, True)
        accepted = run("portable-accept", prefix + ["accept", "assets/state-empty.json", "assets/proposal-batch.json",
            "--requests", "assets/requests.json"], standalone, True)
        state = accepted.get("state") if isinstance(accepted, dict) else None
        results.append({"check": "accepted_output_is_separate_state", "passed": isinstance(state, dict) and state.get("kind") == "M4State"})
        if isinstance(state, dict):
            (standalone / "accepted-state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
            run("portable-check-accepted-state", prefix + ["check", "accepted-state.json"], standalone, True)
        validation = accepted.get("validation", {}) if isinstance(accepted, dict) else {}
        results.append({"check": "acceptance_does_not_claim_overall_semantic_or_media_pass",
                        "passed": validation.get("overall") == "unverified", "validation": validation})

    paths = sorted(p for p in SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    data = {"kind": "M4DeliveryChecks", "started_at": started,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "python": sys.version.split()[0], "checks": results,
            "passed": sum(r["passed"] for r in results), "total": len(results),
            "ok": all(r["passed"] for r in results),
            "file_sha256": {p.relative_to(DELIVERY).as_posix(): sha(p) for p in paths},
            "not_certified": ["natural-language quality", "source authenticity", "body dynamics", "physical contact",
                              "camera visibility", "actual timing", "H3 inference", "generated media", "complete G0-G4 gates"]}
    (HERE / "delivery-checks.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in data.items() if k not in ("file_sha256", "checks")}, ensure_ascii=False, indent=2))
    if not data["ok"]:
        print(json.dumps([r for r in results if not r["passed"]], ensure_ascii=False, indent=2))
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
