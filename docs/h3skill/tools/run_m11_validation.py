#!/usr/bin/env python3
"""Run the bounded M11 gates, preserving commands, raw outputs and tested file hashes."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'docs/h3skill'
OUT = BASE / 'validation/m11'
PACKAGE = BASE / 'h3-model-protocol'


def stamp():
    return datetime.now(timezone.utc).isoformat()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    commands = [
        ('official_format', [sys.executable, 'docs/h3skill/_standards/anthropics-quick-validate.py',
                             'docs/h3skill/h3-model-protocol']),
        ('behavior', [sys.executable, '-m', 'unittest', 'discover', '-s', 'docs/h3skill/tests',
                      '-p', 'test_m11_contract.py', '-v']),
        ('portability', [sys.executable, 'docs/h3skill/tests/m11_portability.py']),
    ]
    package_hashes = [{'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                      for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.suffix != '.pyc']
    records = []
    for name, cmd in commands:
        started = stamp()
        start = time.monotonic()
        proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=180)
        stdout_path = OUT / (name + '.stdout.txt')
        stderr_path = OUT / (name + '.stderr.txt')
        stdout_path.write_text(proc.stdout)
        stderr_path.write_text(proc.stderr)
        record = {'check': name, 'status': 'pass' if proc.returncode == 0 else 'fail',
                  'command': cmd, 'cwd': 'repository root', 'started_utc': started,
                  'finished_utc': stamp(), 'elapsed_seconds': round(time.monotonic() - start, 4),
                  'exit_code': proc.returncode, 'stdout': str(stdout_path.relative_to(ROOT)),
                  'stderr': str(stderr_path.relative_to(ROOT)), 'tested_package': package_hashes}
        (OUT / (name + '.record.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
        records.append({key: record[key] for key in ['check', 'status', 'command', 'exit_code', 'stdout', 'stderr']})
        print(json.dumps({'check': name, 'status': record['status'], 'exit_code': proc.returncode}))
    summary = {'kind': 'M11ValidationResults', 'recorded_utc': stamp(),
               'status': 'pass' if all(r['status'] == 'pass' for r in records) else 'fail',
               'checks': records, 'scope': 'Format, deterministic contract/compiler behavior and isolated package execution.',
               'package_snapshot_sha256': {str(Path(row['path']).relative_to(PACKAGE.relative_to(ROOT))): row['sha256']
                                           for row in package_hashes},
               'not_run': ['h3_inference', 'real_workflow_execution', 'media_observation', 'complete_G0_G4',
                           'host_automatic_trigger_rate']}
    (OUT / 'validation-results.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    return 0 if summary['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
