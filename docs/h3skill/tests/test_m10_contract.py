"""Behavior checks for the M10 contract; all media assertions are synthetic design fixtures."""
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'h3-visual-look'
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('m10_contract', ROOT / 'scripts/m10_contract.py')
m10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m10)


class M10ContractTests(unittest.TestCase):
    def pair(self, index, minimal=False):
        tag = 'minimal' if minimal else 'standalone'
        return (m10.load(ROOT / f'assets/request-{tag}-m10-{index}.json'),
                m10.load(ROOT / f'assets/proposal-{tag}-m10-{index}.json'))

    def empty(self):
        return m10.load(ROOT / 'assets/state-empty.json')

    def batch(self):
        return (m10.load(ROOT / 'assets/requests.json'), m10.load(ROOT / 'assets/proposal-batch.json'))

    def accepted(self):
        requests, proposals = self.batch()
        result = m10.accept(self.empty(), proposals, requests)
        self.assertEqual(result['status'], 'passed_with_unverified', result)
        return result['state']

    def sync(self, request, proposal):
        proposal['context'] = deepcopy(request['inputs'])
        proposal['sources'] = deepcopy(request['sources'])

    def codes(self, errors):
        return {e['code'] for e in errors}

    def rejected(self, request, proposal, code, owner=None):
        errors = m10.check(proposal, request)
        self.assertIn(code, self.codes(errors), errors)
        if owner:
            self.assertTrue(any(e['code'] == code and e['owner'] == owner for e in errors), errors)
        return errors

    def revision(self, request, proposal, version=1):
        request['request_id'] += '_revision'
        request['base_version'] = version
        proposal['proposal_id'] += '_revision'
        proposal['source_request_id'] = request['request_id']
        proposal['base_version'] = version

    def test_four_standalone_routes_and_checks_preserve_inputs(self):
        for i in range(1, 5):
            with self.subTest(i=i):
                request, proposal = self.pair(i)
                before = deepcopy((request, proposal))
                route = m10.route(request)
                self.assertTrue(route['ready'])
                self.assertEqual(route['invocation_status'], 'not_invoked')
                self.assertEqual(m10.check(proposal, request), [])
                self.assertEqual((request, proposal), before)

    def test_all_four_minimal_calls_and_partial_parent_acceptance(self):
        required = {1: {'brief', 'scope_context'}, 2: {'brief', 'scope_context', 'scene_context'},
                    3: {'brief', 'scope_context'}, 4: {'brief', 'scope_context', 'identity_context'}}
        for i in range(1, 5):
            with self.subTest(i=i):
                request, proposal = self.pair(i, True)
                self.assertEqual(set(request['inputs']), required[i])
                self.assertTrue(m10.route(request)['ready'])
                self.assertEqual(m10.check(proposal, request), [])
                result = m10.accept(self.empty(), proposal, request)
                self.assertEqual(result['status'], 'passed_with_unverified', result)
                self.assertEqual(set(result['state']['content']), {m10.PARTS[f'M10.{i}']})
                self.assertEqual(m10.state_errors(result['state']), [])

    def test_batch_atomic_acceptance_idempotency_and_limits(self):
        requests, proposals = self.batch()
        empty = self.empty()
        before = deepcopy((empty, requests, proposals))
        result = m10.accept(empty, proposals, requests)
        self.assertEqual(result['status'], 'passed_with_unverified')
        self.assertEqual(result['state']['status'], 'draft')
        self.assertEqual(result['state']['version'], 1)
        self.assertEqual(len(result['state']['receipts']), 4)
        self.assertIn('h3_inference', result['not_run'])
        again = m10.accept(result['state'], proposals, requests)
        self.assertTrue(again['idempotent'])
        self.assertEqual(again['state'], result['state'])
        self.assertEqual((empty, requests, proposals), before)

    def test_empty_root_style_does_not_inherit_invented_defaults(self):
        request, proposal = self.pair(1)
        proposal['changes']['StyleHierarchy']['layers'][0]['style'] = {}
        self.rejected(request, proposal, 'incomplete_style', 'M10.1')

    def test_empty_child_style_is_valid_explicit_inheritance(self):
        request, proposal = self.pair(1)
        self.assertEqual(proposal['changes']['StyleHierarchy']['layers'][1]['style'], {})
        self.assertEqual(m10.check(proposal, request), [])

    def test_style_override_requires_exact_keys_and_reason(self):
        for field, value, code in [('override_keys', [], 'style_override_keys'), ('override_reason', None, 'style_override_reason')]:
            with self.subTest(field=field):
                request, proposal = self.pair(1)
                proposal['changes']['StyleHierarchy']['layers'][2][field] = value
                self.rejected(request, proposal, code, 'M10.1')

    def test_style_parent_and_scope_cycles_are_rejected(self):
        request, proposal = self.pair(1)
        proposal['changes']['StyleHierarchy']['layers'][0]['parent_scope_id'] = 'shot_handoff'
        self.rejected(request, proposal, 'style_cycle', 'M10.1')
        request, proposal = self.pair(1)
        request['inputs']['scope_context']['values']['scopes'][0]['parent_scope_id'] = 'shot_handoff'
        self.sync(request, proposal)
        self.rejected(request, proposal, 'scope_cycle', 'caller')

    def test_missing_or_duplicate_scope_and_layers_rejected(self):
        request, proposal = self.pair(1)
        proposal['changes']['StyleHierarchy']['layers'].append(deepcopy(proposal['changes']['StyleHierarchy']['layers'][0]))
        self.rejected(request, proposal, 'duplicate_id')
        request, proposal = self.pair(1)
        proposal['changes']['StyleHierarchy']['layers'].pop(1)
        self.rejected(request, proposal, 'missing_style_parent')
        request, proposal = self.pair(1)
        request['inputs']['scope_context']['values']['scopes'][2]['parent_scope_id'] = 'absent_scene'
        self.sync(request, proposal)
        self.rejected(request, proposal, 'missing_scope_parent')

    def test_identity_reference_cannot_supply_style(self):
        request, proposal = self.pair(1)
        proposal['changes']['StyleHierarchy']['layers'][0]['reference_uses'][0]['asset_id'] = 'actor_ref'
        self.rejected(request, proposal, 'reference_use_forbidden', 'M2')

    def test_reference_scope_and_entity_permissions_are_bounded(self):
        request, proposal = self.pair(1)
        request['inputs']['reference_context']['values']['assets'][0]['scope_ids'] = ['shot_handoff']
        self.sync(request, proposal)
        self.rejected(request, proposal, 'reference_scope', 'M2')
        request, proposal = self.pair(4)
        material = proposal['changes']['MaterialEffectPlan']['materials'][0]
        material['reference_uses'] = [{'asset_id': 'look_ref', 'use': 'material', 'scope_id': 'shot_handoff', 'target_ids': ['subject_a']}]
        self.rejected(request, proposal, 'reference_targets', 'M2')

    def test_missing_reference_permission_is_not_guessed(self):
        request, proposal = self.pair(1)
        del request['inputs']['reference_context']
        self.sync(request, proposal)
        self.rejected(request, proposal, 'reference_permission_missing', 'M2')

    def test_conflicting_allowed_and_forbidden_use_is_rejected(self):
        request, proposal = self.pair(1)
        request['inputs']['reference_context']['values']['assets'][0]['forbidden_uses'].append('style')
        self.sync(request, proposal)
        self.rejected(request, proposal, 'permission_conflict', 'M2')

    def test_entity_limited_permission_cannot_expand_to_scope_wide_style(self):
        request, proposal = self.pair(1)
        request['inputs']['reference_context']['values']['assets'][0]['target_ids'] = ['subject_a']
        self.sync(request, proposal)
        self.rejected(request, proposal, 'reference_targets', 'M2')
        self.assertEqual(m10.accept(self.empty(), proposal, request)['status'], 'failed')

    def test_readonly_style_reference_still_needs_consistent_permissions(self):
        request, proposal = self.pair(3)
        request['inputs']['style_context']['values']['layers'][0]['reference_uses'][0]['asset_id'] = 'actor_ref'
        self.sync(request, proposal)
        self.rejected(request, proposal, 'reference_use_forbidden', 'M2')
        self.assertFalse(m10.route(request)['ready'])
        self.assertEqual(m10.accept(self.empty(), proposal, request)['status'], 'failed')

    def test_readonly_reference_closure_is_conditional_not_a_required_upstream_run(self):
        request, proposal = self.pair(3)
        del request['inputs']['reference_context']
        self.sync(request, proposal)
        self.rejected(request, proposal, 'reference_permission_missing', 'M2')
        request['inputs']['style_context']['values']['layers'][0]['reference_uses'] = []
        self.sync(request, proposal)
        self.assertEqual(m10.check(proposal, request), [])

    def test_readonly_lighting_and_color_references_cannot_bypass_permission(self):
        request, proposal = self.pair(3)
        request['inputs']['lighting_context']['values']['setups'][0]['lights'][0]['reference_uses'] = [
            {'asset_id': 'actor_ref', 'use': 'lighting', 'scope_id': 'scene_counter', 'target_ids': []}]
        self.sync(request, proposal)
        self.rejected(request, proposal, 'reference_use_forbidden', 'M2')
        request, proposal = self.pair(4)
        request['inputs']['color_context']['values']['grades'][0]['reference_uses'] = [
            {'asset_id': 'actor_ref', 'use': 'color', 'scope_id': 'work_look', 'target_ids': []}]
        self.sync(request, proposal)
        self.rejected(request, proposal, 'reference_use_forbidden', 'M2')

    def test_readonly_lighting_visibility_scope_is_resolvable(self):
        request, proposal = self.pair(3)
        request['inputs']['lighting_context']['values']['visibility_checks'][0]['scope_id'] = 'unknown_scope'
        self.sync(request, proposal)
        self.rejected(request, proposal, 'unknown_scope', 'M5')
        self.assertFalse(m10.route(request)['ready'])

    def test_local_warm_light_and_global_cool_grade_can_coexist(self):
        request, proposal = self.pair(3)
        self.assertIn('冷中性', proposal['changes']['ColorPlan']['grades'][0]['temperature_bias'])
        self.assertIn('暖', request['inputs']['lighting_context']['values']['setups'][0]['lights'][0]['color_description'])
        self.assertEqual(m10.check(proposal, request), [])

    def test_numeric_kelvin_has_no_invented_default_and_rejects_invalid_values(self):
        request, proposal = self.pair(2)
        self.assertIsNone(proposal['changes']['LightingPlan']['setups'][0]['lights'][0]['temperature_kelvin'])
        for number in (0, -1, True, float('nan')):
            with self.subTest(number=number):
                req, prop = self.pair(2)
                prop['changes']['LightingPlan']['setups'][0]['lights'][0]['temperature_kelvin'] = number
                errors = m10.check(prop, req)
                self.assertIn('schema', self.codes(errors))

    def test_lighting_missing_scene_constraint_is_a_source_gap(self):
        request, proposal = self.pair(2)
        request['inputs']['scene_context']['values']['conditions'][0]['scope_id'] = 'shot_handoff'
        self.sync(request, proposal)
        self.rejected(request, proposal, 'scene_condition_missing', 'M3')

    def test_lighting_inheritance_requires_parent_and_reason(self):
        request, proposal = self.pair(2)
        parent = proposal['changes']['LightingPlan']['setups'][0]
        child = deepcopy(parent)
        child.update(setup_id='lighting_shot', scope_id='shot_handoff', parent_setup_id=parent['setup_id'])
        child['lights'][0]['quality'] = '更集中的边缘光'
        proposal['changes']['LightingPlan']['setups'].append(child)
        self.rejected(request, proposal, 'override_reason', 'M10.2')
        child['override_reason'] = '突出局部材质且保留手部可见条件。'
        self.assertEqual(m10.check(proposal, request), [])
        child['parent_setup_id'] = None
        self.rejected(request, proposal, 'inheritance_parent', 'M10.2')

    def test_provenance_only_change_is_not_an_invented_visual_override(self):
        request, proposal = self.pair(2)
        request['sources']['second'] = deepcopy(request['sources']['design'])
        request['sources']['second']['locator'] = 'synthetic-design-fixture://m10/second-proof'
        self.sync(request, proposal)
        parent = proposal['changes']['LightingPlan']['setups'][0]
        child = deepcopy(parent)
        child.update(setup_id='lighting_shot', scope_id='shot_handoff', parent_setup_id=parent['setup_id'])
        child['lights'][0]['source_refs'] = ['second']
        proposal['changes']['LightingPlan']['setups'].append(child)
        self.assertEqual(m10.check(proposal, request), [])

    def test_visibility_missing_conflict_unknown_and_wrong_scope_do_not_pass(self):
        for mutation, code in [('missing', 'visibility_coverage'), ('conflict', 'visibility_conflict'),
                               ('unverified', 'visibility_unverified'), ('scope', 'visibility_scope')]:
            with self.subTest(mutation=mutation):
                request, proposal = self.pair(2)
                checks = proposal['changes']['LightingPlan']['visibility_checks']
                if mutation == 'missing':
                    checks.clear()
                elif mutation == 'scope':
                    checks[0]['scope_id'] = 'work_look'
                else:
                    checks[0]['result'] = mutation
                self.rejected(request, proposal, code, 'M5')

    def test_color_identity_protection_matches_scope(self):
        request, proposal = self.pair(3)
        proposal['changes']['ColorPlan']['grades'][0]['protected_identity_ids'] = []
        self.rejected(request, proposal, 'identity_preservation', 'M2')
        request, proposal = self.pair(3)
        proposal['changes']['ColorPlan']['grades'][0]['identity_change'] = True
        self.rejected(request, proposal, 'schema')

    def test_color_does_not_write_light_properties(self):
        request, proposal = self.pair(3)
        proposal['changes']['ColorPlan']['grades'][0]['temperature_kelvin'] = 5000
        self.rejected(request, proposal, 'schema')

    def test_material_and_effect_arrays_cannot_both_be_empty(self):
        request, proposal = self.pair(4, True)
        proposal['changes']['MaterialEffectPlan']['materials'] = []
        self.rejected(request, proposal, 'empty_material_effect_plan', 'M10.4')

    def test_material_base_identity_cannot_be_redesigned(self):
        request, proposal = self.pair(4)
        proposal['changes']['MaterialEffectPlan']['materials'][0]['base_material'] = '白色长发纤维'
        self.rejected(request, proposal, 'identity_material_change', 'M2')

    def test_unknown_material_target_or_surface_is_rejected(self):
        for field, value, code in [('target_id', 'missing_subject', 'material_target'),
                                   ('surface_id', 'missing_surface', 'material_surface')]:
            with self.subTest(field=field):
                request, proposal = self.pair(4)
                proposal['changes']['MaterialEffectPlan']['materials'][0][field] = value
                self.rejected(request, proposal, code, 'M2')

    def test_changed_surface_requires_allowed_mutability_and_permission(self):
        request, proposal = self.pair(4)
        request['inputs']['identity_context']['values']['entities'][0]['surfaces'][0]['mutable_properties'] = []
        self.sync(request, proposal)
        self.rejected(request, proposal, 'permission_surface', 'M2/M8')
        request, proposal = self.pair(4)
        del request['inputs']['continuity_context']
        self.sync(request, proposal)
        self.rejected(request, proposal, 'continuity_permission_missing', 'M8')

    def test_state_permission_must_match_value_and_scope(self):
        request, proposal = self.pair(4)
        request['inputs']['continuity_context']['values']['permissions'][0]['allowed_values'] = ['damp']
        self.sync(request, proposal)
        self.rejected(request, proposal, 'continuity_permission_mismatch', 'M8')
        request, proposal = self.pair(4)
        proposal['changes']['MaterialEffectPlan']['materials'][0]['scope_id'] = 'scene_counter'
        self.rejected(request, proposal, 'continuity_permission_mismatch', 'M8')

    def test_visual_condition_handoff_is_exact_not_a_state_write(self):
        request, proposal = self.pair(4)
        proposal['changes']['MaterialEffectPlan']['continuity_handoffs'] = []
        self.rejected(request, proposal, 'continuity_handoff_coverage', 'M8')
        request, proposal = self.pair(4)
        proposal['changes']['StateLedger'] = {'status': 'observed'}
        self.rejected(request, proposal, 'schema')

    def test_effects_need_visibility_mitigation(self):
        request, proposal = self.pair(4)
        proposal['changes']['MaterialEffectPlan']['effects'][0]['mitigation'] = None
        self.rejected(request, proposal, 'effect_mitigation_missing', 'M5')
        request, proposal = self.pair(4)
        proposal['changes']['MaterialEffectPlan']['effects'][0]['visibility_impact'] = 'blocks_key'
        self.rejected(request, proposal, 'effect_blocks_key', 'M5')

    def test_conditional_effect_needs_event_without_inventing_timing(self):
        request, proposal = self.pair(4)
        effect = proposal['changes']['MaterialEffectPlan']['effects'][0]
        effect.update(trigger_kind='event', event_id='touch_event')
        self.rejected(request, proposal, 'effect_event_missing', 'M4/M7')
        request['inputs']['event_context'] = {'owner': 'external', 'source_id': 'design', 'source_version': 'design-1',
                                              'values': {'event_ids': ['touch_event']}}
        self.sync(request, proposal)
        self.assertEqual(m10.check(proposal, request), [])
        effect['time_seconds'] = 2
        self.rejected(request, proposal, 'schema')

    def test_effect_only_plan_can_be_independent(self):
        request, proposal = self.pair(4, True)
        request['inputs']['identity_context']['values']['entities'] = []
        self.sync(request, proposal)
        _, full = self.pair(4)
        effect = deepcopy(full['changes']['MaterialEffectPlan']['effects'][0])
        effect.update(scope_id='local_scope', visibility_impact='none', mitigation=None)
        plan = proposal['changes']['MaterialEffectPlan']
        plan['materials'] = []
        plan['effects'] = [effect]
        self.assertEqual(m10.check(proposal, request), [])

    def test_blank_required_fields_unknown_versions_and_extra_writes_rejected(self):
        for mutation in ('blank', 'version', 'bool_version', 'extra'):
            with self.subTest(mutation=mutation):
                request, proposal = self.pair(1)
                if mutation == 'blank':
                    request['inputs']['brief'] = ' \n '
                elif mutation == 'version':
                    request['contract_version'] = '2.0.0'
                elif mutation == 'bool_version':
                    request['base_version'] = True
                else:
                    proposal['changes']['WorkIntent'] = {'goal': 'unauthorized'}
                self.rejected(request, proposal, 'schema')

    def test_actual_original_request_must_match_context_and_sources(self):
        request, proposal = self.pair(1)
        proposal['context']['brief'] = '替换原请求'
        self.rejected(request, proposal, 'original_request_mismatch')
        request, proposal = self.pair(1)
        proposal['sources']['design']['excerpt'] = '另一份来源声明'
        self.rejected(request, proposal, 'original_request_mismatch')

    def test_source_version_and_evidence_refs_are_resolvable(self):
        request, proposal = self.pair(1)
        request['inputs']['scope_context']['source_version'] = 'missing-version'
        self.sync(request, proposal)
        self.rejected(request, proposal, 'source_version')
        request, proposal = self.pair(1)
        proposal['changes']['StyleHierarchy']['layers'][0]['source_refs'] = ['missing-source']
        self.rejected(request, proposal, 'missing_source')

    def test_unresolved_owner_issue_remains_a_failure(self):
        request, proposal = self.pair(2)
        proposal['issues'] = [{'code': 'unreadable_contact', 'owner': 'M5', 'detail': '接触区域缺少可见性依据'}]
        self.rejected(request, proposal, 'unresolved_issue', 'M5')

    def test_batch_rejection_is_atomic(self):
        requests, proposals = self.batch()
        before = self.empty()
        snapshot = deepcopy(before)
        proposals['proposals'][3]['changes']['MaterialEffectPlan']['materials'][0]['base_material'] = '金属'
        result = m10.accept(before, proposals, requests)
        self.assertEqual(result['status'], 'failed')
        self.assertNotIn('state', result)
        self.assertEqual(before, snapshot)

    def test_batch_sibling_projection_conflict_is_rejected(self):
        requests, proposals = self.batch()
        requests['requests'][2]['inputs']['lighting_context']['values']['setups'][0]['lights'][0]['quality'] = '另一照明快照'
        proposals['proposals'][2]['context'] = deepcopy(requests['requests'][2]['inputs'])
        result = m10.accept(self.empty(), proposals, requests)
        self.assertIn('sibling_snapshot_conflict', self.codes(result['errors']))
        self.assertNotIn('state', result)

    def test_duplicate_partition_and_wrong_request_set_rejected(self):
        requests, proposals = self.batch()
        duplicate = deepcopy(proposals['proposals'][0]); duplicate['proposal_id'] = 'duplicate_writer'
        proposals['proposals'].append(duplicate)
        result = m10.accept(self.empty(), proposals, requests)
        self.assertIn('duplicate_id', self.codes(result['errors']))
        requests, proposals = self.batch()
        requests['requests'].pop()
        result = m10.accept(self.empty(), proposals, requests)
        self.assertIn('request_set', self.codes(result['errors']))

    def test_stale_base_and_reused_ids_rejected(self):
        state = self.accepted()
        request, proposal = self.pair(1)
        proposal['proposal_id'] += '_new'; request['request_id'] += '_new'; proposal['source_request_id'] = request['request_id']
        result = m10.accept(state, proposal, request)
        self.assertIn('stale_base', self.codes(result['errors']))
        request, proposal = self.pair(1)
        proposal['changes']['StyleHierarchy']['layers'][0]['style']['visual_language'] = 'changed'
        result = m10.accept(state, proposal, request)
        self.assertIn('idempotency_conflict', self.codes(result['errors']))

    def test_request_id_cannot_authorize_new_proposal(self):
        state = self.accepted()
        request, proposal = self.pair(1)
        proposal['proposal_id'] += '_new'
        proposal['base_version'] = request['base_version'] = 1
        result = m10.accept(state, proposal, request)
        self.assertIn('request_id_conflict', self.codes(result['errors']))

    def test_retries_and_new_revisions_cannot_mix(self):
        state = self.accepted()
        requests, proposals = self.batch()
        self.revision(requests['requests'][0], proposals['proposals'][0])
        result = m10.accept(state, proposals, requests)
        self.assertIn('mixed_retry', self.codes(result['errors']))

    def test_same_source_version_is_immutable(self):
        state = self.accepted()
        request, proposal = self.pair(1)
        self.revision(request, proposal)
        request['sources']['design']['excerpt'] = '悄悄改来源正文'
        self.sync(request, proposal)
        result = m10.accept(state, proposal, request)
        self.assertIn('immutable_source_version', self.codes(result['errors']))

    def test_style_revision_marks_only_actual_readers_stale(self):
        state = self.accepted()
        request, proposal = self.pair(1)
        self.revision(request, proposal)
        proposal['changes']['StyleHierarchy']['layers'][0]['style']['visual_language'] = '精确清楚的环境叙事'
        result = m10.accept(state, proposal, request)
        self.assertEqual(result['status'], 'passed_with_unverified', result)
        self.assertEqual(result['state']['stale_modules'], ['M10.2', 'M10.3', 'M10.4'])
        self.assertEqual(m10.state_errors(result['state']), [])
        # A minimal color caller did not read style, so installing style does not invalidate it.
        color_request, color_proposal = self.pair(3, True)
        partial = m10.accept(self.empty(), color_proposal, color_request)['state']
        style_request, style_proposal = self.pair(1, True)
        self.revision(style_request, style_proposal)
        combined = m10.accept(partial, style_proposal, style_request)
        self.assertEqual(combined['status'], 'passed_with_unverified', combined)
        self.assertEqual(combined['state']['stale_modules'], [])

    def test_changed_source_version_invalidates_actual_readers(self):
        state = self.accepted()
        request, proposal = self.pair(1)
        self.revision(request, proposal)
        request['sources']['design']['version'] = 'design-2'
        request['sources']['design']['excerpt'] = '明确登记的新版来源'
        for key in request['inputs']:
            if key.endswith('_context'):
                request['inputs'][key]['source_version'] = 'design-2'
        self.sync(request, proposal)
        result = m10.accept(state, proposal, request)
        self.assertEqual(result['status'], 'passed_with_unverified', result)
        self.assertEqual(result['state']['stale_modules'], ['M10.2', 'M10.3', 'M10.4'])

    def test_accept_rejects_stale_sibling_until_dependencies_are_revalidated(self):
        state = self.accepted()
        request, proposal = self.pair(1)
        self.revision(request, proposal)
        proposal['changes']['StyleHierarchy']['layers'][0]['style']['rendering'] = '新的写实渲染意图'
        changed = m10.accept(state, proposal, request)['state']
        request4, proposal4 = self.pair(4)
        self.revision(request4, proposal4, 2)
        request4['inputs']['style_context']['values'] = deepcopy(changed['content']['StyleHierarchy'])
        self.sync(request4, proposal4)
        result = m10.accept(changed, proposal4, request4)
        self.assertIn('stale_sibling_dependency', self.codes(result['errors']))
        self.assertNotIn('state', result)
        requests = []; proposals = []
        for i in (2, 3, 4):
            req, prop = self.pair(i)
            self.revision(req, prop, 2)
            req['inputs']['style_context']['values'] = deepcopy(changed['content']['StyleHierarchy'])
            self.sync(req, prop)
            requests.append(req); proposals.append(prop)
        result = m10.accept(changed, {'kind':'M10ProposalBatch','contract_version':'1.0.0','proposals':proposals},
                            {'kind':'M10RequestBatch','contract_version':'1.0.0','requests':requests})
        self.assertEqual(result['status'], 'passed_with_unverified', result)
        self.assertEqual(result['state']['stale_modules'], [])

    def test_stale_propagates_transitively_only_through_actual_sibling_reads(self):
        requests, proposals = self.batch()
        for key in ('style_context', 'color_context'):
            del requests['requests'][3]['inputs'][key]
        self.sync(requests['requests'][3], proposals['proposals'][3])
        state = m10.accept(self.empty(), proposals, requests)['state']
        self.assertNotIn('/content/StyleHierarchy', state['consumers'][3]['read_paths'])
        request, proposal = self.pair(1)
        self.revision(request, proposal)
        proposal['changes']['StyleHierarchy']['layers'][0]['style']['rendering'] = '新的写实渲染意图'
        result = m10.accept(state, proposal, request)
        self.assertEqual(result['status'], 'passed_with_unverified', result)
        self.assertIn('M10.4', result['state']['stale_modules'])
        candidate = deepcopy(state)
        candidate['content']['StyleHierarchy'] = deepcopy(proposal['changes']['StyleHierarchy'])
        impact = m10.impact(state, candidate)
        material = next(x for x in impact['consumers'] if x['consumer_id'] == 'M10.4')
        self.assertEqual(material['status'], 'stale')
        self.assertEqual(material['stale_dependencies'], ['M10.2'])

    def test_hand_edited_accepted_content_or_source_is_rejected(self):
        state = self.accepted()
        request, proposal = self.pair(1)
        state['content']['StyleHierarchy']['layers'][0]['style']['rendering'] = 'different'
        result = m10.accept(state, proposal, request)
        self.assertIn('state_digest', self.codes(result['errors']))
        state = self.accepted()
        state['sources']['design']['excerpt'] = 'without a receipt'
        for c in state['consumers']:
            c['status'] = 'stale'
        state['stale_modules'] = list(m10.PARTS)
        result = m10.accept(state, proposal, request)
        self.assertIn('state_source_history', self.codes(result['errors']))

    def test_removing_read_paths_or_clearing_stale_does_not_erase_dependencies(self):
        state = self.accepted()
        state['consumers'][1]['read_paths'].remove('/content/StyleHierarchy')
        self.assertIn('actual_read_paths', self.codes(m10.state_errors(state)))
        state = self.accepted()
        request, proposal = self.pair(1)
        self.revision(request, proposal)
        proposal['changes']['StyleHierarchy']['layers'][0]['style']['visual_language'] = 'new design'
        revised = m10.accept(state, proposal, request)['state']
        revised['stale_modules'] = []
        for c in revised['consumers']:
            c['status'] = 'current'
        self.assertIn('sibling_snapshot_conflict', self.codes(m10.state_errors(revised)))

    def test_display_only_impact_does_not_replan_visual_content(self):
        before = self.accepted(); after = deepcopy(before)
        after['display'] = {'title': 'renamed'}
        result = m10.impact(before, after)
        self.assertEqual(result['changed_paths'], ['/display'])
        self.assertTrue(all(c['status'] == 'current' for c in result['consumers']))

    def test_impact_preserves_prior_stale_and_removed_consumers(self):
        before = self.accepted()
        before['consumers'][1]['status'] = 'stale'; before['stale_modules'] = ['M10.2']
        after = deepcopy(before)
        after['consumers'].pop(1); after['stale_modules'] = []
        result = m10.impact(before, after)
        entry = next(c for c in result['consumers'] if c['consumer_id'] == 'M10.2')
        self.assertEqual(entry['status'], 'stale')
        self.assertIn('/content/StyleHierarchy', entry['read_paths'])

    def test_impact_uses_real_source_paths_and_does_not_compare_different_works(self):
        before = self.accepted(); after = deepcopy(before)
        after['sources']['design']['excerpt'] = 'candidate update'
        result = m10.impact(before, after)
        self.assertTrue(all(c['status'] == 'stale' for c in result['consumers']))
        after['work_id'] = 'another_work'
        self.assertEqual(m10.impact(before, after)['status'], 'failed')

    def test_json_parser_rejects_duplicate_keys_and_nonfinite_literals(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            for content in ('{"key":1,"key":2}', '{"value":NaN}', '{"value":Infinity}'):
                with self.subTest(content=content):
                    path.write_text(content)
                    with self.assertRaises(ValueError):
                        m10.load(path)

    def test_another_skills_schema_helper_does_not_change_m10_contract(self):
        old = sys.modules.get('_schema')
        foreign = types.ModuleType('_schema')
        foreign.canonical = lambda value: 'wrong helper'
        foreign.validate = lambda *args: [('foreign', 'Wrong skill helper')]
        sys.modules['_schema'] = foreign
        try:
            isolated_spec = importlib.util.spec_from_file_location('m10_helper_isolation', ROOT / 'scripts/m10_contract.py')
            isolated = importlib.util.module_from_spec(isolated_spec)
            isolated_spec.loader.exec_module(isolated)
            request, proposal = self.pair(2, True)
            self.assertEqual(isolated.check(proposal, request), [])
            proposal['changes']['LightingPlan']['setups'][0]['lights'][0]['temperature_kelvin'] = 0
            self.assertIn('schema', self.codes(isolated.check(proposal, request)))
        finally:
            if old is None:
                del sys.modules['_schema']
            else:
                sys.modules['_schema'] = old

    def test_portable_cli_runs_in_isolation_without_sibling_packages(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            package = work / 'isolated-skill'
            shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns('__pycache__'))
            other = work / 'unrelated'; other.mkdir()
            env = {'PATH': '', 'PYTHONNOUSERSITE': '1'}
            script = package / 'scripts/m10_contract.py'
            for i in range(1, 5):
                request = package / f'assets/request-minimal-m10-{i}.json'
                proposal = package / f'assets/proposal-minimal-m10-{i}.json'
                for args in [('route', str(request)), ('check', str(proposal), '--request', str(request))]:
                    result = subprocess.run([sys.executable, '-I', str(script), *args], cwd=other, env=env,
                                            capture_output=True, text=True, check=False)
                    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                    self.assertEqual(json.loads(result.stdout)['status'], 'passed_with_unverified')
            command = [sys.executable, '-I', str(script), 'accept', str(package/'assets/state-empty.json'),
                       str(package/'assets/proposal-batch.json'), '--requests', str(package/'assets/requests.json')]
            result = subprocess.run(command, cwd=other, env=env, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(json.loads(result.stdout)['state']['version'], 1)
            self.assertFalse(list(package.rglob('__pycache__')))


if __name__ == '__main__':
    unittest.main()
