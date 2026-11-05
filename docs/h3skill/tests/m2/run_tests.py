#!/usr/bin/env python3
"""Run M2 behavioral tests and save honest local evidence outside the skill."""

import hashlib
import io
import json
import platform
import sys
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1] / "h3-asset-reference"


def main():
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_*.py")
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (HERE / "unittest-output.txt").write_text(stream.getvalue(), encoding="utf-8")
    files = [SKILL / "scripts/m2_contract.py", SKILL / "references/contracts.json",
             SKILL / "references/module-registry.json", SKILL / "references/contract-guide.md",
             *sorted((SKILL / "assets").glob("*.json")), HERE / "test_m2_contract.py", Path(__file__).resolve()]
    report = {
        "kind": "M2BehavioralTestRecord", "contract_version": "1.0.0",
        "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(time.monotonic() - clock, 6),
        "python": platform.python_version(),
        "command": "python docs/h3skill/tests/m2/run_tests.py",
        "tests_run": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
        "failures": len(result.failures), "errors": len(result.errors),
        "skipped": [{"test": str(test), "reason": reason} for test, reason in result.skipped],
        "status": "fail" if not result.wasSuccessful() else "pass_with_skip" if result.skipped else "pass",
        "scope": "Independent request routing, candidate/parent contracts, authority integrity, source/entity/channel references, permission scopes and decisions, malformed-input behavior, read-only operation, portability, declared-consumer invalidation.",
        "not_verified": ["Natural-language trigger recall", "Truth of supplied provenance and authority records", "Actual source media", "H3 inference or generated-video quality", "Downstream M3–M12 execution"],
        "file_sha256": {str(path.relative_to(HERE.parents[1])): hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
    }
    (HERE / "test-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("tests_run", "passed", "failures", "errors", "skipped", "status")}, ensure_ascii=False, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
