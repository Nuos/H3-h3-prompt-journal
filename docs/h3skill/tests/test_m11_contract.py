"""M11 behavioral regressions; fixtures are engineering examples, not H3 execution proof.

These tests exercise the public request/proposal API and externally observable
invariants.  They deliberately do not duplicate compiler or schema algorithms.
"""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


sys.dont_write_bytecode = True
PACKAGE = Path(__file__).resolve().parents[1] / 'h3-model-protocol'
EXAMPLES = PACKAGE / 'assets/examples'
SCRIPT = PACKAGE / 'scripts/m11_contract.py'
SPEC = importlib.util.spec_from_file_location('m11_contract_under_test', SCRIPT)
m11 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m11)
PARTITIONS = {
    'M11.1': 'capability_profile',
    'M11.2': 'reference_binding',
    'M11.3': 'prompt_compilation',
    'M11.4': 'task_export',
}
MODES = ('T2VA', 'I2VA', 'FL2VA', 'L2VA', 'Ref2VA')
BASE_FIELDS = ['integrated_multimodal_description', 'overall_soundscape', 'non_diegetic_music']
REF_FIELDS = ['subject_definitions', 'summary', 'retention_analysis', 'detailed_description',
              'overall_soundscape', 'non_diegetic_music']


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


class M11ContractTests(unittest.TestCase):
    def requests(self):
        value = read(EXAMPLES / 'requests.json')
        return value if isinstance(value, list) else value['requests']

    def request(self, stage):
        return next(r for r in self.requests() if r['target'] == f'M11.{stage}')

    def mode_request(self, mode):
        return read(EXAMPLES / f'{mode.lower()}-request.json')

    def binding_request(self, mode):
        request = self.mode_request(mode)
        request['target'] = 'M11.2'
        request['request_id'] += '_binding_audit'
        request['inputs'] = deepcopy(request['inputs']['binding']['declarations'])
        return request

    def rebind(self, compilation_request):
        request = deepcopy(compilation_request)
        request['target'] = 'M11.2'
        request['request_id'] += '_rebind'
        request['inputs'] = deepcopy(compilation_request['inputs']['binding']['declarations'])
        compilation_request['inputs']['binding'] = self.proposal_result(request)
        return compilation_request

    def export_with_profile(self, profile):
        request = self.request(4)
        compile_request = deepcopy(request)
        compile_request['target'] = 'M11.3'
        compile_request['request_id'] += '_recompile'
        compile_request['inputs'] = deepcopy(request['inputs']['compilation']['declarations'])
        compile_request['inputs']['binding']['declarations']['capability_profile'] = deepcopy(profile)
        self.rebind(compile_request)
        request['inputs']['compilation'] = self.proposal_result(compile_request)
        request['inputs']['capability_profile'] = deepcopy(profile)
        return request

    def empty(self):
        return read(EXAMPLES / 'state-empty.json')

    def proposals(self, requests):
        return [m11.propose(request) for request in requests]

    def accepted(self):
        requests = self.requests()
        result = m11.accept(self.proposals(requests), requests, self.empty())
        self.assertEqual(result['status'], 'passed_with_unverified', result)
        return result['state']

    def reject(self, function, *args):
        """Rejection must be a controlled domain error and must not mutate inputs."""
        snapshot = deepcopy(args)
        original_json = json.dumps(args, ensure_ascii=False, sort_keys=True, allow_nan=False)
        with self.assertRaises(m11.ContractError) as caught:
            function(*args)
        self.assertEqual(args, snapshot, 'A rejected operation changed caller-owned input')
        self.assertEqual(json.dumps(args, ensure_ascii=False, sort_keys=True, allow_nan=False), original_json,
                         'Rejected input changed a JSON value or its type')
        self.assertTrue(caught.exception.code)
        return caught.exception

    def proposal_result(self, request):
        proposal = m11.propose(request)
        return proposal['changes'][PARTITIONS[request['target']]]

    def revision(self, request, version=1, suffix='revision'):
        request['base_version'] = version
        request['request_id'] += '_' + suffix
        return request

    def test_each_child_routes_without_invoking_other_modules(self):
        for request in self.requests():
            with self.subTest(stage=request['target']):
                snapshot = deepcopy(request)
                result = m11.route(request)
                self.assertEqual(result['status'], 'ready', result)
                self.assertEqual(result['invocation_status'], 'not_invoked')
                self.assertEqual([item['target'] for item in result['invocations']], [request['target']])
                self.assertEqual(request, snapshot)

    def test_router_requires_the_selected_childs_minimum_input(self):
        for request in self.requests():
            with self.subTest(stage=request['target']):
                request['inputs'] = {}
                self.reject(m11.route, request)

    def test_each_child_can_be_proposed_checked_and_accepted_alone(self):
        for request in self.requests():
            with self.subTest(stage=request['target']):
                initial = self.empty()
                snapshot = deepcopy((request, initial))
                proposal = m11.propose(request)
                self.assertEqual(set(proposal['changes']), {PARTITIONS[request['target']]})
                checked = m11.check(proposal, request)
                self.assertTrue(checked['valid'], checked)
                result = m11.accept(proposal, request, initial)
                self.assertEqual(result['status'], 'passed_with_unverified', result)
                self.assertEqual(set(result['state']['content']), {PARTITIONS[request['target']]})
                self.assertIn(result['state']['status'], ('draft', 'partial'))
                self.assertIn('h3_inference', result['not_run'])
                self.assertEqual((request, initial), snapshot)

    def test_atomic_batch_stays_unexecuted_and_exact_retry_preserves_state(self):
        requests = self.requests()
        proposals = self.proposals(requests)
        initial = self.empty()
        snapshot = deepcopy((requests, proposals, initial))
        result = m11.accept(proposals, requests, initial)
        self.assertEqual(result['status'], 'passed_with_unverified', result)
        self.assertEqual(result['state']['version'], 1)
        self.assertIn(result['state']['status'], ('draft', 'compiled_unexecuted'))
        self.assertIn('workflow_execution', result['not_run'])
        self.assertIn('h3_inference', result['not_run'])
        self.assertEqual(set(result['state']['content']), set(PARTITIONS.values()))
        self.assertEqual(len(result['state']['receipts']), 4)
        retry = m11.accept(proposals, requests, result['state'])
        self.assertTrue(retry['idempotent'])
        self.assertEqual(retry['state'], result['state'])
        self.assertEqual((requests, proposals, initial), snapshot)

    def test_original_request_cannot_be_replaced_by_proposal_self_claims(self):
        request = self.request(1)
        original = deepcopy(request)
        source = next(iter(request['sources']))
        request['sources'][source]['excerpt'] += ' Changed source assertion.'
        proposal = m11.propose(request)
        self.reject(m11.check, proposal, original)
        self.reject(m11.accept, proposal, original, self.empty())

    def test_proposal_context_and_source_tampering_is_rejected(self):
        for field in ('context', 'sources'):
            with self.subTest(field=field):
                request = self.request(1)
                proposal = m11.propose(request)
                if field == 'context':
                    proposal['context']['profile']['profile_id'] += '_other'
                else:
                    source = next(iter(proposal['sources']))
                    proposal['sources'][source]['version'] += '_other'
                self.reject(m11.check, proposal, request)

    def test_proposal_identity_and_version_bind_to_actual_request(self):
        changes = {'work_id': 'unrelated-work', 'source_request_id': 'other-request',
                   'proposal_id': 'unbound-self-assigned-proposal', 'base_version': 7,
                   'module_id': 'M11.4', 'contract_version': '9.0.0'}
        for field, value in changes.items():
            with self.subTest(field=field):
                request = self.request(1)
                proposal = m11.propose(request)
                proposal[field] = value
                self.reject(m11.check, proposal, request)
        request = self.request(1)
        proposal = m11.propose(request)
        proposal['base_version'] = False
        self.reject(m11.check, proposal, request)

    def test_child_cannot_write_another_partition_or_upstream_object(self):
        for key in ('prompt_compilation', 'WorkIntent', 'AssetRegistry', 'StateLedger'):
            with self.subTest(key=key):
                request = self.request(1)
                proposal = m11.propose(request)
                proposal['changes'][key] = {}
                self.reject(m11.check, proposal, request)
                self.reject(m11.accept, proposal, request, self.empty())

    def test_bad_last_child_cannot_partially_commit_a_batch(self):
        requests = self.requests()
        proposals = self.proposals(requests)
        proposals[-1]['changes']['reference_binding'] = {'injected': True}
        self.reject(m11.accept, proposals, requests, self.empty())

    def test_accept_requires_the_exact_original_request_set(self):
        requests = self.requests()
        proposals = self.proposals(requests)
        self.reject(m11.accept, proposals, requests[:-1], self.empty())
        self.reject(m11.accept, proposals[:-1], requests, self.empty())
        self.reject(m11.accept, proposals + [deepcopy(proposals[0])], requests, self.empty())

    def test_duplicate_owner_partition_is_not_last_writer_wins(self):
        request = self.request(1)
        second = deepcopy(request)
        second['request_id'] += '_second_writer'
        self.reject(m11.accept, [m11.propose(request), m11.propose(second)], [request, second], self.empty())

    def test_unknown_contract_route_and_boolean_versions_are_rejected(self):
        for field, value in (('contract_version', '2.0.0'), ('route_version', '2.0.0'),
                             ('base_version', True), ('base_version', -1), ('request_id', '  ')):
            with self.subTest(field=field, value=value):
                request = self.request(1)
                request[field] = value
                self.reject(m11.propose, request)

    def test_stale_base_is_rejected_for_a_new_request(self):
        state = self.accepted()
        request = self.request(1)
        request['request_id'] += '_new_but_stale'
        self.reject(m11.accept, m11.propose(request), request, state)

    def test_reusing_a_request_id_does_not_authorize_a_new_revision(self):
        state = self.accepted()
        request = self.request(1)
        request['base_version'] = 1
        self.reject(m11.accept, m11.propose(request), request, state)

    def test_retry_and_new_work_cannot_be_mixed_in_one_batch(self):
        state = self.accepted()
        requests = self.requests()
        self.revision(requests[0])
        self.reject(m11.accept, self.proposals(requests), requests, state)

    def test_same_source_id_and_version_cannot_silently_change_text(self):
        state = self.accepted()
        request = self.revision(self.request(1))
        source = next(iter(request['sources']))
        request['sources'][source]['excerpt'] += ' A changed fact under the old version.'
        self.reject(m11.accept, m11.propose(request), request, state)

    def test_hand_editing_an_accepted_partition_invalidates_receipts(self):
        for edit_context_too in (False, True):
            with self.subTest(edit_context_too=edit_context_too):
                state = self.accepted()
                if edit_context_too:
                    context = state['contexts']['capability_profile']
                    context['inputs']['profile']['profile_id'] += '_tampered'
                    state['content']['capability_profile'] = self.proposal_result(context)
                else:
                    state['content']['capability_profile']['profile_id'] += '_tampered'
                request = self.request(1)
                self.reject(m11.accept, m11.propose(request), request, state)

    def test_receipts_prevent_deleting_accepted_partition_and_original_context(self):
        for hide_as_partial in (False, True):
            with self.subTest(hide_as_partial=hide_as_partial):
                state = self.accepted()
                del state['content']['reference_binding']
                del state['contexts']['reference_binding']
                if hide_as_partial:
                    state['status'] = 'partial'
                request = self.request(1)
                self.reject(m11.accept, m11.propose(request), request, state)

    def test_profile_change_invalidates_its_actual_downstream_consumers(self):
        state = self.accepted()
        request = self.revision(self.request(1))
        profile = request['inputs']['profile']
        profile.pop('profile_digest', None)
        profile['model']['version'] += '-revision'
        result = m11.accept(m11.propose(request), request, state)
        self.assertEqual(set(result['state']['stale_modules']), {'M11.2', 'M11.3', 'M11.4'})

    def test_binding_change_invalidates_compilation_and_export_transitively(self):
        state = self.accepted()
        request = self.revision(self.request(2))
        request['inputs']['plan']['shots'][1]['start_ms'] = 4200
        result = m11.accept(m11.propose(request), request, state)
        self.assertEqual(set(result['state']['stale_modules']), {'M11.3', 'M11.4'})
        self.assertEqual(result['state']['content']['capability_profile'], state['content']['capability_profile'])

    def test_stale_compilation_cannot_be_reexported_before_revalidation(self):
        state = self.accepted()
        request = self.revision(self.request(2))
        request['inputs']['plan']['shots'][1]['start_ms'] = 4200
        changed = m11.accept(m11.propose(request), request, state)['state']
        export = self.revision(self.request(4), changed['version'])
        self.reject(m11.accept, m11.propose(export), export, changed)

    def test_clearing_stale_flags_cannot_revalidate_old_dependencies(self):
        state = self.accepted()
        request = self.revision(self.request(2))
        request['inputs']['plan']['shots'][1]['start_ms'] = 4200
        changed = m11.accept(m11.propose(request), request, state)['state']
        changed['stale_modules'] = []
        original = self.request(1)
        self.reject(m11.accept, m11.propose(original), original, changed)

    def test_unused_source_change_does_not_stale_unrelated_partitions(self):
        requests = self.requests()
        for request in requests:
            request['sources']['unused-note'] = {'kind': 'simulation', 'locator': 'fixture://unused-note',
                                                 'version': '1', 'excerpt': 'Not consumed by any partition.'}
        state = m11.accept(self.proposals(requests), requests, self.empty())['state']
        request = self.revision(deepcopy(requests[0]))
        request['sources']['unused-note'].update(version='2', excerpt='A display-only source note changed.')
        result = m11.accept(m11.propose(request), request, state)
        self.assertEqual(result['state']['stale_modules'], [])

    def test_batch_rejects_individually_valid_but_incompatible_sibling_snapshots(self):
        requests = self.requests()
        request = next(item for item in requests if item['target'] == 'M11.2')
        request['inputs']['plan']['shots'][1]['start_ms'] = 4200
        proposals = self.proposals(requests)
        for proposal, original in zip(proposals, requests):
            self.assertTrue(m11.check(proposal, original)['valid'])
        self.reject(m11.accept, proposals, requests, self.empty())

    def test_hand_editing_accepted_source_cannot_be_hidden_by_stale_flags(self):
        for hide_with_stale in (False, True):
            with self.subTest(hide_with_stale=hide_with_stale):
                state = self.accepted()
                source = next(iter(state['sources']))
                state['sources'][source]['excerpt'] += ' Not in any receipt.'
                if hide_with_stale:
                    state['stale_modules'] = list(PARTITIONS)
                    for consumer in state['consumers']:
                        if isinstance(consumer, dict):
                            consumer['status'] = 'stale'
                request = self.request(1)
                self.reject(m11.accept, m11.propose(request), request, state)

    def test_foreign_work_and_unknown_state_versions_are_not_accepted(self):
        for field, value in (('work_id', 'another-work'), ('contract_version', '2.0.0'),
                             ('version', True), ('owner', 'M9'), ('object_type', 'WorkIntent')):
            with self.subTest(field=field):
                state = self.empty()
                state[field] = value
                request = self.request(1)
                self.reject(m11.accept, m11.propose(request), request, state)

    def test_nonempty_unresolved_issues_cannot_self_certify_success(self):
        request = self.request(1)
        proposal = m11.propose(request)
        proposal['issues'] = [{'code': 'missing-deployment', 'owner': 'M11.1',
                               'message': 'No execution evidence is available.'}]
        self.reject(m11.check, proposal, request)

    def test_schema_errors_are_controlled_for_wrong_json_shapes(self):
        for bad in (None, [], True, 3, '', {'kind': 'M11Request'}):
            with self.subTest(bad=bad):
                self.reject(m11.propose, bad)

    def test_all_five_modes_compile_and_bind_to_their_original_requests(self):
        for mode in MODES:
            with self.subTest(mode=mode):
                request = self.mode_request(mode)
                snapshot = deepcopy(request)
                proposal = m11.propose(request)
                self.assertEqual(set(proposal['changes']), {'prompt_compilation'})
                self.assertTrue(m11.check(proposal, request)['valid'])
                self.assertEqual(request, snapshot)

    def test_exact_field_sets_style_position_and_local_shot_timestamps(self):
        for mode in MODES:
            with self.subTest(mode=mode):
                request = self.mode_request(mode)
                result = self.proposal_result(request)
                expected = REF_FIELDS if mode == 'Ref2VA' else BASE_FIELDS
                self.assertEqual(result['field_order'], expected)
                self.assertEqual(list(result['fields']), expected)
                body = result['fields']['detailed_description' if mode == 'Ref2VA'
                                        else 'integrated_multimodal_description']
                style = request['inputs']['fragments']['style']
                if mode == 'Ref2VA':
                    self.assertTrue(body.startswith(style + '\n\n[Shot 1] '), body)
                else:
                    self.assertTrue(body.startswith('[Shot 1] ' + style), body)
                self.assertNotIn('[Shot 1] At ', body)
                self.assertIn('[Shot 2] At 00:04.000, ', body)
                self.assertNotIn('{{', '\n'.join(result['fields'].values()))
                for metadata in ('contract_version:', 'profile_digest:', 'obligation_ids:'):
                    self.assertNotIn(metadata, '\n'.join(result['fields'].values()))

    def test_ref_summary_uses_official_bracketed_task_types(self):
        result = self.proposal_result(self.mode_request('Ref2VA'))
        summary = result['fields']['summary']
        self.assertTrue(summary.startswith('[reference generation + audio reuse + audio reference] '), summary)
        self.assertNotIn('Task types:', summary)
        self.assertNotIn('[video editing', summary)

    def test_keyframe_preambles_match_actual_shots_and_exact_end(self):
        for mode, expected in (
                ('I2VA', 'For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.'),
                ('L2VA', 'How the reference pictures align with the target video — <Picture 1> (from [Shot 2]) aligns with the 8.00-second mark of the target video.'),
                ('FL2VA', 'How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 2) aligns with the 8.00-second mark of the target video.')):
            with self.subTest(mode=mode):
                result = self.proposal_result(self.mode_request(mode))
                self.assertEqual(result['alignment_instruction'], expected)
                self.assertTrue(result['rendered_prompt'].startswith(expected + '\n\nintegrated_multimodal_description: '))
                self.assertTrue(result['fields']['integrated_multimodal_description'].startswith('[Shot 1] '))

    def test_t2va_and_ref2va_have_no_invented_keyframe_preamble(self):
        for mode in ('T2VA', 'Ref2VA'):
            with self.subTest(mode=mode):
                result = self.proposal_result(self.mode_request(mode))
                self.assertIsNone(result['alignment_instruction'])
                first = 'subject_definitions' if mode == 'Ref2VA' else 'integrated_multimodal_description'
                self.assertTrue(result['rendered_prompt'].startswith(first + ': '))

    def test_keyframe_end_precision_cannot_be_silently_rounded(self):
        for mode in ('L2VA', 'FL2VA'):
            with self.subTest(mode=mode):
                request = self.binding_request(mode)
                request['inputs']['plan']['duration_ms'] = 8001
                self.reject(m11.propose, request)

    def test_independent_reference_categories_do_not_define_speaker_identity(self):
        result = self.proposal_result(self.binding_request('Ref2VA'))
        self.assertEqual(result['labels']['subjects'], {'aria': '<Subject 1>', 'ben': '<Subject 2>'})
        self.assertEqual(result['labels']['speakers'], {'ben-voice': 'S1', 'aria-voice': 'S2'})
        self.assertEqual(result['labels']['assets']['camera-clip'], {'video': '<Video 1>', 'audio': '<Audio 2>'})
        self.assertEqual(result['labels']['assets']['music-bed'], {'audio': '<Audio 1>'})
        self.assertEqual(result['labels']['assets']['aria-photo'], {'image': '<Picture 1>'})

    def test_subject_identity_retention_is_not_weakened_by_a_new_background(self):
        result = self.proposal_result(self.mode_request('Ref2VA'))
        retention = result['fields']['retention_analysis']
        self.assertIn('<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved', retention)
        self.assertNotIn('(S1)', retention)
        self.assertNotIn('(S2)', retention)

    def test_multiple_subjects_can_come_from_the_same_asset(self):
        request = self.binding_request('Ref2VA')
        subject = deepcopy(request['inputs']['subjects'][0])
        subject.update(subject_id='coat', description='The woven texture of the coat only.',
                       retention_reason='Preserve the defined fabric texture only.')
        request['inputs']['subjects'].append(subject)
        result = self.proposal_result(request)
        self.assertEqual(result['labels']['subjects']['coat'], '<Subject 3>')
        self.assertEqual(result['labels']['assets']['aria-photo']['image'], '<Picture 1>')

    def test_subject_and_video_reference_cannot_escape_their_shot_scope(self):
        request = self.mode_request('Ref2VA')
        request['inputs']['binding']['declarations']['subjects'][0]['shot_ids'] = ['shot-open']
        self.rebind(request)
        self.reject(m11.propose, request)
        request = self.mode_request('Ref2VA')
        request['inputs']['fragments']['shots'][1]['text'] += ' The camera repeats {{ref:camera-clip.video}}.'
        self.reject(m11.propose, request)

    def test_unenabled_video_audio_is_not_inferred_from_the_video(self):
        request = self.binding_request('Ref2VA')
        video = next(asset for asset in request['inputs']['assets'] if asset['asset_id'] == 'camera-clip')
        video['enabled_audio'] = False
        self.reject(m11.propose, request)
        request['inputs']['audio_bindings'] = [item for item in request['inputs']['audio_bindings']
                                              if item['asset_id'] != 'camera-clip']
        result = self.proposal_result(request)
        self.assertEqual(result['labels']['assets']['camera-clip'], {'video': '<Video 1>'})
        self.assertEqual(len([item for item in result['media_inputs'] if item['channel'] == 'audio']), 1)

    def test_dual_channel_reference_needs_an_explicit_channel(self):
        request = self.mode_request('Ref2VA')
        fragment = request['inputs']['fragments']['shots'][0]
        fragment['text'] = fragment['text'].replace('{{ref:camera-clip.video}}', '{{ref:camera-clip}}')
        self.reject(m11.propose, request)

    def test_fully_copy_cannot_claim_a_modified_or_partial_final_soundtrack(self):
        for mutation in ('extra_layer', 'replaced_layer', 'source_window', 'target_window', 'partial_source'):
            with self.subTest(mutation=mutation):
                request = self.binding_request('Ref2VA')
                audio = request['inputs']['audio_bindings'][0]
                audio.update(retention='fully_copy', full_source=True, entire_soundtrack=True,
                             additional_layers=[], replaced_layers=[])
                if mutation == 'extra_layer':
                    audio['additional_layers'] = ['new-foley']
                elif mutation == 'replaced_layer':
                    audio['replaced_layers'] = ['source-voice']
                elif mutation == 'source_window':
                    audio['source_window_ms'] = [1000, 8000]
                elif mutation == 'target_window':
                    audio['target_window_ms'] = [1000, 8000]
                else:
                    audio['full_source'] = False
                self.reject(m11.propose, request)

    def test_exact_dialogue_and_visible_text_survive_compilation(self):
        request = self.mode_request('Ref2VA')
        result = self.proposal_result(request)
        body = result['fields']['detailed_description']
        self.assertIn('<Subject 2> (S1) says <d>[English] Fresh from the oven.</d>', body)
        self.assertIn('<Subject 1> (S2) says <d>[Chinese] 谢谢，闻起来真香。</d>', body)
        self.assertIn('"今日新鲜"', body)
        self.assertEqual(result['visible_text_trace'], request['inputs']['visible_text'])
        for field in ('overall_soundscape', 'non_diegetic_music'):
            self.assertNotIn('<d>', result['fields'][field])

    def test_dialogue_words_cannot_be_changed_under_a_punctuation_exception(self):
        request = self.mode_request('Ref2VA')
        utterance = request['inputs']['utterances'][0]
        utterance['text'] = 'Fresh from another oven.'
        utterance['punctuation_change'] = 'Punctuation-only normalization requested.'
        self.reject(m11.propose, request)

    def test_explicit_ref_punctuation_change_is_traced_but_base_text_stays_exact(self):
        request = self.mode_request('Ref2VA')
        utterance = request['inputs']['utterances'][0]
        utterance['text'] = utterance['text'].rstrip('.') + '!'
        utterance['punctuation_change'] = 'Authorized punctuation normalization in the synthetic request.'
        result = self.proposal_result(request)
        self.assertEqual(len(result['punctuation_trace']), 1)
        self.assertEqual(result['punctuation_trace'][0]['source_text'], 'Fresh from the oven.')
        request = self.mode_request('T2VA')
        request['inputs']['binding']['declarations']['speakers'] = [
            {'speaker_id': 'test-voice', 'first_vocal_ms': 1000, 'first_event_kind': 'speech',
             'source_refs': ['fixture-plan']}]
        self.rebind(request)
        shot = request['inputs']['fragments']['shots'][0]
        shot['text'] += ' A person ({{speaker:test-voice}}) says {{utterance:test-line}}.'
        request['inputs']['utterances'] = [{
            'utterance_id': 'test-line', 'speaker_id': 'test-voice', 'language': 'English',
            'text': 'Hello!', 'source_text': 'Hello.', 'start_ms': 1000, 'shot_id': shot['shot_id'],
            'punctuation_change': 'An exception cannot change Base dialogue.'}]
        self.assertEqual(self.reject(m11.propose, request).code, 'dialogue_fidelity')

    def test_visible_text_change_missing_dialogue_and_false_silence_are_rejected(self):
        for mutation in ('visible_text', 'missing_dialogue', 'false_silence', 'sound_na', 'music_na'):
            with self.subTest(mutation=mutation):
                request = self.mode_request('Ref2VA')
                if mutation == 'visible_text':
                    request['inputs']['visible_text'][0]['text'] = '昨日新鲜'
                elif mutation == 'missing_dialogue':
                    fragment = request['inputs']['fragments']['shots'][0]
                    fragment['text'] = fragment['text'].replace('{{utterance:ben-line}}', 'a greeting')
                elif mutation == 'false_silence':
                    request['inputs']['complete_silence'] = True
                elif mutation == 'sound_na':
                    request['inputs']['fragments']['overall_soundscape'] = 'N/A'
                else:
                    request['inputs']['fragments']['non_diegetic_music'] = 'N/A'
                self.reject(m11.propose, request)

    def test_unknown_runtime_allows_text_compilation_but_blocks_task_export(self):
        request = self.mode_request('Ref2VA')
        profile = request['inputs']['binding']['declarations']['capability_profile']
        self.assertEqual(profile['runtime'], {'status': 'unknown', 'execution': 'unknown'})
        self.assertEqual(self.proposal_result(request)['mode'], 'Ref2VA')
        export_request = self.export_with_profile(profile)
        error = self.reject(m11.propose, export_request)
        self.assertEqual(error.code, 'runtime_unknown')

    def test_simulated_export_keeps_simulation_status_and_explicit_parameters(self):
        result = self.proposal_result(self.request(4))
        self.assertEqual(result['execution'], 'simulation')
        self.assertEqual(result['status'], 'simulation_only')
        self.assertIn('workflow_execution', result['not_run'])
        self.assertIn('h3_inference', result['not_run'])
        payload = result['payload']['request']
        self.assertIsInstance(payload['prompt'], str)
        self.assertEqual(payload['prompt'], result['declarations']['compilation']['rendered_prompt'])
        self.assertEqual(payload['seconds'], 8)
        self.assertEqual((payload['width'], payload['height'], payload['fps']), (1280, 720, 24))
        self.assertEqual(set(payload), {'seconds', 'width', 'height', 'fps', 'mode', 'prompt', 'media'})
        self.assertEqual([item['input_index'] for item in payload['media']], [1, 2, 3, 4, 5])

    def test_simulation_evidence_cannot_be_promoted_to_production(self):
        request = self.request(1)
        request['inputs']['profile']['runtime']['execution'] = 'production'
        self.reject(m11.propose, request)

    def test_unknown_protocol_version_is_not_an_alias_for_the_pinned_protocol(self):
        request = self.request(1)
        request['inputs']['profile']['protocol_version'] = 'future-unreviewed-protocol'
        self.reject(m11.propose, request)

    def test_identity_source_picture_does_not_gain_a_standalone_frame_role(self):
        request = self.binding_request('Ref2VA')
        request['inputs']['reference_items'].append({
            'asset_id': 'aria-photo', 'description': 'Only the facial identity from this source photograph.',
            'retention': 'fully_preserved', 'retention_reason': 'Preserve the defined identity only.',
            'shot_ids': ['shot-open', 'shot-finish']})
        self.reject(m11.propose, request)

    def test_storyboard_reference_is_not_a_concrete_keyframe_anchor(self):
        request = self.binding_request('Ref2VA')
        request['inputs']['assets'].append({
            'asset_id': 'storyboard-sheet', 'version': 'fixture-v1', 'media_type': 'image',
            'uri': 'fixture://storyboard-sheet', 'purpose': 'storyboard', 'source_refs': ['fixture-plan']})
        request['inputs']['reference_items'].append({
            'asset_id': 'storyboard-sheet',
            'description': 'A storyboard indicating viewpoint, subject placement and shot order; it is not an actual target frame.',
            'retention': 'attribute_transfer', 'retention_reason': 'Use the declared storyboard layout only.',
            'shot_ids': ['shot-open', 'shot-finish']})
        result = self.proposal_result(request)
        self.assertIn('reference generation', result['task_types'])
        self.assertNotIn('keyframe completion', result['task_types'])

    def test_two_signals_cannot_both_be_the_complete_final_soundtrack(self):
        request = self.binding_request('Ref2VA')
        for audio in request['inputs']['audio_bindings']:
            audio.update(role='reuse', retention='fully_copy', full_source=True,
                         entire_soundtrack=True, additional_layers=[], replaced_layers=[])
        self.reject(m11.propose, request)

    def test_first_vocal_order_and_actual_dialogue_times_must_agree(self):
        request = self.mode_request('Ref2VA')
        declaration = request['inputs']['binding']['declarations']
        speaker = next(item for item in declaration['speakers'] if item['speaker_id'] == 'ben-voice')
        speaker['first_vocal_ms'] = 500
        self.rebind(request)
        # Ben's declared first event is speech, yet the only first utterance remains at 1000 ms.
        self.reject(m11.propose, request)
        request = self.mode_request('Ref2VA')
        request['inputs']['utterances'][0]['start_ms'] = 5000
        self.reject(m11.propose, request)

    def test_runtime_duration_dimensions_and_assets_must_match_compilation(self):
        for mutation in ('duration', 'unsupported_width', 'bool_fps', 'asset_version', 'missing_asset', 'extra_parameter'):
            with self.subTest(mutation=mutation):
                request = self.request(4)
                if mutation == 'duration':
                    request['inputs']['parameters']['duration_ms'] = 7000
                elif mutation == 'unsupported_width':
                    request['inputs']['parameters']['width'] = 1920
                elif mutation == 'bool_fps':
                    request['inputs']['parameters']['fps'] = True
                elif mutation == 'asset_version':
                    request['inputs']['asset_map']['aria-photo']['version'] = 'different'
                elif mutation == 'missing_asset':
                    del request['inputs']['asset_map']['aria-photo']
                else:
                    request['inputs']['parameters']['invented_seed'] = 1
                self.reject(m11.propose, request)

    def test_runtime_mapping_paths_require_evidence_and_cannot_overlap(self):
        for mutation in ('same_path', 'ancestor_path', 'missing_evidence'):
            with self.subTest(mutation=mutation):
                request = self.request(1)
                runtime = request['inputs']['profile']['runtime']
                if mutation == 'same_path':
                    runtime['mode']['path'] = runtime['prompt']['path']
                elif mutation == 'ancestor_path':
                    runtime['mode']['path'] = '/request'
                else:
                    runtime['mode']['evidence_refs'] = ['missing-source']
                self.reject(m11.propose, request)

    def test_backend_version_change_requires_recompilation_and_asset_rebinding(self):
        request = self.request(4)
        profile = request['inputs']['capability_profile']
        profile.pop('profile_digest', None)
        profile['model']['version'] += '-new'
        self.reject(m11.propose, request)
        request = self.request(4)
        request['inputs']['compilation']['fields']['detailed_description'] += ' An unreviewed extra event.'
        self.reject(m11.propose, request)

    def test_explicit_mode_conflicting_with_actual_asset_role_is_rejected(self):
        for mode, wrong in (('T2VA', 'I2VA'), ('I2VA', 'T2VA'), ('L2VA', 'I2VA'),
                            ('FL2VA', 'L2VA'), ('Ref2VA', 'T2VA')):
            with self.subTest(mode=mode, wrong=wrong):
                request = self.binding_request(mode)
                request['inputs']['plan']['requested_mode'] = wrong
                self.reject(m11.propose, request)

    def test_generation_local_timing_rejects_nonzero_origin_or_outside_cuts(self):
        for problem in ('first_not_zero', 'duplicate_cut', 'cut_at_end', 'zero_duration', 'bool_duration'):
            with self.subTest(problem=problem):
                request = self.binding_request('T2VA')
                plan = request['inputs']['plan']
                if problem == 'first_not_zero':
                    plan['shots'][0]['start_ms'] = 1
                elif problem in ('duplicate_cut', 'cut_at_end'):
                    plan['shots'].append({'shot_id': 'extra_shot',
                                          'start_ms': 0 if problem == 'duplicate_cut' else plan['duration_ms']})
                else:
                    plan['duration_ms'] = 0 if problem == 'zero_duration' else True
                self.reject(m11.propose, request)

    def test_missing_obligation_cannot_disappear_during_compilation(self):
        request = self.mode_request('T2VA')
        self.assertTrue(request['inputs']['obligations'], 'A meaningful fixture needs a preservation obligation')
        for fragment in request['inputs']['fragments']['shots']:
            fragment['obligation_ids'] = []
        self.reject(m11.propose, request)

    def test_unresolved_or_invented_reference_and_metadata_tokens_are_rejected(self):
        for text in (' {{ref:missing_stable_id}}', ' {{utterance:missing_line}}',
                     ' {{speaker:missing_voice}}', ' {{shot:missing_shot}}',
                     ' <Subject 999>', ' <Lighting 1>', ' {{TODO}}'):
            with self.subTest(text=text):
                request = self.mode_request('Ref2VA')
                request['inputs']['fragments']['shots'][0]['text'] += text
                self.reject(m11.propose, request)

    def test_shot_list_and_obligation_scope_cannot_change_by_body_layout(self):
        request = self.mode_request('T2VA')
        request['inputs']['fragments']['shots'][0]['shot_id'] = 'invented_shot'
        self.reject(m11.propose, request)
        request = self.mode_request('T2VA')
        request['inputs']['fragments']['shots'].append(deepcopy(request['inputs']['fragments']['shots'][0]))
        self.reject(m11.propose, request)

    def test_binding_digest_alone_cannot_authorize_mutated_upstream_content(self):
        request = self.mode_request('T2VA')
        request['inputs']['binding']['declarations']['plan']['duration_ms'] += 1000
        self.reject(m11.propose, request)
        request = self.mode_request('Ref2VA')
        request['sources']['fixture-plan']['version'] = 'changed-without-rebinding'
        self.reject(m11.propose, request)

    def test_cli_rejects_duplicate_keys_nonfinite_and_missing_original(self):
        with tempfile.TemporaryDirectory(prefix='m11-invalid-json-') as folder:
            path = Path(folder) / 'input.json'
            valid = json.dumps(self.request(1), ensure_ascii=False)
            # A permissive JSON parser would otherwise accept this complete request.
            duplicate = '{"kind":"M11Request",' + valid[1:]
            for content in (duplicate,
                            '{"value":NaN}', '{"value":Infinity}', '{"value":-Infinity}'):
                with self.subTest(content=content):
                    path.write_text(content, encoding='utf-8')
                    proc = subprocess.run([sys.executable, '-B', str(SCRIPT), 'propose', str(path)],
                                          capture_output=True, text=True)
                    self.assertEqual(proc.returncode, 2, proc)
                    result = json.loads(proc.stdout)
                    self.assertEqual(result['status'], 'fail')
                    self.assertNotIn('Traceback', proc.stderr)
                    self.assertEqual(path.read_text(encoding='utf-8'), content)
            request = self.request(1)
            path.write_text(json.dumps(m11.propose(request)), encoding='utf-8')
            proc = subprocess.run([sys.executable, '-B', str(SCRIPT), 'check', str(path)],
                                  capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)


    def test_fullcopy_can_retain_original_spoken_words_without_adding_a_layer(self):
        request = read(EXAMPLES / 'fullcopy-dialogue-request.json')
        result = self.proposal_result(request)
        self.assertIn('<Subject 1> (S1) says <d>[English] The bread is ready.</d> (copied from <Audio 1>)',
                      result['fields']['detailed_description'])
        self.assertIn('fully_copy', result['fields']['retention_analysis'])
        trace = result['utterance_source_trace'][0]
        self.assertEqual(trace['origin'], 'copied_audio')
        self.assertEqual(trace['audio_asset_id'], 'source-track')
        self.assertEqual(trace['audio_asset_version'], 'fixture-v1')
        self.assertEqual(trace['source_text'], 'The bread is ready.')
        self.assertEqual(trace['source_language'], 'English')
        self.assertEqual(trace['source_refs'], ['fixture-plan'])
        for field, text in result['fields'].items():
            if field != 'detailed_description':
                self.assertNotIn('The bread is ready.', text)
        checked = m11.check(m11.propose(request), request)
        self.assertTrue(checked['valid'])

    def test_fullcopy_still_rejects_newly_generated_or_reperformed_speech(self):
        request = read(EXAMPLES / 'fullcopy-dialogue-request.json')
        utterance = request['inputs']['utterances'][0]
        utterance['origin'] = 'generated'
        del utterance['audio_asset_id']
        error = self.reject(m11.propose, request)
        self.assertEqual(error.code, 'fully_copy_dialogue')

    def test_timbre_reference_cannot_self_certify_copied_words(self):
        request = read(EXAMPLES / 'fullcopy-dialogue-request.json')
        declarations = request['inputs']['binding']['declarations']
        declarations['assets'][0]['purpose'] = 'audio_reference'
        audio = declarations['audio_bindings'][0]
        audio.update(role='reference', retention='reference', full_source=False,
                     entire_soundtrack=False)
        self.rebind(request)
        error = self.reject(m11.propose, request)
        self.assertEqual(error.code, 'copied_dialogue_source')

    def test_copied_words_need_complete_explicit_source_declarations(self):
        for key in ('origin', 'audio_asset_id', 'source_text', 'source_language', 'source_refs'):
            with self.subTest(missing=key):
                request = read(EXAMPLES / 'fullcopy-dialogue-request.json')
                del request['inputs']['utterances'][0][key]
                self.reject(m11.propose, request)
        for key, value in (('audio_asset_id', 'unknown-signal'),
                           ('source_refs', ['unknown-source'])):
            with self.subTest(key=key):
                request = read(EXAMPLES / 'fullcopy-dialogue-request.json')
                request['inputs']['utterances'][0][key] = value
                self.reject(m11.propose, request)

    def test_copied_words_and_original_language_cannot_be_changed(self):
        for key, value in (('text', 'The cake is ready.'), ('source_language', 'Chinese')):
            with self.subTest(key=key):
                request = read(EXAMPLES / 'fullcopy-dialogue-request.json')
                utterance = request['inputs']['utterances'][0]
                utterance[key] = value
                if key == 'text':
                    utterance['punctuation_change'] = 'This cannot authorize changing a source word.'
                self.reject(m11.propose, request)

    def test_reused_bgm_verbal_cue_uses_audio_and_d_without_inventing_speaker(self):
        request = read(EXAMPLES / 'music-cue-request.json')
        result = self.proposal_result(request)
        self.assertEqual(request['inputs']['binding']['labels']['speakers'], {})
        self.assertIn('<Audio 1> reaches the phrase <d>[English] Morning light returns.</d>',
                      result['fields']['detailed_description'])
        self.assertNotRegex(result['rendered_prompt'], r'\bS\d+\b')
        self.assertEqual(result['utterance_source_trace'][0]['speaker_id'], None)
        self.assertEqual(result['utterance_source_trace'][0]['audio_asset_id'], 'music-track')
        for field, text in result['fields'].items():
            if field != 'detailed_description':
                self.assertNotIn('Morning light returns.', text)
                self.assertNotIn('<d>', text)

    def test_generated_words_cannot_use_the_speakerless_bgm_exception(self):
        request = read(EXAMPLES / 'music-cue-request.json')
        utterance = request['inputs']['utterances'][0]
        utterance['origin'] = 'generated'
        del utterance['audio_asset_id']
        error = self.reject(m11.propose, request)
        self.assertEqual(error.code, 'speaker_required')

    def test_a_concrete_bound_voice_cannot_be_erased_into_a_soundtrack_cue(self):
        request = read(EXAMPLES / 'fullcopy-dialogue-request.json')
        del request['inputs']['utterances'][0]['speaker_id']
        error = self.reject(m11.propose, request)
        self.assertEqual(error.code, 'copied_dialogue_speaker')

    def test_audio_definition_lyrics_entry_is_rejected_and_music_reference_imports_no_words(self):
        request = read(EXAMPLES / 'music-reference-request.json')
        result = self.proposal_result(request)
        self.assertEqual(request['inputs']['utterances'], [])
        self.assertNotIn('<d>', result['rendered_prompt'])
        binding_request = deepcopy(request)
        binding_request['target'] = 'M11.2'
        binding_request['inputs'] = deepcopy(request['inputs']['binding']['declarations'])
        binding_request['inputs']['audio_bindings'][0]['lyrics'] = 'Words outside the detailed timeline.'
        error = self.reject(m11.propose, binding_request)
        self.assertEqual(error.code, 'unknown_key')

    def test_verbal_markup_cannot_leak_into_summary_soundscape_or_reference_definitions(self):
        for destination in ('summary', 'overall_soundscape', 'definition', 'raw_d'):
            with self.subTest(destination=destination):
                request = read(EXAMPLES / 'music-cue-request.json')
                if destination == 'definition':
                    request['inputs']['binding']['declarations']['audio_bindings'][0]['description'] += ' {{utterance:song-cue}}'
                    self.rebind(request)
                elif destination == 'raw_d':
                    request['inputs']['fragments']['shots'][0]['text'] += ' <d>[English] Unbound words.</d>'
                else:
                    request['inputs']['fragments'][destination] += ' {{utterance:song-cue}}'
                error = self.reject(m11.propose, request)
                self.assertEqual(error.code, 'literal_control' if destination == 'raw_d' else 'utterance_placement')

    def test_short_words_shared_with_prose_and_visible_text_are_preserved(self):
        request = read(EXAMPLES / 'fullcopy-dialogue-request.json')
        utterance = request['inputs']['utterances'][0]
        utterance['text'] = utterance['source_text'] = 'No'
        request['inputs']['fragments']['overall_soundscape'] = 'No outdoor noise penetrates the quiet copied room tone.'
        request['inputs']['fragments']['shots'][0]['text'] += ' A wall card reads "No".'
        request['inputs']['visible_text'] = [{'text_id': 'wall-card', 'text': 'No', 'shot_id': 'shot-open'}]
        result = self.proposal_result(request)
        self.assertIn('<d>[English] No</d>', result['fields']['detailed_description'])
        self.assertIn('A wall card reads "No".', result['fields']['detailed_description'])
        self.assertEqual(result['fields']['overall_soundscape'], 'No outdoor noise penetrates the quiet copied room tone.')


if __name__ == '__main__':
    unittest.main()
