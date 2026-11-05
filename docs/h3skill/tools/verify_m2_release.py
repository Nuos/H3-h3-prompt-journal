#!/usr/bin/env python3
"""Reproduce M2 release integrity checks. No semantic or media certification.

--write-manifest saves the M2 release inventory; all other operations are read-only.
The historical M1 release-manifest.json is deliberately left unchanged.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

DELIVERY = Path(__file__).resolve().parents[1]
REPO = DELIVERY.parents[1]
SKILL = DELIVERY / 'h3-asset-reference'
BASE = 'faa8edc311589d68d37e93524c7cb8e553fff857'
MANIFEST = DELIVERY / 'release-manifest-m2.json'
SCOPES = ('h3-asset-reference', 'tests/m2', 'validation/m2')
SINGLES = ('README.md', '20261105-development-m2-v001.md', 'tools/verify_m2_release.py')
EXCLUDE = {'validation/m2/release-check.json'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def inventory():
    paths = set(DELIVERY / name for name in SINGLES)
    for scope in SCOPES:
        paths.update(p for p in (DELIVERY / scope).rglob('*') if p.is_file())
    entries = []
    for path in sorted(paths):
        rel = path.relative_to(DELIVERY).as_posix()
        if rel in EXCLUDE or '__pycache__' in path.parts or path.suffix in ('.pyc', '.pyo'):
            continue
        if path.is_file():
            data = path.read_bytes()
            entries.append({'path': rel, 'bytes': len(data), 'sha256': sha(data),
                            'git_blob_sha': blob(data)})
    return {'kind': 'M2ReleaseManifest', 'version': '1.0.0',
            'package': 'h3-asset-reference', 'package_version': '0.1.0',
            'repository_base': BASE, 'scope': list(SCOPES) + list(SINGLES),
            'self_hash_policy': 'Manifest fixed by Git commit; no self hash.',
            'excluded_report': sorted(EXCLUDE),
            'exclusion_reason': 'Avoid a report/manifest self-reference cycle; report is committed separately.',
            'files': entries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-manifest', action='store_true')
    args = parser.parse_args()
    checks = []

    def check(name, ok, detail=None):
        checks.append({'check': name, 'passed': bool(ok), 'detail': detail})

    entry = (SKILL / 'SKILL.md').read_text()
    match = re.match(r'\A---\nname: ([^\n]+)\ndescription: ("[^\n]+")\n---\n', entry)
    valid = bool(match)
    if match:
        name, description = match[1], json.loads(match[2])
        valid = (name == SKILL.name and bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name))
                 and len(name) <= 64 and 1 <= len(description) <= 1024)
    check('minimal_name_description_frontmatter', valid)
    check('entry_below_recommended_500_lines', len(entry.splitlines()) < 500,
          len(entry.splitlines()))
    roots = {p.name for p in SKILL.iterdir() if p.name != '__pycache__'}
    check('only_required_runtime_roots', roots == {'SKILL.md', 'references', 'scripts', 'assets'}, sorted(roots))
    broken, outside = [], []
    for path in sorted(SKILL.rglob('*.md')):
        for target in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)', path.read_text()):
            if target.startswith(('https://', 'http://', '#')):
                continue
            local = (path.parent / target.split('#')[0]).resolve()
            if not local.exists():
                broken.append(f'{path.relative_to(SKILL)} -> {target}')
            if not local.is_relative_to(SKILL.resolve()):
                outside.append(f'{path.relative_to(SKILL)} -> {target}')
    check('runtime_links_exist', not broken, broken)
    check('no_sibling_runtime_links', not outside, outside)
    referenced = set(re.findall(r'\]\((references/[^)#]+)', entry))
    resources = {p.relative_to(SKILL).as_posix() for p in (SKILL / 'references').iterdir() if p.is_file()}
    check('every_reference_discoverable_from_entry', resources <= referenced, sorted(resources - referenced))

    failures = []
    for record in inventory()['files']:
        path = DELIVERY / record['path']
        try:
            if path.suffix == '.json':
                json.loads(path.read_text())
            elif path.suffix == '.py':
                ast.parse(path.read_text())
        except (ValueError, SyntaxError) as exc:
            failures.append({'path': record['path'], 'error': str(exc)})
    check('json_python_parse', not failures, failures)
    registry = json.loads((SKILL / 'references/module-registry.json').read_text())
    check('four_public_nodes', set(registry['nodes']) == {'M2', 'M2.1', 'M2.2', 'M2.3'})
    missing_resources = [r for node in registry['nodes'].values() for r in node['resources']
                         if not (SKILL / r).is_file()]
    check('route_resources_available', not missing_resources, missing_resources)

    lock = json.loads((REPO / 'docs/skillplan/baseline-lock.json').read_text())
    mismatches = [r['path'] for r in lock['files'] + lock['control_files']
                  if sha((REPO / r['path']).read_bytes()) != r['sha256']]
    check('frozen_plan_and_controls_unchanged', not mismatches, mismatches)
    tree = subprocess.run(['git', 'ls-tree', '-r', BASE, '--', 'docs/h3skill/h3-work-intent'],
                          cwd=REPO, text=True, capture_output=True, check=True)
    changed_m1 = []
    for line in tree.stdout.splitlines():
        info, path = line.split('\t', 1)
        q = REPO / path
        if not q.exists() or blob(q.read_bytes()) != info.split()[2]:
            changed_m1.append(path)
    check('m1_runtime_byte_unchanged', bool(tree.stdout) and not changed_m1, changed_m1)

    index = json.loads((SKILL / 'references/case-index.json').read_text())
    source_errors = [r['path'] for r in index['files']
                     if sha((REPO / r['path']).read_bytes()) != r['sha256']
                     or blob((REPO / r['path']).read_bytes()) != r['git_blob_oid']]
    check('case_inventory_29_cases_98_texts', len(index['cases']) == 29 and len(index['files']) == 98)
    check('case_texts_match_pinned_hashes', not source_errors, source_errors)
    check('case_media_not_claimed_observed', index['coverage']['media_observations_performed'] == 0)
    for name, digest in {
        'h3-base-official.txt': '2cfebc096a6e08370f288d468d90b60f7f9bcb938f94bf090816e910e48e75fc',
        'h3-ref-official.txt': '1e574f356716ad55612247ffb7bbccbcdb484ad96599d63c7dca1af186b1fab7',
    }.items():
        check('exact_official_snapshot_' + name, sha((SKILL / 'references' / name).read_bytes()) == digest)

    standard = DELIVERY / '_standards'
    std = json.loads((standard / 'source-files.json').read_text())
    check('official_standard_snapshot_hashes', all(sha((standard / r['local_path']).read_bytes()) == r['sha256']
                                                 for r in std['files']))
    test_record = json.loads((DELIVERY / 'tests/m2/test-results.json').read_text())
    untested_changes = [path for path, digest in test_record['file_sha256'].items()
                        if sha((DELIVERY / path).read_bytes()) != digest]
    check('tested_m2_runtime_and_examples_unchanged', not untested_changes, untested_changes)
    check('m2_behavioral_tests_no_failures', test_record['failures'] == 0 and test_record['errors'] == 0,
          {key: test_record[key] for key in ('tests_run', 'passed', 'skipped')})

    forward = DELIVERY / 'validation/m2/forward-use'
    snapshot_errors = []
    for manifest_name in ('source-manifest.json', 'final-source-manifest.json', 'final-run-source-manifest.json'):
        snapshot_manifest = json.loads((forward / manifest_name).read_text())
        for item in snapshot_manifest['files']:
            captured = forward / item['snapshot']
            if not captured.is_file() or sha(captured.read_bytes()) != item['sha256']:
                snapshot_errors.append(item['snapshot'])
    check('forward_use_recorded_snapshots_match', not snapshot_errors, snapshot_errors)
    final_copy = forward / 'snapshot-final-run/docs/h3skill/h3-asset-reference'
    runtime_names = ('scripts/m2_contract.py', 'references/contracts.json', 'references/module-registry.json')
    check('forward_use_final_executable_resources_match_release',
          all((final_copy / name).read_bytes() == (SKILL / name).read_bytes() for name in runtime_names),
          list(runtime_names))
    log_errors = []
    logs = sorted((forward / 'execution').glob('*/*.json'))
    for path in logs:
        record = json.loads(path.read_text())
        task = path.name.split('--')[0]
        proposal_name = 'proposal.revised.json' if 'proposal-revised-check' in path.name else 'proposal.json'
        files = {'request_sha256': forward / task / 'request.json',
                 'proposal_sha256': forward / task / proposal_name,
                 'script_sha256': forward / path.parent.name / 'docs/h3skill/h3-asset-reference/scripts/m2_contract.py'}
        result = json.loads(record['stdout'])
        expected_exit = 1 if task == 'task2-xiashan-seg01' and 'proposal' in path.name else 0
        if (any(sha(p.read_bytes()) != record[key] for key, p in files.items())
                or record['exit_code'] != expected_exit
                or result['audit']['semantic'] != 'unverified'
                or result['audit']['media'] != 'unverified'):
            log_errors.append(path.relative_to(forward).as_posix())
    check('forward_use_13_logged_calls_preserve_inputs_and_outcomes',
          len(logs) == 13 and not log_errors, {'calls': len(logs), 'mismatches': log_errors})
    fmt = subprocess.run([sys.executable, str(standard / 'anthropics-quick-validate.py'), str(SKILL)],
                         capture_output=True, text=True)
    check('anthropic_official_quick_validate', fmt.returncode == 0,
          {'exit_code': fmt.returncode, 'stdout': fmt.stdout, 'stderr': fmt.stderr})

    with tempfile.TemporaryDirectory(prefix='m2-portability-') as temp:
        portable = Path(temp) / SKILL.name
        shutil.copytree(SKILL, portable, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        proc = subprocess.run([sys.executable, str(portable / 'scripts/m2_contract.py'),
                               'accept', str(portable / 'assets/state-empty.json'),
                               str(portable / 'assets/proposal-batch.json')],
                              cwd=temp, capture_output=True, text=True)
        try:
            result = json.loads(proc.stdout)
        except ValueError:
            result = {}
        check('isolated_directory_acceptance', proc.returncode == 0 and result.get('state', {}).get('version') == 1,
              {'exit_code': proc.returncode, 'outcome': result.get('outcome'), 'stderr': proc.stderr})
        check('portable_result_does_not_certify_media', result.get('audit', {}).get('media') == 'unverified',
              result.get('audit'))

    expected = inventory()
    if args.write_manifest:
        MANIFEST.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + '\n')
    check('m2_release_manifest_matches_files', MANIFEST.is_file() and json.loads(MANIFEST.read_text()) == expected)
    output = {'kind': 'M2ReleaseIntegrityCheck', 'recorded_at': datetime.now(timezone.utc).isoformat(),
              'repository_base': BASE, 'skill_entry_sha256': sha((SKILL / 'SKILL.md').read_bytes()),
              'passed': all(item['passed'] for item in checks), 'checks': checks,
              'scope_limit': 'Structure, integrity and isolated deterministic execution only; semantic/media require separate evidence.'}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
