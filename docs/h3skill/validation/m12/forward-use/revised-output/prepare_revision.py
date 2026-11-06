from pathlib import Path
import json,hashlib
ROOT=Path('/workspace/scratch/67acb32e99b3/m12-forward-run')
OUT=ROOT/'revised-output'
FIRST=ROOT/'output'
def load(p): return json.loads(p.read_text())
def dump(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
# Pin the exact already accepted state and original request bundle used by this review.
initial=load(FIRST/'state/current-state.json')
assert initial['version']==1
originals=load(FIRST/'requests/accept-requests.json')
by_target={r['target']:r for r in originals}
dump(OUT/'state/base-state.json',initial)
dump(OUT/'requests/first-round-accepted-requests.json',originals)
protected=[ROOT/'task.md',*(ROOT/'sources').rglob('*'),*FIRST.rglob('*')]
dump(OUT/'preserved-files-before.json',[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted(protected) if p.is_file()])
rule=ROOT/'h3-audit-repair/references/evidence-and-gates.md'
(OUT/'evidence-and-gates.rule-snapshot.md').write_bytes(rule.read_bytes())
old_audit=by_target['M12.2']
new_audit=json.loads(json.dumps(old_audit))
new_audit['base_version']=initial['version']
new_audit['request_id']='m12-rule-revision-audit-v1'
new_result=next(x for x in new_audit['inputs']['results'] if x['check_id']=='CHK-COMPILE-SOUND')
assert new_result['result']=='unverified'
new_result['result']='fail'
new_result['reason']='The supplied compilation explicitly declares <Audio 1>: fully_copy while adding a new response and metal contact sound, and its soundscape places those added layers alongside copied music. Under the revised evidence-and-gates rule, that explicit text establishes a G2 sound-strategy conflict without listening to media. Actual mixing and synchronization remain unverified in G3/G4. Return retention scope and a suitable partially_copy plan to M6, then compilation to M11.'
cause={
 'id':'CAUSE-ISSUE-SOUND-STRATEGY',
 'kind':'causal_analysis',
 'origin':'synthetic',
 'source_ref':next(x for x in new_audit['inputs']['current_refs'] if x['id']=='compilation'),
 'check_ids':['CHK-COMPILE-SOUND'],
 'locator':'sources/compilation-v1.json#/fields/retention_analysis;#/fields/overall_soundscape; h3-audit-repair/references/evidence-and-gates.md#3',
 'content':'The already supplied synthetic compilation explicitly copies the selected music and adds dialogue/contact sound while marking Audio 1 fully_copy. The updated audit rule identifies this as a text-level sound-strategy conflict and routes retention scope and a suitable partially_copy plan to M6, followed by M11 compilation. This is semantic reassessment of the same source, not new media evidence or proof of actual mixing failure.'}
new_audit['inputs']['evidence'].append(cause)
old_repair=by_target['M12.4']
new_repair=json.loads(json.dumps(old_repair))
new_repair['base_version']=initial['version']
new_repair['request_id']='m12-rule-revision-repair-v1'
new_repair['inputs']['audit']=new_audit['inputs']
check=next(x for x in new_audit['inputs']['plan']['checks'] if x['id']=='CHK-COMPILE-SOUND')
new_issue={
 'id':'ISSUE-SOUND-STRATEGY','check_id':'CHK-COMPILE-SOUND','object_ref':cause['source_ref'],
 'location':'fields.retention_analysis; fields.overall_soundscape; fields.non_diegetic_music',
 'expected':check['expected'],
 'actual':'<Audio 1> is fully_copy, while the same compilation explicitly adds He Yuan\'s new response and a metal contact sound alongside the copied music.',
 'evidence_ids':['EV-SOUND'],
 'owner':'M6',
 'attribution_basis':'The revised audit rule specifically returns the sound retention scope and partially_copy strategy to M6, followed by M11 compilation. Compilation ownership remains M11; M6 is the sound-strategy repair owner, not an asserted cause of an unobserved media failure.',
 'causal_evidence_ids':['CAUSE-ISSUE-SOUND-STRATEGY'],
 'requested_action':'M6 confirms the exact selected music segment and retained scope, proposes a suitable partially_copy sound plan preserving the required original dialogue 我看见了。 and key contact, then M11 compiles that approved strategy. Recheck this text conflict in G2; actual mixing and synchronization require unchanged full-window G3/G4 media observations.'}
new_repair['inputs']['issues'].append(new_issue)
assert new_audit['inputs']['plan']==old_audit['inputs']['plan']
assert new_audit['inputs']['current_refs']==old_audit['inputs']['current_refs']
assert new_repair['inputs']['changes']==[] and new_repair['inputs']['retests']==[]
dump(OUT/'requests/audit-request.json',new_audit)
dump(OUT/'requests/repair-request.json',new_repair)
dump(OUT/'revision-manifest.json',{
 'context':'Same task and same input artifacts; review after one audit-rule revision.',
 'first_round_state':'output/state/current-state.json','base_state_version':1,
 'rule_path':str(rule.relative_to(ROOT)),'rule_sha256':sha(rule),
 'supersedes_semantic_conclusion_of':'m12-current-audit-v2:CHK-COMPILE-SOUND',
 'new_audit_request_id':new_audit['request_id'],
 'unchanged_scope_id':new_audit['inputs']['plan']['scope_id'],
 'unchanged_scope_version':new_audit['inputs']['plan']['scope_version'],
 'unchanged_requirement_ids':new_audit['inputs']['plan']['requirement_ids'],
 'unchanged_check_count':len(new_audit['inputs']['plan']['checks']),
 'changed_check':{'id':'CHK-COMPILE-SOUND','before':'unverified','after':'fail','evidence':'Existing EV-SOUND and the same compilation@1; revised rule interpretation only.'},
 'added_issue':new_issue,
 'unchanged':{'all_other_results':True,'scope_and_methods':True,'object_references':True,'dependency_graph':True,'G3_G4_media_absent':True},
 'no_new_media_evidence':True,'no_repair_executed':True,'original_output_preserved':True})
report='''# 同上下文规则修订后复核

## 修订结论

本次仍是原task.md、brief-current与plan@2下的同一审计，没有新增媒体、生成结果或修复版本。只依据更新后的evidence-and-gates.md第3节复核首轮结论。

原CHK-COMPILE-SOUND从 **unverified修订为fail**。首轮已经引用的compilation@1明确写出“Audio 1 fully_copy”，同时写出新增何远回应和金属接触声，并让它们伴随复制音乐。新增声部在文字中已明确，因此依更新规则足以确认G2声音策略冲突；缺少可试听媒体不能消除该文字失败。首轮把保留范围及新增层整体留作未决，现予以纠正。

这不是新增媒体证据。实际混音、接触声时机、对白同步及最终听感仍无观察支持，原G3/G4检查全部保持unverified。

## 当前审计结果

| 门 | 修订后结果 | 变化 |
|---|---|---|
| G0 | unverified | 无变化：实际来源与绑定缺失。 |
| G1 | unverified | 无变化：当前声音安排仍缺。 |
| G2 | fail | 新确认声音策略冲突；原编译依据、时间、手别、对白四项失败保留。 |
| G3 | unverified | 无实际生成片观察。 |
| G4 | unverified | 无实际装配成片观察。 |

原21项检查、四条需求、方法、目标、通道和0–10秒媒体覆盖范围全部保留。计数由5 pass / 4 fail / 12 unverified修订为 **5 pass / 5 fail / 11 unverified**。没有删去或减弱既有失败。

## 新增问题与复验安排

新增ISSUE-SOUND-STRATEGY，定位compilation@1的retention_analysis与overall_soundscape。M6先确认已选音乐片段、保留范围及合理的partially_copy方案，同时保留“我看见了。”和钥匙接触声；M11将经确认的声音方案重新编译。没有在本次审计中替M6/M11改专业字段或宣称已完成修复。

新编译须复验CHK-COMPILE-SOUND并复查原G2全范围，原四项编译问题仍需同时修复。生成后仍须提供对应版本0–10秒画面与声音观察，才能复验原G3；装配后按原G4范围检查实际混音、同步及成片。changes/retests保持空表，因为尚无已完成修复或新复验结果。

## 记录与接口

保持原output/不变，复制首轮已接受state（version=1）作为本次base；只对需要修订的M12.2与M12.4追加请求。M12.1的范围没有变化，无需新提案；没有实际媒体观察，M12.3仍不执行。

新原请求在requests/；逐次原始命令、stdout、stderr、退出码在commands/与results/；基于首轮状态的新accept结果及current state在state/。精确规则快照与摘要保存在evidence-and-gates.rule-snapshot.md和revision-manifest.json。最终执行结果见interface-summary.json。

依据定位：更新规则evidence-and-gates.md第3节；首轮EV-SOUND与sources/compilation-v1.json的retention_analysis、overall_soundscape；原scope及需求见本次请求中完整保留的plan。
'''
(OUT/'revision-report.zh.md').write_text(report,encoding='utf-8')
print(json.dumps({'base_version':initial['version'],'changed_check':'CHK-COMPILE-SOUND','scope_check_count':len(new_audit['inputs']['plan']['checks']),'repair_issue_count':len(new_repair['inputs']['issues'])},ensure_ascii=False))
