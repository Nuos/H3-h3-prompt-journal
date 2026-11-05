#!/usr/bin/env python3
"""Execute a read/check for the M1 trial and retain its exact subprocess transcript."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, subprocess, sys
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
p=argparse.ArgumentParser()
p.add_argument("name")
p.add_argument("--limit",type=int,default=24000)
p.add_argument("argv",nargs=argparse.REMAINDER)
a=p.parse_args()
argv=a.argv[1:] if a.argv and a.argv[0]=="--" else a.argv
if not argv: p.error("command required")
log=ROOT/"logs"
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
r=subprocess.run(argv,cwd=str(REPO),env=env,capture_output=True)
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
for suffix,b in (("stdout",r.stdout),("stderr",r.stderr)):
    out=log/(a.name+"."+suffix+".txt")
    with out.open("xb") as f: f.write(b)
record={"name":a.name,"argv":argv,"cwd":str(REPO),"started_at":start,"finished_at":end,"exit_code":r.returncode,"environment_overrides":{"PYTHONDONTWRITEBYTECODE":"1"},"stdout_file":str((log/(a.name+".stdout.txt")).relative_to(ROOT)),"stderr_file":str((log/(a.name+".stderr.txt")).relative_to(ROOT)),"stdout_sha256":hashlib.sha256(r.stdout).hexdigest(),"stderr_sha256":hashlib.sha256(r.stderr).hexdigest()}
with (log/"command-history.jsonl").open("a") as f:f.write(json.dumps(record,ensure_ascii=False)+"\n")
print(json.dumps(record,ensure_ascii=False))
out=r.stdout.decode("utf-8",errors="replace")
print(out[:a.limit])
if len(out)>a.limit: print("[Console output limited; exact full stdout is retained in log]")
if r.stderr:print(r.stderr.decode("utf-8",errors="replace"),file=sys.stderr)
sys.exit(r.returncode)
