#!/usr/bin/env python3
"""Record the M1 contract suite and two source-bounded CLI examples.

Run from any directory: python /path/to/docs/h3skill/tests/run_tests.py
Only this tests directory receives reports; skill inputs remain unchanged.
"""

import copy
import hashlib
import io
import json
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent / "h3-work-intent"
SCRIPT = SKILL / "scripts" / "m1_contract.py"


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"test": test.id(), "status": "pass"})

    def addFailure(self, test, error):
        super().addFailure(test, error)
        self.records.append({"test": test.id(), "status": "fail", "details": self._exc_info_to_string(error, test)})

    def addError(self, test, error):
        super().addError(test, error)
        self.records.append({"test": test.id(), "status": "error", "details": self._exc_info_to_string(error, test)})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.records.append({"test": test.id(), "status": "skip", "reason": reason})


def main():
    started = datetime.now(timezone.utc).isoformat()
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_m1_contract.py")
    result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=RecordedResult).run(suite)
    (HERE / "unittest-output.txt").write_text(stream.getvalue(), encoding="utf-8")
    outputs = HERE / "results"
    outputs.mkdir(exist_ok=True)
    executions = []

    def execute(command, *paths):
        argv = [sys.executable, str(SCRIPT), command, *(str(p) for p in paths)]
        process = subprocess.run(argv, text=True, capture_output=True, check=False)
        payload = json.loads(process.stdout) if process.stdout.strip() else None
        executions.append({
            "command": command, "inputs": [str(p.relative_to(HERE.parent)) for p in paths],
            "exit_code": process.returncode, "stderr": process.stderr,
            "outcome": payload.get("outcome") if isinstance(payload, dict) else None,
            "audit": payload.get("audit") if isinstance(payload, dict) else None,
            "execution": payload.get("execution") if isinstance(payload, dict) else None,
        })
        if process.returncode != 0:
            raise RuntimeError("CLI example failed: " + command + "\n" + process.stdout + process.stderr)
        return payload

    example_failure = None
    try:
        for suffix in ("m1", "m1-1", "m1-2", "m1-3"):
            execute("route", SKILL / "assets" / ("request-" + suffix + ".json"))
        for label, empty, batch in (
            ("water", SKILL / "assets" / "workbrief-empty.json", HERE / "fixtures" / "water-batch.json"),
            ("mv", HERE / "fixtures" / "mv-empty.json", HERE / "fixtures" / "mv-batch.json"),
        ):
            accepted = execute("accept", empty, batch)
            write_json(outputs / (label + "-acceptance.json"), accepted)
            work_path = outputs / (label + "-workbrief.json")
            write_json(work_path, accepted["work_brief"])
            checked = execute("check", work_path)
            write_json(outputs / (label + "-check.json"), checked)
            if label == "water":
                previous = copy.deepcopy(accepted["work_brief"])
                previous["consumers"] = [
                    {"consumer_id": "M1-PARAGRAPHS", "module_id": "M1.2", "version": 1,
                     "source_work_version": previous["version"], "read_paths": ["/content/intent"]},
                    {"consumer_id": "M4-P01", "module_id": "M4", "version": 1,
                     "source_work_version": previous["version"], "read_paths": ["/content/paragraphs/P01"]},
                ]
                current = copy.deepcopy(previous)
                current["version"] += 1
                current["display"]["title"] += "（仅展示名称变更）"
                previous_path = outputs / "water-impact-before.json"
                current_path = outputs / "water-impact-after.json"
                write_json(previous_path, previous)
                write_json(current_path, current)
                impact = execute("impact", previous_path, current_path)
                write_json(outputs / "water-impact-display-only.json", impact)
                if impact["stale_consumers"]:
                    raise RuntimeError("Display-only example unexpectedly invalidated semantic consumers.")
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        example_failure = str(error)

    source_paths = [SCRIPT, SKILL / "references" / "contracts.json", SKILL / "references" / "module-registry.json",
                    HERE / "test_m1_contract.py", HERE / "run_tests.py"]
    source_paths.extend(sorted((SKILL / "assets").glob("*.json")))
    source_paths.extend(sorted((HERE / "fixtures").glob("*.json")))
    report = {
        "kind": "M1DevelopmentTestRecord", "contract_version": "1.0.0", "package_version": "0.1.0",
        "scope": "Structure, deterministic invariants, routing, versioned acceptance and explicit dependency impact only.",
        "semantic_assessment": "not_executed_by_these_programs", "h3_generation": "not_executed",
        "media_quality": "unverified", "source_corpus_commit": "0ce8b7b1890052bf1d4dd233ef20e68817b38f28",
        "command": "python docs/h3skill/tests/run_tests.py", "python": sys.version.split()[0],
        "started_at_utc": started, "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "skipped": len(result.skipped), "unit_tests_successful": result.wasSuccessful(),
        "cli_examples_successful": example_failure is None, "cli_example_failure": example_failure,
        "case_examples": [
            {"case": "2026-08-water-obstacle-variety-show", "scope": "Seven source anchors, regrouped into three semantic paragraphs for this example."},
            {"case": "2026-10-classical-wuxia-dance-13-segment", "scope": "First two source segments only; actual audio energy remains explicitly unknown."},
        ],
        "tests": result.records, "cli_executions": executions,
        "tested_file_sha256": {str(p.relative_to(HERE.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
    }
    write_json(HERE / "test-results.json", report)
    sys.stdout.write(stream.getvalue())
    print(json.dumps({"tests_run": result.testsRun, "unit_success": result.wasSuccessful(),
                      "cli_success": example_failure is None, "report": str(HERE / "test-results.json")}, ensure_ascii=False))
    return 0 if result.wasSuccessful() and example_failure is None else 1


if __name__ == "__main__":
    sys.exit(main())
