"""Regression tests for actual M9 ownership, relation, provenance and transaction risks."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2] / 'h3-shot-edit-generation'
spec = importlib.util.spec_from_file_location('m9_contract', ROOT / 'scripts/m9_contract.py')
m9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m9)


def fixture(name):
    return json.loads((ROOT / 'assets' / name).read_text(encoding='utf-8'))


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.requests = fixture('requests.json')
        self.proposals = fixture('proposal-batch.json')
        self.empty = fixture('state-empty.json')

    def req(self, index): return self.requests['requests'][index - 1]
    def prop(self, index): return self.proposals['proposals'][index - 1]
    def sync(self, index):
        self.prop(index)['context'] = deepcopy(self.req(index)['inputs'])
        self.prop(index)['sources'] = deepcopy(self.req(index)['sources'])
    def assertCode(self, errors, code):
        self.assertIn(code, [error['code'] for error in errors], errors)
    def accepted(self):
        out = m9.accept(self.empty, self.proposals, self.requests)
        self.assertEqual(out['status'], 'passed_with_unverified', out)
        return out['state']

    def test_three_modules_route_check_accept_independently(self):
        for i in range(1, 4):
            with self.subTest(module=i):
                self.assertTrue(m9.route(self.req(i))['ready'])
                self.assertEqual(m9.check(self.prop(i), self.req(i)), [])
                accepted = m9.accept(self.empty, self.prop(i), self.req(i))
                self.assertEqual(accepted['status'], 'passed_with_unverified', accepted)
                self.assertEqual(len(accepted['state']['content']), 1)
                self.assertEqual(m9.state_errors(accepted['state']), [])

    def test_batch_is_atomic_and_exact_retry_is_idempotent(self):
        state = self.accepted()
        self.assertEqual(state['version'], 1)
        self.assertEqual(m9.state_errors(state), [])
        again = m9.accept(state, self.proposals, self.requests)
        self.assertTrue(again['idempotent'])
        self.assertEqual(again['state'], state)
        self.prop(3)['changes']['GenerationPlan']['tasks'][0]['context']['scene'] = 'Changed'
        bad = m9.accept(state, self.proposals, self.requests)
        self.assertCode(bad['errors'], 'idempotency_conflict')
        self.assertNotIn('state', bad)
        self.assertEqual(state['version'], 1)

    def test_changed_actual_request_cannot_be_self_attested(self):
        self.prop(2)['context']['brief'] = 'A forged request copied into the proposal'
        self.assertCode(m9.check(self.prop(2), self.req(2)), 'original_request_mismatch')
        self.req(2)['inputs']['source_context']['source_version'] = 'missing-version'
        self.sync(2)
        self.assertCode(m9.check(self.prop(2), self.req(2)), 'source_version')

    def test_exclusive_partition_and_unknown_fields(self):
        self.prop(1)['changes']['EditGraph'] = self.prop(2)['changes']['EditGraph']
        self.assertCode(m9.check(self.prop(1), self.req(1)), 'schema')
        self.prop(1)['changes'].pop('EditGraph')
        self.prop(1)['changes']['ShotMap']['authoritative_timeline'] = []
        self.assertCode(m9.check(self.prop(1), self.req(1)), 'schema')

    def test_five_units_allow_shared_phase_multi_panel_and_many_to_many_tasks(self):
        data = self.prop(1)['changes']['ShotMap']
        self.assertIn('phase_turn', data['shots'][0]['phase_ids'])
        self.assertIn('phase_turn', data['shots'][1]['phase_ids'])
        self.assertEqual(len(data['shots'][0]['panel_ids']), 2)
        gen = self.prop(3)['changes']['GenerationPlan']
        self.assertEqual(gen['tasks'][1]['shot_ids'], ['shot_a', 'shot_b'])
        self.assertEqual(m9.check(self.prop(3), self.req(3)), [])

    def test_camera_motion_is_not_reclassified_as_cut(self):
        event = self.prop(1)['changes']['ShotMap']['events'][0]
        event['kind'] = 'cut'; event['to_shot'] = 'shot_b'
        self.assertCode(m9.check(self.prop(1), self.req(1)), 'camera_is_not_cut')

    def test_duplicate_ids_and_orphan_panels_fail(self):
        data = self.prop(1)['changes']['ShotMap']
        data['phases'].append(deepcopy(data['phases'][0]))
        self.assertCode(m9.check(self.prop(1), self.req(1)), 'duplicate_id')
        data['phases'].pop()
        data['panels'][0]['shot_id'] = 'missing_shot'
        self.assertCode(m9.check(self.prop(1), self.req(1)), 'orphan_panel')

    def test_window_bounds_coordinate_domains_and_source_evidence(self):
        window = self.prop(2)['changes']['EditGraph']['segments'][0]['window']
        window['end'] = 4
        self.assertCode(m9.check(self.prop(2), self.req(2)), 'window_out_of_range')
        window['end'] = 2; window['unit'] = 'frame'
        self.assertCode(m9.check(self.prop(2), self.req(2)), 'coordinate_mismatch')
        window['unit'] = 'second'; window['range_source_ref'] = 'capability_fixture'
        self.assertCode(m9.check(self.prop(2), self.req(2)), 'window_provenance')

    def test_plan_cannot_be_claimed_as_observed_media(self):
        window = self.prop(2)['changes']['EditGraph']['segments'][0]['window']
        window['basis'] = 'observed'
        errors = m9.check(self.prop(2), self.req(2))
        self.assertCode(errors, 'observation_source')
        self.assertCode(errors, 'planned_is_not_observed')

    def test_freeze_intent_is_explicit_and_needs_retained_event(self):
        segment = self.prop(2)['changes']['EditGraph']['segments'][0]
        segment['playback'] = {'kind': 'freeze_intent', 'anchor_event_id': 'camera_pan_track', 'reason': 'Explicit design intent, not an action hold inference.'}
        self.assertEqual(m9.check(self.prop(2), self.req(2)), [])
        segment['playback']['anchor_event_id'] = 'event_cut_ab'
        self.assertCode(m9.check(self.prop(2), self.req(2)), 'freeze_anchor')

    def test_assembly_adjacency_and_internal_cut_are_distinct(self):
        edit = self.prop(2)['changes']['EditGraph']
        edit['boundaries'][1]['execution_stage'] = 'post_edit'
        self.assertCode(m9.check(self.prop(2), self.req(2)), 'internal_boundary')
        edit['boundaries'][1]['execution_stage'] = 'model_internal'
        edit['assembly'] = ['segment_intro', 'segment_finish', 'segment_turn']
        self.assertCode(m9.check(self.prop(2), self.req(2)), 'assembly_boundaries')

    def test_pending_or_forged_continuity_policy_cannot_pass(self):
        self.req(2)['inputs']['continuity_context']['values']['policies'][0]['status'] = 'pending'
        self.sync(2)
        self.assertCode(m9.check(self.prop(2), self.req(2)), 'continuity_pending')
        self.req(2)['inputs']['continuity_context']['values']['policies'][0]['status'] = 'approved'
        self.sync(2)
        self.prop(2)['changes']['EditGraph']['boundaries'][0]['policy_id'] = 'invented'
        self.assertCode(m9.check(self.prop(2), self.req(2)), 'continuity_reference')

    def test_capability_unknown_or_wrong_profile_is_not_execution_permission(self):
        self.req(3)['inputs']['capability_context']['values']['profiles'][0]['status'] = 'unknown'
        self.sync(3)
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'capability_unknown')
        self.req(3)['inputs']['capability_context']['values']['profiles'][0]['status'] = 'known'
        self.sync(3)
        self.prop(3)['changes']['GenerationPlan']['tasks'][0]['profile_id'] = 'invented'
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'missing_capability')

    def test_m7_duration_is_checked_without_assuming_fifteen_seconds(self):
        inputs = self.req(3)['inputs']
        inputs['time_context']['values']['records'][1]['duration']['value'] = 11
        self.sync(3)
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'task_duration')
        inputs['time_context']['values']['records'][1]['duration']['value'] = 3
        self.sync(3)
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'generation_window_limit')
        inputs['time_context']['values']['records'][1]['duration'] = {'unit': 'frame', 'value': 6}
        self.sync(3)
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'time_unit')

    def test_same_shot_split_requires_supplied_capability(self):
        self.req(3)['inputs']['capability_context']['values']['profiles'][0]['supports_same_shot_split'] = False
        self.sync(3)
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'split_capability')

    def test_coverage_missing_duplicate_or_wrong_source_fails(self):
        gen = self.prop(3)['changes']['GenerationPlan']
        removed = gen['coverage'].pop()
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'generation_coverage')
        gen['coverage'].append(removed)
        other = deepcopy(removed); other['coverage_id'] = 'duplicate_selection'
        gen['coverage'].append(other)
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'generation_coverage')
        gen['coverage'].pop()
        gen['tasks'][0]['output_source_id'] = 'wrong_output'
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'output_source')

    def test_task_context_boundaries_and_compile_handoff_preserve_scope(self):
        gen = self.prop(3)['changes']['GenerationPlan']
        gen['tasks'][0]['context']['scene'] = ' '
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'schema')
        gen['tasks'][0]['context']['scene'] = 'Explicit scene'
        gen['tasks'][0]['entry_state_ids'] = ['entry_task_finish']
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'task_boundary_state')
        gen['tasks'][0]['entry_state_ids'] = ['entry_task_intro']
        gen['m11_handoffs'][0]['mode_intent'] = 'Ref2VA'
        self.assertCode(m9.check(self.prop(3), self.req(3)), 'compile_handoff')

    def test_all_observed_media_can_have_zero_generation_tasks(self):
        request, proposal = self.req(3), self.prop(3)
        request['sources']['observation'] = {'kind': 'media_observation', 'locator': 'test-observation://provided-fixture', 'version': '1', 'excerpt': 'Synthetic observation-shaped fixture, not a real video measurement.'}
        edits = request['inputs']['edit_context']['values']
        for segment in edits['segments']:
            segment['window']['basis'] = 'observed'
            segment['window']['range_source_ref'] = 'observation'
        request['inputs']['capability_context']['values']['profiles'] = []
        request['inputs']['time_context']['values']['records'] = []
        self.sync(3)
        gen = proposal['changes']['GenerationPlan']
        gen['reused_segment_ids'] = [s['segment_id'] for s in edits['segments']]
        for key in ['tasks','coverage','m7_requests','m11_handoffs']: gen[key] = []
        self.assertEqual(m9.check(proposal, request), [])
        gen['reused_segment_ids'].pop()
        self.assertCode(m9.check(proposal, request), 'generation_coverage')

    def test_sibling_projection_conflict_rejects_entire_batch(self):
        self.req(2)['inputs']['shot_context']['values']['shots'][0]['purpose'] = 'Different supplied snapshot'
        self.sync(2)
        result = m9.accept(self.empty, self.proposals, self.requests)
        self.assertCode(result['errors'], 'sibling_snapshot_conflict')
        self.assertNotIn('state', result)
        self.assertEqual(self.empty['version'], 0)

    def test_duplicate_writers_and_stale_base_fail(self):
        duplicate = deepcopy(self.prop(1)); duplicate['proposal_id'] = 'other_proposal'
        self.proposals['proposals'].append(duplicate)
        result = m9.accept(self.empty, self.proposals, self.requests)
        self.assertCode(result['errors'], 'duplicate_id')
        self.proposals['proposals'].pop()
        state = self.accepted()
        request, proposal = deepcopy(self.req(1)), deepcopy(self.prop(1))
        request['request_id'] = 'new_request'; proposal['source_request_id'] = request['request_id']; proposal['proposal_id'] = 'new_proposal'
        result = m9.accept(state, proposal, request)
        self.assertCode(result['errors'], 'stale_base')

    def test_partial_revision_invalidates_actual_siblings_and_preserves_receipts(self):
        state = self.accepted()
        request, proposal = deepcopy(self.req(1)), deepcopy(self.prop(1))
        request['request_id'] = 'revision_request'; request['base_version'] = 1
        proposal.update(source_request_id=request['request_id'], proposal_id='revision_proposal', base_version=1)
        proposal['changes']['ShotMap']['shots'][0]['purpose'] = 'Revised narrative purpose'
        result = m9.accept(state, proposal, request)
        self.assertEqual(result['status'], 'passed_with_unverified', result)
        new = result['state']
        self.assertEqual(new['version'], 2)
        self.assertEqual(new['stale_modules'], ['M9.2','M9.3'])
        self.assertEqual(len(new['receipts']), 4)
        self.assertEqual(m9.state_errors(new), [])

    def test_accepted_state_or_dependency_tampering_cannot_skip_revalidation(self):
        state = self.accepted()
        state['content']['ShotMap']['shots'][0]['purpose'] = 'unreceipted mutation'
        self.assertCode(m9.state_errors(state), 'state_digest')
        state = self.accepted()
        state['consumers'][2]['read_paths'] = ['/display']
        self.assertCode(m9.state_errors(state), 'actual_read_paths')

    def test_impact_follows_actual_reads_display_and_prior_stale(self):
        before = fixture('impact-before.json'); after = fixture('impact-after.json')
        result = m9.impact(before, after)
        self.assertEqual(result['changed_paths'], ['/display/title'])
        self.assertTrue(all(x['status'] == 'current' for x in result['consumers']))
        after = deepcopy(before)
        after['content']['EditGraph']['segments'][0]['window']['end'] = 1
        result = m9.impact(before, after)
        hit = {x['consumer_id']:x['status'] for x in result['consumers']}
        self.assertEqual(hit['M9.3'], 'stale')
        self.assertEqual(hit['M7.example_actual_read'], 'stale')
        self.assertEqual(hit['M9.1'], 'current')
        self.assertEqual(hit['M11.example_actual_read'], 'current')
        before['consumers'][0]['status'] = 'stale'
        status = next(x['status'] for x in m9.impact(before, before)['consumers'] if x['consumer_id'] == 'M9.1')
        self.assertEqual(status, 'stale')

    def test_strict_json_duplicate_keys_and_nonfinite_values(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder)/'bad.json'
            for value in ['{"kind":"M9Request","kind":"M9Request"}', '{"number":NaN}']:
                p.write_text(value)
                result = subprocess.run([sys.executable, str(ROOT/'scripts/m9_contract.py'), 'route', str(p)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)['errors'][0]['code'], 'input_error')


if __name__ == '__main__': unittest.main()
