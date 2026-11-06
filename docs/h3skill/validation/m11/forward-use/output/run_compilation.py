#!/usr/bin/env python3
"""Task-specific caller of the unmodified public M11 CLI; no media/network use."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import shlex
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
PKG = ROOT / 'h3-model-protocol'
CLI = PKG / 'scripts/m11_contract.py'
WORK = 'tea-shop-eight-second'
REVISION = 2
PRIOR_STATE = OUT/'revision-history/round-1/results/accepted-state.json'

def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

for folder in ['requests', 'proposals', 'checks', 'logs', 'results']:
    (OUT / folder).mkdir(exist_ok=True)

records = []
def run(name, args, output_path, expected_code=0):
    argv = [sys.executable, str(CLI), *map(str, args)]
    p = subprocess.run(argv, cwd=PKG, text=True, capture_output=True)
    stdout_path = OUT / 'logs' / (name + '.stdout.txt')
    stderr_path = OUT / 'logs' / (name + '.stderr.txt')
    stdout_path.write_text(p.stdout, encoding='utf-8')
    stderr_path.write_text(p.stderr, encoding='utf-8')
    if output_path:
        output_path.write_text(p.stdout, encoding='utf-8')
    rec = {'sequence': len(records)+1, 'name': name,
           'cwd': str(PKG), 'argv': argv, 'command': shlex.join(argv),
           'exit_code': p.returncode, 'expected_exit_code': expected_code,
           'stdout_file': str(stdout_path.relative_to(OUT)),
           'stderr_file': str(stderr_path.relative_to(OUT)),
           'stdout_bytes': len(p.stdout.encode()), 'stderr_bytes': len(p.stderr.encode())}
    records.append(rec)
    write_json(OUT/'command-log.json', records)
    print(f'{name}: exit={p.returncode}; stdout={rec["stdout_file"]}; stderr={rec["stderr_file"]}', flush=True)
    if p.returncode != expected_code:
        print(p.stdout, p.stderr, flush=True)
        raise SystemExit(p.returncode or 1)
    if name == '00-help':
        return p.stdout
    return json.loads(p.stdout)

task_text = (ROOT/'task.md').read_text(encoding='utf-8')
arrangements = {
    'status': 'agent-authored-expression-and-timing-arrangements',
    'version': '1',
    'speaking_onsets_ms': {'luo_voice': 600, 'ye_voice': 4100},
    'reason': 'The public speaker/utterance contract requires concrete first-vocal times. The task fixes speaker order and shot membership but does not specify these onsets.',
    'camera_expression': 'Hold each requested medium viewpoint steady; no extra cut or shot.',
    'delivery_expression': 'Luo speaks conversationally; Ye gives a clear gentle warning; both finish their one line in the assigned shot.',
    'state_expression': 'Cup placement precedes Luo speech and pouring; kettle set-down precedes Ye speech and cup movement; hold the specified result through 8 seconds.',
    'unknown_reference_features': 'No invented face, hair, gender, music instrumentation, tempo, or dynamics; use the declared source role only.',
    'asset_locators': 'declared-media:// locators identify unavailable declared assets, not files, uploads, or executable backend values.'
}
write_json(OUT/'author-arrangements.json', arrangements)

example_sources = read_json(PKG/'assets/examples/m11-1-request.json')['sources']
sources = {k: copy.deepcopy(v) for k,v in example_sources.items() if k in ['official-base','official-ref']}
sources['task-plan'] = {
    'kind':'user_text', 'locator':str(ROOT/'task.md'), 'version':'1',
    'excerpt':task_text, 'sha256':hashlib.sha256((ROOT/'task.md').read_bytes()).hexdigest()
}
sources['agent-arrangement'] = {
    'kind':'agent_arrangement', 'locator':str(OUT/'author-arrangements.json'), 'version':'1',
    'excerpt':json.dumps(arrangements, ensure_ascii=False),
    'sha256':hashlib.sha256((OUT/'author-arrangements.json').read_bytes()).hexdigest()
}
revision_note = {
    'revision':REVISION,'reviewer':'root Agent','basis':'Public Ref2VA guide section 6 and prompt-compilation sound-layer rules',
    'first_round':'All three public checks passed, but root Agent field review found dialogue synchronization and intelligibility requirements in overall_soundscape.',
    'correction':'Move dialogue execution requirements into each detailed_description shot; retain only physical sound layers in overall_soundscape.',
    'unchanged':'Story, actions, cut, exact dialogue/sign, target parameters, reference permissions, and audio reuse strategy.',
    'prior_accepted_state':str(PRIOR_STATE),'base_version':read_json(PRIOR_STATE)['version'],
    'scope':'Supervised field-placement revision, not evidence that first-round semantics had been automatically verified.'
}
write_json(OUT/'revision-notes.json',revision_note)
sources['field-review'] = {
    'kind':'agent_review','locator':str(OUT/'revision-notes.json'),'version':'1',
    'excerpt':json.dumps(revision_note,ensure_ascii=False),
    'sha256':hashlib.sha256((OUT/'revision-notes.json').read_bytes()).hexdigest()
}
write_json(OUT/'source-register.json',sources)
manifest = {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(PKG.rglob('*')) if p.is_file() and p.suffix in ['.py','.json','.md','.txt']}
write_json(OUT/'toolchain-snapshot.json',{
    'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'python':sys.version, 'package_root':str(PKG), 'sha256':manifest,
    'note':'Hashes identify the current supplied package; no historical copy or external repository was used.'})

def request(n, inputs):
    q = {'kind':'M11Request','contract_version':'1.0.0','route_version':'1.0.0',
         'work_id':WORK,'base_version':read_json(PRIOR_STATE)['version'],'request_id':f'tea-m11-{n}-v{REVISION}','target':f'M11.{n}',
         'sources':copy.deepcopy(sources),'inputs':inputs}
    path=OUT/'requests'/f'm11-{n}-request.json'
    write_json(path,q)
    return path,q

requests=[]
proposals=[]
def compile_module(n,inputs):
    path,q=request(n,inputs)
    run(f'{n}1-route',['route',path],OUT/'results'/f'm11-{n}-route.json')
    ppath=OUT/'proposals'/f'm11-{n}-proposal.json'
    p=run(f'{n}2-propose',['propose',path],ppath)
    check=run(f'{n}3-check',['check',ppath,'--request',path],OUT/'checks'/f'm11-{n}-check.json')
    requests.append(q); proposals.append(p)
    return next(iter(p['changes'].values()))

run('00-help',['--help'],None)
profile=compile_module(1, {'profile':read_json(PKG/'assets/profiles/official-protocol-only.json')})
write_json(OUT/'results/capability-profile.json',profile)

shots=[{'shot_id':'tea-front','start_ms':0},{'shot_id':'tea-side','start_ms':3500}]
assets=[
    {'asset_id':'portrait_ye','version':'img-1','media_type':'image','uri':'declared-media://portrait_ye/img-1','purpose':'appearance','source_refs':['task-plan']},
    {'asset_id':'portrait_luo','version':'img-2','media_type':'image','uri':'declared-media://portrait_luo/img-2','purpose':'appearance','source_refs':['task-plan']},
    {'asset_id':'room_music','version':'audio-1','media_type':'audio','uri':'declared-media://room_music/audio-1','purpose':'audio_reuse','source_refs':['task-plan']}
]
subjects=[
    {'subject_id':'ye_qing','source_asset_ids':['portrait_ye'],
     'description':'Ye Qing, the tea-shop clerk, with identity and light-gray apron supplied by the source portrait. Only identity and this apron are retained; the target scene establishes pose, background, camera viewpoint, and natural lighting.',
     'retention':'fully_preserved','retention_reason':'Preserve the defined identity and light-gray apron in both shots; source pose, background, camera viewpoint, and lighting are outside this reference role. The portrait is not a target first or last frame.',
     'shot_ids':['tea-front','tea-side']},
    {'subject_id':'luo_cheng','source_asset_ids':['portrait_luo'],
     'description':'Luo Cheng, the customer, with identity and dark-blue jacket supplied by the source portrait. Only identity and this jacket are retained; the target scene establishes pose, background, camera viewpoint, and natural lighting.',
     'retention':'fully_preserved','retention_reason':'Preserve the defined identity and dark-blue jacket in both shots; source pose, background, camera viewpoint, and lighting are outside this reference role. The portrait is not a target first or last frame.',
     'shot_ids':['tea-front','tea-side']}
]
binding=compile_module(2,{
    'capability_profile':profile,
    'plan':{'duration_ms':8000,'shots':shots,'requested_mode':'Ref2VA'},
    'assets':assets,'subjects':subjects,'reference_items':[],
    'audio_bindings':[{'asset_id':'room_music','role':'reuse',
       'description':'The licensed, lyric-free eight-second music signal, reused in full as audience-only background music throughout both shots. It is inaudible to the characters and forms one layer beneath the newly recorded dialogue and physical sounds.',
       'retention':'partially_copy',
       'retention_reason':'Copy the complete eight-second source music stem while adding newly recorded dialogue, pouring, kettle set-down, and cup-base sliding sounds; the source music is not the complete final soundtrack.',
       'full_source':True,'entire_soundtrack':False,
       'additional_layers':['new-dialogue','tea-pouring','kettle-set-down','cup-base-sliding'],'replaced_layers':[]}],
    'speakers':[
       {'speaker_id':'ye_voice','first_vocal_ms':4100,'first_event_kind':'speech','source_refs':['task-plan','agent-arrangement']},
       {'speaker_id':'luo_voice','first_vocal_ms':600,'first_event_kind':'speech','source_refs':['task-plan','agent-arrangement']}
    ]
})
write_json(OUT/'results/reference-binding.json',binding)

obligation_specs=[
 ('setting-front','tea-front','Bright photorealistic naturally lit street-corner tea shop; Ye inside in light-gray apron, Luo outside in dark-blue jacket, counter between them.'),
 ('framing-front','tea-front','Only first shot starts at 0; frontal medium includes both shoulders/necks, hands and the whole cup.'),
 ('sign-front','tea-front','Wall sign remains clearly readable as 今日茶已备好！ with exact punctuation.'),
 ('place-empty-cup','tea-front','Luo first places an empty ceramic cup at the center of the counter.'),
 ('luo-line','tea-front','Luo says 请给我一杯热茶。 exactly once with unchanged words and punctuation.'),
 ('pouring-hands','tea-front','Ye grips kettle handle with right hand and steadies lid with left hand.'),
 ('pouring-target','tea-front','Hot tea flows into the cup; cup stays at the center and does not move during pouring.'),
 ('cut-side','tea-side','The second and only cut is exactly at generated-local 3500 ms to side medium.'),
 ('continuity-side','tea-side','Same two identities, clothes, counter separation and filled cup continue into the side shot.'),
 ('sign-side','tea-side','Wall sign continues to show the original exact text 今日茶已备好！.'),
 ('return-kettle','tea-side','Ye returns the kettle onto the inner side of the counter before speaking.'),
 ('ye-line','tea-side','Ye says 小心，茶还很烫！ exactly once with unchanged words and punctuation.'),
 ('move-cup','tea-side','Luo grips the cup handle with right hand and carefully moves the cup to the outer counter edge.'),
 ('ye-hands-clear','tea-side','Ye keeps both hands clear of the cup during Luo taking it and in the result state.'),
 ('end-state','tea-side','At the eight-second endpoint both people retain this result state; no extra shot.'),
 ('music-front','tea-front','Use the whole original eight-second lyric-free music as audience-only score with new dialogue and pouring.'),
 ('music-side','tea-side','Continue the same music without restart across the cut; add new dialogue, kettle set-down and cup-base sliding.')
]
obligations=[{'obligation_id':i,'shot_id':s,'description':d,'source_refs':['task-plan']} for i,s,d in obligation_specs]
front = '''A steady frontal medium view establishes the bright street-corner tea shop and keeps both people\'s shoulders and necks, their hands, and the complete ceramic cup visible together. {{ref:ye_qing}}, the clerk in the light-gray apron, stands on the inner side of the counter. {{ref:luo_cheng}}, the customer in the dark-blue jacket, stands on the outer side; the counter separates them throughout. A clearly legible wall sign reads "今日茶已备好！". First, {{ref:luo_cheng}} places an empty ceramic cup at the counter center, then releases it so it rests upright. Beginning about 0.6 seconds into the video, {{ref:luo_cheng}} ({{speaker:luo_voice}}) faces the clerk and says once in a conversational voice, {{utterance:luo-request}}. Synchronize the newly recorded dialogue to visible mouth movement and keep it intelligible. The clerk listens without speaking. After the request, {{ref:ye_qing}} takes the kettle handle firmly in the right hand and steadies its lid with the left. With these distinct hand contacts maintained, the clerk tilts the kettle above the cup and pours hot tea. The visible stream lands inside the cup, accompanied by the sound of pouring; the cup stays in its original central position. The pour finishes before the cut. Keep the medium framing steady and the hands, spout, stream, and whole cup unobstructed. The complete source music signal from {{ref:room_music.audio}} starts with this shot as audience-only score beneath the new dialogue and pouring sounds.'''
side = '''cut to a steady side medium view of the same counter, maintaining the clerk on its inner side and the customer on its outer side. The same filled cup remains at the center at the cut, and the wall sign remains readable. The natural daylight, referenced identities, light-gray apron, and dark-blue jacket continue unchanged. {{ref:ye_qing}} sets the kettle back on the inner counter, with its base contacting the surface audibly, then releases the kettle. Beginning about 4.1 seconds into the video, {{ref:ye_qing}} ({{speaker:ye_voice}}) gives a clear, gentle warning once, {{utterance:ye-warning}}. Synchronize the newly recorded dialogue to visible mouth movement and keep it intelligible. After the warning, {{ref:luo_cheng}} grips the cup handle with the right hand and carefully draws the cup along the surface toward the outer counter edge. A light cup-base sliding sound accompanies this movement. {{ref:ye_qing}} keeps both hands clear of the cup. The side view shows the handle grip, the entire cup, and its path without hiding the counter separation. By the end, the cup rests securely at the outer edge, the customer\'s right hand remains on its handle, and the kettle rests inside with the clerk\'s hands away from the cup. Hold these positions through the eight-second endpoint. {{ref:room_music.audio}} continues seamlessly across the cut and through the end, with the new warning, kettle contact, and cup movement audible above it.'''
compilation=compile_module(3,{
    'binding':binding,
    'fragments':{
       'style':'Photorealistic footage in a bright street-corner tea shop, with natural daylight and clearly readable hand actions. Maintain the same daylight and realistic materials across both shots.',
       'summary':'In an eight-second, two-shot exchange, {{ref:luo_cheng}} requests hot tea and {{ref:ye_qing}} pours it, returns the kettle, and warns the customer before the filled cup moves to the outer counter edge. Preserve both identities and their specified clothing, with the counter between them; reuse {{ref:room_music.audio}} as the complete audience-only music stem with new dialogue and physical sounds.',
       'shots':[
          {'shot_id':'tea-front','text':front,'obligation_ids':[i for i,s,d in obligation_specs if s=='tea-front']},
          {'shot_id':'tea-side','text':side,'obligation_ids':[i for i,s,d in obligation_specs if s=='tea-side']}],
       'overall_soundscape':'Physical sound consists of clear tea pouring, a brief kettle-base contact on the counter, and a light cup-base scrape.',
       'non_diegetic_music':'Copy the complete original eight-second, lyric-free signal from {{ref:room_music.audio}} from beginning to end at its original speed, continuously across the cut. Preserve the source instrumentation, tempo, rhythm, and dynamic progression. This is the audience-only music layer and is inaudible to the characters; new dialogue and the specified physical sounds are added to form the final soundtrack.'
    },
    'obligations':obligations,
    'utterances':[
       {'utterance_id':'luo-request','speaker_id':'luo_voice','language':'Chinese','text':'请给我一杯热茶。','source_text':'请给我一杯热茶。','start_ms':600,'shot_id':'tea-front','mode':'on_screen','origin':'generated','source_refs':['task-plan','agent-arrangement']},
       {'utterance_id':'ye-warning','speaker_id':'ye_voice','language':'Chinese','text':'小心，茶还很烫！','source_text':'小心，茶还很烫！','start_ms':4100,'shot_id':'tea-side','mode':'on_screen','origin':'generated','source_refs':['task-plan','agent-arrangement']}],
    'complete_silence':False,'music_present':True,
    'visible_text':[{'text_id':'wall-sign','text':'今日茶已备好！','shot_id':'tea-front'}]
})
write_json(OUT/'results/prompt-compilation.json',compilation)
(OUT/'model-prompt.txt').write_text(compilation['rendered_prompt']+'\n',encoding='utf-8')
write_json(OUT/'model-fields.json',compilation['fields'])

target_parameters={'duration_ms':8000,'width':1080,'height':1920,'fps':24}
write_json(OUT/'target-parameters.json',target_parameters)
path4,q4=request(4, {'compilation':compilation,'capability_profile':profile,'parameters':target_parameters,'asset_map':{}})
run('41-route',['route',path4],OUT/'results/m11-4-route.json')
run('42-propose-blocked',['propose',path4],OUT/'results/m11-4-export-blocked.json',expected_code=2)

state=read_json(PRIOR_STATE)
write_json(OUT/'state-before-revision.json',state)
write_json(OUT/'requests/accepted-requests.json',requests)
write_json(OUT/'proposals/accepted-proposals.json',proposals)
accepted=run('50-accept',['accept',OUT/'proposals/accepted-proposals.json','--requests',OUT/'requests/accepted-requests.json','--state',OUT/'state-before-revision.json'],OUT/'results/accept-result.json')
write_json(OUT/'results/accepted-state.json',accepted['state'])
print('Accepted status:',accepted['state']['status'],flush=True)
print('Compiled field order:',compilation['field_order'],flush=True)
print('Export block:',read_json(OUT/'results/m11-4-export-blocked.json'),flush=True)
