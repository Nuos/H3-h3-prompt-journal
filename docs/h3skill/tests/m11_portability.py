#!/usr/bin/env python3
"""Run M11 from a copied package with no repository or third-party Python packages.

All generated requests, proposals and state files live in a TemporaryDirectory.
The runner prints its report; the release harness may record that stdout.
"""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


sys.dont_write_bytecode = True
PACKAGE = Path(__file__).resolve().parents[1] / 'h3-model-protocol'


def digest_tree(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}


def main():
    checks = []
    with tempfile.TemporaryDirectory(prefix='m11-detached-') as directory:
        outside = Path(directory)
        installed = outside / 'installed'
        package = installed / PACKAGE.name
        shutil.copytree(PACKAGE, package, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))
        cwd = outside / 'unrelated-working-directory'
        cwd.mkdir()
        before = digest_tree(package)
        script = package / 'scripts/m11_contract.py'
        examples = package / 'assets/examples'
        python = str(Path(sys.executable).resolve())
        env = {'PATH': '', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}

        def save(name, value):
            path = cwd / name
            path.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False), encoding='utf-8')
            return path

        def call(name, *arguments, expected_kind=None, expected_status=None, help_output=False):
            proc = subprocess.run([python, '-I', '-S', '-B', str(script), *map(str, arguments)],
                                  cwd=cwd, env=env, capture_output=True, text=True, timeout=30)
            try:
                result = json.loads(proc.stdout) if not help_output else {}
            except ValueError:
                result = {'status': 'invalid_json'}
            valid = proc.returncode == 0 and isinstance(result, dict)
            if help_output:
                valid = valid and all(word in proc.stdout for word in ('route', 'propose', 'check', 'accept', 'impact'))
            else:
                valid = valid and result.get('status') not in ('fail', 'failed', 'invalid_json')
            if expected_kind:
                valid = valid and result.get('kind') == expected_kind
            if expected_status:
                valid = valid and result.get('status') == expected_status
            checks.append({'name': name, 'passed': valid, 'exit_code': proc.returncode,
                           'status': result.get('status'), 'kind': result.get('kind'),
                           'errors': result.get('errors', []), 'stderr': proc.stderr})
            return result

        call('isolated_help', '--help', help_output=True)
        batch_doc = json.loads((examples / 'requests.json').read_text(encoding='utf-8'))
        requests = batch_doc if isinstance(batch_doc, list) else batch_doc['requests']
        proposals = []
        for request in requests:
            tag = request['target'].lower().replace('.', '-')
            request_file = save(tag + '-request.json', request)
            route = call(tag + '_independent_route', 'route', request_file, expected_status='ready')
            checks.append({'name': tag + '_route_is_not_execution',
                           'passed': route.get('invocation_status') == 'not_invoked'})
            proposal = call(tag + '_independent_propose', 'propose', request_file, expected_kind='M11Proposal')
            proposal_file = save(tag + '-proposal.json', proposal)
            proposals.append(proposal)
            call(tag + '_independent_check', 'check', proposal_file, '--request', request_file,
                 expected_status='passed_with_unverified')
            result = call(tag + '_independent_accept', 'accept', proposal_file, '--requests', request_file,
                          '--state', examples / 'state-empty.json', expected_status='passed_with_unverified')
            checks.append({'name': tag + '_partial_accept_stays_unexecuted',
                           'passed': result.get('state', {}).get('status') in ('draft', 'partial')
                                     and len(result.get('state', {}).get('content', {})) == 1})

        for mode in ('t2va', 'i2va', 'fl2va', 'l2va', 'ref2va'):
            request_file = examples / (mode + '-request.json')
            proposal = call(mode + '_compile', 'propose', request_file, expected_kind='M11Proposal')
            proposal_file = save(mode + '-proposal.json', proposal)
            call(mode + '_original_request_check', 'check', proposal_file, '--request', request_file,
                 expected_status='passed_with_unverified')

        requests_file = save('requests.json', requests)
        proposals_file = save('proposals.json', proposals)
        accepted = call('atomic_parent_accept', 'accept', proposals_file, '--requests', requests_file,
                        '--state', examples / 'state-empty.json', expected_status='passed_with_unverified')
        if 'state' in accepted:
            state_file = save('accepted-state.json', accepted['state'])
            replay = call('exact_parent_retry', 'accept', proposals_file, '--requests', requests_file,
                          '--state', state_file, expected_status='passed_with_unverified')
            checks.append({'name': 'idempotent_retry_preserves_state',
                           'passed': replay.get('idempotent') is True and replay.get('state') == accepted['state']})
            display = json.loads(json.dumps(accepted['state']))
            display['display'] = {'title': 'A new display title'}
            display_file = save('display-change.json', display)
            impact = call('display_only_impact', 'impact', state_file, display_file)
            checks.append({'name': 'display_only_diff_is_a_review_aid',
                           'passed': impact.get('changed_paths') == ['/display']
                                     and impact.get('review_required') is True
                                     and 'child_invocation' in impact.get('not_run', [])})
        else:
            checks.append({'name': 'accepted_state_available', 'passed': False})

        imports = set()
        for path in (package / 'scripts').glob('*.py'):
            for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
                if isinstance(node, ast.Import):
                    imports.update(alias.name.split('.')[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imports.add((node.module or '').split('.')[0])
        bundled = {p.stem for p in (package / 'scripts').glob('*.py')}
        external = imports - set(sys.stdlib_module_names) - bundled - {'__future__'}
        checks.append({'name': 'only_standard_library_and_bundled_imports', 'passed': not external,
                       'external_imports': sorted(external)})
        checks.append({'name': 'installed_package_is_unchanged', 'passed': digest_tree(package) == before})
        checks.append({'name': 'only_one_skill_package_was_installed',
                       'passed': list(installed.iterdir()) == [package]
                                 and not (outside / '.git').exists()
                                 and not (outside / 'docs/skillplan').exists()
                                 and not (outside / 'case-studies').exists()})
        report = {'suite': 'm11-portability', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
                  'status': 'passed' if all(check['passed'] for check in checks) else 'failed',
                  'checks_run': len(checks), 'checks': checks, 'copied_files': len(before),
                  'isolation': 'Python -I -S -B, empty PATH, unrelated cwd, copied M11 package only',
                  'not_run': ['h3_inference', 'real_workflow_execution', 'media_observation',
                              'semantic_quality_certification', 'complete_G0_G4']}
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
