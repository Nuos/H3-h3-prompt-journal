#!/usr/bin/env python3
"""Exercise the detached M10 package without repository, PATH tools, site packages or SDKs."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent / 'h3-visual-look'


def tree_digest(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}


def main():
    checks = []
    with tempfile.TemporaryDirectory(prefix='m10-detached-') as folder:
        outside = Path(folder)
        package = outside / 'installed' / PACKAGE.name
        shutil.copytree(PACKAGE, package, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))
        cwd = outside / 'unrelated-working-directory'
        cwd.mkdir()
        before = tree_digest(package)
        # Only an absolute Python interpreter is available. -I ignores user Python configuration.
        env = {'PATH': '', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}
        script = package / 'scripts/m10_contract.py'
        assets = package / 'assets'

        def call(name, *args, help_output=False):
            proc = subprocess.run([str(Path(sys.executable).resolve()), '-I', '-S', '-B', str(script), *map(str, args)],
                                  cwd=cwd, env=env, capture_output=True, text=True)
            if help_output:
                result = {'status': 'passed' if 'accept' in proc.stdout and 'impact' in proc.stdout else 'invalid_help'}
            else:
                try:
                    result = json.loads(proc.stdout)
                except ValueError:
                    result = {'status': 'invalid_json'}
            passed = proc.returncode == 0 and result.get('status') in ('passed', 'passed_with_unverified')
            checks.append({'name': name, 'passed': passed, 'exit_code': proc.returncode,
                           'status': result.get('status'), 'errors': result.get('errors', []), 'stderr': proc.stderr})
            return result

        call('isolated_help', '--help', help_output=True)
        for i in (1, 2, 3, 4):
            request = assets / f'request-standalone-m10-{i}.json'
            proposal = assets / f'proposal-standalone-m10-{i}.json'
            call(f'independent_route_m10_{i}', 'route', request)
            call(f'independent_check_m10_{i}', 'check', proposal, '--request', request)
            call(f'independent_accept_m10_{i}', 'accept', assets / 'state-empty.json', proposal, '--requests', request)
        for i in (1, 2, 3, 4):
            request = assets / f'request-minimal-m10-{i}.json'
            proposal = assets / f'proposal-minimal-m10-{i}.json'
            call(f'minimal_route_m10_{i}', 'route', request)
            call(f'minimal_check_m10_{i}', 'check', proposal, '--request', request)
            call(f'minimal_accept_m10_{i}', 'accept', assets / 'state-empty.json', proposal, '--requests', request)
        accepted = call('atomic_parent_accept', 'accept', assets / 'state-empty.json', assets / 'proposal-batch.json', '--requests', assets / 'requests.json')
        if 'state' in accepted:
            state_path = cwd / 'accepted-state.json'
            state_path.write_text(json.dumps(accepted['state'], ensure_ascii=False), encoding='utf-8')
            replay = call('idempotent_parent_replay', 'accept', state_path, assets / 'proposal-batch.json', '--requests', assets / 'requests.json')
            checks.append({'name': 'exact_replay_preserves_state_and_version', 'passed': replay.get('idempotent') is True and replay.get('state') == accepted['state']})
        else:
            checks.append({'name': 'accepted_state_available', 'passed': False})
        result = call('registered_read_path_impact', 'impact', '--before', assets / 'impact-before.json', '--after', assets / 'impact-after.json')
        checks.append({'name': 'display_only_change_does_not_stale_unrelated_readers',
                       'passed': result.get('changed_paths') == ['/display'] and all(c['status'] == 'current' for c in result.get('consumers', []))})
        imports = set()
        for path in (package / 'scripts').glob('*.py'):
            for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
                if isinstance(node, ast.Import):
                    imports.update(alias.name.split('.')[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imports.add((node.module or '').split('.')[0])
        bundled = {path.stem for path in (package / 'scripts').glob('*.py')}
        nonstdlib = imports - set(sys.stdlib_module_names) - bundled - {'__future__'}
        checks.append({'name': 'standard_library_and_own_helper_only', 'passed': not nonstdlib, 'unbundled_imports': sorted(nonstdlib)})
        checks.append({'name': 'installed_package_unchanged', 'passed': before == tree_digest(package)})
        checks.append({'name': 'no_upstream_or_repository_in_detached_tree',
                       'passed': list((outside / 'installed').iterdir()) == [package] and not (outside / '.git').exists()
                                 and not (outside / 'docs/skillplan').exists() and not (outside / 'case-studies').exists()})
        report = {'suite': 'm10-portability', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
                  'status': 'passed' if all(c['passed'] for c in checks) else 'failed', 'checks_run': len(checks),
                  'checks': checks, 'copied_files': len(before), 'dependencies': 'Python 3.10+ standard library, only one copied skill package',
                  'isolation': 'Python -I -S -B; empty PATH; unrelated cwd; no SDK/site dependency or upstream invocation',
                  'media_verification': 'not_performed'}
    target = HERE / 'm10/portability-results.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
