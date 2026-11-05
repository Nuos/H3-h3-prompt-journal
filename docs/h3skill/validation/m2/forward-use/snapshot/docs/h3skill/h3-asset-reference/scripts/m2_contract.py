#!/usr/bin/env python3
"""Offline M2 contracts: source registration, entity binding and reference rights.

Only the bundled contract vocabulary is supported. This is not a general JSON
Schema service, natural-language interpreter, media inspector or H3 compiler.
Commands read inputs and print new JSON; no input, media or network is modified.
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
from datetime import datetime, timezone
from pathlib import Path


VERSION = "1.0.0"
PACKAGE_VERSION = "0.1.0"
ROOT = Path(__file__).resolve().parents[1]
OWNED = {"M2.1": "asset_registry", "M2.2": "entity_registry", "M2.3": "reference_map"}
MINIMUM = {
    "M2": ("material_brief",),
    "M2.1": ("material_brief",),
    "M2.2": ("asset_context", "binding_brief"),
    "M2.3": ("asset_context", "entity_context", "permission_brief"),
}
AUTHORITIES = {"user_requirement", "approved_plan"}
AUDIO_ATTRIBUTES = {"voice", "audio_content", "audio_timing"}
ANCHORS = {"first_frame", "last_frame", "keyframe"}
VISUAL_ANCHOR_PROPERTIES = {"pose", "appearance", "clothing", "scene", "spatial_layout", "camera"}
COLLECTIONS = {
    "asset_registry": ((),),
    "entity_registry": (("entities",), ("bindings",)),
    "reference_map": (("permissions",), ("decisions",)),
}


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
        "number": type(value) in (int, float) and math.isfinite(value),
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
        if not math.isfinite(value):
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

    def add(self, code, path, message, owner="M2", status="fail"):
        self.diagnostics.append({
            "code": code, "path": path, "message": message,
            "status": status, "blocking": status == "fail", "repair_target": owner,
        })

    @property
    def failed(self):
        return any(item["status"] == "fail" for item in self.diagnostics)

    def refs(self, refs, sources, path, authority=False):
        for index, source_id in enumerate(refs):
            if source_id not in sources:
                self.add("unresolved_source", ptr(path, index), f"Unknown source {source_id}.")
            elif authority and sources[source_id]["kind"] not in AUTHORITIES:
                self.add("not_an_authorization", ptr(path, index),
                         "Observation, case text and design hypotheses do not authorize target inheritance.", "M2.3")

    def scan_refs(self, value, sources, path=""):
        if isinstance(value, dict):
            for key, item in value.items():
                p = ptr(path, key)
                if key in ("source_refs", "observation_refs", "authority_refs"):
                    self.refs(item, sources, p, authority=key == "authority_refs")
                else:
                    self.scan_refs(item, sources, p)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                self.scan_refs(item, sources, ptr(path, index))

    def shape(self, artifact, path=""):
        if not isinstance(artifact, dict):
            self.add("invalid_shape", path, "Artifact must be an object.")
            return False
        name = artifact.get("kind")
        if not isinstance(name, str) or name not in {"M2Request", "M2Proposal", "M2ProposalBatch", "M2State"}:
            self.add("unknown_artifact_kind", ptr(path, "kind"), "Use a public M2 artifact kind.")
            return False
        errors = shape_errors(artifact, self.defs[name], self.defs, path)
        for p, message in errors:
            self.add("invalid_shape", p, message)
        return not errors

    def assets(self, assets, sources, path):
        for asset_id, asset in assets.items():
            p = ptr(path, asset_id)
            allowed = {"image": {"visual"}, "audio": {"audio"}, "video": {"visual", "audio"}, "text": {"text"}}
            if not set(asset["channels"]) <= allowed[asset["media_type"]]:
                self.add("channel_media_mismatch", ptr(p, "channels"), "Channels do not match the declared media type.", "M2.1")
            if asset["access_state"] == "accessible" and asset["availability"] != "provided":
                self.add("access_availability_conflict", p, "An accessible input must be recorded as provided.", "M2.1")
            if asset["availability"] == "provided" and not isinstance(asset["locator"], str):
                self.add("provided_asset_without_locator", ptr(p, "locator"), "A provided asset needs its actual locator.", "M2.1")
            if asset["observation_state"] == "observed":
                if not asset["observation_refs"] or not asset.get("observation_scope"):
                    self.add("missing_observation_evidence", p, "Recorded observation needs evidence refs and the inspected extent.", "M2.1")
                for ref in asset["observation_refs"]:
                    if ref in sources and sources[ref]["kind"] != "media_observation":
                        self.add("observation_is_not_media_evidence", ptr(p, "observation_refs"),
                                 "Case descriptions or author claims are not actual media observations.", "M2.1")
            elif asset["observation_state"] == "unobserved" and asset["observation_refs"]:
                self.add("observation_state_conflict", p, "Unobserved assets cannot carry observed-evidence refs.", "M2.1")
            if asset["access_state"] != "accessible" or asset["observation_state"] != "observed":
                self.add("asset_not_fully_observed", p,
                         "Access/observation remains limited; registration does not inspect media or confirm readiness.", "M2.1", "unverified")
            if "derived_from" in asset and asset["derived_from"] not in assets:
                self.add("unresolved_derivation", ptr(p, "derived_from"), "Derived source asset is absent.", "M2.1")
            if asset.get("derived_from") == asset_id:
                self.add("self_derivation", ptr(p, "derived_from"), "An asset cannot be derived from itself.", "M2.1")
        for asset_id in assets:
            seen = set()
            current = asset_id
            while current in assets and "derived_from" in assets[current]:
                if current in seen:
                    self.add("derivation_cycle", ptr(path, asset_id), "Asset derivation must not form a cycle.", "M2.1")
                    break
                seen.add(current)
                current = assets[current]["derived_from"]

    def entities(self, registry, assets, path):
        entities, bindings = registry["entities"], registry["bindings"]
        selectors = {}
        for binding_id, binding in bindings.items():
            p = ptr(ptr(path, "bindings"), binding_id)
            entity = entities.get(binding["entity_id"])
            asset = assets.get(binding["asset_id"])
            if entity is None:
                self.add("unresolved_entity", ptr(p, "entity_id"), "Stable entity is not registered.", "M2.2")
            if asset is None:
                self.add("unresolved_asset", ptr(p, "asset_id"), "Asset is not registered in the provided projection.", "M2.2")
            elif binding["channel"] not in asset["channels"]:
                self.add("unavailable_channel", ptr(p, "channel"), "This channel was not declared for the source asset.", "M2.2")
            if binding["state"] == "confirmed":
                if not binding["authority_refs"] or not isinstance(binding["source_selector"], str):
                    self.add("unconfirmed_source_selection", p,
                             "A confirmed mapping needs an explicit selector and target authorization.", "M2.2")
            else:
                self.add("binding_unconfirmed", p, "Candidate/unknown mapping does not grant reference rights.", "M2.2", "unverified")
            if entity and binding["state"] == "confirmed" and isinstance(binding["source_selector"], str):
                key = (binding["asset_id"], binding["channel"], binding["source_selector"].strip(), entity["kind"])
                other = selectors.get(key)
                if other and other[1]["entity_id"] != binding["entity_id"]:
                    if not (binding.get("shared_selection_reason") and other[1].get("shared_selection_reason")):
                        self.add("ambiguous_shared_selector", p,
                                 "Distinct entities sharing the same source selection need an explicit, authorized reason or distinct selectors.", "M2.2")
                selectors[key] = (binding_id, binding)

    def scope(self, scope, path):
        if scope["kind"] == "time" and scope["end_seconds"] <= scope["start_seconds"]:
            self.add("invalid_time_window", path, "End must be after start; intervals are half-open.", "M2.3")
        if scope["kind"] == "unknown":
            self.add("unknown_scope", path, "Unknown scope does not authorize the whole work.", "M2.3", "unverified")

    def permissions(self, reference_map, assets, registry, path):
        permissions, decisions = reference_map["permissions"], reference_map["decisions"]
        bindings = registry["bindings"]
        chosen = {}
        combined_pairs = set()
        for decision_id, decision in decisions.items():
            p = ptr(ptr(path, "decisions"), decision_id)
            members = decision["permission_ids"]
            selected = decision["selected_permission_ids"]
            if not set(selected) <= set(members):
                self.add("invalid_decision_choice", p, "Chosen permission must be one of the listed candidates.", "M2.3")
            if decision["strategy"] == "select" and len(selected) != 1:
                self.add("invalid_decision_choice", p, "A selection decision chooses exactly one permission.", "M2.3")
            if decision["strategy"] == "combine" and len(selected) < 2:
                self.add("invalid_combination", p, "A combination decision needs at least two selected permissions.", "M2.3")
            records = []
            for permission_id in members:
                if permission_id not in permissions:
                    self.add("unresolved_decision_permission", p, f"Permission {permission_id} does not exist.", "M2.3")
                else:
                    records.append(permissions[permission_id])
                if permission_id in chosen:
                    self.add("competing_decisions", p, "A permission cannot participate in competing resolution groups.", "M2.3")
                chosen[permission_id] = set(selected)
            if records:
                keys = {(bindings.get(r["binding_id"], {}).get("entity_id"), r["attribute"], stable_json(r["scope"])) for r in records}
                if len(keys) != 1 or any(r["scope"]["kind"] == "unknown" for r in records):
                    self.add("invalid_decision_scope", p,
                             "A resolution must concern one entity/attribute and exactly equal, known scopes; split scopes before resolving.", "M2.3")
            if not decision["authority_refs"]:
                self.add("decision_without_authority", p, "Conflict resolution requires an explicit target authority.", "M2.3")
            if decision["strategy"] == "combine":
                selected_records = [permissions[key] for key in selected if key in permissions]
                if any(r["decision"] != "allow" or r["use"] != "reference" or r["attribute"] in ANCHORS for r in selected_records):
                    self.add("invalid_combination", p,
                             "Combine only compatible allowed references; contradictions, exact copies and competing anchors need explicit selection/scope splitting.", "M2.3")
                else:
                    combined_pairs.update(frozenset((left, right)) for i, left in enumerate(selected) for right in selected[i + 1:])

        active = {key: item for key, item in permissions.items() if key not in chosen or key in chosen[key]}
        valid = {}
        for permission_id, rule in permissions.items():
            p = ptr(ptr(path, "permissions"), permission_id)
            self.scope(rule["scope"], ptr(p, "scope"))
            binding = bindings.get(rule["binding_id"])
            if not binding:
                self.add("unresolved_binding", ptr(p, "binding_id"), "Permission binding is not registered.", "M2.3")
                continue
            asset = assets.get(binding["asset_id"])
            if not asset:
                continue
            if rule["decision"] != "unknown" and not rule["authority_refs"]:
                self.add("permission_without_authority", p, "Allowed/forbidden inheritance requires an explicit authority.", "M2.3")
            if rule["decision"] == "allow" and binding["state"] != "confirmed":
                self.add("permission_on_unconfirmed_binding", p, "Resolve the target/source mapping before allowing inheritance.", "M2.3")
            if rule["decision"] == "unknown":
                self.add("undecided_permission", p, "Unspecified inheritance remains undecided.", "M2.3", "unverified")
            if rule["decision"] == "allow":
                wanted_channel = "audio" if rule["attribute"] in AUDIO_ATTRIBUTES else "visual"
                if binding["channel"] != wanted_channel:
                    self.add("permission_channel_mismatch", p, "Attribute and selected source channel disagree.", "M2.3")
                if rule["attribute"] in ANCHORS:
                    if asset["media_type"] != "image" or rule["use"] != "anchor":
                        self.add("invalid_frame_anchor", p, "A frame anchor needs a separately registered image and use=anchor.", "M2.3")
                elif rule["use"] == "anchor":
                    self.add("invalid_anchor_attribute", p, "Anchor use belongs to first_frame, last_frame or keyframe.", "M2.3")
                if rule["use"] == "copy" and rule["attribute"] != "audio_content":
                    self.add("unsupported_copy_semantics", p, "This contract reserves exact copy for audio_content; visual inheritance uses reference/anchor.", "M2.3")
                if binding["channel"] == "audio" and asset["media_type"] == "video":
                    self.add("embedded_audio_not_independent_input", p,
                             "Video audio is still an embedded channel; M6/M11 must establish any separate audio input explicitly.", "M11", "unverified")
                if rule["attribute"] == "motion" and asset["media_type"] == "image":
                    self.add("still_image_not_motion_measurement", p,
                             "A still may guide a pose or inferred action but does not verify a temporal motion sequence.", "M4", "unverified")
            if "source_window" in rule:
                window = rule["source_window"]
                if window["end_seconds"] <= window["start_seconds"]:
                    self.add("invalid_source_window", ptr(p, "source_window"), "Source window end must exceed start.", "M2.3")
                if asset["media_type"] not in ("video", "audio"):
                    self.add("window_on_still_asset", ptr(p, "source_window"), "Source seconds require a temporal asset.", "M2.3")
                if "duration_seconds" in asset and window["end_seconds"] > asset["duration_seconds"]:
                    self.add("source_window_out_of_bounds", ptr(p, "source_window"), "Source window exceeds the recorded duration.", "M2.3")
            if permission_id in active:
                valid[permission_id] = (rule, binding)

        pairs = list(valid.items())
        for index, (left_id, (left, lb)) in enumerate(pairs):
            for right_id, (right, rb) in pairs[index + 1:]:
                if lb["entity_id"] != rb["entity_id"]:
                    continue
                if frozenset((left_id, right_id)) in combined_pairs:
                    continue
                overlap = scopes_overlap(left["scope"], right["scope"])
                if overlap is False:
                    continue
                same_source = source_key(lb, left) == source_key(rb, right)
                contradiction = (left["attribute"] == right["attribute"] and same_source
                                 and {left["decision"], right["decision"]} == {"allow", "forbid"})
                competition = (left["attribute"] == right["attribute"] and not same_source
                               and left["decision"] == right["decision"] == "allow")
                anchor_conflict = same_source and (
                    left["attribute"] in ANCHORS and left["decision"] == "allow"
                    and right["attribute"] in VISUAL_ANCHOR_PROPERTIES and right["decision"] == "forbid"
                    or right["attribute"] in ANCHORS and right["decision"] == "allow"
                    and left["attribute"] in VISUAL_ANCHOR_PROPERTIES and left["decision"] == "forbid")
                if not (contradiction or competition or anchor_conflict):
                    continue
                p = ptr(ptr(path, "permissions"), right_id)
                if overlap is None:
                    self.add("scope_overlap_unresolved", p,
                             f"Potential conflict with {left_id}; cross-domain/unknown scope needs M7/M9 mapping.", "M2.3", "unverified")
                else:
                    code = "anchor_permission_conflict" if anchor_conflict else ("permission_conflict" if contradiction else "competing_reference_sources")
                    self.add(code, p, f"Conflicts with {left_id}; resolve or split the exact scope explicitly.", "M2.3")

    def content(self, content, sources, path="/content", paths=None):
        assets = content.get("asset_registry", {})
        entities = content.get("entity_registry", {"entities": {}, "bindings": {}})
        references = content.get("reference_map", {"permissions": {}, "decisions": {}})
        paths = paths or {key: ptr(path, key) for key in OWNED.values()}
        self.assets(assets, sources, paths["asset_registry"])
        self.entities(entities, assets, paths["entity_registry"])
        self.permissions(references, assets, entities, paths["reference_map"])

    def artifact(self, artifact, path=""):
        if not self.shape(artifact, path):
            return
        kind = artifact["kind"]
        if kind == "M2ProposalBatch":
            proposal_ids = set()
            partitions = set()
            identities = set()
            for index, proposal in enumerate(artifact["proposals"]):
                self.artifact(proposal, ptr(ptr(path, "proposals"), index))
                if proposal["proposal_id"] in proposal_ids:
                    self.add("duplicate_proposal", path, "Proposal IDs must be unique within a batch.")
                proposal_ids.add(proposal["proposal_id"])
                identities.add((proposal["work_id"], proposal["base_version"]))
                for partition in proposal["changes"]:
                    if partition in partitions:
                        self.add("partition_write_conflict", path, "Only one child may propose a partition in a batch.")
                    partitions.add(partition)
            if len(identities) != 1:
                self.add("batch_base_mismatch", path, "A batch must target one work and one base version.")
            return
        sources = artifact["sources"]
        self.scan_refs({key: value for key, value in artifact.items() if key != "sources"}, sources, path)
        if kind == "M2Request":
            target, inputs = artifact["target"], artifact["inputs"]
            allowed = set(MINIMUM[target]) | {"intent_context", "capability_context"}
            if target == "M2":
                allowed |= set(self.defs["RequestInputs"]["properties"])
            for key in inputs.keys() - allowed:
                self.add("unrequested_projection", ptr(ptr(path, "inputs"), key), "Pass only fields read by the selected node.", "caller")
            for key in MINIMUM[target]:
                if key not in inputs:
                    self.add("missing_projected_input", ptr(ptr(path, "inputs"), key), "Required input for " + target + ".", "user")
                elif isinstance(inputs[key], dict) and inputs[key].get("state") == "unknown":
                    self.add("unknown_input", ptr(ptr(path, "inputs"), key), "Continue only independent work; this input remains unknown.", "user", "unverified")
            content = {"asset_registry": inputs.get("asset_context", {}),
                       "entity_registry": inputs.get("entity_context", {"entities": {}, "bindings": {}})}
            self.content(content, sources, paths={"asset_registry": ptr(ptr(path, "inputs"), "asset_context"),
                                                  "entity_registry": ptr(ptr(path, "inputs"), "entity_context"),
                                                  "reference_map": ptr(ptr(path, "inputs"), "reference_context")})
        elif kind == "M2Proposal":
            owned = OWNED[artifact["module_id"]]
            if set(artifact["changes"]) != {owned}:
                self.add("out_of_scope_write", ptr(path, "changes"), f"This child owns only {owned}.", artifact["module_id"])
            context = artifact["context"]
            if owned in context:
                self.add("self_context_write_ambiguity", ptr(path, "context"), "Do not duplicate the owned partition in read-only context.")
            allowed_context = set() if artifact["module_id"] == "M2.1" else {"asset_registry"}
            if artifact["module_id"] == "M2.3":
                allowed_context.add("entity_registry")
            if set(context) - allowed_context:
                self.add("unrequested_projection", ptr(path, "context"), "Child context must stay within its declared dependencies.")
            combined = {**context, **artifact["changes"]}
            self.content(combined, sources, paths={key: ptr(ptr(path, "changes" if key in artifact["changes"] else "context"), key) for key in OWNED.values()})
        else:
            self.content(artifact["content"], sources, ptr(path, "content"))
            seen = set()
            for index, history in enumerate(artifact["accepted_proposals"]):
                p = ptr(ptr(path, "accepted_proposals"), index)
                if history["proposal_id"] in seen:
                    self.add("duplicate_history_id", p, "Accepted proposal IDs must be unique.")
                seen.add(history["proposal_id"])
                if history["to_version"] != history["from_version"] + 1 or history["to_version"] > artifact["version"]:
                    self.add("invalid_acceptance_history", p, "Acceptance history must record a real, nonfuture version step.")
                if OWNED[history["module_id"]] != history["changed_partition"]:
                    self.add("history_ownership_mismatch", p, "Accepted history cannot attribute a partition to the wrong child.")
            for consumer_id, consumer in artifact["consumers"].items():
                p = ptr(ptr(path, "consumers"), consumer_id)
                if consumer["source_state_version"] > artifact["version"]:
                    self.add("future_consumer_version", p, "Consumer cannot depend on a future state.")
                if consumer["source_state_version"] == artifact["version"]:
                    for pointer in consumer["read_paths"]:
                        try:
                            read_pointer(artifact, pointer)
                        except (KeyError, IndexError):
                            self.add("unresolved_consumer_path", p, f"Declared dependency {pointer} does not exist.")
        issue_ids = set()
        for issue in artifact.get("issues", []):
            if issue["issue_id"] in issue_ids:
                self.add("duplicate_issue_id", ptr(path, "issues"), "Issue IDs must remain unique.")
            issue_ids.add(issue["issue_id"])
            if issue["state"] == "resolved" and ("resolution" not in issue or issue["resolution"]["issue_id"] != issue["issue_id"]):
                self.add("missing_issue_resolution", ptr(path, "issues"), "Resolved issue needs its matching, sourced resolution.")
            if issue["state"] == "open":
                self.add("declared_open_issue", "/issues/" + esc(issue["issue_id"]), issue["description"], issue["owner"], "unverified")


def source_key(binding, rule):
    return (binding["asset_id"], binding["channel"], stable_json(binding["source_selector"]),
            stable_json(rule.get("source_window")))


def scopes_overlap(left, right):
    """Return True/False only when the provided scope domains make it knowable."""
    if left["kind"] == "unknown" or right["kind"] == "unknown":
        return None
    if left["kind"] == "work" or right["kind"] == "work":
        return True
    if left["kind"] == right["kind"] == "shots":
        return bool(set(left["shot_ids"]) & set(right["shot_ids"]))
    if left["kind"] == right["kind"] == "time":
        if (left["domain"], left["timeline_id"]) != (right["domain"], right["timeline_id"]):
            return None
        return max(left["start_seconds"], right["start_seconds"]) < min(left["end_seconds"], right["end_seconds"])
    return None


def check_request_match(check, artifact, request):
    if not check.shape(request):
        return
    if request["kind"] != "M2Request":
        check.add("request_kind_mismatch", "/request", "--request needs an M2Request.")
        return
    check.artifact(request, "/request")
    proposals = artifact.get("proposals", []) if artifact.get("kind") == "M2ProposalBatch" else [artifact]
    for proposal in proposals:
        if proposal.get("kind") != "M2Proposal":
            check.add("request_match_unsupported", "", "Request comparison applies to proposals or proposal batches.")
            continue
        for field in ("work_id", "base_version"):
            if proposal[field] != request[field]:
                check.add("request_mismatch", "/" + field, "Proposal differs from its source request.")
        if proposal["source_request_id"] != request["request_id"]:
            check.add("request_mismatch", "/source_request_id", "Proposal source request ID differs.")
        if request["target"] not in ("M2", proposal["module_id"]):
            check.add("request_target_mismatch", "/module_id", "Proposal is outside the requested node.")
        for source_id, source in request["sources"].items():
            if source_id not in proposal["sources"]:
                check.add("request_source_omitted", "/sources/" + esc(source_id),
                          "Preserve the request's declared evidence projection; additional sources may use new IDs.")
            elif proposal["sources"][source_id] != source:
                check.add("request_source_redefinition", "/sources/" + esc(source_id),
                          "The proposal cannot redefine the request's evidence or authorization under the same source ID.")
        for field, context_key in (("asset_context", "asset_registry"), ("entity_context", "entity_registry")):
            if field in request["inputs"] and proposal["context"].get(context_key) != request["inputs"][field]:
                check.add("request_projection_mismatch", "/context/" + context_key, "Read-only context differs from the explicit request projection.")


def merged_sources(check, current, additions, path):
    result = copy.deepcopy(current)
    for source_id, source in additions.items():
        if source_id in result and result[source_id] != source:
            check.add("source_redefinition", ptr(path, source_id), "Use a new source ID for changed evidence; do not overwrite provenance.")
        else:
            result[source_id] = copy.deepcopy(source)
    return result


def collection_values(content, partition, subpath):
    value = content[partition]
    for key in subpath:
        value = value[key]
    return value


def accept(check, current, offered):
    check.artifact(current, "/current")
    check.artifact(offered, "/offered")
    if check.failed:
        return None
    if current["kind"] != "M2State" or offered["kind"] not in ("M2Proposal", "M2ProposalBatch"):
        check.add("accept_kind_mismatch", "", "accept requires a state and child proposal(s).")
        return None
    proposals = offered["proposals"] if offered["kind"] == "M2ProposalBatch" else [offered]
    result = copy.deepcopy(current)
    history_ids = {entry["proposal_id"] for entry in current["accepted_proposals"]}
    changed = set()
    issues = {issue["issue_id"]: copy.deepcopy(issue) for issue in current["issues"]}
    for proposal in proposals:
        if proposal["work_id"] != current["work_id"]:
            check.add("work_mismatch", "/offered/work_id", "Proposal belongs to another work.")
        if proposal["base_version"] != current["version"]:
            check.add("stale_base_version", "/offered/base_version", "Re-read current records and re-evaluate; changing only the number is insufficient.", proposal["module_id"])
        if proposal["proposal_id"] in history_ids:
            check.add("already_accepted_proposal", "/offered/proposal_id", "This operation ID was already accepted; do not repeat it.")
        partition = OWNED[proposal["module_id"]]
        if partition in changed:
            check.add("partition_write_conflict", "/offered/changes", "A partition has more than one proposer.")
        changed.add(partition)
        result["sources"] = merged_sources(check, result["sources"], proposal["sources"], "/sources")
        incoming = proposal["changes"][partition]
        for subpath in COLLECTIONS[partition]:
            old_collection = collection_values(current["content"], partition, subpath)
            new_collection = incoming
            for key in subpath:
                new_collection = new_collection[key]
            removed = set(old_collection) - set(new_collection)
            if removed:
                check.add("implicit_record_removal", "/content/" + partition,
                          "Version 1 does not delete accepted IDs; preserve records and resolve permissions explicitly: " + ", ".join(sorted(removed)), proposal["module_id"])
        result["content"][partition] = copy.deepcopy(incoming)
        for issue in proposal["issues"]:
            if issue["issue_id"] in issues and issues[issue["issue_id"]] != issue:
                check.add("issue_redefinition", "/issues/" + esc(issue["issue_id"]), "Preserve prior issue records; use an explicit resolution.")
            else:
                issues[issue["issue_id"]] = copy.deepcopy(issue)
        for resolution in proposal["resolutions"]:
            issue = issues.get(resolution["issue_id"])
            if not issue or issue["owner"] != proposal["module_id"] or issue["state"] != "open":
                check.add("out_of_scope_resolution", "/resolutions", "A child can resolve only its own existing open issue.")
            else:
                issue["state"] = "resolved"
                issue["resolution"] = copy.deepcopy(resolution)
    for proposal in proposals:
        for partition, projection in proposal["context"].items():
            for subpath in COLLECTIONS[partition]:
                selected = projection
                actual = result["content"][partition]
                for key in subpath:
                    selected, actual = selected[key], actual[key]
                for key, value in selected.items():
                    if actual.get(key) != value:
                        check.add("context_version_mismatch", "/offered/context/" + partition + "/" + esc(key),
                                  "A read-only dependency differs from the candidate accepted state.", proposal["module_id"])
    result["issues"] = list(issues.values())
    result["version"] = current["version"] + 1
    for proposal in proposals:
        result["accepted_proposals"].append({
            "proposal_id": proposal["proposal_id"], "module_id": proposal["module_id"],
            "source_request_id": proposal["source_request_id"], "from_version": current["version"],
            "to_version": result["version"], "changed_partition": OWNED[proposal["module_id"]],
        })
    check.artifact(result, "/candidate")
    return None if check.failed else result


def changed_paths(left, right, path=""):
    if type(left) is not type(right):
        return [path]
    if isinstance(left, dict):
        result = []
        for key in sorted(set(left) | set(right)):
            p = ptr(path, key)
            if key not in left or key not in right:
                result.append(p)
            else:
                result.extend(changed_paths(left[key], right[key], p))
        return result
    return [] if left == right else [path]


def impact(check, previous, current):
    check.artifact(previous, "/previous")
    check.artifact(current, "/current")
    if check.failed:
        return None
    if previous["kind"] != "M2State" or current["kind"] != "M2State":
        check.add("impact_kind_mismatch", "", "impact requires two M2State snapshots.")
        return None
    if previous["work_id"] != current["work_id"] or current["version"] <= previous["version"]:
        check.add("impact_version_mismatch", "", "Compare an earlier and later snapshot of the same work.")
        return None
    changes = changed_paths(previous, current)
    records = {}
    for consumer_id, consumer in previous["consumers"].items():
        if consumer["source_state_version"] != previous["version"]:
            records[consumer_id] = {"status": "stale", "reason": "Consumer already refers to another version; no new pass is inferred."}
            continue
        affected = [p for p in changes if any(p == q or p.startswith(q + "/") or q.startswith(p + "/") for q in consumer["read_paths"])]
        records[consumer_id] = {"status": "stale" if affected else "unchanged_dependencies", "changed_paths": affected,
                                "module_id": consumer["module_id"], "result_version": consumer["result_version"]}
    return {"changed_paths": changes, "consumers": records,
            "unregistered_dependencies": "unknown; no other modules were called or cleared"}


def result(check, command, started, inputs, extra=None):
    # Repeated checks may encounter the same source through several projections.
    unique = {stable_json(item): item for item in check.diagnostics}
    diagnostics = list(unique.values())
    failed = any(item["status"] == "fail" for item in diagnostics)
    output = {
        "kind": "M2ToolResult", "contract_version": VERSION, "package_version": PACKAGE_VERSION,
        "command": command, "execution_status": "completed",
        "outcome": "rejected" if failed else "completed",
        "audit": {"deterministic": "fail" if failed else "pass", "semantic": "unverified",
                  "media": "unverified", "overall": "fail" if failed else "unverified"},
        "diagnostics": diagnostics,
        "execution": {"call_id": "CALL-" + uuid.uuid4().hex, "started_utc": started,
                      "finished_utc": datetime.now(timezone.utc).isoformat(),
                      "input_sha256": [digest(item) for item in inputs], "contract_version": VERSION,
                      "operation": "read_only_calculation", "retries": 0,
                      "read_resources": ["references/contracts.json"] + (["references/module-registry.json"] if command == "route" and not failed else [])},
        "limitations": ["No media or network was read.", "Source truth and natural-language fidelity need Agent/human review.",
                        "No H3 mode, label, prompt, model inference or downstream invocation was executed."],
    }
    if extra:
        output.update(extra)
    return output


def load_json(path):
    def reject_constant(value):
        raise ValueError("Non-finite JSON number: " + value)

    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result

    return json.loads(Path(path).read_text(encoding="utf-8"), parse_constant=reject_constant, object_pairs_hook=unique_keys)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    route = sub.add_parser("route", help="Resolve the explicit module target without executing semantic work.")
    route.add_argument("request")
    check_parser = sub.add_parser("check", help="Check a public artifact and optionally its source request.")
    check_parser.add_argument("artifact")
    check_parser.add_argument("--request")
    accept_parser = sub.add_parser("accept", help="Return a new draft state after checking a child proposal/batch.")
    accept_parser.add_argument("state")
    accept_parser.add_argument("proposal")
    impact_parser = sub.add_parser("impact", help="Find changes affecting explicitly registered consumers.")
    impact_parser.add_argument("previous")
    impact_parser.add_argument("current")
    args = parser.parse_args(argv)
    started = datetime.now(timezone.utc).isoformat()
    try:
        schema = load_json(ROOT / "references/contracts.json")
        checker = Check(schema["$defs"])
        extra, inputs = {}, []
        if args.command == "route":
            request = load_json(args.request)
            inputs = [request]
            checker.artifact(request)
            if not checker.failed and request["kind"] != "M2Request":
                checker.add("route_kind_mismatch", "", "route requires an M2Request.")
            if not checker.failed:
                registry = load_json(ROOT / "references/module-registry.json")
                node = registry["nodes"][request["target"]]
                extra = {"dispatch": {"target": request["target"], "route_id": node["route_id"],
                                      "route_version": VERSION, "input_projection": copy.deepcopy(request["inputs"]),
                                      "resources": node["resources"], "return_to": node["return_to"],
                                      "semantic_execution": "not_started"}}
        elif args.command == "check":
            artifact = load_json(args.artifact)
            inputs = [artifact]
            checker.artifact(artifact)
            if args.request and not checker.failed:
                request = load_json(args.request)
                inputs.append(request)
                check_request_match(checker, artifact, request)
            extra = {"checked_kind": artifact.get("kind") if isinstance(artifact, dict) else None,
                     "request_match_checked": bool(args.request) and len(inputs) == 2}
        elif args.command == "accept":
            current, offered = load_json(args.state), load_json(args.proposal)
            inputs = [current, offered]
            accepted = accept(checker, current, offered)
            if accepted is not None:
                extra = {"outcome": "accepted_draft", "state": accepted,
                         "registry_views": {"AssetRegistry": "/state/content/asset_registry",
                                            "EntityRegistry": "/state/content/entity_registry",
                                            "ReferenceMap": "/state/content/reference_map"}}
        else:
            previous, current = load_json(args.previous), load_json(args.current)
            inputs = [previous, current]
            impact_result = impact(checker, previous, current)
            if impact_result is not None:
                extra["impact"] = impact_result
        output = result(checker, args.command, started, inputs, extra)
        print(json.dumps(output, ensure_ascii=False, indent=2, allow_nan=False))
        return 1 if checker.failed else 0
    except (OSError, ValueError, RecursionError) as error:
        print(json.dumps({"kind": "M2ToolResult", "contract_version": VERSION, "command": args.command,
                          "execution_status": "input_error", "outcome": "rejected",
                          "audit": {"deterministic": "fail", "semantic": "unverified", "media": "unverified", "overall": "fail"},
                          "diagnostics": [{"code": "input_or_resource_error", "message": str(error), "repair_target": "caller"}]},
                         ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
