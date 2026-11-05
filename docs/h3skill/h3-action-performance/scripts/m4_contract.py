#!/usr/bin/env python3
"""Portable M4 contract checker. Python 3.10+, standard library, no network.

Checks data contracts and explicit graph/token relations. It does not create a
prompt, judge acting, solve physics, inspect media, or certify H3 generations.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import uuid
from datetime import datetime, timezone

VERSION = "1.0.0"
PACKAGE_VERSION = "0.1.0"
ROOT = Path(__file__).resolve().parents[1]
OWNED = {"M4.1": "events", "M4.2": "mechanics", "M4.3": "outcomes"}
MINIMUM = {
    "M4": ("action_brief",), "M4.1": ("action_brief",),
    "M4.2": ("event_context", "mechanics_brief"),
    "M4.3": ("event_context", "mechanics_context", "outcome_brief"),
}
EMPTY = {"events": {"entities": {}, "requirements": {}, "items": {}},
         "mechanics": {"items": {}}, "outcomes": {"items": {}, "change_requests": {}}}
UNVERIFIED = ["semantic_intent", "source_authenticity", "physical_feasibility",
              "media_observation", "generated_video_quality", "global_G0_G4"]


def esc(value):
    return str(value).replace("~", "~0").replace("/", "~1")


def ptr(path, key):
    return path + "/" + esc(key)


def stable_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def same(left, right):
    """JSON equality preserves booleans vs numbers in opaque readonly payloads."""
    return stable_json(left) == stable_json(right)


def read_pointer(value, pointer):
    if not pointer.startswith("/"):
        raise ValueError("JSON Pointer must start with /")
    for part in pointer[1:].split("/"):
        if re.search(r"~(?![01])", part):
            raise ValueError("invalid JSON Pointer escape")
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            value = value[part]
        elif isinstance(value, list) and re.fullmatch(r"0|[1-9][0-9]*", part):
            value = value[int(part)]
        else:
            raise KeyError(part)
    return value


def type_ok(value, name):
    if name == "number":
        return ((isinstance(value, int) and not isinstance(value, bool))
                or (isinstance(value, float) and math.isfinite(value)))
    return {"object": isinstance(value, dict), "array": isinstance(value, list),
            "string": isinstance(value, str), "boolean": isinstance(value, bool),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "null": value is None}[name]


def shape_errors(value, schema, defs, path=""):
    """Only the finite JSON Schema vocabulary used by bundled contracts.json."""
    if "$ref" in schema:
        return shape_errors(value, defs[schema["$ref"].split("/")[-1]], defs, path)
    errors = []
    if "oneOf" in schema or "anyOf" in schema:
        key = "oneOf" if "oneOf" in schema else "anyOf"
        matches = sum(not shape_errors(value, item, defs, path) for item in schema[key])
        if (key == "oneOf" and matches != 1) or (key == "anyOf" and matches == 0):
            errors.append((path, f"{key} has {matches} matching alternatives"))
        return errors
    if "type" in schema and not type_ok(value, schema["type"]):
        return [(path, "expected " + schema["type"])]
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        errors.append((path, "unexpected constant"))
    if "enum" in schema and not any(type(value) is type(x) and value == x for x in schema["enum"]):
        errors.append((path, "value outside enum"))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append((path, "string too short"))
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append((path, "string does not match pattern"))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append((path, "number below minimum"))
    if isinstance(value, dict):
        if len(value) < schema.get("minProperties", 0):
            errors.append((path, "object has too few properties"))
        for key in schema.get("required", []):
            if key not in value:
                errors.append((ptr(path, key), "required property missing"))
        for key, item in value.items():
            if "propertyNames" in schema:
                errors += shape_errors(key, schema["propertyNames"], defs, ptr(path, key))
            if key in schema.get("properties", {}):
                errors += shape_errors(item, schema["properties"][key], defs, ptr(path, key))
            elif schema.get("additionalProperties") is False:
                errors.append((ptr(path, key), "unknown property"))
            elif isinstance(schema.get("additionalProperties"), dict):
                errors += shape_errors(item, schema["additionalProperties"], defs, ptr(path, key))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append((path, "array has too few items"))
        if schema.get("uniqueItems") and len({stable_json(x) for x in value}) != len(value):
            errors.append((path, "duplicate array items"))
        for i, item in enumerate(value):
            errors += shape_errors(item, schema.get("items", {}), defs, ptr(path, i))
    return errors


class Check:
    def __init__(self, definitions):
        self.defs = definitions
        self.diagnostics = []

    def add(self, code, path, message, owner="M4", status="fail"):
        self.diagnostics.append({"code": code, "path": path, "message": message,
                                 "status": status, "blocking": status == "fail",
                                 "repair_target": owner})

    @property
    def failed(self):
        return any(x["blocking"] for x in self.diagnostics)

    def shape(self, artifact, expected=None, path=""):
        kind = artifact.get("kind") if isinstance(artifact, dict) else None
        if kind not in ("M4Request", "M4Proposal", "M4ProposalBatch", "M4State") or (expected and kind != expected):
            self.add("artifact_kind", path, "Unexpected artifact kind; expected " + str(expected))
            return False
        errors = shape_errors(artifact, self.defs[kind], self.defs, path)
        for where, message in errors:
            self.add("contract_shape", where, message)
        return not errors

    def refs(self, value, sources, path="", owner="M4"):
        if isinstance(value, dict):
            if value.get("state") == "unknown":
                self.add("explicit_unknown", path, value["reason"], owner, "unverified")
            for key, item in value.items():
                if ((key == "values" and ("source_id" in value or value.get("state") == "known"))
                        or (key == "value" and "path" in value and "source_version" in value)):
                    # ExternalContext.values, StateObservation.values and a
                    # Projection.value are opaque; their keys are not protocol.
                    continue
                if key == "source_refs":
                    for i, source in enumerate(item):
                        if source not in sources:
                            self.add("unresolved_source", ptr(ptr(path, key), i), source, owner)
                elif key == "source_id" and item not in sources:
                    self.add("unresolved_source", ptr(path, key), item, owner)
                else:
                    self.refs(item, sources, ptr(path, key), owner)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                self.refs(item, sources, ptr(path, i), owner)

    def request(self, request, path=""):
        if not self.shape(request, "M4Request", path):
            return False
        target, inputs = request["target"], request["inputs"]
        for key in MINIMUM[target]:
            if key not in inputs:
                self.add("minimum_input_missing", ptr(ptr(path, "inputs"), key),
                         "Supply this input or an explicit unknown with a reason", target)
        self.refs(inputs, request["sources"], ptr(path, "inputs"), target)
        for field, owner in {"task_context": "M1", "reference_context": "M2", "space_context": "M3", "state_context": "M8"}.items():
            context = inputs.get(field, {})
            if "owner" in context and context["owner"] != owner:
                self.add("context_owner", ptr(ptr(path, "inputs"), field), f"Expected readonly {owner} context", target)
            if "source_id" in context and context["source_version"] != request["sources"].get(context["source_id"], {}).get("version"):
                self.add("context_version", ptr(ptr(path, "inputs"), field), "External source version differs from source entry", target)
        for i, projection in enumerate(inputs.get("readonly_projection", [])):
            if projection["source_version"] != request["base_version"]:
                self.add("projection_version", ptr(ptr(ptr(path, "inputs"), "readonly_projection"), i), "Readonly projection must identify request base version", target)
        return not self.failed

    def proposal(self, proposal, request=None, path=""):
        if not self.shape(proposal, "M4Proposal", path):
            return False
        owner = proposal["module_id"]
        partition = OWNED[owner]
        if set(proposal["changes"]) != {partition}:
            self.add("write_ownership", ptr(path, "changes"), "Child may replace only " + partition, owner)
        self.refs(proposal["context"], proposal["sources"], ptr(path, "context"), owner)
        self.refs(proposal["changes"], proposal["sources"], ptr(path, "changes"), owner)
        self.refs(proposal["issues"], proposal["sources"], ptr(path, "issues"), owner)
        self.refs(proposal["resolutions"], proposal["sources"], ptr(path, "resolutions"), owner)
        for key in MINIMUM[owner]:
            if key not in proposal["context"]:
                self.add("minimum_input_missing", ptr(ptr(path, "context"), key), "Required input absent", owner)
        if request is None:
            self.add("original_request_missing", path, "Source fidelity requires the actual request", owner, "unverified")
        elif self.shape(request, "M4Request", "/request"):
            self.request(request, "/request")
            for field in ("work_id", "base_version", "sources"):
                if proposal[field] != request[field]:
                    self.add("request_fidelity", ptr(path, field), "Proposal differs from original request", owner)
            if proposal["source_request_id"] != request["request_id"]:
                self.add("request_binding", ptr(path, "source_request_id"), "Wrong original request", owner)
            if request["target"] != owner:
                self.add("request_target", ptr(path, "module_id"), "Child proposal requires a request addressed to that child", owner)
            if not same(proposal["context"], request["inputs"]):
                self.add("request_fidelity", ptr(path, "context"), "Readonly inputs were changed or omitted", owner)
        for issue in proposal["issues"]:
            if issue["owner"] != owner or issue["status"] != "open" or "resolution" in issue:
                self.add("issue_ownership", ptr(path, "issues"), "New issues must be open and owned by this child", owner)
        if len({x["issue_id"] for x in proposal["issues"]}) != len(proposal["issues"]):
            self.add("duplicate_issue", ptr(path, "issues"), "Issue IDs must be unique", owner)
        if len({x["issue_id"] for x in proposal["resolutions"]}) != len(proposal["resolutions"]):
            self.add("duplicate_resolution", ptr(path, "resolutions"), "Resolution IDs must be unique", owner)
        content = copy.deepcopy(EMPTY)
        known = set(proposal["changes"])
        content.update(proposal["changes"])
        for field, part in (("event_context", "events"), ("mechanics_context", "mechanics")):
            context = proposal["context"].get(field)
            if isinstance(context, dict) and context.get("state") != "unknown":
                if part in known and content[part] != context:
                    self.add("readonly_conflict", ptr(ptr(path, "context"), field), "Proposed partition conflicts with readonly context", owner)
                else:
                    content[part] = context
                    known.add(part)
        self.content(content, known, ptr(path, "changes"))
        return not self.failed

    def content(self, content, known, path="/content"):
        events = content["events"]["items"]
        entities = content["events"]["entities"]
        requirements = content["events"]["requirements"]
        if "events" in known:
            for rid, requirement in requirements.items():
                for eid in requirement["event_ids"]:
                    if eid not in events:
                        self.add("dangling_requirement", ptr(ptr(ptr(path, "events"), "requirements"), rid), eid, "M4.1")
            covered = {eid for requirement in requirements.values() for eid in requirement["event_ids"]}
            for eid, event in events.items():
                where = path + "/events/items/" + esc(eid)
                for actor in event["actor_ids"]:
                    if entities.get(actor, {}).get("kind") != "actor":
                        self.add("actor_identity", where + "/actor_ids", actor + " must name a stable actor ID", "M4.1")
                for obj in event["object_ids"]:
                    if entities.get(obj, {}).get("kind") not in ("actor", "prop", "environment"):
                        self.add("object_identity", where + "/object_ids", obj + " must name a stable actor/prop/environment ID", "M4.1")
                for dependency in event["depends_on"]:
                    if dependency not in events:
                        self.add("dangling_dependency", where + "/depends_on", dependency, "M4.1")
                if eid not in covered:
                    self.add("requirement_coverage_unknown", where, "Event has no explicit requirement link", "M4.1", "unverified")
                self.snapshot(event["entry_state"], set(event["actor_ids"] + event["object_ids"]), where + "/entry_state", "M4.1")
            self.dag({eid: event["depends_on"] for eid, event in events.items()}, path + "/events/items", "event_cycle", "M4.1")
        by_event = {"mechanics": {}, "outcomes": {}}
        for part, owner in (("mechanics", "M4.2"), ("outcomes", "M4.3")):
            if part not in known:
                continue
            for ident, record in content[part]["items"].items():
                eid = record["event_id"]
                where = path + "/" + part + "/items/" + esc(ident)
                if eid in by_event[part]:
                    self.add("duplicate_event_record", where, "At most one record per event in each partition", owner)
                by_event[part][eid] = record
                if "events" not in known:
                    self.add("event_context_unknown", where, "Event linkage cannot be checked without event context", owner, "unverified")
                    continue
                if eid not in events:
                    self.add("dangling_event", where + "/event_id", eid, owner)
                    continue
                participants = set(events[eid]["actor_ids"] + events[eid]["object_ids"])
                if part == "mechanics" and record["contact"]["state"] == "known":
                    for participant in record["contact"]["participants"]:
                        if participant not in participants:
                            self.add("contact_participant", where + "/contact/participants", participant + " is not a declared event participant", owner)
                if part == "outcomes":
                    self.snapshot(record["end_state"], participants, where + "/end_state", owner)
            if "events" in known:
                for eid in events:
                    if eid not in by_event[part]:
                        self.add("coverage_incomplete", path + "/" + part, eid + " has no " + part + " record", owner, "unverified")
        if "events" in known:
            for part, owner in (("mechanics", "M4.2"), ("outcomes", "M4.3")):
                if part not in known and events:
                    self.add("coverage_unavailable", path + "/" + part, "Entry/process/result coverage is not complete", owner, "unverified")
        if "outcomes" in known and "events" in known:
            graph = {}
            for oid, outcome in content["outcomes"]["items"].items():
                eid = outcome["event_id"]
                continuation = outcome["continuation"]
                targets = continuation.get("event_ids", [])
                graph[eid] = targets
                for target in targets:
                    where = path + "/outcomes/items/" + esc(oid) + "/continuation"
                    if target not in events:
                        self.add("dangling_continuation", where, target, "M4.3")
                    elif eid not in events[target]["depends_on"]:
                        self.add("continuation_dependency", where, "Next event must explicitly depend on the preceding event", "M4.3")
            self.dag(graph, path + "/outcomes/items", "continuation_cycle", "M4.3")
            for eid, event in events.items():
                for before in event["depends_on"]:
                    outcome = by_event["outcomes"].get(before)
                    if not outcome:
                        continue
                    if eid not in outcome["continuation"].get("event_ids", []):
                        self.add("dependency_state_not_inferred", path + "/events/items/" + esc(eid),
                                 "A dependency without an explicit adjacent continuation does not impose state equality", "M4.3", "unverified")
                        continue
                    entry, end = event["entry_state"], outcome["end_state"]
                    where = path + "/events/items/" + esc(eid) + "/entry_state"
                    if entry["state"] != "known" or end["state"] != "known":
                        self.add("inheritance_unknown", where, "Dependency state inheritance is unknown", "M4.3", "unverified")
                        continue
                    shared = set(events[eid]["actor_ids"] + events[eid]["object_ids"]) & set(end["values"])
                    for actor in shared:
                        for key, value in end["values"][actor].items():
                            actual = entry["values"].get(actor, {}).get(key)
                            if actual is None:
                                self.add("inheritance_missing", where, actor + "/" + key + " has no explicit inherited entry token", "M4.3", "unverified")
                            elif actual != value:
                                self.add("inheritance_conflict", where, actor + "/" + key + " differs from predecessor result", "M4.3")
        if "outcomes" in known:
            for cid, change in content["outcomes"]["change_requests"].items():
                expected = {"M3": "space_change", "M5": "visibility_need", "M6": "sound_candidate", "M7": "relative_dependency", "M8": "state_change_request"}[change["target_module"]]
                where = path + "/outcomes/change_requests/" + esc(cid)
                if change["request_kind"] != expected:
                    self.add("handoff_owner", where, "Request kind does not match target owner", "M4.3")
                if "proposed_state" in change and change["target_module"] != "M8":
                    self.add("handoff_owner", where, "Only an M8 request may carry a proposed state", "M4.3")
                if "events" not in known:
                    self.add("handoff_events_unknown", where, "Event references cannot be checked without event context", "M4.3", "unverified")
                    continue
                participants = set()
                for eid in change["event_ids"]:
                    if eid not in events:
                        self.add("dangling_handoff", where, eid, "M4.3")
                    else:
                        participants.update(events[eid]["actor_ids"] + events[eid]["object_ids"])
                if "proposed_state" in change:
                    self.snapshot(change["proposed_state"], participants, where + "/proposed_state", "M4.3")

    def snapshot(self, snapshot, participants, path, owner):
        if snapshot["state"] == "known":
            for ident in snapshot["values"]:
                if ident not in participants:
                    self.add("state_participant", path + "/values/" + esc(ident), "State token names an undeclared event participant", owner)

    def dag(self, graph, path, code, owner):
        visited, active = set(), set()
        def visit(node):
            if node in active:
                self.add(code, path, "Cycle involving " + node, owner)
                return
            if node in visited:
                return
            active.add(node)
            for other in graph.get(node, []):
                if other in graph:
                    visit(other)
            active.remove(node)
            visited.add(node)
        for node in graph:
            visit(node)

    def state(self, state, path="", reject_blockers=True):
        if not self.shape(state, "M4State", path):
            return False
        self.refs(state["content"], state["sources"], path + "/content")
        self.refs(state["issues"], state["sources"], path + "/issues")
        self.content(state["content"], set(EMPTY), path + "/content")
        for ident, receipt in state["accepted_proposals"].items():
            if receipt["accepted_version"] > state["version"]:
                self.add("receipt_version", path + "/accepted_proposals/" + esc(ident), "Receipt version is in the future")
        for ident, issue in state["issues"].items():
            if ident != issue["issue_id"]:
                self.add("issue_identity", path + "/issues/" + esc(ident), "Issue key differs from ID")
            if (issue["status"] == "resolved") != ("resolution" in issue):
                self.add("issue_resolution", path + "/issues/" + esc(ident), "Resolved status requires resolution evidence")
            if reject_blockers and issue["status"] == "open" and issue["severity"] == "blocking":
                self.add("open_blocker", path + "/issues/" + esc(ident), issue["message"], issue["owner"])
        for ident, consumer in state["consumers"].items():
            where = path + "/consumers/" + esc(ident)
            if consumer["source_state_version"] > state["version"]:
                self.add("consumer_version", where, "Consumer source version is in the future")
            for pointer in consumer["read_paths"]:
                try:
                    read_pointer(state, pointer)
                except (KeyError, ValueError, IndexError):
                    self.add("consumer_read_path", where, "Unresolved read path: " + pointer)
        return not self.failed


def changed_paths(before, after, path=""):
    if type(before) is type(after) and isinstance(before, dict):
        result = []
        for key in sorted(set(before) | set(after)):
            if key not in before or key not in after:
                result.append(ptr(path, key))
            else:
                result += changed_paths(before[key], after[key], ptr(path, key))
        return result
    if not same(before, after):
        return [path]
    return []


def overlaps(left, right):
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def impact(before, after):
    paths = [p for p in changed_paths(before, after) if any(p == x or p.startswith(x + "/") for x in ("/content", "/sources", "/issues", "/display"))]
    stale = {}
    for ident, consumer in before["consumers"].items():
        touched = [p for p in paths if any(overlaps(p, r) for r in consumer["read_paths"])]
        if consumer["status"] == "stale" or touched:
            stale[ident] = {"module_id": consumer["module_id"], "changed_paths": touched,
                            "status": "stale", "already_stale": consumer["status"] == "stale"}
    return {"changed_paths": paths, "stale_consumers": stale,
            "scope": "declared read-path intersections only; hidden dependencies unverified"}


def request_index(check, requests):
    if not isinstance(requests, list):
        check.add("requests_array", "/requests", "--requests must contain the original request array")
        return {}
    index = {}
    for i, request in enumerate(requests):
        if check.shape(request, "M4Request", "/requests/" + str(i)):
            if request["request_id"] in index:
                check.add("duplicate_request", "/requests/" + str(i), request["request_id"])
            index[request["request_id"]] = request
    return index


def accept(check, state, batch, requests):
    state_ok = check.state(state, reject_blockers=False)
    batch_ok = check.shape(batch, "M4ProposalBatch", "/batch")
    index = request_index(check, requests)
    if not state_ok or not batch_ok or check.failed:
        return None
    proposals = batch["proposals"]
    if batch["work_id"] != state["work_id"]:
        check.add("work_identity", "/batch/work_id", "Batch addresses another ActionPlan")
    if len({p["proposal_id"] for p in proposals}) != len(proposals):
        check.add("duplicate_proposal", "/batch/proposals", "Proposal IDs must be unique")
    if len({p["module_id"] for p in proposals}) != len(proposals):
        check.add("partition_conflict", "/batch/proposals", "At most one write per child partition per atomic batch")
    replays = []
    for i, proposal in enumerate(proposals):
        path = "/batch/proposals/" + str(i)
        request = index.get(proposal["source_request_id"])
        if request is None:
            check.add("original_request_required", path, "Actual original request is missing", proposal["module_id"])
        check.proposal(proposal, request, path)
        if proposal["work_id"] != batch["work_id"] or proposal["base_version"] != batch["base_version"]:
            check.add("batch_binding", path, "Proposal work/base differs from batch")
        receipt = state["accepted_proposals"].get(proposal["proposal_id"])
        replays.append(receipt is not None)
        if receipt and (receipt["digest"] != digest(proposal) or receipt["source_request_id"] != proposal["source_request_id"] or receipt["module_id"] != proposal["module_id"]):
            check.add("idempotency_conflict", path, "Accepted proposal ID was reused with different bytes or identity")
    if check.failed:
        return None
    if all(replays):
        check.state(state)
        if check.failed:
            return None
        return {"state": copy.deepcopy(state), "acceptance": "idempotent_replay", "impact": impact(state, state)}
    if any(replays):
        check.add("mixed_replay", "/batch/proposals", "Separate an exact retry from new writes")
    if batch["base_version"] != state["version"]:
        check.add("stale_base_version", "/batch/base_version", "Refresh requests and proposals against current parent version")
    if check.failed:
        return None
    candidate = copy.deepcopy(state)
    for proposal in proposals:
        owner, part = proposal["module_id"], OWNED[proposal["module_id"]]
        old, new = state["content"][part], proposal["changes"][part]
        for group in old:
            for ident in old[group]:
                if ident not in new[group]:
                    check.add("accepted_record_deleted", "/content/" + part + "/" + group + "/" + esc(ident), "Accepted IDs cannot be removed by partition replacement", owner)
                elif part == "events" and group == "requirements" and old[group][ident] != new[group][ident]:
                    check.add("accepted_requirement_changed", "/content/events/requirements/" + esc(ident), "Accepted demand text, source and event coverage are immutable", owner)
                elif part == "events" and group == "entities" and old[group][ident] != new[group][ident]:
                    check.add("accepted_identity_changed", "/content/events/entities/" + esc(ident), "Stable actor/prop identity cannot be repurposed", owner)
        candidate["content"][part] = copy.deepcopy(new)
        for source, entry in proposal["sources"].items():
            if source in candidate["sources"] and candidate["sources"][source] != entry:
                check.add("source_collision", "/sources/" + esc(source), "Source ID cannot be rebound", owner)
            candidate["sources"][source] = copy.deepcopy(entry)
        for issue in proposal["issues"]:
            existing = candidate["issues"].get(issue["issue_id"])
            if existing is not None and existing != issue:
                check.add("issue_collision", "/issues/" + esc(issue["issue_id"]), "Existing issue cannot be overwritten", owner)
            candidate["issues"][issue["issue_id"]] = copy.deepcopy(issue)
        for resolution in proposal["resolutions"]:
            ident = resolution["issue_id"]
            existing = state["issues"].get(ident)
            if not existing or existing["owner"] != owner or existing["status"] != "open":
                check.add("resolution_ownership", "/issues/" + esc(ident), "Resolution requires an existing open issue owned by this child", owner)
            else:
                candidate["issues"][ident]["status"] = "resolved"
                candidate["issues"][ident]["resolution"] = {"state": "known", "value": resolution["rationale"], "source_refs": resolution["source_refs"]}
    for proposal in proposals:
        for field, part in (("event_context", "events"), ("mechanics_context", "mechanics")):
            context = proposal["context"].get(field)
            if isinstance(context, dict) and context.get("state") != "unknown" and context != candidate["content"][part]:
                check.add("readonly_conflict", "/context/" + field, "Borrowed context differs from the accepted candidate", proposal["module_id"])
        for projection in proposal["context"].get("readonly_projection", []):
            try:
                actual = read_pointer(candidate, projection["path"])
            except (KeyError, ValueError, IndexError):
                check.add("projection_unresolved", "/context/readonly_projection", projection["path"], proposal["module_id"])
            else:
                if not same(actual, projection["value"]):
                    check.add("readonly_conflict", projection["path"], "Readonly projection differs from candidate", proposal["module_id"])
    candidate["version"] += 1
    for proposal in proposals:
        candidate["accepted_proposals"][proposal["proposal_id"]] = {"digest": digest(proposal), "source_request_id": proposal["source_request_id"], "module_id": proposal["module_id"], "accepted_version": candidate["version"]}
    result_impact = impact(state, candidate)
    for ident in result_impact["stale_consumers"]:
        candidate["consumers"][ident]["status"] = "stale"
    check.state(candidate)
    if check.failed:
        return None
    return {"state": candidate, "acceptance": "accepted_draft", "impact": result_impact}


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    def bad_constant(value):
        raise ValueError("Non-finite JSON number: " + value)
    def finite_float(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValueError("Non-finite JSON number: " + value)
        return parsed
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=bad_constant, parse_float=finite_float)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    r = sub.add_parser("route", help="Return callable module routes; do not invoke agents")
    r.add_argument("artifact", nargs="?"); r.add_argument("--request")
    c = sub.add_parser("check", help="Check a public contract artifact")
    c.add_argument("artifact", nargs="?"); c.add_argument("--proposal"); c.add_argument("--state")
    c.add_argument("--request"); c.add_argument("--requests")
    a = sub.add_parser("accept", help="Atomically return a new draft state; original requests required")
    a.add_argument("state_path", nargs="?"); a.add_argument("batch_path", nargs="?")
    a.add_argument("--state"); a.add_argument("--proposals"); a.add_argument("--requests", required=True)
    i = sub.add_parser("impact", help="Compare changes with declared consumer read paths")
    i.add_argument("before_path", nargs="?"); i.add_argument("after_path", nargs="?")
    i.add_argument("--before"); i.add_argument("--after")
    args = parser.parse_args(argv)
    started = datetime.now(timezone.utc).isoformat()
    loaded = {}
    def get(path, label):
        if not path:
            raise ValueError("Missing path: " + label)
        value = load_json(path)
        loaded[label] = value
        return value
    try:
        schema = load_json(ROOT / "references/contracts.json")
        registry = load_json(ROOT / "references/module-registry.json")
        check = Check(schema["$defs"])
        payload = {}
        if args.command == "route":
            request = get(args.request or args.artifact, "request")
            check.request(request)
            if not check.failed:
                modules = list(OWNED) if request["target"] == "M4" else [request["target"]]
                payload = {"routes": [{"module_id": m, "resources": registry["modules"][m]["resources"],
                                        "write_scope": "/content/" + OWNED[m], "return_to": "M4",
                                        "minimum_inputs": list(MINIMUM[m]), "repair_target": m} for m in modules],
                           "route_status": "ready_with_unverified_inputs" if check.diagnostics else "ready_for_call",
                           "invocation": "not_invoked"}
        elif args.command == "check":
            artifact = get(args.proposal or args.state or args.artifact, "artifact")
            request = get(args.request, "request") if args.request else None
            index = request_index(check, get(args.requests, "requests")) if args.requests else {}
            if check.shape(artifact):
                kind = artifact["kind"]
                if kind == "M4Request": check.request(artifact)
                elif kind == "M4State": check.state(artifact)
                elif kind == "M4Proposal": check.proposal(artifact, request or index.get(artifact["source_request_id"]))
                else:
                    proposals = artifact["proposals"]
                    if len({p["proposal_id"] for p in proposals}) != len(proposals):
                        check.add("duplicate_proposal", "/proposals", "Proposal IDs must be unique")
                    if len({p["module_id"] for p in proposals}) != len(proposals):
                        check.add("partition_conflict", "/proposals", "At most one write per child partition")
                    for n, proposal in enumerate(artifact["proposals"]):
                        check.proposal(proposal, index.get(proposal["source_request_id"]), "/proposals/" + str(n))
                        if proposal["work_id"] != artifact["work_id"] or proposal["base_version"] != artifact["base_version"]:
                            check.add("batch_binding", "/proposals/" + str(n), "Proposal work/base differs from batch")
        elif args.command == "accept":
            payload = accept(check, get(args.state or args.state_path, "state"),
                             get(args.proposals or args.batch_path, "batch"), get(args.requests, "requests")) or {}
        elif args.command == "impact":
            before = get(args.before or args.before_path, "before")
            after = get(args.after or args.after_path, "after")
            before_ok, after_ok = check.state(before), check.state(after)
            if before_ok and after_ok:
                if before["work_id"] != after["work_id"]:
                    check.add("work_identity", "", "States address different ActionPlans")
                elif after["version"] < before["version"]:
                    check.add("impact_version", "", "After-state version cannot precede before-state")
                else: payload = {"impact": impact(before, after)}
        status = "fail" if check.failed else "pass"
        original_requests = []
        for artifact in loaded.values():
            if isinstance(artifact, dict) and artifact.get("kind") == "M4Request":
                original_requests.append(artifact)
            elif isinstance(artifact, list):
                original_requests.extend(r for r in artifact if isinstance(r, dict) and r.get("kind") == "M4Request")
        trace = {"call_id": "m4-" + uuid.uuid4().hex, "parent_module": "M4", "started_at": started,
                 "finished_at": datetime.now(timezone.utc).isoformat(), "package_version": PACKAGE_VERSION,
                 "schema_version": VERSION, "route_version": registry["route_version"], "registry_version": registry["registry_version"],
                 "input_digests": {k: digest(v) for k, v in loaded.items()},
                 "resources": {"references/contracts.json": digest(schema), "references/module-registry.json": digest(registry)},
                 "side_effects": "none", "operation_id": loaded.get("batch", {}).get("batch_id"),
                 "revision": payload.get("state", {}).get("version"),
                 "request_ids": sorted({r["request_id"] for r in original_requests if isinstance(r.get("request_id"), str)}),
                 "input_versions": [{"request_id": r.get("request_id"), "target": r.get("target"), "base_version": r.get("base_version"), "contract_version": r.get("contract_version")} for r in original_requests],
                 "source_versions": {r["request_id"]: {k: v.get("version") for k, v in r.get("sources", {}).items() if isinstance(v, dict)} for r in original_requests if isinstance(r.get("request_id"), str) and isinstance(r.get("sources"), dict)},
                 "applicability": {"local_contract": status, "physical_and_media": "unverified"},
                 "retry": payload.get("acceptance", "not_applicable"), "output_status": status,
                 "error_codes": sorted({d["code"] for d in check.diagnostics if d["blocking"]})}
        result = {"kind": "M4ToolResult", "contract_version": VERSION, "command": args.command,
                  "execution": "completed", "disposition": "rejected" if check.failed else "checked_draft",
                  "validation": {"local_contract": status, "overall": "fail" if check.failed else "unverified", "unverified": UNVERIFIED},
                  "diagnostics": check.diagnostics, "trace": trace, **payload}
        if args.command == "route" and check.failed:
            result.update({"route_status": "blocked", "invocation": "not_invoked", "routes": []})
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 1 if check.failed else 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, RecursionError) as exc:
        print(json.dumps({"kind": "M4ToolError", "command": args.command,
                          "execution": "error", "error": str(exc), "side_effects": "none"}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
