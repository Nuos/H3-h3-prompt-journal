#!/usr/bin/env python3
"""Black-box M6 CLI behavior checks using copies of the public design fixtures.

Run with: python -B -m unittest discover -s docs/h3skill/tests -p test_m6_contract.py -v
These tests do not import the runtime, modify distributed inputs, or test media.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / "docs/h3skill/h3-sound-music-dialogue"
SCRIPT = PACKAGE / "scripts/m6_contract.py"
ASSETS = PACKAGE / "assets"
PARTITIONS = ("sources", "vocal_events", "music", "effects")


class M6ContractBehavior(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="m6-contract-test-")
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name)
        shutil.copytree(ASSETS, self.work / "assets")

    def fixture(self, name):
        return json.loads((self.work / "assets" / name).read_text(encoding="utf-8"))

    def write(self, name, value):
        path = self.work / name
        path.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False), encoding="utf-8")
        return path

    def cli(self, command, *arguments, expected=0):
        completed = subprocess.run(
            [sys.executable, "-I", "-S", str(SCRIPT), command, *map(str, arguments)],
            cwd=self.work, capture_output=True, text=True, timeout=20, check=False,
        )
        detail = f"{command}: stdout={completed.stdout}\nstderr={completed.stderr}"
        self.assertEqual(completed.returncode, expected, detail)
        try:
            result = json.loads(completed.stdout)
        except ValueError as exc:
            self.fail(f"CLI did not return JSON: {exc}\n{detail}")
        self.assertIsInstance(result, dict, detail)
        self.assertEqual(result["validation"]["local_contract"], "pass" if expected == 0 else "fail", detail)
        if expected == 0:
            self.assertEqual(result["validation"]["overall"], "unverified", detail)
        else:
            self.assertTrue(any(item.get("blocking") for item in result["diagnostics"]), detail)
            self.assertNotIn("state", result, "A rejected command must not return an acceptable state")
        return result

    def check_proposal(self, proposal, request, expected=0):
        return self.cli("check", self.write("proposal.json", proposal),
                        "--request", self.write("request.json", request), expected=expected)

    def accept(self, state=None, batch=None, requests=None, expected=0):
        if state is None:
            state = self.fixture("state-empty.json")
        if batch is None:
            batch = self.fixture("proposal-batch.json")
        if requests is None:
            requests = self.fixture("requests.json")
        return self.cli("accept", self.write("state.json", state), self.write("batch.json", batch),
                        "--requests", self.write("requests.json", requests), expected=expected)

    def standalone(self, number):
        return (self.fixture(f"request-standalone-m6-{number}.json"),
                self.fixture(f"proposal-standalone-m6-{number}.json"))

    def test_four_children_route_and_check_without_running_siblings(self):
        for number, partition in enumerate(PARTITIONS, 1):
            with self.subTest(module=f"M6.{number}"):
                request, proposal = self.standalone(number)
                routed = self.cli("route", self.write("request.json", request))
                self.assertEqual([r["module_id"] for r in routed["routes"]], [f"M6.{number}"])
                self.assertEqual(routed["routes"][0]["write_scope"], f"/content/{partition}")
                self.assertEqual(routed["invocation"], "not_invoked")
                self.check_proposal(proposal, request)

    def test_parent_accepts_all_partitions_as_one_unverified_draft(self):
        parent = self.cli("route", self.work / "assets/request-m6.json")
        self.assertEqual(parent["invocation"], "not_invoked")
        batch = self.fixture("proposal-batch.json")
        result = self.accept(batch=batch)
        state = result["state"]
        self.assertEqual(state["version"], 1)
        self.assertEqual(state["status"], "draft")
        self.assertEqual(set(state["accepted_proposals"]), {p["proposal_id"] for p in batch["proposals"]})
        for proposal in batch["proposals"]:
            for partition, content in proposal["changes"].items():
                self.assertEqual(state["content"][partition], content)
        self.cli("check", self.write("accepted.json", state))

    def test_sources_and_readonly_context_must_match_actual_request(self):
        for field in ("sources", "context"):
            with self.subTest(field=field):
                request, proposal = self.standalone(2)
                if field == "sources":
                    proposal["sources"]["brief"]["excerpt"] = "A different claimed original requirement."
                else:
                    proposal["context"]["vocal_brief"] = "Replace the actual request with another task."
                self.check_proposal(proposal, request, expected=1)

    def test_original_words_and_punctuation_cannot_be_changed_or_renamed_away(self):
        for mutation in ("punctuation", "event_id"):
            with self.subTest(mutation=mutation):
                request, proposal = self.standalone(2)
                items = proposal["changes"]["vocal_events"]["items"]
                if mutation == "punctuation":
                    items["lineA"]["original_text"] = "Keep this line exactly!"
                    items["lineA"]["approved_text"] = "Keep this line exactly!"
                else:
                    items["lineB"] = items.pop("lineA")
                    items["lineB"]["vocal_event_id"] = "lineB"
                self.check_proposal(proposal, request, expected=1)

    def approved_revision(self):
        request, proposal = self.standalone(2)
        revised = "Keep the revised line, exactly!"
        request["inputs"]["vocal_brief"] = "Retain the original separately and use the explicitly approved revision."
        request["inputs"]["approved_vocal_texts"] = {"lineA": revised}
        request["sources"]["approval"] = {
            "kind": "user_requirement", "locator": "synthetic-design-fixture://m6/approved-revision",
            "version": "1", "excerpt": f"The user explicitly approves this replacement: {revised}",
        }
        proposal["sources"] = deepcopy(request["sources"])
        proposal["context"] = deepcopy(request["inputs"])
        event = proposal["changes"]["vocal_events"]["items"]["lineA"]
        event["approved_text"] = revised
        event["rewrite_approval"] = {"state": "known", "value": True, "source_refs": ["approval"]}
        return request, proposal

    def test_rewrite_needs_actual_approved_text_and_true_approval(self):
        for mutation in ("false_approval", "missing_requested_approval", "different_approved_text"):
            with self.subTest(mutation=mutation):
                request, proposal = self.approved_revision()
                event = proposal["changes"]["vocal_events"]["items"]["lineA"]
                if mutation == "false_approval":
                    event["rewrite_approval"]["value"] = False
                elif mutation == "missing_requested_approval":
                    del request["inputs"]["approved_vocal_texts"]
                    proposal["context"] = deepcopy(request["inputs"])
                else:
                    event["approved_text"] = "A revision the user did not approve."
                self.check_proposal(proposal, request, expected=1)

    def test_explicitly_approved_revision_preserves_separate_original(self):
        request, proposal = self.approved_revision()
        original = request["inputs"]["vocal_texts"]["lineA"]
        self.check_proposal(proposal, request)
        event = proposal["changes"]["vocal_events"]["items"]["lineA"]
        self.assertEqual(event["original_text"], original)
        self.assertEqual(event["approved_text"], request["inputs"]["approved_vocal_texts"]["lineA"])
        self.assertNotEqual(event["original_text"], event["approved_text"])

    def test_registered_audio_identity_and_version_cannot_be_substituted(self):
        for field, value in (("asset_id", "unregisteredAudio"), ("asset_version", "2")):
            with self.subTest(field=field):
                request, proposal = self.standalone(3)
                proposal["changes"]["music"]["items"]["musicA"]["audio_selection"]["asset"][field] = value
                self.check_proposal(proposal, request, expected=1)

    def full_copy_plan(self):
        request, proposal = self.standalone(3)
        request["inputs"]["music_brief"] = "Use this complete source as the only final audio, with no new layers."
        request["sources"]["brief"]["excerpt"] = request["inputs"]["music_brief"]
        proposal["sources"] = deepcopy(request["sources"])
        proposal["context"] = deepcopy(request["inputs"])
        music = proposal["changes"]["music"]["items"]["musicA"]
        music["use_strategy"] = "fully_copy"
        music["additional_audio"] = "no"
        music["music_requirement"]["value"] = request["inputs"]["music_brief"]
        return request, proposal

    def test_full_copy_is_valid_alone_but_rejects_new_vocal_or_effect_layers(self):
        request, proposal = self.full_copy_plan()
        self.check_proposal(proposal, request)
        batch = self.fixture("proposal-batch.json")
        music = batch["proposals"][2]["changes"]["music"]["items"]["musicA"]
        music["use_strategy"] = "fully_copy"
        music["additional_audio"] = "no"
        # The other partitions still contain an independently generated voice and footstep.
        self.accept(batch=batch, expected=1)

    def test_full_copy_cannot_hide_a_partial_source_window(self):
        request, proposal = self.full_copy_plan()
        music = proposal["changes"]["music"]["items"]["musicA"]
        music["audio_selection"]["window"]["end_seconds"] = 6
        self.check_proposal(proposal, request, expected=1)

    def lyric_cue(self):
        request, proposal = self.standalone(2)
        source = self.fixture("proposal-m6-1.json")["changes"]["sources"]["items"]["speakerA"]
        source["sound_source_id"] = "bgmA"
        source["source_kind"] = "bgm_audio"
        source["subject_ref"] = {"state": "not_applicable", "reason": "This is a background track, not a visible performer."}
        source["voice_ref"] = {"state": "not_applicable", "reason": "No independent character voice is assigned."}
        source["description"]["value"] = "The supplied words are a cue within a reused background track."
        request["inputs"]["vocal_brief"] = "Keep these words as a track cue without creating a separate singer."
        request["inputs"]["source_context"] = {"items": {"bgmA": source}}
        proposal["context"] = deepcopy(request["inputs"])
        event = proposal["changes"]["vocal_events"]["items"]["lineA"]
        event["event_kind"] = "lyric_semantic"
        event["source_ref"] = {"kind": "internal", "id": "bgmA"}
        event["lip_sync"] = "not_required"
        event["audio_origin"] = "within_registered_audio"
        event["track_ref"] = {"state": "unknown", "reason": "The exact track binding remains to be supplied."}
        return request, proposal

    def test_lyric_cue_does_not_create_lip_sync_or_a_physical_speaker(self):
        request, proposal = self.lyric_cue()
        self.check_proposal(proposal, request)
        changed = deepcopy(proposal)
        changed["changes"]["vocal_events"]["items"]["lineA"]["lip_sync"] = "required"
        self.check_proposal(changed, request, expected=1)
        wrong_request, wrong_proposal = self.lyric_cue()
        wrong_request["inputs"]["source_context"]["items"]["bgmA"]["source_kind"] = "speaker"
        wrong_proposal["context"] = deepcopy(wrong_request["inputs"])
        self.check_proposal(wrong_proposal, wrong_request, expected=1)

    def test_unknown_and_not_applicable_keep_distinct_meanings(self):
        state = self.accept()["state"]
        self.assertEqual(state["content"]["sources"]["items"]["speakerA"]["voice_ref"]["state"], "unknown")
        self.assertEqual(state["content"]["vocal_events"]["items"]["lineA"]["track_ref"]["state"], "not_applicable")
        request, _ = self.standalone(1)
        request["inputs"]["source_brief"] = {"state": "unknown", "reason": "The requested binding has not been provided."}
        result = self.cli("route", self.write("request.json", request))
        self.assertEqual(result["route_status"], "ready_with_unverified_inputs")
        request["inputs"]["source_brief"] = {"state": "not_applicable", "reason": "Treat the missing required task as absent."}
        self.cli("route", self.write("request.json", request), expected=1)

    def test_missing_verbal_text_is_unknown_not_inapplicable(self):
        request, proposal = self.standalone(2)
        request["inputs"].pop("vocal_texts", None)
        proposal["context"] = deepcopy(request["inputs"])
        event = proposal["changes"]["vocal_events"]["items"]["lineA"]
        unknown = {"state": "unknown", "reason": "The dialogue words have not been provided."}
        event["original_text"] = deepcopy(unknown)
        event["approved_text"] = deepcopy(unknown)
        self.check_proposal(proposal, request)
        for field in ("original_text", "approved_text"):
            with self.subTest(field=field):
                changed = deepcopy(proposal)
                changed["changes"]["vocal_events"]["items"]["lineA"][field] = {
                    "state": "not_applicable", "reason": "Missing spoken words treated as inapplicable."}
                self.check_proposal(changed, request, expected=1)
        nonverbal = deepcopy(proposal)
        event = nonverbal["changes"]["vocal_events"]["items"]["lineA"]
        event["event_kind"] = "nonverbal"
        event["original_text"] = {"state": "not_applicable", "reason": "A wordless breath has no dialogue."}
        event["approved_text"] = deepcopy(event["original_text"])
        self.check_proposal(nonverbal, request)

    def test_stale_base_version_cannot_be_used_for_a_new_batch(self):
        accepted = self.accept()["state"]
        batch = self.fixture("proposal-batch.json")
        requests = self.fixture("requests.json")
        batch["batch_id"] = "stale_new_batch"
        for proposal, request in zip(batch["proposals"], requests):
            proposal["proposal_id"] += "_new"
            request["request_id"] += "_new"
            proposal["source_request_id"] = request["request_id"]
        self.accept(state=accepted, batch=batch, requests=requests, expected=1)

    def test_same_proposal_id_with_changed_content_is_not_a_retry(self):
        accepted = self.accept()["state"]
        batch = self.fixture("proposal-batch.json")
        batch["proposals"][1]["changes"]["vocal_events"]["items"]["lineA"]["delivery"]["value"] = "Whisper instead."
        self.accept(state=accepted, batch=batch, expected=1)

    def test_exact_retry_returns_the_entire_state_unchanged(self):
        accepted = self.accept()["state"]
        replayed = self.accept(state=accepted)["state"]
        self.assertEqual(replayed, accepted)
        self.assertEqual(replayed["version"], 1)

    def test_retry_still_checks_the_actual_original_requests(self):
        accepted = self.accept()["state"]
        requests = self.fixture("requests.json")
        requests[1]["inputs"]["vocal_texts"]["lineA"] = "A changed original request."
        self.accept(state=accepted, requests=requests, expected=1)

    def test_failed_batch_is_atomic_and_does_not_modify_any_inputs(self):
        batch = self.fixture("proposal-batch.json")
        batch["proposals"][-1]["changes"]["effects"]["items"]["stepA"]["action_ref"] = {
            "state": "not_applicable", "reason": "Deliberately invalid for an action sound.",
        }
        paths = [self.write("state.json", self.fixture("state-empty.json")),
                 self.write("batch.json", batch), self.write("requests.json", self.fixture("requests.json"))]
        before = {path: path.read_bytes() for path in paths}
        self.cli("accept", paths[0], paths[1], "--requests", paths[2], expected=1)
        self.assertEqual({path: path.read_bytes() for path in paths}, before)
        accepted = self.accept()["state"]
        self.assertEqual(accepted["version"], 1)
        self.assertEqual(len(accepted["accepted_proposals"]), 4)

    def test_child_cannot_write_a_sibling_partition(self):
        request, proposal = self.standalone(1)
        proposal["changes"]["music"] = self.fixture("proposal-m6-3.json")["changes"]["music"]
        self.check_proposal(proposal, request, expected=1)

    def cross_shot_batch(self, permitted):
        batch = self.fixture("proposal-batch.json")
        requests = self.fixture("requests.json")
        shots = ["shot1", "shot2"] if permitted else ["shot1"]
        batch["proposals"][0]["changes"]["sources"]["items"]["speakerA"]["applies_to_shots"] = shots[:]
        batch["proposals"][2]["changes"]["music"]["items"]["musicA"]["applies_to_shots"] = shots[:]
        for request, proposal in zip(requests, batch["proposals"]):
            context = request["inputs"].get("source_context", {})
            if "items" in context:
                context["items"]["speakerA"]["applies_to_shots"] = shots[:]
            proposal["context"] = deepcopy(request["inputs"])
        event = batch["proposals"][1]["changes"]["vocal_events"]["items"]["lineA"]
        event["shot_id"] = "shot2"
        event["audio_origin"] = "within_registered_audio"
        event["track_ref"] = {"kind": "internal", "id": "musicA"}
        event["continuity"] = {
            "state": "known", "value": "The same registered voice and audio track continue into Shot 2.",
            "source_refs": ["brief"],
        }
        return batch, requests

    def test_same_source_and_track_can_continue_across_permitted_shots(self):
        batch, requests = self.cross_shot_batch(permitted=True)
        state = self.accept(batch=batch, requests=requests)["state"]
        self.assertEqual(set(state["content"]["sources"]["items"]), {"speakerA"})
        self.assertEqual(set(state["content"]["music"]["items"]), {"musicA"})
        event = state["content"]["vocal_events"]["items"]["lineA"]
        self.assertEqual((event["shot_id"], event["source_ref"]["id"], event["track_ref"]["id"]),
                         ("shot2", "speakerA", "musicA"))

    def test_cross_shot_reference_outside_declared_scope_is_rejected(self):
        batch, requests = self.cross_shot_batch(permitted=False)
        self.accept(batch=batch, requests=requests, expected=1)

    def test_impact_invalidates_only_registered_intersecting_consumers(self):
        before = self.accept()["state"]
        before["consumers"] = {
            "voice_timing": {"module_id": "M7", "result_version": 1, "source_state_version": 1,
                             "read_paths": ["/content/vocal_events/items/lineA"], "status": "current"},
            "music_edit": {"module_id": "M9", "result_version": 1, "source_state_version": 1,
                           "read_paths": ["/content/music"], "status": "current"},
            "display_reader": {"module_id": "M12", "result_version": 1, "source_state_version": 1,
                               "read_paths": ["/display/title"], "status": "current"},
        }
        for mutation, expected in (("voice", {"voice_timing"}), ("display", {"display_reader"}), ("metadata", set())):
            with self.subTest(mutation=mutation):
                after = deepcopy(before)
                after["version"] += 1
                if mutation == "voice":
                    after["content"]["vocal_events"]["items"]["lineA"]["delivery"]["value"] = "Speak more quietly."
                elif mutation == "display":
                    after["display"]["title"] = "Only the display title changed"
                result = self.cli("impact", self.write("before.json", before), self.write("after.json", after))
                self.assertEqual(set(result["impact"]["stale_consumers"]), expected)


if __name__ == "__main__":
    unittest.main()
