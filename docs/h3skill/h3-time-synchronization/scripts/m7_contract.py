#!/usr/bin/env python3
"""Portable M7 TimingMap contract checker and exact time math.

Python 3.10+, standard library, no network. Three independent child scopes.
Never changes action/dialogue/camera/edit intent or certifies generated media.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import bisect
from fractions import Fraction
from pathlib import Path
import re
import sys
import uuid
from datetime import datetime, timezone

VERSION = "1.0.0"
PACKAGE_VERSION = "0.1.0"
ROOT = Path(__file__).resolve().parents[1]
OWNED = {"M7.1": "timebase", "M7.2": "schedule", "M7.3": "mappings"}
CONTEXTS = {"timebase_context": "timebase", "schedule_context": "schedule", "mapping_context": "mappings"}
MINIMUM = {"M7": ("timing_brief",), "M7.1": ("timebase_brief",),
           "M7.2": ("schedule_brief", "timebase_context"),
           "M7.3": ("mapping_brief", "timebase_context")}
EMPTY = {part: {"items": {}} for part in OWNED.values()}
UNVERIFIED = ["semantic_intent", "source_authenticity", "measurement_authenticity",
              "actual_lip_sync", "generated_video_quality", "global_G0_G4"]


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


def rational(value, label="value"):
    """Exact decimal/rational parsing; bool, NaN and infinities are never numbers."""
    if isinstance(value, dict) and value.get("state") == "unknown":
        return None
    if isinstance(value, Fraction):
        return value
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError(label + " must be a finite rational, not a boolean")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(label + " must be finite")
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError(label + " must be a finite rational with nonzero denominator") from exc


def exact(value):
    return str(value.numerator) if value.denominator == 1 else str(value.numerator) + "/" + str(value.denominator)


def positive(value, label):
    result = rational(value, label)
    if result is None:
        raise MissingBasis(label + " is unknown")
    if result <= 0:
        raise ValueError(label + " must be positive")
    return result


class MissingBasis(ValueError):
    """A valid unknown has no exact numeric conclusion."""


def convert_value(value, from_unit, to_unit, fps=None, bpm=None, origin=None):
    aliases = {"seconds": "s", "milliseconds": "ms", "frame": "frames", "beat": "beats"}
    from_unit, to_unit = aliases.get(from_unit, from_unit), aliases.get(to_unit, to_unit)
    if from_unit not in ("s", "ms", "frames", "beats") or to_unit not in ("s", "ms", "frames", "beats"):
        raise ValueError("Units must be s, ms, frames or beats")
    value = rational(value)
    if value is None:
        raise MissingBasis("Input value is unknown")
    f = positive(fps, "FPS") if "frames" in (from_unit, to_unit) and fps is not None else None
    b = positive(bpm, "BPM") if "beats" in (from_unit, to_unit) and bpm is not None else None
    o = rational(origin, "beat origin") if origin is not None else None
    if "frames" in (from_unit, to_unit) and f is None:
        raise MissingBasis("Frame conversion needs known CFR FPS")
    if "beats" in (from_unit, to_unit) and (b is None or o is None):
        raise MissingBasis("Absolute beat conversion needs BPM and an explicit first-beat origin; none is inferred")
    seconds = {"s": lambda: value, "ms": lambda: value / 1000,
               "frames": lambda: value / f, "beats": lambda: o + value * 60 / b}[from_unit]()
    return {"s": lambda: seconds, "ms": lambda: seconds * 1000,
            "frames": lambda: seconds * f, "beats": lambda: (seconds - o) * b / 60}[to_unit]()


def quantize_value(value, fps, rule, origin=0, pts=None):
    """CFR frame zero is at origin; nearest ties select the later frame."""
    t, o = rational(value, "time"), rational(origin, "clock origin")
    if t is None or o is None:
        raise MissingBasis("Quantization needs known time and clock origin")
    if rule not in ("floor", "ceil", "nearest"):
        raise ValueError("Unknown rounding rule")
    if pts is not None:
        points = [rational(x, "PTS") for x in pts]
        if not points or any(x is None for x in points) or any(a >= b for a, b in zip(points, points[1:])):
            raise ValueError("PTS must be a nonempty strictly increasing array")
        if t < points[0] or t > points[-1]:
            raise ValueError("Time is outside known PTS sample range; no extrapolation")
        upper = bisect.bisect_left(points, t)
        if points[upper] == t:
            n = upper
        elif rule == "floor":
            n = upper - 1
        elif rule == "ceil":
            n = upper
        else:
            n = upper if points[upper] - t <= t - points[upper - 1] else upper - 1
        tq = points[n]
    else:
        f = positive(fps, "FPS")
        x = (t - o) * f
        if x < 0:
            raise ValueError("Frame sample time precedes frame zero")
        n = x.numerator // x.denominator
        if rule == "ceil" and x.denominator != 1:
            n += 1
        elif rule == "nearest" and x - n >= Fraction(1, 2):
            n += 1
        tq = o + Fraction(n, 1) / f
    return n, tq, tq - t


def map_value(value, source_start, destination_start, speed):
    v = positive(speed, "speed")
    t, s, d = rational(value), rational(source_start), rational(destination_start)
    if any(x is None for x in (t, s, d)):
        raise MissingBasis("Mapping requires known time and endpoints")
    return d + (t - s) / v


def event_key(reference):
    return tuple(reference[k] for k in ("owner", "kind", "id", "domain", "domain_id"))


class Check:
    def __init__(self, definitions):
        self.defs = definitions
        self.diagnostics = []
        self.precision_evaluated = False

    def add(self, code, path, message, owner="M7", status="fail"):
        self.diagnostics.append({"code": code, "path": path, "message": message,
                                 "status": status, "blocking": status == "fail", "repair_target": owner})

    @property
    def failed(self):
        return any(x["blocking"] for x in self.diagnostics)

    def shape(self, artifact, expected=None, path=""):
        kind = artifact.get("kind") if isinstance(artifact, dict) else None
        if kind not in ("M7Request", "M7Proposal", "M7ProposalBatch", "M7State") or (expected and kind != expected):
            self.add("artifact_kind", path, "Unexpected artifact kind; expected " + str(expected))
            return False
        errors = shape_errors(artifact, self.defs[kind], self.defs, path)
        for where, message in errors:
            self.add("contract_shape", where, message)
        return not errors

    def refs(self, value, sources, path="", owner="M7"):
        if isinstance(value, dict):
            if value.get("state") == "unknown":
                self.add("explicit_unknown", path, value["reason"], owner, "unverified")
            for key, item in value.items():
                if ((key == "values" and "source_id" in value)
                        or (key == "value" and (value.get("state") == "known" or ("path" in value and "source_version" in value)))):
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

    def partition_context(self, context, part, path=""):
        if not isinstance(context,dict):
            return None
        if "items" in context:
            return context
        if "source_id" in context and isinstance(context.get("values"),dict) and "items" in context["values"]:
            value=context["values"]
            name={"timebase":"Timebase", "schedule":"Schedule", "mappings":"Mappings"}[part]
            errors=shape_errors(value,self.defs[name],self.defs,path+"/values")
            for where,message in errors:
                self.add("external_partition_shape",where,message)
            return None if errors else value
        return None

    def request(self, request, path=""):
        if not self.shape(request, "M7Request", path):
            return False
        target, inputs = request["target"], request["inputs"]
        for key in MINIMUM[target]:
            if key not in inputs:
                self.add("minimum_input_missing", ptr(ptr(path, "inputs"), key), "Supply this input or an explicit unknown with a reason", target)
        self.refs(inputs, request["sources"], ptr(path, "inputs"), target)
        owners = {"task_context":"M1", "reference_context":"M2", "action_context":"M4", "camera_context":"M5", "sound_context":"M6", "state_context":"M8", "edit_context":"M9", "label_context":"M11", "timebase_context":"M7.1", "schedule_context":"M7.2", "mapping_context":"M7.3"}
        for field, owner in owners.items():
            context = inputs.get(field, {})
            if "owner" in context and context["owner"] not in (owner, "external"):
                self.add("context_owner", ptr(ptr(path, "inputs"), field), "Expected readonly " + owner + " context", target)
        for i, projection in enumerate(inputs.get("readonly_projection", [])):
            if projection["source_version"] != request["base_version"]:
                self.add("projection_version", ptr(ptr(ptr(path, "inputs"), "readonly_projection"), i), "Readonly projection must identify request base version", target)
        # Public local context is real typed input, not a bypass around semantic validation.
        content, known = copy.deepcopy(EMPTY), set()
        for field, part in CONTEXTS.items():
            context = self.partition_context(inputs.get(field),part,path+"/inputs/"+field)
            if context is not None:
                self.refs(context,request["sources"],path+"/inputs/"+field,target)
                content[part] = context
                known.add(part)
        self.content(content, known, path + "/inputs")
        self.domain_evidence(content, request["sources"], inputs, path + "/inputs")
        return not self.failed

    def proposal(self, proposal, request=None, path=""):
        if not self.shape(proposal, "M7Proposal", path):
            return False
        owner = proposal["module_id"]
        partition = OWNED[owner]
        if set(proposal["changes"]) != {partition}:
            self.add("write_ownership", ptr(path, "changes"), "Child may replace only " + partition, owner)
        for field in ("context", "changes", "issues", "resolutions"):
            self.refs(proposal[field], proposal["sources"], ptr(path, field), owner)
        for key in MINIMUM[owner]:
            if key not in proposal["context"]:
                self.add("minimum_input_missing", ptr(ptr(path, "context"), key), "Required input absent", owner)
        if request is None:
            self.add("original_request_missing", path, "Source fidelity requires the actual request", owner, "unverified")
            self.request({"kind":"M7Request", "contract_version":VERSION, "request_id":proposal["source_request_id"], "target":owner, "work_id":proposal["work_id"], "base_version":proposal["base_version"], "sources":proposal["sources"], "inputs":proposal["context"]}, path + "/declared_context")
        elif self.shape(request, "M7Request", "/request"):
            self.request(request, "/request")
            for field in ("work_id", "base_version", "sources"):
                if not same(proposal[field], request[field]):
                    self.add("request_fidelity", ptr(path, field), "Proposal differs from original request", owner)
            if proposal["source_request_id"] != request["request_id"]:
                self.add("request_binding", ptr(path, "source_request_id"), "Wrong original request", owner)
            if request["target"] != owner:
                self.add("request_target", ptr(path, "module_id"), "Child requires a request addressed to that child", owner)
            if not same(proposal["context"], request["inputs"]):
                self.add("request_fidelity", ptr(path, "context"), "Readonly inputs were changed or omitted", owner)
        for issue in proposal["issues"]:
            if issue["owner"] != owner or issue["status"] != "open" or "resolution" in issue:
                self.add("issue_ownership", ptr(path, "issues"), "New issues must be open and owned by this child", owner)
        for field in ("issues", "resolutions"):
            if len({x["issue_id"] for x in proposal[field]}) != len(proposal[field]):
                self.add("duplicate_" + field, ptr(path, field), "Issue IDs must be unique", owner)
        content, known = copy.deepcopy(EMPTY), set(proposal["changes"])
        content.update(proposal["changes"])
        for field, part in CONTEXTS.items():
            context = self.partition_context(proposal["context"].get(field),part,path+"/context/"+field)
            if context is not None:
                if part in known and not same(content[part], context):
                    self.add("readonly_conflict", ptr(ptr(path, "context"), field), "Proposed partition conflicts with readonly context", owner)
                else:
                    content[part] = context
                    known.add(part)
        self.content(content, known, ptr(path, "changes"))
        own_content = copy.deepcopy(EMPTY)
        own_content.update(proposal["changes"])
        self.domain_evidence(own_content, proposal["sources"], proposal["context"], ptr(path, "changes"))
        return not self.failed

    def number(self, value, path, owner):
        try:
            return rational(value, path)
        except ValueError as exc:
            self.add("invalid_rational", path, str(exc), owner)
            return None

    def clock(self, ident, clocks, known, path, owner):
        if ident in clocks:
            return clocks[ident]
        if "timebase" in known:
            self.add("dangling_clock", path, ident + " is absent from timebase", owner)
        else:
            self.add("clock_context_unknown", path, ident + " cannot be checked without timebase context", owner, "unverified")
        return None

    def bounds(self, start, end, clock, path, owner):
        if clock is None:
            return
        origin = self.number(clock["origin"], path + "/clock/origin", owner)
        extent = self.number(clock["extent"], path + "/clock/extent", owner)
        if origin is not None:
            if start is not None and start < origin:
                self.add("clock_range", path, "Start precedes clock origin", owner)
            if end is not None and extent is not None and end > origin + extent:
                self.add("clock_range", path, "End exceeds clock coverage boundary", owner)

    def content(self, content, known, path="/content"):
        clocks = {k:v for k,v in content["timebase"]["items"].items() if v["record_type"] == "clock"}
        identifiers = {"clock":"clock_id", "beat_grid":"grid_id", "event":"timing_id", "constraint":"constraint_id", "mapping":"mapping_id", "quantization":"quantization_id"}
        owners = {part:module for module,part in OWNED.items()}
        for part in sorted(known):
            owner = owners[part]
            for ident, record in content[part]["items"].items():
                where = path + "/" + part + "/items/" + esc(ident)
                if record[identifiers[record["record_type"]]] != ident:
                    self.add("record_identity", where, "Map key differs from stable record ID", owner)
        for ident, record in content["timebase"]["items"].items():
            where, owner = path + "/timebase/items/" + esc(ident), "M7.1"
            if record["record_type"] == "clock":
                fps = self.number(record["fps"], where + "/fps", owner)
                origin = self.number(record["origin"], where + "/origin", owner)
                extent = self.number(record["extent"], where + "/extent", owner)
                if fps is not None and fps <= 0:
                    self.add("fps_positive", where + "/fps", "FPS must be positive", owner)
                if extent is not None and extent <= 0:
                    self.add("clock_extent", where + "/extent", "Clock extent must be positive", owner)
                if "frame_count" in record:
                    count=self.number(record["frame_count"],where+"/frame_count",owner)
                    if count is None:
                        self.add("frame_count_unknown",where,"Sample count is unknown",owner,"unverified")
                    elif record["rate_mode"] == "cfr":
                        if fps is not None and fps>0 and extent is not None:
                            if extent != count/fps:
                                self.add("frame_count_duration",where,"CFR coverage extent must equal frame_count/fps; last sample is origin+(N-1)/fps",owner)
                        else:
                            self.add("frame_count_unverified",where,"CFR count consistency needs known positive FPS and extent",owner,"unverified")
                    elif record["rate_mode"] == "vfr" and "pts" in record and count != len(record["pts"]):
                        self.add("frame_count_pts",where,"VFR frame_count must match the supplied PTS sample count",owner)
                if record["rate_mode"] == "cfr" and fps is None:
                    self.add("fps_unknown", where, "CFR precision cannot be established without FPS", owner, "unverified")
                if record["rate_mode"] == "unknown":
                    self.add("rate_mode_unknown", where, "Unknown sampling mode cannot support exact frame conversion", owner, "unverified")
                pts = [self.number(x, where + "/pts", owner) for x in record.get("pts", [])]
                if pts and all(x is not None for x in pts):
                    if any(a >= b for a,b in zip(pts,pts[1:])):
                        self.add("pts_order", where + "/pts", "PTS must be strictly increasing", owner)
                    if record["rate_mode"] != "vfr":
                        self.add("pts_mode", where + "/pts", "PTS is the VFR sample contract; CFR uses its exact FPS", owner)
                    if origin is not None and pts[0] < origin:
                        self.add("pts_range", where + "/pts", "PTS precedes clock origin", owner)
                    if origin is not None and extent is not None and pts[-1] >= origin + extent:
                        self.add("pts_range", where + "/pts", "A PTS sample must lie inside half-open coverage", owner)
                elif record["rate_mode"] == "vfr":
                    self.add("vfr_pts_unknown", where, "VFR average FPS does not supply sample locations", owner, "unverified")
            else:
                self.clock(record["clock_id"], clocks, known, where + "/clock_id", owner)
                bpm = self.number(record["bpm"], where + "/bpm", owner)
                self.number(record["first_beat"], where + "/first_beat", owner)
                if bpm is not None and bpm <= 0:
                    self.add("bpm_positive", where + "/bpm", "BPM must be positive", owner)
                self.add("beat_grid_candidate", where, "BPM gives a conditional grid; it does not establish measured beat timing", owner, "unverified")
        events = {}
        for ident, record in content["schedule"]["items"].items():
            if record["record_type"] != "event":
                continue
            where, owner = path + "/schedule/items/" + esc(ident), "M7.2"
            key = event_key(record["event_ref"])
            if key in events:
                self.add("duplicate_event_binding", where, "The same typed event in one domain has multiple timing records", owner)
            events[key] = record
            expected = {"action":"M4", "camera":"M5", "vocal":"M6", "music":"M6", "sound":"M6", "state":"M8", "cut":"M9"}.get(record["event_ref"]["kind"])
            if expected and record["event_ref"]["owner"] not in (expected, "external"):
                self.add("event_owner", where + "/event_ref", "Event kind belongs to " + expected, owner)
            clock = self.clock(record["clock_id"], clocks, known, where + "/clock_id", owner)
            if clock and any(record["event_ref"][k] != clock[k] for k in ("domain", "domain_id")):
                self.add("event_domain", where, "Typed event domain must match its clock", owner)
            start, end = [self.number(record[k], where + "/" + k, owner) for k in ("start", "end")]
            if start is not None and end is not None:
                if (record["extent_kind"] == "interval" and end <= start) or (record["extent_kind"] == "instant" and end != start):
                    self.add("event_interval", where, "Intervals require start < end; instants require start == end", owner)
            self.bounds(start, end, clock, where, owner)
        for ident, record in content["schedule"]["items"].items():
            if record["record_type"] != "constraint":
                continue
            self.constraint(record, events, path + "/schedule/items/" + esc(ident))
        for ident, record in content["mappings"]["items"].items():
            where = path + "/mappings/items/" + esc(ident)
            if record["record_type"] == "mapping":
                self.mapping(record, clocks, known, where)
            else:
                self.quantization(record, clocks, known, where)

    def constraint(self, record, events, path):
        owner, relation = "M7.2", record["relation"]
        refs = record["event_refs"]
        if len({event_key(x) for x in refs}) != len(refs):
            self.add("constraint_duplicate_event", path, "Constraint references must be distinct typed events", owner)
        if relation not in ("capacity", "duration_budget") and len(refs) != 2:
            self.add("constraint_arity", path, "Binary timing relation requires exactly two events", owner)
            return
        selected = [events.get(event_key(x)) for x in refs]
        if any(x is None for x in selected):
            self.add("dangling_event", path + "/event_refs", "Constraint references an absent typed event", owner)
            return
        if len({x["clock_id"] for x in selected}) != 1:
            self.add("constraint_clock", path, "Compare events on the same clock; map domains first", owner)
            return
        values = [[self.number(x[k], path + "/" + k, owner) for k in ("start", "end")] for x in selected]
        offset, tolerance = [self.number(record[k], path + "/" + k, owner) for k in ("offset", "tolerance")]
        if tolerance is not None and tolerance < 0:
            self.add("negative_tolerance", path, "Tolerance cannot be negative", owner)
            return
        if any(t is None for pair in values for t in pair) or offset is None or tolerance is None:
            self.add("constraint_unverified", path, "Unknown event timing or tolerance prevents a numeric verdict", owner, "unverified")
            return
        if relation == "duration_budget":
            window = record.get("window")
            if not window:
                self.add("duration_window_missing", path, "Sequential duration budget requires a declared window", owner)
                return
            if window["clock_id"] != selected[0]["clock_id"]:
                self.add("duration_window_clock", path, "Budget window and events need one clock", owner)
                return
            ws,we = [self.number(window[k], path + "/window/" + k, owner) for k in ("start", "end")]
            if ws is None or we is None:
                self.add("duration_budget_unverified", path, "Available duration is unknown", owner, "unverified")
                return
            if we <= ws:
                self.add("duration_window", path, "Budget window must have positive duration", owner)
                return
            required=[]
            for event in selected:
                raw = event.get("binding",{}).get("value",{})
                req = raw.get("timing_requirements",{}) if isinstance(raw,dict) else {}
                duration = req.get("required_duration", req.get("minimum_duration"))
                if duration is None:
                    self.add("duration_budget_unverified", path, "Each budgeted event needs explicit readonly required_duration or minimum_duration", owner, "unverified")
                else:
                    value=self.number(duration,path+"/duration_requirements",owner)
                    if value is None:
                        self.add("duration_budget_unverified",path,"Minimum required duration is unknown",owner,"unverified")
                    else: required.append(value)
            if len(required)==len(selected) and sum(required,Fraction(0)) > we-ws:
                self.add("duration_budget_exceeded",path,"Sum of readonly required durations exceeds available sequential window",owner)
            if sum((e-s for s,e in values),Fraction(0)) > we-ws:
                self.add("duration_budget_exceeded",path,"Scheduled total duration exceeds declared sequential window",owner)
            if any(s < ws or e > we for s,e in values):
                self.add("duration_window_range",path,"Scheduled event lies outside budget window",owner)
            if offset != 0 or tolerance != 0:
                self.add("duration_budget_parameters",path,"Duration budget uses exact duration; offset/tolerance must be zero",owner)
            return
        if relation == "capacity":
            if "capacity" not in record:
                self.add("capacity_missing", path, "Capacity relation requires a positive integer capacity", owner)
                return
            edges = sorted([(s,1) for s,e in values if e>s] + [(e,-1) for s,e in values if e>s])
            active = 0
            for _,delta in edges: # end (-1) precedes start (+1) at the same half-open boundary
                active += delta
                if active > record["capacity"]:
                    self.add("capacity_exceeded", path, "Concurrent interval count exceeds declared capacity", owner)
                    break
            if offset != 0 or tolerance != 0:
                self.add("capacity_parameters", path, "Capacity uses exact half-open occupancy; offset/tolerance must be zero", owner)
            return
        a,b=values
        if relation == "before":
            if offset < 0:
                self.add("before_gap",path,"Before minimum gap cannot be negative; use a signed offset relation",owner)
            ok = a[1] + offset <= b[0] + tolerance
        elif relation == "meets":
            ok = abs((b[0] - a[1]) - offset) <= tolerance
        elif relation == "overlap":
            duration = min(a[1],b[1])-max(a[0],b[0])
            ok = duration > 0 and duration + tolerance >= offset
            if offset < 0:
                self.add("overlap_duration", path, "Minimum overlap cannot be negative", owner)
        else:
            ai,bi = (0 if record["left_edge"] == "start" else 1), (0 if record["right_edge"] == "start" else 1)
            ok = abs((b[bi] - a[ai]) - offset) <= tolerance
            if relation == "sync" and offset != 0:
                self.add("sync_offset", path, "Use offset for nonzero delay; sync has zero offset", owner)
        if not ok:
            self.add("timing_constraint", path, "Declared " + relation + " relation is not satisfied", owner)
        if any(r["kind"] == "camera" for r in refs) and relation in ("sync", "offset"):
            policy = record.get("policy_binding", {})
            if "policy_binding" not in record:
                self.add("camera_policy_missing",path,"Supply M5 readonly policy or an explicit unknown; M7 does not choose camera lead/lag", "M5")
            if "source_id" not in policy:
                self.add("camera_policy_unknown", path, "M5 camera lead/sync/lag/fixed policy must remain explicit and readonly", "M5", "unverified")
            elif policy["owner"] not in ("M5", "external"):
                self.add("camera_policy_owner", path, "Camera policy belongs to M5", "M5")
            else:
                value = policy["value"]
                if not isinstance(value, dict) or value.get("mode") not in ("early", "synchronous", "late", "fixed") or "offset" not in value:
                    self.add("camera_policy_shape", path, "Readonly policy requires mode and signed camera-minus-other offset", "M5")
                else:
                    camera_offset = offset if refs[1]["kind"] == "camera" else -offset
                    declared = self.number(value["offset"], path + "/policy_binding/value/offset", "M5")
                    if declared is None:
                        self.add("camera_policy_unknown", path, "Camera offset remains unknown", "M5", "unverified")
                    elif declared != camera_offset:
                        self.add("camera_policy_changed", path, "M7 timing changed the readonly M5 offset", "M5")
                    if declared is not None and ((value["mode"] == "early" and declared >= 0) or (value["mode"] == "late" and declared <= 0) or (value["mode"] == "synchronous" and declared != 0)):
                        self.add("camera_policy_sign", path, "Camera mode contradicts its signed offset", "M5")
                    if value["mode"] == "fixed":
                        self.add("fixed_camera_policy", path, "Fixed camera is not a lead/lag move; preserve M5 scope and audit the anchor separately", "M5", "unverified")

    def mapping(self, record, clocks, known, path):
        owner = "M7.3"
        source = self.clock(record["source_clock_id"], clocks, known, path + "/source_clock_id", owner)
        target = self.clock(record["target_clock_id"], clocks, known, path + "/target_clock_id", owner)
        if record["source_clock_id"] == record["target_clock_id"]:
            self.add("mapping_clock_identity", path, "Mapping instances must identify distinct clocks", owner)
        fields = ("source_start", "source_end", "target_start", "target_end", "speed")
        s0,s1,d0,d1,v = [self.number(record[k], path + "/" + k, owner) for k in fields]
        self.bounds(s0,s1,source,path + "/source",owner)
        self.bounds(d0,d1,target,path + "/target",owner)
        binding = record["edit_binding"]
        if "source_id" in binding:
            if binding["owner"] not in ("M9", "external"):
                self.add("edit_owner", path + "/edit_binding", "Selection, speed and freeze intent belong to M9 or an explicit compatible external decision", "M9")
            value = binding["value"]
            for key in ("source_clock_id", "target_clock_id", "mode") + fields:
                if not isinstance(value,dict) or key not in value or not same(value[key], record[key]):
                    self.add("edit_intent_changed", path + "/" + key, "Mapping must preserve the exact readonly edit decision", "M9")
        elif record["mode"] != "unknown":
            self.add("edit_intent_missing", path + "/edit_binding", "Known trim/speed/freeze mapping requires an explicit readonly edit decision", "M9")
        if record["mode"] == "unknown" or any(x is None for x in (s0,s1,d0,d1,v)):
            self.add("mapping_unverified", path, "Mapping lacks a known mode or numeric parameter", owner, "unverified")
            return
        if d1 <= d0:
            self.add("mapping_target_interval", path, "Target interval must have positive duration", owner)
        if record["mode"] == "linear":
            if v <= 0 or s1 <= s0:
                self.add("mapping_linear", path, "Linear forward mapping requires positive speed and source duration", owner)
            elif d1-d0 != (s1-s0)/v:
                self.add("mapping_duration", path, "Target duration must equal source duration divided by speed", owner)
        else:
            if s0 != s1 or v != 0:
                self.add("mapping_freeze", path, "Freeze requires one source instant, zero speed, positive target duration", owner)
            if source is not None:
                origin = self.number(source["origin"], path + "/source/origin", owner)
                extent = self.number(source["extent"], path + "/source/extent", owner)
                if origin is not None and extent is not None and s0 >= origin + extent:
                    self.add("freeze_source_outside_coverage", path + "/source_start", "A freeze source instant must lie inside the half-open source coverage, not at its end boundary", owner)
            self.add("freeze_multivalued", path, "Source-to-target freeze is an interval; inverse target-to-source is constant", owner, "unverified")

    def quantization(self, record, clocks, known, path):
        self.precision_evaluated = True
        owner = "M7.3"
        clock = self.clock(record["clock_id"], clocks, known, path + "/clock_id", owner)
        tolerance = self.number(record["tolerance"], path + "/tolerance", owner)
        if tolerance is not None and tolerance < 0:
            self.add("negative_tolerance", path, "Tolerance cannot be negative", owner)
            return
        for key in ("time", "quantized_time", "error_seconds"):
            self.number(record[key], path + "/" + key, owner)
        try:
            if clock is None or clock["rate_mode"] == "unknown":
                raise MissingBasis("Known clock sampling mode required")
            if clock["rate_mode"] == "vfr" and "pts" not in clock:
                raise MissingBasis("VFR requires explicit PTS; average FPS cannot quantize")
            n,tq,error = quantize_value(record["time"],clock["fps"],record["rule"],clock["origin"],clock.get("pts") if clock["rate_mode"] == "vfr" else None)
        except MissingBasis as exc:
            self.add("precision_unverified", path, str(exc), owner, "unverified")
            if any(not isinstance(record[k], dict) for k in ("frame_index","quantized_time","error_seconds")):
                self.add("fabricated_precision", path, "Unknown timing/FPS/PTS requires unknown derived frame/time/error", owner)
            return
        except ValueError as exc:
            self.add("quantization_input", path, str(exc), owner)
            return
        expected = {"frame_index":Fraction(n), "quantized_time":tq, "error_seconds":error}
        for key,value in expected.items():
            actual = self.number(record[key], path + "/" + key, owner)
            if actual is None:
                self.add("quantization_result_unknown", path + "/" + key, "Recomputable result not yet supplied", owner, "unverified")
            elif actual != value:
                self.add("quantization_result", path + "/" + key, "Expected " + exact(value), owner)
        self.bounds(rational(record["time"]), tq, clock, path, owner)
        extent=self.number(clock["extent"],path+"/clock/extent",owner)
        origin=self.number(clock["origin"],path+"/clock/origin",owner)
        if record.get("position_kind","sample") == "sample" and extent is not None and origin is not None:
            if rational(record["time"]) >= origin+extent or tq >= origin+extent:
                self.add("sample_outside_coverage",path,"Sample must precede the half-open coverage end; use explicit boundary semantics for an end boundary",owner)
        if record["requirement"] == "exact" and error != 0:
            self.add("quantization_exactness", path, "Exact requirement has nonzero quantization error", owner)
        elif record["requirement"] == "within_tolerance":
            if tolerance is None:
                self.add("precision_unverified", path, "Tolerance is unknown", owner, "unverified")
            elif abs(error) > tolerance:
                self.add("quantization_tolerance", path, "Quantization error exceeds declared tolerance", owner)

    def domain_evidence(self, content, sources, inputs=None, path="/content"):
        contexts = [x for x in (inputs or {}).values() if isinstance(x,dict) and "source_id" in x and "values" in x]
        def binding_check(binding, where, owner):
            if "source_id" not in binding:
                self.add("binding_unknown", where, "Original semantic record remains unknown; no action/dialogue/camera/edit content may be invented", owner, "unverified")
                return
            if inputs is None:
                return # accepted state carries source-bound copy; exact request fidelity is checked at acceptance
            matching = [x for x in contexts if x["source_id"] == binding["source_id"] and x["source_version"] == binding["source_version"] and x["owner"] == binding["owner"]]
            if not matching:
                self.add("binding_context_missing", where, "Readonly binding requires a matching public context in the actual request", owner)
                return
            found=False
            for context in matching:
                try:
                    actual=read_pointer(context["values"],binding["path"])
                except (KeyError,ValueError,IndexError):
                    continue
                if same(actual,binding["value"]): found=True
            if not found:
                self.add("readonly_binding_changed", where, "Readonly record path/value differs from original external context", owner)
        for part, container in content.items():
            owner = next(k for k,v in OWNED.items() if v == part)
            for ident, record in container["items"].items():
                where=path+"/"+part+"/items/"+esc(ident)
                evidence=record.get("evidence")
                if evidence:
                    basis=evidence["basis"]
                    if basis == "reported_measurement":
                        if "observation" not in evidence or not any(sources.get(s,{}).get("kind") == "media_observation" for s in evidence["source_refs"]):
                            self.add("measurement_evidence",where+"/evidence","Reported measurement requires asset/version/method/observer/scope/locator and a media_observation source",owner)
                        self.add("measurement_authenticity_unverified",where,"Measurement metadata is not independent media verification",owner,"unverified")
                    else:
                        if "observation" in evidence:
                            self.add("evidence_basis_conflict",where,"Observation metadata requires reported_measurement basis",owner)
                        self.add("conditional_basis",where,"Numeric results are conditional on "+basis+" inputs; source authenticity remains unverified",owner,"unverified")
                for field in ("binding","edit_binding","policy_binding"):
                    if field in record:
                        binding_check(record[field],where+"/"+field,owner)
                if record["record_type"] == "event" and "source_id" in record["binding"]:
                    binding=record["binding"]
                    if binding["owner"] not in (record["event_ref"]["owner"],"external"):
                        self.add("event_binding_owner",where,"Semantic event and readonly source owner disagree",owner)
                    value=binding["value"]
                    # Public adapter shape preserves the whole opaque payload and a typed identity.
                    if not isinstance(value,dict) or not same(value.get("event_ref"),record["event_ref"]):
                        self.add("event_binding_identity",where,"Readonly event adapter must carry exactly the same event_ref; payload remains opaque",owner)
                    requirements=value.get("timing_requirements",{}) if isinstance(value,dict) else {}
                    if not isinstance(requirements,dict):
                        self.add("duration_requirements_shape",where,"Readonly timing_requirements must be an object",owner)
                        requirements={}
                    start,end=[self.number(record[k],where+"/"+k,owner) for k in ("start","end")]
                    duration=end-start if start is not None and end is not None else None
                    for field in ("minimum_duration","maximum_duration","required_duration"):
                        if field in requirements:
                            limit=self.number(requirements[field],where+"/binding/value/timing_requirements/"+field,owner)
                            if limit is not None and limit < 0:
                                self.add("duration_requirement",where,"Duration requirements cannot be negative",owner)
                            elif limit is None or duration is None:
                                self.add("duration_requirement_unverified",where,"Unknown duration prevents a required-budget verdict",owner,"unverified")
                            elif (field=="minimum_duration" and duration<limit) or (field=="maximum_duration" and duration>limit) or (field=="required_duration" and duration!=limit):
                                self.add("event_duration_requirement",where,"Scheduled duration violates readonly "+field,owner)
                if record["record_type"] == "event":
                    if record["timing_basis"] == "reported_measurement":
                        if "observation" not in record or not any(sources.get(s,{}).get("kind") == "media_observation" for s in record["source_refs"]):
                            self.add("measurement_evidence",where,"Reported event timing requires observation metadata and a registered media observation",owner)
                        self.add("measurement_authenticity_unverified",where,"Reported event metadata does not verify actual media",owner,"unverified")
                    elif "observation" in record:
                        self.add("evidence_basis_conflict",where,"Observation metadata requires reported_measurement timing basis",owner)

    def state(self, state, path="", reject_blockers=True):
        if not self.shape(state, "M7State", path):
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
    batch_ok = check.shape(batch, "M7ProposalBatch", "/batch")
    index = request_index(check, requests)
    if not state_ok or not batch_ok or check.failed:
        return None
    proposals = batch["proposals"]
    if batch["work_id"] != state["work_id"]:
        check.add("work_identity", "/batch/work_id", "Batch addresses another TimingMap")
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
            context = check.partition_context(proposal["context"].get(field),part,"/context/"+field)
            if context is not None and not same(context, candidate["content"][part]):
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
    cv = sub.add_parser("convert", help="Exact unit arithmetic; beat origin is never inferred")
    cv.add_argument("--value", required=True); cv.add_argument("--from-unit", required=True); cv.add_argument("--to-unit", required=True)
    cv.add_argument("--fps"); cv.add_argument("--bpm"); cv.add_argument("--origin")
    qz = sub.add_parser("quantize", help="Exact CFR/VFR sample quantization; nearest ties later")
    qz.add_argument("--value", required=True); qz.add_argument("--fps"); qz.add_argument("--rule", choices=("floor","ceil","nearest"), required=True)
    qz.add_argument("--origin", default="0", help="Mathematical frame-zero coordinate, default zero; not a media assertion")
    qz.add_argument("--rate-mode", choices=("cfr","vfr","unknown"), default="cfr"); qz.add_argument("--pts")
    qz.add_argument("--tolerance"); qz.add_argument("--require-exact", action="store_true")
    mp = sub.add_parser("map", help="Pure linear arithmetic d=d0+(s-s0)/v; does not grant edit authorization")
    mp.add_argument("--value", required=True); mp.add_argument("--source-start", required=True); mp.add_argument("--destination-start", required=True); mp.add_argument("--speed", required=True)
    mp.add_argument("--source-end")
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
                modules = list(OWNED) if request["target"] == "M7" else [request["target"]]
                payload = {"routes": [{"module_id": m, "resources": registry["modules"][m]["resources"],
                                        "write_scope": "/content/" + OWNED[m], "return_to": "M7",
                                        "minimum_inputs": list(MINIMUM[m]), "repair_target": m} for m in modules],
                           "route_status": "ready_with_unverified_inputs" if check.diagnostics else "ready_for_call",
                           "invocation": "not_invoked"}
        elif args.command == "check":
            artifact = get(args.proposal or args.state or args.artifact, "artifact")
            request = get(args.request, "request") if args.request else None
            index = request_index(check, get(args.requests, "requests")) if args.requests else {}
            if check.shape(artifact):
                kind = artifact["kind"]
                if kind == "M7Request": check.request(artifact)
                elif kind == "M7State": check.state(artifact)
                elif kind == "M7Proposal": check.proposal(artifact, request or index.get(artifact["source_request_id"]))
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
                    check.add("work_identity", "", "States address different TimingMaps")
                elif after["version"] < before["version"]:
                    check.add("impact_version", "", "After-state version cannot precede before-state")
                else: payload = {"impact": impact(before, after)}
        elif args.command in ("convert", "quantize", "map"):
            loaded["math_arguments"] = vars(args)
            def arg(value):
                return {"state":"unknown", "reason":"explicit CLI unknown"} if value in (None,"unknown") else value
            try:
                if args.command == "convert":
                    number = convert_value(arg(args.value), args.from_unit, args.to_unit, arg(args.fps), arg(args.bpm), None if args.origin is None else arg(args.origin))
                    payload = {"numeric_status":"calculated_conditionally", "value":exact(number), "unit":args.to_unit,
                               "assumptions":["frame coordinates are zero-based CFR", "beat indices are zero-based and need explicit origin"], "media_verified":False}
                elif args.command == "map":
                    t, end = rational(arg(args.value)), rational(arg(args.source_end)) if args.source_end is not None else None
                    start = rational(arg(args.source_start))
                    if t is not None and start is not None and (t < start or (end is not None and t >= end)):
                        raise ValueError("Sample is outside the declared half-open source window")
                    number = map_value(arg(args.value),arg(args.source_start),arg(args.destination_start),arg(args.speed))
                    payload = {"numeric_status":"calculated_conditionally", "value":exact(number), "formula":"d=d0+(s-s0)/v", "edit_authorized":False, "media_verified":False}
                else:
                    if args.rate_mode == "unknown" or (args.rate_mode == "vfr" and not args.pts):
                        raise MissingBasis("Known CFR FPS or explicit VFR PTS are required")
                    if args.rate_mode == "cfr" and args.pts:
                        raise ValueError("PTS requires --rate-mode vfr")
                    pts = get(args.pts,"pts") if args.pts else None
                    if pts is not None and not isinstance(pts,list):
                        raise ValueError("PTS file must contain a JSON array")
                    n,tq,error = quantize_value(arg(args.value),arg(args.fps),args.rule,arg(args.origin),pts)
                    tolerance = rational(arg(args.tolerance)) if args.tolerance is not None else None
                    if tolerance is not None and tolerance < 0:
                        raise ValueError("Tolerance cannot be negative")
                    if args.require_exact and error != 0:
                        check.add("quantization_exactness","","Exact requirement has nonzero error","M7.3")
                    if tolerance is not None and abs(error)>tolerance:
                        check.add("quantization_tolerance","","Quantization exceeds tolerance","M7.3")
                    payload = {"numeric_status":"calculated_conditionally", "frame_index":n, "quantized_time":exact(tq), "error_seconds":exact(error), "absolute_error_seconds":exact(abs(error)), "within_tolerance":None if tolerance is None else abs(error)<=tolerance, "frame_rule":"zero-based sample at origin+n/f; nearest ties to later frame", "media_verified":False}
            except MissingBasis as exc:
                check.add("numeric_basis_unknown","",str(exc),"M7.1" if args.command=="convert" else "M7.3","unverified")
                payload={"numeric_status":"unverified", "media_verified":False}
        status = "fail" if check.failed else "pass"
        original_requests = []
        for artifact in loaded.values():
            if isinstance(artifact, dict) and artifact.get("kind") == "M7Request":
                original_requests.append(artifact)
            elif isinstance(artifact, list):
                original_requests.extend(r for r in artifact if isinstance(r, dict) and r.get("kind") == "M7Request")
        trace = {"call_id": "m7-" + uuid.uuid4().hex, "parent_module": "M7", "started_at": started,
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
        precision_unknown={"fps_unknown","clock_context_unknown","precision_unverified","quantization_result_unknown","rate_mode_unknown","vfr_pts_unknown","numeric_basis_unknown"}
        precision_status="not_evaluated"
        if check.precision_evaluated or args.command=="quantize":
            precision_status="fail" if check.failed else ("unverified" if any(d["code"] in precision_unknown for d in check.diagnostics) else "calculated_conditionally")
        elif any(d["code"] in precision_unknown for d in check.diagnostics):
            precision_status="unverified"
        result = {"kind": "M7ToolResult", "contract_version": VERSION, "command": args.command,
                  "execution": "completed", "disposition": "rejected" if check.failed else "checked_draft",
                  "validation": {"local_contract": status, "overall": "fail" if check.failed else "unverified", "numeric_precision":precision_status, "unverified": UNVERIFIED},
                  "diagnostics": check.diagnostics, "trace": trace, **payload}
        if args.command == "accept":
            result["accepted"] = "state" in payload and not check.failed
        if args.command == "route" and check.failed:
            result.update({"route_status": "blocked", "invocation": "not_invoked", "routes": []})
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 1 if check.failed else 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, RecursionError) as exc:
        print(json.dumps({"kind": "M7ToolError", "command": args.command,
                          "execution": "error", "error": str(exc), "side_effects": "none"}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
