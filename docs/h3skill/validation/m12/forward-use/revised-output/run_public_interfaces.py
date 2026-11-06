from pathlib import Path
import subprocess,json,datetime
ROOT=Path('/workspace/scratch/67acb32e99b3/m12-forward-run')
OUT=ROOT/'revised-output'
CLI=ROOT/'h3-audit-repair/scripts/m12_contract.py'
def invoke(label,args):
    command=['python',str(CLI),*map(str,args)]
    r=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
    record={'command':command,'cwd':str(ROOT),'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    (OUT/'commands'/f'{label}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    (OUT/'results'/f'{label}.stdout.json').write_text(r.stdout)
    (OUT/'results'/f'{label}.stderr.txt').write_text(r.stderr)
    parsed=json.loads(r.stdout) if r.stdout else {}
    print(json.dumps({'label':label,'exit_code':r.returncode,'status':parsed.get('status'),'kind':parsed.get('kind'),'errors':parsed.get('errors',[]),'stderr':r.stderr[:300]},ensure_ascii=False))
    return r
if __name__=='__main__':
    for name in ['audit','repair']:
        req=OUT/'requests'/f'{name}-request.json'
        invoke(f'01-{name}-route',['route',req])
        r=invoke(f'01-{name}-propose',['propose',req])
        if r.returncode==0:
            invoke(f'01-{name}-check',['check',OUT/'results'/f'01-{name}-propose.stdout.json','--request',req])
