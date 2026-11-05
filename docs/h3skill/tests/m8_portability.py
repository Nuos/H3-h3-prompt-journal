#!/usr/bin/env python3
"""Run M8 as a detached skill with only its own files and Python stdlib."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent / "h3-state-continuity"


def tree_digest(root):
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(root.rglob("*")) if path.is_file()}


def main():
    checks = []
    with tempfile.TemporaryDirectory(prefix="m8-detached-") as tmp:
        outside = Path(tmp)
        package = outside / "installed" / PACKAGE.name
        shutil.copytree(PACKAGE, package, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
        cwd = outside / "unrelated-working-directory"
        cwd.mkdir()
        before = tree_digest(package)
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONHOME")}
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        script, assets = package / "scripts/m8_contract.py", package / "assets"

        def call(name, *args):
            proc = subprocess.run([sys.executable, "-B", str(script), *map(str, args)], cwd=cwd, env=env, capture_output=True, text=True)
            try:
                result = json.loads(proc.stdout)
            except ValueError:
                result = {"status": "invalid_json"}
            passed = proc.returncode == 0 and result.get("status") in ("passed", "passed_with_unverified")
            checks.append({"name": name, "passed": passed, "exit_code": proc.returncode, "status": result.get("status"), "diagnostics": result.get("diagnostics", []), "stderr": proc.stderr})
            return result

        for child in (1, 2, 3):
            request = assets / ("request-standalone-m8-" + str(child) + ".json")
            proposal = assets / ("proposal-standalone-m8-" + str(child) + ".json")
            call("standalone_route_m8_" + str(child), "route", request)
            call("standalone_check_m8_" + str(child), "check", proposal, "--request", request)
        accepted = call("atomic_parent_accept", "accept", assets / "state-empty.json", assets / "proposal-batch.json", "--requests", assets / "requests.json")
        if "state" in accepted:
            state_path = cwd / "accepted-state.json"
            state_path.write_text(json.dumps(accepted["state"], ensure_ascii=False), encoding="utf-8")
            call("accepted_state_check", "check", state_path)
            replay = call("idempotent_parent_replay", "accept", state_path, assets / "proposal-batch.json", "--requests", assets / "requests.json")
            checks.append({"name": "replay_preserves_state", "passed": replay.get("state") == accepted["state"] and replay.get("acceptance") == "idempotent_replay"})
            call("registered_consumer_impact", "impact", "--before", assets / "state-empty.json", "--after", state_path)
        else:
            checks.append({"name": "accepted_state_available", "passed": False})
        checks.append({"name": "installed_package_unchanged", "passed": before == tree_digest(package)})
        checks.append({"name": "repository_unavailable_in_detached_root", "passed": not (outside / ".git").exists() and not (outside / "docs/skillplan").exists() and not (outside / "case-studies").exists()})
        report = {"suite": "m8-portability", "timestamp_utc": datetime.now(timezone.utc).isoformat(), "status": "passed" if all(c["passed"] for c in checks) else "failed", "checks_run": len(checks), "checks": checks, "copied_files": len(before), "dependencies": "Python standard library; one copied skill; no upstream invocation", "media_verification": "not_performed"}
    target = HERE / "m8/portability-results.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
