"""M4 public-boundary regression tests. All synthetic content is D design data."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1] / "h3-action-performance"
spec = importlib.util.spec_from_file_location("m4_contract", PACKAGE / "scripts/m4_contract.py")
m4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m4)
SCHEMA = json.loads((PACKAGE / "references/contracts.json").read_text(encoding="utf-8"))


def fixture(name):
    return json.loads((PACKAGE / "assets" / name).read_text(encoding="utf-8"))


class PublicContractTests(unittest.TestCase):
    def setUp(self):
        self.state = fixture("state-empty.json")
        self.batch = fixture("proposal-batch.json")
        self.requests = fixture("requests.json")

    def checked_accept(self, state=None, batch=None, requests=None):
        check = m4.Check(SCHEMA["$defs"])
        result = m4.accept(check, self.state if state is None else state,
                           self.batch if batch is None else batch,
                           self.requests if requests is None else requests)
        return check, result

    def assert_rejected(self, code, state=None, batch=None, requests=None):
        check, result = self.checked_accept(state, batch, requests)
        self.assertIsNone(result)
        self.assertIn(code, {d["code"] for d in check.diagnostics}, check.diagnostics)
        return check

    def accepted(self):
        check, result = self.checked_accept()
        self.assertFalse(check.failed, check.diagnostics)
        return result["state"]

    def sync_contexts(self):
        events = copy.deepcopy(self.batch["proposals"][0]["changes"]["events"])
        mechanics = copy.deepcopy(self.batch["proposals"][1]["changes"]["mechanics"])
        for index in (1, 2):
            self.requests[index]["inputs"]["event_context"] = copy.deepcopy(events)
        self.requests[2]["inputs"]["mechanics_context"] = mechanics
        for request, proposal in zip(self.requests, self.batch["proposals"]):
            proposal["context"] = copy.deepcopy(request["inputs"])

    def revise(self, version=1):
        self.batch["batch_id"] = "d_batch_revision"
        self.batch["base_version"] = version
        for request, proposal in zip(self.requests, self.batch["proposals"]):
            request["base_version"] = proposal["base_version"] = version
            request["request_id"] += "_rev"
            proposal["proposal_id"] += "_rev"
            proposal["source_request_id"] = request["request_id"]

    def cli(self, *args, root=PACKAGE):
        proc = subprocess.run([sys.executable, "-I", str(root / "scripts/m4_contract.py"), *map(str, args)],
                              cwd=root, text=True, capture_output=True, timeout=20)
        return proc, json.loads(proc.stdout)

    def test_three_children_independently_check(self):
        for request, proposal in zip(self.requests, self.batch["proposals"]):
            with self.subTest(module=proposal["module_id"]):
                check = m4.Check(SCHEMA["$defs"])
                self.assertTrue(check.proposal(proposal, request), check.diagnostics)

    def test_atomic_composition_preserves_inputs(self):
        original = copy.deepcopy((self.state, self.batch, self.requests))
        state = self.accepted()
        self.assertEqual(state["version"], 1)
        self.assertEqual(set(state["content"]), {"events", "mechanics", "outcomes"})
        self.assertEqual(len(state["accepted_proposals"]), 3)
        self.assertEqual((self.state, self.batch, self.requests), original)
        self.assertEqual(state["status"], "draft")

    def test_partial_event_acceptance_is_explicitly_unverified(self):
        self.batch["proposals"] = self.batch["proposals"][:1]
        check, result = self.checked_accept()
        self.assertIsNotNone(result)
        self.assertIn("coverage_incomplete", {d["code"] for d in check.diagnostics})

    def test_external_unknown_minimum_needs_no_sources(self):
        request = fixture("request-minimal-m4-2.json")
        check = m4.Check(SCHEMA["$defs"])
        self.assertTrue(check.request(request), check.diagnostics)
        self.assertEqual(request["sources"], {})
        self.assertIn("explicit_unknown", {d["code"] for d in check.diagnostics})

    def test_missing_minimum_is_not_silent_unknown(self):
        del self.requests[1]["inputs"]["mechanics_brief"]
        check = m4.Check(SCHEMA["$defs"])
        self.assertFalse(check.request(self.requests[1]))
        self.assertIn("minimum_input_missing", {d["code"] for d in check.diagnostics})

    def test_unknown_fact_is_allowed_without_fake_source(self):
        self.batch["proposals"][1]["changes"]["mechanics"]["items"]["mechanism_take"]["force"] = {"state": "unknown", "reason": "D: force was not supplied."}
        self.sync_contexts()
        check, result = self.checked_accept()
        self.assertIsNotNone(result, check.diagnostics)
        self.assertIn("explicit_unknown", {d["code"] for d in check.diagnostics})

    def test_expression_can_have_no_body_motion_or_contact(self):
        event = self.batch["proposals"][0]["changes"]["events"]["items"]["take_cup"]
        event["performance_kind"] = "expression"
        event["object_ids"] = []
        event["entry_state"] = {"state": "unknown", "reason": "D expression-only regression."}
        event["goal"] = {"state": "known", "value": "D fixture: visible brow tension.", "source_refs": ["fixture_d"]}
        mechanism = self.batch["proposals"][1]["changes"]["mechanics"]["items"]["mechanism_take"]
        for field in ("support", "force", "motion", "contact"):
            mechanism[field] = {"state": "not_applicable", "reason": "D fixture describes facial expression, without body translation or prop contact."}
        mechanism["process"] = {"state": "known", "steps": [{"state": "known", "value": "Brows draw together visibly.", "source_refs": ["fixture_d"]}]}
        self.batch["proposals"][2]["changes"]["outcomes"]["items"]["result_take"]["end_state"] = {"state": "unknown", "reason": "D expression state not tokenized."}
        self.sync_contexts()
        check, result = self.checked_accept()
        self.assertIsNotNone(result, check.diagnostics)

    def test_not_applicable_requires_reason(self):
        self.batch["proposals"][1]["changes"]["mechanics"]["items"]["mechanism_take"]["support"] = {"state": "not_applicable"}
        self.assert_rejected("contract_shape")

    def test_opaque_external_payload_does_not_become_protocol(self):
        request = self.requests[0]
        request["inputs"]["space_context"] = {"owner": "M3", "source_id": "fixture_d", "source_version": "D-1",
                                                 "values": {"state": "unknown", "source_refs": 3, "nested": {"state": "unknown"}}}
        check = m4.Check(SCHEMA["$defs"])
        self.assertTrue(check.request(request), check.diagnostics)

    def test_opaque_projection_payload_does_not_become_protocol(self):
        request = self.requests[0]
        request["inputs"]["readonly_projection"] = [{"path": "/sources", "source_version": 0,
                                                       "value": {"state": "unknown", "source_refs": 3}}]
        check = m4.Check(SCHEMA["$defs"])
        self.assertTrue(check.request(request), check.diagnostics)

    def test_large_integer_version_does_not_overflow(self):
        self.requests[0]["base_version"] = 10 ** 400
        check = m4.Check(SCHEMA["$defs"])
        self.assertTrue(check.request(self.requests[0]), check.diagnostics)

    def test_boolean_is_not_version(self):
        self.requests[0]["base_version"] = False
        check = m4.Check(SCHEMA["$defs"])
        self.assertFalse(check.request(self.requests[0]))

    def test_unsupported_contract_rejected(self):
        self.batch["contract_version"] = "2.0.0"
        self.assert_rejected("contract_shape")

    def test_original_requests_required(self):
        self.assert_rejected("original_request_required", requests=[])

    def test_actual_request_cannot_be_replaced_by_proposal_context(self):
        self.batch["proposals"][0]["context"]["action_brief"] = "D attacker changed the request."
        self.assert_rejected("request_fidelity")

    def test_proposal_cannot_invent_source(self):
        self.batch["proposals"][0]["sources"]["invented"] = copy.deepcopy(self.requests[0]["sources"]["fixture_d"])
        self.assert_rejected("request_fidelity")

    def test_unresolved_source_is_blocking(self):
        self.batch["proposals"][0]["changes"]["events"]["items"]["take_cup"]["source_refs"] = ["missing"]
        self.sync_contexts()
        self.assert_rejected("unresolved_source")

    def test_child_cannot_write_foreign_partition(self):
        self.batch["proposals"][0]["changes"] = copy.deepcopy(self.batch["proposals"][1]["changes"])
        self.assert_rejected("write_ownership")

    def test_no_absolute_schedule_or_authoritative_state_field(self):
        self.batch["proposals"][0]["changes"]["events"]["items"]["take_cup"]["start_seconds"] = 2
        self.assert_rejected("contract_shape")

    def test_child_target_must_match_original(self):
        self.requests[0]["target"] = "M4"
        self.assert_rejected("request_target")

    def test_readonly_events_cannot_be_installed_by_mechanics(self):
        self.batch["proposals"] = [self.batch["proposals"][1]]
        self.assert_rejected("readonly_conflict")

    def test_readonly_projection_is_checked_on_candidate(self):
        self.requests[0]["inputs"]["readonly_projection"] = [{"path": "/content/mechanics", "source_version": 0, "value": {"items": {}}}]
        self.batch["proposals"][0]["context"] = copy.deepcopy(self.requests[0]["inputs"])
        self.assert_rejected("readonly_conflict")

    def test_projection_version_and_json_pointer_are_precise(self):
        request = self.requests[0]
        request["inputs"]["readonly_projection"] = [{"path": "/content", "source_version": 2, "value": {}}]
        check = m4.Check(SCHEMA["$defs"])
        self.assertFalse(check.request(request))
        diag = next(d for d in check.diagnostics if d["code"] == "projection_version")
        self.assertEqual(diag["path"], "/inputs/readonly_projection/0")

    def test_stale_new_proposal_rejected(self):
        state = self.accepted()
        self.revise(version=0)
        self.assert_rejected("stale_base_version", state=state)

    def test_exact_replay_keeps_state_and_version(self):
        state = self.accepted()
        check, result = self.checked_accept(state=state)
        self.assertFalse(check.failed, check.diagnostics)
        self.assertEqual(result["acceptance"], "idempotent_replay")
        self.assertEqual(result["state"], state)

    def test_changed_reused_proposal_id_rejected(self):
        state = self.accepted()
        self.batch["proposals"][0]["changes"]["events"]["items"]["take_cup"]["goal"]["value"] += " altered"
        self.sync_contexts()
        self.assert_rejected("idempotency_conflict", state=state)

    def test_mixed_replay_and_new_proposal_rejected(self):
        state = self.accepted()
        self.batch["proposals"][0]["proposal_id"] += "_new"
        self.assert_rejected("mixed_replay", state=state)

    def test_duplicate_partition_writes_rejected(self):
        self.batch["proposals"].append(copy.deepcopy(self.batch["proposals"][0]))
        self.batch["proposals"][-1]["proposal_id"] += "_dup"
        self.assert_rejected("partition_conflict")

    def test_accepted_requirement_cannot_be_deleted(self):
        state = self.accepted()
        self.revise()
        self.batch["proposals"][0]["changes"]["events"]["requirements"] = {}
        self.sync_contexts()
        self.assert_rejected("accepted_record_deleted", state=state)

    def test_accepted_requirement_coverage_cannot_be_shrunk(self):
        state = self.accepted()
        self.revise()
        self.batch["proposals"][0]["changes"]["events"]["requirements"]["req_take_raise"]["event_ids"] = ["take_cup"]
        self.sync_contexts()
        self.assert_rejected("accepted_requirement_changed", state=state)

    def test_stable_prop_identity_cannot_be_repurposed(self):
        state = self.accepted()
        self.revise()
        self.batch["proposals"][0]["changes"]["events"]["entities"]["cup_1"]["label"] = "D different object"
        self.sync_contexts()
        self.assert_rejected("accepted_identity_changed", state=state)

    def test_source_id_cannot_be_rebound_after_acceptance(self):
        state = self.accepted()
        self.revise()
        for request, proposal in zip(self.requests, self.batch["proposals"]):
            request["sources"]["fixture_d"]["excerpt"] = "D replaced provenance"
            proposal["sources"] = copy.deepcopy(request["sources"])
        self.assert_rejected("source_collision", state=state)

    def test_event_dependency_cycle(self):
        self.batch["proposals"][0]["changes"]["events"]["items"]["take_cup"]["depends_on"] = ["raise_cup"]
        self.sync_contexts()
        self.assert_rejected("event_cycle")

    def test_dangling_event_dependency(self):
        self.batch["proposals"][0]["changes"]["events"]["items"]["take_cup"]["depends_on"] = ["missing"]
        self.sync_contexts()
        self.assert_rejected("dangling_dependency")

    def test_contact_requires_declared_participants(self):
        self.batch["proposals"][1]["changes"]["mechanics"]["items"]["mechanism_take"]["contact"]["participants"] = ["actor_a", "cup_renamed"]
        self.sync_contexts()
        self.assert_rejected("contact_participant")

    def test_result_inheritance_conflict(self):
        self.batch["proposals"][0]["changes"]["events"]["items"]["raise_cup"]["entry_state"]["values"]["cup_1"]["holder"] = "table_1"
        self.sync_contexts()
        self.assert_rejected("inheritance_conflict")

    def test_missing_inheritance_is_unverified(self):
        del self.batch["proposals"][0]["changes"]["events"]["items"]["raise_cup"]["entry_state"]["values"]["cup_1"]
        self.sync_contexts()
        check, result = self.checked_accept()
        self.assertIsNotNone(result, check.diagnostics)
        self.assertIn("inheritance_missing", {d["code"] for d in check.diagnostics})

    def test_next_event_requires_dependency_link(self):
        self.batch["proposals"][0]["changes"]["events"]["items"]["raise_cup"]["depends_on"] = []
        self.sync_contexts()
        self.assert_rejected("continuation_dependency")

    def test_terminal_action_segment_can_have_causal_dependents(self):
        self.batch["proposals"][2]["changes"]["outcomes"]["items"]["result_take"]["continuation"] = {"state": "terminal", "reason": "D first action segment ends; later events may still have a causal dependency."}
        check, result = self.checked_accept()
        self.assertIsNotNone(result, check.diagnostics)
        self.assertIn("dependency_state_not_inferred", {d["code"] for d in check.diagnostics})

    def test_another_actor_can_be_a_gaze_object(self):
        events = self.batch["proposals"][0]["changes"]["events"]
        events["entities"]["actor_b"] = {"kind": "actor", "label": "D gaze target", "source_refs": ["fixture_d"]}
        events["items"]["take_cup"]["object_ids"].append("actor_b")
        events["items"]["take_cup"]["performance_kind"] = "mixed"
        self.sync_contexts()
        check, result = self.checked_accept()
        self.assertIsNotNone(result, check.diagnostics)

    def test_nonadjacent_dependency_does_not_force_state_equality(self):
        events = self.batch["proposals"][0]["changes"]["events"]
        events["items"]["finish"] = copy.deepcopy(events["items"]["raise_cup"])
        events["items"]["finish"]["depends_on"] = ["take_cup", "raise_cup"]
        events["items"]["finish"]["entry_state"]["values"]["actor_a"]["hand"] = "resting_with_cup"
        events["requirements"]["req_take_raise"]["event_ids"].append("finish")
        mechanics = self.batch["proposals"][1]["changes"]["mechanics"]
        mechanics["items"]["mechanism_finish"] = copy.deepcopy(mechanics["items"]["mechanism_raise"])
        mechanics["items"]["mechanism_finish"]["event_id"] = "finish"
        outcomes = self.batch["proposals"][2]["changes"]["outcomes"]
        outcomes["items"]["result_raise"]["end_state"]["values"]["actor_a"]["hand"] = "resting_with_cup"
        outcomes["items"]["result_raise"]["continuation"] = {"state": "next", "event_ids": ["finish"]}
        events["items"]["finish"]["entry_state"]["values"]["cup_1"]["level"] = "chest"
        outcomes["items"]["result_finish"] = copy.deepcopy(outcomes["items"]["result_raise"])
        outcomes["items"]["result_finish"]["event_id"] = "finish"
        outcomes["items"]["result_finish"]["continuation"] = {"state": "terminal", "reason": "D final segment"}
        self.sync_contexts()
        check, result = self.checked_accept()
        self.assertIsNotNone(result, check.diagnostics)
        self.assertIn("dependency_state_not_inferred", {d["code"] for d in check.diagnostics})

    def test_m8_request_remains_proposal_and_owner_is_checked(self):
        change = self.batch["proposals"][2]["changes"]["outcomes"]["change_requests"]["state_raise"]
        self.assertEqual(change["request_kind"], "state_change_request")
        change["target_module"] = "M5"
        self.assert_rejected("handoff_owner")

    def test_open_blocker_rejects_entire_batch(self):
        self.batch["proposals"][0]["issues"] = [{"issue_id": "d_blocker", "owner": "M4.1", "status": "open", "severity": "blocking", "message": "D unresolved precondition", "source_refs": ["fixture_d"]}]
        self.assert_rejected("open_blocker")
        self.assertEqual(self.state["version"], 0)

    def test_owned_existing_issue_can_be_resolved(self):
        state = self.accepted()
        state["issues"]["d_old"] = {"issue_id": "d_old", "owner": "M4.1", "status": "open", "severity": "blocking", "message": "D review required", "source_refs": ["fixture_d"]}
        self.revise()
        self.batch["proposals"][0]["resolutions"] = [{"issue_id": "d_old", "rationale": "D original request now clarifies the precondition.", "source_refs": ["fixture_d"]}]
        check, result = self.checked_accept(state=state)
        self.assertIsNotNone(result, check.diagnostics)
        self.assertEqual(result["state"]["issues"]["d_old"]["status"], "resolved")

    def test_child_cannot_resolve_other_owner_issue(self):
        state = self.accepted()
        state["issues"]["d_old"] = {"issue_id": "d_old", "owner": "M4.2", "status": "open", "severity": "warning", "message": "D review required", "source_refs": ["fixture_d"]}
        self.revise()
        self.batch["proposals"][0]["resolutions"] = [{"issue_id": "d_old", "rationale": "D unauthorized resolution", "source_refs": ["fixture_d"]}]
        self.assert_rejected("resolution_ownership", state=state)

    def test_impact_tracks_declared_m9_m11_m12_readers(self):
        state = self.accepted()
        for module in ("M9", "M11", "M12"):
            state["consumers"][module] = {"module_id": module, "result_version": 1, "source_state_version": 1, "read_paths": ["/content/events"], "status": "current"}
        after = copy.deepcopy(state)
        after["content"]["events"]["items"]["take_cup"]["goal"]["value"] += " D revision"
        report = m4.impact(state, after)
        self.assertEqual(set(report["stale_consumers"]), {"M9", "M11", "M12"})
        check = m4.Check(SCHEMA["$defs"])
        self.assertTrue(check.state(state), check.diagnostics)

    def test_display_change_does_not_stale_data_consumer(self):
        state = self.accepted()
        state["consumers"]["reader"] = {"module_id": "M5", "result_version": 1, "source_state_version": 1, "read_paths": ["/content"], "status": "current"}
        after = copy.deepcopy(state)
        after["display"] = {"title": "D new display title"}
        self.assertFalse(m4.impact(state, after)["stale_consumers"])
        state["consumers"]["reader"]["status"] = "stale"
        self.assertIn("reader", m4.impact(state, after)["stale_consumers"])

    def test_duplicate_keys_and_non_finite_numbers_rejected(self):
        for text in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":1e999}'):
            with self.subTest(text=text), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "bad.json"
                path.write_text(text)
                with self.assertRaises(ValueError):
                    m4.load_json(path)

    def test_boolean_to_number_change_in_readonly_payload_is_rejected(self):
        self.requests[0]["inputs"]["space_context"] = {"owner": "M3", "source_id": "fixture_d", "source_version": "D-1", "values": {"opaque": True}}
        self.batch["proposals"][0]["context"] = copy.deepcopy(self.requests[0]["inputs"])
        self.batch["proposals"][0]["context"]["space_context"]["values"]["opaque"] = 1
        self.assert_rejected("request_fidelity")

    def test_handoff_ownership_checked_with_unknown_events(self):
        proposal = self.batch["proposals"][2]
        request = self.requests[2]
        request["inputs"]["event_context"] = {"state": "unknown", "reason": "D no event projection"}
        proposal["context"] = copy.deepcopy(request["inputs"])
        proposal["changes"]["outcomes"]["change_requests"]["state_raise"]["target_module"] = "M5"
        check = m4.Check(SCHEMA["$defs"])
        self.assertFalse(check.proposal(proposal, request))
        self.assertIn("handoff_owner", {d["code"] for d in check.diagnostics})

    def test_route_does_not_invoke_agent_and_check_never_certifies_media(self):
        proc, report = self.cli("route", "assets/request-m4-1.json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(report["invocation"], "not_invoked")
        self.assertEqual(report["validation"]["overall"], "unverified")
        self.assertIn("physical_feasibility", report["validation"]["unverified"])
        self.assertIn("media_observation", report["validation"]["unverified"])

    def test_cli_malformed_source_preserves_contract_diagnostic(self):
        request = self.requests[0]
        request["sources"]["fixture_d"] = None
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad-source.json"
            path.write_text(json.dumps(request), encoding="utf-8")
            proc, report = self.cli("route", path)
        self.assertEqual(proc.returncode, 1, report)
        self.assertEqual(report["execution"], "completed")
        self.assertIn("contract_shape", {d["code"] for d in report["diagnostics"]})

    def test_portable_copy_runs_without_repo_or_siblings(self):
        with tempfile.TemporaryDirectory() as directory:
            isolated = Path(directory) / "isolated-skill"
            shutil.copytree(PACKAGE, isolated)
            proc, report = self.cli("accept", "assets/state-empty.json", "assets/proposal-batch.json", "--requests", "assets/requests.json", root=isolated)
            self.assertEqual(proc.returncode, 0, (proc.stderr, report))
            self.assertEqual(report["state"]["version"], 1)
            self.assertEqual(report["trace"]["side_effects"], "none")
            self.assertFalse(list(isolated.rglob("__pycache__")))

    def test_asset_contracts_are_valid_json_schema_if_validator_available(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("Optional jsonschema absent; bundled standard-library validator is exercised above")
        jsonschema.Draft202012Validator.check_schema(SCHEMA)
        validator = jsonschema.Draft202012Validator(SCHEMA)
        for path in (PACKAGE / "assets").glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            values = data if isinstance(data, list) else [data]
            for value in values:
                if isinstance(value, dict) and value.get("kind") in ("M4Request", "M4Proposal", "M4ProposalBatch", "M4State"):
                    with self.subTest(file=path.name):
                        validator.validate(value)


if __name__ == "__main__":
    unittest.main()
