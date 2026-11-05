"""Behavioral regression tests for camera contracts; no H3 or media claims."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1] / 'h3-camera-visibility'
ASSETS = PACKAGE / 'assets'
spec = importlib.util.spec_from_file_location('m5_contract', PACKAGE / 'scripts/m5_contract.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
DEFS = m.load_json(PACKAGE / 'references/contracts.json')['$defs']


def fixture(name):
    return m.load_json(ASSETS / name)


def fresh():
    return fixture('state-empty.json'), fixture('proposal-batch.json'), fixture('requests.json')


def codes(check):
    return {d['code'] for d in check.diagnostics if d['blocking']}


class CameraContractTests(unittest.TestCase):
    def accepted(self):
        check = m.Check(DEFS)
        result = m.accept(check, *fresh())
        self.assertFalse(check.failed, check.diagnostics)
        return result['state']

    def check_proposal(self, number, mutate=None):
        p = fixture(f'proposal-m5-{number}.json')
        r = fixture(f'request-m5-{number}.json')
        if mutate:
            mutate(p, r)
        c = m.Check(DEFS)
        c.proposal(p, r)
        return c

    def revised(self, number=4):
        state = self.accepted()
        batch, requests = fresh()[1:]
        p, r = copy.deepcopy(batch['proposals'][number - 1]), copy.deepcopy(requests[number - 1])
        p.update(proposal_id='PROP-REVISION', source_request_id='REQ-REVISION', base_version=state['version'])
        r.update(request_id='REQ-REVISION', base_version=state['version'])
        batch.update(batch_id='BATCH-REVISION', base_version=state['version'], proposals=[p])
        return state, batch, [r]

    def test_four_standalone_children_accept_external_compatible_inputs(self):
        for number in range(1, 5):
            with self.subTest(child=number):
                r = fixture(f'request-standalone-m5-{number}.json')
                p = fixture(f'proposal-standalone-m5-{number}.json')
                state, batch, _ = fresh()
                batch['proposals'] = [p]
                c = m.Check(DEFS)
                result = m.accept(c, state, batch, [r])
                self.assertFalse(c.failed, c.diagnostics)
                self.assertEqual(result['state']['version'], 1)
                self.assertEqual([k for k, v in result['state']['content'].items() if v['items']], [m.OWNED[f'M5.{number}']])

    def test_combined_parent_accepts_one_atomic_revision_without_mutating_inputs(self):
        state, batch, requests = fresh()
        before = copy.deepcopy((state, batch, requests))
        c = m.Check(DEFS)
        result = m.accept(c, state, batch, requests)
        self.assertFalse(c.failed, c.diagnostics)
        self.assertEqual((state, batch, requests), before)
        self.assertEqual(result['state']['version'], 1)
        self.assertEqual(len(result['state']['accepted_proposals']), 4)
        self.assertTrue(all(result['state']['content'][part]['items'] for part in m.EMPTY))

    def test_minimum_inputs_are_not_silently_omitted(self):
        for number in range(1, 5):
            r = fixture(f'request-m5-{number}.json')
            for key in m.MINIMUM[r['target']]:
                with self.subTest(child=number, field=key):
                    bad = copy.deepcopy(r)
                    del bad['inputs'][key]
                    c = m.Check(DEFS)
                    c.request(bad)
                    self.assertIn('minimum_input_missing', codes(c))

    def test_explicit_unknown_context_allows_limited_standalone_check(self):
        r = fixture('request-minimal-m5-2.json')
        p = fixture('proposal-standalone-m5-2.json')
        p.update(source_request_id=r['request_id'], context=copy.deepcopy(r['inputs']))
        next(iter(p['changes']['framing']['items'].values()))['viewpoint_ref'] = {'state': 'unknown', 'reason': '尚未给出观察机位'}
        c = m.Check(DEFS)
        c.proposal(p, r)
        self.assertFalse(c.failed, c.diagnostics)
        self.assertIn('explicit_unknown', {d['code'] for d in c.diagnostics})

    def test_public_extra_fields_and_unsupported_versions_fail_closed(self):
        for mutate in [lambda p: p.update(absolute_time=1), lambda p: p.update(contract_version='2.0.0'), lambda p: p['changes']['focus']['items']['FC-HANDOFF'].update(aperture_fake=1)]:
            p = fixture('proposal-m5-3.json')
            mutate(p)
            c = m.Check(DEFS)
            c.proposal(p)
            self.assertIn('contract_shape', codes(c))

    def test_child_cannot_write_other_or_multiple_partitions(self):
        p = fixture('proposal-m5-1.json')
        p['changes'] = {'focus': fixture('proposal-m5-3.json')['changes']['focus']}
        c = m.Check(DEFS)
        c.proposal(p)
        self.assertIn('write_ownership', codes(c))
        p['changes']['viewpoints'] = fixture('proposal-m5-1.json')['changes']['viewpoints']
        c = m.Check(DEFS)
        c.proposal(p)
        self.assertIn('contract_shape', codes(c))

    def test_parent_is_not_a_child_proposal_owner(self):
        p = fixture('proposal-m5-1.json')
        p['module_id'] = 'M5'
        c = m.Check(DEFS)
        c.proposal(p)
        self.assertIn('contract_shape', codes(c))

    def test_original_request_required_for_accept_but_missing_check_is_unverified(self):
        state, batch, requests = fresh()
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests[:-1]))
        self.assertIn('original_request_required', codes(c))
        c = m.Check(DEFS)
        c.proposal(batch['proposals'][0])
        self.assertFalse(c.failed, c.diagnostics)
        self.assertIn('original_request_missing', {d['code'] for d in c.diagnostics})

    def test_actual_request_sources_context_and_target_are_bound(self):
        for field in ('source', 'context', 'target'):
            p, r = fixture('proposal-m5-1.json'), fixture('request-m5-1.json')
            if field == 'source':
                p['sources']['D-brief']['excerpt'] = '改写来源'
            elif field == 'context':
                p['context']['viewpoint_brief'] = '更换任务'
            else:
                r['target'] = 'M5.2'
            c = m.Check(DEFS)
            c.proposal(p, r)
            self.assertTrue(c.failed)
            self.assertTrue(codes(c) & {'request_fidelity', 'request_target'})

    def test_external_and_fact_payloads_are_opaque_but_envelope_is_checked(self):
        p, r = fixture('proposal-standalone-m5-2.json'), fixture('request-standalone-m5-2.json')
        p['changes']['framing']['items']['FR-HANDOFF']['composition']['value'] = {'state': 'unknown', 'source_refs': ['business-only-key'], 'source_id': 'business-id', 'value': True}
        c = m.Check(DEFS)
        c.proposal(p, r)
        self.assertFalse(c.failed, c.diagnostics)
        r['inputs']['viewpoint_context']['owner'] = 'M3'
        p['context'] = copy.deepcopy(r['inputs'])
        c = m.Check(DEFS)
        c.proposal(p, r)
        self.assertIn('context_owner', codes(c))

    def test_source_refs_and_external_source_versions_must_resolve(self):
        for mutate, expected in [(lambda p: p['changes']['viewpoints']['items']['VP-HANDOFF']['source_refs'].append('Missing'), 'unresolved_source'), (lambda p: p['context'].update(space_context={'owner': 'M3', 'source_id': 'D-brief', 'source_version': 'wrong-version', 'values': {}}), 'context_version')]:
            p = fixture('proposal-m5-1.json')
            mutate(p)
            c = m.Check(DEFS)
            c.proposal(p)
            self.assertIn(expected, codes(c))

    def test_batch_failure_is_atomic_and_state_stays_unchanged(self):
        state, batch, requests = fresh()
        original = copy.deepcopy(state)
        batch['proposals'][3]['changes']['movements']['items']['CE-CONTACT']['position_change'] = 'changed'
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('fixed_pose_change', codes(c))
        self.assertEqual(state, original)

    def test_conflicting_partition_writes_are_rejected(self):
        state, batch, requests = fresh()
        other = copy.deepcopy(batch['proposals'][0])
        other['proposal_id'] = 'PROP-OTHER'
        batch['proposals'].append(other)
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('partition_conflict', codes(c))

    def test_stale_base_versions_are_rejected(self):
        state, batch, requests = self.revised()
        batch['base_version'] = 0
        batch['proposals'][0]['base_version'] = 0
        requests[0]['base_version'] = 0
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('stale_base_version', codes(c))

    def test_exact_retry_is_idempotent_and_changed_payload_is_not(self):
        state = self.accepted()
        _, batch, requests = fresh()
        c = m.Check(DEFS)
        result = m.accept(c, state, batch, requests)
        self.assertFalse(c.failed, c.diagnostics)
        self.assertEqual(result['acceptance'], 'idempotent_replay')
        self.assertEqual(result['state'], state)
        batch['proposals'][0]['changes']['viewpoints']['items']['VP-HANDOFF']['position']['value'] = '另一机位'
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('idempotency_conflict', codes(c))

    def test_exact_retry_cannot_be_mixed_with_new_writes(self):
        state = self.accepted()
        _, batch, requests = fresh()
        batch['proposals'][0]['proposal_id'] = 'PROP-NEW'
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('mixed_replay', codes(c))

    def test_source_identity_cannot_be_rebound(self):
        state, batch, requests = self.revised(1)
        requests[0]['sources']['D-brief']['excerpt'] = '重绑定旧来源 ID'
        batch['proposals'][0]['sources'] = copy.deepcopy(requests[0]['sources'])
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('source_collision', codes(c))

    def test_readonly_context_must_equal_composed_candidate(self):
        state, batch, requests = fresh()
        requests[1]['inputs']['viewpoint_context']['items']['VP-HANDOFF']['position']['value'] = '只读内容被另一调用改变'
        batch['proposals'][1]['context'] = copy.deepcopy(requests[1]['inputs'])
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('readonly_conflict', codes(c))

    def test_readonly_projection_preserves_boolean_number_distinction(self):
        state, batch, requests = fresh()
        vp = batch['proposals'][0]['changes']['viewpoints']['items']['VP-HANDOFF']
        vp['roll']['value'] = True
        for index in (1, 3):
            requests[index]['inputs']['viewpoint_context']['items']['VP-HANDOFF']['roll']['value'] = True
            batch['proposals'][index]['context'] = copy.deepcopy(requests[index]['inputs'])
        projection = {'path': '/content/viewpoints/items/VP-HANDOFF/roll/value', 'source_version': 0, 'value': 1}
        requests[0]['inputs']['readonly_projection'] = [projection]
        batch['proposals'][0]['context'] = copy.deepcopy(requests[0]['inputs'])
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('readonly_conflict', codes(c))

    def test_projection_version_and_unresolved_path_fail(self):
        for projection, expected in [({'path': '/content/viewpoints', 'source_version': 99, 'value': {}}, 'projection_version'), ({'path': '/content/nonexistent', 'source_version': 0, 'value': {}}, 'projection_unresolved')]:
            state, batch, requests = fresh()
            requests[0]['inputs']['readonly_projection'] = [projection]
            batch['proposals'][0]['context'] = copy.deepcopy(requests[0]['inputs'])
            c = m.Check(DEFS)
            self.assertIsNone(m.accept(c, state, batch, requests))
            self.assertIn(expected, codes(c))

    def test_accepted_ids_cannot_be_deleted(self):
        state, batch, requests = self.revised(4)
        del batch['proposals'][0]['changes']['movements']['items']['CE-WATERLINE']
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('accepted_record_deleted', codes(c))

    def test_map_id_and_cross_shot_relations_are_checked(self):
        for mutate, expected in [(lambda p: p['changes']['framing']['items']['FR-HANDOFF'].update(framing_id='DIFFERENT'), 'record_identity'), (lambda p: p['changes']['framing']['items']['FR-HANDOFF'].update(shot_id='SHOT-OTHER'), 'cross_shot_reference')]:
            c = self.check_proposal(2, lambda p, r: mutate(p))
            self.assertIn(expected, codes(c))

    def test_dangling_internal_reference_fails_when_context_is_present(self):
        c = self.check_proposal(2, lambda p, r: p['changes']['framing']['items']['FR-HANDOFF']['viewpoint_ref'].update(id='VP-MISSING'))
        self.assertIn('dangling_reference', codes(c))

    def test_camera_and_action_event_ids_cannot_alias(self):
        p = fixture('proposal-m5-4.json')
        record = p['changes']['movements']['items'].pop('CE-HANDOFF')
        record['camera_event_id'] = 'AE-DANCE'
        p['changes']['movements']['items']['AE-DANCE'] = record
        c = m.Check(DEFS)
        c.proposal(p, fixture('request-m5-4.json'))
        self.assertIn('camera_action_identity', codes(c))

    def test_fixed_camera_does_not_require_subject_action_to_be_static(self):
        c = self.check_proposal(4)
        self.assertFalse(c.failed, c.diagnostics)
        for field in ('position_change', 'optical_axis_change', 'roll_change'):
            c = self.check_proposal(4, lambda p, r: p['changes']['movements']['items']['CE-CONTACT'].update({field: 'changed'}))
            self.assertIn('fixed_pose_change', codes(c))

    def test_unknown_fixed_pose_does_not_claim_verification(self):
        c = self.check_proposal(4, lambda p, r: p['changes']['movements']['items']['CE-CONTACT'].update(position_change='unknown'))
        self.assertFalse(c.failed, c.diagnostics)
        self.assertIn('fixed_pose_unknown', {d['code'] for d in c.diagnostics})

    def test_task_trigger_does_not_need_action_and_loop_endpoints_may_match(self):
        def change(p, r):
            record = p['changes']['movements']['items']['CE-WATERLINE']
            record['path_end'] = copy.deepcopy(record['path_start'])
            record['path_description']['value'] = '沿闭环观察路径返回起点'
        c = self.check_proposal(4, change)
        self.assertFalse(c.failed, c.diagnostics)

    def test_moving_trigger_cannot_be_not_applicable_but_can_be_unknown(self):
        c = self.check_proposal(4, lambda p, r: p['changes']['movements']['items']['CE-WATERLINE'].update(trigger={'state': 'not_applicable', 'reason': '缺少资料不能写成不适用'}))
        self.assertIn('movement_trigger_required', codes(c))
        c = self.check_proposal(4, lambda p, r: p['changes']['movements']['items']['CE-WATERLINE'].update(trigger={'state': 'unknown', 'reason': '等待任务开始条件'}))
        self.assertFalse(c.failed, c.diagnostics)

    def test_response_relation_requires_action_or_explicit_unknown(self):
        c = self.check_proposal(4, lambda p, r: p['changes']['movements']['items']['CE-WATERLINE'].update(coordination_strategy='ahead'))
        self.assertIn('action_relation_required', codes(c))
        c = self.check_proposal(4, lambda p, r: p['changes']['movements']['items']['CE-HANDOFF'].update(action_event_ref={'state': 'unknown', 'reason': '等待动作身份'}))
        self.assertFalse(c.failed, c.diagnostics)

    def test_optical_and_visibility_claims_remain_unverified(self):
        for number, part, ident, field in [(2, 'framing', 'FR-HANDOFF', 'visibility_assessment'), (3, 'focus', 'FC-HANDOFF', 'focus_assessment')]:
            c = self.check_proposal(number, lambda p, r: p['changes'][part]['items'][ident][field].update(state='verified'))
            self.assertIn('contract_shape', codes(c))
        c = self.check_proposal(3)
        self.assertFalse(c.failed, c.diagnostics)
        self.assertIn('focus_unverified', {d['code'] for d in c.diagnostics})

    def test_impact_uses_actual_paths_and_preserves_existing_staleness(self):
        before = self.accepted()
        before['display'] = {'title': '展示标题'}
        before['consumers'] = {
            'READ-FOCUS': {'module_id': 'M11', 'result_version': 1, 'source_state_version': 1, 'read_paths': ['/content/focus/items/FC-HANDOFF'], 'status': 'current'},
            'READ-VIEW': {'module_id': 'M3', 'result_version': 1, 'source_state_version': 1, 'read_paths': ['/content/viewpoints'], 'status': 'current'},
            'ALREADY': {'module_id': 'M12', 'result_version': 1, 'source_state_version': 1, 'read_paths': ['/sources'], 'status': 'stale'}}
        after = copy.deepcopy(before)
        after['display']['title'] = '另一标题'
        self.assertEqual(set(m.impact(before, after)['stale_consumers']), {'ALREADY'})
        after['content']['focus']['items']['FC-HANDOFF']['focus_target']['value'] = '交接后的道具'
        result = m.impact(before, after)
        self.assertEqual(set(result['stale_consumers']), {'READ-FOCUS', 'ALREADY'})
        self.assertFalse(result['stale_consumers']['ALREADY']['changed_paths'])

    def test_child_consumers_become_stale_only_when_their_declared_input_changes(self):
        state, batch, requests = self.revised(number=1)
        state['consumers'] = {
            'FRAME-RESULT': {'module_id': 'M5.2', 'result_version': 1, 'source_state_version': 1, 'read_paths': ['/content/viewpoints/items/VP-HANDOFF'], 'status': 'current'},
            'FOCUS-RESULT': {'module_id': 'M5.3', 'result_version': 1, 'source_state_version': 1, 'read_paths': ['/content/viewpoints/items/VP-HANDOFF'], 'status': 'current'},
            'MOVE-RESULT': {'module_id': 'M5.4', 'result_version': 1, 'source_state_version': 1, 'read_paths': ['/content/viewpoints/items/VP-HANDOFF'], 'status': 'current'},
            'OTHER-VIEW': {'module_id': 'M5.1', 'result_version': 1, 'source_state_version': 1, 'read_paths': ['/content/framing/items/FR-HANDOFF'], 'status': 'current'},
        }
        batch['proposals'][0]['changes']['viewpoints']['items']['VP-HANDOFF']['position']['value'] = '根据新观看要求移到柜台左侧；其余分区未改'
        c = m.Check(DEFS)
        result = m.accept(c, state, batch, requests)
        self.assertFalse(c.failed, c.diagnostics)
        self.assertEqual(set(result['impact']['stale_consumers']), {'FRAME-RESULT', 'FOCUS-RESULT', 'MOVE-RESULT'})
        self.assertTrue(all(result['state']['consumers'][ident]['status'] == 'stale' for ident in ('FRAME-RESULT', 'FOCUS-RESULT', 'MOVE-RESULT')))
        self.assertEqual(result['state']['consumers']['OTHER-VIEW']['status'], 'current')
        self.assertEqual(state['consumers']['FRAME-RESULT']['status'], 'current')

    def test_blocking_issue_requires_owned_evidenced_resolution(self):
        state, batch, requests = fresh()
        state['sources'] = copy.deepcopy(requests[0]['sources'])
        state['issues'] = {'ISSUE-1': {'issue_id': 'ISSUE-1', 'owner': 'M5.4', 'status': 'open', 'severity': 'blocking', 'message': '需要明确固定观察条件', 'source_refs': ['D-brief']}}
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('open_blocker', codes(c))
        resolution = {'issue_id': 'ISSUE-1', 'rationale': '已将固定观察的位移、光轴、滚转声明为不变化', 'source_refs': ['D-brief']}
        batch['proposals'][0]['resolutions'] = [resolution]
        c = m.Check(DEFS)
        self.assertIsNone(m.accept(c, state, batch, requests))
        self.assertIn('resolution_ownership', codes(c))
        batch['proposals'][0]['resolutions'] = []
        batch['proposals'][3]['resolutions'] = [resolution]
        c = m.Check(DEFS)
        result = m.accept(c, state, batch, requests)
        self.assertFalse(c.failed, c.diagnostics)
        self.assertEqual(result['state']['issues']['ISSUE-1']['status'], 'resolved')

    def test_strict_json_rejects_duplicates_nonfinite_and_overflow(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'bad.json'
            for raw in ('{"x": 1, "x": 2}', '{"x": NaN}', '{"x": Infinity}', '{"x": -Infinity}', '{"x": 1e999}'):
                p.write_text(raw)
                with self.assertRaises(ValueError):
                    m.load_json(p)

    def test_cli_four_commands_from_isolated_portable_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / 'skill'
            shutil.copytree(PACKAGE, package, ignore=shutil.ignore_patterns('__pycache__'))
            script = package / 'scripts/m5_contract.py'
            assets = package / 'assets'
            commands = [
                ['route', str(assets / 'request-m5.json')],
                ['check', str(assets / 'proposal-batch.json'), '--requests', str(assets / 'requests.json')],
                ['accept', str(assets / 'state-empty.json'), str(assets / 'proposal-batch.json'), '--requests', str(assets / 'requests.json')]]
            for command in commands:
                process = subprocess.run([sys.executable, str(script), *command], cwd=tmp, text=True, capture_output=True)
                self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
                result = json.loads(process.stdout)
                self.assertEqual(result['validation']['overall'], 'unverified')
                self.assertEqual(result['trace']['side_effects'], 'none')
                self.assertEqual(set(result['trace']['resources']), {'references/contracts.json', 'references/module-registry.json'})
                if command[0] == 'accept':
                    statefile = Path(tmp) / 'accepted.json'
                    statefile.write_text(json.dumps(result['state']))
            process = subprocess.run([sys.executable, str(script), 'impact', str(statefile), str(statefile)], cwd=tmp, text=True, capture_output=True)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            self.assertEqual(json.loads(process.stdout)['impact']['changed_paths'], [])

    def test_malformed_batch_is_structural_failure_without_trace_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'batch.json'
            for malformed in ([], 7, None, 'not-a-batch'):
                with self.subTest(batch=malformed):
                    path.write_text(json.dumps(malformed))
                    result = subprocess.run([sys.executable, str(PACKAGE / 'scripts/m5_contract.py'), 'accept', str(ASSETS / 'state-empty.json'), str(path), '--requests', str(ASSETS / 'requests.json')], text=True, capture_output=True)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    output = json.loads(result.stdout)
                    self.assertEqual(output['execution'], 'completed')
                    self.assertEqual(output['validation']['local_contract'], 'fail')
                    self.assertIsNone(output['trace']['operation_id'])
                    self.assertNotIn('state', output)

    def test_moving_endpoints_and_trigger_cannot_be_omitted(self):
        for field in ('path_start', 'path_end', 'trigger'):
            p = fixture('proposal-m5-4.json')
            del p['changes']['movements']['items']['CE-WATERLINE'][field]
            c = m.Check(DEFS)
            c.proposal(p, fixture('request-m5-4.json'))
            self.assertIn('contract_shape', codes(c))

    def test_cli_parse_errors_are_execution_errors_with_no_effects(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bad.json'
            path.write_text('{"kind":"M5State","kind":"M5Request"}')
            result = subprocess.run([sys.executable, str(PACKAGE / 'scripts/m5_contract.py'), 'check', str(path)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)['side_effects'], 'none')


if __name__ == '__main__':
    unittest.main()
