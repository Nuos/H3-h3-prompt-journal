"""Construct the minimal SEG10 trial artifacts; does not accept proposals."""
from pathlib import Path
import hashlib, json, subprocess

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
SKILL = REPO / 'docs/h3skill/h3-work-intent'
CASE = REPO / 'case-studies/2026-10-four-subject-formation-choreography'
VERSION = '0ce8b7b1890052bf1d4dd233ef20e68817b38f28'
WORK = 'WORK-TRIAL-FOUR'
def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def src(kind, locator, excerpt, version=VERSION):
    return dict(kind=kind, locator=locator, version=version, excerpt=excerpt)
def issue(id, code, status, message, owner, field, blocking, refs):
    return dict(id=id, code=code, status=status, message=message, owner_module=owner, field=field, blocking=blocking, source_refs=refs)
readme = (CASE/'README.md').read_text()
prompt = (CASE/'prompt.md').read_text()
readme_lines = readme.splitlines()
ban = '\n'.join('\n'.join(readme_lines[max(0,i-1):i+1]) for i,line in enumerate(readme_lines) if 'center-line' in line.lower())
cross = '\n'.join(line for line in prompt.splitlines() if 'k184' in line or 'k186' in line or 'k192' in line or 'front/back swap' in line.lower() or line.startswith('Story of the segment:'))
assert ban and cross, 'Exact conflict evidence must be retained'
sources = {
 'SRC_TASK': src('user_requirement', 'conversation:mv-trial-task', '整理四人队形 MV 为 M1 作品意图、必保事项、段落功能/观众信息、情绪能量和母题；仅有 README 与 prompt 文本。交付真实请求、子提案、父接受结果及 WorkBrief。', 'task-2026-11-05'),
 'SRC_README': src('case_text', str(CASE/'README.md'), '作者报告整片 181.56 秒、14 段，固定四人和木墙外廊，通过相同锚定块、动作状态交接和跳舞式换阵维持连续性；本次未检查媒体。'),
 'SRC_PROMPT': src('case_text', str(CASE/'prompt.md'), 'SEG10：同一四人、固定外观和场景；保护弧与会合、前后换层、转身接力、重组、四条不同方向的星芒线，Saten 前臂擦镜接续 SEG11；沿用原音轨。'),
 'SRC_BAN': src('case_text', str(CASE/'README.md')+'#centerline', ban),
 'SRC_CROSS': src('case_text', str(CASE/'prompt.md')+'#SEG10-formation-and-beats', cross),
 'SRC_DESIGN': src('design_decision', 'mv-trial:semantic-proposal', '仅把已提供完整文本的 SEG10 整理为四个语义段。四段不是镜头数、生成任务数或整片 14 段的替代。情绪与母题是可追溯的文本解读，不声称已通过音画验证。', 'trial-design-1')
}
scope = dict(kind='work', paragraph_ids=[])
def c(text, refs=('SRC_PROMPT',), priority='must'):
    return dict(text=text, priority=priority, scope=scope, source_refs=list(refs))
def event(text): return dict(description=text, source_refs=['SRC_PROMPT'])
conflict = issue('ISS_CENTERLINE','source_constraint_conflict','conflict','README 要求各自象限且不越中心线；SEG10 要求交叉行进、中心会合与前后换层。现有文本未定义可兼容的中心线/路径，不能同时确认全部要求成立，也未获授权删改任一条。须由需求所有者明确优先级或提供可同时满足的路径定义。','user','/content/constraints/C_CENTERLINE',True,['SRC_BAN','SRC_CROSS'])
missing = issue('ISS_MEDIA','media_not_supplied','unverified','Picture 1、Audio 1、生成视频与相邻段素材均未提供；四人识别、锚图外观、节拍同步、音轨保真及交接连续性不可验证。','M2','/content/intent',False,['SRC_TASK','SRC_PROMPT'])
timing = issue('ISS_TIMING','timing_manifest_missing','unverified','13.767 秒、93.75 BPM、绝对音轨区间和 beat cells 均为源文本声明；cuts_manifest.json 与音频缺失，未测量或核实。','M7','/content/emotion_energy',False,['SRC_PROMPT'])
camera = issue('ISS_CAMERA','camera_instruction_ambiguity','unverified','源文同时出现 operator backpedal front-side parallax 和禁止通过退镜揭示队形；需 M5 判定局部跟随与退镜限制的边界。此项不替代已明确保留的中心线来源冲突。','M5','/content/constraints/C_CAMERA',False,['SRC_PROMPT'])
changes11 = {
 'intent': dict(work_type='mv', creative_goal='在固定木墙外廊中，以 Mikoto、Kuroko、Uiharu、Saten 四人的稳定身份、个性化舞姿与连续换阵呈现保护、信任和重新聚合；本次 M1 细化范围为 SEG10，整片 14 段仅作上下文。', audience_takeaway='观众始终辨认同一四人，读出彼此保护和熟悉感；队形从交叉会合经换层接力、扩张重组，到四个不同方向的开放姿态，动作持续流向下一段。', delivery_use='供后续专业模块审查的 SEG10 M1 候选方案；来源冲突未解决，不能作为已接受的生产依据。', target_duration={'seconds':13.767,'domain':'generation_request','basis':'requested','source_refs':['SRC_PROMPT']}, source_refs=['SRC_TASK','SRC_README','SRC_PROMPT','SRC_DESIGN']),
 'constraints': {
  'C_IDENTITY':c('保持且仅保持四人：S1 Mikoto、S2 Kuroko、S3 Uiharu、S4 Saten；各自脸型、发型、发饰、服装和身体比例绑定 Picture 1，不换人、串脸、重设计或增加第五人。实际图像尚未提供。'),
  'C_ANCHOR':c('Picture 1 同时锁定四人与木条墙、灰石砖地、柔和自然光及右侧米色门框的外廊；保留源文逐字复用锚定块的意图，空手且无新增道具。'),
  'C_AUDIO':c('仅沿用原 Audio 1，保持波形、原速原调和原有拍点；不新增对白、环境声、音效或音乐，禁止对口型。歌词只作情绪和乐句线索，不字面生成星图、电光、粒子或道具。'),
  'C_CONTINUITY':c('从 SEG09 的在行动作接入：保留脚部压力、重心、躯干扭转、手部回收及行进方向；换阵由舞步完成，不步行填充、瞬移、滑脚或恢复锚图站姿；SEG10 末动作未完即接续 SEG11。'),
  'C_INDIVIDUAL':c('保留 S1 紧凑果断、S2 活泼前倾、S3 精确细腻、S4 轻快调皮的动作差异；非指定重音使用接力、镜像、半拍及幅度差，其余成员在近景中继续舞动。'),
  'C_CENTERLINE':c('README 声明四人保持各自象限、不越中心线；与 C_CROSS 同时保留，当前存在阻塞性来源冲突。',['SRC_BAN']),
  'C_CROSS':c('SEG10 明确要求双人弧线与交叉、中心近肩会合和 S1/S2 前后换层；不得在未裁决前删去这些主体动作来假装满足中心线限制。',['SRC_CROSS','SRC_PROMPT']),
  'C_CAMERA':c('镜头切换须提供成员、队形或动作峰值的新信息；维持真实速度和有支撑的身体运动，不穿体、随意环绕或靠退镜/变焦揭示队形。局部 backpedal 措辞需 M5 审查。')
 },
 'must_keep_events': {
  'E_PROTECT':event('保持进入时的在行动量；双人保护弧和反向半拍呼应，近肩不接触的中心会合，脚持续驱动。'),
  'E_TRUST':event('S1/S2 前后换层，S3 主导转身、S1 同向响应，S2/S4 错拍接力，形成熟悉同伴仍在身旁的观众信息。'),
  'E_REGROUP':event('对角扩张与持续回流重组，四人通过不同手臂高度与个性动作保持可辨识性，不能收成静态展示排。'),
  'E_HANDOFF':event('S1/S4 前进、S2/S3 后退一次并向外传波；落成四个不同方向的星芒线后，S4 前臂擦镜，后三人沿不同方向继续，连接 SEG11。')
 }
}
def para(order, function, before, after, eventid, predecessors, focus):
    return dict(order=order,function=function,audience_information_before=before,audience_information_after=after,must_keep_event_ids=[eventid],information_predecessors=predecessors,performance_focus=focus,source_refs=['SRC_PROMPT','SRC_DESIGN'])
changes12 = {'paragraphs': {
 'P1':para(1,'保护弧 / 会合：承接在行动量，建立四人互相照应的关系。',['SEG09 的动作仍在继续；此点仅由源文声明，未观看相邻段。'],['同一四人各有明确身份；保护弧和近肩会合表达相互照应。'],'E_PROTECT',[],'从脚和重心发起保护弧，保留半拍差与不接触的近肩关系；中心线路径冲突尚未裁决。'),
 'P2':para(2,'换层与信任接力：空间位置变化仍保留熟悉关系。',['四人已经通过保护弧和会合建立照应关系。'],['前后层级可交换；转身后同伴仍在旁边，关系通过回应和错拍延续。'],'E_TRUST',['P1'],'S3 的转身头部最后到位；S1 响应，S2/S4 错拍接力；保留各人的动作签名。'),
 'P3':para(3,'扩张重组：让群体打开并持续重新关联。',['观众已读出换层后的信任接力。'],['空间扩大但四人仍是一个有联系的群体；个体差异能在重组中辨认。'],'E_REGROUP',['P2'],'以对角流动、不同手臂高度和回收再启动形成呼吸；不能变成站定排队。'),
 'P4':para(4,'未完动作接续：以向外传波和四向展开收束本段信息，保留下一段的动势。',['群体已扩张并重组，四人的个性仍清晰。'],['四人共同展开但保留不同方向；前臂擦镜只遮挡视线，身体运动并未结束。'],'E_HANDOFF',['P3'],'前后一次对向步与向外传波，四条不同身体线接 S4 前臂擦镜；后三人继续运动。')
}}
def energy(start,end,intent): return dict(emotion_start=start,emotion_end=end,energy_intent=intent,source_refs=['SRC_PROMPT','SRC_DESIGN'])
def motif(desc,ids,development): return dict(description=desc,paragraph_ids=ids,development=development,source_refs=['SRC_PROMPT','SRC_DESIGN'])
changes13 = {
 'emotion_energy': {
  'P1':energy('在行动作中的警觉与轻快','彼此保护的靠近感','由错拍弧线聚向会合；保持弹性膝与脚底压力，聚拢时有紧张度而不冻结。'),
  'P2':energy('靠近后的信任','转身仍获回应的熟悉感','重心换层与半拍回应形成有张有弛的接力；动作幅度依人物而异，不要求持续加大。'),
  'P3':energy('信任带来的松展','重组中的活泼和期待','空间扩张、回收再发；用高度与方向差使群体呼吸，保持持续流动。'),
  'P4':energy('重新聚合后的开放感','明亮而未完的前行动势','向外传波后给出明确四向重音，再把能量交给擦镜与下一段；不以合照或长停姿封口。')
 },
 'motifs': {
  'M_PROTECT':motif('双人保护弧与近肩不接触会合',['P1','P2'],'从互相保护的弧线发展为换层后仍能互相回应的关系；受中心线来源冲突约束，尚不可执行锁定。'),
  'M_ECHO':motif('转身及半拍回应',['P1','P2','P3'],'反向半拍弧线引出转身接力，再扩展为群体方向和高度差，保持同伴关系的可读性。'),
  'M_FOUR':motif('四人可区分的身体方向和动作签名',['P1','P2','P3','P4'],'始终可识别的个体差异在末段汇成四条不同方向的身体线；星芒是队形隐喻，不新增特效。'),
  'M_CONTINUE':motif('动作回收成为下一动作起点',['P1','P2','P3','P4'],'从 SEG09 的未完动作进入，贯穿重组的回收再启动，终至擦镜之后仍在继续的 SEG11 交接。')
 }
}
request = dict(kind='M1Request',contract_version='1.0.0',request_id='REQ_FOUR_M1',target='M1',work_id=WORK,base_version=0,sources=sources,inputs=dict(work_type='mv',creative_request='保留四人队形 MV 的人物与作品方向，整理 M1；本次仅细化完整给出的 SEG10 为四个语义段。',delivery_use='后续专业模块的可审查候选依据；保留真实冲突并实际执行父接受。',notes='只有两份文本；未提供图片、音乐、视频、cuts_manifest.json 或整片其余 13 段完整稿。'))
save('request-m1.json',request)
proposals=[]
for i, changes, issues in [(1,changes11,[conflict,missing,camera]),(2,changes12,[]),(3,changes13,[timing])]:
    child=dict(request,request_id=f'REQ_FOUR_M1_{i}',target=f'M1.{i}',requested_fields=list(changes))
    if i==2: child['inputs']=dict(work_type='mv',intent_context=changes11['intent']['creative_goal'],paragraph_material='完整 SEG10 源文；必保事件 E_PROTECT / E_TRUST / E_REGROUP / E_HANDOFF 由同批 M1.1 提案供给，尚未经父接受。',notes='读取父请求与相关候选分区的隔离逻辑上下文；本次由同一代理依所有权分别构造，未声称独立子代理执行。')
    if i==3: child['inputs']=dict(work_type='mv',intent_context=changes11['intent']['creative_goal'],emotion_material='按同批候选 P1 保护会合、P2 换层接力、P3 扩张重组、P4 未完接续组织；原文歌词只作情绪提示，无实际音频。',notes='只提议情绪能量与母题；四段及其事件归 M1.2/M1.1 所有。')
    save(f'request-m1-{i}.json',child)
    proposal=dict(kind='M1Proposal',contract_version='1.0.0',proposal_id=f'PROP_FOUR_M1_{i}',module_id=f'M1.{i}',work_id=WORK,base_version=0,source_request_id=child['request_id'],sources=sources,changes=changes,issues=issues,resolutions=[])
    save(f'proposal-m1-{i}.json',proposal)
    proposals.append(proposal)
save('proposal-batch.json',dict(kind='M1ProposalBatch',contract_version='1.0.0',proposals=proposals))
brief=dict(kind='WorkBrief',contract_version='1.0.0',work_id=WORK,version=0,owner_module='M1',status='draft',display={'title':'四人队形 MV — SEG10 文本试用'},sources=sources,content={},issues=[],accepted_proposals=[],consumers=[])
save('workbrief.json',brief)
candidate=dict(brief,content={**changes11,**changes12,**changes13},issues=[conflict,missing,camera,timing])
save('workbrief-proposed.json',candidate)
snapshot=OUT/'inputs'
snapshot.mkdir(exist_ok=True)
for filename in ('README.md','prompt.md'):
    (snapshot/filename).write_bytes((CASE/filename).read_bytes())
resources=['SKILL.md','references/contracts.json','references/contract-guide.md','references/intent-constraints.md','references/paragraph-information.md','references/emotion-motif.md','references/audit-and-handoff.md','scripts/m1_contract.py','assets/workbrief-empty.json']
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def git_blob(path):
    proc=subprocess.run(['git','show',VERSION+':'+str(path.relative_to(REPO))],cwd=REPO,capture_output=True)
    return dict(exit_code=proc.returncode,sha256=hashlib.sha256(proc.stdout).hexdigest() if proc.returncode==0 else None,matches_worktree=(proc.returncode==0 and proc.stdout==path.read_bytes()))
save('input-version-summary.json',dict(work_id=WORK,source_version=VERSION,scope='SEG10 only; 14-segment complete work is contextual',inputs=[dict(path=str(CASE/n),snapshot='inputs/'+n,sha256=digest(CASE/n),git_source=git_blob(CASE/n)) for n in ('README.md','prompt.md')],read_skill_resources=[dict(path=str(SKILL/n),sha256=digest(SKILL/n),read_extent='complete or selected spans as recorded in invocation logs; script selected spans only') for n in resources],log_note='Early calls are explicitly retrospective in logs/prior-tool-invocations-retrospective.json; later exact argv, stdout, stderr and exit codes are retained by run_trial.py. No image/audio/video or actual generation was inspected.',official_protocol_validation='not performed in this trial'))
print(json.dumps({'created':['request-m1.json','request-m1-1.json','request-m1-2.json','request-m1-3.json','proposal-m1-1.json','proposal-m1-2.json','proposal-m1-3.json','proposal-batch.json','workbrief.json','workbrief-proposed.json','input-version-summary.json'],'blocking_issue':conflict['id'],'canonical_version':0},ensure_ascii=False))
