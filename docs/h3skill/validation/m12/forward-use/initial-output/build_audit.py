from pathlib import Path
import json, hashlib

ROOT=Path('/workspace/scratch/67acb32e99b3/m12-forward-run')
OUT=ROOT/'output'
def dump(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(b): return 'sha256:'+hashlib.sha256(b).hexdigest()
def canonical(obj): return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
source={p.name:json.loads(p.read_text()) for p in sorted((ROOT/'sources').glob('*.json'))}
manifest=[{'path':'sources/'+p.name,'digest':digest(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted((ROOT/'sources').glob('*.json'))]
dump(OUT/'source-manifest.json',manifest)
def file_ref(id,version,owner,kind,file): return {'id':id,'version':str(version),'digest':digest((ROOT/'sources'/file).read_bytes()),'owner':owner,'kind':kind}
brief=file_ref('brief','current','external','brief','brief-current.json')
p1=file_ref('plan','1','M7','execution_plan','plan-v1.json')
p2=file_ref('plan','2','M7','execution_plan','plan-v2.json')
comp=file_ref('compilation','1','M11','compiled_prompt','compilation-v1.json')
inv=file_ref('media-inventory','current','external','media_inventory','media-inventory.json')
prior=file_ref('legacy-review','1','external','external_report','prior-review.json')
dep=file_ref('dependencies','current','external','dependency_manifest','object-dependencies.json')
declarations=[
 {'id':'assembly','version':'1','owner':'M9','kind':'assembled_media','availability':'not_provided','basis':['sources/object-dependencies.json','sources/media-inventory.json'],'meaning':'Only the declared assembly identity; no media bytes were provided.'},
 {'id':'identity-sheet','version':'1','owner':'M2','kind':'identity_sheet','availability':'not_provided','basis':['sources/object-dependencies.json','sources/media-inventory.json'],'meaning':'Only the declared identity-sheet identity; no asset bytes were provided.'},
 {'id':'required-generated-media','version':'not-provided','owner':'external','kind':'generated_media','availability':'not_provided','basis':['sources/media-inventory.json'],'meaning':'Explicit missing target required for audit scope; not a generated artifact or observation.'}
]
refs=[]
for d in declarations:
    refs.append({k:d[k] for k in ['id','version','owner','kind']}|{'digest':digest(canonical(d))})
dump(OUT/'target-declarations.json',{'digest_basis':'sha256 of canonical declaration JSON only; these digests are not hashes of media or asset bytes. No actual media or identity asset is asserted.','declarations':declarations,'references':refs})
assembly,identity,generated=refs
current=[brief,p2,comp,inv,prior,dep,assembly,identity,generated]
checks=[]
results=[]
evidence=[]
def add(id,req,gate,expected,method,targets,status,reason,evs=None,channels=None,window=None):
    checks.append({'id':id,'requirement_id':req,'gate':gate,'expected':expected,'method':method,'targets':targets,'channels':channels or [],'time_window_ms':window,'coverage':'full_window' if window else 'document'})
    results.append({'check_id':id,'result':status,'evidence_ids':evs or [],'reason':reason})
def ev(id,ref,ids,loc,content,kind='document'):
    evidence.append({'id':id,'kind':kind,'origin':'synthetic','source_ref':ref,'check_ids':ids,'locator':loc,'content':content})
add('CHK-BASIS','R-DURATION','G0','Use brief-current and plan@2 as the current task basis.','compare_supplied_current_basis',[brief,p2],'pass','The task identifies plan-v2 as current; its change record retains action and words.',['EV-BASIS'])
ev('EV-BASIS',p2,['CHK-BASIS'],'sources/plan-v2.json#/change_record','Synthetic source: plan@2 reports the change from 8 to 10 seconds and the second shot start from 5 to 6 seconds; the task explicitly selects plan-v2.')
add('CHK-SOURCES','R-SOUND','G0','Current source media and their binding are available for the requested images and selected music.','inspect_supplied_inventory',[inv,comp],'unverified','No actual image, audio or video files are provided; Picture 1/2 and Audio 1 binding cannot be verified.',['EV-INVENTORY'])
ev('EV-INVENTORY',inv,['CHK-SOURCES'],'sources/media-inventory.json','The synthetic inventory explicitly provides zero files, no generation/run record, no assembly and no actual image/video/audio.')
add('CHK-PLAN-DURATION','R-DURATION','G1','Plan retains two shots totaling 10 seconds, with shot 2 starting at 6 seconds.','compare_current_brief_and_plan',[brief,p2],'pass','Plan@2 has [0,6] and [6,10], two contiguous shots totaling 10 seconds.',['EV-PLAN-DURATION'])
ev('EV-PLAN-DURATION',p2,['CHK-PLAN-DURATION'],'sources/plan-v2.json#/shots','duration_seconds=10; s1=[0,6], s2=[6,10].')
add('CHK-PLAN-ACTION','R-ACTION','G1','Lin Che uses the left hand to place the brass key on the counter right, and it stays after release.','compare_current_brief_and_plan',[brief,p2],'pass','The current plan explicitly preserves left hand, counter right and key resting after the hand leaves.',['EV-PLAN-ACTION'])
ev('EV-PLAN-ACTION',p2,['CHK-PLAN-ACTION'],'sources/plan-v2.json#/action',source['plan-v2.json']['action'])
add('CHK-PLAN-DIALOGUE','R-DIALOGUE','G1','He Yuan sees the key before saying exactly 我看见了。','compare_current_brief_and_plan',[brief,p2],'pass','Plan action orders seeing before response; its dialogue field retains the exact required words.',['EV-PLAN-DIALOGUE'])
ev('EV-PLAN-DIALOGUE',p2,['CHK-PLAN-DIALOGUE'],'sources/plan-v2.json#/dialogue','action: 何远看见钥匙后回应。 dialogue: 我看见了。')
add('CHK-PLAN-SOUND','R-SOUND','G1','A current sound plan specifies the selected music segment while retaining dialogue and key contact.','inspect_current_sound_plan',[brief,p2],'unverified','The brief defines the sound requirement, but plan@2 contains no source segment or mixing arrangement; no current M6 sound plan is supplied.')
add('CHK-COMPILE-BASIS','R-DURATION','G2','The compilation consumes current plan@2.','compare_declared_consumed_version',[p2,comp],'fail','compilation@1 explicitly consumes plan@1 and therefore is not a compilation of the current plan.',['EV-COMPILE-BASIS'])
ev('EV-COMPILE-BASIS',comp,['CHK-COMPILE-BASIS'],'sources/compilation-v1.json#/consumes','consumes=[{object_id:plan,version:1}], while the task current plan is plan@2.')
add('CHK-COMPILE-DURATION','R-DURATION','G2','Compiled duration is 10 seconds, with two shots and shot 2 beginning at 00:06.000.','compare_plan_with_parameters_and_shot_timing',[p2,comp],'fail','The compilation declares duration_seconds=8 and starts shot 2 at 00:05.000.',['EV-COMPILE-DURATION'])
ev('EV-COMPILE-DURATION',comp,['CHK-COMPILE-DURATION'],'sources/compilation-v1.json#/parameters;#/fields/detailed_description','duration_seconds=8; At 00:05.000, [Shot 2]. Current plan requires 10 seconds and shot 2 start at 6 seconds.')
add('CHK-COMPILE-ACTION','R-ACTION','G2','The compiled action retains the left hand, counter right, and resting key.','compare_approved_action_with_compiled_action',[p2,comp],'fail','The compiled action uses right hand, contradicting both plan@1 and plan@2; right-side placement and resting key are retained.',['EV-COMPILE-ACTION'])
ev('EV-COMPILE-ACTION',comp,['CHK-COMPILE-ACTION'],'sources/compilation-v1.json#/fields/detailed_description','Lin Che uses his right hand to place the brass key at the right side of the counter. The key remains on the counter as the hand withdraws.')
add('CHK-COMPILE-DIALOGUE','R-DIALOGUE','G2','The compiled dialogue retains exactly 我看见了。 after He Yuan sees the key.','compare_approved_dialogue_with_compiled_dialogue',[p2,comp],'fail','The compilation changes the required words to 我知道了。; the look-before-speech sequence is textually present.',['EV-COMPILE-DIALOGUE'])
ev('EV-COMPILE-DIALOGUE',comp,['CHK-COMPILE-DIALOGUE'],'sources/compilation-v1.json#/fields/detailed_description','He Yuan looks at the key and says (S1) in Chinese, <d>我知道了。</d>.')
add('CHK-COMPILE-FIELDS','R-ACTION','G2','The Ref2VA compilation contains its six named text fields.','inspect_six_field_presence_only',[comp],'pass','All six expected fields are present. This verifies field presence only, not full H3 validity or media quality.',['EV-FIELDS'])
ev('EV-FIELDS',comp,['CHK-COMPILE-FIELDS'],'sources/compilation-v1.json#/fields','Present: subject_definitions, summary, retention_analysis, detailed_description, overall_soundscape, non_diegetic_music.')
add('CHK-COMPILE-SOUND','R-SOUND','G2','The source-music retention strategy is compatible with the exact new dialogue and key contact sound.','inspect_sound_retention_declaration',[brief,comp],'unverified','The text combines Audio 1 fully_copy with added speech/contact sound; source content, exact retention scope and an explicit compatible sound plan are missing. This audit does not certify that combination.',['EV-SOUND'])
ev('EV-SOUND',comp,['CHK-COMPILE-SOUND'],'sources/compilation-v1.json#/fields/retention_analysis','<Audio 1>: fully_copy; add the new response and a metal contact sound. Overall soundscape adds dialogue/contact while copying music; no source audio exists in supplied files.')
add('CHK-RUNTIME','R-DURATION','G2','A current run configuration and generation record agree with the approved plan and compiled prompt.','compare_current_run_declarations',[comp,inv],'unverified','No generation submission or execution record is supplied; declared text parameters do not establish actual runtime use.')
for gate,target,prefix in [('G3',generated,'GENERATED'),('G4',assembly,'ASSEMBLY')]:
    for key,req,expected,channels in [
      ('DURATION','R-DURATION','Actual media lasts 10 seconds with two shots and the second shot at 6 seconds.',['video']),
      ('ACTION','R-ACTION','The visible left-hand key placement, release and resting state meet the brief.',['video']),
      ('DIALOGUE','R-DIALOGUE','He Yuan sees the key and audibly says exactly 我看见了。 in correct order.',['video','audio']),
      ('SOUND','R-SOUND','The selected source music segment, dialogue and key contact are audibly present and compatible.',['audio'])]:
        add('CHK-'+prefix+'-'+key,req,gate,expected,'observe_current_media_full_window',[target],'unverified','No actual current media or observations are supplied. The target reference is a missing-target declaration, not media evidence.',channels=channels,window=[0,10000])
scope={'scope_id':'SCOPE-CURRENT-PRODUCTION','scope_version':'1','plan_ref':p2,'scope_sources':[brief,p2,inv,prior,dep],'gates':['G0','G1','G2','G3','G4'],'requirement_ids':['R-DURATION','R-ACTION','R-DIALOGUE','R-SOUND'],'checks':checks}
audit={'plan':scope,'current_refs':current,'results':results,'evidence':evidence,'observations':[]}
issues=[]
for id,cid,loc,actual,action in [
 ('ISSUE-STALE-COMPILE','CHK-COMPILE-BASIS','consumes','编译声明读取 plan@1；当前依据为 plan@2。','M11 读取 plan@2 重编译，记录实际读取版本；保留编译1历史。'),
 ('ISSUE-TIMING','CHK-COMPILE-DURATION','parameters.duration_seconds; fields.detailed_description shot 2 marker','8秒及00:05.000；当前要求10秒及00:06.000。','M11 从 plan@2 编译10秒参数与第二镜6秒起点；不改变两镜结构。'),
 ('ISSUE-HAND','CHK-COMPILE-ACTION','fields.detailed_description','right hand；两版计划均要求左手。','M11 恢复 left hand，并保持柜台右侧、松手后钥匙留台面的既定动作。'),
 ('ISSUE-WORDS','CHK-COMPILE-DIALOGUE','fields.detailed_description dialogue','我知道了。；要求我看见了。','M11 恢复原词我看见了。及先看见后说话的顺序；由M6核对说话人和对白绑定。')]:
    check=next(c for c in checks if c['id']==cid)
    result=next(r for r in results if r['check_id']==cid)
    cause='CAUSE-'+id
    ev(cause,comp,[cid],'sources/compilation-v1.json; sources/plan-v1.json; sources/plan-v2.json','Semantic comparison of supplied synthetic documents: '+actual+' The compilation is owned by M11. The hand and words mismatch already existed against plan@1; the duration/shot-start mismatch follows the declared plan@2 update. This attributes a text compilation repair, not a cause of unobserved media failure.',kind='causal_analysis')
    issues.append({'id':id,'check_id':cid,'object_ref':comp,'location':loc,'expected':check['expected'],'actual':actual,'evidence_ids':result['evidence_ids'],'owner':'M11','attribution_basis':'源文件明确编译归M11；本次仅归责可直接比对的编译字段差异，不推断未观察媒体的失败根因。','causal_evidence_ids':[cause],'requested_action':action})
# audit and repair share the same current audit declaration, including transparent causal evidence.
repair={'audit':audit,'issues':issues,'changes':[],'dependencies':{'nodes':[p2,comp,assembly,identity],'edges':[{'upstream':p2,'downstream':comp},{'upstream':comp,'downstream':assembly}],'complete':False},'retests':[]}
def req(target,id,inputs): return {'kind':'M12Request','contract_version':'1.0.0','route_version':'1.0.0','work_id':'counter-key-transfer','base_version':0,'request_id':id,'target':target,'inputs':inputs}
for name,target,id,inputs in [('scope','M12.1','m12-current-scope-v1',scope),('audit','M12.2','m12-current-audit-v1',audit),('repair','M12.4','m12-current-repair-v1',repair)]: dump(OUT/'requests'/f'{name}-request-v1.json',req(target,id,inputs))
dump(OUT/'state'/'initial-state.json',{'kind':'M12State','contract_version':'1.0.0','work_id':'counter-key-transfer','version':0,'records':[],'receipts':[]})
dump(OUT/'audit-checks.json',{'scope':scope,'results':results,'evidence':evidence,'missing_observations':True})
dump(OUT/'repair-retest-plan.json',{'current_basis':'plan@2','actual_reported_input_change':{'before':p1,'after':p2,'basis':'sources/plan-v2.json#/change_record','status':'reported_applied','effect':'compilation@1 still consumes plan@1; assembly@1 transitively depends on compilation. No new compilation or assembly bytes were supplied.','ledger_treatment':'Preserved as supplied source history and a current mismatch finding. Not falsely entered as a completed repair.'},'confirmed_issues':issues,'open_gaps':[{'owner':'M6','item':'Provide selected music segment, retention/mixing arrangement, speaker binding and dialogue/key contact preservation.'},{'owner':'M2','item':'Provide actual Picture 1/2 and Audio 1 assets with binding/order and source identity.'},{'owner':'M11','item':'Provide current compiled artifact and actual submitted run configuration/record.'},{'owner':'external','item':'Provide current generated media plus actual video/audio observations over 0–10 seconds.'},{'owner':'M9','item':'Provide current assembly artifact, consumed versions and complete video/audio observations.'}], 'dependency_limit':'Known graph is plan -> compilation -> assembly. identity-sheet is disconnected only within this incomplete supplied graph; its validity is unverified, and no external dependency completeness is claimed.','retest_steps':[{'step':1,'owner':'M11','checks':['CHK-COMPILE-BASIS','CHK-COMPILE-DURATION','CHK-COMPILE-ACTION','CHK-COMPILE-DIALOGUE','CHK-COMPILE-FIELDS','CHK-COMPILE-SOUND','CHK-RUNTIME'],'requires':'New actual compilation version and its consumed plan@2; current assets/sound plan and run declaration. Rerun all original G2 checks, not only changed fields.'},{'step':2,'owner':'external','checks':[c['id'] for c in checks if c['gate']=='G3'],'requires':'New generated media/version and actual observed video/audio 0–10000ms with source/run binding. Use M12.3 only when observations exist.'},{'step':3,'owner':'M9','checks':[c['id'] for c in checks if c['gate']=='G4'],'requires':'New final assembly/version with dependencies and actual full-window video/audio observations.'},{'step':4,'owner':'M12','checks':[c['id'] for c in checks],'requires':'Same scope ID, all four requirement IDs, every current check and full media window retained. Advance object versions, rerun M12.2/M12.4. Close issues only with corresponding new evidence; retain immutable failure history.'}], 'implemented_repairs':[],'completed_retests':[]})
report='''# 当前制作资料审计

## 结论与可交付范围

当前依据是 brief-current.json 与 plan@2。可交付的是这组**合成文字材料的审计记录、四项明确编译问题及修复复验安排**。不能据此交付已验证的生成片或装配成片。全部输入均为合成工程材料；本报告没有真实生成、试听、观看或媒体质量判断。

| 门 | 当前结果 | 依据与边界 |
|---|---|---|
| G0 依据与证据 | unverified | 当前brief与plan@2明确；真实图片、音频、视频和绑定材料缺失。 |
| G1 设计 | unverified | 10秒两镜（0–6、6–10）、左手放钥匙、台面右侧、松手后留台面及原词均有当前计划支持；音乐片段与混音安排未提供。 |
| G2 编译与运行 | fail | 编译仍读取plan@1，时长8秒、第二镜5秒；右手与“我知道了。”分别违背左手与原词要求。六字段齐全只支持字段存在检查；资产、声音策略和实际运行记录未验证。 |
| G3 生成片 | unverified | 没有生成片或实际音视频观察。 |
| G4 成片 | unverified | 没有装配成片或实际音视频观察。 |

## 四项确认问题及最小修复

| 问题 | 当前内容 | 要求与修复责任 |
|---|---|---|
| 编译依据过期 | compilation@1 consumes plan@1 | M11按当前plan@2重编译并记录读取版本。 |
| 时间与切镜不符 | 8秒；第二镜00:05.000 | M11编译为10秒、第二镜00:06.000，保持两镜。 |
| 手别改写 | right hand | M11恢复left hand，保留柜台右侧与松手后钥匙留台面。 |
| 对白改写 | 我知道了。 | M11恢复“我看见了。”与先看见后回应；M6核对说话人绑定。 |

前两项与plan@2已声明的时间更新相关；后两项对plan@1也已经不符，不能把它们解释为此次延长片长造成。这里的责任判断只限可核对的编译文字，不推断不存在的媒体观察。

Audio 1的fully_copy与新增对白、金属接触声并列，但源音频与保留范围未提供。需M6明确选曲片段、保留策略和各声部安排，再由M11按合同编译；本次不据文字宣称声音已经正确。没有执行专业模块字段修改，没有提交生成。

## 历史记录、依赖与复验

prior-review.json保留“G0至G4均通过、动作衔接良好”的原历史说明；它针对plan@1/compilation@1，无原始观察或当前媒体定位，不能作为当前plan@2的通过证据。它仍是合成场景中的外部说明，不是本次验证结果。

已知依赖为plan→compilation→assembly。当前编译未更新，assembly@1的当前有效性也不能沿旧说明继承。identity-sheet在所给四对象图中没有连边，但图明确不完整；不能因此宣称它已验证或对外部变更不受影响。

1. M2补实际图片/音频及绑定；M6补声音安排；M11交付读取plan@2的新编译版本与运行资料。完整复查原G2检查，保留时长、两镜、动作、原词和声音要求。
2. 提供当前生成片及0–10秒真实画面/声音观察后，才调用M12.3并复查全部G3检查；不能用文字脚本代替动作、对白或声音观察。
3. M9基于新版本装配并交付成片与依赖记录；完整复查G4的0–10秒画面和声音。
4. 保持本次scope、四条原要求及全部检查项，追加新版本复验记录；只有匹配的新证据才关闭对应问题。保留本次失败和历史记录。

## 接口、证据与状态文件

原请求保存在requests/；逐次命令、标准输出、标准错误和退出码保存在commands/；原始结果保存在results/；接受前后状态保存在state/。最终接口执行结果见interface-summary.json。

M12.1用于审计范围，M12.2用于当前审计账本，M12.4用于问题和复验安排；没有可用实际媒体观察，M12.3不执行。接受仅表示公开合同接收了声明，不证明真实来源、实际生成质量或修复已经完成。

媒体目标引用的摘要对应target-declarations.json中明确标为未提供的声明，不是媒体字节摘要，也不声称目标文件实际存在。没有已实施修复，changes与retests保持空表；已提供的plan@1→plan@2变更在repair-retest-plan.json中按来源原样说明，没有冒充本次完成的修复。

引用：sources/brief-current.json、plan-v1.json、plan-v2.json、compilation-v1.json、media-inventory.json、prior-review.json、object-dependencies.json；逐项定位与摘要见audit-checks.json及source-manifest.json。
'''
(OUT/'audit-report.zh.md').write_text(report,encoding='utf-8')
print(json.dumps({'written':'output/','checks':len(checks),'results':len(results),'issues':len(issues),'evidence_items':len(evidence)},ensure_ascii=False))
