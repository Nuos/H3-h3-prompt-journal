from pathlib import Path
import json,hashlib,collections
ROOT=Path('/workspace/scratch/67acb32e99b3/m12-forward-run')
OUT=ROOT/'revised-output'
def load(p): return json.loads(p.read_text())
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
accepted=load(OUT/'results/02-batch-accept.stdout.json')
base=load(OUT/'state/base-state.json')
originals={r['target']:r for r in load(OUT/'requests/first-round-accepted-requests.json')}
audit_request=load(OUT/'requests/audit-request.json')
repair_request=load(OUT/'requests/repair-request.json')
new_audit=load(OUT/'results/01-audit-propose.stdout.json')['record']['content']
new_repair=load(OUT/'results/01-repair-propose.stdout.json')['record']['content']
old_results={x['check_id']:x for x in originals['M12.2']['inputs']['results']}
new_results={x['check_id']:x for x in audit_request['inputs']['results']}
changed=[k for k in old_results if old_results[k]!=new_results[k]]
assert changed==['CHK-COMPILE-SOUND']
assert audit_request['inputs']['plan']==originals['M12.2']['inputs']['plan']
assert audit_request['inputs']['current_refs']==originals['M12.2']['inputs']['current_refs']
assert repair_request['inputs']['dependencies']==originals['M12.4']['inputs']['dependencies']
assert repair_request['inputs']['issues'][:-1]==originals['M12.4']['inputs']['issues']
assert accepted['state']['records'][:len(base['records'])]==base['records']
protected=load(OUT/'preserved-files-before.json')
for item in protected:
    item['after_sha256']=hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()
    item['unchanged']=item['sha256']==item['after_sha256']
unchanged=all(x['unchanged'] for x in protected)
assert unchanged
integrity={'original_task_sources_and_output_unchanged':unchanged,'file_count':len(protected),'files':protected}
dump(OUT/'preserved-files-integrity.json',integrity)
summary={
 'task':'counter-key-transfer','context':'same-context review following the audit-rule update',
 'base_state_version':base['version'],'new_state_version':accepted['state']['version'],
 'acceptance_status':accepted['status'],'idempotent':accepted['idempotent'],
 'first_round_record_count':len(base['records']),'new_record_count':len(accepted['state']['records'])-len(base['records']),'total_record_count':len(accepted['state']['records']),
 'first_round_records_preserved_verbatim':True,
 'scope_unchanged':True,'scope_id':audit_request['inputs']['plan']['scope_id'],'scope_version':audit_request['inputs']['plan']['scope_version'],
 'requirements_unchanged':audit_request['inputs']['plan']['requirement_ids'],
 'check_count':len(new_results),'changed_result_ids':changed,
 'changed_result':{'check_id':'CHK-COMPILE-SOUND','previous':'unverified','current':'fail'},
 'check_results':dict(collections.Counter(x['result'] for x in new_results.values())),
 'gate_results':new_audit['gate_results'],'scope_result':new_audit['scope_result'],
 'repair_issue_count':len(repair_request['inputs']['issues']),
 'repair_executed':new_repair['repair_executed'],'all_issues_closed':new_repair['all_issues_closed'],
 'interfaces':[{'module':'M12.2','request':'requests/audit-request.json','route':'ready','propose':'M12Proposal','check':'valid'},{'module':'M12.4','request':'requests/repair-request.json','route':'ready','propose':'M12Proposal','check':'valid'}],
 'unchanged_interfaces':[{'module':'M12.1','reason':'Same full scope; original accepted AuditPlan retained.'},{'module':'M12.3','reason':'No actual observation; still not run.'}],
 'command_count':len(list((OUT/'commands').glob('*.json'))),'all_new_commands_exit_zero':all(load(p)['exit_code']==0 for p in (OUT/'commands').glob('*.json')),
 'acceptance_result':'results/02-batch-accept.stdout.json','current_state':'state/current-state.json','current_view':'state/current-view.json',
 'original_output_sources_task_unchanged':unchanged,
 'semantic_revision_boundary':'The newest version-2 audit corrects the same check under the revised rule. The original version-1 unverified declaration remains in immutable history; no actual object change, repair, generation or new media observation is asserted.',
 'verification_boundary':accepted['verification_boundary']}
dump(OUT/'interface-summary.json',summary)
p=OUT/'revision-report.zh.md'
s=p.read_text()
s += '''\n## 实际执行与接受结果\n\nM12.2与M12.4均已实际执行route→propose→check，分别返回ready、M12Proposal、valid；七次新CLI调用（含一次原子accept）均退出0。accept返回accepted、idempotent=false，状态由首轮version=1追加至 **version=2**。当前共有5条记录：原3条逐字保留，新增2条version=2记录。\n\n新账本明确记录CHK-COMPILE-SOUND=fail；首轮同项unverified仍保留在version=1历史中，不回写旧记录。本次没有对象版本变化或修复执行，未声称程序因规则修订自动将旧结论标记stale。当前解释以新增version=2审计修订为准。accepted只说明合同接收成功，整体范围仍为fail；5项问题均未关闭。\n\n已核对原task.md、sources/和output/全部现有文件的前后摘要，均未改变。精确校验记录见preserved-files-integrity.json。\n'''
p.write_text(s)
(OUT/'README.zh.md').write_text('''# 规则修订后复核交付\n\n先读revision-report.zh.md。此次延续首轮状态，没有重建独立试验或覆盖旧输出。\n\n| 文件/目录 | 内容 |\n|---|---|\n| revision-report.zh.md | 修订原因、当前结论、责任与复验安排、实际接受结果 |\n| revision-manifest.json | 精确规则摘要、唯一变化项和保持不变的范围 |\n| evidence-and-gates.rule-snapshot.md | 本次已读更新规则的固定副本 |\n| interface-summary.json | 公开接口执行摘要与状态边界 |\n| requests/first-round-accepted-requests.json | 首轮已接受原请求副本 |\n| requests/audit-request.json | 本次M12.2原请求 |\n| requests/repair-request.json | 本次M12.4原请求 |\n| requests/accept-requests.json / accept-proposals.json | 本次实际接受的请求/提案配对 |\n| results/ | 每次原始提案、检查和接受输出，含stderr |\n| commands/ | 准确argv、时间、退出码、完整stdout/stderr |\n| state/base-state.json | 首轮version=1状态副本 |\n| state/current-state.json | 追加后的version=2状态 |\n| state/current-view.json | 程序返回的当前视图 |\n| preserved-files-integrity.json | 原task.md、sources/、output/未变核对 |\n\n唯一审计结果变化：CHK-COMPILE-SOUND由unverified改为fail。新增声音策略问题回传M6确认保留范围与partially_copy，再由M11编译；实际混音与同步继续等待媒体观察。\n''',encoding='utf-8')
print(json.dumps({'acceptance':summary['acceptance_status'],'state_version':summary['new_state_version'],'records':summary['total_record_count'],'check_results':summary['check_results'],'gates':summary['gate_results'],'only_changed_check':changed,'protected_files_unchanged':unchanged,'protected_file_count':len(protected)},ensure_ascii=False))
