#!/usr/bin/env python3
"""Self-contained, offline M3 spatial contracts; only the bundled schema vocabulary.
No media inspection, physics solver, natural-language interpreter or H3 compiler.
Every operation reads JSON and prints a result; input files are never modified.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
import re
import sys
import uuid
from fractions import Fraction
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"
PACKAGE_VERSION = "0.1.0"
ROOT = Path(__file__).resolve().parents[1]
OWNED = {"M3.1": "topology", "M3.2": "blocking", "M3.3": "interactions"}
MINIMUM = {"M3": ("scene_brief",), "M3.1": ("scene_brief",),
           "M3.2": ("topology_context", "entity_context", "blocking_brief"),
           "M3.3": ("topology_context", "blocking_context", "interaction_brief")}
EMPTY = {"topology": {"frames": {}, "regions": {}, "connections": {}},
         "blocking": {"entities": {}, "placements": {}, "routes": {}},
         "interactions": {"relations": {}, "change_requests": {}}}
PUBLIC = {"M3Request", "M3Proposal", "M3ProposalBatch", "M3State"}
UNVERIFIED = ["natural_language_intent", "source_authenticity", "media_observation",
              "geometric_collision_and_contact", "camera_projection_M5", "actual_timing_M7",
              "generated_video_quality", "global_acceptance_G0_to_G4"]

def esc(value):
    return str(value).replace("~", "~0").replace("/", "~1")


def ptr(path, key):
    return path + "/" + esc(key)


def read_pointer(value, pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise KeyError(pointer)
    for token in pointer[1:].split("/"):
        if re.search(r"~(?:[^01]|$)", token):
            raise KeyError(pointer)
        key = token.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            value = value[key]
        elif isinstance(value, list) and re.fullmatch(r"0|[1-9][0-9]*", key):
            value = value[int(key)]
        else:
            raise KeyError(pointer)
    return value


def stable_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def type_ok(value, name):
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": type(value) is int,
        "number": type(value) is int or type(value) is float and math.isfinite(value),
        "boolean": type(value) is bool,
        "null": value is None,
    }.get(name, False)


def shape_errors(value, schema, definitions, path=""):
    """Validate only the vocabulary present in our fixed, bundled schema."""
    errors = []
    if "$ref" in schema:
        name = schema["$ref"].removeprefix("#/$defs/")
        return shape_errors(value, definitions[name], definitions, path)
    for operator in ("oneOf", "anyOf"):
        if operator in schema:
            branches = [shape_errors(value, item, definitions, path) for item in schema[operator]]
            valid = sum(not item for item in branches)
            if (operator == "oneOf" and valid != 1) or (operator == "anyOf" and valid == 0):
                errors.append((path, f"Value does not satisfy {operator}."))
                if valid == 0:
                    errors.extend(min(branches, key=len))
            return errors
    if "type" in schema and not type_ok(value, schema["type"]):
        return [(path, "Expected " + schema["type"] + ".")]
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        errors.append((path, "Expected constant " + repr(schema["const"]) + "."))
    if "enum" in schema and value not in schema["enum"]:
        errors.append((path, "Value is outside the declared enumeration."))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append((path, "String is too short."))
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append((path, "String does not match the declared pattern."))
    if type(value) in (int, float):
        if type(value) is float and not math.isfinite(value):
            errors.append((path, "Numbers must be finite."))
        if "minimum" in schema and value < schema["minimum"]:
            errors.append((path, "Number is below the minimum."))
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append((path, "Number is not greater than the minimum."))
    if isinstance(value, dict):
        if len(value) < schema.get("minProperties", 0):
            errors.append((path, "Object has fewer than the required entries."))
        for key in schema.get("required", []):
            if key not in value:
                errors.append((ptr(path, key), "Required field is missing."))
        properties = schema.get("properties", {})
        for key, item in value.items():
            if "propertyNames" in schema:
                errors.extend(shape_errors(key, schema["propertyNames"], definitions, ptr(path, key)))
            if key in properties:
                errors.extend(shape_errors(item, properties[key], definitions, ptr(path, key)))
            elif schema.get("additionalProperties") is False:
                errors.append((ptr(path, key), "Field is not in this contract."))
            elif isinstance(schema.get("additionalProperties"), dict):
                errors.extend(shape_errors(item, schema["additionalProperties"], definitions, ptr(path, key)))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append((path, "Array has fewer than the required items."))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append((path, "Array has too many items."))
        if schema.get("uniqueItems"):
            serialized = [stable_json(item) for item in value]
            if len(set(serialized)) != len(serialized):
                errors.append((path, "Array items must be unique."))
        for index, item in enumerate(value):
            if "items" in schema:
                errors.extend(shape_errors(item, schema["items"], definitions, ptr(path, index)))
    return errors


class Check:
    def __init__(self, definitions):
        self.defs = definitions
        self.diagnostics = []

    def add(self, code, path, message, owner="M3", status="fail"):
        self.diagnostics.append({"code": code, "path": path, "message": message,
                                 "status": status, "blocking": status == "fail", "repair_target": owner})

    @property
    def failed(self):
        return any(d["blocking"] for d in self.diagnostics)

    def shape(self, artifact, path=""):
        if not isinstance(artifact, dict) or not isinstance(artifact.get("kind"), str) or artifact["kind"] not in PUBLIC:
            self.add("invalid_shape", path, "Expected a public M3 artifact object.")
            return False
        errors = shape_errors(artifact, self.defs[artifact["kind"]], self.defs, path)
        for p, message in errors:
            self.add("invalid_shape", p, message)
        return not errors

    def scan_refs(self, value, sources, path=""):
        if isinstance(value, dict):
            for key, item in value.items():
                p = ptr(path, key)
                if key == "source_refs":
                    for i, source_id in enumerate(item):
                        if source_id not in sources:
                            self.add("unresolved_source", ptr(p, i), "Source ID is absent from the declared source map.")
                else:
                    self.scan_refs(item, sources, p)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                self.scan_refs(item, sources, ptr(path, i))

    def minimum(self, target, inputs, path):
        for name in MINIMUM[target]:
            if name not in inputs:
                self.add("missing_minimum_input", ptr(path, name), "This independently callable module requires this input.", target)
            elif isinstance(inputs[name], dict) and inputs[name].get("state") == "unknown":
                self.add("unknown_brief", ptr(path, name), "The brief is explicitly unknown; routing does not infer its content.", target, "unverified")

    def topology(self, topology, path):
        frames, regions = topology["frames"], topology["regions"]
        for fid, frame in frames.items():
            p = ptr(ptr(path, "frames"), fid)
            if frame["space"] == "entity_local" and "anchor_entity_id" not in frame:
                self.add("missing_frame_anchor", p, "An entity-local frame requires its stable anchor entity ID.", "M3.1")
            if frame["space"] != "entity_local" and "anchor_entity_id" in frame:
                self.add("unexpected_frame_anchor", p, "Only an entity-local frame has an anchor entity.", "M3.1")
            if frame["space"] == "screen" and "view_context" not in frame:
                self.add("missing_view_context", p, "A screen frame requires declared or explicitly unknown viewing conditions.", "M3.1")
            if frame["space"] != "screen" and "view_context" in frame:
                self.add("unexpected_view_context", p, "Viewing conditions attach to the screen frame; world/body coordinates stay separate.", "M3.1")
            if frame["space"] == "screen":
                self.add("screen_projection_unverified", p, "Screen coordinates are view dependent; M5 must establish the projection.", "M5", "unverified")
        for rid, region in regions.items():
            if region["frame_id"] not in frames:
                self.add("unresolved_frame", ptr(ptr(path, "regions"), rid), "Region refers to an undeclared coordinate frame.", "M3.1")
            for other in region.get("exclusive_with", []):
                if other not in regions or other == rid:
                    self.add("invalid_region_exclusion", ptr(ptr(path, "regions"), rid), "Region exclusion must reference another declared region.", "M3.1")
        for cid, connection in topology["connections"].items():
            p = ptr(ptr(path, "connections"), cid)
            left, right = regions.get(connection["from_region"]), regions.get(connection["to_region"])
            if left is None or right is None:
                self.add("unresolved_region", p, "Connection endpoint is not a declared region.", "M3.1")
            elif left["scene_id"] != right["scene_id"]:
                self.add("cross_scene_connection", p, "This local topology has no inter-scene transition model.", "M3.1")
            elif left["frame_id"] != right["frame_id"]:
                self.add("undeclared_frame_transform", p, "A connection cannot silently transform coordinates between frames.", "M3.1")
            if connection["from_region"] == connection["to_region"]:
                self.add("self_connection", p, "Within-region movement needs no self-connection.", "M3.1")

    def scope(self, scope, region, path):
        if region and scope["scene_id"] != region["scene_id"]:
            self.add("scene_scope_mismatch", path, "Scope scene differs from the region's scene.", "M3.2")
        if not isinstance(scope["shot_id"], str) or not isinstance(scope["phase"], str):
            self.add("scope_unverified", path, "Shot/phase is unknown; simultaneity and continuity cannot be concluded.", "M7", "unverified")

    def blocking(self, blocking, topology, path):
        entities, placements, routes = blocking["entities"], blocking["placements"], blocking["routes"]
        regions, frames = topology["regions"], topology["frames"]
        seen = {}
        for pid, placement in placements.items():
            p = ptr(ptr(path, "placements"), pid)
            if placement["entity_id"] not in entities:
                self.add("unresolved_entity", ptr(p, "entity_id"), "Placement must use a stable entity from the provided projection.", "M3.2")
            region = regions.get(placement["region_id"])
            if region is None:
                self.add("unresolved_region", ptr(p, "region_id"), "Placement region is absent from topology.", "M3.2")
            if placement["frame_id"] not in frames:
                self.add("unresolved_frame", ptr(p, "frame_id"), "Placement frame is undeclared.", "M3.2")
            elif region and placement["frame_id"] != region["frame_id"]:
                self.add("coordinate_frame_mismatch", p, "Placement and region must use the same declared frame.", "M3.2")
            self.scope(placement["scope"], region, ptr(p, "scope"))
            for field in ("position", "facing"):
                value = placement[field]
                if isinstance(value, dict):
                    self.add("coordinate_unverified", ptr(p, field), "Unknown coordinates remain unknown.", "M3.2", "unverified")
            if isinstance(placement["facing"], list) and not any(placement["facing"]):
                self.add("zero_facing_vector", ptr(p, "facing"), "A declared facing direction must have nonzero length.", "M3.2")
            gaze = placement["gaze"]
            if gaze["kind"] == "entity" and gaze["target_id"] not in entities:
                self.add("unresolved_gaze_target", ptr(p, "gaze"), "Gaze entity is not declared.", "M3.2")
            elif gaze["kind"] == "region" and gaze["target_id"] not in regions:
                self.add("unresolved_gaze_target", ptr(p, "gaze"), "Gaze region is not declared.", "M3.2")
            scope = placement["scope"]
            if isinstance(scope["shot_id"], str) and isinstance(scope["phase"], str):
                key = (placement["entity_id"], scope["scene_id"], scope["shot_id"], scope["phase"])
                for previous in seen.get(key, []):
                    conflict = regions_exclusive(regions, previous["region_id"], placement["region_id"])
                    if previous["frame_id"] == placement["frame_id"]:
                        if isinstance(previous["position"], list) and isinstance(placement["position"], list) and previous["position"] != placement["position"]:
                            conflict = True
                        if isinstance(previous["facing"], list) and isinstance(placement["facing"], list) and not same_direction(previous["facing"], placement["facing"]):
                            conflict = True
                    else:
                        self.add("placement_transform_unverified", p, "Multiple frames cannot be compared without an explicit transform; no projection is inferred.", "M3.2", "unverified")
                    if conflict:
                        self.add("same_phase_placement_conflict", p, "One entity has contradictory declared placements in the same scene, shot and phase.", "M3.2")
                seen.setdefault(key, []).append(placement)
        edges = set()
        for connection in topology["connections"].values():
            if connection["passable"]:
                a, b = connection["from_region"], connection["to_region"]
                edges.add((a, b))
                if connection["direction"] == "both":
                    edges.add((b, a))
        for rid, route in routes.items():
            p = ptr(ptr(path, "routes"), rid)
            if route["entity_id"] not in entities:
                self.add("unresolved_entity", ptr(p, "entity_id"), "Route entity is absent.", "M3.2")
            if route["frame_id"] not in frames:
                self.add("unresolved_frame", ptr(p, "frame_id"), "Route frame is absent.", "M3.2")
            start, end = placements.get(route["start_placement"]), placements.get(route["end_placement"])
            for field, endpoint in (("start_placement", start), ("end_placement", end)):
                if endpoint is None:
                    self.add("unresolved_placement", ptr(p, field), "Route endpoint placement is absent.", "M3.2")
                elif endpoint["entity_id"] != route["entity_id"] or endpoint["frame_id"] != route["frame_id"]:
                    self.add("route_endpoint_mismatch", ptr(p, field), "Endpoint must belong to this entity and coordinate frame.", "M3.2")
                elif not same_scene_shot(endpoint["scope"], route["scope"]):
                    self.add("route_scope_mismatch", ptr(p, field), "Route endpoint belongs to a different declared scene or shot.", "M3.2")
            route_regions = route["region_path"]
            if start and start["region_id"] != route_regions[0] or end and end["region_id"] != route_regions[-1]:
                self.add("route_endpoint_region_mismatch", p, "Declared path must start and end at its endpoint regions.", "M3.2")
            for i, region_id in enumerate(route_regions):
                region = regions.get(region_id)
                if region is None:
                    self.add("unresolved_region", ptr(ptr(p, "region_path"), i), "Route region is absent.", "M3.2")
                elif not region["traversable"]:
                    self.add("nontraversable_route", p, "A declared route uses an explicitly nontraversable region.", "M3.2")
                elif region["frame_id"] != route["frame_id"]:
                    self.add("coordinate_frame_mismatch", p, "Route cannot silently switch coordinate frames.", "M3.2")
                self.scope(route["scope"], region, ptr(p, "scope"))
            for a, b in zip(route_regions, route_regions[1:]):
                if (a, b) not in edges:
                    self.add("disconnected_route", p, "Consecutive path regions require a passable connection in the declared direction.", "M3.2")
        for fid, frame in frames.items():
            if frame["space"] == "entity_local" and frame.get("anchor_entity_id") not in entities:
                used = any(v["frame_id"] == fid for v in list(placements.values()) + list(routes.values()))
                self.add("unresolved_frame_anchor" if used else "frame_anchor_unverified", ptr(path, "entities"), "Entity-local frame anchor is absent from this projection.", "M3.2", "fail" if used else "unverified")

    def interactions(self, interactions, blocking, topology, path):
        entities, placements, routes = blocking["entities"], blocking["placements"], blocking["routes"]
        regions = topology["regions"]
        policies = {}
        for iid, relation in interactions["relations"].items():
            p = ptr(ptr(path, "relations"), iid)
            region = regions.get(relation["region_id"])
            if region is None:
                self.add("unresolved_region", ptr(p, "region_id"), "Interaction region is absent.", "M3.3")
            self.scope(relation["scope"], region, ptr(p, "scope"))
            participants = set(relation["participants"])
            if not participants <= set(entities):
                self.add("unresolved_participant", ptr(p, "participants"), "Interaction participant is absent from the entity projection.", "M3.3")
            if not set(relation["order"]) <= participants:
                self.add("invalid_interaction_order", ptr(p, "order"), "Order may reference only the declared participants.", "M3.3")
            if relation["kind"] in ("crossing", "avoidance") and set(relation["order"]) != participants:
                self.add("interaction_order_unverified", ptr(p, "order"), "Crossing/avoidance order is incomplete; no temporal or physical success is certified.", "M3.3", "unverified")
            for route_id in relation["route_ids"]:
                route = routes.get(route_id)
                if route is None:
                    self.add("unresolved_route", ptr(p, "route_ids"), "Interaction refers to an absent route.", "M3.3")
                elif route["entity_id"] not in participants:
                    self.add("interaction_route_entity_mismatch", ptr(p, "route_ids"), "Associated route belongs to a nonparticipant entity.", "M3.3")
                elif relation["region_id"] not in route["region_path"]:
                    self.add("interaction_route_region_mismatch", ptr(p, "route_ids"), "Associated route does not reach this declared interaction region.", "M3.3")
                elif not same_scene_shot(route["scope"], relation["scope"]):
                    self.add("interaction_route_scope_mismatch", ptr(p, "route_ids"), "Associated route belongs to a different declared scene or shot.", "M3.3")
            for eid in participants:
                simultaneous = [v for v in placements.values() if v["entity_id"] == eid and same_phase(v["scope"], relation["scope"])]
                if simultaneous and all(regions_exclusive(regions, v["region_id"], relation["region_id"]) for v in simultaneous):
                    self.add("interaction_placement_conflict", p, "Participant is in an explicitly exclusive region at this same declared phase.", "M3.3")
                elif not simultaneous or all(v["region_id"] != relation["region_id"] for v in simultaneous):
                    self.add("interaction_placement_unverified", p, "No same-phase placement establishes this participant's presence in the interaction region.", "M3.3", "unverified")
            scope = relation["scope"]
            target = relation.get("occlusion_target", {})
            target_known = "occluder_id" in target
            if target_known and (target["occluder_id"] not in participants or target["occluded_id"] not in participants or target["occluder_id"] == target["occluded_id"]):
                self.add("invalid_occlusion_target", ptr(p, "occlusion_target"), "Directed occlusion must name two distinct declared participants.", "M3.3")
            if relation["occlusion"] in ("allowed", "forbidden") and not target_known:
                self.add("occlusion_target_unverified", ptr(p, "occlusion_target"), "Occluder, occluded entity and body/object part must be explicit before comparing visibility policies.", "M3.3", "unverified")
            if target_known and all(isinstance(scope[k], str) for k in ("scene_id", "shot_id", "phase")) and isinstance(relation["view_context"], str) and relation["occlusion"] in ("allowed", "forbidden"):
                key = (target["occluder_id"], target["occluded_id"], target["part"], relation["region_id"], scope["scene_id"], scope["shot_id"], scope["phase"], relation["view_context"])
                if key in policies and policies[key] != relation["occlusion"]:
                    self.add("conflicting_occlusion_policy", p, "The same directed occluder/target/part/region/phase/view has explicitly opposing occlusion policies.", "M3.3")
                policies[key] = relation["occlusion"]
            if isinstance(relation["view_context"], dict) or relation["occlusion"] == "unknown":
                self.add("visibility_unverified", p, "Visibility/occlusion requires M5's view and semantic inspection.", "M5", "unverified")
        for cid, request in interactions["change_requests"].items():
            for pointer in request["read_paths"]:
                try:
                    read_pointer({"content": {"topology": topology, "blocking": blocking, "interactions": interactions}}, pointer)
                except (KeyError, IndexError, TypeError):
                    self.add("unresolved_change_request_read", ptr(ptr(path, "change_requests"), cid), "Change request read path is not in this supplied projection.", "M3.3")

    def content(self, content, sources, path="/content"):
        self.scan_refs(content, sources, path)
        self.topology(content["topology"], ptr(path, "topology"))
        self.blocking(content["blocking"], content["topology"], ptr(path, "blocking"))
        self.interactions(content["interactions"], content["blocking"], content["topology"], ptr(path, "interactions"))

    def artifact(self, artifact, path=""):
        initial_count = len(self.diagnostics)
        if not self.shape(artifact, path):
            return False
        kind = artifact["kind"]
        if kind == "M3Request":
            self.minimum(artifact["target"], artifact["inputs"], ptr(path, "inputs"))
            self.scan_refs(artifact["inputs"], artifact["sources"], ptr(path, "inputs"))
            if "topology_context" in artifact["inputs"]:
                top = artifact["inputs"]["topology_context"]
                self.topology(top, ptr(ptr(path, "inputs"), "topology_context"))
                if "blocking_context" in artifact["inputs"]:
                    self.blocking(artifact["inputs"]["blocking_context"], top, ptr(ptr(path, "inputs"), "blocking_context"))
        elif kind == "M3Proposal":
            module = artifact["module_id"]
            self.minimum(module, artifact["context"], ptr(path, "context"))
            self.scan_refs(artifact["context"], artifact["sources"], ptr(path, "context"))
            self.scan_refs(artifact["issues"], artifact["sources"], ptr(path, "issues"))
            self.scan_refs(artifact["resolutions"], artifact["sources"], ptr(path, "resolutions"))
            if set(artifact["changes"]) != {OWNED[module]}:
                self.add("cross_owner_write", ptr(path, "changes"), "Child proposal must replace exactly its one owned partition.", module)
                return False
            if not all(key in artifact["context"] for key in MINIMUM[module]):
                return False
            content = copy.deepcopy(EMPTY)
            context = artifact["context"]
            if "topology_context" in context:
                content["topology"] = context["topology_context"]
            if "blocking_context" in context:
                content["blocking"] = context["blocking_context"]
            content.update(artifact["changes"])
            if module == "M3.2" and content["blocking"]["entities"] != context["entity_context"]:
                self.add("entity_projection_changed", ptr(ptr(ptr(path, "changes"), "blocking"), "entities"), "M3 copies public entity IDs and metadata; identity editing belongs to M2.", "M2.2")
            self.content(content, artifact["sources"], ptr(path, "candidate"))
            for iid, issue in artifact["issues"].items():
                if issue["owner"] != module or issue["state"] != "open":
                    self.add("issue_owner_violation", ptr(ptr(path, "issues"), iid), "New child issues must be open and owned by that child.", module)
            resolution_ids = [r["issue_id"] for r in artifact["resolutions"]]
            if len(set(resolution_ids)) != len(resolution_ids):
                self.add("duplicate_resolution", ptr(path, "resolutions"), "An issue may be resolved only once per proposal.", module)
        elif kind == "M3ProposalBatch":
            authors, ids = set(), set()
            for i, proposal in enumerate(artifact["proposals"]):
                p = ptr(ptr(path, "proposals"), i)
                self.artifact(proposal, p)
                if proposal["module_id"] in authors:
                    self.add("competing_partition_proposals", p, "One batch permits one author/proposal per owned partition.")
                if proposal["proposal_id"] in ids:
                    self.add("duplicate_proposal_id", p, "Proposal IDs must be unique within a batch.")
                authors.add(proposal["module_id"]); ids.add(proposal["proposal_id"])
                if proposal["work_id"] != artifact["work_id"] or proposal["base_version"] != artifact["base_version"]:
                    self.add("batch_version_mismatch", p, "Child work/base must match its batch.")
        elif kind == "M3State":
            self.content(artifact["content"], artifact["sources"], ptr(path, "content"))
            self.scan_refs(artifact["issues"], artifact["sources"], ptr(path, "issues"))
            for iid, issue in artifact["issues"].items():
                if issue["state"] == "resolved" and "resolution" not in issue:
                    self.add("missing_resolution_evidence", ptr(ptr(path, "issues"), iid), "A resolved issue retains its owner's resolution reason and source refs.")
                if issue["state"] == "open" and "resolution" in issue:
                    self.add("premature_resolution", ptr(ptr(path, "issues"), iid), "An open issue cannot already claim a resolution.")
            for cid, consumer in artifact["consumers"].items():
                p = ptr(ptr(path, "consumers"), cid)
                if consumer["source_state_version"] > artifact["version"]:
                    self.add("future_consumer_version", p, "A consumer cannot read a future version.")
                for pointer in consumer["read_paths"]:
                    try:
                        read_pointer(artifact, pointer)
                    except (KeyError, IndexError, TypeError):
                        self.add("unresolved_consumer_read", p, "Consumer read path does not exist in this snapshot.")
            for pid, receipt in artifact["accepted_proposals"].items():
                if receipt["accepted_version"] > artifact["version"]:
                    self.add("future_receipt_version", ptr(ptr(path, "accepted_proposals"), pid), "Receipt cannot belong to a future version.")
        return not any(d["blocking"] for d in self.diagnostics[initial_count:])


def regions_exclusive(regions, a, b):
    return a != b and (b in regions.get(a, {}).get("exclusive_with", []) or a in regions.get(b, {}).get("exclusive_with", []))


def same_direction(a, b):
    if not any(a) or not any(b):
        return False
    i = next(i for i, v in enumerate(a) if v)
    ratio = Fraction(b[i]) / Fraction(a[i])
    return ratio > 0 and all(Fraction(y) == Fraction(x) * ratio for x, y in zip(a, b))


def same_scene_shot(a, b):
    return a["scene_id"] == b["scene_id"] and (not isinstance(a["shot_id"], str) or not isinstance(b["shot_id"], str) or a["shot_id"] == b["shot_id"])


def same_phase(a, b):
    return all(isinstance(a[k], str) and isinstance(b[k], str) and a[k] == b[k] for k in ("scene_id", "shot_id", "phase"))


def request_match(check, proposal, request, path=""):
    if not check.artifact(request, ptr(path, "request")):
        return
    if request["kind"] != "M3Request":
        check.add("wrong_request_kind", path, "Original request must have kind M3Request.")
        return
    mapping = {"work_id": "work_id", "base_version": "base_version", "source_request_id": "request_id", "module_id": "target", "sources": "sources", "context": "inputs"}
    for field, reqfield in mapping.items():
        if proposal[field] != request[reqfield]:
            check.add("request_mismatch", ptr(path, field), "Proposal must preserve the actual original request's " + reqfield + ".", proposal["module_id"])


def merge_sources(check, target, sources, path):
    for sid, source in sources.items():
        if sid in target and target[sid] != source:
            check.add("source_identity_mutation", ptr(path, sid), "Source IDs are immutable; use a new ID for changed content/version.")
        else:
            target[sid] = copy.deepcopy(source)


def accept(check, state, batch, requests):
    check.artifact(state, "/state"); check.artifact(batch, "/batch")
    if check.failed:
        return None, "rejected"
    if state["kind"] != "M3State" or batch["kind"] != "M3ProposalBatch":
        check.add("wrong_accept_kind", "", "Accept requires M3State and M3ProposalBatch.")
        return None, "rejected"
    if not isinstance(requests, list):
        check.add("missing_original_requests", "/requests", "Accept requires a JSON array of actual original requests.")
        return None, "rejected"
    by_id = {}
    for i, request in enumerate(requests):
        if check.artifact(request, "/requests/" + str(i)) and request["kind"] == "M3Request":
            rid = request["request_id"]
            if rid in by_id:
                check.add("duplicate_request_id", "/requests/" + str(i), "Original request IDs must be unique.")
            by_id[rid] = request
        elif isinstance(request, dict) and request.get("kind") != "M3Request":
            check.add("wrong_request_kind", "/requests/" + str(i), "Only actual M3Request artifacts are allowed.")
    for i, proposal in enumerate(batch["proposals"]):
        request = by_id.get(proposal["source_request_id"])
        if request is None:
            check.add("missing_original_request", "/batch/proposals/" + str(i), "No actual request matches source_request_id.")
        else:
            request_match(check, proposal, request, "/batch/proposals/" + str(i))
    if state["work_id"] != batch["work_id"]:
        check.add("wrong_work", "/batch/work_id", "Batch and state must identify the same work.")
    pending = []
    for proposal in batch["proposals"]:
        pid = proposal["proposal_id"]
        receipt = state["accepted_proposals"].get(pid)
        if receipt:
            if receipt["digest"] != digest(proposal):
                check.add("proposal_id_reused", "/batch/proposals", "An accepted proposal ID cannot identify changed content.")
        else:
            pending.append(proposal)
    if not pending and not check.failed:
        return copy.deepcopy(state), "idempotent_replay"
    if len(pending) != len(batch["proposals"]):
        check.add("mixed_replay_and_revision", "/batch", "Do not mix accepted operations with new proposals in one revision.")
    if batch["base_version"] != state["version"]:
        check.add("stale_base_version", "/batch/base_version", "Read the current state and submit a new versioned proposal; no last-writer-wins.")
    candidate = copy.deepcopy(state)
    for proposal in pending:
        module = proposal["module_id"]; partition = OWNED[module]
        before = state["content"][partition]; after = proposal["changes"][partition]
        for collection in before:
            if not set(before[collection]) <= set(after[collection]):
                check.add("accepted_id_deletion", "/content/" + partition + "/" + collection, "This version does not support deleting accepted IDs; revise them explicitly under their owner.", module)
        candidate["content"][partition] = copy.deepcopy(after)
        merge_sources(check, candidate["sources"], proposal["sources"], "/sources")
        for iid, issue in proposal["issues"].items():
            if iid in candidate["issues"] and candidate["issues"][iid] != issue:
                check.add("issue_identity_mutation", "/issues/" + iid, "Existing issues cannot be silently replaced; resolve through the owner.", module)
            else:
                candidate["issues"][iid] = copy.deepcopy(issue)
        for resolution in proposal["resolutions"]:
            iid = resolution["issue_id"]; issue = candidate["issues"].get(iid)
            if iid not in state["issues"] or issue is None or issue["owner"] != module or issue["state"] != "open":
                check.add("invalid_issue_resolution", "/issues/" + iid, "Only the owning child may resolve an existing open issue.", module)
            else:
                issue["state"] = "resolved"
                issue["resolution"] = {"description": resolution["description"], "source_refs": copy.deepcopy(resolution["source_refs"])}
    for proposal in pending:
        context = proposal["context"]
        for field, partition in (("topology_context", "topology"), ("blocking_context", "blocking")):
            if field in context and context[field] != candidate["content"][partition]:
                check.add("composition_projection_mismatch", "/context/" + field, "Standalone projection differs from the actual composed candidate; dependencies must exist and match at acceptance.", proposal["module_id"])
    check.content(candidate["content"], candidate["sources"])
    for iid, issue in candidate["issues"].items():
        if issue["state"] == "open" and issue["blocking"]:
            check.add("open_blocking_issue", "/issues/" + iid, issue["description"], issue["owner"])
    if check.failed:
        return None, "rejected"
    candidate["version"] += 1
    for proposal in pending:
        candidate["accepted_proposals"][proposal["proposal_id"]] = {"digest": digest(proposal), "source_request_id": proposal["source_request_id"], "module_id": proposal["module_id"], "accepted_version": candidate["version"]}
    check.artifact(candidate, "/accepted_state")
    return (None, "rejected") if check.failed else (candidate, "accepted_draft")


def changed_paths(before, after, path=""):
    if type(before) is not type(after):
        return [path]
    if isinstance(before, dict):
        result = []
        for key in sorted(set(before) | set(after)):
            p = ptr(path, key)
            if key not in before or key not in after:
                result.append(p)
            else:
                result.extend(changed_paths(before[key], after[key], p))
        return result
    return [] if before == after else [path]


def impact(check, before, after):
    check.artifact(before, "/before"); check.artifact(after, "/after")
    if check.failed:
        return None
    if before["kind"] != "M3State" or after["kind"] != "M3State":
        check.add("wrong_impact_kind", "", "Impact requires two M3State snapshots.")
        return None
    if before["work_id"] != after["work_id"] or after["version"] < before["version"]:
        check.add("invalid_impact_versions", "", "Compare the same work in nondecreasing version order.")
        return None
    changes = [p for p in changed_paths(before, after) if re.match(r"^/(content|sources|issues|display)(/|$)", p)]
    reports = {}
    for cid, consumer in before["consumers"].items():
        affected = [p for p in changes if any(p == r or p.startswith(r + "/") or r.startswith(p + "/") for r in consumer["read_paths"])]
        stale = consumer["source_state_version"] != before["version"] or bool(affected)
        reports[cid] = {"module_id": consumer["module_id"], "result_version": consumer["result_version"], "status": "stale" if stale else "unaffected_by_declared_changes", "affected_paths": affected, "read_paths": consumer["read_paths"]}
    return {"changed_paths": changes, "consumers": reports, "unregistered_consumers": "unverified", "recheck": "Only owners of affected declared reads; M11/M12 inspect resulting versions as applicable."}


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError("Nonfinite JSON number: " + value)
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs, parse_constant=nonfinite)


def output(check, command, payload=None, disposition=None, inputs=None, started=None, registry=None, schema=None):
    failed = check.failed
    value = {"kind": "M3ToolResult", "contract_version": VERSION, "command": command,
             "execution": "completed", "disposition": disposition or ("rejected" if failed else "checked_draft"),
             "validation": {"local_contract": "fail" if failed else "pass", "overall": "fail" if failed else "unverified", "unverified": UNVERIFIED},
             "diagnostics": check.diagnostics,
             "trace": {"call_id": "call_" + uuid.uuid4().hex, "started_at": started, "finished_at": datetime.now(timezone.utc).isoformat(), "package_version": PACKAGE_VERSION, "input_digests": {k: digest(v) for k, v in (inputs or {}).items()}, "route_version": "1.0.0", "parent_module": "M3", "resources": {"contracts.json": digest(schema), "module-registry.json": digest(registry)}, "registry_version": registry["contract_version"], "side_effects": "none", "retry": "Technical retry keeps proposal ID and exact content; domain revision uses current base_version and a new proposal ID."}}
    if payload:
        value.update(payload)
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    route = subs.add_parser("route", help="Validate and route a request; no child is executed.")
    route.add_argument("artifact", nargs="?"); route.add_argument("--request", dest="request_flag")
    checkp = subs.add_parser("check", help="Check any public artifact; use --request for original-request fidelity.")
    checkp.add_argument("artifact", nargs="?"); checkp.add_argument("--proposal"); checkp.add_argument("--state"); checkp.add_argument("--request"); checkp.add_argument("--requests")
    acceptp = subs.add_parser("accept", help="Accept a proposed draft only after matching actual original requests.")
    acceptp.add_argument("state_path", nargs="?"); acceptp.add_argument("batch_path", nargs="?"); acceptp.add_argument("--state"); acceptp.add_argument("--proposals"); acceptp.add_argument("--requests", required=True)
    impactp = subs.add_parser("impact", help="Report affected consumers from their registered actual read paths.")
    impactp.add_argument("before_path", nargs="?"); impactp.add_argument("after_path", nargs="?"); impactp.add_argument("--before"); impactp.add_argument("--after")
    args = parser.parse_args(argv)
    started = datetime.now(timezone.utc).isoformat()
    try:
        schema = load_json(ROOT / "references/contracts.json")
        registry = load_json(ROOT / "references/module-registry.json")
        if registry.get("contract_version") != VERSION or any(registry["modules"][key]["minimum_inputs"] != list(value) for key, value in MINIMUM.items()):
            raise ValueError("Bundled registry/contract minimum-input definitions disagree.")
        check = Check(schema["$defs"])
        inputs = {}; payload = {}; disposition = None
        if args.command == "route":
            request = load_json(args.request_flag or args.artifact or "")
            inputs["request"] = request
            check.artifact(request)
            if not check.failed and request["kind"] != "M3Request":
                check.add("wrong_route_kind", "", "Routing requires M3Request.")
            if isinstance(request, dict) and request.get("kind") == "M3Request" and isinstance(request.get("target"), str) and request["target"] in MINIMUM:
                target = request["target"]
                entry = registry["modules"][target]
                payload["route"] = {"target": target, "route_id": "route_" + target.replace(".", "_"), "route_version": entry["interface_version"], "minimum_inputs": entry["minimum_inputs"], "resources": entry["resources"], "machine_dependencies": registry["resources"]["required_for_machine_checks"], "status": "blocked" if check.failed else "ready_with_unverified_inputs" if any(d["status"] == "unverified" for d in check.diagnostics) else "ready_for_call", "execution": "not_invoked", "return_to": "M3.accept" if target != "M3" else "caller", "write_partition": OWNED.get(target), "branch_candidates": list(OWNED) if target == "M3" else [], "repair_owner": entry["failure_owner"], "failure_return": "Return structured diagnostics to the caller and semantic owner; no automatic retry of semantic conflicts.", "input_mapping": {k: "/inputs/" + k for k in entry["minimum_inputs"]}, "output_kind": entry["result"]}
                disposition = "rejected" if check.failed else "routed_not_executed"
        elif args.command == "check":
            path = args.proposal or args.state or args.artifact
            artifact = load_json(path or "")
            inputs["artifact"] = artifact
            check.artifact(artifact)
            if not check.failed and artifact["kind"] == "M3Proposal":
                if args.request:
                    request = load_json(args.request); inputs["request"] = request
                    request_match(check, artifact, request)
                else:
                    check.add("original_request_unverified", "/source_request_id", "Supply --request to compare the actual request. Parent accept requires it.", "M3", "unverified")
            elif not check.failed and artifact["kind"] == "M3ProposalBatch" and args.requests:
                requests = load_json(args.requests); inputs["requests"] = requests
                if not isinstance(requests, list):
                    check.add("invalid_request_set", "/requests", "--requests must be a JSON array.")
                else:
                    by_id = {}
                    for i, request in enumerate(requests):
                        if check.artifact(request, "/requests/" + str(i)) and request["kind"] == "M3Request":
                            if request["request_id"] in by_id:
                                check.add("duplicate_request_id", "/requests", "Request IDs must be unique.")
                            by_id[request["request_id"]] = request
                        elif isinstance(request, dict) and request.get("kind") != "M3Request":
                            check.add("wrong_request_kind", "/requests/" + str(i), "Only actual M3Request artifacts are allowed.")
                    for proposal in artifact["proposals"]:
                        request = by_id.get(proposal["source_request_id"])
                        if request is None:
                            check.add("missing_original_request", "/requests", "No matching original request.")
                        else:
                            request_match(check, proposal, request)
        elif args.command == "accept":
            state = load_json(args.state or args.state_path or ""); batch = load_json(args.proposals or args.batch_path or ""); requests = load_json(args.requests)
            inputs.update(state=state, batch=batch, requests=requests)
            state, disposition = accept(check, state, batch, requests)
            if state is not None:
                payload["state"] = state
        elif args.command == "impact":
            before = load_json(args.before or args.before_path or ""); after = load_json(args.after or args.after_path or "")
            inputs.update(before=before, after=after)
            report = impact(check, before, after)
            if report is not None:
                payload["impact"] = report
        value = output(check, args.command, payload, disposition, inputs, started, registry, schema)
        print(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))
        return 1 if check.failed else 0
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        print(json.dumps({"kind": "M3ToolResult", "contract_version": VERSION, "command": args.command, "execution": "failed", "disposition": "input_or_resource_error", "diagnostics": [{"code": "input_or_resource_error", "path": "", "message": str(exc), "status": "fail", "blocking": True, "repair_target": "caller"}]}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
