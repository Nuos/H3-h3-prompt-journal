from pathlib import Path
import json,hashlib,collections
ROOT=Path('/workspace/scratch/67acb32e99b3/m12-forward-run')
OUT=ROOT/'output'
def load(p): return json.loads(p.read_text())
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def normalize(x):
    if isinstance(x,dict): return {k:(v.removeprefix('sha256:') if k=='digest' and isinstance(v,str) else normalize(v)) for k,v in x.items()}
    if isinstance(x,list): return [normalize(v) for v in x]
    return x
# Narrative sidecars use the same digest encoding as the accepted public requests.
for name in ['audit-checks.json','repair-retest-plan.json','target-declarations.json']:
    p=OUT/name; dump(p,normalize(load(p)))
accepted=load(OUT/'results/05-batch-accept.stdout.json')
audit=load(OUT/'results/02-audit-propose.stdout.json')['record']['content']
repair=load(OUT/'results/03-repair-propose.stdout.json')['record']['content']
checks=load(OUT/'requests/audit-request-v2.json')['inputs']['results']
command_records=[load(p) for p in sorted((OUT/'commands').glob('*.json'))]
summary={
 'task':'counter-key-transfer','artifact_kind':'synthetic_engineering_audit',
 'current_task_basis':'brief-current.json + plan@2',
 'scope_id':'SCOPE-CURRENT-PRODUCTION','requirement_ids':['R-DURATION','R-ACTION','R-DIALOGUE','R-SOUND'],
 'check_count':len(checks),'check_results':dict(collections.Counter(r['result'] for r in checks)),
 'gate_results':audit['gate_results'],'scope_result':audit['scope_result'],
 'interfaces':[
  {'module':'M12.1','request':'requests/scope-request-v2.json','route':'ready','propose':'M12Proposal','check':'valid'},
  {'module':'M12.2','request':'requests/audit-request-v2.json','route':'ready','propose':'M12Proposal','check':'valid'},
  {'module':'M12.3','status':'not_run','reason':'No actual media or observation is supplied. No synthetic observation is promoted to actual evidence.'},
  {'module':'M12.4','request':'requests/repair-request-v3.json','route':'ready','propose':'M12Proposal','check':'valid'}],
 'acceptance':{'status':accepted['status'],'idempotent':accepted['idempotent'],'state_version':accepted['state']['version'],'record_count':len(accepted['state']['records']),'request_bundle':'requests/accept-requests.json','proposal_bundle':'requests/accept-proposals.json','raw_result':'results/05-batch-accept.stdout.json','current_state':'state/current-state.json','current_view':'state/current-view.json'},
 'repair_state':{k:repair.get(k) for k in ['repair_executed','all_issues_closed','impact_status','planned_affected_ids','affected_ids','invalidated_refs','unknown_dependency_ids']},
 'public_command_invocations':len(command_records),
 'failed_invocations_preserved':[{'command':r['command'],'exit_code':r['exit_code'],'errors':json.loads(r['stdout']).get('errors',[])} for r in command_records if r['exit_code']!=0],
 'format_corrections':['Initial request digests used a sha256: prefix; the public contract requires the lowercase 64-character hex only. Original v1 requests and all error outputs are retained.','Initial dependency edges used full references; the public template uses object ID strings. Repair v2 error and corrected v3 request are both retained.'],
 'state_interpretation':'Started from an empty ledger. No historical pass ledger or completed repair was invented. Current validity is the supplied-declaration version status; the obsolete consumed plan is an explicit failing check. The reported plan@1 to plan@2 input change is retained in repair-retest-plan.json, not declared as a newly completed repair.',
 'verification_boundary':accepted['verification_boundary']}
dump(OUT/'interface-summary.json',summary)
manifest=load(OUT/'source-manifest.json')
integrity=[]
for item in manifest:
    actual='sha256:'+hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()
    integrity.append({'path':item['path'],'expected':item['digest'],'actual':actual,'unchanged':item['digest']==actual})
dump(OUT/'source-integrity.json',{'all_sources_unchanged':all(i['unchanged'] for i in integrity),'files':integrity})
p=OUT/'audit-report.zh.md'
s=p.read_text()
s += '''\n## 实际执行结果\n\nM12.1、M12.2、M12.4均已实际执行route→propose→check；最终route为ready、check为valid。三份提案已通过一次原子accept，返回accepted，状态从0升至1，保留3条记录。账本计算结果为G0/G1/G3/G4 unverified、G2 fail，总范围fail；21项检查为5 pass、4 fail、12 unverified。修复未执行，四项问题未关闭。\n\n首次调用的摘要带有sha256:前缀，另一次修复请求把依赖边写成完整引用，均被合同拒绝；已分别改为64位小写十六进制摘要与对象ID字符串。原错误请求、退出码2和原输出全部保留；最终接受使用scope/audit的v2请求和repair的v3请求。这些修改只纠正接口表示，没有删除检查、修改源资料或减弱失败结论。\n\n本次从空账本登记当前审计，没有把历史“全通过”说明伪装为已接受的历史审计，也没有登记不存在的新修复版本。程序current_validity=current表示本次声明引用的版本一致，不表示编译读取的旧计划已经更新；该过期读取仍明确为fail。已知plan更新与其下游影响另存于repair-retest-plan.json，未声称本次程序执行了旧账本失效传播。\n\n七份sources文件已按执行前后摘要核对，内容均未改变。\n'''
p.write_text(s)
(OUT/'README.zh.md').write_text('''# 交付索引\n\n先读 **audit-report.zh.md**。本次是合成制作资料的文字审计，没有真实媒体观察或生成。\n\n| 文件 | 用途 |\n|---|---|\n| audit-report.zh.md | 简洁中文结论、四项问题、修复与复验顺序、实际接受结果 |\n| audit-checks.json | 21项检查、四条要求、G0–G4范围与逐项证据定位 |\n| repair-retest-plan.json | 责任分配、已有计划变更、依赖边界及完整复验安排 |\n| interface-summary.json | 实际CLI调用与接受摘要、失败尝试和程序验证边界 |\n| requests/accept-requests.json | 最终接受的三份原请求数组 |\n| requests/accept-proposals.json | 与原请求逐一配对的提案数组 |\n| state/current-state.json | accept原样返回的当前状态，version=1 |\n| state/current-view.json | 当前状态视图 |\n| commands/ | 每次调用的准确argv、工作目录、时间、退出码、stdout、stderr |\n| results/ | 每次调用未经修改的stdout与stderr |\n| target-declarations.json | 缺失媒体/资产的显式声明及摘要边界 |\n| source-manifest.json / source-integrity.json | 输入摘要及执行前后未改动核对 |\n\n所有请求尝试均保留。原始输入未改。程序accepted表示声明与记录合同接收成功；总审计仍为fail，并不代表生产可交付。\n''',encoding='utf-8')
print(json.dumps({'acceptance':summary['acceptance'],'check_results':summary['check_results'],'gate_results':summary['gate_results'],'repair_state':summary['repair_state'],'source_integrity':all(i['unchanged'] for i in integrity)},ensure_ascii=False))
