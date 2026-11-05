#!/usr/bin/env python3
"""Record actual route/check invocations; never accept proposals or call media services."""
import hashlib, json, shlex, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone
out=Path(__file__).resolve().parent
repo=out.parents[4]
which=sys.argv[1] if len(sys.argv)>1 else 'snapshot'
if which not in ('snapshot','snapshot-final','snapshot-final-run'): raise SystemExit('unknown snapshot')
runner=out/which/'docs/h3skill/h3-asset-reference/scripts/m2_contract.py'
record=out/'execution'/which
record.mkdir(parents=True,exist_ok=True)
logs=[]
for task in ['task1-identity','task2-xiashan-seg01']:
    request=out/task/'request.json'; proposal=out/task/'proposal.json'
    for action,extra in [('route',['route',str(request)]),('request-check',['check',str(request)]),('proposal-check',['check',str(proposal),'--request',str(request)])]:
        target=record/(task+'--'+action+'.json')
        if target.exists(): raise SystemExit('Refusing to overwrite first result: '+str(target))
        cmd=[sys.executable,str(runner),*extra]
        before=datetime.now(timezone.utc).isoformat()
        proc=subprocess.run(cmd,cwd=repo,text=True,capture_output=True)
        data={'start_time':before,'end_time':datetime.now(timezone.utc).isoformat(),
              'cwd':str(repo),'argv':cmd,'command':shlex.join(cmd),'exit_code':proc.returncode,
              'script_sha256':hashlib.sha256(runner.read_bytes()).hexdigest(),
              'request_sha256':hashlib.sha256(request.read_bytes()).hexdigest(),
              'proposal_sha256':hashlib.sha256(proposal.read_bytes()).hexdigest(),
              'stdout':proc.stdout,'stderr':proc.stderr}
        target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        logs.append(data)
        print(task,action,'exit',proc.returncode)
        print(proc.stdout)
        if proc.stderr: print(proc.stderr)
(record/'commands.md').write_text('# 实际执行命令\n\n'+''.join('## '+str(n+1)+'\n\n```sh\n'+x['command']+'\n```\n\n退出码：'+str(x['exit_code'])+'。开始：'+x['start_time']+'。\n\n' for n,x in enumerate(logs)))
