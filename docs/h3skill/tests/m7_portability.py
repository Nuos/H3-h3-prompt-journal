#!/usr/bin/env python3
"""Exercise the distributed M7 folder without sibling skills or site packages."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "docs/h3skill/h3-time-synchronization"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    symlinks = [p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob("*") if p.is_symlink()]
    if symlinks:
        print(json.dumps({"status":"fail", "failures":["package contains symlinks"],
                          "symlinks":symlinks}, ensure_ascii=False))
        return 1
    runs = []
    started = datetime.now(timezone.utc).isoformat()
    fingerprint = {
        path.relative_to(SOURCE).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in SOURCE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    with tempfile.TemporaryDirectory(prefix="m7-portable-") as temp:
        package = Path(temp) / SOURCE.name
        shutil.copytree(SOURCE, package, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

        def run(name, arguments):
            command = [sys.executable, "-I", "-S", "scripts/m7_contract.py", *arguments]
            completed = subprocess.run(command, cwd=package, capture_output=True, text=True,
                                       timeout=30, check=False)
            try:
                payload = json.loads(completed.stdout)
            except ValueError:
                payload = None
            item = {"name": name, "command": ["python", *command[1:]],
                    "exit_code": completed.returncode,
                    "stdout": payload if payload is not None else completed.stdout,
                    "stderr": completed.stderr}
            if not isinstance(payload, dict):
                item["semantic_failure"] = "CLI did not return the expected JSON object"
            runs.append(item)
            return payload if completed.returncode == 0 and not item.get("semantic_failure") else None

        for index in range(1, 4):
            req = f"assets/request-standalone-m7-{index}.json"
            prop = f"assets/proposal-standalone-m7-{index}.json"
            run(f"standalone_route_M7.{index}", ["route", req])
            run(f"standalone_check_M7.{index}", ["check", prop, "--request", req])
        run("parent_route", ["route", "assets/request-m7.json"])
        run("combined_proposals", ["check", "assets/proposal-batch.json", "--requests", "assets/requests.json"])
        accepted = run("atomic_accept", ["accept", "assets/state-empty.json", "assets/proposal-batch.json",
                                          "--requests", "assets/requests.json"])
        if isinstance(accepted, dict) and isinstance(accepted.get("state"), dict):
            (package / "accepted-state.json").write_text(json.dumps(accepted["state"], ensure_ascii=False), encoding="utf-8")
            run("accepted_state_contract", ["check", "accepted-state.json"])
            replay = run("exact_accept_replay", ["accept", "accepted-state.json", "assets/proposal-batch.json",
                                                 "--requests", "assets/requests.json"])
            if not isinstance(replay, dict) or replay.get("state") != accepted["state"]:
                runs[-1]["semantic_failure"] = "exact replay changed accepted state"
            run("registered_impact", ["impact", "assets/state-empty.json", "accepted-state.json"])
        else:
            runs.append({"name":"accepted_state_handoff", "exit_code":1,
                         "semantic_failure":"accept did not provide a usable .state"})
        after = {
            name: hashlib.sha256((package / name).read_bytes()).hexdigest()
            for name in fingerprint
        }
        unchanged = after == fingerprint
    failures = [item["name"] for item in runs if item["exit_code"] != 0 or item.get("semantic_failure")]
    if not unchanged:
        failures.append("runtime_modified_distributed_inputs")
    result = {"kind":"M7PortabilityRun", "started_at_utc":started,
              "finished_at_utc":datetime.now(timezone.utc).isoformat(),
              "environment":"Only a temporary copy of the skill directory; python -I -S disables site packages and ambient import paths.",
              "python":sys.version.split()[0], "status":"fail" if failures else "pass",
              "invocations":len(runs), "failures":failures, "inputs_unchanged":unchanged,
              "runtime_file_sha256":fingerprint, "runs":runs,
              "limits":["No H3 call, audio/video reading, synthesis, mixing, or media-quality claim.",
                        "Successful routing does not execute an Agent's professional timing-planning work."]}
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(serialized, encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "invocations", "failures", "inputs_unchanged")}, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
