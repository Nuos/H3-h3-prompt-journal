#!/usr/bin/env python3
"""Exercise all M12 public routes from an isolated package copy.

This is release verification, not a runtime dependency or media evaluation.
The supplied examples remain synthetic; the program writes only temporary data
and emits its reproducible checks and raw command outputs to stdout.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
PACKAGE = Path(__file__).resolve().parents[1] / "h3-audit-repair"


def snapshot(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def main():
    initial = snapshot(PACKAGE)
    commands, checks = [], []
    with tempfile.TemporaryDirectory(prefix="m12-isolation-") as temp:
        root = Path(temp)
        package, working = root / "h3-audit-repair", root / "unrelated-cwd"
        shutil.copytree(PACKAGE, package)
        working.mkdir()
        script = package / "scripts/m12_contract.py"

        def execute(args):
            argv = [sys.executable, "-I", "-B", str(script), *map(str, args)]
            proc = subprocess.run(argv, cwd=working, capture_output=True, text=True)
            normalized = [a.replace(str(root), "<isolated-root>") for a in argv]
            row = {"argv": normalized, "cwd": "<isolated-root>/unrelated-cwd",
                   "exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
            commands.append(row)
            if proc.returncode:
                raise RuntimeError("Isolated command failed: " + json.dumps(row, ensure_ascii=False))
            return json.loads(proc.stdout)

        requests, proposals = [], []
        for name in ("scope", "audit", "observation", "repair"):
            path = package / "assets" / (name + "-request.json")
            request = json.loads(path.read_text(encoding="utf-8"))
            routed = execute(["route", path])
            proposed = execute(["propose", path])
            proposal_path = working / (name + "-proposal.json")
            proposal_path.write_text(json.dumps(proposed, ensure_ascii=False), encoding="utf-8")
            verified = execute(["check", proposal_path, "--request", path])
            checks.append({"check": request["target"] + "_standalone_route_propose_check",
                           "status": "pass" if routed["status"] == "ready" and verified["status"] == "valid" else "fail"})
            requests.append(request)
            proposals.append(proposed)
        request_file, proposal_file = working / "requests.json", working / "proposals.json"
        request_file.write_text(json.dumps(requests, ensure_ascii=False), encoding="utf-8")
        proposal_file.write_text(json.dumps(proposals, ensure_ascii=False), encoding="utf-8")
        accepted = execute(["accept", proposal_file, "--requests", request_file,
                            "--state", package / "assets/empty-state.json"])
        state_path = working / "accepted-state.json"
        state_path.write_text(json.dumps(accepted["state"], ensure_ascii=False), encoding="utf-8")
        replay = execute(["accept", proposal_file, "--requests", request_file, "--state", state_path])
        checks.extend([
            {"check": "four_partition_atomic_accept", "status": "pass" if accepted["status"] == "accepted" and accepted["state"]["version"] == 1 and len(accepted["state"]["records"]) == 4 else "fail"},
            {"check": "idempotent_replay", "status": "pass" if replay["idempotent"] and replay["state"] == accepted["state"] else "fail"},
            {"check": "isolated_package_unmodified", "status": "pass" if snapshot(package) == initial else "fail"},
            {"check": "source_package_unmodified", "status": "pass" if snapshot(PACKAGE) == initial else "fail"},
        ])
    result = {"kind": "M12IsolationVerification", "status": "pass" if all(c["status"] == "pass" for c in checks) else "fail",
              "python": sys.version, "package_snapshot_sha256": initial,
              "checks": checks, "commands": commands, "command_count": len(commands),
              "isolation": "Complete package copy, unrelated cwd, Python -I -B; no repository imports.",
              "fixture_nature": "synthetic", "h3_inference": "not_run", "real_media_observation": "not_run"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
