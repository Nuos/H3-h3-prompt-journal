#!/usr/bin/env python3
"""Run and record the M3 delivery checks; do not edit prior-module reports."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIVERY = HERE.parents[1]
REPO = DELIVERY.parents[1]
SKILL = DELIVERY / "h3-scene-blocking"


def main():
    started = datetime.now(timezone.utc).isoformat()
    logdir = HERE / "logs"
    logdir.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    results = []

    def run(name, args, cwd=REPO, portable=False):
        result = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True)
        (logdir / (name + ".stdout.txt")).write_text(result.stdout)
        (logdir / (name + ".stderr.txt")).write_text(result.stderr)
        record = {"check": name, "argv": [str(a) for a in args],
                  "cwd": "isolated copied skill directory" if portable else str(cwd.relative_to(REPO) or "."),
                  "exit_code": result.returncode, "passed": result.returncode == 0,
                  "stdout": "logs/" + name + ".stdout.txt", "stderr": "logs/" + name + ".stderr.txt"}
        match = re.search(r"Ran (\d+) tests", result.stderr)
        if match:
            skipped = re.search(r"skipped=(\d+)", result.stderr)
            record.update(tests_run=int(match[1]), skipped=int(skipped[1]) if skipped else 0)
        results.append(record)
        return result

    run("anthropic-format", [sys.executable, "docs/h3skill/_standards/anthropics-quick-validate.py",
                             "docs/h3skill/h3-scene-blocking"])
    run("m3-unittest", [sys.executable, "-m", "unittest", "discover", "-s", "docs/h3skill/tests/m3", "-p", "test*.py", "-v"])
    run("m1-regression", [sys.executable, "-m", "unittest", "discover", "-s", "docs/h3skill/tests", "-p", "test_m1_contract.py"])
    run("m2-regression", [sys.executable, "-m", "unittest", "discover", "-s", "docs/h3skill/tests/m2", "-p", "test_m2_contract.py"])
    with tempfile.TemporaryDirectory(prefix="h3-m3-portability-") as temp:
        portable = Path(temp) / SKILL.name
        shutil.copytree(SKILL, portable, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        run("portable-help", [sys.executable, "scripts/m3_contract.py", "--help"], portable, True)
        for p in sorted((portable / "assets").glob("*.json")):
            data = json.loads(p.read_text())
            if not isinstance(data, dict) or not data.get("kind", "").startswith(("M3", "SpatialPlan")):
                continue
            run("portable-check-" + p.stem, [sys.executable, "scripts/m3_contract.py", "check", "assets/" + p.name], portable, True)
            if data["kind"] == "M3Request":
                run("portable-route-" + p.stem, [sys.executable, "scripts/m3_contract.py", "route", "assets/" + p.name], portable, True)
        run("portable-accept", [sys.executable, "scripts/m3_contract.py", "accept",
                               "assets/state-empty.json", "assets/proposal-batch.json",
                               "--requests", "assets/requests.json"], portable, True)
    files = sorted(p for p in SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    hashes = {p.relative_to(DELIVERY).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    tests = next((r for r in results if r["check"] == "m3-unittest"), {})
    nonempty = tests.get("tests_run", 0) > 0
    result = {"kind": "M3DeliveryValidation", "python": sys.version,
              "date": "2026-11-05", "timezone": "America/Los_Angeles",
              "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
              "executions": results,
              "m3_tests_nonempty": nonempty,
              "ok": all(r["passed"] for r in results) and nonempty,
              "file_sha256": hashes,
              "limits": ["No H3 inference or media inspection", "No host automatic-trigger benchmark",
                         "CLI results cover only implemented structural and deterministic relations",
                         "Optional dependency skips are recorded by the underlying suites"]}
    (HERE / "delivery-checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"ok": result["ok"], "executions": len(results),
                      "failed": [r["check"] for r in results if not r["passed"]],
                      "test_suites": [{k: v for k, v in r.items() if k in ("check", "tests_run", "skipped", "passed")} for r in results if "tests_run" in r]}, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
