#!/usr/bin/env python3
"""Deterministic H3 protocol compiler. No inference, networking or file writes.

This compiler consumes approved English fragments and explicit semantic declarations.
It checks their structure and provenance, not the truth of natural-language claims.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
VERSION = "1.0.0"
PROTOCOL_VERSION = "199b7d0e1fd95e7b3eafa8c15eca692534142427"
PARTS = {"M11.1": "capability_profile", "M11.2": "reference_binding",
         "M11.3": "prompt_compilation", "M11.4": "task_export"}
MODES = ["T2VA", "I2VA", "FL2VA", "L2VA", "Ref2VA"]
BASE_FIELDS = ["integrated_multimodal_description", "overall_soundscape", "non_diegetic_music"]
REF_FIELDS = ["subject_definitions", "summary", "retention_analysis", "detailed_description",
              "overall_soundscape", "non_diegetic_music"]
VISUAL_RETENTION = {"fully_preserved", "partially_preserved", "attribute_transfer", "weak_reference"}
AUDIO_RETENTION = {"fully_copy", "partially_copy", "reference", "weak_reference"}
PURPOSES = {"first_frame", "last_frame", "keyframe", "identity", "appearance", "composition",
            "style", "motion", "structure", "editing_source", "continuation_source",
            "audio_reuse", "audio_reference", "storyboard"}
NOT_RUN = ["natural_language_semantic_audit", "source_authenticity_verification", "media_file_read",
           "media_decode", "workflow_execution", "h3_inference", "generated_video_acceptance"]
LIMITATIONS = ["Only explicit JSON declarations, supplied evidence references and protocol structure were checked.",
               "English fragments and their semantic obligation coverage require Agent review.",
               "A source excerpt is supplied evidence, not independent verification of a deployment.",
               "Export does not load media, execute a workflow, run H3 or certify generated video quality."]
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
TOKEN_RE = re.compile(r"\{\{(ref|speaker|utterance|shot):([A-Za-z0-9_.-]+)\}\}")
RAW_LABEL_RE = re.compile(r"<[A-Za-z][A-Za-z _-]*\s+\d+>|\[Shot\s+\d+\]|\bS\d+\b")
META_RE = re.compile(r"(?:^|\n)\s*(?:TaskPlan|CapabilityProfile|CompilationResult|ReferenceBinding|"
                     r"source_refs|obligation_ids|profile_digest|contract_version|route_version|"
                     r"integrated_multimodal_description|subject_definitions|retention_analysis)\s*[:=]", re.I)


class ContractError(ValueError):
    def __init__(self, code, message, path="", owner="M11"):
        super().__init__(message)
        self.code, self.message, self.path, self.owner = code, message, path, owner

    def as_dict(self):
        return {"code": self.code, "detail": self.message, "path": self.path, "owner": self.owner}


def fail(code, message, path="", owner="M11"):
    raise ContractError(code, message, path, owner)


def canonical(value):
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError, RecursionError) as exc:
        fail("json_value", str(exc))


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def same(left, right):
    """JSON equality must not inherit Python's False == 0 / True == 1 behavior."""
    return canonical(left) == canonical(right)


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            fail("duplicate_json_key", "Duplicate object key: " + key)
        out[key] = value
    return out


def load(path):
    def bad_constant(value):
        fail("non_finite_number", "Non-finite JSON number: " + value)
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                          parse_constant=bad_constant)
    except ContractError:
        raise
    except (OSError, ValueError, RecursionError) as exc:
        fail("json_read", str(exc), str(path), "caller")


def obj(value, required=(), optional=(), path=""):
    if not isinstance(value, dict):
        fail("type", "Expected an object", path)
    missing, extra = set(required) - set(value), set(value) - set(required) - set(optional)
    if missing:
        fail("required", "Missing keys: " + ", ".join(sorted(missing)), path)
    if extra:
        fail("unknown_key", "Unknown keys: " + ", ".join(sorted(extra)), path)
    return value


def string(value, path="", allow_empty=False):
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        fail("type", "Expected a non-empty string", path)
    if any(ord(c) < 32 and c not in "\n\t\r" for c in value):
        fail("control_character", "Control characters are not allowed", path)
    return value


def identifier(value, path=""):
    string(value, path)
    if not ID_RE.fullmatch(value):
        fail("identifier", "Use a stable ASCII identifier containing letters, digits, _ or -", path)
    return value


def integer(value, path="", minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        fail("type", "Expected an integer >= " + str(minimum), path)
    return value


def boolean(value, path=""):
    if not isinstance(value, bool):
        fail("type", "Expected a boolean", path)
    return value


def choice(value, choices, path=""):
    if not isinstance(value, str) or value not in choices:
        fail("enum", "Expected one of: " + ", ".join(sorted(choices)), path)
    return value


def array(value, path="", minimum=0):
    if not isinstance(value, list) or len(value) < minimum:
        fail("type", "Expected an array with at least " + str(minimum) + " item(s)", path)
    return value


def unique_strings(value, path="", minimum=0):
    array(value, path, minimum)
    for item in value:
        string(item, path)
    if len(value) != len(set(value)):
        fail("duplicate", "Duplicate values", path)
    return value


def index(rows, key, path=""):
    array(rows, path)
    out = {}
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or key not in row:
            fail("required", "Each row needs " + key, path + "/" + str(i))
        rid = identifier(row[key], path + "/" + str(i) + "/" + key)
        if rid in out:
            fail("duplicate_id", "Duplicate " + key + ": " + rid, path)
        out[rid] = row
    return out


def evidence_refs(refs, sources, path="", minimum=1):
    unique_strings(refs, path, minimum)
    for ref in refs:
        if ref not in sources:
            fail("missing_source", "Unknown evidence source: " + ref, path, "caller")


def source_ids(value):
    result = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"source_refs", "evidence_refs"} and isinstance(child, list):
                result.update(x for x in child if isinstance(x, str))
            result.update(source_ids(child))
    elif isinstance(value, list):
        for child in value:
            result.update(source_ids(child))
    return result


def evidence_snapshot(value, sources):
    ids = sorted(source_ids(value))
    evidence_refs(ids, sources, "/evidence_snapshot", minimum=0)
    return {sid: {"version": sources[sid]["version"], "digest": digest(sources[sid])} for sid in ids}


def validate_sources(sources):
    if not isinstance(sources, dict) or not sources:
        fail("sources", "Supply at least one versioned evidence source", "/sources", "caller")
    for sid, source in sources.items():
        identifier(sid, "/sources")
        obj(source, ("kind", "locator", "version", "excerpt"), ("sha256",), "/sources/" + sid)
        for key in ("kind", "locator", "version", "excerpt"):
            string(source[key], "/sources/" + sid + "/" + key)
        if "sha256" in source and (not isinstance(source["sha256"], str) or not re.fullmatch(r"[a-f0-9]{64}", source["sha256"])):
            fail("sha256", "Expected a lowercase SHA-256 hex digest", "/sources/" + sid)


def validate_request(request):
    obj(request, ("kind", "contract_version", "route_version", "work_id", "base_version", "request_id",
                  "target", "sources", "inputs"), (), "")
    if request["kind"] != "M11Request":
        fail("kind", "Expected M11Request")
    for key in ("contract_version", "route_version"):
        if request[key] != VERSION:
            fail("version", "Unsupported " + key, "/" + key)
    identifier(request["work_id"], "/work_id")
    identifier(request["request_id"], "/request_id")
    integer(request["base_version"], "/base_version")
    choice(request["target"], PARTS, "/target")
    validate_sources(request["sources"])
    if not isinstance(request["inputs"], dict):
        fail("type", "inputs must be an object", "/inputs")
    canonical(request)


def path_parts(path):
    string(path, "/runtime/path")
    if path.startswith("/"):
        parts = path[1:].split("/")
        if any(re.search(r"~(?![01])", part) for part in parts):
            fail("mapping_path", "Invalid JSON Pointer escape", path)
        parts = [part.replace("~1", "/").replace("~0", "~") for part in parts]
    else:
        parts = [path]
    if any(not part or part in {"__proto__", "constructor", "prototype"} for part in parts):
        fail("mapping_path", "Empty or unsafe mapping component", path)
    return parts


def validate_mapping(mapping, sources, path, parameter=False, prompt=False, media=False):
    required = ("path", "evidence_refs") + (("type",) if parameter else ()) + (("format",) if prompt or media else ())
    optional = ("unit", "enum", "minimum", "maximum") if parameter else ()
    obj(mapping, required, optional, path)
    path_parts(mapping["path"])
    evidence_refs(mapping["evidence_refs"], sources, path + "/evidence_refs")
    if prompt:
        choice(mapping["format"], {"text"}, path + "/format")
    if media:
        choice(mapping["format"], {"ordered_channel_objects"}, path + "/format")
    if parameter:
        choice(mapping["type"], {"integer", "number", "string", "boolean"}, path + "/type")
        if "unit" in mapping:
            choice(mapping["unit"], {"ms", "seconds", "pixels", "fps", "unitless"}, path + "/unit")
        if "enum" in mapping:
            array(mapping["enum"], path + "/enum", 1)
        for key in ("minimum", "maximum"):
            if key in mapping and (isinstance(mapping[key], bool) or not isinstance(mapping[key], (int, float))):
                fail("type", "Parameter bounds must be numeric", path + "/" + key)
        if "minimum" in mapping and "maximum" in mapping and mapping["minimum"] > mapping["maximum"]:
            fail("parameter_range", "minimum exceeds maximum", path)


def capability(inputs, sources):
    obj(inputs, ("profile",), (), "/inputs")
    return validate_profile(inputs["profile"], sources)


def validate_profile(profile, sources):
    p = deepcopy(profile)
    obj(p, ("profile_id", "backend", "model", "workflow", "protocol_version", "evidence_refs", "protocol", "runtime"),
        ("profile_digest", "evidence_snapshot"), "/profile")
    supplied_digest = p.pop("profile_digest", None)
    supplied_evidence = p.pop("evidence_snapshot", None)
    identifier(p["profile_id"], "/profile/profile_id")
    for key in ("backend", "model", "workflow"):
        obj(p[key], ("name", "version"), (), "/profile/" + key)
        string(p[key]["name"])
        string(p[key]["version"])
    string(p["protocol_version"], "/profile/protocol_version")
    if p["protocol_version"] != PROTOCOL_VERSION:
        fail("protocol_version", "This compiler implements only the pinned official protocol revision", "/profile/protocol_version")
    evidence_refs(p["evidence_refs"], sources, "/profile/evidence_refs")
    protocol_sources = [sources[sid] for sid in p["evidence_refs"] if sources[sid]["kind"] == "official_protocol"]
    if not protocol_sources or any(s["version"] != PROTOCOL_VERSION for s in protocol_sources):
        fail("protocol_evidence", "The protocol profile must cite the pinned official protocol evidence")
    obj(p["protocol"], ("supported_modes", "language"), (), "/profile/protocol")
    unique_strings(p["protocol"]["supported_modes"], "/profile/protocol/supported_modes", 1)
    for mode in p["protocol"]["supported_modes"]:
        choice(mode, MODES, "/profile/protocol/supported_modes")
    if p["protocol"]["language"] != "en":
        fail("language", "This compiler implements the supplied English protocol", "/profile/protocol/language")
    runtime = p["runtime"]
    obj(runtime, ("status", "execution"), ("supported_modes", "parameters", "required_parameters", "media", "prompt", "mode", "limits", "evidence_refs"), "/profile/runtime")
    choice(runtime["status"], {"unknown", "documented"})
    choice(runtime["execution"], {"unknown", "simulation", "production"})
    if runtime["status"] == "unknown":
        if runtime != {"status": "unknown", "execution": "unknown"}:
            fail("unknown_runtime", "Unknown runtime must not contain invented mappings or execution claims", "/profile/runtime")
    else:
        needed = {"supported_modes", "parameters", "required_parameters", "media", "prompt", "mode", "evidence_refs"}
        if not needed <= set(runtime) or runtime["execution"] == "unknown":
            fail("runtime_mapping", "Documented runtime needs explicit mode, prompt, media and parameter mappings with evidence", "/profile/runtime")
        evidence_refs(runtime["evidence_refs"], sources, "/profile/runtime/evidence_refs")
        if runtime["execution"] == "simulation" and not any(sources[s]["kind"] == "simulation" for s in runtime["evidence_refs"]):
            fail("simulation_evidence", "A simulation profile must cite a simulation source", "/profile/runtime")
        if runtime["execution"] == "production" and any(sources[s]["kind"] == "simulation" for s in source_ids(runtime)):
            fail("simulation_not_production", "Simulation evidence cannot establish production readiness", "/profile/runtime")
        if runtime["execution"] == "production" and any(sources[s]["kind"] not in {"deployment", "workflow"} for s in source_ids(runtime)):
            fail("deployment_evidence", "Production mappings require deployment or workflow evidence, not prompt-guide citations", "/profile/runtime")
        if any(p[key]["name"] == "unknown" or p[key]["version"] == "unknown" for key in ("backend", "model", "workflow")):
            fail("runtime_identity", "A documented runtime needs explicit backend, model and workflow identities")
        unique_strings(runtime["supported_modes"], "/profile/runtime/supported_modes", 1)
        if not set(runtime["supported_modes"]) <= set(p["protocol"]["supported_modes"]):
            fail("runtime_modes", "Runtime modes must be within documented protocol modes", "/profile/runtime")
        if not isinstance(runtime["parameters"], dict) or "duration_ms" not in runtime["parameters"]:
            fail("duration_mapping", "Runtime must document canonical duration_ms", "/profile/runtime/parameters")
        paths = []
        for name, mapping in runtime["parameters"].items():
            identifier(name)
            validate_mapping(mapping, sources, "/profile/runtime/parameters/" + name, True)
            paths.append(path_parts(mapping["path"]))
        duration = runtime["parameters"]["duration_ms"]
        if duration.get("unit") not in {"ms", "seconds"} or duration["type"] not in {"integer", "number"}:
            fail("duration_mapping", "duration_ms requires numeric type and ms or seconds unit")
        unique_strings(runtime["required_parameters"], "/profile/runtime/required_parameters")
        if "duration_ms" not in runtime["required_parameters"] or not set(runtime["required_parameters"]) <= set(runtime["parameters"]):
            fail("required_parameters", "Required parameters must be mapped and include duration_ms")
        for key in ("media", "prompt", "mode"):
            validate_mapping(runtime[key], sources, "/profile/runtime/" + key, prompt=key == "prompt", media=key == "media")
            paths.append(path_parts(runtime[key]["path"]))
        for i, a in enumerate(paths):
            for b in paths[i + 1:]:
                if a == b[:len(a)] or b == a[:len(b)]:
                    fail("mapping_collision", "Runtime mapping paths must not overlap", "/profile/runtime")
        if "limits" in runtime:
            obj(runtime["limits"], (), ("max_assets",), "/profile/runtime/limits")
            if "max_assets" in runtime["limits"]:
                integer(runtime["limits"]["max_assets"], minimum=0)
    p["evidence_snapshot"] = evidence_snapshot(p, sources)
    if supplied_evidence is not None and not same(supplied_evidence, p["evidence_snapshot"]):
        fail("evidence_changed", "Profile consumed evidence changed; build a new profile from its declarations")
    actual = digest(p)
    if supplied_digest is not None and supplied_digest != actual:
        fail("profile_digest", "Profile fingerprint differs from its declarations", "/profile/profile_digest")
    p["profile_digest"] = actual
    return p


def checked_text(text, path, tokens=True):
    string(text, path)
    if META_RE.search(text):
        fail("meta_leak", "Machine metadata must not enter model-facing text", path)
    if RAW_LABEL_RE.search(text):
        fail("literal_label", "Use stable-ID placeholders instead of handwritten H3 labels", path)
    if not tokens and ("{{" in text or "}}" in text):
        fail("placeholder", "Placeholders are not allowed in this value", path)
    if re.search(r"</?(?:d|scenetrans|cutoff)(?:>|\s)", text):
        fail("literal_control", "Dialogue and continuation controls are emitted from structured declarations", path)
    if re.search(r"[<>]", re.sub(r'"[^"\n]*"', '', text)):
        fail("unknown_markup", "Unrecognized raw markup in an approved fragment", path)
    return text


def validate_plan(plan):
    obj(plan, ("duration_ms", "shots"), ("requested_mode",), "/inputs/plan")
    integer(plan["duration_ms"], "/inputs/plan/duration_ms", 1)
    array(plan["shots"], "/inputs/plan/shots", 1)
    shots = index(plan["shots"], "shot_id", "/inputs/plan/shots")
    previous = -1
    for i, shot in enumerate(plan["shots"]):
        obj(shot, ("shot_id", "start_ms"), (), "/inputs/plan/shots/" + str(i))
        start = integer(shot["start_ms"])
        if start <= previous or start >= plan["duration_ms"] or (i == 0 and start != 0):
            fail("shot_timeline", "Shot 1 starts at 0; later cuts strictly increase and precede the end", "/inputs/plan/shots")
        previous = start
    if "requested_mode" in plan:
        choice(plan["requested_mode"], MODES)
    return shots


def reference_binding(inputs, sources):
    obj(inputs, ("capability_profile", "plan", "assets", "subjects", "reference_items", "audio_bindings", "speakers"), (), "/inputs")
    profile = validate_profile(inputs["capability_profile"], sources)
    plan = inputs["plan"]
    shots = validate_plan(plan)
    assets = index(inputs["assets"], "asset_id", "/inputs/assets")
    subjects = index(inputs["subjects"], "subject_id", "/inputs/subjects")
    refs = index(inputs["reference_items"], "asset_id", "/inputs/reference_items")
    audios = index(inputs["audio_bindings"], "asset_id", "/inputs/audio_bindings")
    speakers = index(inputs["speakers"], "speaker_id", "/inputs/speakers")
    if set(assets) & set(subjects):
        fail("ambiguous_id", "Asset and Subject stable IDs must be distinct")
    labels = {"subjects": {}, "assets": {}, "speakers": {}, "shots": {sid: "[Shot " + str(i + 1) + "]" for i, sid in enumerate(shots)}}
    counts = {"image": 0, "video": 0, "audio": 0}
    media = []
    for aid, asset in assets.items():
        obj(asset, ("asset_id", "version", "media_type", "uri", "purpose", "source_refs"), ("enabled_audio",), "/inputs/assets/" + aid)
        string(asset["version"])
        string(asset["uri"])
        choice(asset["media_type"], counts)
        choice(asset["purpose"], PURPOSES)
        evidence_refs(asset["source_refs"], sources, "/inputs/assets/" + aid + "/source_refs")
        if "enabled_audio" in asset:
            boolean(asset["enabled_audio"])
            if asset["media_type"] != "video":
                fail("audio_channel", "enabled_audio is reserved for video sources")
        kind, purpose = asset["media_type"], asset["purpose"]
        if purpose in {"first_frame", "last_frame", "keyframe", "composition", "storyboard"} and kind != "image":
            fail("media_purpose", "A frame or composition anchor requires an image", "/inputs/assets/" + aid)
        if purpose in {"structure", "editing_source", "continuation_source"} and kind != "video":
            fail("media_purpose", "A video structural task requires a video", "/inputs/assets/" + aid)
        if purpose in {"audio_reuse", "audio_reference"} and kind == "image":
            fail("media_purpose", "An image cannot supply an audio channel", "/inputs/assets/" + aid)
        if kind == "audio" and purpose not in {"audio_reuse", "audio_reference"}:
            fail("media_purpose", "An audio source requires an audio purpose", "/inputs/assets/" + aid)
        if kind == "video" and purpose.startswith("audio_") and not asset.get("enabled_audio", False):
            fail("audio_not_enabled", "Video audio use requires enabled_audio:true", "/inputs/assets/" + aid)
        labels["assets"][aid] = {}
        channels = [kind] + (["audio"] if kind == "video" and asset.get("enabled_audio", False) else [])
        for channel in channels:
            counts[channel] += 1
            label = "<" + {"image": "Picture", "video": "Video", "audio": "Audio"}[channel] + " " + str(counts[channel]) + ">"
            labels["assets"][aid][channel] = label
            media.append({"asset_id": aid, "asset_version": asset["version"], "uri": asset["uri"],
                          "channel": channel, "category_index": counts[channel], "input_index": len(media) + 1,
                          "label": label, "purpose": purpose})
    purposes = [a["purpose"] for a in assets.values()]
    if not assets:
        inferred = "T2VA"
    elif purposes == ["first_frame"]:
        inferred = "I2VA"
    elif purposes == ["last_frame"]:
        inferred = "L2VA"
    elif len(purposes) == 2 and set(purposes) == {"first_frame", "last_frame"}:
        inferred = "FL2VA"
    else:
        inferred = "Ref2VA"
    mode = plan.get("requested_mode", inferred)
    if mode != inferred and not (mode == "Ref2VA" and assets):
        fail("mode_purpose_conflict", "Requested mode conflicts with declared reference purposes", "/inputs/plan/requested_mode")
    if mode not in profile["protocol"]["supported_modes"]:
        fail("unsupported_protocol_mode", "Profile does not document this protocol mode")
    if profile["runtime"]["status"] == "documented" and mode not in profile["runtime"]["supported_modes"]:
        fail("unsupported_runtime_mode", "The documented runtime explicitly excludes the selected mode")
    if mode == "FL2VA" and purposes != ["first_frame", "last_frame"]:
        fail("asset_order", "FL2VA inputs must explicitly serialize first frame before last frame", "/inputs/assets")
    if mode in {"FL2VA", "L2VA"} and plan["duration_ms"] % 10:
        fail("alignment_precision", "Two-decimal official alignment cannot exactly express this duration", "/inputs/plan/duration_ms")
    if mode != "Ref2VA" and (subjects or refs or audios):
        fail("base_reference_metadata", "Base modes do not take Ref2VA Subject/retention tables")
    for i, (sid, subject) in enumerate(subjects.items()):
        obj(subject, ("subject_id", "source_asset_ids", "description", "retention", "retention_reason", "shot_ids"), (), "/inputs/subjects/" + sid)
        unique_strings(subject["source_asset_ids"], minimum=1)
        if not set(subject["source_asset_ids"]) <= set(assets) or any(assets[a]["media_type"] == "audio" for a in subject["source_asset_ids"]):
            fail("subject_source", "Subject sources must be supplied image/video assets", "/inputs/subjects/" + sid)
        choice(subject["retention"], VISUAL_RETENTION)
        checked_text(subject["description"], "/inputs/subjects/" + sid + "/description")
        checked_text(subject["retention_reason"], "/inputs/subjects/" + sid + "/retention_reason")
        unique_strings(subject["shot_ids"], minimum=1)
        if not set(subject["shot_ids"]) <= set(shots):
            fail("unknown_shot", "Subject scope names an unknown shot", "/inputs/subjects/" + sid)
        labels["subjects"][sid] = "<Subject " + str(i + 1) + ">"
    for aid, ref in refs.items():
        obj(ref, ("asset_id", "description", "retention", "retention_reason", "shot_ids"), (), "/inputs/reference_items/" + aid)
        if aid not in assets or assets[aid]["media_type"] == "audio":
            fail("reference_asset", "Standalone visual references require an image/video asset")
        if assets[aid]["purpose"] not in {"first_frame", "last_frame", "keyframe", "composition", "storyboard", "structure", "editing_source", "continuation_source"}:
            fail("source_only_reference", "Identity, appearance, style and extracted motion sources belong in Subject definitions; standalone entries need a frame, storyboard or whole-video purpose")
        choice(ref["retention"], VISUAL_RETENTION)
        checked_text(ref["description"], "/inputs/reference_items/" + aid + "/description")
        checked_text(ref["retention_reason"], "/inputs/reference_items/" + aid + "/retention_reason")
        unique_strings(ref["shot_ids"], minimum=1)
        if not set(ref["shot_ids"]) <= set(shots):
            fail("unknown_shot", "Reference scope names an unknown shot")
    first_times = []
    for sid, speaker in speakers.items():
        obj(speaker, ("speaker_id", "first_vocal_ms"), ("tie_order", "source_refs", "first_event_kind"), "/inputs/speakers/" + sid)
        when = integer(speaker["first_vocal_ms"])
        if when >= plan["duration_ms"]:
            fail("speaker_timeline", "First vocal event must lie within the target video")
        if "tie_order" in speaker:
            integer(speaker["tie_order"])
        if "source_refs" in speaker:
            evidence_refs(speaker["source_refs"], sources)
        if "first_event_kind" in speaker:
            choice(speaker["first_event_kind"], {"speech", "singing", "nonverbal"})
        first_times.append((when, speaker.get("tie_order", 0), sid))
    if len({(t, order) for t, order, _ in first_times}) != len(first_times):
        fail("speaker_order_ambiguous", "Simultaneous first vocals need distinct explicit tie_order values")
    for i, (_, _, sid) in enumerate(sorted(first_times)):
        labels["speakers"][sid] = "S" + str(i + 1)
    for aid, audio in audios.items():
        obj(audio, ("asset_id", "role", "description", "retention", "retention_reason", "full_source", "entire_soundtrack", "additional_layers", "replaced_layers"),
            ("speaker_id", "subject_id", "source_window_ms", "target_window_ms"), "/inputs/audio_bindings/" + aid)
        if aid not in assets or "audio" not in labels["assets"][aid]:
            fail("audio_not_enabled", "Audio binding requires an actual audio input or explicitly enabled video audio")
        choice(audio["role"], {"reuse", "reference"})
        choice(audio["retention"], AUDIO_RETENTION)
        purpose = assets[aid]["purpose"]
        if purpose in {"audio_reuse", "audio_reference"} and audio["role"] != purpose.removeprefix("audio_"):
            fail("audio_purpose_conflict", "The declared audio asset purpose must agree with its binding role")
        if (audio["role"] == "reuse") != (audio["retention"] in {"fully_copy", "partially_copy"}):
            fail("audio_role", "Reuse copies a signal; reference does not claim copied signal")
        for key in ("full_source", "entire_soundtrack"):
            boolean(audio[key])
        for key in ("additional_layers", "replaced_layers"):
            unique_strings(audio[key])
        if audio["retention"] == "fully_copy" and (not audio["full_source"] or not audio["entire_soundtrack"] or audio["additional_layers"] or audio["replaced_layers"] or "source_window_ms" in audio):
            fail("fully_copy_conflict", "fully_copy requires the complete source to be the entire unchanged final soundtrack")
        if audio["retention"] == "fully_copy" and audio.get("target_window_ms", [0, plan["duration_ms"]]) != [0, plan["duration_ms"]]:
            fail("fully_copy_window", "A fully copied entire soundtrack must occupy the complete target interval")
        for key in ("description", "retention_reason"):
            checked_text(audio[key], "/inputs/audio_bindings/" + aid + "/" + key)
        if re.search(r"\bS\d+\b|\{\{speaker:", audio["retention_reason"]):
            fail("speaker_in_retention", "Retention analysis must not contain S labels")
        if "speaker_id" in audio and audio["speaker_id"] not in speakers:
            fail("unknown_speaker", "Audio voice binding names an unknown speaker")
        if "subject_id" in audio and (audio["subject_id"] not in subjects or "speaker_id" not in audio):
            fail("audio_subject", "An audio Subject voice binding also needs its speaker")
        for key in ("source_window_ms", "target_window_ms"):
            if key in audio:
                window = audio[key]
                array(window, minimum=2)
                if len(window) != 2:
                    fail("audio_window", "Audio window must contain start/end milliseconds")
                integer(window[0]); integer(window[1], minimum=1)
                if window[0] >= window[1] or (key == "target_window_ms" and window[1] > plan["duration_ms"]):
                    fail("audio_window", "Invalid source or target audio window")
    if any(a["retention"] == "fully_copy" for a in audios.values()) and len(audios) != 1:
        fail("fully_copy_multiple_tracks", "A complete unchanged final soundtrack cannot also have another enabled audio binding")
    if mode == "Ref2VA":
        source_only = {aid for subject in subjects.values() for aid in subject["source_asset_ids"]}
        for aid, asset in assets.items():
            if asset["media_type"] != "audio" and aid not in refs and aid not in source_only and not asset["purpose"].startswith("audio_"):
                fail("reference_coverage", "Each visual asset needs a standalone role or a Subject source relationship", "/inputs/assets/" + aid)
            if asset["purpose"] in {"first_frame", "last_frame", "keyframe", "composition", "storyboard", "structure", "editing_source", "continuation_source"} and aid not in refs:
                fail("standalone_reference_required", "Frame and whole-video tasks require standalone reference entries", "/inputs/assets/" + aid)
            if "audio" in labels["assets"][aid] and aid not in audios:
                fail("audio_coverage", "Every enabled audio channel requires an explicit binding", "/inputs/assets/" + aid)
    task_types = []
    for predicate, task in ((any(p in {"first_frame", "last_frame", "keyframe", "composition"} for p in purposes), "keyframe completion"),
                            (bool(subjects) or any(p in {"identity", "appearance", "style", "motion", "structure", "storyboard"} for p in purposes), "reference generation"),
                            ("editing_source" in purposes, "video editing"), ("continuation_source" in purposes, "video continuation"),
                            (any(a["role"] == "reuse" for a in audios.values()), "audio reuse"),
                            (any(a["role"] == "reference" for a in audios.values()), "audio reference")):
        if predicate:
            task_types.append(task)
    editing = [a for a in assets if assets[a]["purpose"] == "editing_source"]
    if len(editing) > 1:
        fail("editing_source_count", "This compiler supports one explicit editing source")
    if editing and labels["assets"][editing[0]]["video"] != "<Video 1>":
        fail("editing_source_order", "Serialize the editing source as Video 1 for the exact official opening")
    result = {"kind": "ReferenceBinding", "contract_version": VERSION, "mode": mode,
              "profile_digest": profile["profile_digest"], "duration_ms": plan["duration_ms"],
              "shots": deepcopy(plan["shots"]), "labels": labels, "media_inputs": media,
              "task_types": task_types, "declarations": deepcopy(inputs),
              "evidence_snapshot": evidence_snapshot(inputs, sources)}
    result["binding_digest"] = digest(result)
    return result


def validate_binding(binding, sources):
    if not isinstance(binding, dict) or not isinstance(binding.get("declarations"), dict):
        fail("binding_contract", "Supply a self-contained ReferenceBinding including declarations")
    expected = reference_binding(binding["declarations"], sources)
    if not same(binding, expected):
        fail("binding_mismatch", "ReferenceBinding differs from its recomputed declarations")
    return expected


def timestamp(milliseconds):
    return f"{milliseconds // 60000:02d}:{milliseconds // 1000 % 60:02d}.{milliseconds % 1000:03d}"


def seconds_centiseconds(milliseconds):
    return str(milliseconds // 1000) + "." + f"{milliseconds % 1000 // 10:02d}"


def words_only(text):
    # Punctuation may change; word boundaries and spelling may not silently change.
    return re.findall(r"\w+", text, re.UNICODE)


def compile_prompt(inputs, sources):
    obj(inputs, ("binding", "fragments", "obligations", "utterances", "complete_silence", "music_present"), ("visible_text",), "/inputs")
    binding = validate_binding(inputs["binding"], sources)
    mode, labels = binding["mode"], binding["labels"]
    declaration = binding["declarations"]
    boolean(inputs["complete_silence"]); boolean(inputs["music_present"])
    fragments = inputs["fragments"]
    obj(fragments, ("style", "shots", "overall_soundscape", "non_diegetic_music"), ("summary",), "/inputs/fragments")
    checked_text(fragments["style"], "/inputs/fragments/style")
    shot_fragments = index(fragments["shots"], "shot_id", "/inputs/fragments/shots")
    if list(shot_fragments) != list(labels["shots"]):
        fail("shot_fragment_order", "Supply exactly one fragment per actual shot in planned order")
    obligations = index(inputs["obligations"], "obligation_id", "/inputs/obligations")
    array(inputs["obligations"], minimum=1)
    for oid, obligation in obligations.items():
        obj(obligation, ("obligation_id", "description"), ("shot_id", "source_refs"), "/inputs/obligations/" + oid)
        string(obligation["description"])
        if "shot_id" in obligation and obligation["shot_id"] not in shot_fragments:
            fail("unknown_shot", "Obligation names an unknown shot")
        if "source_refs" in obligation:
            evidence_refs(obligation["source_refs"], sources)
    utterances = index(inputs["utterances"], "utterance_id", "/inputs/utterances")
    rendered_utterances, utterance_usage, punctuation_trace, utterance_order = {}, {}, [], []
    utterance_source_trace = []
    audio_sources = {audio["asset_id"]: audio for audio in declaration["audio_bindings"]}
    asset_sources = {asset["asset_id"]: asset for asset in declaration["assets"]}
    for uid, utterance in utterances.items():
        obj(utterance, ("utterance_id", "language", "text", "start_ms", "shot_id"),
            ("source_text", "punctuation_change", "mode", "visible_lips_subject", "continues_from", "continues_to", "cutoff",
             "origin", "audio_asset_id", "source_language", "source_refs", "speaker_id"), "/inputs/utterances/" + uid)
        origin = utterance.get("origin", "generated")
        choice(origin, {"generated", "copied_audio"}, "/inputs/utterances/" + uid + "/origin")
        if "source_refs" in utterance:
            evidence_refs(utterance["source_refs"], sources, "/inputs/utterances/" + uid + "/source_refs")
        if "source_language" in utterance:
            string(utterance["source_language"])
            if "source_text" not in utterance or utterance["source_language"] != utterance["language"]:
                fail("dialogue_language_fidelity", "A supplied source language requires source_text and must equal the target dialogue language")
        if origin == "copied_audio":
            required_copy = {"audio_asset_id", "source_text", "source_language", "source_refs"}
            if not required_copy <= set(utterance):
                fail("copied_dialogue_declaration", "Copied dialogue needs audio_asset_id, source_text, source_language and source_refs", "/inputs/utterances/" + uid)
            aid = identifier(utterance["audio_asset_id"])
            if aid not in audio_sources or audio_sources[aid]["role"] != "reuse":
                fail("copied_dialogue_source", "Copied dialogue must name an explicitly enabled reused Audio signal; a timbre reference is not a copy", "/inputs/utterances/" + uid)
            bound_speaker = audio_sources[aid].get("speaker_id")
            if bound_speaker is not None and utterance.get("speaker_id") != bound_speaker:
                fail("copied_dialogue_speaker", "A copied source explicitly bound to a concrete voice must preserve that speaker")
            if "speaker_id" not in utterance and any(key in utterance for key in ("mode", "visible_lips_subject")):
                fail("soundtrack_cue_source", "A soundtrack verbal cue has no independently performing on-screen or voiceover speaker")
            if "target_window_ms" in audio_sources[aid]:
                lower, upper = audio_sources[aid]["target_window_ms"]
                if not lower <= integer(utterance["start_ms"]) < upper:
                    fail("copied_dialogue_window", "Copied dialogue must begin inside the declared reused-audio target window")
        elif "audio_asset_id" in utterance:
            fail("generated_dialogue_source", "An audio_asset_id copy assertion requires origin:copied_audio; reference-based re-performance remains generated")
        if origin == "generated" and "speaker_id" not in utterance:
            fail("speaker_required", "Generated or re-performed words require an explicit speaker; only directly reused soundtrack cues may omit it")
        if "speaker_id" in utterance and utterance["speaker_id"] not in labels["speakers"]:
            fail("unknown_speaker", "Utterance names an unregistered speaker")
        if utterance["shot_id"] not in shot_fragments:
            fail("unknown_shot", "Utterance names an unknown shot")
        string(utterance["language"])
        if not re.fullmatch(r"[A-Za-z][A-Za-z -]*", utterance["language"]):
            fail("dialogue_language", "Use an explicit English language name in the language marker")
        string(utterance["text"])
        if re.search(r"[<>]|\{\{|\}\}", utterance["text"]):
            fail("dialogue_control", "Dialogue text cannot contain markup or placeholders")
        when = integer(utterance["start_ms"])
        speaker = next((s for s in declaration["speakers"] if s["speaker_id"] == utterance.get("speaker_id")), None)
        shot_index = list(shot_fragments).index(utterance["shot_id"])
        start = binding["shots"][shot_index]["start_ms"]
        end = binding["shots"][shot_index + 1]["start_ms"] if shot_index + 1 < len(binding["shots"]) else binding["duration_ms"]
        if when < start or when >= end or (speaker is not None and when < speaker["first_vocal_ms"]):
            fail("utterance_timeline", "Utterance must lie in its shot and cannot precede the speaker's first vocal event")
        if "source_text" in utterance:
            string(utterance["source_text"])
            if utterance["source_text"] != utterance["text"]:
                if mode != "Ref2VA" or not utterance.get("punctuation_change") or words_only(utterance["source_text"]) != words_only(utterance["text"]):
                    fail("dialogue_fidelity", "Only explicitly recorded Ref2VA punctuation changes may differ from source_text")
                string(utterance["punctuation_change"])
                punctuation_trace.append({"utterance_id": uid, "source_text": utterance["source_text"], "text": utterance["text"], "reason": utterance["punctuation_change"]})
            elif utterance.get("punctuation_change"):
                fail("punctuation_trace", "Do not claim a punctuation change when the text is unchanged")
        elif "punctuation_change" in utterance:
            fail("punctuation_source", "Punctuation changes require source_text")
        if "mode" in utterance:
            choice(utterance["mode"], {"on_screen", "off_screen_voiceover"})
        if "visible_lips_subject" in utterance and utterance["visible_lips_subject"] not in labels["subjects"]:
            fail("voiceover_subject", "Visible closed-lips subject must be a registered Subject")
        if "visible_lips_subject" in utterance and utterance.get("mode") != "off_screen_voiceover":
            fail("voiceover_subject", "Closed-lips control belongs to an explicit off-screen voiceover")
        if "cutoff" in utterance:
            boolean(utterance["cutoff"])
            if utterance["cutoff"] and shot_index != len(binding["shots"]) - 1:
                fail("cutoff_position", "A target-end cutoff belongs in the final shot")
        prefix = "<scenetrans>" if "continues_from" in utterance else ""
        suffix = "<scenetrans>" if "continues_to" in utterance else ""
        if utterance.get("cutoff", False):
            suffix += "<cutoff>"
        rendered_utterances[uid] = "<d>[" + utterance["language"] + "] " + prefix + utterance["text"] + suffix + "</d>"
        if "visible_lips_subject" in utterance:
            rendered_utterances[uid] += " " + labels["subjects"][utterance["visible_lips_subject"]] + " keeps their lips closed."
        if origin == "copied_audio" and "speaker_id" in utterance:
            rendered_utterances[uid] += " (copied from " + labels["assets"][utterance["audio_asset_id"]]["audio"] + ")"
        elif origin == "copied_audio":
            rendered_utterances[uid] = labels["assets"][utterance["audio_asset_id"]]["audio"] + " reaches the phrase " + rendered_utterances[uid]
        utterance_source_trace.append({"utterance_id": uid, "origin": origin,
                                       "speaker_id": utterance.get("speaker_id"),
                                       "audio_asset_id": utterance.get("audio_asset_id"),
                                       "audio_asset_version": asset_sources[utterance["audio_asset_id"]]["version"] if origin == "copied_audio" else None,
                                       "audio_label": labels["assets"][utterance["audio_asset_id"]]["audio"] if origin == "copied_audio" else None,
                                       "source_text": utterance.get("source_text"), "source_language": utterance.get("source_language"),
                                       "source_refs": deepcopy(utterance.get("source_refs", []))})
        utterance_usage[uid] = []
    for uid, utterance in utterances.items():
        for key, reverse, delta in (("continues_to", "continues_from", 1), ("continues_from", "continues_to", -1)):
            if key in utterance:
                other = utterances.get(utterance[key])
                if not other or other.get(reverse) != uid or other.get("speaker_id") != utterance.get("speaker_id") or other["language"] != utterance["language"]:
                    fail("cross_shot_speech", "Cross-shot speech must be reciprocal and preserve speaker/language")
                if other.get("origin", "generated") != utterance.get("origin", "generated") or other.get("audio_asset_id") != utterance.get("audio_asset_id"):
                    fail("cross_shot_speech", "Cross-shot speech must preserve its generation/copy relationship and source signal")
                if list(shot_fragments).index(other["shot_id"]) - list(shot_fragments).index(utterance["shot_id"]) != delta:
                    fail("cross_shot_speech", "Speech continuations must cross adjacent actual shots")
    for speaker in declaration["speakers"]:
        events = [u["start_ms"] for u in utterances.values() if u.get("speaker_id") == speaker["speaker_id"]]
        if events and speaker.get("first_event_kind", "speech") == "speech" and min(events) != speaker["first_vocal_ms"]:
            fail("first_vocal_mismatch", "The first declared speech time must match the first actual utterance")
    trace = []
    covered = set()

    def replace(text, field, shot_id=None, allow_utterances=False, retention=False):
        checked_text(text, field)
        def token(match):
            kind, sid = match.groups()
            if kind == "ref":
                if sid in labels["subjects"]:
                    subject = next(s for s in declaration["subjects"] if s["subject_id"] == sid)
                    if shot_id is not None and shot_id not in subject["shot_ids"]:
                        fail("reference_scope", "Subject is referenced outside its declared shot scope", field)
                    return labels["subjects"][sid]
                bits = sid.split(".")
                aid, channel = bits[0], bits[1] if len(bits) == 2 else None
                if aid not in labels["assets"] or len(bits) > 2:
                    fail("unknown_reference", "Unknown reference placeholder: " + sid, field)
                choices = labels["assets"][aid]
                standalone = next((r for r in declaration["reference_items"] if r["asset_id"] == aid), None)
                if shot_id is not None and standalone and channel != "audio" and shot_id not in standalone["shot_ids"]:
                    fail("reference_scope", "Standalone reference is used outside its declared shot scope", field)
                if shot_id is not None and not standalone and "audio" not in choices:
                    fail("source_only_label", "An identity-only source picture/video is referenced through its Subject, not as a standalone label", field)
                if channel is None:
                    if len(choices) != 1:
                        fail("ambiguous_channel", "Choose .video or .audio for a dual-channel asset", field)
                    return next(iter(choices.values()))
                if channel not in choices:
                    fail("unknown_channel", "Reference channel is not enabled: " + sid, field)
                return choices[channel]
            if kind == "shot":
                if sid not in labels["shots"]:
                    fail("unknown_shot", "Unknown shot placeholder: " + sid, field)
                return labels["shots"][sid]
            if kind == "speaker":
                if retention:
                    fail("speaker_in_retention", "Retention analysis does not use speaker labels", field)
                if sid not in labels["speakers"]:
                    fail("unknown_speaker", "Unknown speaker placeholder: " + sid, field)
                return labels["speakers"][sid]
            if not allow_utterances or sid not in rendered_utterances:
                fail("utterance_placement", "Utterances are allowed only in their detailed shot fragment", field)
            if utterances[sid]["shot_id"] != shot_id:
                fail("utterance_shot", "Utterance placeholder appears in the wrong shot", field)
            utterance_usage[sid].append(shot_id)
            utterance_order.append(sid)
            return rendered_utterances[sid]
        result = TOKEN_RE.sub(token, text)
        if "{{" in result or "}}" in result:
            fail("unresolved_placeholder", "Unknown or malformed placeholder", field)
        return result

    style = replace(fragments["style"], "/fragments/style")
    details = []
    for i, (sid, fragment) in enumerate(shot_fragments.items()):
        obj(fragment, ("shot_id", "text", "obligation_ids"), (), "/fragments/shots/" + sid)
        unique_strings(fragment["obligation_ids"], minimum=1)
        for oid in fragment["obligation_ids"]:
            if oid not in obligations:
                fail("unknown_obligation", "Fragment cites an undeclared obligation: " + oid)
            if obligations[oid].get("shot_id", sid) != sid:
                fail("obligation_scope", "Fragment claims an obligation from another shot")
            covered.add(oid)
            trace.append({"obligation_id": oid, "shot_id": sid, "output_field": "detailed_description" if mode == "Ref2VA" else "integrated_multimodal_description"})
        text = replace(fragment["text"], "/fragments/shots/" + sid, sid, True)
        for uid, utterance in utterances.items():
            if utterance["shot_id"] != sid:
                continue
            if "{{utterance:" + uid + "}}" not in fragment["text"]:
                continue
            before_utterance = fragment["text"].split("{{utterance:" + uid + "}}", 1)[0]
            if "speaker_id" in utterance:
                if "{{speaker:" + utterance["speaker_id"] + "}}" not in fragment["text"]:
                    fail("speaker_binding", "A dialogue fragment must explicitly name its stable speaker")
                preceding_speakers = re.findall(r"\{\{speaker:([A-Za-z0-9_-]+)\}\}", before_utterance)
                if not preceding_speakers or preceding_speakers[-1] != utterance["speaker_id"]:
                    fail("speaker_binding", "The nearest preceding speaker marker must bind this utterance")
            if utterance.get("mode") == "off_screen_voiceover":
                local_delivery = before_utterance.rsplit("{{speaker:" + utterance["speaker_id"] + "}}", 1)[-1]
                if "says in an off-screen voiceover" not in local_delivery:
                    fail("voiceover_phrase", "Use the exact off-screen voiceover phrase")
            if "continues_from" in utterance and not re.search(r"\bcontinu(?:es|ing|ation)\b", text, re.I):
                fail("speech_continuation", "The next shot must explicitly state continuation")
        if i == 0:
            details.append(labels["shots"][sid] + " " + ((style + " ") if mode != "Ref2VA" else "") + text)
        else:
            details.append(labels["shots"][sid] + " At " + timestamp(binding["shots"][i]["start_ms"]) + ", " + text)
    if covered != set(obligations):
        fail("obligation_coverage", "Uncovered obligation IDs: " + ", ".join(sorted(set(obligations) - covered)))
    if any(len(uses) != 1 for uses in utterance_usage.values()):
        fail("utterance_coverage", "Every utterance must occur exactly once in its declared shot")
    ordered_times = [utterances[uid]["start_ms"] for uid in utterance_order]
    if ordered_times != sorted(ordered_times):
        fail("utterance_order", "Dialogue placeholders must follow the actual vocal timeline")
    if inputs["complete_silence"] and (utterances or labels["speakers"] or declaration["audio_bindings"] or inputs["music_present"]):
        fail("silence_conflict", "Complete silence conflicts with vocal, audio or music declarations")
    sound = replace(fragments["overall_soundscape"], "/fragments/overall_soundscape")
    music = replace(fragments["non_diegetic_music"], "/fragments/non_diegetic_music")
    if (sound == "N/A") != inputs["complete_silence"]:
        fail("soundscape_na", "overall_soundscape is N/A if and only if the whole video is silent")
    if (music == "N/A") != (not inputs["music_present"]):
        fail("music_na", "non_diegetic_music is N/A if and only if there is no non-diegetic music")
    complete_audio = next((a["asset_id"] for a in declaration["audio_bindings"] if a["retention"] == "fully_copy"), None)
    if complete_audio is not None and any(u.get("origin", "generated") != "copied_audio" or u.get("audio_asset_id") != complete_audio for u in utterances.values()):
        fail("fully_copy_dialogue", "A complete copied soundtrack permits only dialogue copied from that same signal, not newly generated or re-performed speech")
    body = "\n\n".join(details)
    alignment = None
    if mode == "I2VA":
        alignment = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced."
    elif mode == "FL2VA":
        alignment = ("How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot "
                     + str(len(details)) + ") aligns with the " + seconds_centiseconds(binding["duration_ms"]) + "-second mark of the target video.")
    elif mode == "L2VA":
        alignment = ("How the reference pictures align with the target video — <Picture 1> (from [Shot " + str(len(details))
                     + "]) aligns with the " + seconds_centiseconds(binding["duration_ms"]) + "-second mark of the target video.")
    if mode != "Ref2VA":
        if "summary" in fragments:
            fail("base_summary", "Base modes have no summary field")
        fields = dict(zip(BASE_FIELDS, (body, sound, music)))
    else:
        if "summary" not in fragments:
            fail("ref_summary", "Ref2VA requires an approved English summary fragment")
        definitions, retention = [], []
        for subject in declaration["subjects"]:
            sid = subject["subject_id"]
            source_labels = [labels["assets"][aid]["image" if "image" in labels["assets"][aid] else "video"] for aid in subject["source_asset_ids"]]
            definitions.append(labels["subjects"][sid] + ": " + replace(subject["description"], "/subjects/description") + " Source: " + ", ".join(source_labels) + ".")
            retention.append(labels["subjects"][sid] + " (appears in " + ", ".join(labels["shots"][x] for x in subject["shot_ids"]) + "): " + subject["retention"] + " - " + replace(subject["retention_reason"], "/subjects/retention_reason", retention=True))
        for ref in declaration["reference_items"]:
            aid = ref["asset_id"]
            label = labels["assets"][aid]["image" if "image" in labels["assets"][aid] else "video"]
            definitions.append(label + ": " + replace(ref["description"], "/reference_items/description"))
            retention.append(label + " (" + ", ".join(labels["shots"][x] for x in ref["shot_ids"]) + "): " + ref["retention"] + " - " + replace(ref["retention_reason"], "/reference_items/retention_reason", retention=True))
        for audio in declaration["audio_bindings"]:
            label = labels["assets"][audio["asset_id"]]["audio"]
            description = replace(audio["description"], "/audio_bindings/description")
            if "speaker_id" in audio:
                description += " Voice of " + (labels["subjects"][audio["subject_id"]] + " " if "subject_id" in audio else "") + "(" + labels["speakers"][audio["speaker_id"]] + ")."
            definitions.append(label + ": " + description)
            retention.append(label + ": " + audio["retention"] + " - " + replace(audio["retention_reason"], "/audio_bindings/retention_reason", retention=True))
        summary = replace(fragments["summary"], "/fragments/summary")
        if "video editing" in binding["task_types"]:
            opening = "The target video is an edited version of <Video 1>."
            summary = opening + " " + summary
        summary = "[" + " + ".join(binding["task_types"]) + "] " + summary
        fields = dict(zip(REF_FIELDS, ("\n".join(definitions), summary, "\n".join(retention), style + "\n\n" + body, sound, music)))
    visible = inputs.get("visible_text", [])
    index(visible, "text_id", "/inputs/visible_text")
    visible_trace = []
    for item in visible:
        obj(item, ("text_id", "text", "shot_id"), (), "/inputs/visible_text")
        string(item["text"])
        if item["shot_id"] not in shot_fragments:
            fail("unknown_shot", "Visible text names an unknown shot")
        if '"' in item["text"] or "\n" in item["text"]:
            fail("visible_text_encoding", "This adapter accepts one-line visible text without embedded double quotes")
        if '"' + item["text"] + '"' not in shot_fragments[item["shot_id"]]["text"]:
            fail("visible_text_fidelity", "Visible text must appear verbatim inside double quotes in its shot")
        visible_trace.append(deepcopy(item))
    for name, field in fields.items():
        # This is a script-range guard, not an English-language or semantic classifier.
        outside = re.sub(r"<d>.*?</d>|\"(?:[^\"\\]|\\.)*\"", "", field, flags=re.S)
        if any(c.isalpha() and ord(c) > 127 and "LATIN" not in unicodedata.name(c, "") for c in outside):
            fail("non_english_script", "Use English outside verbatim dialogue and quoted visible text/lyrics", "/fields/" + name)
    rendered_prompt = ((alignment + "\n\n") if alignment else "") + "\n\n".join(name + ": " + content for name, content in fields.items())
    result = {"kind": "PromptCompilation", "contract_version": VERSION, "mode": mode,
              "profile_digest": binding["profile_digest"], "binding_digest": binding["binding_digest"],
              "duration_ms": binding["duration_ms"], "fields": fields, "field_order": list(fields),
              "alignment_instruction": alignment, "rendered_prompt": rendered_prompt,
              "media_inputs": deepcopy(binding["media_inputs"]), "obligation_trace": trace,
              "punctuation_trace": punctuation_trace, "visible_text_trace": visible_trace,
              "utterance_source_trace": utterance_source_trace,
              "declarations": deepcopy(inputs), "evidence_snapshot": evidence_snapshot(inputs, sources),
              "status": "passed_with_unverified", "not_run": list(NOT_RUN)}
    result["compilation_digest"] = digest(result)
    return result


def validate_compilation(compilation, sources):
    if not isinstance(compilation, dict) or not isinstance(compilation.get("declarations"), dict):
        fail("compilation_contract", "Supply a self-contained PromptCompilation including declarations")
    expected = compile_prompt(compilation["declarations"], sources)
    if not same(expected, compilation):
        fail("compilation_mismatch", "PromptCompilation differs from its recomputed declarations")
    return expected


def assign_path(result, path, value):
    parts = path_parts(path)
    cursor = result
    for part in parts[:-1]:
        cursor = cursor.setdefault(part, {})
    cursor[parts[-1]] = deepcopy(value)


def runtime_value(name, value, mapping):
    expected_type = mapping["type"]
    if name == "duration_ms":
        integer(value, "/inputs/parameters/duration_ms", 1)
        if mapping["unit"] == "seconds":
            if expected_type == "integer" and value % 1000:
                fail("duration_precision", "An integer-seconds runtime cannot represent this exact duration")
            value = value // 1000 if value % 1000 == 0 else value / 1000
    matches = {"integer": isinstance(value, int) and not isinstance(value, bool),
               "number": isinstance(value, (int, float)) and not isinstance(value, bool),
               "string": isinstance(value, str), "boolean": isinstance(value, bool)}
    if not matches[expected_type]:
        fail("parameter_type", "Wrong runtime type for " + name, "/inputs/parameters/" + name)
    if "enum" in mapping and value not in mapping["enum"]:
        fail("parameter_enum", "Unsupported documented value for " + name)
    for bound, predicate in (("minimum", lambda a, b: a < b), ("maximum", lambda a, b: a > b)):
        if bound in mapping and (not isinstance(value, (int, float)) or isinstance(value, bool) or predicate(value, mapping[bound])):
            fail("parameter_range", "Value violates documented " + bound + " for " + name)
    return value


def task_export(inputs, sources):
    obj(inputs, ("compilation", "capability_profile", "parameters", "asset_map"), (), "/inputs")
    profile = validate_profile(inputs["capability_profile"], sources)
    compilation = validate_compilation(inputs["compilation"], sources)
    if profile["profile_digest"] != compilation["profile_digest"]:
        fail("profile_mismatch", "Compile again with this exact backend/model/workflow profile")
    runtime = profile["runtime"]
    if runtime["status"] != "documented":
        fail("runtime_unknown", "No executable task export: actual runtime fields and capabilities are unknown", "/inputs/capability_profile/runtime", "caller")
    if compilation["mode"] not in runtime["supported_modes"]:
        fail("runtime_mode", "This runtime profile does not document the compiled mode")
    parameters = inputs["parameters"]
    obj(parameters, runtime["required_parameters"], set(runtime["parameters"]) - set(runtime["required_parameters"]), "/inputs/parameters")
    if parameters["duration_ms"] != compilation["duration_ms"]:
        fail("duration_mismatch", "Actual runtime duration must equal compiled prompt duration", "/inputs/parameters/duration_ms")
    if not isinstance(inputs["asset_map"], dict):
        fail("type", "asset_map must be an object")
    asset_ids = {m["asset_id"] for m in compilation["media_inputs"]}
    if set(inputs["asset_map"]) != asset_ids:
        fail("asset_mapping", "Runtime asset_map must exactly cover the serialized assets")
    if len(asset_ids) > runtime.get("limits", {}).get("max_assets", len(asset_ids)):
        fail("asset_limit", "Documented runtime asset limit exceeded")
    payload, mapping_trace = {}, []
    assign_path(payload, runtime["prompt"]["path"], compilation["rendered_prompt"])
    assign_path(payload, runtime["mode"]["path"], compilation["mode"])
    for name, value in parameters.items():
        mapping = runtime["parameters"][name]
        actual = runtime_value(name, value, mapping)
        assign_path(payload, mapping["path"], actual)
        mapping_trace.append({"canonical_parameter": name, "canonical_value": value, "runtime_path": mapping["path"], "runtime_value": actual, "evidence_refs": mapping["evidence_refs"]})
    runtime_media = []
    for media in compilation["media_inputs"]:
        mapped = inputs["asset_map"][media["asset_id"]]
        obj(mapped, ("version", "value"), (), "/inputs/asset_map/" + media["asset_id"])
        if mapped["version"] != media["asset_version"]:
            fail("asset_version", "Runtime asset version differs from the compiled asset version")
        if not isinstance(mapped["value"], str) or not mapped["value"].strip():
            fail("asset_value", "This adapter maps each runtime asset to an explicit locator string")
        runtime_media.append({"value": mapped["value"], "channel": media["channel"], "label": media["label"], "input_index": media["input_index"]})
    assign_path(payload, runtime["media"]["path"], runtime_media)
    execution = runtime["execution"]
    return {"kind": "TaskExport", "contract_version": VERSION, "profile_digest": profile["profile_digest"],
            "compilation_digest": compilation["compilation_digest"], "mode": compilation["mode"],
            "execution": execution, "status": "simulation_only" if execution == "simulation" else "exported_unexecuted",
            "payload": payload, "parameter_mapping_trace": mapping_trace,
            "media_binding_trace": deepcopy(compilation["media_inputs"]), "declarations": deepcopy(inputs),
            "evidence_snapshot": evidence_snapshot(inputs, sources),
            "not_run": list(NOT_RUN), "limitations": list(LIMITATIONS)}


BUILDERS = {"M11.1": capability, "M11.2": reference_binding, "M11.3": compile_prompt, "M11.4": task_export}


def propose(request):
    validate_request(request)
    module = request["target"]
    changes = {PARTS[module]: BUILDERS[module](request["inputs"], request["sources"])}
    return {"kind": "M11Proposal", "contract_version": VERSION, "route_version": VERSION,
            "work_id": request["work_id"], "base_version": request["base_version"],
            "proposal_id": "p-" + digest(request), "module_id": module, "source_request_id": request["request_id"],
            "sources": deepcopy(request["sources"]), "context": deepcopy(request["inputs"]), "changes": changes,
            "issues": [], "status": "passed_with_unverified", "execution_status": "completed",
            "not_run": list(NOT_RUN), "limitations": list(LIMITATIONS)}


def check(proposal, request):
    expected = propose(request)
    canonical(proposal)
    if not same(proposal, expected):
        fail("proposal_mismatch", "Proposal must exactly match deterministic recompilation of the original request", "", "caller")
    return {"status": "passed_with_unverified", "valid": True, "module_id": request["target"],
            "proposal_id": proposal["proposal_id"], "execution_status": "completed", "not_run": list(NOT_RUN), "limitations": list(LIMITATIONS)}


def route(request):
    validate_request(request)
    input_keys = {"M11.1": (("profile",), ()),
                  "M11.2": (("capability_profile", "plan", "assets", "subjects", "reference_items", "audio_bindings", "speakers"), ()),
                  "M11.3": (("binding", "fragments", "obligations", "utterances", "complete_silence", "music_present"), ("visible_text",)),
                  "M11.4": (("compilation", "capability_profile", "parameters", "asset_map"), ())}
    required, optional = input_keys[request["target"]]
    obj(request["inputs"], required, optional, "/inputs")
    evidence_refs(sorted(source_ids(request["inputs"])), request["sources"], "/inputs", minimum=0)
    # Definition/shape routing is intentionally separate from invoking a child compiler.
    return {"status": "ready", "invocation_status": "not_invoked", "route_version": VERSION,
            "invocations": [{"invocation_id": "i-" + digest(request), "target": request["target"],
                             "contract_version": VERSION, "route_version": VERSION,
                             "input_refs": sorted(source_ids(request["inputs"])),
                             "resources": ["scripts/m11_contract.py", "references/contracts.json"],
                             "status": "not_invoked", "output": None, "error": None}],
            "not_run": list(NOT_RUN) + ["child_invocation"]}


def empty_state(work_id):
    return {"kind": "M11State", "contract_version": VERSION, "work_id": work_id, "version": 0,
            "owner": "M11", "object_type": "CompilationResult", "status": "draft", "content": {},
            "contexts": {}, "sources": {}, "receipts": [], "consumers": [], "stale_modules": []}


def state_staleness(state):
    stale = set()
    for part, request in state["contexts"].items():
        for sid in source_ids(request["inputs"]):
            if state["sources"].get(sid) != request["sources"].get(sid):
                stale.add(request["target"])
    content = state["content"]
    profile = content.get("capability_profile")
    binding = content.get("reference_binding")
    compilation = content.get("prompt_compilation")
    exported = content.get("task_export")
    if profile:
        for module, child in (("M11.2", binding), ("M11.3", compilation), ("M11.4", exported)):
            if child and child["profile_digest"] != profile["profile_digest"]:
                stale.add(module)
    if binding and compilation and compilation["binding_digest"] != binding["binding_digest"]:
        stale.add("M11.3")
    if compilation and exported and exported["compilation_digest"] != compilation["compilation_digest"]:
        stale.add("M11.4")
    # A dependent result cannot stay current merely because its stale predecessor's
    # obsolete fingerprint still agrees with the dependent result.
    if "M11.2" in stale and compilation and binding and compilation["binding_digest"] == binding["binding_digest"]:
        stale.add("M11.3")
    if "M11.3" in stale and exported and compilation and exported["compilation_digest"] == compilation["compilation_digest"]:
        stale.add("M11.4")
    return sorted(stale)


def validate_state(state):
    obj(state, ("kind", "contract_version", "work_id", "version", "content", "contexts", "sources", "receipts", "consumers", "stale_modules"),
        ("owner", "object_type", "status"), "/state")
    if state["kind"] != "M11State" or state["contract_version"] != VERSION or state.get("owner", "M11") != "M11" or state.get("object_type", "CompilationResult") != "CompilationResult":
        fail("state_contract", "Invalid M11 state identity/version")
    identifier(state["work_id"]); integer(state["version"])
    if not isinstance(state["content"], dict) or not set(state["content"]) <= set(PARTS.values()):
        fail("state_partition", "State has an unowned partition")
    for key in ("contexts", "sources"):
        if not isinstance(state[key], dict):
            fail("state_type", key + " must be an object")
    if set(state["contexts"]) != set(state["content"]):
        fail("state_contexts", "Every accepted partition needs its original request")
    if state["sources"]:
        validate_sources(state["sources"])
    array(state["receipts"]); unique_strings(state["consumers"]); unique_strings(state["stale_modules"])
    for module in state["stale_modules"]:
        choice(module, PARTS)
    for part, request in state["contexts"].items():
        validate_request(request)
        if PARTS[request["target"]] != part or request["work_id"] != state["work_id"]:
            fail("state_context", "State context does not own its partition")
        actual = propose(request)["changes"][part]
        if not same(actual, state["content"][part]):
            fail("state_content", "Accepted state content differs from its original request")
    seen, request_ids, expected_contexts, expected_sources = set(), set(), {}, {}
    receipt_versions = []
    for receipt in state["receipts"]:
        obj(receipt, ("proposal_id", "request_digest", "proposal_digest", "accepted_version", "request", "proposal"), (), "/state/receipts")
        if receipt["proposal_id"] in seen:
            fail("receipt_duplicate", "Duplicate receipt proposal ID")
        seen.add(receipt["proposal_id"])
        integer(receipt["accepted_version"], minimum=1)
        if receipt["accepted_version"] > state["version"]:
            fail("receipt_version", "Receipt version is newer than state")
        check(receipt["proposal"], receipt["request"])
        if receipt["proposal_id"] != receipt["proposal"]["proposal_id"] or receipt["request_digest"] != digest(receipt["request"]) or receipt["proposal_digest"] != digest(receipt["proposal"]):
            fail("receipt_digest", "Receipt does not match its original immutable inputs")
        request = receipt["request"]
        if request["request_id"] in request_ids:
            fail("request_id_reuse", "Each accepted revision requires a new request_id")
        request_ids.add(request["request_id"])
        if request["work_id"] != state["work_id"] or request["base_version"] != receipt["accepted_version"] - 1:
            fail("receipt_context", "Receipt work/base version does not match the accepted transaction")
        receipt_versions.append(receipt["accepted_version"])
        part = PARTS[request["target"]]
        expected_contexts[part] = request
        for sid, source in request["sources"].items():
            if sid in expected_sources and source != expected_sources[sid] and source["version"] == expected_sources[sid]["version"]:
                fail("source_version_reuse", "Receipt history changes a source without changing its version")
            expected_sources[sid] = source
    if state["version"] == 0 and (state["content"] or state["receipts"] or state["sources"]):
        fail("state_version", "Version zero must be empty")
    if receipt_versions != sorted(receipt_versions) or set(receipt_versions) != set(range(1, state["version"] + 1)):
        fail("receipt_history", "Receipt history must cover every state version in order")
    if not same(state["contexts"], expected_contexts) or not same(state["sources"], expected_sources):
        fail("state_provenance", "State contexts and sources must match the last immutable receipts")
    if state["stale_modules"] != state_staleness(state):
        fail("state_staleness", "Stale module flags must reflect actual source and prerequisite dependencies")
    expected_status = "draft" if state["version"] == 0 else ("partial" if len(state["content"]) < 4 else "compiled_unexecuted")
    if state.get("status", expected_status) != expected_status or state["consumers"] != []:
        fail("state_status", "State status is derived; external consumer activation is not supported by this local adapter")


def accept(proposals, requests, state):
    proposals = proposals if isinstance(proposals, list) else [proposals]
    requests = requests if isinstance(requests, list) else [requests]
    array(proposals, minimum=1); array(requests, minimum=1)
    validate_state(state)
    request_map = index(requests, "request_id", "/requests")
    if len(requests) != len(proposals):
        fail("batch_pairing", "Every proposal needs exactly one original request")
    seen_parts, seen_ids, checked, old = set(), set(), [], []
    receipts = {r["proposal_id"]: r for r in state["receipts"]}
    prior_request_ids = {r["request"]["request_id"] for r in state["receipts"]}
    for proposal in proposals:
        if not isinstance(proposal, dict) or proposal.get("source_request_id") not in request_map:
            fail("original_request_missing", "Cannot accept without the original source request")
        request = request_map[proposal["source_request_id"]]
        check(proposal, request)
        if proposal["work_id"] != state["work_id"]:
            fail("work_id", "Proposal belongs to another work")
        part = PARTS[proposal["module_id"]]
        if part in seen_parts or proposal["proposal_id"] in seen_ids:
            fail("batch_duplicate", "An atomic batch may contain each module exactly once")
        seen_parts.add(part); seen_ids.add(proposal["proposal_id"])
        if proposal["proposal_id"] in receipts:
            receipt = receipts[proposal["proposal_id"]]
            if receipt["request_digest"] != digest(request) or receipt["proposal_digest"] != digest(proposal):
                fail("replay_mutation", "Receipt replay must match original request and proposal exactly")
            old.append(proposal)
        else:
            if request["request_id"] in prior_request_ids:
                fail("request_id_reuse", "A new accepted revision requires a new request_id")
            if proposal["base_version"] != state["version"]:
                fail("stale_base_version", "Proposal base_version must equal current state version")
            checked.append((proposal, request))
    if old and checked:
        fail("mixed_replay", "Do not mix idempotent replay with new changes")
    if old:
        return {"status": "passed_with_unverified", "state": deepcopy(state), "idempotent": True, "execution_status": "completed", "not_run": list(NOT_RUN), "limitations": list(LIMITATIONS)}
    updated = deepcopy(state)
    changed_sources = set()
    batch_sources = {}
    for proposal, request in checked:
        for sid, source in request["sources"].items():
            if sid in batch_sources and batch_sources[sid] != source:
                fail("batch_source_conflict", "Atomic batch uses conflicting source records: " + sid)
            batch_sources[sid] = source
            if sid in state["sources"] and source != state["sources"][sid]:
                if source["version"] == state["sources"][sid]["version"]:
                    fail("source_version_reuse", "Changed source content requires a changed source version: " + sid)
                changed_sources.add(sid)
    updated["sources"].update(deepcopy(batch_sources))
    changed_parts = set()
    for proposal, request in checked:
        part = PARTS[proposal["module_id"]]
        if state["content"].get(part) != proposal["changes"][part]:
            changed_parts.add(part)
        updated["content"][part] = deepcopy(proposal["changes"][part])
        updated["contexts"][part] = deepcopy(request)
    stale = set(state_staleness(updated))
    if any(proposal["module_id"] in stale for proposal, _ in checked):
        fail("batch_dependency_conflict", "Accepted proposals contain incompatible capability, binding or compilation versions")
    updated.update({"owner": "M11", "object_type": "CompilationResult", "version": state["version"] + 1,
                    "status": "partial" if len(updated["content"]) < 4 else "compiled_unexecuted",
                    "stale_modules": sorted(stale)})
    for proposal, request in checked:
        updated["receipts"].append({"proposal_id": proposal["proposal_id"], "request_digest": digest(request),
                                    "proposal_digest": digest(proposal), "accepted_version": updated["version"],
                                    "request": deepcopy(request), "proposal": deepcopy(proposal)})
    return {"status": "passed_with_unverified", "state": updated, "idempotent": False, "execution_status": "completed", "not_run": list(NOT_RUN), "limitations": list(LIMITATIONS)}


def impact(before, after):
    changes = []
    def walk(a, b, path):
        if type(a) is not type(b):
            changes.append(path or "/"); return
        if isinstance(a, dict):
            for key in sorted(set(a) | set(b)):
                child = path + "/" + key.replace("~", "~0").replace("/", "~1")
                if key not in a or key not in b:
                    changes.append(child)
                else:
                    walk(a[key], b[key], child)
        elif isinstance(a, list):
            if a != b:
                changes.append(path or "/")
        elif a != b:
            changes.append(path or "/")
    canonical(before); canonical(after)
    walk(before, after, "")
    return {"status": "completed", "changed_paths": changes, "changed": bool(changes),
            "review_required": bool(changes), "not_run": ["semantic_change_classification", "child_invocation"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("route", "propose"):
        p = sub.add_parser(command); p.add_argument("request")
    p = sub.add_parser("check"); p.add_argument("proposal"); p.add_argument("--request", required=True)
    p = sub.add_parser("accept"); p.add_argument("proposals"); p.add_argument("--requests", required=True); p.add_argument("--state", required=True)
    p = sub.add_parser("impact"); p.add_argument("before"); p.add_argument("after")
    try:
        args = parser.parse_args(argv)
        if args.command in {"route", "propose"}:
            result = globals()[args.command](load(args.request))
        elif args.command == "check":
            result = check(load(args.proposal), load(args.request))
        elif args.command == "accept":
            result = accept(load(args.proposals), load(args.requests), load(args.state))
        else:
            result = impact(load(args.before), load(args.after))
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except ContractError as exc:
        print(json.dumps({"status": "fail", "execution_status": "failed", "errors": [exc.as_dict()], "not_run": list(NOT_RUN)}, ensure_ascii=False, indent=2))
        return 2
    except (KeyError, TypeError, ValueError, OverflowError, RecursionError) as exc:
        print(json.dumps({"status": "fail", "execution_status": "failed", "errors": [{"code": "malformed_input", "detail": str(exc), "owner": "caller", "path": ""}], "not_run": list(NOT_RUN)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
