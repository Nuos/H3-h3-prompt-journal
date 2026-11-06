#!/usr/bin/env python3
"""Validate explicit M9 declarations. No inference, network, files written, or media analysis."""
from __future__ import annotations
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

# Python -I portability: import only our sibling helper, never another skill.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _schema import canonical, validate

ROOT = Path(__file__).resolve().parent.parent
VERSION = '1.0.0'
PARTS = {'M9.1': 'ShotMap', 'M9.2': 'EditGraph', 'M9.3': 'GenerationPlan'}
INPUTS = {'M9.1': ('action_context', 'camera_context'),
          'M9.2': ('shot_context', 'source_context', 'continuity_context'),
          'M9.3': ('shot_context', 'edit_context', 'continuity_context', 'capability_context', 'time_context', 'asset_context')}
LIMITS = ['Only explicit JSON relationships and supplied provenance were checked.',
          'No automatic NLP, media observation, H3 execution, M7 time conversion, or full G1–G4 certification.']


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


def issue(errors, code, path, detail, owner='M9'):
    errors.append({'code': code, 'path': path, 'owner': owner, 'detail': detail})


def shape(value, name, errors, path=''):
    found = validate(value, SCHEMA['$defs'][name], SCHEMA, path)
    for where, detail in found:
        issue(errors, 'schema', where, detail)
    return not found


def indexed(rows, key, errors, path):
    result = {}
    for i, row in enumerate(rows):
        value = row[key]
        if value in result:
            issue(errors, 'duplicate_id', path + '/' + str(i) + '/' + key, value)
        result[value] = row
    return result


def source_references(value):
    refs = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == 'source_refs':
                refs.update(child)
            elif key in ('source_id', 'range_source_ref') and isinstance(child, str):
                # source_id also denotes media in segments; only projections below add it.
                if key == 'range_source_ref' or 'source_version' in value:
                    refs.add(child)
            refs.update(source_references(child))
    elif isinstance(value, list):
        for child in value:
            refs.update(source_references(child))
    return refs


def refs_valid(value, sources, errors, path):
    for ref in sorted(source_references(value)):
        if ref not in sources:
            issue(errors, 'missing_source', path, 'Unknown evidence source ' + ref)


def request_errors(request):
    errors = []
    target = request.get('target') if isinstance(request, dict) else None
    name = 'Request' + target[-1] if target in PARTS else 'Request'
    if not shape(request, name, errors):
        return errors
    inputs, sources = request['inputs'], request['sources']
    refs_valid(inputs, sources, errors, '/inputs')
    for key in INPUTS[target]:
        projection = inputs[key]
        source = sources.get(projection['source_id'])
        if source and projection['source_version'] != source['version']:
            issue(errors, 'source_version', '/inputs/' + key, 'Projection version differs from actual source version')
    if target == 'M9.3':
        for profile in inputs['capability_context']['values']['profiles']:
            if profile['status'] != 'known':
                issue(errors, 'capability_unknown', '/inputs/capability_context',
                      'Formal task proposals require known supplied capability; retain unknown candidates outside this validator.', 'M11')
    return errors


def validate_shots(data, sources, errors, inputs=None, path='/ShotMap'):
    phases = indexed(data['phases'], 'phase_id', errors, path + '/phases')
    shots = indexed(data['shots'], 'shot_id', errors, path + '/shots')
    panels = indexed(data['panels'], 'panel_id', errors, path + '/panels')
    events = indexed(data['events'], 'event_id', errors, path + '/events')
    refs_valid(data, sources, errors, path)
    used_phases = set()
    for shot_id, shot in shots.items():
        used_phases.update(shot['phase_ids'])
        if not set(shot['phase_ids']) <= phases.keys():
            issue(errors, 'orphan_phase', path + '/shots/' + shot_id, 'Shot references an unknown action phase', 'M9.1')
        expected = {key for key, panel in panels.items() if panel['shot_id'] == shot_id}
        if set(shot['panel_ids']) != expected:
            issue(errors, 'panel_membership', path + '/shots/' + shot_id, 'Panel assignment must agree in both directions', 'M9.1')
    if used_phases != phases.keys():
        issue(errors, 'unassigned_phase', path + '/phases', 'Every declared phase needs at least one shot; shared phases are allowed', 'M9.1')
    for panel in panels.values():
        shot = shots.get(panel['shot_id'])
        if not shot or not set(panel['phase_ids']) <= set(shot['phase_ids']):
            issue(errors, 'orphan_panel', path + '/panels/' + panel['panel_id'], 'Panel shot/phase assignment is invalid', 'M9.1')
    for event in events.values():
        a, b = shots.get(event['from_shot']), shots.get(event['to_shot'])
        where = path + '/events/' + event['event_id']
        if not a or not b or not set(event['phase_ids']) <= set(a['phase_ids'] + b['phase_ids']):
            issue(errors, 'orphan_event', where, 'Event refers to an unknown shot or unrelated phase', 'M9.1')
        same = event['from_shot'] == event['to_shot']
        if (event['kind'] == 'cut' and same) or (event['kind'] != 'cut' and not same):
            issue(errors, 'event_kind', where, 'A cut changes the shot; camera changes and same-shot joins do not', 'M9.1')
    if inputs:
        action = inputs['action_context']['values']
        camera = inputs['camera_context']['values']
        if set(phases) != set(action['phase_ids']):
            issue(errors, 'action_projection', path + '/phases', 'M9 must preserve the supplied phase IDs', 'M4')
        if set(events) != set(action['event_ids'] + camera['camera_event_ids']):
            issue(errors, 'event_projection', path + '/events', 'Explicit event IDs must match the supplied action/camera projection', 'M9.1')
        for event_id in camera['camera_event_ids']:
            if event_id in events and events[event_id]['kind'] != 'camera_change':
                issue(errors, 'camera_is_not_cut', path + '/events/' + event_id, 'A supplied within-shot camera event cannot become a cut', 'M5')
    return shots, phases, events


def validate_continuity(data, sources, errors, path='/continuity_context'):
    refs_valid(data, sources, errors, path)
    return (indexed(data['policies'], 'policy_id', errors, path + '/policies'),
            indexed(data['states'], 'state_id', errors, path + '/states'))


def check_span(span, errors, path):
    if span['end'] <= span['start']:
        issue(errors, 'invalid_window', path, 'Use a positive half-open source interval [start, end); freeze is a separate intent', 'M9.2')
    if span['unit'] == 'frame' and any(type(span[x]) is not int for x in ('start', 'end')):
        issue(errors, 'frame_integer', path, 'Frame coordinates must be integers; M9 does not round or convert', 'M7')


def validate_edits(data, shotmap, continuity, sources, errors, ranges=None, path='/EditGraph'):
    shots, phases, events = validate_shots(shotmap, sources, errors, path='/context/ShotMap')
    policies, _ = validate_continuity(continuity, sources, errors)
    segments = indexed(data['segments'], 'segment_id', errors, path + '/segments')
    boundaries = indexed(data['boundaries'], 'boundary_id', errors, path + '/boundaries')
    requests = indexed(data['time_requests'], 'request_id', errors, path + '/time_requests')
    refs_valid(data, sources, errors, path)
    range_map = None
    if ranges is not None:
        range_map = indexed(ranges, 'media_id', errors, '/source_context/sources')
        for source in range_map.values():
            check_span(source['span'], errors, '/source_context/' + source['media_id'])
            if not set(source['shot_ids']) <= shots.keys():
                issue(errors, 'source_shots', '/source_context/' + source['media_id'], 'Source range references an unknown shot', 'M9.2')
            if source['basis'] == 'observed' and not any(sources.get(x, {}).get('kind') == 'media_observation' for x in source['source_refs']):
                issue(errors, 'observation_source', '/source_context/' + source['media_id'], 'Observed ranges require supplied media-observation evidence', 'M12')
    if set(data['assembly']) != segments.keys():
        issue(errors, 'assembly_coverage', path + '/assembly', 'Assembly must list every segment exactly once; reuse source with a new segment ID', 'M9.2')
    for segment_id, segment in segments.items():
        where = path + '/segments/' + segment_id
        if not set(segment['shot_ids']) <= shots.keys():
            issue(errors, 'segment_shot', where, 'Unknown shot ID', 'M9.2')
        available = {p for s in segment['shot_ids'] if s in shots for p in shots[s]['phase_ids']}
        if not set(segment['phase_ids']) <= available:
            issue(errors, 'segment_phase', where, 'Segment phase does not belong to its shots', 'M9.2')
        window = segment['window']
        check_span(window, errors, where + '/window')
        if window['basis'] == 'observed' and sources.get(window['range_source_ref'], {}).get('kind') != 'media_observation':
            issue(errors, 'observation_source', where, 'Observed selected windows require a media-observation source; plans are not observations', 'M12')
        if range_map is not None:
            source = range_map.get(segment['source_id'])
            if not source:
                issue(errors, 'missing_media_source', where, 'Selected source ID has no supplied range and media version', 'M9.2')
            else:
                span = source['span']
                if window['unit'] != span['unit'] or window['domain'] != span['domain']:
                    issue(errors, 'coordinate_mismatch', where, 'No implicit frame/time/domain conversion; request M7 mapping', 'M7')
                elif window['start'] < span['start'] or window['end'] > span['end']:
                    issue(errors, 'window_out_of_range', where, 'Selected window lies outside the supplied source span', 'M9.2')
                if window['range_source_ref'] not in source['source_refs']:
                    issue(errors, 'window_provenance', where, 'Selected range evidence does not belong to the supplied source range', 'M9.2')
                if not set(segment['shot_ids']) <= set(source['shot_ids']):
                    issue(errors, 'source_shots', where, 'The source range does not declare all selected shots', 'M9.2')
                if window['basis'] == 'observed' and source['basis'] != 'observed':
                    issue(errors, 'planned_is_not_observed', where, 'A planned source cannot authorize an observed window', 'M12')
        playback = segment['playback']
        if playback['kind'] == 'speed_intent' and playback['factor'] <= 0:
            issue(errors, 'playback_factor', where, 'Speed intent requires a positive factor; M7 owns duration conversion', 'M7')
        if playback['kind'] == 'freeze_intent':
            event = events.get(playback['anchor_event_id'])
            if not event or not set(event['phase_ids']) & set(segment['phase_ids']):
                issue(errors, 'freeze_anchor', where, 'Freeze intent needs a declared retained event, not an inferred action hold', 'M9.2')
    outer = {}
    inner = {}
    for boundary in boundaries.values():
        where = path + '/boundaries/' + boundary['boundary_id']
        a, b = segments.get(boundary['from_segment']), segments.get(boundary['to_segment'])
        event = events.get(boundary['event_id'])
        policy = policies.get(boundary['policy_id'])
        if not a or not b:
            issue(errors, 'orphan_boundary', where, 'Boundary segment is missing', 'M9.2')
            continue
        pair = (boundary['from_shot'], boundary['to_shot'])
        if not event or (event['from_shot'], event['to_shot']) != pair:
            issue(errors, 'boundary_event', where, 'Boundary must match its explicit event endpoints', 'M9.2')
        elif (event['kind'] == 'cut' and boundary['execution_stage'] == 'no_cut') or (event['kind'] == 'camera_change' and boundary['execution_stage'] != 'no_cut'):
            issue(errors, 'cut_stage', where, 'Within-shot camera motion cannot be declared a cut, and a cut cannot be no_cut', 'M9.2')
        if boundary['continuity_strategy'] == 'same_shot_continuation' and pair[0] != pair[1]:
            issue(errors, 'continuity_strategy', where, 'Same-shot continuation must preserve the shot ID', 'M9.2')
        if not policy or policy['boundary_id'] != boundary['boundary_id'] or (policy['from_shot'], policy['to_shot']) != pair:
            issue(errors, 'continuity_reference', where, 'Boundary policy ID/endpoints must match a supplied M8/external projection', 'M8')
        elif policy['status'] != 'approved':
            issue(errors, 'continuity_pending', where, 'M9 cannot approve a pending continuity policy', 'M8')
        if a is b:
            neighbors = list(zip(a['shot_ids'], a['shot_ids'][1:]))
            if pair not in neighbors or boundary['execution_stage'] != 'model_internal' or not event or event['kind'] != 'cut':
                issue(errors, 'internal_boundary', where, 'An internal boundary is an explicit model cut between neighboring source shots', 'M9.2')
            inner.setdefault((boundary['from_segment'], *pair), []).append(boundary['boundary_id'])
        else:
            outer.setdefault((boundary['from_segment'], boundary['to_segment']), []).append(boundary['boundary_id'])
            if pair != (a['shot_ids'][-1], b['shot_ids'][0]):
                issue(errors, 'boundary_endpoints', where, 'Assembly boundary must connect outgoing last shot and incoming first shot', 'M9.2')
            if boundary['execution_stage'] == 'model_internal':
                issue(errors, 'external_boundary', where, 'A boundary between separate source selections belongs to post_edit/no_cut', 'M9.2')
    expected_outer = set(zip(data['assembly'], data['assembly'][1:]))
    if set(outer) != expected_outer or any(len(v) != 1 for v in outer.values()):
        issue(errors, 'assembly_boundaries', path + '/boundaries', 'Every adjacent assembly pair needs exactly one boundary; orphan pairs are forbidden', 'M9.2')
    expected_inner = {(sid, a, b) for sid, seg in segments.items() for a, b in zip(seg['shot_ids'], seg['shot_ids'][1:])}
    if set(inner) != expected_inner or any(len(v) != 1 for v in inner.values()):
        issue(errors, 'internal_boundaries', path + '/boundaries', 'Every multi-shot source selection needs explicit internal cuts', 'M9.2')
    if sorted(x['segment_id'] for x in requests.values()) != sorted(segments):
        issue(errors, 'm7_segment_requests', path + '/time_requests', 'Each segment needs exactly one M7 timing handoff', 'M7')
    return segments, boundaries


def validate_generation(data, inputs, sources, errors):
    path = '/GenerationPlan'
    shotmap = inputs['shot_context']['values']
    edits = inputs['edit_context']['values']
    continuity = inputs['continuity_context']['values']
    segments, boundaries = validate_edits(edits, shotmap, continuity, sources, errors)
    shots = {s['shot_id']: s for s in shotmap['shots']}
    _, states = validate_continuity(continuity, sources, errors)
    profiles = indexed(inputs['capability_context']['values']['profiles'], 'profile_id', errors, '/capability_context/profiles')
    times = indexed(inputs['time_context']['values']['records'], 'request_id', errors, '/time_context/records')
    assets = set(inputs['asset_context']['values']['asset_ids'])
    tasks = indexed(data['tasks'], 'task_id', errors, path + '/tasks')
    indexed(data['coverage'], 'coverage_id', errors, path + '/coverage')
    indexed(data['tasks'], 'output_source_id', errors, path + '/tasks')
    refs_valid(data, sources, errors, path)
    by_segment = {key: [] for key in segments}
    by_task = {key: [] for key in tasks}
    for coverage in data['coverage']:
        where = path + '/coverage/' + coverage['coverage_id']
        task, segment = tasks.get(coverage['task_id']), segments.get(coverage['segment_id'])
        if not task or not segment:
            issue(errors, 'coverage_reference', where, 'Coverage refers to an unknown task or selected segment', 'M9.3')
            continue
        by_task[coverage['task_id']].append(coverage)
        if not set(segment['shot_ids']) <= set(task['shot_ids']) or set(coverage['phase_ids']) != set(segment['phase_ids']):
            issue(errors, 'coverage_content', where, 'Task must include the segment shots and every selected segment phase', 'M9.3')
        order = [task['shot_ids'].index(s) for s in segment['shot_ids'] if s in task['shot_ids']]
        if order != sorted(order):
            issue(errors, 'task_shot_order', where, 'The task cannot reverse the shot order inside a source selection', 'M9.3')
        if coverage['selected']:
            by_segment[coverage['segment_id']].append(coverage)
            if task['output_source_id'] != segment['source_id']:
                issue(errors, 'output_source', where, 'Selected generation coverage must bind the task output to the selected source ID', 'M9.3')
            if coverage['coverage_kind'] == 'candidate_overlap':
                issue(errors, 'candidate_selected', where, 'Choose a candidate explicitly as full/partial/repeat before accepting it', 'M9.3')
        elif coverage['coverage_kind'] != 'candidate_overlap':
            issue(errors, 'unselected_coverage', where, 'Only explicitly marked alternatives may remain unselected', 'M9.3')
    reused = set(data['reused_segment_ids'])
    for sid in reused:
        if sid not in segments or segments[sid]['window']['basis'] != 'observed':
            issue(errors, 'reused_source', path + '/reused_segment_ids', 'Reuse needs a supplied observed segment; planned candidates are not existing media', 'M12')
    for sid, assigned in by_segment.items():
        expected = 0 if sid in reused else 1
        if len(assigned) != expected:
            issue(errors, 'generation_coverage', path + '/coverage', sid + ' must be either explicitly reused or have exactly one selected task', 'M9.3')
    shot_tasks = {}
    for tid, task in tasks.items():
        where = path + '/tasks/' + tid
        if not set(task['shot_ids']) <= shots.keys():
            issue(errors, 'task_shot', where, 'Task refers to an unknown shot', 'M9.3')
        if not set(task['asset_ids']) <= assets:
            issue(errors, 'task_asset', where, 'Task uses an asset outside the supplied M2/external projection', 'M2')
        rows = by_task[tid]
        assigned_shots = {s for row in rows for s in segments[row['segment_id']]['shot_ids']}
        if assigned_shots != set(task['shot_ids']):
            issue(errors, 'task_coverage', where, 'Every declared task shot needs a coverage row; each task needs content', 'M9.3')
        profile = profiles.get(task['profile_id'])
        timing = times.get(task['time_request_id'])
        if not profile:
            issue(errors, 'missing_capability', where, 'Unknown capability profile', 'M11')
        else:
            if profile['status'] != 'known':
                issue(errors, 'capability_unknown', where, 'Unknown capability cannot authorize an executable task proposal', 'M11')
            if task['mode_intent'] not in profile['supported_modes'] or len(task['shot_ids']) > profile['max_shots']:
                issue(errors, 'capability_mismatch', where, 'Mode intent or shot count exceeds the supplied capability', 'M11')
            if profile['duration_limit']['value'] <= 0:
                issue(errors, 'capability_limit', where, 'Known duration limit must be positive', 'M11')
        if not timing or timing['task_id'] != tid:
            issue(errors, 'time_reference', where, 'Task duration must come from its own M7/external record', 'M7')
        elif profile:
            duration, limit = timing['duration'], profile['duration_limit']
            if duration['unit'] != limit['unit']:
                issue(errors, 'time_unit', where, 'M9 cannot compare different time units; request M7 conversion', 'M7')
            elif duration['value'] <= 0 or duration['value'] > limit['value']:
                issue(errors, 'task_duration', where, 'The supplied M7 duration exceeds the supplied capability, or is non-positive', 'M11')
            for row in rows:
                if row['selected']:
                    window = segments[row['segment_id']]['window']
                    if window['domain'] != 'generation_local' or window['unit'] != duration['unit']:
                        issue(errors, 'generation_mapping_required', where, 'Supply M7 generation-local coordinates in the task duration unit before comparing a generated selection', 'M7')
                    elif window['end'] > duration['value']:
                        issue(errors, 'generation_window_limit', where, 'Selected output window exceeds its supplied M7 task duration', 'M7')
            if duration['unit'] == 'frame' and type(duration['value']) is not int:
                issue(errors, 'frame_integer', where, 'Frame duration must be an integer', 'M7')
        for edge, key, shot in [('initial', 'entry_state_ids', task['shot_ids'][0]), ('final', 'exit_state_ids', task['shot_ids'][-1])]:
            for state_id in task[key]:
                state = states.get(state_id)
                if not state or state['shot_id'] != shot or state['edge'] != edge:
                    issue(errors, 'task_boundary_state', where + '/' + key, 'Task boundary needs a matching supplied state ID, shot, and edge', 'M8')
        if any(row['selected'] for row in rows):
            for shot in task['shot_ids']:
                shot_tasks.setdefault(shot, []).append(task)
    for shot, assigned in shot_tasks.items():
        if len(assigned) > 1:
            for task in assigned:
                profile = profiles.get(task['profile_id'])
                if profile and not profile['supports_same_shot_split']:
                    issue(errors, 'split_capability', path + '/tasks/' + task['task_id'], 'Supplied capability does not permit this same-shot split', 'M11')
    for boundary in boundaries.values():
        if boundary['execution_stage'] == 'model_internal':
            # An internal cut in one source must stay inside one selected generating task.
            assigned = by_segment.get(boundary['from_segment'], [])
            if boundary['from_segment'] not in reused and len(assigned) != 1:
                issue(errors, 'internal_task_cut', path + '/coverage', 'Internal model cut has no unique selected generation task', 'M9.3')
    for key, index_key in [('m7_requests', 'task_id'), ('m11_handoffs', 'task_id')]:
        rows = indexed(data[key], index_key, errors, path + '/' + key)
        if set(rows) != set(tasks):
            issue(errors, 'handoff_coverage', path + '/' + key, 'Each task needs exactly one handoff', 'M9.3')
        for tid, row in rows.items():
            if tid not in tasks:
                continue
            task = tasks[tid]
            if key == 'm7_requests' and row['time_request_id'] != task['time_request_id']:
                issue(errors, 'time_handoff', path + '/' + key, 'M7 handoff does not match the referenced task time request', 'M7')
            if key == 'm11_handoffs' and (row['shot_ids'] != task['shot_ids'] or row['mode_intent'] != task['mode_intent']):
                issue(errors, 'compile_handoff', path + '/' + key, 'M11 semantic handoff must preserve task shot order and mode intent', 'M11')


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
    if module == 'M9.1':
        validate_shots(data, sources, errors, inputs)
    elif module == 'M9.2':
        validate_edits(data, inputs['shot_context']['values'], inputs['continuity_context']['values'], sources, errors,
                       inputs['source_context']['values']['sources'])
    else:
        validate_generation(data, inputs, sources, errors)
    # Issues may be recorded, but unresolved ownership/compatibility problems never pass silently.
    for record in proposal['issues']:
        issue(errors, 'unresolved_issue', '/issues', record['code'] + ': ' + record['detail'], record['owner'])
    return errors


def read_paths(request, proposal):
    module = request['target']
    paths = ['/contexts/' + module + '/brief']
    paths += ['/contexts/' + module + '/' + key for key in INPUTS[module]]
    paths += ['/sources/' + key for key in sorted(source_references(request['inputs']) | source_references(proposal['changes']))]
    if module in ('M9.2', 'M9.3'):
        paths.append('/content/ShotMap')
    if module == 'M9.3':
        paths.append('/content/EditGraph')
    return sorted(set(paths))


def escape(key):
    return str(key).replace('~', '~0').replace('/', '~1')


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
    # Arrays are a declared collection dependency; do not infer stable indices after insertion.
    return [path or '/']


def overlaps(a, b):
    return a == b or a.startswith(b + '/') or b.startswith(a + '/') or a == '/' or b == '/'


def impact(before, after):
    changes = changed_paths(before, after)
    consumers = {x['consumer_id']: x for x in before['consumers']}
    consumers.update({x['consumer_id']: x for x in after['consumers']})
    result = []
    for consumer_id, consumer in sorted(consumers.items()):
        old = next((x for x in before['consumers'] if x['consumer_id'] == consumer_id), None)
        old_stale = old is not None and old['status'] == 'stale'
        consumer = deepcopy(consumer)
        if old:
            consumer['read_paths'] = sorted(set(consumer['read_paths']) | set(old['read_paths']))
        hits = sorted({path for path in changes if any(overlaps(path, read) for read in consumer['read_paths'])})
        result.append({'consumer_id': consumer_id, 'read_paths': consumer['read_paths'], 'changed_dependencies': hits,
                       'status': 'stale' if hits or old_stale or consumer['status'] == 'stale' else 'current'})
    return {'status': 'passed', 'changed_paths': changes, 'consumers': result,
            'limitations': ['Only registered actual read paths are evaluated; this does not re-run consumers or inspect media.']}


def state_errors(state):
    errors = []
    if not shape(state, 'State', errors):
        return errors
    latest = {}
    previous_accepted_version = 0
    seen_proposals, seen_requests = set(), set()
    for receipt in state['receipts']:
        if receipt['proposal_id'] in seen_proposals or receipt['request_id'] in seen_requests:
            issue(errors, 'receipt_duplicate', '/receipts', 'Accepted request and proposal IDs must be unique')
        seen_proposals.add(receipt['proposal_id']); seen_requests.add(receipt['request_id'])
        if receipt['accepted_version'] > state['version'] or receipt['base_version'] + 1 != receipt['accepted_version']:
            issue(errors, 'receipt_version', '/receipts', 'Receipt version is inconsistent with parent version')
        if receipt['accepted_version'] < previous_accepted_version:
            issue(errors, 'receipt_order', '/receipts', 'Receipts must preserve acceptance order')
        previous_accepted_version = receipt['accepted_version']
        latest[receipt['module_id']] = receipt
    for module, part in PARTS.items():
        present = part in state['content']
        if present != (module in latest) or present != (module in state['contexts']):
            issue(errors, 'state_partition', '/content/' + part, 'Accepted partition, context, and receipt must exist together')
        if present and module in latest:
            receipt = latest[module]
            if digest(state['content'][part]) != receipt['output_digest'] or digest(state['contexts'][module]) != receipt['context_digest']:
                issue(errors, 'state_digest', '/content/' + part, 'Accepted output/context differs from its receipt')
            paths = read_paths({'target': module, 'inputs': state['contexts'][module]}, {'changes': {part: state['content'][part]}})
            consumer = next((c for c in state['consumers'] if c['consumer_id'] == module), None)
            if paths != receipt['read_paths'] or not consumer or paths != consumer['read_paths']:
                issue(errors, 'actual_read_paths', '/receipts/' + module, 'Child dependency paths must match the actual accepted context and output sources')
    if not state['receipts'] and state['version'] != 0:
        issue(errors, 'state_version', '/version', 'An empty plan starts at version 0')
    indexed(state['consumers'], 'consumer_id', errors, '/consumers')
    expected_stale = sorted(c['consumer_id'] for c in state['consumers'] if c['consumer_id'] in PARTS and c['status'] == 'stale')
    if sorted(state['stale_modules']) != expected_stale:
        issue(errors, 'stale_registry', '/stale_modules', 'Stale module list must match actual consumers')
    return errors


def unwrap(value, kind, singular, plural, errors):
    expected = kind + 'Batch'
    if isinstance(value, dict) and value.get('kind') == expected:
        if shape(value, singular + 'Batch', errors):
            return value[plural]
        return []
    if shape(value, singular, errors):
        return [value]
    return []


def accept(state, proposals_doc, requests_doc):
    errors = state_errors(state)
    proposals = unwrap(proposals_doc, 'M9Proposal', 'Proposal', 'proposals', errors)
    requests = unwrap(requests_doc, 'M9Request', 'Request', 'requests', errors)
    request_map = indexed(requests, 'request_id', errors, '/requests') if requests else {}
    if not errors:
        indexed(proposals, 'proposal_id', errors, '/proposals')
        indexed(proposals, 'module_id', errors, '/proposals')
    if len({p['source_request_id'] for p in proposals}) != len(proposals):
        issue(errors, 'request_reuse', '/proposals', 'One request may not authorize multiple proposals in one acceptance')
    used = {p['source_request_id'] for p in proposals}
    if set(request_map) != used:
        issue(errors, 'request_set', '/requests', 'Supply the exact actual original request set for the proposal batch')
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
                issue(errors, 'idempotency_conflict', '/proposal_id', 'Accepted proposal/request ID was reused with different content')
        else:
            repeats.append(False)
            if request['request_id'] in old_request_ids:
                issue(errors, 'request_id_conflict', '/request_id', 'Accepted request ID cannot authorize a different proposal')
            if proposal['base_version'] != state['version']:
                issue(errors, 'stale_base', '/base_version', 'Proposal does not target the current parent version')
    if any(repeats) and not all(repeats):
        issue(errors, 'mixed_retry', '/proposals', 'Retry the exact prior batch separately from new revisions')
    if errors:
        return failed(errors)
    if all(repeats):
        return {'status': 'passed_with_unverified', 'idempotent': True, 'state': state, 'limitations': LIMITS}
    candidate = deepcopy(state)
    previous_sources = deepcopy(candidate['sources'])
    incoming_sources = {}
    for proposal in proposals:
        module = proposal['module_id']
        candidate['content'][PARTS[module]] = deepcopy(proposal['changes'][PARTS[module]])
        candidate['contexts'][module] = deepcopy(proposal['context'])
        for source_id, source in proposal['sources'].items():
            if source_id in incoming_sources and canonical(incoming_sources[source_id]) != canonical(source):
                issue(errors, 'source_conflict', '/sources/' + source_id, 'Atomic batch disagrees about one source/version')
            old = previous_sources.get(source_id)
            if old and old['version'] == source['version'] and canonical(old) != canonical(source):
                issue(errors, 'immutable_source_version', '/sources/' + source_id, 'Changed source content must receive a new version')
            incoming_sources[source_id] = source
    candidate['sources'].update(deepcopy(incoming_sources))
    for proposal in proposals:
        module, context = proposal['module_id'], proposal['context']
        for key, part in [('shot_context', 'ShotMap'), ('edit_context', 'EditGraph')]:
            if key in context and part in candidate['content'] and canonical(context[key]['values']) != canonical(candidate['content'][part]):
                issue(errors, 'sibling_snapshot_conflict', '/contexts/' + module + '/' + key,
                      'Readonly sibling/external projection differs from the candidate accepted partition')
    if errors:
        return failed(errors)
    candidate['version'] += 1
    for proposal in proposals:
        module = proposal['module_id']
        request = request_map[proposal['source_request_id']]
        paths = read_paths(request, proposal)
        candidate['receipts'].append({'proposal_id': proposal['proposal_id'], 'request_id': request['request_id'],
            'module_id': module, 'proposal_digest': digest(proposal), 'request_digest': digest(request),
            'output_digest': digest(proposal['changes'][PARTS[module]]), 'context_digest': digest(request['inputs']),
            'base_version': state['version'], 'accepted_version': candidate['version'], 'read_paths': paths})
    changes = changed_paths(state, candidate)
    accepted_modules = {p['module_id'] for p in proposals}
    consumers = {c['consumer_id']: deepcopy(c) for c in state['consumers']}
    for receipt in candidate['receipts']:
        module = receipt['module_id']
        if module in accepted_modules:
            consumers[module] = {'consumer_id': module, 'read_paths': receipt['read_paths'], 'status': 'current'}
    for consumer_id, consumer in consumers.items():
        if consumer_id not in accepted_modules and any(overlaps(change, read) for change in changes for read in consumer['read_paths']):
            consumer['status'] = 'stale'
    candidate['consumers'] = list(consumers.values())
    candidate['stale_modules'] = sorted(c['consumer_id'] for c in candidate['consumers'] if c['consumer_id'] in PARTS and c['status'] == 'stale')
    return {'status': 'passed_with_unverified', 'idempotent': False, 'state': candidate, 'limitations': LIMITS}


def failed(errors):
    return {'status': 'failed', 'errors': errors, 'limitations': LIMITS}


def route(request):
    errors = request_errors(request)
    if errors:
        return {**failed(errors), 'ready': False, 'invocation_status': 'not_invoked'}
    module = request['target']
    registry = load(ROOT / 'references/module-registry.json')
    entry = next(x for x in registry['modules'] if x['module_id'] == module)
    return {'status': 'passed_with_unverified', 'ready': True, 'invocation_status': 'not_invoked',
            'module_id': module, 'parent': 'M9', 'work_id': request['work_id'], 'request_id': request['request_id'],
            'contract_version': VERSION, 'route_version': registry['route_version'], 'base_version': request['base_version'],
            'input_versions': {k: request['inputs'][k]['source_version'] for k in INPUTS[module]},
            'write_path': '/content/' + PARTS[module], 'resources': entry['resources'],
            'rationale': entry['responsibility'], 'limitations': LIMITS}


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
            result = failed(errors) if errors else {'status': 'passed_with_unverified', 'module_id': proposal['module_id'],
                'read_paths': read_paths(request, proposal), 'limitations': LIMITS}
        elif args.command == 'accept':
            result = accept(load(args.state), load(args.proposal), load(args.requests))
        else:
            before, after = load(args.before), load(args.after)
            errors = []
            shape(before, 'State', errors, '/before'); shape(after, 'State', errors, '/after')
            result = failed(errors) if errors else impact(before, after)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        result = failed([{'code': 'input_error', 'path': '', 'owner': 'caller', 'detail': str(exc)}])
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 2 if result['status'] == 'failed' else 0


if __name__ == '__main__':
    raise SystemExit(main())
