from pathlib import Path
import copy, json, subprocess, sys
from fractions import Fraction as F

OUT = Path(__file__).resolve().parent
REPO = next(p for p in OUT.parents if (p / 'docs/h3skill/h3-time-synchronization/SKILL.md').is_file())
PKG = REPO / 'docs/h3skill/h3-time-synchronization'
RUNNER = PKG / 'scripts/m7_contract.py'
def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
unknown = lambda why: {'state':'unknown','reason':why}
sources = {'task': {'kind':'user_requirement','locator':'docs/h3skill/validation/m7/forward-use/mapping-task.txt','version':'1','excerpt':'用户固定 sourceA CFR24、[2,8) 2x 到 workA[10,13)，gen02 局部 [0,3) 1x 到 editA[5,8) CFR30；contactA=4.125s，cameraReadyA=3.5s，至少提前0.2工作秒；选接触后的第一编辑帧，误差不超过0.005s。'}}
def clock(cid, domain, did, fps, extent):
    return {'record_type':'clock','clock_id':cid,'domain':domain,'domain_id':did,'rate_mode':'unknown' if isinstance(fps,dict) else 'cfr','fps':fps,'origin':0,'extent':extent,'evidence':{'basis':'planned','source_refs':['task']},'source_refs':['task']}
clocks = {
 'source_clock':clock('source_clock','source','sourceA',24,10),
 'work_clock':clock('work_clock','work','workA',unknown('任务未指定工作域帧率'),unknown('任务未指定完整工作域时长')),
 'generation_clock':clock('generation_clock','generation','gen02',unknown('任务未指定生成端帧率，禁止从其他域推断'),3),
 'edit_clock':clock('edit_clock','edit','editA',30,unknown('任务只指定所用编辑区间，不代表完整编辑域时长'))}
def mapping(a,b,s0,s1,t0,t1,speed):
    return dict(source_clock_id=a,target_clock_id=b,mode='linear',source_start=s0,source_end=s1,target_start=t0,target_end=t1,speed=speed)
maps = {
 'source_to_work':mapping('source_clock','work_clock',2,8,10,13,2),
 'work_to_generation':mapping('work_clock','generation_clock',10,13,0,3,1),
 'generation_to_edit':mapping('generation_clock','edit_clock',0,3,5,8,1)}
edit = {'owner':'M9','source_id':'task','source_version':'1','values':{'mappings':{k:maps[k] for k in ['source_to_work','generation_to_edit']},'cut_policy':{'selected_visual_switch':'cutA','after':'contactA','rule':'ceil','tolerance_seconds':'1/200'}}}
task = {'owner':'external','source_id':'task','source_version':'1','values':{'mappings':{'work_to_generation':maps['work_to_generation']},'generation_id':'gen02','work_start':10,'local_duration':3}}
action = {'owner':'M4','source_id':'task','source_version':'1','values':{'contactA':{'event_ref':{'owner':'M4','kind':'action','id':'contactA','domain':'source','domain_id':'sourceA'},'time':'33/8'}}}
camera = {'owner':'M5','source_id':'task','source_version':'1','values':{'cameraReadyA':{'event_ref':{'owner':'M5','kind':'camera','id':'cameraReadyA','domain':'source','domain_id':'sourceA'},'time':'7/2','meaning':'camera ready, not camera motion start'},'minimum_work_lead':'1/5'}}
inputs = {'mapping_brief':'核验已确定的三段映射；推导 contactA 与 cameraReadyA 的 work/gen/edit 秒数；检查工作域提前0.2秒，并量化唯一已选切换至接触后的第一个30fps编辑帧，误差<=0.005秒。','timebase_context':{'items':clocks},'edit_context':edit,'task_context':task,'action_context':action,'camera_context':camera}
req = {'kind':'M7Request','contract_version':'1.0.0','work_id':'forward_mapping','base_version':0,'request_id':'req_mapping','target':'M7.3','sources':sources,'inputs':inputs}
items={}
for key, spec in maps.items():
    owner = 'external' if key == 'work_to_generation' else 'M9'
    items[key] = {'record_type':'mapping','mapping_id':key,**spec,'edit_binding':{'owner':owner,'source_id':'task','source_version':'1','path':'/mappings/'+key,'value':copy.deepcopy(spec)},'source_refs':['task']}
items['cutA_quantization']={'record_type':'quantization','quantization_id':'cutA_quantization','clock_id':'edit_clock','time':'97/16','rule':'ceil','frame_index':182,'quantized_time':'91/15','error_seconds':'1/240','tolerance':'1/200','requirement':'within_tolerance','position_kind':'boundary','source_refs':['task']}
prop = {'kind':'M7Proposal','contract_version':'1.0.0','work_id':'forward_mapping','base_version':0,'proposal_id':'proposal_mapping','module_id':'M7.3','source_request_id':'req_mapping','sources':sources,'context':copy.deepcopy(inputs),'changes':{'mappings':{'items':items}},'issues':[],'resolutions':[]}
save('request.json',req)
save('proposal.json',prop)
(OUT/'task-copy.txt').write_text((REPO/'docs/h3skill/validation/m7/forward-use/mapping-task.txt').read_text(encoding='utf-8'),encoding='utf-8')
commands=[]
def run(label,args):
    argv=[sys.executable,str(RUNNER),*args]
    p=subprocess.run(argv,cwd=REPO,text=True,capture_output=True)
    (OUT/(label+'.stdout.txt')).write_text(p.stdout,encoding='utf-8')
    (OUT/(label+'.stderr.txt')).write_text(p.stderr,encoding='utf-8')
    commands.append({'label':label,'argv':argv,'cwd':str(REPO),'returncode':p.returncode,'stdout':label+'.stdout.txt','stderr':label+'.stderr.txt'})
    print(label, 'exit',p.returncode, p.stdout[:1500],p.stderr[:1000])
    save('commands.json',commands)
run('01-help',['--help'])
run('02-route',['route',str(OUT/'request.json')])
run('03-check',['check',str(OUT/'proposal.json'),'--request',str(OUT/'request.json')])
for label,value,start,end,dest,speed in [
 ('04-contact-source-work','33/8','2','8','10','2'),
 ('05-contact-work-generation','177/16','10','13','0','1'),
 ('06-contact-generation-edit','17/16','0','3','5','1'),
 ('07-camera-source-work','7/2','2','8','10','2'),
 ('08-camera-work-generation','43/4','10','13','0','1'),
 ('09-camera-generation-edit','3/4','0','3','5','1')]:
    run(label,['map','--value',value,'--source-start',start,'--source-end',end,'--destination-start',dest,'--speed',speed])
run('10-cut-quantize',['quantize','--value','97/16','--fps','30','--rule','ceil','--tolerance','1/200'])
run('11-contact-source-frame',['convert','--value','33/8','--from-unit','s','--to-unit','frames','--fps','24'])
run('12-camera-source-frame',['convert','--value','7/2','--from-unit','s','--to-unit','frames','--fps','24'])
# Exact checks are independent arithmetic over supplied plans, not media measurements.
def data(v):
    v=F(v)
    return {'rational':str(v),'decimal_seconds':float(v)}
contact_s=F(33,8);camera_s=F(7,2)
contact_w=10+(contact_s-2)/2;camera_w=10+(camera_s-2)/2
contact_g=contact_w-10;camera_g=camera_w-10
contact_e=contact_g+5;camera_e=camera_g+5
cut_e=F(182,30);cut_g=cut_e-5;rendered_g=F(1067,1000)
lead=contact_w-camera_w;quant_error=cut_e-contact_e
results={'basis':'planned user inputs only; no H3 invocation or media measurement','events':{'contactA':{k:data(v) for k,v in [('source',contact_s),('work',contact_w),('generation',contact_g),('edit',contact_e)]},'cameraReadyA':{k:data(v) for k,v in [('source',camera_s),('work',camera_w),('generation',camera_g),('edit',camera_e)]}},'camera_lead':{'actual':data(lead),'minimum':data(F(1,5)),'margin':data(lead-F(1,5)),'passes':lead>=F(1,5)},'cut':{'edit_frame_zero_based':182,'edit_time':data(cut_e),'generation_time':data(cut_g),'work_time':data(cut_g+10),'error':data(quant_error),'tolerance':data(F(1,200)),'margin':data(F(1,200)-quant_error),'first_frame_not_before_contact':F(181,30)<contact_e<=cut_e,'within_tolerance':abs(quant_error)<=F(1,200)},'m11':{'timestamp':'At 00:01.067','generation_seconds':data(rendered_g),'format_error':data(rendered_g-cut_g),'combined_contact_to_cut_seconds':data(rendered_g-contact_g),'still_after_contact':rendered_g>=contact_g,'combined_error_within_005':rendered_g-contact_g<=F(1,200)},'generation_fps':'unknown','generation_frame_index':'not computed'}
save('results.json',results)
assert lead>=F(1,5) and F(181,30)<contact_e<=cut_e and abs(quant_error)<=F(1,200)
assert rendered_g>=contact_g and rendered_g-contact_g<=F(1,200)
print('INDEPENDENT_EXACT_CHECKS_PASS; calls =',len(commands))
