#!/usr/bin/env python3
"""Portable M6 contract checker. Python 3.10+, standard library, no network.

Checks sound contracts, preserved dialogue, audio use and ID/shot ownership.
It does not inspect audio, assign final times, mix tracks or certify H3 generations.
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
OWNED = {"M6.1": "sources", "M6.2": "vocal_events", "M6.3": "music", "M6.4": "effects"}
CONTEXTS = {"source_context": "sources", "vocal_context": "vocal_events",
            "music_context": "music", "effects_context": "effects"}
MINIMUM = {"M6": ("sound_brief",), "M6.1": ("source_brief",),
           "M6.2": ("vocal_brief", "source_context"),
           "M6.3": ("music_brief", "reference_context"),
           "M6.4": ("effects_brief", "action_context")}
EMPTY = {part: {"items": {}} for part in OWNED.values()}
UNVERIFIED = ["semantic_intent", "source_authenticity", "audio_availability_and_quality",
              "measured_beat_authenticity", "actual_lip_sync", "generated_video_quality", "global_G0_G4"]


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

    def add(self, code, path, message, owner="M6", status="fail"):
        self.diagnostics.append({"code": code, "path": path, "message": message,
                                 "status": status, "blocking": status == "fail",
                                 "repair_target": owner})

    @property
    def failed(self):
        return any(x["blocking"] for x in self.diagnostics)

    def shape(self, artifact, expected=None, path=""):
        kind = artifact.get("kind") if isinstance(artifact, dict) else None
        if kind not in ("M6Request", "M6Proposal", "M6ProposalBatch", "M6State") or (expected and kind != expected):
            self.add("artifact_kind", path, "Unexpected artifact kind; expected " + str(expected))
            return False
        errors = shape_errors(artifact, self.defs[kind], self.defs, path)
        for where, message in errors:
            self.add("contract_shape", where, message)
        return not errors

    def refs(self, value, sources, path="", owner="M6"):
        if isinstance(value, dict):
            if value.get("state") == "unknown":
                self.add("explicit_unknown", path, value["reason"], owner, "unverified")
            for key, item in value.items():
                if ((key == "values" and "source_id" in value)
                        or (key == "value" and (value.get("state") == "known"
                            or ("path" in value and "source_version" in value)))):
                    # ExternalContext.values, KnownFact.value and Projection.value
                    # are opaque; their business keys are not protocol.
                    continue
                if key == "source_refs":
                    for i, source in enumerate(item):
                        if source not in sources:
                            self.add("unresolved_source", ptr(ptr(path, key), i), source, owner)
                elif key == "source_id":
                    if item not in sources:
                        self.add("unresolved_source", ptr(path, key), item, owner)
                    elif value.get("source_version") != sources[item]["version"]:
                        self.add("context_version", ptr(path, "source_version"), "Source version differs from registered source", owner)
                else:
                    self.refs(item, sources, ptr(path, key), owner)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                self.refs(item, sources, ptr(path, i), owner)

    def request(self, request, path=""):
        if not self.shape(request, "M6Request", path):
            return False
        target, inputs = request["target"], request["inputs"]
        for key in MINIMUM[target]:
            if key not in inputs:
                self.add("minimum_input_missing", ptr(ptr(path, "inputs"), key),
                         "Supply this input or an explicit unknown with a reason", target)
        self.refs(inputs, request["sources"], ptr(path, "inputs"), target)
        for ident, asset in inputs.get("audio_assets", {}).items():
            if asset["asset_id"] != ident:
                self.add("audio_asset_identity", ptr(path + "/inputs/audio_assets", ident), "Registered audio key must match asset_id", target)
            if asset["duration_seconds"] <= 0:
                self.add("audio_duration", ptr(path + "/inputs/audio_assets", ident), "Registered asset duration must be positive", target)
        for field, owner in {"task_context": "M1", "reference_context": "M2", "space_context": "M3", "action_context": "M4", "camera_context": "M5", "time_context": "M7", "state_context": "M8", "edit_context": "M9", "label_context": "M11", "source_context": "M6.1", "vocal_context": "M6.2", "music_context": "M6.3", "effects_context": "M6.4"}.items():
            context = inputs.get(field, {})
            if "owner" in context and context["owner"] not in (owner, "external"):
                self.add("context_owner", ptr(ptr(path, "inputs"), field), f"Expected readonly {owner} context", target)
            if "source_id" in context and context["source_version"] != request["sources"].get(context["source_id"], {}).get("version"):
                self.add("context_version", ptr(ptr(path, "inputs"), field), "External source version differs from source entry", target)
        for i, projection in enumerate(inputs.get("readonly_projection", [])):
            if projection["source_version"] != request["base_version"]:
                self.add("projection_version", ptr(ptr(ptr(path, "inputs"), "readonly_projection"), i), "Readonly projection must identify request base version", target)
        return not self.failed

    def proposal(self, proposal, request=None, path=""):
        if not self.shape(proposal, "M6Proposal", path):
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
        elif self.shape(request, "M6Request", "/request"):
            self.request(request, "/request")
            for field in ("work_id", "base_version", "sources"):
                if not same(proposal[field], request[field]):
                    self.add("request_fidelity", ptr(path, field), "Proposal differs from original request", owner)
            if proposal["source_request_id"] != request["request_id"]:
                self.add("request_binding", ptr(path, "source_request_id"), "Wrong original request", owner)
            if request["target"] != owner:
                self.add("request_target", ptr(path, "module_id"), "Child proposal requires a request addressed to that child", owner)
            if not same(proposal["context"], request["inputs"]):
                self.add("request_fidelity", ptr(path, "context"), "Readonly inputs were changed or omitted", owner)
        if request is None:
            self.request({"kind": "M6Request", "contract_version": VERSION,
                          "request_id": proposal["source_request_id"], "target": owner,
                          "work_id": proposal["work_id"], "base_version": proposal["base_version"],
                          "sources": proposal["sources"], "inputs": proposal["context"]}, path + "/declared_context")
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
        for field, part in CONTEXTS.items():
            context = proposal["context"].get(field)
            if isinstance(context, dict) and "items" in context:
                if part in known and not same(content[part], context):
                    self.add("readonly_conflict", ptr(ptr(path, "context"), field), "Proposed partition conflicts with readonly context", owner)
                else:
                    content[part] = context
                    known.add(part)
        self.content(content, known, ptr(path, "changes"))
        own_content = copy.deepcopy(EMPTY)
        own_content.update(proposal["changes"])
        self.domain_evidence(own_content, proposal["sources"], proposal["context"], ptr(path, "changes"), check_vocal_inputs=owner == "M6.2")
        return not self.failed

    def linked(self, reference, part, shot, content, known, path, owner):
        if reference.get("state") in ("unknown", "not_applicable"):
            return None
        if reference["kind"] == "external":
            if reference["shot_id"] != shot:
                self.add("cross_shot_reference", path, "External reference belongs to another shot", owner)
            self.add("external_record_unverified", path, "Source identity/version is checked; opaque external record content is not reinterpreted", owner, "unverified")
            return None
        if part not in known:
            self.add("reference_context_unknown", path, "Internal reference cannot be checked without " + part, owner, "unverified")
            return None
        record = content[part]["items"].get(reference["id"])
        if record is None:
            self.add("dangling_reference", path, reference["id"] + " is absent from " + part, owner)
        elif part in ("sources", "music"):
            if shot not in record["applies_to_shots"]:
                self.add("reference_outside_shot_scope", path, "Stable source/track is not declared for this shot", owner)
        elif record["shot_id"] != shot:
            self.add("cross_shot_reference", path, "Referenced event belongs to another shot", owner)
        return record

    def content(self, content, known, path="/content"):
        identifiers = {"sources": "sound_source_id", "vocal_events": "vocal_event_id",
                       "music": "music_id", "effects": "effect_id"}
        owners = {part: module for module, part in OWNED.items()}
        for part in sorted(known):
            owner = owners[part]
            for ident, record in content[part]["items"].items():
                where = path + "/" + part + "/items/" + esc(ident)
                if ident != record[identifiers[part]]:
                    self.add("record_identity", where, "Map key differs from stable record ID", owner)
                shot = record["shot_id"]
                if part in ("sources", "music") and shot not in record["applies_to_shots"]:
                    self.add("declaration_outside_shot_scope", where, "The declaration shot must be included in applies_to_shots", owner)
                source = None
                if "source_ref" in record:
                    source = self.linked(record["source_ref"], "sources", shot, content, known, where + "/source_ref", owner)
                if "track_ref" in record:
                    track = self.linked(record["track_ref"], "music", shot, content, known, where + "/track_ref", owner)
                    if record["audio_origin"] == "within_registered_audio":
                        if record["track_ref"].get("state") == "not_applicable":
                            self.add("audio_origin_binding", where + "/track_ref", "Retained audio requires a track reference or explicit unknown", owner)
                        if track and track["use_strategy"] not in ("fully_copy", "partially_copy", "unknown"):
                            self.add("audio_origin_binding", where + "/track_ref", "Retained event requires a copied audio track", owner)
                for field in ("subject_ref", "voice_ref", "action_ref"):
                    reference = record.get(field, {})
                    if reference.get("kind") == "external" and reference["shot_id"] != shot:
                        self.add("cross_shot_reference", where + "/" + field, "Reference belongs to another shot", owner)
                if part == "sources":
                    if record["source_kind"] == "bgm_audio" and record["subject_ref"].get("kind") == "external":
                        self.add("bgm_subject_invention", where + "/subject_ref", "BGM Audio is not a Subject or an invented speaker", owner)
                    if record["source_kind"] == "unknown":
                        self.add("source_kind_unknown", where, "Sound source remains unclassified", owner, "unverified")
                elif part == "vocal_events":
                    text, approved = record["original_text"], record["approved_text"]
                    approval = record["rewrite_approval"]
                    if record["event_kind"] in ("spoken_dialogue", "voiceover", "sung_lyric", "lyric_semantic"):
                        for field in ("original_text", "approved_text"):
                            value = record[field]
                            if isinstance(value, dict) and value.get("state") == "not_applicable":
                                self.add("verbal_text_required", where + "/" + field,
                                         "Verbal events need text or explicit unknown; missing words are not inapplicable", owner)
                    if isinstance(text, str) and isinstance(approved, str) and text != approved:
                        if approval.get("state") != "known" or approval.get("value") is not True:
                            self.add("unapproved_text_rewrite", where + "/approved_text", "Keep the original exact text; changes need separately recorded approval", owner)
                    elif isinstance(text, str) and not isinstance(approved, str):
                        self.add("approved_text_unknown", where + "/approved_text", "The original is preserved but approved output text is unresolved", owner, "unverified")
                    if record["event_kind"] == "lyric_semantic":
                        if record["lip_sync"] != "not_required":
                            self.add("lyric_lip_sync", where + "/lip_sync", "Semantic lyrics of copied BGM do not assign lip synchronization", owner)
                        if source and source["source_kind"] != "bgm_audio":
                            self.add("lyric_source", where + "/source_ref", "Semantic BGM lyrics must bind Audio, not an invented speaker", owner)
                        if record["audio_origin"] == "new":
                            self.add("lyric_new_voice", where, "Semantic BGM lyrics cannot introduce a new vocal performance", owner)
                    elif source and source["source_kind"] in ("bgm_audio", "environment", "object"):
                        self.add("vocal_source_kind", where + "/source_ref", "An independent vocal performance requires a speaker, narrator or independent voice", owner)
                    if record["event_kind"] != "unknown" and record["source_ref"].get("state") == "not_applicable":
                        self.add("vocal_source_required", where + "/source_ref", "Vocal events require a source binding or explicit unknown", owner)
                elif part == "music":
                    selection = record["audio_selection"]
                    asset = selection.get("asset")
                    window = selection.get("window", {})
                    strategy = record["use_strategy"]
                    if asset:
                        if asset["duration_seconds"] <= 0:
                            self.add("audio_duration", where + "/audio_selection", "Registered asset duration must be positive", owner)
                        if "start_seconds" in window:
                            if window["start_seconds"] >= window["end_seconds"] or window["end_seconds"] > asset["duration_seconds"]:
                                self.add("audio_window", where + "/audio_selection/window", "Audio selection must be nonempty and inside the currently registered asset", owner)
                            full = window["start_seconds"] == 0 and window["end_seconds"] == asset["duration_seconds"]
                            if record["whole_source"] == "yes" and not full:
                                self.add("whole_source_window", where + "/whole_source", "Whole source refers to the registered asset, not its historical mother track", owner)
                            if strategy == "fully_copy" and not full:
                                self.add("fully_copy_window", where + "/audio_selection/window", "A selected subwindow is partially_copy", owner)
                    if strategy in ("fully_copy", "partially_copy", "reference") and selection.get("state") == "not_applicable":
                        self.add("audio_asset_required", where + "/audio_selection", "Reference or copy strategy needs the registered asset or explicit unknown", owner)
                    if strategy == "fully_copy":
                        for field, bad in (("whole_source", "no"), ("additional_audio", "yes"), ("removals_or_replacements", "yes")):
                            if record[field] == bad:
                                self.add("fully_copy_conflict", where + "/" + field, "fully_copy uses the complete current asset as the entire final soundtrack; any added, deleted or replaced sound requires partially_copy", owner)
                            elif record[field] == "unknown":
                                self.add("fully_copy_unverified", where + "/" + field, "Entire soundtrack constraint remains unresolved", owner, "unverified")
                        for other_part in ("vocal_events", "effects"):
                            if other_part not in known:
                                self.add("soundtrack_context_unknown", where, "Cannot inspect " + other_part + " additions in this isolated call", owner, "unverified")
                            for event in content[other_part]["items"].values():
                                if event["audio_origin"] == "new":
                                    self.add("fully_copy_added_sound", where, "New vocal/effect audio conflicts with fully_copy, including additions in other shots", owner)
                        for other in content["music"]["items"].values():
                            if other["music_id"] != ident and other["use_strategy"] not in ("none", "unknown"):
                                if not same(selection, other["audio_selection"]) or other["use_strategy"] != "fully_copy":
                                    self.add("fully_copy_second_track", where, "Another soundtrack conflicts with the complete final source track", owner)
                    beat = record["beat_plan"]
                    if beat.get("kind") == "measured":
                        if not asset or not asset["available"]:
                            self.add("measured_audio_required", where + "/beat_plan", "Measured beat positions require the actual audio; BPM alone is not a measurement", owner)
                        elif beat["measurement_asset"] != {"asset_id": asset["asset_id"], "asset_version": asset["asset_version"]}:
                            self.add("measurement_asset_mismatch", where + "/beat_plan", "Beat evidence must name the current asset and version", owner)
                    if beat.get("kind") == "none" and beat["beat_times_seconds"]:
                        self.add("beat_kind_conflict", where + "/beat_plan", "No beat plan cannot contain beat times", owner)
                    if beat.get("kind") in ("planned", "measured"):
                        times = beat["beat_times_seconds"]
                        if any(left >= right for left, right in zip(times, times[1:])):
                            self.add("beat_order", where + "/beat_plan", "Beat candidates must be strictly increasing", owner)
                        if asset and any(t > asset["duration_seconds"] for t in times):
                            self.add("beat_outside_asset", where + "/beat_plan", "Beat position lies outside the registered source asset", owner)
                elif part == "effects":
                    if record["event_kind"] not in ("whole_track_silence", "unknown") and record["source_ref"].get("state") == "not_applicable":
                        self.add("effect_source_required", where + "/source_ref", "Sound effects require a source binding or explicit unknown", owner)
                    if record["event_kind"] == "action" and record["action_ref"].get("state") == "not_applicable":
                        self.add("action_sound_binding", where + "/action_ref", "Action sound requires an action reference or explicit unknown", owner)
                    if record["event_kind"] == "whole_track_silence":
                        if record["explicit_silence"].get("state") != "known" or record["explicit_silence"].get("value") is not True:
                            self.add("silence_authorization", where + "/explicit_silence", "Whole-track silence requires the user's explicit full-silence instruction; no music does not imply silence", owner)
                        if record["audio_origin"] != "none":
                            self.add("silence_audio_origin", where, "A whole-track silence directive cannot emit audio", owner)
                    elif record["audio_origin"] == "none":
                        self.add("effect_audio_origin", where, "A sound event must declare new, retained or unknown audio origin", owner)
        silence = [r for r in content["effects"]["items"].values() if r["event_kind"] == "whole_track_silence"]
        if silence:
            audible = bool(content["vocal_events"]["items"]) or any(r["use_strategy"] not in ("none", "unknown") for r in content["music"]["items"].values()) or any(r["event_kind"] != "whole_track_silence" for r in content["effects"]["items"].values())
            if audible:
                self.add("silence_sound_conflict", path, "Whole-track silence conflicts with declared vocal, music or effect events", "M6.4")

    def domain_evidence(self, content, sources, inputs=None, path="/content", check_vocal_inputs=False):
        texts = (inputs or {}).get("vocal_texts", {})
        if check_vocal_inputs:
            for ident in texts:
                if ident not in content["vocal_events"]["items"]:
                    self.add("verbatim_input_omitted", path + "/vocal_events", "Locked vocal text cannot be omitted or rebound to another event ID: " + ident, "M6.2")
        for ident, record in content["vocal_events"]["items"].items():
            where = path + "/vocal_events/items/" + esc(ident)
            texts = (inputs or {}).get("vocal_texts", {})
            if inputs is not None and ident in texts and record["original_text"] != texts[ident]:
                self.add("verbatim_input_changed", where + "/original_text", "Original dialogue/lyric text must retain every input character and punctuation mark", "M6.2")
            elif inputs is not None and isinstance(record["original_text"], str) and ident not in texts:
                self.add("verbatim_input_unverified", where, "Supply vocal_texts to verify original text mechanically", "M6.2", "unverified")
            if inputs is not None and isinstance(record["original_text"], str) and isinstance(record["approved_text"], str) and record["original_text"] != record["approved_text"]:
                approved = inputs.get("approved_vocal_texts", {}).get(ident)
                if approved != record["approved_text"]:
                    self.add("rewrite_request_fidelity", where + "/approved_text", "Changed text must match the separately approved text in the actual request", "M6.2")
            if record["rewrite_approval"].get("state") == "known":
                if not any(sources[s]["kind"] in ("user_requirement", "approved_plan") for s in record["rewrite_approval"]["source_refs"] if s in sources):
                    self.add("rewrite_approval_evidence", where, "Text rewriting needs a user requirement or approved-plan evidence", "M6.2")
        for ident, record in content["music"]["items"].items():
            where = path + "/music/items/" + esc(ident)
            asset = record["audio_selection"].get("asset")
            assets = (inputs or {}).get("audio_assets", {})
            if asset and inputs is not None:
                registered = assets.get(asset["asset_id"])
                if registered is None and assets:
                    self.add("audio_asset_fidelity", where + "/audio_selection/asset", "Asset ID is not present in the actual request's registered audio_assets", "M6.3")
                elif registered is None:
                    self.add("asset_registration_unverified", where, "Supply audio_assets to verify current asset/version identity", "M6.3", "unverified")
                elif not same(registered, asset):
                    self.add("audio_asset_fidelity", where + "/audio_selection/asset", "Proposed asset differs from actual request's registered asset", "M6.3")
            beat = record["beat_plan"]
            if beat.get("kind") == "measured" and not any(sources[s]["kind"] == "media_observation" for s in beat["source_refs"] if s in sources):
                self.add("beat_measurement_evidence", where + "/beat_plan", "Measured beat claims need media-observation evidence, not a BPM hypothesis", "M6.3")
        for ident, record in content["effects"]["items"].items():
            if record["event_kind"] != "whole_track_silence":
                continue
            where = path + "/effects/items/" + esc(ident)
            fact = record["explicit_silence"]
            if fact.get("state") == "known" and not any(sources[s]["kind"] == "user_requirement" for s in fact["source_refs"] if s in sources):
                self.add("silence_user_evidence", where, "Full silence must cite the user's requirement", "M6.4")
            if inputs is not None and not same(inputs.get("whole_track_silence"), fact):
                self.add("silence_request_fidelity", where, "Full silence must be explicitly present in the actual input, not inferred from no music", "M6.4")

    def state(self, state, path="", reject_blockers=True):
        if not self.shape(state, "M6State", path):
            return False
        self.refs(state["content"], state["sources"], path + "/content")
        self.refs(state["issues"], state["sources"], path + "/issues")
        self.content(state["content"], set(EMPTY), path + "/content")
        self.domain_evidence(state["content"], state["sources"], path=path + "/content")
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
        if check.request(request, "/requests/" + str(i)):
            if request["request_id"] in index:
                check.add("duplicate_request", "/requests/" + str(i), request["request_id"])
            index[request["request_id"]] = request
    return index


def accept(check, state, batch, requests):
    state_ok = check.state(state, reject_blockers=False)
    batch_ok = check.shape(batch, "M6ProposalBatch", "/batch")
    index = request_index(check, requests)
    if not state_ok or not batch_ok or check.failed:
        return None
    proposals = batch["proposals"]
    if batch["work_id"] != state["work_id"]:
        check.add("work_identity", "/batch/work_id", "Batch addresses another SoundPlan")
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
        candidate["content"][part] = copy.deepcopy(new)
        for source, entry in proposal["sources"].items():
            if source in candidate["sources"] and not same(candidate["sources"][source], entry):
                check.add("source_collision", "/sources/" + esc(source), "Source ID cannot be rebound", owner)
            candidate["sources"][source] = copy.deepcopy(entry)
        for issue in proposal["issues"]:
            existing = candidate["issues"].get(issue["issue_id"])
            if existing is not None and not same(existing, issue):
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
        for field, part in CONTEXTS.items():
            context = proposal["context"].get(field)
            if isinstance(context, dict) and "items" in context and not same(context, candidate["content"][part]):
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
                modules = list(OWNED) if request["target"] == "M6" else [request["target"]]
                payload = {"routes": [{"module_id": m, "resources": registry["modules"][m]["resources"],
                                        "write_scope": "/content/" + OWNED[m], "return_to": "M6",
                                        "minimum_inputs": list(MINIMUM[m]), "repair_target": m} for m in modules],
                           "route_status": "ready_with_unverified_inputs" if check.diagnostics else "ready_for_call",
                           "invocation": "not_invoked"}
        elif args.command == "check":
            artifact = get(args.proposal or args.state or args.artifact, "artifact")
            request = get(args.request, "request") if args.request else None
            index = request_index(check, get(args.requests, "requests")) if args.requests else {}
            if check.shape(artifact):
                kind = artifact["kind"]
                if kind == "M6Request": check.request(artifact)
                elif kind == "M6State": check.state(artifact)
                elif kind == "M6Proposal": check.proposal(artifact, request or index.get(artifact["source_request_id"]))
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
                    check.add("work_identity", "", "States address different SoundPlans")
                elif after["version"] < before["version"]:
                    check.add("impact_version", "", "After-state version cannot precede before-state")
                else: payload = {"impact": impact(before, after)}
        status = "fail" if check.failed else "pass"
        original_requests = []
        for artifact in loaded.values():
            if isinstance(artifact, dict) and artifact.get("kind") == "M6Request":
                original_requests.append(artifact)
            elif isinstance(artifact, list):
                original_requests.extend(r for r in artifact if isinstance(r, dict) and r.get("kind") == "M6Request")
        trace = {"call_id": "m6-" + uuid.uuid4().hex, "parent_module": "M6", "started_at": started,
                 "finished_at": datetime.now(timezone.utc).isoformat(), "package_version": PACKAGE_VERSION,
                 "schema_version": VERSION, "route_version": registry["route_version"], "registry_version": registry["registry_version"],
                 "input_digests": {k: digest(v) for k, v in loaded.items()},
                 "resources": {"references/contracts.json": digest(schema), "references/module-registry.json": digest(registry)},
                 "side_effects": "none", "operation_id": loaded["batch"].get("batch_id") if isinstance(loaded.get("batch"), dict) else None,
                 "revision": payload.get("state", {}).get("version"),
                 "request_ids": sorted({r["request_id"] for r in original_requests if isinstance(r.get("request_id"), str)}),
                 "input_versions": [{"request_id": r.get("request_id"), "target": r.get("target"), "base_version": r.get("base_version"), "contract_version": r.get("contract_version")} for r in original_requests],
                 "source_versions": {r["request_id"]: {k: v.get("version") for k, v in r.get("sources", {}).items() if isinstance(v, dict)} for r in original_requests if isinstance(r.get("request_id"), str) and isinstance(r.get("sources"), dict)},
                 "applicability": {"local_contract": status, "physical_and_media": "unverified"},
                 "retry": payload.get("acceptance", "not_applicable"), "output_status": status,
                 "error_codes": sorted({d["code"] for d in check.diagnostics if d["blocking"]})}
        result = {"kind": "M6ToolResult", "contract_version": VERSION, "command": args.command,
                  "execution": "completed", "disposition": "rejected" if check.failed else "checked_draft",
                  "validation": {"local_contract": status, "overall": "fail" if check.failed else "unverified", "unverified": UNVERIFIED},
                  "diagnostics": check.diagnostics, "trace": trace, **payload}
        if args.command == "route" and check.failed:
            result.update({"route_status": "blocked", "invocation": "not_invoked", "routes": []})
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 1 if check.failed else 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, RecursionError) as exc:
        print(json.dumps({"kind": "M6ToolError", "command": args.command,
                          "execution": "error", "error": str(exc), "side_effects": "none"}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
