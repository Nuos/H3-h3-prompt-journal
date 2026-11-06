#!/usr/bin/env python3
"""Verify the M11 release's files, source pins, portable layout and protected baseline."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
RELEASE = ROOT / 'docs/h3skill'
PACKAGE = RELEASE / 'h3-model-protocol'
VALIDATION = RELEASE / 'validation/m11'


def load(path):
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError(f'duplicate JSON key in {path}: {key}')
            result[key] = value
        return result

    def nonfinite(value):
        raise ValueError(f'nonfinite JSON in {path}: {value}')

    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=nonfinite)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checks = []

    def record(name, errors, **details):
        checks.append({'check': name, 'status': 'fail' if errors else 'pass',
                       'errors': errors, **details})

    manifest = load(RELEASE / 'release-manifest-m11.json')
    errors, paths = [], set()
    for row in manifest['files']:
        rel = row['path']
        p = ROOT / rel
        if Path(rel).is_absolute() or '..' in Path(rel).parts or rel in paths:
            errors.append('unsafe or duplicate manifest path: ' + rel)
        elif not p.is_file():
            errors.append('missing release file: ' + rel)
        elif sha(p) != row['sha256'] or p.stat().st_size != row['bytes']:
            errors.append('release file drift: ' + rel)
        paths.add(rel)
    record('release_file_hashes', errors, count=len(paths))

    roots = {p.name for p in PACKAGE.iterdir()}
    errors = []
    if roots != {'SKILL.md', 'scripts', 'references', 'assets', 'agents'}:
        errors.append('unexpected package roots: ' + repr(sorted(roots)))
    for p in PACKAGE.rglob('*'):
        if p.is_symlink() or p.name == '__pycache__' or p.suffix == '.pyc':
            errors.append('symlink or generated cache: ' + str(p.relative_to(PACKAGE)))
        if p.is_file() and str(p.relative_to(ROOT)) not in paths:
            errors.append('package file absent from manifest: ' + str(p.relative_to(ROOT)))
    record('portable_layout', errors, roots=sorted(roots),
           note='Only SKILL.md is universal; the other directories are deliberate optional resources.')

    text = (PACKAGE / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    fields, errors = {}, []
    if not match:
        errors.append('frontmatter missing')
    else:
        for line in match.group(1).splitlines():
            key, value = line.split(': ', 1)
            if key in fields:
                errors.append('duplicate frontmatter: ' + key)
            fields[key] = json.loads(value) if value.startswith('"') else value
    name, desc = fields.get('name', ''), fields.get('description', '')
    if set(fields) != {'name', 'description'}:
        errors.append('entry expects name and description')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or name != PACKAGE.name or len(name) > 64:
        errors.append('name constraints or folder mismatch')
    if not isinstance(desc, str) or not 1 <= len(desc) <= 1024 or '<' in desc or '>' in desc:
        errors.append('description constraints')
    if len(text.splitlines()) >= 500 or '[TODO' in text:
        errors.append('entry length or unfinished template')
    record('frontmatter_and_entry', errors, lines=len(text.splitlines()), description_chars=len(desc))

    errors, links = [], []
    for p in [PACKAGE / 'SKILL.md', *sorted((PACKAGE / 'references').glob('*.md'))]:
        content = p.read_text(encoding='utf-8')
        for ref in re.findall(r'\]\(([^)]+)\)', content):
            if re.match(r'[a-z]+://|#', ref):
                continue
            target = (p.parent / ref.split('#')[0]).resolve()
            links.append((str(p.relative_to(PACKAGE)), ref))
            if not target.exists():
                errors.append(f'broken link in {p.name}: {ref}')
    entry_refs = {ref for source, ref in links if source == 'SKILL.md'}
    for p in (PACKAGE / 'references').iterdir():
        if p.is_file() and 'references/' + p.name not in entry_refs:
            errors.append('reference not directly routed from SKILL.md: ' + p.name)
    record('progressive_resource_routes', errors, link_count=len(links))

    errors, json_count, py_count = [], 0, 0
    for p in PACKAGE.rglob('*'):
        try:
            if p.suffix == '.json':
                load(p)
                json_count += 1
            elif p.suffix == '.py':
                ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
                py_count += 1
        except (ValueError, SyntaxError) as exc:
            errors.append(str(exc))
    record('strict_json_and_python_syntax', errors, json_files=json_count, python_files=py_count)

    registry = load(PACKAGE / 'references/module-registry.json')
    schema = load(PACKAGE / 'references/contracts.json')
    expected_parts = {'M11.1': 'capability_profile', 'M11.2': 'reference_binding',
                      'M11.3': 'prompt_compilation', 'M11.4': 'task_export'}
    modules = {row['module_id']: row for row in registry['modules']}
    errors = []
    if len(modules) != len(registry['modules']) or set(modules) != {'M11', *expected_parts}:
        errors.append('registry must define M11 and exactly four independently routed children')
    if schema['x-owned-partitions'] != expected_parts:
        errors.append('contract ownership differs from the registry')
    for mid, part in expected_parts.items():
        row = modules.get(mid, {})
        if row.get('parent_id') != 'M11' or row.get('output_contract', {}).get('exclusive_partition') != part:
            errors.append('wrong parent or partition: ' + mid)
        if row.get('route', {}).get('explicit_target') != mid:
            errors.append('missing explicit child route: ' + mid)
        for key in ('responsibility', 'input_contract', 'output_contract', 'readonly',
                    'write_permissions', 'forbidden_writes', 'dependencies', 'resources',
                    'official_mapping', 'route', 'parent_acceptance', 'consumers', 'invalidation'):
            if key not in row:
                errors.append('missing registry contract key: ' + mid + '.' + key)
    for row in modules.values():
        for ref in row.get('resources', []):
            if not (PACKAGE / ref).is_file():
                errors.append('registry resource missing: ' + ref)
    record('independent_module_registry', errors, module_count=len(modules))

    refs, errors = [], []

    def visit(value):
        if isinstance(value, dict):
            if '$ref' in value:
                refs.append(value['$ref'])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(schema)
    for ref in refs:
        if not isinstance(ref, str) or not ref.startswith('#/'):
            errors.append('schema dependency is not a packaged local reference: ' + str(ref))
            continue
        cursor = schema
        try:
            for part in ref[2:].split('/'):
                cursor = cursor[part.replace('~1', '/').replace('~0', '~')]
        except (KeyError, TypeError):
            errors.append('unresolved schema reference: ' + ref)
    record('contract_schema_reference_closure', errors, definitions=len(schema['$defs']),
           local_references=len(refs),
           note='Local reference closure only; behavioral validation uses the supplied Python contract implementation.')

    case_index = load(PACKAGE / 'references/case-index.json')
    errors, full_lines, projection_lines = [], 0, 0
    for row in case_index['files']:
        rel = row['path']
        if not rel.startswith('case-studies/') or '..' in Path(rel).parts:
            errors.append('case outside content boundary: ' + rel)
            continue
        p = ROOT / rel
        data = p.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        count = len(data.decode('utf-8').splitlines())
        if sha(p) != row['sha256'] or len(data) != row['byte_count'] or blob != row['git_blob_sha1'] or count != row['line_count']:
            errors.append('case source drift: ' + rel)
        if row['read_status'] == 'full_text':
            full_lines += count
            if row['line_ranges'] != [{'start': 1, 'end': count}]:
                errors.append('inconsistent full-text range: ' + rel)
        elif row['read_status'] == 'structured_projection':
            projection_lines += count
            workflow = load(p)
            review = row['structured_review']
            if row['line_ranges'] or len(workflow['nodes']) != review['node_count'] or len(workflow['links']) != review['link_count']:
                errors.append('inconsistent structured projection: ' + rel)
        else:
            errors.append('unknown case reading scope: ' + rel)
    coverage = case_index['coverage']
    if full_lines != coverage['full_text_read_lines'] or projection_lines != coverage['structured_projection_source_lines']:
        errors.append('case scope totals differ from source rows')
    record('case_source_pins_and_scope', errors, indexed_files=len(case_index['files']),
           full_text_lines=full_lines, structured_projection_source_lines=projection_lines,
           note='Hash and scope checks reproduce source identity, not media observation.')

    baseline = load(VALIDATION / 'protected-baseline.json')
    errors = []
    for row in baseline['files']:
        p = ROOT / row['path']
        if not p.is_file() or sha(p) != row['sha256'] or p.stat().st_size != row['bytes']:
            errors.append('protected baseline changed: ' + row['path'])
    record('protected_existing_text', errors, count=len(baseline['files']),
           base_commit=baseline['base_commit'])

    src = load(PACKAGE / 'references/h3-protocol-source.json')
    errors = []
    for row in src['sources']:
        name = row.get('offline_snapshot')
        if name not in {'h3-base-official.txt', 'h3-ref-official.txt'}:
            continue
        p = PACKAGE / 'references' / name
        data = p.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if sha(p) != row['sha256'] or blob != row['git_blob_sha']:
            errors.append('official protocol drift: ' + name)
    record('official_protocol_bytes', errors, commit=src['authority']['commit'])

    std = load(VALIDATION / 'standards-verification.json')
    errors = []
    for row in std['files']:
        p = RELEASE / '_standards' / row['local_path']
        if sha(p) != row['sha256'] or not row['utf8_exact_match'] or not row['remote_blob_match']:
            errors.append('standards source mismatch: ' + row['local_path'])
    record('standards_source_verification', errors, files=len(std['files']))

    validation = load(VALIDATION / 'validation-results.json')
    errors = []
    for row in validation['checks']:
        if row['status'] != 'pass':
            errors.append('validation not passed: ' + row['check'])
    actual_package = {str(p.relative_to(PACKAGE)): sha(p) for p in PACKAGE.rglob('*') if p.is_file()}
    recorded_package = validation['package_snapshot_sha256']
    if actual_package != recorded_package:
        errors.append('package changed after recorded validation')
    record('recorded_validation', errors, note='Records are scoped; no H3 inference or media certification.')

    forward = VALIDATION / 'forward-use'
    review = load(forward / 'review.json')
    errors = []
    if review['status'] != 'pass' or any(row['status'] != 'pass' for row in review['checks']):
        errors.append('forward text-task review has unresolved findings')
    if review['package_snapshot_sha256'] != actual_package:
        errors.append('forward review used a different final package')
    if sha(forward / 'task.md') != review['task_sha256'] or sha(VALIDATION / 'forward-use-task.md') != review['task_sha256']:
        errors.append('forward raw task differs from the reviewed task')
    finalization = load(forward / 'finalization.json')
    final_script = (PACKAGE / 'scripts/m11_contract.py').read_text(encoding='utf-8')
    historical_lines = final_script.splitlines(keepends=True)
    for number in finalization['changed_lines']:
        historical_lines[number - 1] = historical_lines[number - 1].rstrip('\n') + ' \n'
    historical_script = ''.join(historical_lines)
    historical_hash = hashlib.sha256(historical_script.encode()).hexdigest()
    historical_package = load(forward / 'final-input-snapshot.json')['package_files']
    recheck = load(forward / 'release-recheck/record.json')
    if (historical_hash != finalization['before_sha256']
            or historical_hash != historical_package['scripts/m11_contract.py']
            or actual_package['scripts/m11_contract.py'] != finalization['after_sha256']
            or ast.dump(ast.parse(historical_script)) != ast.dump(ast.parse(final_script))):
        errors.append('historical task compiler does not match the documented whitespace-only finalization')
    if recheck['status'] != 'pass' or recheck['package_snapshot_sha256'] != actual_package:
        errors.append('final public CLI recheck used a different package')
    if len(recheck['calls']) != 5 or any(row['exit_code'] != row['expected_exit_code'] for row in recheck['calls']):
        errors.append('final public CLI recheck has incomplete or unexpected outcomes')
    for row in review['integrity_files']:
        rel = Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:
            errors.append('unsafe forward record path: ' + str(rel))
            continue
        p = forward / rel
        if not p.is_file() or sha(p) != row['sha256'] or p.stat().st_size != row['bytes']:
            errors.append('forward record drift: ' + str(rel))
    record('forward_use_and_review_records', errors, counts=review['counts'],
           note='One text task with a disclosed supervised correction; expected runtime_unknown is not a successful runtime export.')
    result = {'kind': 'M11ReleaseVerification', 'status': 'pass' if all(c['status'] == 'pass' for c in checks) else 'fail',
              'checks': checks, 'h3_inference': 'not_run', 'media_observation': 'not_run'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'kind': 'M11ReleaseVerification', 'status': 'fail', 'error': str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
