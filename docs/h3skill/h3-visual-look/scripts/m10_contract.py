#!/usr/bin/env python3
"""Check explicit M10 LookPlan declarations; no NLP, media analysis, network or file writes."""
from __future__ import annotations
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
# Load the exact bundled helper even when another skill already imported a module named _schema.
_schema_spec = importlib.util.spec_from_file_location('_h3_visual_look_schema', ROOT / 'scripts/_schema.py')
_schema_module = importlib.util.module_from_spec(_schema_spec)
_schema_spec.loader.exec_module(_schema_module)
canonical, validate = _schema_module.canonical, _schema_module.validate

VERSION = '1.0.0'
PARTS = {'M10.1': 'StyleHierarchy', 'M10.2': 'LightingPlan', 'M10.3': 'ColorPlan', 'M10.4': 'MaterialEffectPlan'}
SIBLINGS = {'style_context': ('StyleHierarchy', {'layers': 'scope_id'}),
            'lighting_context': ('LightingPlan', {'setups': 'setup_id', 'visibility_checks': 'requirement_id'}),
            'color_context': ('ColorPlan', {'grades': 'grade_id'})}
STYLE_KEYS = {'rendering', 'visual_language', 'image_texture'}
LIMITS = ['Only explicit JSON structure, relationships and supplied provenance/permissions were checked.',
          'Free-text meaning and the truth of supplied assertions remain unverified.',
          'No physical light simulation, actual visibility/continuity observation, H3 execution or complete G0-G4 certification.']
NOT_RUN = ['natural_language_semantic_audit', 'physical_lighting_simulation', 'actual_media_visibility',
           'actual_media_continuity', 'h3_inference']


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON object key: ' + key)
        result[key] = value
    return result


def load(path):
    def bad_number(value):
        raise ValueError('Non-finite JSON number: ' + value)
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_object,
                      parse_constant=bad_number)


SCHEMA = load(ROOT / 'references/contracts.json')


def digest(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def issue(errors, code, path, detail, owner='M10'):
    errors.append({'code': code, 'path': path, 'owner': owner, 'detail': detail})


def shape(value, name, errors, path=''):
    found = validate(value, SCHEMA['$defs'][name], SCHEMA, path)
    for where, detail in found:
        issue(errors, 'schema', where, detail, 'caller')
    return not found


def indexed(rows, key, errors, path, owner='M10'):
    result = {}
    for i, row in enumerate(rows):
        item = row[key]
        if item in result:
            issue(errors, 'duplicate_id', path + '/' + str(i) + '/' + key, item, owner)
        result[item] = row
    return result


def values(inputs, key, default=None):
    return inputs[key]['values'] if key in inputs else ({} if default is None else default)


def source_references(value):
    refs = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == 'source_refs':
                refs.update(child)
            elif key == 'source_id' and 'source_version' in value:
                refs.add(child)
            refs.update(source_references(child))
    elif isinstance(value, list):
        for child in value:
            refs.update(source_references(child))
    return refs


def refs_valid(data, sources, errors, path):
    for ref in sorted(source_references(data)):
        if ref not in sources:
            issue(errors, 'missing_source', path, 'Unknown evidence source ' + ref, 'caller')


def within(scope, ancestor, scopes):
    seen = set()
    while scope is not None and scope in scopes and scope not in seen:
        if scope == ancestor:
            return True
        seen.add(scope)
        scope = scopes[scope]['parent_scope_id']
    return False


def validate_scopes(data, errors, path='/inputs/scope_context'):
    scopes = indexed(data['scopes'], 'scope_id', errors, path + '/scopes', 'caller')
    levels = {'work': 0, 'scene': 1, 'shot': 2}
    for sid, scope in scopes.items():
        parent = scope['parent_scope_id']
        if parent is not None and parent not in scopes:
            issue(errors, 'missing_scope_parent', path + '/' + sid, 'Scope parent is not in the supplied projection', 'caller')
        elif parent is not None and levels[scopes[parent]['level']] >= levels[scope['level']]:
            issue(errors, 'scope_order', path + '/' + sid, 'A parent must have a broader scope level', 'caller')
        seen, cursor = set(), sid
        while cursor is not None and cursor in scopes:
            if cursor in seen:
                issue(errors, 'scope_cycle', path + '/' + sid, 'Scope ancestry is cyclic', 'caller')
                break
            seen.add(cursor)
            cursor = scopes[cursor]['parent_scope_id']
    return scopes


def known_scope(scope, scopes, errors, path, owner):
    if scope not in scopes:
        issue(errors, 'unknown_scope', path, 'Unknown scope ' + scope, owner)
        return False
    return True


def validate_reference_context(inputs, scopes, errors):
    assets = indexed(values(inputs, 'reference_context', {'assets': []})['assets'], 'asset_id', errors,
                     '/inputs/reference_context/assets', 'M2')
    for aid, asset in assets.items():
        where = '/inputs/reference_context/assets/' + aid
        if set(asset['allowed_uses']) & set(asset['forbidden_uses']):
            issue(errors, 'permission_conflict', where, 'A use is both allowed and forbidden', 'M2')
        for scope in asset['scope_ids']:
            known_scope(scope, scopes, errors, where, 'M2')
        if 'identity_context' in inputs:
            declared = {e['entity_id'] for e in values(inputs, 'identity_context')['entities']}
            if not set(asset['target_ids']) <= declared:
                issue(errors, 'permission_identity_target', where, 'Named reference targets require matching supplied identities', 'M2')
    return assets


def uses_valid(uses, purpose, scope, targets, inputs, scopes, errors, path):
    assets = {a['asset_id']: a for a in values(inputs, 'reference_context', {'assets': []})['assets']}
    for use in uses:
        asset = assets.get(use['asset_id'])
        if not asset:
            issue(errors, 'reference_permission_missing', path, 'A direct reference use needs an explicit M2/external permission record', 'M2')
            continue
        if use['use'] != purpose or use['scope_id'] != scope or set(use['target_ids']) != set(targets):
            issue(errors, 'reference_binding', path, 'Use purpose, scope and targets must match the current look declaration', 'M2')
        if use['use'] not in asset['allowed_uses'] or use['use'] in asset['forbidden_uses']:
            issue(errors, 'reference_use_forbidden', path, 'Reference permission does not authorize this visual use; identity is not style', 'M2')
        if not any(within(scope, s, scopes) for s in asset['scope_ids']):
            issue(errors, 'reference_scope', path, 'Reference permission does not cover this scope', 'M2')
        if (not targets and asset['target_ids']) or (targets and not set(targets) <= set(asset['target_ids'])):
            issue(errors, 'reference_targets', path, 'Reference permission does not cover the bound entities', 'M2')


def validate_identities(inputs, scopes, errors):
    identities = indexed(values(inputs, 'identity_context', {'entities': []})['entities'], 'entity_id', errors,
                         '/inputs/identity_context/entities', 'M2')
    for eid, entity in identities.items():
        for scope in entity['scope_ids']:
            known_scope(scope, scopes, errors, '/inputs/identity_context/' + eid, 'M2')
        indexed(entity['surfaces'], 'surface_id', errors, '/inputs/identity_context/' + eid + '/surfaces', 'M2')
    return identities


def validate_style(data, scopes, inputs, errors, enforce_permissions=True, complete=True, path='/StyleHierarchy'):
    layers = indexed(data['layers'], 'scope_id', errors, path + '/layers', 'M10.1')
    if complete and set(layers) != set(scopes):
        issue(errors, 'style_scope_coverage', path, 'One layer is required for each scope explicitly selected in this request', 'M10.1')
    for sid, layer in layers.items():
        where = path + '/' + sid
        if known_scope(sid, scopes, errors, where, 'M10.1') and layer['parent_scope_id'] != scopes[sid]['parent_scope_id']:
            issue(errors, 'style_parent', where, 'Style ancestry must use the supplied scope hierarchy', 'M10.1')
        if layer['parent_scope_id'] is not None and layer['parent_scope_id'] not in layers:
            issue(errors, 'missing_style_parent', where, 'Include the referenced ancestor layer in a self-contained projection', 'M10.1')
        if enforce_permissions:
            uses_valid(layer['reference_uses'], 'style', sid, [], inputs, scopes, errors, where)
    resolved, visiting = {}, set()

    def resolve(sid):
        if sid in resolved:
            return resolved[sid]
        if sid in visiting:
            issue(errors, 'style_cycle', path + '/' + sid, 'Style inheritance is cyclic', 'M10.1')
            return {}
        visiting.add(sid)
        layer = layers[sid]
        parent = layer['parent_scope_id']
        prior = resolve(parent) if parent in layers else {}
        explicit = layer['style']
        changed = {key for key, value in explicit.items() if key in prior and prior[key] != value}
        if set(layer['override_keys']) != changed:
            issue(errors, 'style_override_keys', path + '/' + sid, 'override_keys must list exactly the changed inherited style keys', 'M10.1')
        if bool(changed) != (layer['override_reason'] is not None):
            issue(errors, 'style_override_reason', path + '/' + sid, 'An actual inherited override requires a reason; non-overrides use null', 'M10.1')
        effective = {**prior, **explicit}
        if set(effective) != STYLE_KEYS:
            issue(errors, 'incomplete_style', path + '/' + sid, 'Resolved style needs rendering, visual_language and image_texture', 'M10.1')
        visiting.remove(sid)
        resolved[sid] = effective
        return effective

    for sid in layers:
        resolve(sid)


def semantic_values(value):
    """Compare declared visual values; provenance/permission changes are tracked separately."""
    if isinstance(value, dict):
        return {k: semantic_values(v) for k, v in value.items() if k not in ('source_refs', 'reference_uses', 'permission_id')}
    if isinstance(value, list):
        return [semantic_values(v) for v in value]
    return value


def inheritance(rows, id_key, parent_key, payload_keys, scopes, errors, owner, path, group_keys=()):
    items = indexed(rows, id_key, errors, path, owner)
    by_scope = {}
    for rid, row in items.items():
        group = tuple(row[k] for k in group_keys)
        key = (row['scope_id'], group)
        if key in by_scope:
            issue(errors, 'ambiguous_scope_rule', path + '/' + rid, 'Only one rule per scope and target partition is allowed', owner)
        by_scope[key] = rid
        known_scope(row['scope_id'], scopes, errors, path + '/' + rid, owner)
    for rid, row in items.items():
        where = path + '/' + rid
        parent_id = row[parent_key]
        group = tuple(row[k] for k in group_keys)
        cursor = scopes.get(row['scope_id'], {}).get('parent_scope_id')
        seen, expected = set(), None
        while cursor is not None and cursor in scopes and cursor not in seen:
            if (cursor, group) in by_scope:
                expected = by_scope[(cursor, group)]
                break
            seen.add(cursor)
            cursor = scopes[cursor]['parent_scope_id']
        if parent_id != expected:
            issue(errors, 'inheritance_parent', where, 'Parent must identify the nearest declared ancestor rule for the same target', owner)
        parent = items.get(parent_id)
        if parent_id is not None and parent is None:
            issue(errors, 'missing_inheritance_parent', where, 'Unknown inherited rule ID', owner)
        if parent is not None:
            if parent_id == rid or not within(row['scope_id'], parent['scope_id'], scopes) or row['scope_id'] == parent['scope_id']:
                issue(errors, 'inheritance_cycle_or_scope', where, 'Inherited rule must have a strict ancestor scope', owner)
            changed = any(canonical(semantic_values(row[k])) != canonical(semantic_values(parent[k])) for k in payload_keys)
        else:
            changed = False
        if changed != (row['override_reason'] is not None):
            issue(errors, 'override_reason', where, 'Changed inherited values require a reason; roots and unchanged values use null', owner)
    return items


def visibility_checks(checks, inputs, scopes, covered_scopes, errors, path):
    requirements = indexed(values(inputs, 'visibility_context', {'requirements': []})['requirements'],
                           'requirement_id', errors, '/inputs/visibility_context/requirements', 'M5')
    records = indexed(checks, 'requirement_id', errors, path, 'M5')
    if set(requirements) != set(records):
        issue(errors, 'visibility_coverage', path, 'Each supplied critical visibility requirement needs exactly one scoped design check', 'M5')
    for rid, row in records.items():
        requirement = requirements.get(rid)
        if not requirement:
            continue
        if row['scope_id'] != requirement['scope_id'] or not any(within(row['scope_id'], s, scopes) for s in covered_scopes):
            issue(errors, 'visibility_scope', path + '/' + rid, 'Visibility check must belong to the supplied requirement and the look scope', 'M5')
        if row['result'] != 'preserved_by_design':
            issue(errors, 'visibility_' + row['result'], path + '/' + rid,
                  'An unresolved critical visibility condition is not an accepted design check', 'M5')


def validate_lighting(data, scopes, inputs, errors, readonly=False, path='/LightingPlan'):
    setups = inheritance(data['setups'], 'setup_id', 'parent_setup_id', ['lights'], scopes, errors, 'M10.2', path + '/setups')
    conditions = values(inputs, 'scene_context', {'conditions': []})['conditions']
    for setup_id, setup in setups.items():
        where = path + '/setups/' + setup_id
        if not readonly and not any(within(setup['scope_id'], c['scope_id'], scopes) for c in conditions):
            issue(errors, 'scene_condition_missing', where, 'A lighting setup needs applicable supplied scene conditions', 'M3')
        lights = indexed(setup['lights'], 'light_id', errors, where + '/lights', 'M10.2')
        for light in lights.values():
            uses_valid(light['reference_uses'], 'lighting', setup['scope_id'], [], inputs, scopes, errors, where)
    if not readonly:
        visibility_checks(data['visibility_checks'], inputs, scopes, [r['scope_id'] for r in setups.values()], errors,
                          path + '/visibility_checks')
    else:
        checks = indexed(data['visibility_checks'], 'requirement_id', errors, path + '/visibility_checks', 'M5')
        for rid, row in checks.items():
            where = path + '/visibility_checks/' + rid
            known_scope(row['scope_id'], scopes, errors, where, 'M5')
            if not any(within(row['scope_id'], setup['scope_id'], scopes) for setup in setups.values()):
                issue(errors, 'visibility_scope', where, 'A supplied check lies outside its lighting setups', 'M5')
            if row['result'] != 'preserved_by_design':
                issue(errors, 'visibility_' + row['result'], where, 'The supplied lighting snapshot has an unresolved critical design check', 'M5')


def validate_color(data, scopes, inputs, errors, readonly=False, path='/ColorPlan'):
    payload = ['palette', 'temperature_bias', 'contrast', 'saturation', 'exposure_intent']
    grades = inheritance(data['grades'], 'grade_id', 'parent_grade_id', payload, scopes, errors, 'M10.3', path + '/grades')
    identities = {e['entity_id']: e for e in values(inputs, 'identity_context', {'entities': []})['entities']}
    for gid, grade in grades.items():
        where = path + '/grades/' + gid
        uses_valid(grade['reference_uses'], 'color', grade['scope_id'], [], inputs, scopes, errors, where)
        if 'identity_context' in inputs:
            relevant = {eid for eid, ent in identities.items() if any(within(grade['scope_id'], s, scopes) or within(s, grade['scope_id'], scopes) for s in ent['scope_ids'])}
            if set(grade['protected_identity_ids']) != relevant:
                issue(errors, 'identity_preservation', where, 'Color design must explicitly preserve all and only supplied identities in this scope', 'M2')
        elif grade['protected_identity_ids']:
            issue(errors, 'identity_context_missing', where, 'Named identity protection needs the corresponding source projection', 'M2')


def validate_materials(data, scopes, inputs, errors, path='/MaterialEffectPlan'):
    if not data['materials'] and not data['effects']:
        issue(errors, 'empty_material_effect_plan', path, 'Declare at least one material or effect; do not manufacture an empty successful result', 'M10.4')
    materials = inheritance(data['materials'], 'material_id', 'parent_material_id', ['base_material', 'appearance', 'conditions'],
                            scopes, errors, 'M10.4', path + '/materials', ('target_id', 'surface_id'))
    identities = {e['entity_id']: e for e in values(inputs, 'identity_context')['entities']}
    permissions = indexed(values(inputs, 'continuity_context', {'permissions': []})['permissions'], 'permission_id', errors,
                          '/inputs/continuity_context/permissions', 'M8')
    expected_handoffs = set()
    for mid, material in materials.items():
        where = path + '/materials/' + mid
        entity = identities.get(material['target_id'])
        if not entity:
            issue(errors, 'material_target', where, 'Material target lacks an explicit identity/surface projection', 'M2')
            continue
        if not any(within(material['scope_id'], s, scopes) for s in entity['scope_ids']):
            issue(errors, 'material_target_scope', where, 'Material target is not authorized in this scope projection', 'M2')
        surface = next((s for s in entity['surfaces'] if s['surface_id'] == material['surface_id']), None)
        if not surface:
            issue(errors, 'material_surface', where, 'The referenced surface does not belong to this entity', 'M2')
            continue
        if material['base_material'] != surface['base_material']:
            issue(errors, 'identity_material_change', where, 'A material appearance proposal may not redesign the supplied base material', 'M2')
        uses_valid(material['reference_uses'], 'material', material['scope_id'], [material['target_id']], inputs, scopes, errors, where)
        conditions = indexed(material['conditions'], 'property', errors, where + '/conditions', 'M10.4')
        for prop, condition in conditions.items():
            if prop not in surface['properties']:
                issue(errors, 'surface_baseline_missing', where, 'The baseline value for ' + prop + ' is unknown', 'M2')
                continue
            changed = condition['value'] != surface['properties'][prop]
            if changed and prop not in surface['mutable_properties']:
                issue(errors, 'immutable_surface_property', where, prop + ' is not declared mutable by the supplied asset projection', 'M2')
            permission_id = condition['permission_id']
            if not changed and permission_id is not None:
                issue(errors, 'unneeded_change_permission', where, 'An unchanged baseline property uses permission_id null', 'M8')
            if changed:
                permission = permissions.get(permission_id)
                expected_handoffs.add((mid, material['scope_id'], material['target_id'], material['surface_id'], prop,
                                       condition['value'], permission_id))
                if not permission:
                    issue(errors, 'continuity_permission_missing', where, 'A changed surface condition needs an explicit M8/external permission', 'M8')
                elif (permission['target_id'] != material['target_id'] or permission['surface_id'] != material['surface_id']
                      or permission['property'] != prop or condition['value'] not in permission['allowed_values']
                      or not any(within(material['scope_id'], s, scopes) for s in permission['scope_ids'])):
                    issue(errors, 'continuity_permission_mismatch', where, 'Permission does not authorize this target/surface/property/value/scope', 'M8')
    effects = indexed(data['effects'], 'effect_id', errors, path + '/effects', 'M10.4')
    events = set(values(inputs, 'event_context', {'event_ids': []})['event_ids'])
    for eid, effect in effects.items():
        where = path + '/effects/' + eid
        known_scope(effect['scope_id'], scopes, errors, where, 'M10.4')
        if not set(effect['target_ids']) <= identities.keys():
            issue(errors, 'effect_target', where, 'Effect refers to an unknown identity/prop/scene entity', 'M2')
        for target in effect['target_ids']:
            if target in identities and not any(within(effect['scope_id'], s, scopes) for s in identities[target]['scope_ids']):
                issue(errors, 'effect_target_scope', where, 'Effect entity is outside the supplied scope', 'M2')
        uses_valid(effect['reference_uses'], 'effects', effect['scope_id'], effect['target_ids'], inputs, scopes, errors, where)
        if effect['trigger_kind'] == 'event' and effect['event_id'] not in events:
            issue(errors, 'effect_event_missing', where, 'An event-triggered effect needs the supplied event ID; timing remains with M7', 'M4/M7')
        if effect['trigger_kind'] == 'constant' and effect['event_id'] is not None:
            issue(errors, 'constant_effect_event', where, 'A constant effect must not claim an event trigger', 'M10.4')
        if effect['visibility_impact'] == 'blocks_key':
            issue(errors, 'effect_blocks_key', where, 'Declared key-action obstruction requires a design revision with M5', 'M5')
        if effect['visibility_impact'] == 'managed' and effect['mitigation'] is None:
            issue(errors, 'effect_mitigation_missing', where, 'A managed visibility effect requires an explicit mitigation', 'M5')
    handoffs = set()
    for row in data['continuity_handoffs']:
        key = tuple(row[k] for k in ('material_id', 'scope_id', 'target_id', 'surface_id', 'property', 'value', 'permission_id'))
        if key in handoffs:
            issue(errors, 'duplicate_handoff', path + '/continuity_handoffs', 'Duplicate M8 visual-condition handoff', 'M8')
        handoffs.add(key)
    if handoffs != expected_handoffs:
        issue(errors, 'continuity_handoff_coverage', path + '/continuity_handoffs', 'Every changed material condition needs exactly its matching M8 handoff', 'M8')
    visibility_checks(data['visibility_checks'], inputs, scopes,
                      [r['scope_id'] for r in [*materials.values(), *effects.values()]], errors, path + '/visibility_checks')


def request_errors(request):
    errors = []
    target = request.get('target') if isinstance(request, dict) else None
    name = 'Request' + target[-1] if target in PARTS else 'Request'
    if not shape(request, name, errors):
        return errors
    inputs, sources = request['inputs'], request['sources']
    refs_valid(inputs, sources, errors, '/inputs')
    for key, projection in inputs.items():
        if not key.endswith('_context'):
            continue
        source = sources.get(projection['source_id'])
        if source and source['version'] != projection['source_version']:
            issue(errors, 'source_version', '/inputs/' + key, 'Projection version differs from the supplied source record', 'caller')
    scopes = validate_scopes(values(inputs, 'scope_context'), errors)
    validate_reference_context(inputs, scopes, errors)
    identities = validate_identities(inputs, scopes, errors)
    if 'scene_context' in inputs:
        rows = indexed(values(inputs, 'scene_context')['conditions'], 'scope_id', errors, '/inputs/scene_context/conditions', 'M3')
        for scope in rows:
            known_scope(scope, scopes, errors, '/inputs/scene_context/conditions/' + scope, 'M3')
    if 'visibility_context' in inputs:
        rows = indexed(values(inputs, 'visibility_context')['requirements'], 'requirement_id', errors,
                       '/inputs/visibility_context/requirements', 'M5')
        for row in rows.values():
            known_scope(row['scope_id'], scopes, errors, '/inputs/visibility_context/' + row['requirement_id'], 'M5')
            if 'identity_context' in inputs and row['target_id'] not in identities:
                issue(errors, 'visibility_target', '/inputs/visibility_context', 'Visibility target is not in the supplied identity projection', 'M5')
    if 'continuity_context' in inputs:
        rows = indexed(values(inputs, 'continuity_context')['permissions'], 'permission_id', errors,
                       '/inputs/continuity_context/permissions', 'M8')
        for row in rows.values():
            for scope in row['scope_ids']:
                known_scope(scope, scopes, errors, '/inputs/continuity_context/' + row['permission_id'], 'M8')
            if row['target_id'] not in identities:
                issue(errors, 'permission_target', '/inputs/continuity_context', 'Continuity permission refers to an unknown target', 'M8')
            else:
                entity = identities[row['target_id']]
                surface = next((s for s in entity['surfaces'] if s['surface_id'] == row['surface_id']), None)
                if not surface or row['property'] not in surface['properties'] or row['property'] not in surface['mutable_properties']:
                    issue(errors, 'permission_surface', '/inputs/continuity_context/' + row['permission_id'],
                          'Continuity permission needs a known, explicitly mutable surface property', 'M2/M8')
                if not all(any(within(scope, s, scopes) for s in entity['scope_ids']) for scope in row['scope_ids']):
                    issue(errors, 'permission_target_scope', '/inputs/continuity_context/' + row['permission_id'],
                          'The supplied continuity permission exceeds the entity scope', 'M2/M8')
    if 'style_context' in inputs:
        validate_style(values(inputs, 'style_context'), scopes, inputs, errors, enforce_permissions=True,
                       complete=False, path='/inputs/style_context/values')
    if 'lighting_context' in inputs:
        validate_lighting(values(inputs, 'lighting_context'), scopes, inputs, errors, readonly=True,
                          path='/inputs/lighting_context/values')
    if 'color_context' in inputs:
        validate_color(values(inputs, 'color_context'), scopes, inputs, errors, readonly=True,
                       path='/inputs/color_context/values')
    return errors


def check(proposal, request):
    errors = request_errors(request)
    module = proposal.get('module_id') if isinstance(proposal, dict) else None
    name = 'Proposal' + module[-1] if module in PARTS else 'Proposal'
    valid = shape(proposal, name, errors)
    if errors or not valid:
        return errors
    pairs = [('contract_version', 'contract_version'), ('work_id', 'work_id'), ('base_version', 'base_version'),
             ('module_id', 'target'), ('source_request_id', 'request_id'), ('sources', 'sources'), ('context', 'inputs')]
    for left, right in pairs:
        if canonical(proposal[left]) != canonical(request[right]):
            issue(errors, 'original_request_mismatch', '/' + left, 'Proposal differs from the actual original request: ' + right, module)
    if errors:
        return errors
    inputs, sources = request['inputs'], request['sources']
    data = proposal['changes'][PARTS[module]]
    refs_valid(data, sources, errors, '/changes')
    scopes = {s['scope_id']: s for s in values(inputs, 'scope_context')['scopes']}
    if module == 'M10.1':
        validate_style(data, scopes, inputs, errors)
    elif module == 'M10.2':
        validate_lighting(data, scopes, inputs, errors)
    elif module == 'M10.3':
        validate_color(data, scopes, inputs, errors)
    else:
        validate_materials(data, scopes, inputs, errors)
    for record in proposal['issues']:
        issue(errors, 'unresolved_issue', '/issues', record['code'] + ': ' + record['detail'], record['owner'])
    return errors


def escape(key):
    return str(key).replace('~', '~0').replace('/', '~1')


def read_paths(request, proposal):
    module = request['target']
    paths = ['/contexts/' + module + '/brief']
    paths += ['/contexts/' + module + '/' + key for key in request['inputs'] if key.endswith('_context')]
    paths += ['/sources/' + escape(key) for key in sorted(source_references(request['inputs']) | source_references(proposal['changes']))]
    paths += ['/content/' + part for key, (part, _) in SIBLINGS.items() if key in request['inputs']]
    return sorted(set(paths))


def changed_paths(before, after, path=''):
    if canonical(before) == canonical(after):
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        out = []
        for key in sorted(before.keys() | after.keys()):
            child = path + '/' + escape(key)
            if key not in before or key not in after:
                out.append(child)
            else:
                out.extend(changed_paths(before[key], after[key], child))
        return out
    return [path or '/']  # Arrays are declared collection dependencies, not guessed stable indices.


def overlaps(a, b):
    return a == b or a.startswith(b + '/') or b.startswith(a + '/') or a == '/' or b == '/'


def stale_dependencies(consumer, consumers):
    return [module for module, part in PARTS.items() if module != consumer['consumer_id']
            and consumers.get(module, {}).get('status') == 'stale'
            and any(overlaps(path, '/content/' + part) for path in consumer['read_paths'])]


def propagate_stale(consumers):
    """Invalidate only registered readers, including those whose direct producer is stale."""
    changed = True
    while changed:
        changed = False
        for consumer in consumers.values():
            if consumer['status'] != 'stale' and stale_dependencies(consumer, consumers):
                consumer['status'] = 'stale'
                changed = True


def outcome(**kwargs):
    return {'status': 'passed_with_unverified', **kwargs, 'limitations': LIMITS,
            'not_run': NOT_RUN}


def failed(errors):
    return {'status': 'failed', 'errors': errors, 'limitations': LIMITS, 'not_run': NOT_RUN}


def impact(before, after):
    errors = []
    shape(before, 'State', errors, '/before'); shape(after, 'State', errors, '/after')
    if errors:
        return failed(errors)
    if before['work_id'] != after['work_id']:
        return failed([{'code': 'work_id', 'path': '/work_id', 'owner': 'caller', 'detail': 'Impact snapshots must refer to the same work'}])
    indexed(before['consumers'], 'consumer_id', errors, '/before/consumers')
    indexed(after['consumers'], 'consumer_id', errors, '/after/consumers')
    if errors:
        return failed(errors)
    changes = changed_paths(before, after)
    consumers = {x['consumer_id']: x for x in before['consumers']}
    consumers.update({x['consumer_id']: x for x in after['consumers']})
    result = []
    for cid, consumer in sorted(consumers.items()):
        old = next((x for x in before['consumers'] if x['consumer_id'] == cid), None)
        consumer = deepcopy(consumer)
        if old:
            consumer['read_paths'] = sorted(set(consumer['read_paths']) | set(old['read_paths']))
        hits = sorted({p for p in changes if any(overlaps(p, read) for read in consumer['read_paths'])})
        result.append({'consumer_id': cid, 'read_paths': consumer['read_paths'], 'changed_dependencies': hits,
                       'status': 'stale' if hits or consumer['status'] == 'stale' or (old and old['status'] == 'stale') else 'current'})
    result_map = {entry['consumer_id']: entry for entry in result}
    propagate_stale(result_map)
    for entry in result:
        entry['stale_dependencies'] = stale_dependencies(entry, result_map)
    return outcome(changed_paths=changes, consumers=result)


def state_errors(state):
    errors = []
    if not shape(state, 'State', errors):
        return errors
    latest, latest_sources, seen_proposals, seen_requests = {}, {}, set(), set()
    previous_version = 0
    for receipt in state['receipts']:
        if receipt['proposal_id'] in seen_proposals or receipt['request_id'] in seen_requests:
            issue(errors, 'receipt_duplicate', '/receipts', 'Accepted request and proposal IDs must be unique')
        seen_proposals.add(receipt['proposal_id']); seen_requests.add(receipt['request_id'])
        version = receipt['accepted_version']
        if receipt['base_version'] + 1 != version or version > state['version'] or version not in (previous_version, previous_version + 1):
            issue(errors, 'receipt_version', '/receipts', 'Receipt versions must form consecutive atomic acceptance batches')
        previous_version = version
        latest[receipt['module_id']] = receipt
        latest_sources.update(receipt['source_digests'])
    if previous_version != state['version']:
        issue(errors, 'state_version', '/version', 'Parent version must match the latest receipt, or zero for an empty plan')
    consumers = indexed(state['consumers'], 'consumer_id', errors, '/consumers')
    for cid, consumer in consumers.items():
        if consumer['status'] == 'current' and stale_dependencies(consumer, consumers):
            issue(errors, 'current_reads_stale', '/consumers/' + cid, 'A current consumer may not depend on a stale sibling', cid)
    for sid, expected in latest_sources.items():
        if sid not in state['sources'] or digest(state['sources'][sid]) != expected:
            issue(errors, 'state_source_history', '/sources/' + sid, 'Current evidence content must match its latest accepted receipt')
    for module, part in PARTS.items():
        present = part in state['content']
        if present != (module in latest) or present != (module in state['contexts']):
            issue(errors, 'state_partition', '/content/' + part, 'Accepted partition, context and receipt must exist together')
        if not present or module not in latest or module not in state['contexts']:
            continue
        receipt = latest[module]
        if digest(state['content'][part]) != receipt['output_digest'] or digest(state['contexts'][module]) != receipt['context_digest']:
            issue(errors, 'state_digest', '/content/' + part, 'Accepted content/context differs from its receipt')
        request = {'target': module, 'inputs': state['contexts'][module]}
        proposal = {'changes': {part: state['content'][part]}}
        paths = read_paths(request, proposal)
        consumer = consumers.get(module)
        if paths != receipt['read_paths'] or not consumer or paths != consumer['read_paths']:
            issue(errors, 'actual_read_paths', '/receipts/' + module, 'Child dependencies must equal their accepted actual input/output source paths')
        expected_sources = source_references(request['inputs']) | source_references(proposal['changes'])
        if expected_sources != receipt['source_digests'].keys():
            issue(errors, 'receipt_sources', '/receipts/' + module, 'Receipt must name every actual source dependency exactly once')
        for sid in expected_sources:
            if sid not in state['sources']:
                issue(errors, 'state_source_missing', '/sources/' + sid, 'An accepted dependency source is absent')
            elif consumer and consumer['status'] == 'current' and digest(state['sources'][sid]) != receipt['source_digests'].get(sid):
                issue(errors, 'state_source_digest', '/sources/' + sid, 'A current partition has an unacknowledged changed source')
    expected_stale = sorted(c['consumer_id'] for c in state['consumers'] if c['consumer_id'] in PARTS and c['status'] == 'stale')
    if sorted(state['stale_modules']) != expected_stale:
        issue(errors, 'stale_registry', '/stale_modules', 'Stale module list must match actual registered consumers')
    current = [{'module_id': module, 'context': state['contexts'][module]} for module in PARTS
               if module in state['contexts'] and consumers.get(module, {}).get('status') == 'current']
    sibling_checks(state, current, errors)
    return errors


def unwrap(value, kind, singular, plural, errors):
    if isinstance(value, dict) and value.get('kind') == kind + 'Batch':
        return value[plural] if shape(value, singular + 'Batch', errors) else []
    return [value] if shape(value, singular, errors) else []


def sibling_checks(candidate, proposals, errors):
    for proposal in proposals:
        module, context = proposal['module_id'], proposal['context']
        for key, (part, tables) in SIBLINGS.items():
            if key not in context or part not in candidate['content']:
                continue
            for table, id_key in tables.items():
                actual = {r[id_key]: r for r in candidate['content'][part][table]}
                for row in context[key]['values'][table]:
                    if row[id_key] not in actual or canonical(row) != canonical(actual[row[id_key]]):
                        issue(errors, 'sibling_snapshot_conflict', '/contexts/' + module + '/' + key,
                              'Supplied read-only rows differ from the candidate accepted sibling partition', 'caller')


def accept(state, proposals_doc, requests_doc):
    errors = state_errors(state)
    proposals = unwrap(proposals_doc, 'M10Proposal', 'Proposal', 'proposals', errors)
    requests = unwrap(requests_doc, 'M10Request', 'Request', 'requests', errors)
    if errors:
        return failed(errors)
    request_map = indexed(requests, 'request_id', errors, '/requests')
    indexed(proposals, 'proposal_id', errors, '/proposals')
    indexed(proposals, 'module_id', errors, '/proposals')
    if len({p['source_request_id'] for p in proposals}) != len(proposals):
        issue(errors, 'request_reuse', '/proposals', 'One request cannot authorize multiple proposals in an acceptance batch')
    if set(request_map) != {p['source_request_id'] for p in proposals}:
        issue(errors, 'request_set', '/requests', 'Supply the exact original request set for this proposal batch')
    if errors:
        return failed(errors)
    old_receipts = {x['proposal_id']: x for x in state['receipts']}
    old_request_ids = {x['request_id'] for x in state['receipts']}
    repeats = []
    for proposal in proposals:
        request = request_map[proposal['source_request_id']]
        errors += check(proposal, request)
        if request['work_id'] != state['work_id']:
            issue(errors, 'work_id', '/work_id', 'Request belongs to a different work')
        old = old_receipts.get(proposal['proposal_id'])
        if old:
            same = old['proposal_digest'] == digest(proposal) and old['request_digest'] == digest(request)
            repeats.append(same)
            if not same:
                issue(errors, 'idempotency_conflict', '/proposal_id', 'Accepted IDs were reused with changed content')
        else:
            repeats.append(False)
            if request['request_id'] in old_request_ids:
                issue(errors, 'request_id_conflict', '/request_id', 'An accepted request cannot authorize another proposal')
            if proposal['base_version'] != state['version']:
                issue(errors, 'stale_base', '/base_version', 'Proposal does not target the current parent version')
    if any(repeats) and not all(repeats):
        issue(errors, 'mixed_retry', '/proposals', 'Retry the prior immutable batch separately from new revisions')
    if errors:
        return failed(errors)
    if all(repeats):
        return outcome(idempotent=True, state=state)
    candidate = deepcopy(state)
    incoming_sources = {}
    for proposal in proposals:
        module = proposal['module_id']
        candidate['content'][PARTS[module]] = deepcopy(proposal['changes'][PARTS[module]])
        candidate['contexts'][module] = deepcopy(proposal['context'])
        for sid, source in proposal['sources'].items():
            if sid in incoming_sources and canonical(incoming_sources[sid]) != canonical(source):
                issue(errors, 'source_conflict', '/sources/' + sid, 'Atomic batch disagrees about a source/version')
            old = state['sources'].get(sid)
            if old and old['version'] == source['version'] and canonical(old) != canonical(source):
                issue(errors, 'immutable_source_version', '/sources/' + sid, 'Changed source content requires a new version')
            incoming_sources[sid] = source
    candidate['sources'].update(deepcopy(incoming_sources))
    sibling_checks(candidate, proposals, errors)
    if errors:
        return failed(errors)
    candidate['version'] += 1
    for proposal in proposals:
        module = proposal['module_id']
        request = request_map[proposal['source_request_id']]
        paths = read_paths(request, proposal)
        used_sources = source_references(request['inputs']) | source_references(proposal['changes'])
        candidate['receipts'].append({'proposal_id': proposal['proposal_id'], 'request_id': request['request_id'],
            'module_id': module, 'proposal_digest': digest(proposal), 'request_digest': digest(request),
            'output_digest': digest(proposal['changes'][PARTS[module]]), 'context_digest': digest(request['inputs']),
            'source_digests': {sid: digest(request['sources'][sid]) for sid in sorted(used_sources)},
            'base_version': state['version'], 'accepted_version': candidate['version'], 'read_paths': paths})
    changes = changed_paths(state, candidate)
    accepted_modules = {p['module_id'] for p in proposals}
    consumers = {c['consumer_id']: deepcopy(c) for c in state['consumers']}
    for receipt in candidate['receipts']:
        module = receipt['module_id']
        if module in accepted_modules:
            consumers[module] = {'consumer_id': module, 'read_paths': receipt['read_paths'], 'status': 'current'}
    for cid, consumer in consumers.items():
        if cid not in accepted_modules and any(overlaps(change, read) for change in changes for read in consumer['read_paths']):
            consumer['status'] = 'stale'
    propagate_stale(consumers)
    for module in accepted_modules:
        stale = stale_dependencies(consumers[module], consumers)
        if stale:
            issue(errors, 'stale_sibling_dependency', '/contexts/' + module,
                  'Revalidate the consumed stale sibling in this batch or a preceding revision: ' + ', '.join(stale), stale[0])
    if errors:
        return failed(errors)
    candidate['consumers'] = list(consumers.values())
    candidate['stale_modules'] = sorted(c['consumer_id'] for c in candidate['consumers'] if c['consumer_id'] in PARTS and c['status'] == 'stale')
    final_errors = state_errors(candidate)
    return failed(final_errors) if final_errors else outcome(idempotent=False, state=candidate)


def route(request):
    errors = request_errors(request)
    if errors:
        return {**failed(errors), 'ready': False, 'invocation_status': 'not_invoked'}
    module = request['target']
    registry = load(ROOT / 'references/module-registry.json')
    entry = next(x for x in registry['modules'] if x['module_id'] == module)
    return outcome(ready=True, invocation_status='not_invoked', module_id=module, parent='M10',
                   work_id=request['work_id'], request_id=request['request_id'], contract_version=VERSION,
                   route_version=registry['route_version'], base_version=request['base_version'],
                   input_versions={k: v['source_version'] for k, v in request['inputs'].items() if k.endswith('_context')},
                   write_path='/content/' + PARTS[module], resources=entry['resources'], rationale=entry['responsibility'])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('route'); p.add_argument('request')
    p = sub.add_parser('check'); p.add_argument('proposal'); p.add_argument('--request', required=True)
    p = sub.add_parser('accept'); p.add_argument('state'); p.add_argument('proposal'); p.add_argument('--requests', required=True)
    p = sub.add_parser('impact'); p.add_argument('--before', required=True); p.add_argument('--after', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'route':
            result = route(load(args.request))
        elif args.command == 'check':
            proposal, request = load(args.proposal), load(args.request)
            errors = check(proposal, request)
            result = failed(errors) if errors else outcome(module_id=proposal['module_id'], read_paths=read_paths(request, proposal))
        elif args.command == 'accept':
            result = accept(load(args.state), load(args.proposal), load(args.requests))
        else:
            result = impact(load(args.before), load(args.after))
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        result = failed([{'code': 'input_error', 'path': '', 'owner': 'caller', 'detail': str(exc)}])
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 2 if result['status'] == 'failed' else 0


if __name__ == '__main__':
    raise SystemExit(main())
