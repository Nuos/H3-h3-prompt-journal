"""Behavioral regressions for M2 provenance, permissions and independent use.

Run from the repository root:
  python -m unittest discover -s docs/h3skill/tests/m2 -p 'test_*.py' -v
Fixtures are controlled projections of case text, never inspected media.
"""

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[2] / "h3-asset-reference"
SCRIPT = SKILL / "scripts/m2_contract.py"
SPEC = importlib.util.spec_from_file_location("m2_contract_under_test", SCRIPT)
M2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M2)
SCHEMA = json.loads((SKILL / "references/contracts.json").read_text())


def fixture(name):
    return json.loads((SKILL / "assets" / name).read_text())


def inspect(value):
    check = M2.Check(SCHEMA["$defs"])
    check.artifact(value)
    return check


def codes(check):
    return {item["code"] for item in check.diagnostics}


def accepted():
    check = M2.Check(SCHEMA["$defs"])
    value = M2.accept(check, fixture("state-empty.json"), fixture("proposal-batch.json"))
    assert value is not None, check.diagnostics
    return value


def permission_state():
    value = accepted()
    return value, value["content"]["reference_map"]["permissions"]


def add_conflicting_source(value):
    rules = value["content"]["reference_map"]["permissions"]
    rules["PERM-BODY-ID"] = copy.deepcopy(rules["PERM-FACE-ID"])
    rules["PERM-BODY-ID"]["binding_id"] = "BIND-BODY"
    return rules


def add_decision(value, strategy="select", selected=None):
    value["content"]["reference_map"]["decisions"]["DECISION-ID"] = {
        "permission_ids": ["PERM-FACE-ID", "PERM-BODY-ID"], "strategy": strategy,
        "selected_permission_ids": selected or ["PERM-FACE-ID"],
        "reason": "Controlled request explicitly resolves these candidate sources.",
        "authority_refs": ["SRC-EXAMPLE-REQUEST"], "source_refs": ["SRC-EXAMPLE-REQUEST"],
    }


class M2BehaviorTests(unittest.TestCase):
    def assert_bad(self, value, code):
        result = inspect(value)
        self.assertTrue(result.failed, result.diagnostics)
        self.assertIn(code, codes(result), result.diagnostics)

    def cli(self, args, inputs=None, skill=SKILL):
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for index, value in enumerate(inputs or []):
                path = Path(tmp) / f"input-{index}.json"
                path.write_text(json.dumps(value, ensure_ascii=False))
                paths.append(str(path))
            expanded = [paths[int(arg[1:])] if arg.startswith("@") else str(arg) for arg in args]
            before = [Path(path).read_bytes() for path in paths]
            process = subprocess.run([sys.executable, str(skill / "scripts/m2_contract.py"), *expanded],
                                     capture_output=True, text=True, timeout=20, cwd=tmp)
            self.assertEqual(before, [Path(path).read_bytes() for path in paths], "CLI modified its inputs")
            self.assertNotIn("Traceback", process.stderr)
            return process, json.loads(process.stdout)

    def test_each_public_node_routes_without_running_upstream(self):
        for target in ("m2", "m2-1", "m2-2", "m2-3"):
            with self.subTest(target=target):
                process, result = self.cli(["route", "@0"], [fixture(f"request-{target}.json")])
                self.assertEqual(process.returncode, 0)
                self.assertEqual(result["dispatch"]["semantic_execution"], "not_started")
                self.assertEqual(result["audit"]["semantic"], "unverified")

    def test_each_child_accepts_compatible_external_projection(self):
        for child in ("m2-1", "m2-2", "m2-3"):
            with self.subTest(child=child):
                process, result = self.cli(["check", "@0", "--request", "@1"],
                                           [fixture(f"proposal-{child}.json"), fixture(f"request-{child}.json")])
                self.assertEqual(process.returncode, 0, result)
                self.assertTrue(result["request_match_checked"])

    def test_batch_acceptance_preserves_pending_media_and_exact_version(self):
        process, result = self.cli(["accept", "@0", "@1"], [fixture("state-empty.json"), fixture("proposal-batch.json")])
        self.assertEqual(process.returncode, 0)
        self.assertEqual(result["outcome"], "accepted_draft")
        self.assertEqual(result["state"]["version"], 1)
        self.assertEqual(result["state"]["status"], "draft")
        self.assertEqual(len(result["state"]["accepted_proposals"]), 3)
        self.assertTrue(all(a["availability"] == "pending" for a in result["state"]["content"]["asset_registry"].values()))
        self.assertEqual(result["audit"], {"deterministic": "pass", "semantic": "unverified", "media": "unverified", "overall": "unverified"})

    def test_portable_directory_has_no_sibling_runtime_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "isolated-skill"
            shutil.copytree(SKILL, copied, ignore=shutil.ignore_patterns("__pycache__"))
            process, result = self.cli(["accept", str(copied / "assets/state-empty.json"), str(copied / "assets/proposal-batch.json")], skill=copied)
            self.assertEqual(process.returncode, 0, result)

    def test_unknown_input_remains_explicit_without_global_default(self):
        request = fixture("request-m2-1.json")
        request["inputs"]["material_brief"] = {"state": "unknown", "reason": "No input was provided."}
        check = inspect(request)
        self.assertFalse(check.failed)
        self.assertIn("unknown_input", codes(check))

    def test_missing_required_projection_is_not_implicit_empty_input(self):
        request = fixture("request-m2-2.json")
        request["inputs"].pop("asset_context")
        self.assert_bad(request, "missing_projected_input")

    def test_extra_global_projection_is_rejected_for_local_child(self):
        request = fixture("request-m2-1.json")
        request["inputs"]["entity_context"] = {"entities": {}, "bindings": {}}
        self.assert_bad(request, "unrequested_projection")

    def test_empty_source_map_is_not_valid_request_evidence(self):
        request = fixture("request-m2-1.json")
        request["sources"] = {}
        self.assert_bad(request, "invalid_shape")

    def test_backend_labels_cannot_be_stable_entity_ids(self):
        value = accepted()
        value["content"]["entity_registry"]["entities"]["<Subject 1>"] = value["content"]["entity_registry"]["entities"].pop("ENTITY-PERFORMER")
        self.assert_bad(value, "invalid_shape")

    def test_author_claim_cannot_be_promoted_to_observed_media(self):
        value = accepted()
        asset = value["content"]["asset_registry"]["ASSET-FACE"]
        asset.update(observation_state="observed", observation_scope="whole image")
        self.assert_bad(value, "observation_is_not_media_evidence")

    def test_external_observation_record_does_not_make_cli_media_auditor(self):
        value = accepted()
        value["sources"]["OBS-1"] = {"kind": "media_observation", "locator": "external-observer:record-1", "version": "1", "excerpt": "Controlled example of a supplied observation record; this test did not inspect media."}
        asset = value["content"]["asset_registry"]["ASSET-FACE"]
        asset.update(observation_state="observed", observation_refs=["OBS-1"], observation_scope="reported face crop")
        process, result = self.cli(["check", "@0"], [value])
        self.assertEqual(process.returncode, 0)
        self.assertEqual(result["audit"]["media"], "unverified")

    def test_accessible_and_pending_is_inconsistent(self):
        value = accepted()
        value["content"]["asset_registry"]["ASSET-FACE"]["access_state"] = "accessible"
        self.assert_bad(value, "access_availability_conflict")

    def test_image_does_not_declare_an_audio_channel(self):
        value = accepted()
        value["content"]["asset_registry"]["ASSET-FACE"]["channels"].append("audio")
        self.assert_bad(value, "channel_media_mismatch")

    def test_asset_reference_and_entity_reference_must_resolve(self):
        for field, target, code in (("asset_id", "MISSING-ASSET", "unresolved_asset"), ("entity_id", "MISSING-ENTITY", "unresolved_entity")):
            with self.subTest(field=field):
                value = accepted()
                value["content"]["entity_registry"]["bindings"]["BIND-FACE"][field] = target
                self.assert_bad(value, code)

    def test_derived_asset_graph_cannot_form_a_cycle(self):
        value = accepted()
        assets = value["content"]["asset_registry"]
        assets["ASSET-FACE"]["derived_from"] = "ASSET-BODY-SCENE"
        assets["ASSET-BODY-SCENE"]["derived_from"] = "ASSET-FACE"
        self.assert_bad(value, "derivation_cycle")

    def test_video_audio_is_not_implicitly_available(self):
        value = accepted()
        asset = value["content"]["asset_registry"]["ASSET-MUSIC"]
        asset.update(media_type="video", channels=["visual"])
        self.assert_bad(value, "unavailable_channel")

    def test_declared_embedded_video_audio_stays_explicitly_unverified(self):
        value = accepted()
        assets = value["content"]["asset_registry"]
        assets["ASSET-MUSIC"].update(media_type="video", channels=["visual", "audio"])
        before = copy.deepcopy(value)
        check = inspect(value)
        self.assertFalse(check.failed, check.diagnostics)
        self.assertIn("embedded_audio_not_independent_input", codes(check))
        self.assertEqual(before, value)
        self.assertEqual(len(assets), 3)

    def test_shared_photo_requires_distinct_selectors_for_distinct_people(self):
        value = accepted()
        registry = value["content"]["entity_registry"]
        registry["entities"]["ENTITY-SECOND"] = copy.deepcopy(registry["entities"]["ENTITY-PERFORMER"])
        registry["bindings"]["BIND-SECOND"] = copy.deepcopy(registry["bindings"]["BIND-FACE"])
        registry["bindings"]["BIND-SECOND"]["entity_id"] = "ENTITY-SECOND"
        self.assert_bad(value, "ambiguous_shared_selector")
        registry["bindings"]["BIND-SECOND"]["source_selector"] = "Explicit second person on the right of the source image."
        self.assertFalse(inspect(value).failed)

    def test_explicitly_shared_identity_selection_can_be_declared(self):
        value = accepted()
        registry = value["content"]["entity_registry"]
        registry["entities"]["ENTITY-DOUBLE"] = copy.deepcopy(registry["entities"]["ENTITY-PERFORMER"])
        registry["bindings"]["BIND-DOUBLE"] = copy.deepcopy(registry["bindings"]["BIND-FACE"])
        registry["bindings"]["BIND-DOUBLE"]["entity_id"] = "ENTITY-DOUBLE"
        for bid in ("BIND-FACE", "BIND-DOUBLE"):
            registry["bindings"][bid]["shared_selection_reason"] = "Controlled user request intentionally duplicates one identity into two target entities."
        self.assertFalse(inspect(value).failed)

    def test_identity_reference_does_not_infer_first_frame_permission(self):
        value, rules = permission_state()
        self.assertFalse(inspect(value).failed)
        self.assertEqual(rules["PERM-FACE-FIRST"]["decision"], "forbid")

    def test_actual_first_frame_permission_conflicts_with_same_source_pose_denial(self):
        value, rules = permission_state()
        rules["PERM-FACE-FIRST"]["decision"] = "allow"
        self.assert_bad(value, "anchor_permission_conflict")

    def test_frame_anchor_needs_a_separate_image_asset(self):
        value, rules = permission_state()
        value["content"]["asset_registry"]["ASSET-FACE"]["media_type"] = "video"
        rules["PERM-FACE-FIRST"]["decision"] = "allow"
        self.assert_bad(value, "invalid_frame_anchor")

    def test_audio_attribute_cannot_use_visual_channel(self):
        value, rules = permission_state()
        rules["PERM-MUSIC"]["binding_id"] = "BIND-FACE"
        self.assert_bad(value, "permission_channel_mismatch")

    def test_permission_cannot_grant_an_unconfirmed_binding(self):
        value = accepted()
        value["content"]["entity_registry"]["bindings"]["BIND-FACE"]["state"] = "candidate"
        self.assert_bad(value, "permission_on_unconfirmed_binding")

    def test_case_text_is_evidence_not_target_authorization(self):
        value, rules = permission_state()
        rules["PERM-FACE-ID"]["authority_refs"] = ["SRC-CASE-019"]
        self.assert_bad(value, "not_an_authorization")

    def test_permission_needs_explicit_authority(self):
        value, rules = permission_state()
        rules["PERM-FACE-ID"]["authority_refs"] = []
        self.assert_bad(value, "permission_without_authority")

    def test_allow_for_one_source_and_forbid_for_another_is_valid(self):
        value, rules = permission_state()
        rules["PERM-FACE-POSE"]["decision"] = "allow"
        self.assertFalse(inspect(value).failed)

    def test_same_source_allow_and_forbid_overlap_is_rejected(self):
        value, rules = permission_state()
        rules["PERM-ID-DENY"] = copy.deepcopy(rules["PERM-FACE-ID"])
        rules["PERM-ID-DENY"]["decision"] = "forbid"
        self.assert_bad(value, "permission_conflict")

    def test_adjacent_half_open_time_scopes_do_not_overlap(self):
        value, rules = permission_state()
        rules["PERM-ID-DENY"] = copy.deepcopy(rules["PERM-FACE-ID"])
        rules["PERM-ID-DENY"]["decision"] = "forbid"
        for key, start, end in (("PERM-FACE-ID", 0, 1), ("PERM-ID-DENY", 1, 2)):
            rules[key]["scope"] = {"kind": "time", "domain": "work", "timeline_id": "WORK-TIME", "start_seconds": start, "end_seconds": end}
        self.assertFalse(inspect(value).failed)

    def test_cross_clock_overlap_is_unknown_without_a_mapping(self):
        value, rules = permission_state()
        rules["PERM-ID-DENY"] = copy.deepcopy(rules["PERM-FACE-ID"])
        rules["PERM-ID-DENY"]["decision"] = "forbid"
        for key, domain in (("PERM-FACE-ID", "work"), ("PERM-ID-DENY", "generation")):
            rules[key]["scope"] = {"kind": "time", "domain": domain, "timeline_id": "T1", "start_seconds": 0, "end_seconds": 1}
        check = inspect(value)
        self.assertFalse(check.failed)
        self.assertIn("scope_overlap_unresolved", codes(check))

    def test_unknown_scope_does_not_expand_to_work(self):
        value, rules = permission_state()
        rules["PERM-FACE-ID"]["scope"] = {"kind": "unknown", "reason": "Shot assignment has not been provided."}
        check = inspect(value)
        self.assertFalse(check.failed)
        self.assertIn("unknown_scope", codes(check))
        self.assertEqual(rules["PERM-FACE-ID"]["scope"]["kind"], "unknown")

    def test_competing_sources_require_an_explicit_decision(self):
        value = accepted()
        add_conflicting_source(value)
        self.assert_bad(value, "competing_reference_sources")

    def test_explicit_source_selection_is_accepted(self):
        value = accepted()
        add_conflicting_source(value)
        add_decision(value)
        self.assertFalse(inspect(value).failed)

    def test_multiangle_reference_combination_is_supported(self):
        value = accepted()
        add_conflicting_source(value)
        add_decision(value, "combine", ["PERM-FACE-ID", "PERM-BODY-ID"])
        self.assertFalse(inspect(value).failed)

    def test_combination_cannot_erase_allow_forbid_contradiction(self):
        value = accepted()
        rules = add_conflicting_source(value)
        rules["PERM-BODY-ID"].update(binding_id="BIND-FACE", decision="forbid")
        add_decision(value, "combine", ["PERM-FACE-ID", "PERM-BODY-ID"])
        self.assert_bad(value, "invalid_combination")

    def test_resolution_scope_cannot_silently_expand_or_change_entity(self):
        value = accepted()
        rules = add_conflicting_source(value)
        rules["PERM-BODY-ID"]["scope"] = {"kind": "shots", "shot_ids": ["SHOT-1"]}
        add_decision(value)
        self.assert_bad(value, "invalid_decision_scope")

    def test_audio_words_reference_can_coexist_with_signal_copy_forbidden(self):
        value, rules = permission_state()
        rules["PERM-MUSIC"]["use"] = "reference"
        rules["PERM-NO-SIGNAL"] = copy.deepcopy(rules["PERM-MUSIC"])
        rules["PERM-NO-SIGNAL"].update(use="copy", decision="forbid",
                                        reason="Controlled case: re-perform the words without copying their original signal.")
        check = inspect(value)
        self.assertFalse(check.failed, check.diagnostics)
        self.assertNotIn("permission_conflict", codes(check))

    def test_audio_same_use_allow_and_forbid_still_conflict(self):
        value, rules = permission_state()
        rules["PERM-NO-SIGNAL"] = copy.deepcopy(rules["PERM-MUSIC"])
        rules["PERM-NO-SIGNAL"]["decision"] = "forbid"
        self.assert_bad(value, "permission_conflict")

    def test_different_audio_sources_with_different_uses_are_not_automatic_competitors(self):
        value, rules = permission_state()
        assets = value["content"]["asset_registry"]
        bindings = value["content"]["entity_registry"]["bindings"]
        assets["ASSET-ALT-AUDIO"] = copy.deepcopy(assets["ASSET-MUSIC"])
        assets["ASSET-ALT-AUDIO"]["description"] = "Controlled second source for a distinct reference use."
        bindings["BIND-ALT-AUDIO"] = copy.deepcopy(bindings["BIND-MUSIC"])
        bindings["BIND-ALT-AUDIO"]["asset_id"] = "ASSET-ALT-AUDIO"
        rules["PERM-ALT-REFERENCE"] = copy.deepcopy(rules["PERM-MUSIC"])
        rules["PERM-ALT-REFERENCE"].update(binding_id="BIND-ALT-AUDIO", use="reference")
        check = inspect(value)
        self.assertFalse(check.failed, check.diagnostics)
        self.assertNotIn("competing_reference_sources", codes(check))
        rules["PERM-ALT-REFERENCE"]["use"] = "copy"
        self.assert_bad(value, "competing_reference_sources")

    def test_resolution_cannot_discard_distinct_use_permissions(self):
        value, rules = permission_state()
        rules["PERM-MUSIC"]["use"] = "reference"
        rules["PERM-NO-SIGNAL"] = copy.deepcopy(rules["PERM-MUSIC"])
        rules["PERM-NO-SIGNAL"].update(use="copy", decision="forbid")
        value["content"]["reference_map"]["decisions"]["DECISION-MIXED-USE"] = {
            "permission_ids": ["PERM-MUSIC", "PERM-NO-SIGNAL"], "strategy": "select",
            "selected_permission_ids": ["PERM-MUSIC"],
            "reason": "Invalid controlled selection would erase a separate signal-copy prohibition.",
            "authority_refs": ["SRC-EXAMPLE-REQUEST"], "source_refs": ["SRC-EXAMPLE-REQUEST"],
        }
        self.assert_bad(value, "invalid_decision_scope")

    def test_source_window_cannot_exceed_recorded_duration(self):
        value, rules = permission_state()
        value["content"]["asset_registry"]["ASSET-MUSIC"]["duration_seconds"] = 3.0
        rules["PERM-MUSIC"]["source_window"] = {"domain": "source", "unit": "seconds", "start_seconds": 0, "end_seconds": 4}
        self.assert_bad(value, "source_window_out_of_bounds")

    def test_source_wide_prohibition_applies_to_a_selected_subwindow(self):
        value, rules = permission_state()
        rules["PERM-NO-SIGNAL"] = copy.deepcopy(rules["PERM-MUSIC"])
        rules["PERM-NO-SIGNAL"]["decision"] = "forbid"
        rules["PERM-MUSIC"]["source_window"] = {
            "domain": "source", "unit": "seconds", "start_seconds": 1, "end_seconds": 2}
        self.assert_bad(value, "permission_conflict")

    def test_overlapping_source_windows_do_not_hide_same_use_contradiction(self):
        value, rules = permission_state()
        rules["PERM-NO-SIGNAL"] = copy.deepcopy(rules["PERM-MUSIC"])
        rules["PERM-NO-SIGNAL"]["decision"] = "forbid"
        for key, start, end in (("PERM-MUSIC", 1, 3), ("PERM-NO-SIGNAL", 2, 4)):
            rules[key]["source_window"] = {
                "domain": "source", "unit": "seconds", "start_seconds": start, "end_seconds": end}
        self.assert_bad(value, "permission_conflict")

    def test_disjoint_or_adjacent_source_windows_are_not_a_copy_contradiction(self):
        for start in (2, 3):
            with self.subTest(forbidden_start=start):
                value, rules = permission_state()
                rules["PERM-NO-SIGNAL"] = copy.deepcopy(rules["PERM-MUSIC"])
                rules["PERM-NO-SIGNAL"]["decision"] = "forbid"
                for key, begin, end in (("PERM-MUSIC", 0, 2), ("PERM-NO-SIGNAL", start, 4)):
                    rules[key]["source_window"] = {
                        "domain": "source", "unit": "seconds", "start_seconds": begin, "end_seconds": end}
                check = inspect(value)
                self.assertFalse(check.failed, check.diagnostics)
                self.assertNotIn("permission_conflict", codes(check))

    def test_boolean_or_negative_time_is_not_a_valid_measurement(self):
        for start in (True, -1):
            with self.subTest(start=start):
                value, rules = permission_state()
                rules["PERM-MUSIC"]["source_window"] = {"domain": "source", "unit": "seconds", "start_seconds": start, "end_seconds": 4}
                self.assert_bad(value, "invalid_shape")

    def test_stale_proposal_and_repeated_operation_do_not_get_reaccepted(self):
        check = M2.Check(SCHEMA["$defs"])
        self.assertIsNone(M2.accept(check, accepted(), fixture("proposal-m2-1.json")))
        self.assertIn("stale_base_version", codes(check))
        self.assertIn("already_accepted_proposal", codes(check))

    def test_foreign_work_and_unowned_partition_are_rejected(self):
        proposal = fixture("proposal-m2-1.json")
        proposal["work_id"] = "ANOTHER-WORK"
        check = M2.Check(SCHEMA["$defs"])
        self.assertIsNone(M2.accept(check, fixture("state-empty.json"), proposal))
        self.assertIn("work_mismatch", codes(check))
        proposal = fixture("proposal-m2-1.json")
        proposal["changes"]["reference_map"] = {"permissions": {}, "decisions": {}}
        self.assert_bad(proposal, "out_of_scope_write")

    def test_source_versions_are_not_silently_rewritten(self):
        state = accepted()
        proposal = fixture("proposal-m2-1.json")
        proposal.update(base_version=1, proposal_id="PROP-NEW")
        proposal["sources"]["SRC-CASE-019"]["version"] = "changed-in-place"
        check = M2.Check(SCHEMA["$defs"])
        self.assertIsNone(M2.accept(check, state, proposal))
        self.assertIn("source_redefinition", codes(check))

    def test_batch_prevents_multiple_writers_for_same_partition(self):
        batch = fixture("proposal-batch.json")
        duplicate = copy.deepcopy(batch["proposals"][0])
        duplicate["proposal_id"] = "PROP-DUPLICATE-WRITER"
        batch["proposals"].append(duplicate)
        self.assert_bad(batch, "partition_write_conflict")

    def test_parent_verifies_context_against_the_candidate_state(self):
        batch = fixture("proposal-batch.json")
        batch["proposals"][1]["context"]["asset_registry"]["ASSET-FACE"]["description"] = "Different unreviewed source revision."
        check = M2.Check(SCHEMA["$defs"])
        self.assertIsNone(M2.accept(check, fixture("state-empty.json"), batch))
        self.assertIn("context_version_mismatch", codes(check))

    def test_omitting_old_ids_is_not_authorized_deletion(self):
        state = accepted()
        proposal = fixture("proposal-m2-3.json")
        proposal.update(base_version=1, proposal_id="PROP-REMOVE")
        proposal["changes"]["reference_map"]["permissions"].pop("PERM-FACE-POSE")
        check = M2.Check(SCHEMA["$defs"])
        self.assertIsNone(M2.accept(check, state, proposal))
        self.assertIn("implicit_record_removal", codes(check))

    def test_foreign_blocking_issue_cannot_be_cleared_by_a_child(self):
        state = accepted()
        state["issues"].append({"issue_id": "ISSUE-USER", "owner": "user", "state": "open", "blocking": True, "description": "Unresolved user choice.", "source_refs": ["SRC-EXAMPLE-REQUEST"]})
        proposal = fixture("proposal-m2-1.json")
        proposal.update(base_version=1, proposal_id="PROP-ISSUE")
        proposal["resolutions"] = [{"issue_id": "ISSUE-USER", "reason": "Pretend resolved.", "source_refs": ["SRC-EXAMPLE-REQUEST"]}]
        check = M2.Check(SCHEMA["$defs"])
        self.assertIsNone(M2.accept(check, state, proposal))
        self.assertIn("out_of_scope_resolution", codes(check))
        self.assertEqual(state["issues"][0]["state"], "open")

    def test_request_projection_and_request_identity_are_checked(self):
        proposal = fixture("proposal-m2-2.json")
        request = fixture("request-m2-2.json")
        proposal["source_request_id"] = "REQ-OTHER"
        proposal["context"]["asset_registry"]["ASSET-FACE"]["description"] = "Changed context."
        check = M2.Check(SCHEMA["$defs"])
        M2.check_request_match(check, proposal, request)
        self.assertIn("request_mismatch", codes(check))
        self.assertIn("request_projection_mismatch", codes(check))

    def test_parent_request_checks_only_each_childs_declared_read_projections(self):
        request = fixture("request-m2-3.json")
        request["target"] = "M2"
        request["inputs"]["material_brief"] = "Controlled complete parent request with supplied asset and entity projections."
        request["inputs"]["binding_brief"] = "Use the confirmed supplied bindings."
        for child in ("m2-1", "m2-2", "m2-3"):
            with self.subTest(child=child):
                proposal = fixture(f"proposal-{child}.json")
                proposal["source_request_id"] = request["request_id"]
                check = M2.Check(SCHEMA["$defs"])
                M2.check_request_match(check, proposal, request)
                self.assertFalse(check.failed, check.diagnostics)
        proposal = fixture("proposal-m2-2.json")
        proposal["source_request_id"] = request["request_id"]
        proposal["context"]["asset_registry"]["ASSET-FACE"]["description"] = "Unauthorized change to a genuinely read projection."
        check = M2.Check(SCHEMA["$defs"])
        M2.check_request_match(check, proposal, request)
        self.assertIn("request_projection_mismatch", codes(check))

    def test_source_authority_cannot_drift_while_request_id_stays_the_same(self):
        request = fixture("request-m2-1.json")
        proposal = fixture("proposal-m2-1.json")
        proposal["sources"]["SRC-EXAMPLE-REQUEST"]["excerpt"] = "Forged broader authorization under the original source ID."
        process, result = self.cli(["check", "@0", "--request", "@1"], [proposal, request])
        self.assertEqual(process.returncode, 1)
        self.assertIn("request_source_redefinition", {item["code"] for item in result["diagnostics"]})

    def test_request_sources_are_preserved_but_new_evidence_can_be_added(self):
        request = fixture("request-m2-1.json")
        proposal = fixture("proposal-m2-1.json")
        proposal["sources"]["NEW-SOURCE"] = {"kind": "external_input", "locator": "controlled-example:supplement", "version": "1", "excerpt": "Additional evidence, not a redefinition of target authorization."}
        check = M2.Check(SCHEMA["$defs"])
        M2.check_request_match(check, proposal, request)
        self.assertFalse(check.failed)
        del proposal["sources"]["SRC-DESIGN"]
        check = M2.Check(SCHEMA["$defs"])
        M2.check_request_match(check, proposal, request)
        self.assertIn("request_source_omitted", codes(check))

    def test_precise_consumer_invalidation_ignores_unread_title(self):
        previous = accepted()
        previous["consumers"] = {"USE-FACE": {"module_id": "M4", "result_version": 1, "source_state_version": 1, "read_paths": ["/content/reference_map/permissions/PERM-FACE-ID"]}, "USE-SCENE": {"module_id": "M3", "result_version": 2, "source_state_version": 1, "read_paths": ["/content/entity_registry/entities/ENTITY-SCENE"]}}
        current = copy.deepcopy(previous)
        current["version"] = 2
        current["display"]["title"] = "Display-only title change."
        check = M2.Check(SCHEMA["$defs"])
        result = M2.impact(check, previous, current)
        self.assertEqual(result["consumers"]["USE-FACE"]["status"], "unchanged_dependencies")
        current["content"]["reference_map"]["permissions"]["PERM-FACE-ID"]["reason"] = "Changed declared reference purpose."
        check = M2.Check(SCHEMA["$defs"])
        result = M2.impact(check, previous, current)
        self.assertEqual(result["consumers"]["USE-FACE"]["status"], "stale")
        self.assertEqual(result["consumers"]["USE-SCENE"]["status"], "unchanged_dependencies")

    def test_existing_stale_consumer_does_not_regain_a_pass(self):
        previous = accepted()
        previous["consumers"] = {"OLD": {"module_id": "M4", "result_version": 1, "source_state_version": 0, "read_paths": ["/content/asset_registry/ASSET-FACE"]}}
        current = copy.deepcopy(previous)
        current["version"] = 2
        check = M2.Check(SCHEMA["$defs"])
        result = M2.impact(check, previous, current)
        self.assertEqual(result["consumers"]["OLD"]["status"], "stale")

    def test_malformed_nested_values_produce_diagnostics_not_tracebacks(self):
        proposal = fixture("proposal-m2-3.json")
        mutations = [None, [], 4, True, "invalid", {}]
        for bad in mutations:
            for field in ("changes", "context", "sources", "module_id"):
                with self.subTest(field=field, bad=bad):
                    value = copy.deepcopy(proposal)
                    value[field] = bad
                    self.assertTrue(inspect(value).failed)
        for bad in mutations:
            value = copy.deepcopy(proposal)
            value["changes"]["reference_map"]["permissions"]["PERM-FACE-ID"] = bad
            self.assertTrue(inspect(value).failed)

    def test_cli_rejects_duplicate_keys_nan_and_invalid_json(self):
        for text in ('{"kind":"M2State","kind":"M2Request"}', '{"value":NaN}', 'not JSON'):
            with self.subTest(text=text), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "broken.json"
                path.write_text(text)
                process = subprocess.run([sys.executable, str(SCRIPT), "check", str(path)], capture_output=True, text=True, timeout=20)
                self.assertEqual(process.returncode, 2)
                self.assertEqual(json.loads(process.stdout)["execution_status"], "input_error")
                self.assertNotIn("Traceback", process.stderr)

    def test_schema_and_named_shape_checks_agree_on_public_examples(self):
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("Optional development-only jsonschema is unavailable.")
        Draft202012Validator.check_schema(SCHEMA)
        validator = Draft202012Validator(SCHEMA)
        values = [fixture(path.name) for path in (SKILL / "assets").glob("*.json")]
        values.append(accepted())
        for value in values:
            with self.subTest(kind=value["kind"]):
                self.assertEqual(list(validator.iter_errors(value)), [])
                self.assertTrue(M2.Check(SCHEMA["$defs"]).shape(value))
        value = fixture("request-m2-1.json")
        value["sources"] = {}
        self.assertTrue(list(validator.iter_errors(value)))
        self.assertFalse(M2.Check(SCHEMA["$defs"]).shape(value))


if __name__ == "__main__":
    unittest.main()
