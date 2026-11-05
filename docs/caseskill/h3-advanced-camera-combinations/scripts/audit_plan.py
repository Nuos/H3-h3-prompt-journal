#!/usr/bin/env python3
"""Audit an H3 case plan and optional prompt files; never run inference.

Python 3.10+, standard library only. Exit 0 means the requested static checks
passed, 1 means a contract violation, and 2 means input/JSON could not be read.
Human attestations in case_checks are not independently verified by this tool.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

BASE_FIELDS = ["integrated_multimodal_description", "overall_soundscape", "non_diegetic_music"]
REF_FIELDS = ["subject_definitions", "summary", "retention_analysis", "detailed_description", "overall_soundscape", "non_diegetic_music"]
MODES = {"T2VA", "I2VA", "FL2VA", "L2VA", "Ref2VA"}
LABEL = re.compile(r"<(Subject|Picture|Video|Audio) ([1-9][0-9]*)>")
EPS = 0.000001


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def audit(plan, root, contract, strict=False, check_files=False):
    errors, warnings = [], []

    def need(ok, message):
        if not ok:
            errors.append(message)
        return bool(ok)

    def pending(message):
        (errors if strict else warnings).append(message)

    def rows(value, location):
        if not need(isinstance(value, list), f"{location}: expected an array"):
            return []
        result = []
        for i, item in enumerate(value):
            if need(isinstance(item, dict), f"{location}[{i}]: expected an object"):
                result.append(item)
        return result

    if not isinstance(plan, dict):
        return {"errors": ["Plan must be a JSON object"], "warnings": []}
    need(plan.get("schema_version") == "1.0", "schema_version must be 1.0")
    need(plan.get("case_id") == contract.get("case_id"), "case_id does not match this skill")
    kind = plan.get("delivery_kind")
    need(kind in {"component", "prompts"}, "delivery_kind must be component or prompts")
    need(plan.get("status") in {"draft", "ready"}, "status must be draft or ready")
    if strict:
        need(plan.get("status") == "ready", "Strict review requires status=ready")
    unresolved = plan.get("unresolved", [])
    need(isinstance(unresolved, list), "unresolved must be an array")
    if unresolved:
        pending("Unresolved input, timing, or version decisions remain")
    assembly = plan.get("assembly", "sequential")
    need(assembly in {"sequential", "variants", "component"}, "Invalid assembly")
    assets = {}
    for asset in rows(plan.get("assets", []), "assets"):
        aid = asset.get("id")
        if not need(nonempty(aid), "Every asset needs a nonempty id"):
            continue
        need(aid not in assets, f"Duplicate asset id: {aid}")
        assets[aid] = asset
        need(asset.get("kind") in {"image", "video", "audio"}, f"{aid}: invalid kind")
        need(asset.get("status") in {"provided", "missing"}, f"{aid}: invalid asset status")
        if asset.get("status") != "provided" or not nonempty(asset.get("locator")):
            pending(f"{aid}: source asset has not been supplied")
        roles = asset.get("roles")
        need(isinstance(roles, list) and bool(roles) and all(nonempty(r) for r in roles), f"{aid}: specify asset roles")

    refs = {}
    for ref in rows(plan.get("references", []), "references"):
        label = ref.get("label")
        if not need(isinstance(label, str) and LABEL.fullmatch(label), "Reference label must use <Subject N>, <Picture N>, <Video N>, or <Audio N>"):
            continue
        need(label not in refs, f"Duplicate reference label: {label}")
        refs[label] = ref
        need(nonempty(ref.get("role")), f"{label}: missing reference role")
        ids = ref.get("asset_ids")
        if not need(isinstance(ids, list) and bool(ids) and all(nonempty(a) for a in ids), f"{label}: supply asset_ids"):
            continue
        for aid in ids:
            if not need(aid in assets, f"{label}: unknown asset {aid}"):
                continue
            asset = assets[aid]
            if label.startswith("<Picture"):
                need(asset.get("kind") == "image", f"{label}: a picture must bind an image")
                need(len(ids) == 1, f"{label}: a concrete picture label must name exactly one image")
            elif label.startswith("<Video"):
                need(asset.get("kind") == "video", f"{label}: a video must bind a video")
            elif label.startswith("<Audio"):
                need(asset.get("kind") == "audio" or (asset.get("kind") == "video" and asset.get("audio_enabled") is True), f"{label}: enable the source video's audio explicitly or supply an audio asset")

    checks = rows(plan.get("case_checks", []), "case_checks")
    seen_checks = {}
    expected = set(contract.get("required_check_ids", []))
    for check in checks:
        cid = check.get("id")
        if not need(nonempty(cid), "A case check needs a nonempty id"):
            continue
        need(cid not in seen_checks, f"Duplicate case check: {cid}")
        seen_checks[cid] = check
        need(cid in expected, f"Unknown case check: {cid}")
        state = check.get("status")
        need(state in {"pass", "fail", "unverified", "not_applicable"}, f"{cid}: invalid check status")
        if state == "fail":
            need(False, f"{cid}: case-specific review failed")
        elif state == "unverified":
            pending(f"{cid}: case-specific review has not been performed")
        elif state in {"pass", "not_applicable"}:
            need(nonempty(check.get("evidence")), f"{cid}: provide concrete review evidence or a non-applicability reason")
    need(expected <= seen_checks.keys(), "Missing case checks: " + ", ".join(sorted(expected - seen_checks.keys())))

    runtime = plan.get("runtime", {})
    if not need(isinstance(runtime, dict), "runtime must be an object"):
        runtime = {}
    profile = runtime.get("profile", "official-2026-10-28")
    need(profile in {"official-2026-10-28", "verified-custom"}, "Unknown runtime profile")
    min_duration, max_duration, expected_fps = 4, 15, 24
    if profile == "verified-custom":
        need(nonempty(runtime.get("evidence")), "A custom runtime needs a concrete version/capability evidence reference")
        for key in ("min_duration_s", "max_duration_s", "fps"):
            need(number(runtime.get(key)) and runtime[key] > 0, f"Custom runtime needs positive {key}")
        if all(number(runtime.get(k)) for k in ("min_duration_s", "max_duration_s", "fps")):
            min_duration, max_duration, expected_fps = (runtime[k] for k in ("min_duration_s", "max_duration_s", "fps"))
            need(min_duration <= max_duration, "Custom duration interval is reversed")
    fps = plan.get("fps")
    need(number(fps) and fps > 0, "fps must be a positive finite number")
    if plan.get("edit_fps") is not None:
        need(number(plan["edit_fps"]) and plan["edit_fps"] > 0, "edit_fps must be positive; it does not alter the generation runtime")
    if number(fps):
        need(abs(fps - expected_fps) <= EPS, "fps disagrees with the selected runtime profile")

    segments = rows(plan.get("segments", []), "segments")
    if kind == "prompts":
        if not segments:
            pending("A prompt deliverable needs at least one generation segment")
    elif segments:
        need(False, "Component-only output must not masquerade as a generation payload; select delivery_kind=prompts")
    ids, prev_end = set(), 0.0
    for segment in segments:
        sid = segment.get("id")
        if not need(nonempty(sid), "Each segment needs a nonempty id"):
            continue
        need(sid not in ids, f"Duplicate segment id: {sid}")
        ids.add(sid)
        mode = segment.get("mode")
        need(mode in MODES, f"{sid}: invalid H3 mode")
        duration = segment.get("duration_s")
        if not need(number(duration) and duration > 0, f"{sid}: positive finite duration_s required"):
            continue
        need(min_duration - EPS <= duration <= max_duration + EPS, f"{sid}: duration is outside the selected runtime range {min_duration}–{max_duration}s; split the generation or verify a custom runtime")
        edit_duration = duration
        window = segment.get("edit_window_s")
        if window is not None:
            if need(isinstance(window, list) and len(window) == 2 and all(number(x) for x in window), f"{sid}: edit_window_s must contain two finite seconds"):
                a, b = window
                if need(0 <= a < b <= duration + EPS, f"{sid}: crop window is outside the generated clip"):
                    edit_duration = b - a
        crop_duration = edit_duration
        previous_hold = -1.0
        for hold in rows(segment.get("edit_holds", []), f"{sid}.edit_holds"):
            at, length = hold.get("at_s"), hold.get("duration_s")
            if need(number(at) and number(length) and length > 0, f"{sid}: a freeze addition needs a finite position and positive duration"):
                need(0 <= at <= crop_duration and at > previous_hold, f"{sid}: freeze positions must increase within the cropped, pre-freeze clip")
                previous_hold = at
                edit_duration += length
            if not nonempty(hold.get("evidence")):
                pending(f"{sid}: identify the retained frame and reason for each freeze addition")
        if segment.get("edit_duration_s") is not None:
            need(number(segment["edit_duration_s"]) and abs(segment["edit_duration_s"] - edit_duration) <= EPS, f"{sid}: edit_duration_s disagrees with the selected crop and added freezes")
        start = segment.get("global_start_s")
        if need(number(start) and start >= 0, f"{sid}: nonnegative global_start_s required"):
            if assembly == "sequential":
                need(abs(start - prev_end) <= EPS, f"{sid}: global timeline gap or overlap")
                prev_end = start + edit_duration
        frames = segment.get("frame_count")
        if frames is not None and number(fps) and fps > 0:
            need(isinstance(frames, int) and not isinstance(frames, bool) and frames > 0 and abs(frames / fps - duration) <= 0.5 / fps + EPS, f"{sid}: frame_count does not match duration/fps within half a frame")

        used_labels = segment.get("reference_labels", [])
        if not need(isinstance(used_labels, list) and all(nonempty(x) for x in used_labels), f"{sid}: reference_labels must be an array of strings"):
            used_labels = []
        need(len(used_labels) == len(set(used_labels)), f"{sid}: duplicate reference label")
        used_assets = set()
        for label in used_labels:
            if need(label in refs, f"{sid}: undefined label {label}"):
                used_assets.update(a for a in refs[label].get("asset_ids", []) if isinstance(a, str) and a in assets)
        for key in ("first_frame_asset_id", "last_frame_asset_id"):
            aid = segment.get(key)
            required = (key == "first_frame_asset_id" and mode in {"I2VA", "FL2VA"}) or (key == "last_frame_asset_id" and mode in {"L2VA", "FL2VA"})
            if required:
                need(isinstance(aid, str) and aid in assets and assets[aid].get("kind") == "image", f"{sid}: {key} must name a supplied image")
            if isinstance(aid, str) and aid in assets:
                used_assets.add(aid)
        anchors = []
        if mode in {"I2VA", "FL2VA"}:
            anchors.append(("<Picture 1>", segment.get("first_frame_asset_id")))
        if mode == "FL2VA":
            anchors.append(("<Picture 2>", segment.get("last_frame_asset_id")))
        if mode == "L2VA":
            anchors.append(("<Picture 1>", segment.get("last_frame_asset_id")))
        for label, aid in anchors:
            need(label in used_labels and refs.get(label, {}).get("asset_ids") == [aid], f"{sid}: {label} does not bind the actual keyframe asset")
        if mode == "T2VA":
            need(not used_labels, f"{sid}: T2VA cannot claim bound reference inputs")
        if mode == "Ref2VA":
            need(bool(used_labels), f"{sid}: Ref2VA needs actual reference bindings")
            kinds = {k: [assets[a] for a in used_assets if assets[a].get("kind") == k] for k in ("image", "video", "audio")}
            # Limits are per generation, never across an entire multi-segment film.
            need(len(used_assets) <= 12, f"{sid}: more than 12 reference files in one generation")
            for kind_, limit in (("image", 9), ("video", 3), ("audio", 3)):
                need(len(kinds[kind_]) <= limit, f"{sid}: too many {kind_} files")
            for kind_ in ("video", "audio"):
                total, complete = 0, True
                for asset in kinds[kind_]:
                    length = asset.get("duration_s")
                    if not number(length):
                        pending(f"{sid}/{asset['id']}: record the measured {kind_} input duration")
                        complete = False
                    else:
                        need(2 - EPS <= length <= 15 + EPS, f"{sid}/{asset['id']}: reference {kind_} must be 2–15s under the documented input contract")
                        total += length
                if complete:
                    need(total <= 15 + EPS, f"{sid}: total {kind_} reference duration exceeds 15s")
        shots = rows(segment.get("shots", []), f"{sid}.shots")
        need(bool(shots), f"{sid}: no shots")
        last = 0.0
        for n, shot in enumerate(shots, 1):
            need(shot.get("id") == n, f"{sid}: shot IDs must be consecutive from 1")
            a, b = shot.get("start_s"), shot.get("end_s")
            if not need(number(a) and number(b), f"{sid}/Shot{n}: numeric boundaries required"):
                continue
            need(abs(a - last) <= EPS, f"{sid}/Shot{n}: shot timeline gap or overlap")
            need(b > a and b <= duration + EPS, f"{sid}/Shot{n}: invalid shot interval")
            last = b
            for key in ("action", "camera", "sound"):
                if not nonempty(shot.get(key)):
                    pending(f"{sid}/Shot{n}: missing {key}")
        if shots:
            need(abs(last - duration) <= EPS, f"{sid}: shots do not cover the complete segment")
        if check_files:
            prompt_name = segment.get("prompt_file")
            if not need(nonempty(prompt_name), f"{sid}: prompt_file missing"):
                continue
            path = (root / prompt_name).resolve()
            if not need(path.is_relative_to(root.resolve()), f"{sid}: prompt_file must stay inside the plan directory"):
                continue
            try:
                prompt = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                need(False, f"{sid}: cannot read prompt_file: {exc}")
                continue
            check_prompt(prompt, segment, used_labels, need)

    if assembly == "sequential" and len(segments) > 1:
        links = rows(plan.get("handoffs", []), "handoffs")
        pairs = {}
        for link in links:
            pair = (link.get("from"), link.get("to"))
            if not all(isinstance(x, str) for x in pair):
                need(False, "A handoff needs from/to segment IDs")
                continue
            need(pair not in pairs, f"Duplicate handoff: {pair}")
            pairs[pair] = link
            need(link.get("type") in {"continuous", "hard_cut"}, f"{pair}: select continuous or hard_cut")
            if not nonempty(link.get("evidence")) or not nonempty(link.get("audio_strategy")):
                pending(f"{pair}: handoff needs state and audio-transfer evidence")
        expected_pairs = {(a.get("id"), b.get("id")) for a, b in zip(segments, segments[1:])}
        need(set(pairs) == expected_pairs, "Handoff records must cover every consecutive segment pair exactly once")
    return {"errors": errors, "warnings": warnings}


def check_prompt(prompt, segment, used_labels, need):
    sid, mode = segment["id"], segment["mode"]
    fields = REF_FIELDS if mode == "Ref2VA" else BASE_FIELDS
    need(not re.search(r"\{(?:define actual|task-type|one applicable|one or two|composition,|MM:SS|ambient and|audience-only|style,|N\}|S\.SS)", prompt), f"{sid}: an output-template placeholder remains")
    need(not re.search(r"<(?:Subject|Picture|Video|Audio) N>", prompt), f"{sid}: a reference-number placeholder remains")
    candidates = list(re.finditer(r"^(" + "|".join(REF_FIELDS + BASE_FIELDS) + r"): *(.*)$", prompt, re.M))
    need([m.group(1) for m in candidates] == fields, f"{sid}: wrong, duplicate, missing, or unordered official fields")
    chunks = {}
    for i, match in enumerate(candidates):
        end = candidates[i + 1].start() if i + 1 < len(candidates) else len(prompt)
        chunks[match.group(1)] = prompt[match.start() + len(match.group(1)) + 1:end].strip()
    for field in fields:
        need(nonempty(chunks.get(field)), f"{sid}: empty {field}")
    body = chunks.get("detailed_description" if mode == "Ref2VA" else "integrated_multimodal_description", "")
    markers = list(re.finditer(r"\[Shot ([0-9]+)\]", body))
    shots = segment.get("shots", [])
    need([int(m.group(1)) for m in markers] == list(range(1, len(shots) + 1)), f"{sid}: prompt shot markers disagree with the plan")
    if markers:
        if mode == "Ref2VA":
            need(nonempty(body[:markers[0].start()]), f"{sid}: Ref2VA style opening must precede [Shot 1]")
        else:
            need(not body[:markers[0].start()].strip(), f"{sid}: base description begins with [Shot 1]")
    for i, marker in enumerate(markers):
        tail = body[marker.end():].lstrip()
        if i == 0:
            need(not re.match(r"At \d+:\d", tail), f"{sid}: [Shot 1] must not have a cut timestamp")
        else:
            match = re.match(r"At (\d{2,}):(\d{2})\.(\d{3}),", tail)
            if need(match is not None, f"{sid}/Shot{i + 1}: expected At MM:SS.mmm,"):
                mins, sec, ms = map(int, match.groups())
                timestamp = mins * 60 + sec + ms / 1000
                need(sec < 60 and 0 < timestamp < segment["duration_s"], f"{sid}: invalid cut timestamp")
                if i < len(shots) and number(shots[i].get("start_s")):
                    need(abs(timestamp - shots[i]["start_s"]) <= 0.0005 + EPS, f"{sid}: prompt cut time disagrees with the plan")
    labels = {m.group(0) for m in LABEL.finditer(prompt)}
    need(labels <= set(used_labels), f"{sid}: prompt uses undeclared reference labels: {sorted(labels - set(used_labels))}")
    if mode == "Ref2VA":
        need(set(used_labels) <= labels, f"{sid}: reference labels in the plan never appear in the prompt: {sorted(set(used_labels)-labels)}")
    malformed = [m.group(0) for m in re.finditer(r"<(?:Subject|Picture|Video|Audio)\s*\d+>", prompt) if not LABEL.fullmatch(m.group(0))]
    need(not malformed, f"{sid}: malformed labels: {malformed}")
    n, duration = len(shots), segment["duration_s"]
    prefixes = {
        "I2VA": "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.",
        "FL2VA": f"How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot {n}) aligns with the {duration:.2f}-second mark of the target video.",
        "L2VA": f"How the reference pictures align with the target video — <Picture 1> (from [Shot {n}]) aligns with the {duration:.2f}-second mark of the target video.",
    }
    if mode in prefixes:
        need(prompt.strip().startswith(prefixes[mode] + "\n\n"), f"{sid}: keyframe alignment instruction is missing or inconsistent")
    elif mode in {"T2VA", "Ref2VA"}:
        need(prompt.lstrip().startswith(fields[0] + ":"), f"{sid}: unexpected material before the first official field")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--contract", type=Path, default=Path(__file__).resolve().parents[1] / "assets" / "case-contract.json")
    parser.add_argument("--strict", action="store_true", help="Reject draft status, missing inputs, and unverified manual gates")
    parser.add_argument("--check-files", action="store_true", help="Read only local prompt files and check official fields/cut times; never inspect media or execute a workflow")
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
        if not isinstance(contract, dict):
            raise ValueError("Contract must be a JSON object")
        result = audit(plan, args.plan.resolve().parent, contract, args.strict, args.check_files)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        print(json.dumps({"static_pass": False, "input_error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    result.update({"static_pass": not result["errors"], "complete_under_requested_checks": not result["errors"] and not result["warnings"], "checked_prompt_files": args.check_files, "semantic_validation": "not_performed", "human_case_checks": "declared_by_plan_author_not_independently_verified", "model_inference": "not_performed"})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
