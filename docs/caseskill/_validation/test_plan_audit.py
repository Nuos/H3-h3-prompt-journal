"""Regression checks for concrete risks in the case collection's plan auditor.

Run with: python3 -m unittest discover -s docs/caseskill/_validation -p 'test_*.py' -v
This checks tooling behavior; it is not a video-generation benchmark.
"""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
if (HERE / 'audit_plan.py').is_file():
    AUDITOR = HERE / 'audit_plan.py'
else:
    AUDITOR = next(HERE.parent.glob('h3-*/scripts/audit_plan.py'))
spec = importlib.util.spec_from_file_location('case_plan_auditor', AUDITOR)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
CONTRACT = {'case_id': 'fixture', 'required_check_ids': ['TIMING', 'STATE']}


def baseline():
    return {
        'schema_version': '1.0', 'case_id': 'fixture', 'delivery_kind': 'prompts',
        'status': 'ready', 'assembly': 'sequential', 'runtime': {'profile': 'official-2026-10-28'},
        'fps': 24, 'assets': [], 'references': [], 'unresolved': [], 'handoffs': [],
        'case_checks': [{'id': k, 'status': 'pass', 'evidence': 'Fixture review only; no inference claim.'} for k in CONTRACT['required_check_ids']],
        'segments': [{'id': 'SEG01', 'mode': 'T2VA', 'duration_s': 8, 'global_start_s': 0,
                      'reference_labels': [], 'prompt_file': 'SEG01.txt',
                      'shots': [{'id': 1, 'start_s': 0, 'end_s': 8,
                                 'action': 'The dancer shifts weight to the left foot.',
                                 'camera': 'A static full-body view.', 'sound': 'Cloth and footsteps.'}]}]
    }


BASE_PROMPT = '''integrated_multimodal_description: [Shot 1] Live-action, a full-body static view shows the dancer shifting weight to the left foot, lowering both hands and stopping in balance.

overall_soundscape: Cloth rustles and the shoes touch the floor.

non_diegetic_music: N/A
'''


class PlanAuditRegression(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'SEG01.txt').write_text(BASE_PROMPT, encoding='utf-8')

    def tearDown(self):
        self.temp.cleanup()

    def run_audit(self, plan=None, files=False):
        return module.audit(plan or baseline(), self.root, CONTRACT, strict=True, check_files=files)

    def assert_error(self, result, fragment):
        self.assertTrue(any(fragment in message for message in result['errors']), result)

    def test_complete_plan_and_three_field_prompt(self):
        self.assertEqual(self.run_audit(files=True)['errors'], [])

    def test_empty_template_cannot_be_ready(self):
        p = baseline()
        p.update(status='draft', segments=[], unresolved=['audio not supplied'])
        p['case_checks'][0]['status'] = 'unverified'
        result = self.run_audit(p)
        self.assert_error(result, 'status=ready')
        self.assert_error(result, 'Unresolved')
        self.assert_error(result, 'has not been performed')

    def test_timing_gap_from_inconsistent_dance_blocks(self):
        p = baseline()
        shot = copy.deepcopy(p['segments'][0]['shots'][0])
        p['segments'][0]['shots'][0]['end_s'] = 3.5
        shot.update(id=2, start_s=3.75, end_s=8)
        p['segments'][0]['shots'].append(shot)
        self.assert_error(self.run_audit(p), 'gap or overlap')

    def test_duration_and_frame_count_mismatch(self):
        p = baseline()
        p['segments'][0]['frame_count'] = 226
        self.assert_error(self.run_audit(p), 'frame_count')

    def test_long_case_requires_generation_slices(self):
        p = baseline()
        p['segments'][0].update(duration_s=30)
        p['segments'][0]['shots'][0]['end_s'] = 30
        self.assert_error(self.run_audit(p), 'outside the selected runtime')

    def test_custom_runtime_requires_evidence(self):
        p = baseline()
        p['runtime'] = {'profile': 'verified-custom', 'min_duration_s': 4, 'max_duration_s': 30, 'fps': 24, 'evidence': ''}
        self.assert_error(self.run_audit(p), 'capability evidence')
        p['runtime']['evidence'] = 'Fixture capability record, not a claim about any deployed runtime.'
        self.assertEqual(self.run_audit(p)['errors'], [])

    def test_missing_first_frame_and_wrong_picture_binding(self):
        p = baseline()
        s = p['segments'][0]
        s.update(mode='I2VA', first_frame_asset_id='a', reference_labels=['<Picture 1>'])
        p['assets'] = [{'id': x, 'kind': 'image', 'status': 'provided', 'locator': x+'.png', 'roles': ['frame']} for x in ['a', 'b']]
        p['references'] = [{'label': '<Picture 1>', 'asset_ids': ['b'], 'role': 'first frame'}]
        self.assert_error(self.run_audit(p), 'actual keyframe')
        p['references'][0]['asset_ids'] = ['a']
        (self.root / 'SEG01.txt').write_text('For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\n'+BASE_PROMPT, encoding='utf-8')
        self.assertEqual(self.run_audit(p, files=True)['errors'], [])

    def test_video_sound_is_not_automatically_an_audio_reference(self):
        p = baseline()
        p['assets'] = [{'id': 'clip', 'kind': 'video', 'status': 'provided', 'locator': 'clip.mp4', 'duration_s': 8, 'roles': ['motion'], 'audio_enabled': False}]
        p['references'] = [{'label': '<Audio 1>', 'asset_ids': ['clip'], 'role': 'beats'}]
        p['segments'][0].update(mode='Ref2VA', reference_labels=['<Audio 1>'])
        self.assert_error(self.run_audit(p), 'enable the source video')

    def test_ref2va_rejects_base_mode_field(self):
        p = baseline()
        p['assets'] = [{'id': 'portrait', 'kind': 'image', 'status': 'provided', 'locator': 'portrait.png', 'roles': ['identity']}]
        p['references'] = [{'label': '<Subject 1>', 'asset_ids': ['portrait'], 'role': 'dancer identity'}]
        p['segments'][0].update(mode='Ref2VA', reference_labels=['<Subject 1>'])
        self.assert_error(self.run_audit(p, files=True), 'official fields')

    def test_ref2va_accepts_six_fields_and_source_only_picture(self):
        p = baseline()
        p['assets'] = [{'id': 'portrait', 'kind': 'image', 'status': 'provided', 'locator': 'portrait.png', 'roles': ['identity']}]
        p['references'] = [{'label': '<Subject 1>', 'asset_ids': ['portrait'], 'role': 'dancer identity'}, {'label': '<Picture 1>', 'asset_ids': ['portrait'], 'role': 'source only', 'standalone': False}]
        p['segments'][0].update(mode='Ref2VA', reference_labels=['<Subject 1>', '<Picture 1>'])
        text = '''subject_definitions: <Subject 1> is the dancer whose identity comes from <Picture 1>.
summary: [reference generation] <Subject 1> performs a weight shift.
retention_analysis: <Subject 1> (appears in [Shot 1]): fully_preserved - retain the dancer's identity.
detailed_description: The target is a live-action rehearsal recording. [Shot 1] <Subject 1> shifts onto the left foot, lowers both hands and stops in balance while the camera stays at chest height in a full-body view.
overall_soundscape: Shoes touch the floor.
non_diegetic_music: N/A
'''
        (self.root / 'SEG01.txt').write_text(text, encoding='utf-8')
        self.assertEqual(self.run_audit(p, files=True)['errors'], [])

    def test_per_generation_reference_limits_not_whole_project(self):
        p = baseline()
        s2 = copy.deepcopy(p['segments'][0])
        s2.update(id='SEG02', global_start_s=8, prompt_file='SEG02.txt')
        p['segments'].append(s2)
        for n, s in enumerate(p['segments']):
            s.update(mode='Ref2VA', reference_labels=[])
            for i in range(7):
                idx = n*7+i+1
                aid, label = f'a{idx}', f'<Subject {idx}>'
                p['assets'].append({'id':aid,'kind':'image','status':'provided','locator':aid+'.png','roles':['identity']})
                p['references'].append({'label':label,'asset_ids':[aid],'role':'identity'})
                s['reference_labels'].append(label)
        p['handoffs'] = [{'from':'SEG01','to':'SEG02','type':'hard_cut','evidence':'Separate scene established.', 'audio_strategy':'silent'}]
        self.assertEqual(self.run_audit(p)['errors'], [])

    def test_unknown_reference_and_more_than_nine_images(self):
        p = baseline()
        p['segments'][0].update(mode='Ref2VA', reference_labels=['<Subject 99>'])
        self.assert_error(self.run_audit(p), 'undefined label')
        p['segments'][0]['reference_labels'] = []
        for i in range(10):
            aid, label = f'a{i}', f'<Subject {i+1}>'
            p['assets'].append({'id':aid,'kind':'image','status':'provided','locator':aid+'.png','roles':['identity']})
            p['references'].append({'label':label,'asset_ids':[aid],'role':'identity'})
            p['segments'][0]['reference_labels'].append(label)
        self.assert_error(self.run_audit(p), 'too many image')

    def test_multi_segment_requires_state_and_audio_handoff(self):
        p = baseline()
        s2 = copy.deepcopy(p['segments'][0])
        s2.update(id='SEG02', global_start_s=8)
        p['segments'].append(s2)
        self.assert_error(self.run_audit(p), 'Handoff records')

    def test_short_edit_uses_legal_generation_and_crop_timeline(self):
        p = baseline()
        p['edit_fps'] = 30
        first = p['segments'][0]
        first.update(duration_s=4, edit_window_s=[0,3], edit_duration_s=3)
        first['shots'][0]['end_s'] = 4
        second = copy.deepcopy(first)
        second.update(id='SEG02', global_start_s=3)
        p['segments'].append(second)
        p['handoffs'] = [{'from':'SEG01','to':'SEG02','type':'hard_cut','evidence':'Crop-end pose cuts to next entry; independently reviewed.', 'audio_strategy':'master track in edit'}]
        self.assertEqual(self.run_audit(p)['errors'], [])

    def test_crop_cannot_claim_unavailable_generated_frames(self):
        p = baseline()
        p['segments'][0]['edit_window_s'] = [5,9]
        self.assert_error(self.run_audit(p), 'outside the generated clip')

    def test_postproduction_freeze_additions_have_separate_time_budget(self):
        p = baseline()
        s = p['segments'][0]
        s.update(duration_s=14,edit_window_s=[0,13.5],edit_duration_s=15)
        s['shots'][0]['end_s'] = 14
        s['edit_holds'] = [{'at_s':t,'duration_s':0.5,'evidence':'Selected visible reaction frame in the cropped clip.'} for t in [3,7,10]]
        self.assertEqual(self.run_audit(p)['errors'], [])

    def test_postproduction_freeze_outside_usable_clip_is_rejected(self):
        p = baseline()
        p['segments'][0]['edit_holds'] = [{'at_s':9,'duration_s':0.5,'evidence':'A frame outside the available clip.'}]
        self.assert_error(self.run_audit(p), 'freeze positions')

    def test_prompt_cut_must_match_plan(self):
        p = baseline()
        s = p['segments'][0]
        s['shots'][0]['end_s'] = 4
        second = copy.deepcopy(s['shots'][0])
        second.update(id=2, start_s=4, end_s=8)
        s['shots'].append(second)
        text = BASE_PROMPT.replace('\n\noverall_soundscape:', ' [Shot 2] At 00:04.200, the camera cuts to the dancer standing in balance.\n\noverall_soundscape:')
        (self.root / 'SEG01.txt').write_text(text, encoding='utf-8')
        self.assert_error(self.run_audit(p, files=True), 'cut time disagrees')

    def test_nonfinite_time_rejected(self):
        p = baseline()
        p['segments'][0]['duration_s'] = float('nan')
        self.assert_error(self.run_audit(p), 'finite duration')

    def test_component_output_does_not_need_fake_generation(self):
        p = baseline()
        p.update(delivery_kind='component', assembly='component', segments=[])
        self.assertEqual(self.run_audit(p, files=True)['errors'], [])

    def test_prompt_file_cannot_escape_task_directory(self):
        p = baseline()
        p['segments'][0]['prompt_file'] = '../outside.txt'
        self.assert_error(self.run_audit(p, files=True), 'stay inside')


if __name__ == '__main__':
    unittest.main()
