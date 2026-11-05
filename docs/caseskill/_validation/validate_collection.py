#!/usr/bin/env python3
"""Validate the whole case-skill collection, using the pinned skills-ref too.

Install validation-only dependencies with:
  python3 -m pip install ./docs/caseskill/_standards/skills-ref
Skill execution itself only needs the standard library.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, help='Write a JSON result as well as stdout')
    args = parser.parse_args()
    root = args.root.resolve()
    sys.path.insert(0, str(root / '_standards/skills-ref/src'))
    try:
        from skills_ref import validate
    except ImportError as exc:
        print(json.dumps({'pass':False,'dependency_error':str(exc),'remedy':'Install the bundled skills-ref validation package; do not silently skip official validation.'}))
        return 2
    try:
        catalog = json.loads((root/'catalog.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        print(json.dumps({'pass':False,'catalog_error':str(exc)}))
        return 2
    entries = catalog['skills']
    errors, results = [], []
    expected_cases = set(catalog['source_cases'])
    declared_cases = [x['case_id'] for x in entries]
    if len(declared_cases) != len(set(declared_cases)) or set(declared_cases) != expected_cases:
        errors.append('Case coverage is not one-to-one')
    repo = root.parent.parent
    actual_cases_dir = repo/'case-studies'
    if actual_cases_dir.exists():
        actual_cases = {p.name for p in actual_cases_dir.iterdir() if p.is_dir()}
        if actual_cases != expected_cases:
            errors.append('Repository case inventory has changed; refresh coverage and source manifests')
    directories = {p.name for p in root.iterdir() if p.is_dir() and p.name.startswith('h3-')}
    if directories != {x['skill_name'] for x in entries}:
        errors.append('Skill directories do not match the catalog')
    scripts = set()
    source_total = 0
    for entry in entries:
        skill = root/entry['skill_name']
        local = []
        official = validate(skill)
        local.extend('skills-ref: '+str(x) for x in official)
        content = (skill/'SKILL.md').read_text(encoding='utf-8')
        count = len(content.splitlines())
        if count >= 500:
            local.append('SKILL.md exceeds the collection limit of 499 lines')
        if '[TODO:' in content or 'Structuring This Skill' in content:
            local.append('Initializer placeholder remains')
        if f'name: {skill.name}\n' not in content:
            local.append('name and directory do not match')
        for rel in ('references/case-method.md','references/h3-official.md','references/source-index.md','references/plan-schema.md','references/provenance.json','assets/plan-template.json','assets/output-template.md','assets/case-contract.json','scripts/audit_plan.py','agents/openai.yaml','evals/evals.json','LICENSE.txt'):
            if not (skill/rel).is_file() or not (skill/rel).stat().st_size:
                local.append('Missing or empty resource: '+rel)
        # Source snapshots intentionally retain original media links and local paths.
        authored = [skill/'SKILL.md',skill/'references/case-method.md',skill/'references/source-index.md',skill/'references/h3-official.md',skill/'references/plan-schema.md',skill/'assets/output-template.md']
        for p in authored:
            text = p.read_text(encoding='utf-8')
            for target in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)',text):
                if target.startswith(('https://','http://','#')):
                    continue
                target = target.split('#')[0]
                if target and not (p.parent/target).exists():
                    local.append(f'Broken authored link in {p.name}: {target}')
        meta = json.loads((skill/'references/provenance.json').read_text())
        records = meta['case_and_review_files']
        case_records = [x for x in records if x['path'].startswith('case-studies/')]
        source_total += len(case_records)
        if len(case_records) != entry['source_text_count']:
            local.append('Case text count mismatch')
        if actual_cases_dir.exists():
            originals = {p.relative_to(repo).as_posix() for p in (actual_cases_dir/entry['case_id']).rglob('*') if p.is_file() and p.suffix.lower() in {'.md','.txt','.json','.yaml','.yml','.csv','.tsv','.py','.sh','.toml','.html','.js','.ts'}}
            if originals != {x['path'] for x in case_records}:
                local.append('Not all case text files are represented')
        for rec in records:
            copy = skill/rec['local_path']
            if not copy.is_file():
                local.append('Missing source copy: '+rec['local_path'])
                continue
            data = copy.read_bytes()
            if hashlib.sha256(data).hexdigest() != rec['sha256'] or len(data) != rec['bytes']:
                local.append('Source copy changed: '+rec['local_path'])
            original = repo/rec['path']
            if original.is_file() and hashlib.sha256(original.read_bytes()).hexdigest() != rec['sha256']:
                local.append('Upstream case/review changed: '+rec['path'])
        contract = json.loads((skill/'assets/case-contract.json').read_text())
        plan = json.loads((skill/'assets/plan-template.json').read_text())
        if contract['case_id'] != entry['case_id'] or plan['case_id'] != entry['case_id']:
            local.append('Contract/template case mismatch')
        if set(contract['required_check_ids']) != {x['id'] for x in plan['case_checks']}:
            local.append('Case gate template differs from contract')
        scenarios = json.loads((skill/'evals/evals.json').read_text())
        if scenarios['skill_name'] != skill.name or len(scenarios['evals']) < 3:
            local.append('Missing representative scenarios')
        ui = (skill/'agents/openai.yaml').read_text()
        if '$'+skill.name not in ui:
            local.append('Default UI prompt does not invoke this skill')
        script = skill/'scripts/audit_plan.py'
        scripts.add(hashlib.sha256(script.read_bytes()).hexdigest())
        help_run = subprocess.run([sys.executable,str(script),'--help'],capture_output=True,text=True)
        if help_run.returncode:
            local.append('Audit script --help failed')
        draft_run = subprocess.run([sys.executable,str(script),str(skill/'assets/plan-template.json'),'--strict'],capture_output=True,text=True)
        if draft_run.returncode != 1:
            local.append('Unfilled draft template must be rejected by strict audit')
        results.append({'case_id':entry['case_id'],'skill_name':skill.name,'official_skills_ref_pass':not official,'skill_lines':count,'source_text_count':len(case_records),'scenario_count':len(scenarios['evals']),'errors':local,'pass':not local})
    if len(scripts) != 1:
        errors.append('Independent copies of the shared auditor have diverged')
    report = {'pass':not errors and all(x['pass'] for x in results),'cases':len(entries),'case_text_files':source_total,'official_spec_commit':catalog['official_sources']['agentskills_commit'],'h3_official_commit':catalog['official_sources']['minimax_h3_commit'],'errors':errors,'skills':results,'scope':'Format, coverage, resource paths, source integrity and tooling; no model inference or semantic-video certification.'}
    text = json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding='utf-8')
    print(text,end='')
    return 0 if report['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
