"""Reproduce the INITIAL independent attempt using only the public CLI.

Optional argument: fresh output directory name below this script's directory.
Original run-001 inputs and logs must not be overwritten.
This intentionally preserves the initial projection/source-ID mistakes.
The final checked artifacts are run-001/*m7-1.json and run-003/*m7-2.json.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]
OUT = HERE / (sys.argv[1] if len(sys.argv) > 1 else "run-001")
if OUT.parent.resolve() != HERE.resolve():
    raise SystemExit("Output must be directly beneath the designated music directory")
OUT.mkdir(exist_ok=True)
if any(OUT.iterdir()):
    raise SystemExit("Choose a fresh run directory; existing evidence is preserved")

def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def unknown(reason):
    return {"state": "unknown", "reason": reason}

sources = {"user_design": {
    "kind": "user_requirement",
    "locator": "docs/h3skill/validation/m7/forward-use/music-task.txt",
    "version": "provided-task",
    "excerpt": "12秒舞蹈MV；名义BPM100，无音频及首拍偏移；生成FPS未知，编辑计划30FPS；actionA生成局部0.5至2.5秒不可删除或缩短；后续动作未设计；固定摄影机观察12秒；单次12秒生成，无新增切镜要求。均为设计条件，非媒体实测。"
}}
refs = ["user_design"]
evidence = {"basis": "planned", "source_refs": refs}

def clock(name, domain, domain_id, fps, origin, extent):
    return {"record_type": "clock", "clock_id": name, "domain": domain,
            "domain_id": domain_id, "rate_mode": "unknown", "fps": fps,
            "origin": origin, "extent": extent, "evidence": evidence,
            "source_refs": refs}

timebase = {"items": {
    "generation_clock": clock("generation_clock", "generation", "generation_job1",
        unknown("生成FPS尚未确定，不能借用后期30FPS"), 0, 12),
    "edit_clock": clock("edit_clock", "edit", "edit_plan",
        30, unknown("编辑时间线的放置起点未提供"), unknown("尚无生成至编辑的映射及速度计划")),
    "music_grid": {"record_type": "beat_grid", "grid_id": "music_grid",
        "clock_id": "generation_clock", "bpm": 100,
        "first_beat": unknown("无音频、无首拍偏移；不能把生成局部0秒视为首拍"),
        "beat_index_origin": 0, "evidence": evidence, "source_refs": refs}
}}

inputs1 = {"timebase_brief": "建立本次12秒生成的局部秒时钟及计划编辑时钟；100BPM只给出3/5秒拍间隔。首拍相位、生成FPS和编辑放置未知。所有条件来自任务设计。"}

action_ref = {"owner": "M4", "kind": "action", "id": "actionA",
              "domain": "generation", "domain_id": "generation_job1"}
camera_ref = {"owner": "M5", "kind": "camera", "id": "fixed_camera",
              "domain": "generation", "domain_id": "generation_job1"}
action = {"event_ref": action_ref,
          "payload": {"text": "M4给定actionA不可删除或缩短；具体动作语义未提供，不补写。"},
          "timing_requirements": {"required_duration": 2}}
camera = {"event_ref": camera_ref,
          "payload": {"text": "M5已选固定摄影机，观察整个12秒片段；无每拍重启要求。"},
          "timing_requirements": {"required_duration": 12}}

def context(owner, source_id, key, value):
    return {"owner": owner, "source_id": source_id, "source_version": "provided-task",
            "values": {"events": {key: value}}}

def binding(owner, source_id, key, value):
    return {"owner": owner, "source_id": source_id, "source_version": "provided-task",
            "path": "/events/" + key, "value": value}

ab = binding("M4", "m4_design", "actionA", action)
cb = binding("M5", "m5_design", "fixed_camera", camera)
inputs2 = {
    "schedule_brief": "只编排已有actionA[0.5,2.5)和固定摄影机[0,12)，互相独立；后续动作及节拍绝对同步保留未知，不新增切镜。",
    "timebase_context": timebase,
    "action_context": context("M4", "m4_design", "actionA", action),
    "camera_context": context("M5", "m5_design", "fixed_camera", camera),
    "readonly_projection": [ab, cb]
}

def event(timing_id, event_ref, start, end, bound):
    return {"record_type": "event", "timing_id": timing_id,
            "event_ref": event_ref, "clock_id": "generation_clock",
            "start": start, "end": end, "extent_kind": "interval",
            "timing_basis": "planned", "binding": bound, "source_refs": refs}

schedule = {"items": {
    "actionA_timing": event("actionA_timing", action_ref, "1/2", "5/2", ab),
    "fixed_camera_timing": event("fixed_camera_timing", camera_ref, 0, 12, cb),
    "camera_covers_action": {"record_type": "constraint", "constraint_id": "camera_covers_action",
        "relation": "overlap", "event_refs": [action_ref, camera_ref],
        "left_edge": "start", "right_edge": "start", "offset": 2, "tolerance": 0,
        "source_refs": refs}
}}

def issue(module, key, message):
    return {"issue_id": key, "owner": module, "status": "open",
            "severity": "warning", "message": message, "source_refs": refs}

def pair(suffix, module, inputs, changes, issues):
    req = {"kind": "M7Request", "contract_version": "1.0.0", "work_id": "forward_music_12s",
           "base_version": 0, "request_id": "music_req_" + suffix, "target": module,
           "sources": sources, "inputs": inputs}
    prop = {"kind": "M7Proposal", "contract_version": "1.0.0", "work_id": "forward_music_12s",
            "base_version": 0, "proposal_id": "music_proposal_" + suffix, "module_id": module,
            "source_request_id": req["request_id"], "sources": sources,
            "context": copy.deepcopy(inputs), "changes": changes, "issues": issues, "resolutions": []}
    write("request-" + suffix + ".json", req)
    write("proposal-" + suffix + ".json", prop)

pair("m7-1", "M7.1", inputs1, {"timebase": timebase}, [
    issue("M7.1", "missing_phase", "M2/M12向音乐责任方补首拍与节拍依据；M6确认音频及其相位后才能放置绝对拍点。"),
    issue("M7.1", "missing_sampling", "M11确认生成FPS及采样方式；M9确认编辑放置及映射。当前不做帧量化或跨域转换。")])
pair("m7-2", "M7.2", inputs2, {"schedule": schedule}, [
    issue("M7.2", "remaining_actions", "M4尚未设计后续动作；[0,0.5)及[2.5,12)无已知动作内容，不推断静止、空白或停顿。"),
    issue("M7.2", "unknown_beat_alignment", "首拍相位未知，actionA起点是否落拍无法验证；2秒持续时间必须保留，不为卡拍缩短。"),
    issue("M7.2", "partial_only", "只交付秒域局部排程；缺生成采样与跨域映射，尚不能形成完整TimingMap或验证H3效果。")])

runner = ROOT / "docs/h3skill/h3-time-synchronization/scripts/m7_contract.py"
records = []
for suffix in ("m7-1", "m7-2"):
    req = OUT / ("request-" + suffix + ".json")
    prop = OUT / ("proposal-" + suffix + ".json")
    for command, args in (("route", ["--request", str(req)]),
                          ("check", ["--proposal", str(prop), "--request", str(req)])):
        argv = [sys.executable, "-B", str(runner), command] + args
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        name = suffix + "-" + command
        (OUT / (name + ".stdout.txt")).write_text(result.stdout)
        (OUT / (name + ".stderr.txt")).write_text(result.stderr)
        records.append({"command": argv, "command_shell": shlex.join(argv), "cwd": str(ROOT),
                        "exit_code": result.returncode, "stdout": name + ".stdout.txt",
                        "stderr": name + ".stderr.txt",
                        "inputs": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in ([req] if command == "route" else [req, prop])}})
        write("commands.json", records)
        print(name, "exit", result.returncode, result.stdout, result.stderr)
