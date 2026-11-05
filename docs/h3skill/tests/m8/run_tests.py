#!/usr/bin/env python3
"""Run the M8 regression suite; reports stay outside the installed skill."""
import io
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
stream = io.StringIO()
suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_m8_contract.py")
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
report = {"suite": "m8-contract", "timestamp_utc": datetime.now(timezone.utc).isoformat(), "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped), "successful": result.wasSuccessful(), "media_execution": "none; M12 records in tests are synthetic contract test doubles"}
(HERE / "unittest-output.txt").write_text(stream.getvalue(), encoding="utf-8")
(HERE / "test-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(stream.getvalue(), end="")
print(json.dumps(report, ensure_ascii=False))
sys.exit(0 if result.wasSuccessful() else 1)
