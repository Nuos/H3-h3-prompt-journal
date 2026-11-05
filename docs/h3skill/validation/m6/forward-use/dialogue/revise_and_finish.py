#!/usr/bin/env python3
"""Preserve the actual v1 failure and repair only its invalid Fact values."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
CLI = ROOT / 'docs/h3skill/h3-sound-music-dialogue/scripts/m6_contract.py'

def load(name):
    return json.loads((OUT / name).read_text())

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def repair_sources(partition):
    for item in partition['items'].values():
        if item['source_kind'] in ('environment', 'object'):
            item['voice_requirement'] = {'state': 'known', 'value': '非人声源：不设置人声音色或发声要求。', 'source_refs': ['sound_design']}

requests = load('requests.json')
proposals = load('proposal-batch-v1.json')['proposals']
for i in (1, 2, 4):
    r = requests[i-1]
    p = proposals[i-1]
    r['request_id'] += '_v2'
    if 'source_context' in r['inputs']:
        repair_sources(r['inputs']['source_context'])
    p['proposal_id'] = p['proposal_id'].replace('_v1', '_v2')
    p['source_request_id'] = r['request_id']
    p['context'] = copy.deepcopy(r['inputs'])
    if i == 1:
        repair_sources(p['changes']['sources'])
    save(f'request-m6-{i}-v2.json', r)
    save(f'proposal-m6-{i}-v2.json', p)
save('requests-v2.json', requests)
batch = load('proposal-batch-v1.json')
batch.update(batch_id='dialogue_batch_v2', proposals=proposals)
save('proposal-batch-v2.json', batch)

run_dir = OUT / ('repair-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
run_dir.mkdir()
summary = load('run-summary.json')
save('run-summary-v1.json', summary)
logs = summary['commands']
commands = [(f'check-m6-{i}-v2', ['check', f'proposal-m6-{i}-v2.json', '--request', f'request-m6-{i}-v2.json']) for i in (1, 2, 4)]
commands += [('accept-v2', ['accept', 'state-empty.json', 'proposal-batch-v2.json', '--requests', 'requests-v2.json'])]
for label, args in commands:
    index = len(logs) + 1
    cmd = [sys.executable, '-B', str(CLI), *args]
    cp = subprocess.run(cmd, cwd=OUT, text=True, capture_output=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    prefix = f'{index:02d}-{label}'
    (run_dir / (prefix + '.stdout.json')).write_text(cp.stdout)
    (run_dir / (prefix + '.stderr.txt')).write_text(cp.stderr)
    entry = {'call': index, 'label': label, 'command': cmd, 'cwd': str(OUT), 'returncode': cp.returncode, 'stdout': f'{run_dir.name}/{prefix}.stdout.json', 'stderr': f'{run_dir.name}/{prefix}.stderr.txt'}
    logs.append(entry)
    with (run_dir / 'commands.jsonl').open('a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    result = json.loads(cp.stdout)
    print(json.dumps({'label': label, 'returncode': cp.returncode, 'validation': result.get('validation'), 'blocking': [d for d in result.get('diagnostics', []) if d.get('blocking')], 'keys': list(result)}, ensure_ascii=False))
    if label == 'accept-v2' and cp.returncode == 0:
        save('final-state.json', result['state'])
        summary['final_disposition'] = result['disposition']
        summary['final_validation'] = result['validation']
summary.update(cli_calls=len(logs), failure_calls=sum(x['returncode'] != 0 for x in logs), commands=logs, repair_directory=run_dir.name,
               state_status=load('final-state.json')['status'] if (OUT / 'final-state.json').exists() else 'not_accepted',
               revision='v2: corrected voice_requirement Fact type for environment/object sources; retained all v1 artifacts and actual failures',
               runtime_sha256_after=hashlib.sha256(CLI.read_bytes()).hexdigest())
if (OUT / 'final-state.json').exists():
    final = load('final-state.json')
    summary['final_version'] = final['version']
    summary['record_counts'] = {key: len(value['items']) for key, value in final['content'].items()}
    summary['open_issues'] = len(final['issues'])
save('run-summary.json', summary)
print(json.dumps({k:v for k,v in summary.items() if k != 'commands'},ensure_ascii=False,indent=2))
