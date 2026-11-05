#!/usr/bin/env python3
"""Build the two text-only forward-use artifacts. Writes only inside this directory."""
import copy, hashlib, json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[4]
SNAP = OUT / 'snapshot'
MANIFEST = json.loads((OUT/'source-manifest.json').read_text())
HASHES = {x['path']:x['sha256'] for x in MANIFEST['files']}
SK = 'docs/h3skill/h3-asset-reference/'
C1 = 'case-studies/2026-10-identity-only-half-body-dance-six-segment/'
C2 = 'case-studies/2026-10-xiashan-veiled-solo-twelve-segment/'

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
def read(rel): return (SNAP/rel).read_text()
def excerpt(text, start, end): return text[text.index(start):text.index(end, text.index(start))].strip()
def case_source(rel, text):
    return {'kind':'case_text','locator':rel,'version':'sha256:'+HASHES[rel],'excerpt':text}
def unknown(why): return {'state':'unknown','reason':why}
def asset(desc, typ, refs):
    return {'media_type':typ,'channels':['audio' if typ=='audio' else 'visual'],
            'locator':unknown('实际媒体没有提供；案例中的标签或旧机器路径不等于可访问文件。'),
            'source_version':unknown('没有取得实际媒体，不能记录其版本或哈希。'),
            'description':desc,'availability':'pending','access_state':'not_checked',
            'observation_state':'description_only','observation_refs':[], 'source_refs':refs}
def entity(kind,desc,refs): return {'kind':kind,'description':desc,'source_refs':refs}
def binding(ent, ast, chan, sel, refs):
    return {'entity_id':ent,'asset_id':ast,'channel':chan,'source_selector':sel,
            'state':'confirmed','authority_refs':['SRC-TASK'],'source_refs':refs}
def permission(bind,attr,dec,use,reason,refs,scope):
    return {'binding_id':bind,'attribute':attr,'decision':dec,'use':use,'scope':scope,
            'authority_refs':['SRC-TASK'],'source_refs':refs,'reason':reason}
def issue(i,owner,blocking,desc,refs):
    return {'issue_id':i,'owner':owner,'state':'open','blocking':blocking,'description':desc,'source_refs':refs}
def make(task,work,sources,assets,entities,bindings,brief,perms,issues):
    ctx={'assets':assets,'entities':{'entities':entities,'bindings':bindings}}
    req={'kind':'M2Request','contract_version':'1.0.0','request_id':'REQ-'+task,
         'target':'M2.3','work_id':work,'base_version':0,'sources':sources,
         'inputs':{'asset_context':assets,'entity_context':ctx['entities'],'permission_brief':brief}}
    prop={'kind':'M2Proposal','contract_version':'1.0.0','proposal_id':'PROP-'+task,
          'module_id':'M2.3','work_id':work,'base_version':0,'source_request_id':req['request_id'],
          'sources':copy.deepcopy(sources),'context':{'asset_registry':copy.deepcopy(assets),
          'entity_registry':copy.deepcopy(ctx['entities'])},
          'changes':{'reference_map':{'permissions':perms,'decisions':{}}},
          'issues':issues,'resolutions':[]}
    folder=OUT/task.lower()
    write_json(folder/'request.json',req)
    write_json(folder/'proposal.json',prop)
    return folder

# Preserve original snapshots. Capture the final dependency bytes separately.
files = [x['path'] for x in MANIFEST['files']]
files += [SK+'references/h3-label-mapping.md',SK+'references/h3-protocol-source.json']
final={'captured_at':datetime.now(timezone.utc).isoformat(),
       'basis':'Read the then-existing bytes per file; not an atomic repository snapshot. Original snapshot is preserved.',
       'files':[], 'unreadable':[]}
for rel in files:
    try:
        data=(REPO/rel).read_bytes()
    except OSError as e:
        final['unreadable'].append({'path':rel,'error':str(e)})
        continue
    dst=OUT/'snapshot-final'/rel
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_bytes(data)
    final['files'].append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),
                           'bytes':len(data),'snapshot':str(dst.relative_to(OUT))})
write_json(OUT/'final-source-manifest.json',final)

# Task 1: direct M2.3 input, without running M2.1 or M2.2.
p1=read(C1+'prompt.md')
s1={
 'SRC-TASK':{'kind':'user_requirement','locator':'current-task:forward-use/task-1','version':'2026-11-05',
  'excerpt':'基于 identity-only-half-body-dance-six-segment 的 README.md 与 prompt.md，把当前双图用途整理为可直接独立调用 M2.3 的请求和提案，并给人可读权限表及 H3 模式/字段交接。只拿到了案例文字，图片/视频/音频没有提供；不改技能、案例、冻结计划，不调用模型/媒体服务或远程写入。'},
 'SRC-README':case_source(C1+'README.md',read(C1+'README.md')[:2200]),
 'SRC-PROMPT':case_source(C1+'prompt.md',excerpt(p1,'<Picture 1> is ONLY','## CAMERA / LENS LANGUAGE')),
 'SRC-CAMERA':case_source(C1+'prompt.md',excerpt(p1,'## CAMERA / LENS LANGUAGE','## COLOR AND LIGHTING'))}
r1=['SRC-TASK','SRC-PROMPT']
a1={'IMG-FACE':asset('案例指称的 Picture 1：面部身份用途。没有看到实际图像。','image',r1),
    'IMG-BODY-SCENE':asset('案例指称的 Picture 2：身体外观、服装、环境用途。没有看到实际图像。','image',r1)}
e1={'PERFORMER':entity('person','按文字要求绑定的唯一表演者；未核验跨图身份。',r1),
    'ENVIRONMENT':entity('scene','文字指定由 Picture 2 提供的环境部分；空间实况未知。',r1)}
b1={'FACE':binding('PERFORMER','IMG-FACE','visual','文字指定的面部身份区域；实际区域未观察。',r1),
    'BODY':binding('PERFORMER','IMG-BODY-SCENE','visual','文字指定的表演者身体、服装、饰品及发型区域。',r1),
    'SCENE':binding('ENVIRONMENT','IMG-BODY-SCENE','visual','文字指定的环境、建筑、背景区域，排除人物姿态。',r1)}
pms1={}
for pid,b,attr,dec,use,why in [
 ('FACE-IDENTITY','FACE','identity','allow','reference','只用于面部身份、五官结构与可辨认比例；不称已观察。'),
 ('FACE-POSE','FACE','pose','forbid','reference','排除头角、手位、臂位、朝向、站姿及静态构图。'),
 ('FACE-MOTION','FACE','motion','forbid','reference','面部参考不提供编舞。'),
 ('FACE-FIRST','FACE','first_frame','forbid','anchor','原文明确不是 opening-frame reference。'),
 ('BODY-APPEARANCE','BODY','appearance','allow','reference','身体比例、整体尺度、参考中可见发型。'),
 ('BODY-CLOTHING','BODY','clothing','allow','reference','服装与配饰。'),
 ('BODY-POSE','BODY','pose','forbid','reference','不复制精确站姿，也不以该静态姿势开场。'),
 ('BODY-MOTION','BODY','motion','forbid','reference','全身参考不提供编舞。'),
 ('BODY-FIRST','BODY','first_frame','forbid','anchor','不得从这张图的静态姿态开场；首帧由文字新动作定义。'),
 ('SCENE-ENV','SCENE','scene','allow','reference','环境、建筑、背景。'),
 ('SCENE-LIGHT','SCENE','lighting','allow','reference','文字授权借用光线方向与曝光；实图光照未核验。'),
 ('SCENE-SPACE','SCENE','spatial_layout','allow','reference','空间深度与环境关系用途，未推断具体几何。'),
 ('SCENE-STYLE','SCENE','style','allow','reference','写实摄影质感用途。')]:
    pms1[pid]=permission(b,attr,dec,use,why,r1,{'kind':'work'})
f1=make('TASK1-IDENTITY','WORK-FORWARD-IDENTITY',s1,a1,e1,b1,
 '独立运行 M2.3：输入已包含文字依据下的素材/实体上下文；以面部身份、身体服装、环境分权，排除两图姿态/编舞/静态首帧。半身机位按文字交 M5。音乐仅作为范围外的待补交接，不因本提案登记图片而视为取得音频。',pms1,
 [issue('MEDIA-MISSING','user',False,'文字层权限可整理；实际图像未提供，必须在生成前补齐并核验区域/跨图身份。',r1),
  issue('H3-MAPPING','M11',False,'Ref2VA 是候选路由；实际模式、上传对象、官方标签及字段编译尚未执行。',['SRC-TASK'])])

# Task 2: keep contradictory source requirements on the same binding and scope.
p2=read(C2+'prompt.md')
seg=excerpt(p2,'# SEGMENT 01','\n# SEGMENT 02')
s2={
 'SRC-TASK':{'kind':'user_requirement','locator':'current-task:forward-use/task-2','version':'2026-11-05',
  'excerpt':'基于 xiashan-veiled-solo-twelve-segment 的 README.md 与 prompt.md，处理 SEG01 的参考资产和音频策略；忠实保留原始要求，没有授权删改矛盾要求。给出可完成部分、缺项与实际需要的决定。只有案例文字，没有实际图片、视频、音频；不改源文件、不调用模型/媒体服务。'},
 'SRC-README':case_source(C2+'README.md',read(C2+'README.md')[:2600]),
 'SRC-ROLES':case_source(C2+'prompt.md',excerpt(seg,'subject_definitions:','<Audio 1> is the song track')),
 'SRC-RHYTHM':case_source(C2+'prompt.md',excerpt(seg,'<Audio 1> is the song track','summary:')),
 'SRC-COPY':case_source(C2+'prompt.md',excerpt(seg,'summary:','COLOR & ATMOSPHERE')),
 'SRC-COLOR':case_source(C2+'prompt.md',excerpt(seg,'COLOR & ATMOSPHERE','PERFORMANCE:')),
 'SRC-POSE':case_source(C2+'prompt.md','CHAIN C1 提沉起势 (4拍) — 入态: <Picture 1> standing pose.'),
 'SRC-FIELDS':case_source(C2+'prompt.md','integrated_multimodal_description:\n\noverall_soundscape: N/A — the reused <Audio 1> is the complete final audio track.\n\nnon_diegetic_music: N/A — <Audio 1> is directly reused 1:1 as the complete final audio track.')}
r2=['SRC-TASK','SRC-ROLES']; ar=['SRC-TASK','SRC-RHYTHM','SRC-COPY']
a2={'IMG-FRONT':asset('案例称 Picture 1 为无头部信息的正面全身图；实际图像未提供。','image',r2),
    'IMG-THREE-VIEW':asset('案例称 Picture 2 为脸部、背部与口鼻半纱面纱的三视图；实际图像未提供。','image',r2),
    'AUDIO-SEG01':asset('案例指称 Audio 1；旧本地路径只作文字记录，不视为已挂载。段内音频与源窗口未取得。','audio',ar)}
e2={'DANCER':entity('person','SEG01 的唯一目标舞者；相同人物为文字绑定要求，未观察核验。',r2),
    'ENVIRONMENT':entity('scene','文字要求星海高台夜景且无其他人物；并非实图场景观察。',r2),
    'SOUNDTRACK':entity('soundtrack','SEG01 指定歌曲音轨；不自动授权角色音色模仿。',ar)}
b2={'FRONT':binding('DANCER','IMG-FRONT','visual','正面身体与服装部分，不含头部；文字用途确认。',r2),
    'FACE-BACK':binding('DANCER','IMG-THREE-VIEW','visual','三视图中的脸、发型、背面服装与半面纱部分；文字用途确认。',r2),
    'ENV-LOOK':binding('ENVIRONMENT','IMG-FRONT','visual','原文 COLOR & ATMOSPHERE 声称来自 Picture 1 的环境语言，待实际图像验证。',['SRC-TASK','SRC-COLOR']),
    'MUSIC':binding('SOUNDTRACK','AUDIO-SEG01','audio','SEG01 所称 Audio 1；具体媒体与源时间窗口未提供。',ar)}
sc={'kind':'shots','shot_ids':['SEG01']}
pms2={}
rows=[
 ('FRONT-BODY','FRONT','appearance','allow','reference','正面身体用途；不推断未见的头部。',r2),
 ('FRONT-CLOTHES','FRONT','clothing','allow','reference','subject_definitions 指定正面服装唯一来自图1。',r2),
 ('FACE-ID','FACE-BACK','identity','allow','reference','面部身份、眼眉来自图2。',r2),
 ('FACE-HAIR','FACE-BACK','appearance','allow','reference','图2负责脸与发型，图1无头部信息。',r2),
 ('BACK-VEIL','FACE-BACK','clothing','allow','reference','图2负责背面服装与半纱面纱；面纱全程遮口鼻、眼眉可见；不新增服装描述。',r2),
 ('COLOR-EXCLUSIVE','FACE-BACK','clothing','forbid','reference','保留 COLOR 段“costume comes solely from Picture 1”的排他要求；按其字面会排除图2服装权限，与 BACK-VEIL 冲突，未裁决。',['SRC-TASK','SRC-COLOR']),
 ('FRONT-POSE','FRONT','pose','allow','reference','原文 C1 入态明写 Picture 1 standing pose；只保留该链入态，不提升为首帧锚定。',['SRC-TASK','SRC-POSE']),
 ('FRONT-ANCHOR','FRONT','first_frame','unknown','anchor','0.00 fully referenced 没有明确等同于实图首帧；且开场是袖/衣摆局部特写，待 M11 澄清。',r2),
 ('ENV-LIGHT','ENV-LOOK','lighting','allow','reference','原文授权的环境调色与光照语言；非媒体观察。',['SRC-TASK','SRC-COLOR']),
 ('ENV-COLOR','ENV-LOOK','color','allow','reference','调色只影响光和环境，不授权变装。',['SRC-TASK','SRC-COLOR']),
 ('AUDIO-TIMING','MUSIC','audio_timing','allow','reference','BPM 134.0、beat 0.4478、bar 1.7910、首拍 0.441 与歌词起点按文字登记，未分析音频。',['SRC-TASK','SRC-RHYTHM']),
 ('AUDIO-REF-ONLY','MUSIC','audio_content','allow','reference','保留 referenced only for rhythm；只借用节奏语义，不增加音色模仿授权。',['SRC-TASK','SRC-RHYTHM']),
 ('AUDIO-NO-COPY','MUSIC','audio_content','forbid','copy','保留明确的 No signal copy。',['SRC-TASK','SRC-RHYTHM']),
 ('AUDIO-EXACT-COPY','MUSIC','audio_content','allow','copy','同时保留 reused 1:1、complete final audio track 与 fully_copy；不得擅自选掉另一要求。',['SRC-TASK','SRC-COPY'])]
for pid,b,attr,dec,use,why,refs in rows: pms2[pid]=permission(b,attr,dec,use,why,refs,sc)
f2=make('TASK2-XIASHAN-SEG01','WORK-FORWARD-XIASHAN',s2,a2,e2,b2,
 '仅处理 SEG01。忠实保存双图属性分工、C1 的图1站姿入态与半纱面纱要求。把仅参考节奏/禁止信号复制和完整音轨1:1复制同时建模；decisions 留空，用户尚未授权选择。不要把0秒fully referenced直接改成首帧锚定。',pms2,
 [issue('AUDIO-POLICY-CONFLICT','user',True,'同一 MUSIC/SEG01/audio_content/copy 同时 forbid 与 allow；需要原需求权威明确音频政策。',ar),
  issue('COSTUME-SOURCE-CONFLICT','user',True,'图2的背面服装/面纱权威与 COLOR 中全服装只来自图1不能同时按字面执行。',['SRC-TASK','SRC-ROLES','SRC-COLOR']),
  issue('MISSING-MEDIA','user',False,'双图和 SEG01 实际音频未提供；文字登记可完成，媒体身份、区域、时长与内容不可验证。',r2+['SRC-COPY']),
  issue('SOURCE-WINDOW','M7',True,'prompt SEG01 为0.000–11.116；README切段表起始区间另有12.860秒等记录；必须明确本段音频、版本及源窗口。',['SRC-TASK','SRC-README','SRC-COPY']),
  issue('PREVIOUS-SEGMENT','M9',False,'SEG01声称延续上段，但未给前段资产或状态；不虚构续接。',['SRC-TASK','SRC-COPY']),
  issue('H3-FIELD-MIX','M11',False,'原案把 Ref2VA 字段与 integrated_multimodal_description 并用；只交接迁移建议，不改写源案例。',['SRC-TASK','SRC-FIELDS'])])

for folder,case,text in [(f1,C1,p1),(f2,C2,seg)]:
    name='task1' if folder==f1 else 'task2'
    (folder/'actual-input.md').write_text('# 实际输入：'+name+'\n\n来源为当前请求与两份案例文字。没有提供图片、视频、音频，也没有访问案例中旧机器路径。\n\n'
        '本次只采用原始 snapshot 的案例字节；完整文件和 SHA256 见 source-manifest.json。媒体字段均为 pending / not_checked / description_only；binding 的 confirmed 只表示用户要求采用该文字分工。\n\n'
        + ''.join('- `'+case+x+'` SHA256 `'+HASHES[case+x]+'`\n' for x in ['README.md','prompt.md'])
        +'\n## 当前请求\n\n'+(s1 if folder==f1 else s2)['SRC-TASK']['excerpt']
        +'\n\n## 本次直接使用的 prompt 文字\n\n'+(text[:text.index('## COLOR AND LIGHTING')] if folder==f1 else text)+'\n')
    (folder/'permissions.md').write_text('# 人可读权限表\n\n这是文字权限提案，不是已接受状态或媒体观察。内部 ID 不直接充当 H3 官方标签。\n\n'
        +'|权限 ID|绑定|属性|决策|用途|理由|\n|---|---|---|---|---|---|\n'
        +''.join('|'+pid+'|'+p['binding_id']+'|'+p['attribute']+'|'+p['decision']+'|'+p['use']+'|'+p['reason'].replace('|','/').replace('\n',' ')+'|\n' for pid,p in (pms1 if folder==f1 else pms2).items())
        +'\n`decisions` 为空。本次未执行 accept。'+('本表工作级范围覆盖六段相同双图用法。' if folder==f1 else '本表范围仅 SEG01；两组相反服装/音频要求同时保留，尚不能成为可接受权限状态。')+'\n')

write_json(OUT/'initial-errors.json',[
 {'order':1,'recorded_after_fact':True,'timestamp':None,'command':'cat docs/h3skill/h3-asset-reference/references/contract-guide.md','exit_code':1,
  'stderr':'cat: docs/h3skill/h3-asset-reference/references/contract-guide.md: No such file or directory',
  'revision':'文件随后由其他工作落盘；重新读取成功并记录于原始 source-manifest.json；没有为绕过规则自行创建该依赖。'},
 {'order':2,'recorded_after_fact':True,'timestamp':None,'command':'rg --files docs/h3skill/h3-asset-reference docs/h3skill/validation/m2/forward-use','exit_code':2,
  'stderr':'rg: docs/h3skill/validation/m2/forward-use: No such file or directory (os error 2)',
  'revision':'随后在用户允许的目录建立验证目录并保存快照。'}])
print(json.dumps({'written':['task1-identity/request.json','task1-identity/proposal.json','task2-xiashan-seg01/request.json','task2-xiashan-seg01/proposal.json'], 'final_snapshot_unreadable':final['unreadable']},ensure_ascii=False))
