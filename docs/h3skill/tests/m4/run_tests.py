#!/usr/bin/env python3
"""Run real M4 tests and write the report outside the installable skill."""
import hashlib
import io
import json
from pathlib import Path
import sys
import time
import unittest
from datetime import datetime, timezone

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1] / "h3-action-performance"
start = datetime.now(timezone.utc).isoformat()
tick = time.monotonic()
stream = io.StringIO()
suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_*.py")
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
elapsed = time.monotonic() - tick
(HERE / "unittest-output.txt").write_text(stream.getvalue(), encoding="utf-8")
paths = [PACKAGE / "scripts/m4_contract.py", PACKAGE / "references/contracts.json",
         PACKAGE / "references/module-registry.json", PACKAGE / "references/contract-guide.md",
         HERE / "test_contract.py", HERE / "run_tests.py", *sorted((PACKAGE / "assets").glob("*.json"))]
report = {
    "classification": "D design fixtures; local deterministic implementation tests",
    "started_at": start, "finished_at": datetime.now(timezone.utc).isoformat(),
    "duration_seconds": round(elapsed, 4), "python": sys.version,
    "command": "python docs/h3skill/tests/m4/run_tests.py",
    "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
    "skips": [{"test": str(test), "reason": reason} for test, reason in result.skipped],
    "status": "pass" if result.wasSuccessful() else "fail",
    "scope": ["standalone children", "atomic composition", "actual-request fidelity", "ownership",
              "unknown/not_applicable", "event DAG", "contact IDs", "state-token inheritance",
              "idempotency", "nondeletion", "impact", "portable copy", "strict JSON"],
    "not_verified": ["natural-language intent", "physical feasibility", "media observations", "H3 execution", "G0-G4"],
    "file_sha256": {str(path.relative_to(HERE.parents[1])): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
}
(HERE / "test-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: report[key] for key in ("tests_run", "failures", "errors", "skips", "status", "duration_seconds")}, ensure_ascii=False))
if not result.wasSuccessful():
    print(stream.getvalue())
raise SystemExit(0 if result.wasSuccessful() else 1)
