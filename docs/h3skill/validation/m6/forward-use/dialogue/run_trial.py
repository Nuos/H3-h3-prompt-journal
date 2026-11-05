#!/usr/bin/env python3
"""Reproduce this directed offline trial. All generated files stay beside this script."""
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
SKILL = ROOT / 'docs/h3skill/h3-sound-music-dialogue'
ASSETS = SKILL / 'assets'
CLI = SKILL / 'scripts/m6_contract.py'
WORK = 'm6_forward_dialogue'

def read(name):
    return json.loads((ASSETS / name).read_text())

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def unknown(reason):
    return {'state': 'unknown', 'reason': reason}

def na(reason):
    return {'state': 'not_applicable', 'reason': reason}

def known(value, refs=('brief',)):
    return {'state': 'known', 'value': value, 'source_refs': list(refs)}

def ext(id_, shot, source='brief'):
    return {'kind': 'external', 'id': id_, 'shot_id': shot, 'source_id': source, 'source_version': '1'}

def internal(id_):
    return {'kind': 'internal', 'id': id_}

def issue(id_, owner, message):
    return {'issue_id': id_, 'owner': owner, 'status': 'open', 'severity': 'warning', 'message': message, 'source_refs': ['brief']}

task = (OUT.parent / 'dialogue-task.txt').read_text()
(OUT / 'actual-request.txt').write_text(task)
sources = {
    'brief': {'kind': 'user_requirement', 'locator': 'docs/h3skill/validation/m6/forward-use/dialogue-task.txt', 'version': '1', 'excerpt': task},
    'draft_assumption': {'kind': 'hypothesis', 'locator': 'local-design://m6-forward-dialogue/provisional-shot-binding', 'version': '1', 'excerpt': '用户未指定旁白与 ACT-PLACE 所属镜头。仅为本轮可组合草稿暂挂 SHOT-B；不是已确认输入，交接前需确认或重绑定。'},
    'sound_design': {'kind': 'design_decision', 'locator': 'local-design://m6-forward-dialogue/sound-requirements', 'version': '1', 'excerpt': '新设计声音，不复制 VOICE-REF 原信号。语音清晰自然，不推断音色质地、口音或节奏；环境底声低于语音，轻放声仅绑定桌面接触。'}
}

source_template = read('proposal-m6-1.json')['changes']['sources']['items']['speakerA']
sound_sources = {}
for id_, shot, kind, subject, description, shots in [
    ('SOUND-CLERK', 'SHOT-A', 'speaker', ext('ENTITY-CLERK', 'SHOT-A'), '店员 ENTITY-CLERK；对白和画外旁白共用稳定角色声源，不新建独立旁白人物。', ['SHOT-A', 'SHOT-B']),
    ('SOUND-VISITOR', 'SHOT-B', 'speaker', ext('ENTITY-VISITOR', 'SHOT-B'), '顾客 ENTITY-VISITOR；VOICE-REF 只服务该角色的音色参考。', ['SHOT-B']),
    ('SOUND-ROOM', 'SHOT-A', 'environment', na('室内环境声源不绑定人物。'), '两镜共享低声室内环境底声。', ['SHOT-A', 'SHOT-B']),
    ('SOUND-BOX', 'SHOT-B', 'object', unknown('用户未提供盒子的稳定实体 ID；本声源为 ACT-PLACE 接触声的本地设计标识。'), 'ACT-PLACE 所涉及盒子与桌面的轻接触声源；SHOT-B 只是待确认的草稿归属。', ['SHOT-B'])
]:
    s = copy.deepcopy(source_template)
    s.update(sound_source_id=id_, shot_id=shot, source_kind=kind, subject_ref=subject,
             voice_ref=ext('VOICE-REF', 'SHOT-B') if id_ == 'SOUND-VISITOR' else (unknown('未提供店员音色参考。') if id_ == 'SOUND-CLERK' else na('非人声源。')),
             description=known(description, ('brief', 'draft_assumption') if id_ == 'SOUND-BOX' else ('brief',)),
             voice_requirement=known('只参考 VOICE-REF 音色；不复制信号、不复演其台词。未听取文件，质地、口音、声域均未确认。') if id_ == 'SOUND-VISITOR' else (unknown('店员音色、口音、声域未指定。') if id_ == 'SOUND-CLERK' else na('非人声源。')),
             permission=unknown('无实际媒体及其授权记录；本轮只执行用户要求的离线声音设计。'),
             source_refs=['brief', 'draft_assumption'] if id_ == 'SOUND-BOX' else ['brief'], applies_to_shots=shots)
    sound_sources[id_] = s

lines = [('VOCAL-01', 'SHOT-A', 'SOUND-CLERK', 'spoken_dialogue', '先放在桌上，别松手。', 'required'),
         ('VOCAL-02', 'SHOT-B', 'SOUND-VISITOR', 'spoken_dialogue', '好，我接住了。', 'unknown'),
         ('VOCAL-03', 'SHOT-B', 'SOUND-CLERK', 'voiceover', '这一次，我记住了。', 'not_required')]
vocal_template = read('proposal-m6-2.json')['changes']['vocal_events']['items']['lineA']
vocals = {}
for index, (id_, shot, source, kind, text, lips) in enumerate(lines, 1):
    v = copy.deepcopy(vocal_template)
    v.update(vocal_event_id=id_, shot_id=shot, source_ref=internal(source), event_kind=kind,
             original_text=text, approved_text=text, rewrite_approval=na('逐字保留用户原文及标点，没有改写。'),
             delivery=known('保持清晰自然的中文表达；不推断已确认音色。' + ('店员在画面中但不做开口表演，声音作为画外旁白。' if kind == 'voiceover' else ''), ('brief', 'sound_design')),
             lip_sync=lips, audio_origin='new', track_ref=na('新设计语音事件，不位于被复制的注册音轨内。'),
             language=known('中文；具体口音未确认。'),
             continuity=known(f'用户指定语音顺序第 {index} 项：VOCAL-01 → VOCAL-02 → VOCAL-03。台词无需跨切；绝对开始时刻、时长及间隔未知。' + ('旁白暂挂 SHOT-B，镜头归属待确认。' if kind == 'voiceover' else ''), ('brief', 'draft_assumption') if kind == 'voiceover' else ('brief',)),
             source_refs=['brief', 'sound_design', 'draft_assumption'] if kind == 'voiceover' else ['brief', 'sound_design'])
    vocals[id_] = v

music = copy.deepcopy(read('proposal-m6-3.json')['changes']['music']['items']['musicA'])
music.update(music_id='MUSIC-NONE', shot_id='SHOT-A', use_strategy='none',
             audio_selection=na('用户明确没有画外配乐，不选取音乐音轨。'), whole_source='no', additional_audio='yes', removals_or_replacements='no',
             music_requirement=known('无画外配乐；保留对白、旁白、低声室内环境底声及 ACT-PLACE 轻放接触声，不是全片静音。'),
             beat_plan={'kind': 'none', 'bpm': na('无配乐，不制定音乐节拍。'), 'beat_times_seconds': [], 'measurement_asset': na('没有测量媒体。'), 'source_refs': ['brief']},
             applies_to_shots=['SHOT-A', 'SHOT-B'])

effect_template = read('proposal-m6-4.json')['changes']['effects']['items']['stepA']
effects = {}
for id_, shot in [('ROOM-A', 'SHOT-A'), ('ROOM-B', 'SHOT-B')]:
    e = copy.deepcopy(effect_template)
    e.update(effect_id=id_, shot_id=shot, source_ref=internal('SOUND-ROOM'), action_ref=na('环境底声不绑定离散动作。'), event_kind='environment',
             description=known('低声室内环境底声，保持语音可辨识；具体声学质地未观察。', ('brief', 'sound_design')),
             spatial_relation=unknown('没有空间或媒体资料，室内混响、方位及距离未确认。'),
             continuity=known('SHOT-A → SHOT-B 环境底声连续，切镜不重启；具体接缝交由 M9，绝对时刻交由 M7。'),
             track_ref=na('未复制原音轨；此为新设计声层。'), explicit_silence=na('用户要求环境底声存在。'), source_refs=['brief', 'sound_design'])
    effects[id_] = e
e = copy.deepcopy(effect_template)
e.update(effect_id='EFFECT-PLACE', shot_id='SHOT-B', source_ref=internal('SOUND-BOX'), action_ref=ext('ACT-PLACE', 'SHOT-B'),
         description=known('盒子与桌面接触时的一次轻放声。仅绑定接触，不以声音确认释放动作已发生。SHOT-B 归属只是待确认假设。', ('brief', 'sound_design', 'draft_assumption')),
         spatial_relation=known('声源定位为盒子与桌面接触处；声像、距离和混响待空间资料。', ('brief', 'sound_design')),
         continuity=unknown('ACT-PLACE 镜头、接触时刻以及它与三句语音的关系未给出；不可据对白自行排定动作。'),
         track_ref=na('无可复制的注册媒体；新设计接触声。'), explicit_silence=na('用户明确要求保留轻放声。'), source_refs=['brief', 'sound_design', 'draft_assumption'])
effects['EFFECT-PLACE'] = e

common = {
    'task_context': {'owner': 'external', 'source_id': 'brief', 'source_version': '1', 'values': {'source_type': '本轮用户设计输入，不是新案例或媒体观察', 'vocal_order': ['VOCAL-01', 'VOCAL-02', 'VOCAL-03']}},
    'time_context': unknown('无绝对时刻、事件时长或总片长；仅给出三句语音的先后顺序。'),
    'reference_context': {'owner': 'external', 'source_id': 'brief', 'source_version': '1', 'values': {'VOICE-REF': {'role': 'ENTITY-VISITOR 的音色参考', 'audible_file_available': False, 'original_signal_copy': False, 'source_dialogue_reenactment': False, 'asset_version': unknown('用户未提供媒体版本。')}}}
}
requests = []
proposals = []
partitions = [('sources', sound_sources), ('vocal_events', vocals), ('music', {'MUSIC-NONE': music}), ('effects', effects)]
issue_lists = [
    [issue('VOICE-UNHEARD', 'M6.1', 'VOICE-REF 无可听文件，不能确认音色质地、口音或声域；没有执行真实声音服务。')],
    [issue('VO-SHOT-UNKNOWN', 'M6.2', '旁白所属镜头未知，草稿暂挂 SHOT-B；M7/M9 交接前需确认，不得当成用户确定镜头。'), issue('VISITOR-VISIBILITY', 'M6.2', '顾客发言时是否在画面内未说明，lip_sync 保留 unknown。')],
    [],
    [issue('PLACE-SHOT-TIME', 'M6.4', 'ACT-PLACE 的镜头和时刻未知，草稿暂挂 SHOT-B；外部资料由用户转述，URL 与版本未提供，未执行外部检索。'), issue('PLACE-RELEASE-TENSION', 'M6.4', '外部动作描述为顾客将盒子放桌面并释放；对白包含别松手、接住了。声音域仅绑定接触，动作/对白关系交外部动作责任方确认，不改写对白或动作。')]
]
briefs = ['绑定店员、顾客、室内环境与物件接触声源；音色引用仅供顾客。', '逐字保留三句中文及标点；顺序固定；旁白与店员同一稳定声源。', '明确无画外配乐，仍保留其他用户要求的声音。', '两镜室内底声连续；ACT-PLACE 仅设计盒子与桌面的轻放接触声。']
brief_keys = ['source_brief', 'vocal_brief', 'music_brief', 'effects_brief']
for i, (partition, items) in enumerate(partitions, 1):
    r = read(f'request-m6-{i}.json')
    r.update(work_id=WORK, request_id=f'dialogue_request_m6_{i}', sources=copy.deepcopy(sources), inputs=copy.deepcopy(common))
    r['inputs'][brief_keys[i-1]] = briefs[i-1]
    if i in (2, 4):
        r['inputs']['source_context'] = {'items': copy.deepcopy(sound_sources)}
    if i == 2:
        r['inputs']['vocal_texts'] = {x[0]: x[4] for x in lines}
    if i == 4:
        r['inputs']['action_context'] = {'owner': 'external', 'source_id': 'brief', 'source_version': '1', 'values': {'ACT-PLACE': {'description_as_reported_by_user': '顾客将盒子放在桌面并释放', 'shot': unknown('未提供'), 'time': unknown('未提供'), 'external_url_and_version': unknown('未提供')}}}
    p = read(f'proposal-m6-{i}.json')
    p.update(work_id=WORK, proposal_id=f'dialogue_proposal_m6_{i}_v1', source_request_id=r['request_id'], sources=copy.deepcopy(sources), context=copy.deepcopy(r['inputs']), changes={partition: {'items': items}}, issues=issue_lists[i-1], resolutions=[])
    requests.append(r)
    proposals.append(p)
    save(f'request-m6-{i}.json', r)
    save(f'proposal-m6-{i}-v1.json', p)

parent = read('request-m6.json')
parent.update(work_id=WORK, request_id='dialogue_request_m6', sources=copy.deepcopy(sources), inputs=copy.deepcopy(common))
parent['inputs']['sound_brief'] = task
state = read('state-empty.json')
state.update(work_id=WORK, consumers={}, display={'title': '双人对白与同角色画外旁白：离线可组合声音草稿'})
batch = read('proposal-batch.json')
batch.update(work_id=WORK, batch_id='dialogue_batch_v1', proposals=proposals)
save('request-m6.json', parent)
save('requests.json', requests)
save('proposal-batch-v1.json', batch)
save('state-empty.json', state)

run_dir = OUT / ('run-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
run_dir.mkdir()
logs = []
commands = [('route', ['route', 'request-m6.json'])]
commands += [(f'check-m6-{i}', ['check', f'proposal-m6-{i}-v1.json', '--request', f'request-m6-{i}.json']) for i in range(1, 5)]
commands += [('accept', ['accept', 'state-empty.json', 'proposal-batch-v1.json', '--requests', 'requests.json'])]
for index, (label, args) in enumerate(commands, 1):
    cmd = [sys.executable, '-B', str(CLI), *args]
    started = datetime.now(timezone.utc).isoformat()
    cp = subprocess.run(cmd, cwd=OUT, text=True, capture_output=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    prefix = f'{index:02d}-{label}'
    (run_dir / (prefix + '.stdout.json')).write_text(cp.stdout)
    (run_dir / (prefix + '.stderr.txt')).write_text(cp.stderr)
    entry = {'call': index, 'label': label, 'command': cmd, 'cwd': str(OUT), 'started_utc': started, 'returncode': cp.returncode, 'stdout': f'{run_dir.name}/{prefix}.stdout.json', 'stderr': f'{run_dir.name}/{prefix}.stderr.txt'}
    logs.append(entry)
    with (run_dir / 'commands.jsonl').open('a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(json.dumps({'label': label, 'returncode': cp.returncode, 'stdout': cp.stdout if cp.returncode else cp.stdout[:1000]}, ensure_ascii=False))
    if label == 'accept' and cp.returncode == 0:
        result = json.loads(cp.stdout)
        if 'state' in result:
            save('final-state.json', result['state'])

summary = {'trial_type': '主线程收窄流程的定向文字试用，不是严格盲测', 'cli_calls': len(logs), 'failure_calls': sum(x['returncode'] != 0 for x in logs), 'runtime_sha256': hashlib.sha256(CLI.read_bytes()).hexdigest(), 'run_directory': run_dir.name, 'commands': logs, 'state_status': json.loads((OUT / 'final-state.json').read_text())['status'] if (OUT / 'final-state.json').exists() else 'not_accepted', 'scope': 'M6 离线声音计划，未调用真实媒体服务、未制作动作计划、绝对时间轴或完整 H3 提示词', 'provisional_shot_binding': {'VOCAL-03': 'SHOT-B', 'EFFECT-PLACE': 'SHOT-B', 'confirmed': False}}
save('run-summary.json', summary)
print(json.dumps(summary, ensure_ascii=False, indent=2))
