#!/usr/bin/env python3
"""Reproduce the guided, offline M6.3 audit; write only beneath this directory."""
import copy
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
SKILL = REPO / "docs/h3skill/h3-sound-music-dialogue"
BRIEF = HERE.parent / "mv-task.txt"


def unknown(reason):
    return {"state": "unknown", "reason": reason}


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    run = HERE / "trial" / stamp
    run.mkdir(parents=True, exist_ok=False)
    brief_text = BRIEF.read_text(encoding="utf-8")
    (run / "actual-request.txt").write_text(brief_text, encoding="utf-8")

    request_path = run / "request.json"
    proposal_path = run / "proposal.json"
    templates = {
        "request": SKILL / "assets/request-standalone-m6-3.json",
        "proposal": SKILL / "assets/proposal-standalone-m6-3.json",
    }
    shutil.copyfile(templates["request"], request_path)
    shutil.copyfile(templates["proposal"], proposal_path)
    request = json.loads(request_path.read_text(encoding="utf-8"))
    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))

    sources = {"MV-BRIEF": {
        "kind": "user_requirement",
        "locator": str(BRIEF.relative_to(REPO)),
        "version": "1",
        "excerpt": brief_text,
    }}
    inputs = {
        "music_brief": "12 秒双人海边舞蹈；AUDIO-MASTER 必须完整 1:1 保留并作为完整最终音轨，同时新增两个清楚脚步声与海浪环境声。用户未同意修改任何要求；约 120 BPM 仅为文字说明。",
        "reference_context": {
            "owner": "external",
            "source_id": "MV-BRIEF",
            "source_version": "1",
            "values": {
                "target_duration_seconds": 12,
                "generation_mode": unknown("待 M11 协议层确认"),
                "audio_registration": {
                    "asset_id": "AUDIO-MASTER",
                    "available": False,
                    "asset_version": unknown("未提供实际媒体或其版本"),
                    "duration_seconds": unknown("用户未提供音轨时长；12 秒是目标视频时长"),
                    "source_window": unknown("用户未提供源音轨窗口"),
                    "first_beat_offset_seconds": unknown("没有可播放信号或拍点测量"),
                    "measurement_evidence": unknown("音轨登记仅为用户说明，没有信号观测"),
                    "bpm_description": "约 120 BPM，用户文字说明，未经测量",
                },
                "lyric_cue": {
                    "function": "仅提示 ROLE-B 开始 ACT-GESTURE，不据此指定 ROLE-B 唱词或口型",
                    "original_text": unknown("未取得经核对歌词转写"),
                    "approved_text": unknown("未取得经核对歌词文本"),
                    "time_seconds": unknown("无歌词转写及音频定位依据"),
                },
                "action_reference": "用户称参考视频用于动作；当前无可播放视频，未授权将视频音频作为最终声源",
                "known_action_ids": ["ACT-STEP", "ACT-GESTURE"],
                "second_footstep_action": unknown("只提供 ROLE-A 的 ACT-STEP；第二个脚步对应动作未提供"),
                "voice_information": unknown("未提供角色音色资料；语义歌词提示不构成新演唱要求"),
                "scope_id_note": "MV-SCOPE-12S 只是本次审计的内部范围 ID，非已批准镜头编号或 H3 标签",
            },
        },
    }
    # AudioAsset requires a numeric duration. Unknown duration is retained in the
    # external registry above; do not fabricate duration=0 or preserve sample data.
    request.update({
        "work_id": "m6_forward_mv_guided_audit",
        "request_id": "mv_request_m6_3",
        "sources": sources,
        "inputs": inputs,
    })
    proposal.update({
        "work_id": request["work_id"],
        "proposal_id": "mv_proposal_m6_3",
        "source_request_id": request["request_id"],
        "sources": copy.deepcopy(sources),
        "context": copy.deepcopy(inputs),
        "changes": {"music": {"items": {"MV-MUSIC": {
            "music_id": "MV-MUSIC",
            "shot_id": "MV-SCOPE-12S",
            "use_strategy": "fully_copy",
            "audio_selection": unknown("AUDIO-MASTER 登记可识别，但媒体 unavailable，真实时长及源窗口均未知；不能填造 AudioAsset 或选择窗口"),
            "whole_source": "yes",
            "additional_audio": "yes",
            "removals_or_replacements": "no",
            "music_requirement": {
                "state": "known",
                "value": "忠实保留相互冲突的用户要求：AUDIO-MASTER 完整 1:1 作为完整最终音轨，同时新合成两个清楚脚步声和海浪环境声。尚无同意变更的记录；此提案用于审计，不是可接受的成片方案。",
                "source_refs": ["MV-BRIEF"],
            },
            "beat_plan": unknown("约 120 BPM 不能确定真实拍点、首拍偏移、歌词位置或每个动作的精确卡点；交 M7 在取得信号和动作资料后确定"),
            "timing_owner": "M7",
            "edit_owner": "M9",
            "source_refs": ["MV-BRIEF"],
            "applies_to_shots": ["MV-SCOPE-12S"],
        }}}},
        "issues": [{
            "issue_id": "MV-FULL-COPY-ADDITIONS",
            "owner": "M6.3",
            "status": "open",
            "severity": "blocking",
            "message": "完整最终音轨 1:1 保留与新增声层冲突。需用户经 M1/M2 明确取舍后，由 M6.3 更新策略并交 M9 实现；当前不得擅改为 partially_copy 或删去音效要求。",
            "source_refs": ["MV-BRIEF"],
        }],
        "resolutions": [],
    })
    dump(request_path, request)
    dump(proposal_path, proposal)

    script = SKILL / "scripts/m6_contract.py"
    calls = [
        ("route", [sys.executable, "-B", str(script), "route", str(request_path)]),
        ("check", [sys.executable, "-B", str(script), "check", str(proposal_path), "--request", str(request_path)]),
    ]
    manifest = {
        "trial_type": "主线程引导后的定向审计；非盲测",
        "cwd": str(REPO),
        "brief_sha256": hashlib.sha256(BRIEF.read_bytes()).hexdigest(),
        "runtime_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "templates": {name: str(path.relative_to(REPO)) for name, path in templates.items()},
        "artifact_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (request_path, proposal_path)
        },
        "calls": [],
    }
    for name, argv in calls:
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        result = subprocess.run(argv, cwd=REPO, text=True, capture_output=True, check=False)
        (run / f"{name}.stdout.txt").write_text(result.stdout, encoding="utf-8")
        (run / f"{name}.stderr.txt").write_text(result.stderr, encoding="utf-8")
        (run / f"{name}.exit.txt").write_text(str(result.returncode) + "\n", encoding="utf-8")
        manifest["calls"].append({
            "name": name, "argv": argv, "started_utc": started,
            "exit_code": result.returncode,
            "stdout_file": f"{name}.stdout.txt", "stderr_file": f"{name}.stderr.txt",
        })
    dump(run / "command-manifest.json", manifest)
    print(json.dumps({"run_directory": str(run), "calls": [
        {"name": call["name"], "exit_code": call["exit_code"]} for call in manifest["calls"]
    ]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
