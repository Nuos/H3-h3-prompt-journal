"""M8 contract regressions. All media observations below are synthetic test doubles.

No test reads or claims a generated video, measured audio or real observation.
"""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
PACKAGE = Path(__file__).resolve().parents[2] / "h3-state-continuity"
sys.path.insert(0, str(PACKAGE / "scripts"))
spec = importlib.util.spec_from_file_location("m8_contract", PACKAGE / "scripts/m8_contract.py")
m8 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m8)


def fixture(name):
    return m8.load_json(PACKAGE / "assets" / (name + ".json"))


def fact(value):
    return {"state": "known", "value": value, "source_refs": ["design"]}


def context(owner, values):
    return {"owner": owner, "source_id": "design", "source_version": "1", "values": values}


def pair(n):
    return fixture("request-standalone-m8-" + str(n)), fixture("proposal-standalone-m8-" + str(n))


def synchronize(request, proposal):
    proposal["context"] = copy.deepcopy(request["inputs"])
    proposal["sources"] = copy.deepcopy(request["sources"])


def reconcile_handoff(request, proposal):
    """Generate a declared text fixture from an intentionally modified plan.

    This helper is only a test author, not an NLP extractor or production writer.
    """
    ledger = request["inputs"]["ledger_context"]["values"]
    handoff = proposal["changes"]["ContinuityHandoffs"]["items"]["handoff_contact"]
    docs = request["inputs"]["prompt_context"]["values"]["documents"]
    for side, endpoint, edge in (("from", "previous_prompt", "final"), ("to", "next_prompt", "initial")):
        state = ledger["states"][handoff[side + "_state"]]
        handoff["table"][side] = copy.deepcopy(state["attributes"])
        document = docs[handoff[endpoint]["document_id"]]
        declaration = document["declarations"][handoff[endpoint]["declaration_id"]]
        text = "中文测试设计声明：" + "；".join(f["value"] for f in state["attributes"].values() if f["state"] == "known") + "。"
        document["text"] = text
        declaration["attributes"] = copy.deepcopy(state["attributes"])
        declaration["spans"] = {a: {"start": text.index(f["value"]), "end": text.index(f["value"]) + len(f["value"]), "quote": f["value"]} for a, f in state["attributes"].items() if f["state"] == "known"}
    synchronize(request, proposal)


def boundary_variant(kind):
    request, proposal = pair(3)
    policy = request["inputs"]["policy_context"]["values"]["items"]["p_contact"]
    ledger = request["inputs"]["ledger_context"]["values"]
    policy["boundary_type"] = kind
    policy["invariants"] = ["person.identity"]
    policy["match_attributes"] = ["person.direction"] if kind == "match_cut" else []
    policy["allowed_changes"].append({"attribute": "scene.location", "reason": "显式设计许可", "source_refs": ["design"]})
    policy["cue"] = fact("同一主题转入下一地点" if kind == "montage" else "稍后抵达新地点")
    ledger["states"]["state_after"]["attributes"]["scene.location"] = fact("另一个石面场景")
    ledger["transitions"]["t_cut"]["changed_attributes"].append("scene.location")
    reconcile_handoff(request, proposal)
    return request, proposal


class ContractTests(unittest.TestCase):
    def checked(self, request, proposal, expected=None):
        check = m8.Check()
        check.proposal(proposal, request)
        codes = {d["code"] for d in check.diagnostics}
        if expected:
            self.assertTrue(check.failed, check.diagnostics)
            self.assertIn(expected, codes, check.diagnostics)
        else:
            self.assertFalse(check.failed, check.diagnostics)
        return check

    def accepted(self):
        state, batch, requests = fixture("state-empty"), fixture("proposal-batch"), fixture("requests")
        check = m8.Check()
        result = m8.accept(check, state, batch, requests)
        self.assertFalse(check.failed, check.diagnostics)
        self.assertIsNotNone(result)
        return result, state, batch, requests

    def test_three_standalone_children_and_routes(self):
        for n in (1, 2, 3):
            with self.subTest(module=n):
                self.checked(*pair(n))
                run = subprocess.run([sys.executable, "-B", str(PACKAGE / "scripts/m8_contract.py"), "route", str(PACKAGE / "assets" / ("request-standalone-m8-" + str(n) + ".json"))], capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                result = json.loads(run.stdout)
                self.assertEqual(result["invocation"], "not_invoked")
                self.assertEqual(result["routes"][0]["module_id"], "M8." + str(n))

    def test_accept_atomic_and_precise_invalidation(self):
        result, state, batch, requests = self.accepted()
        self.assertEqual(result["state"]["version"], 1)
        self.assertEqual(state, fixture("state-empty"))
        self.assertEqual(batch, fixture("proposal-batch"))
        self.assertEqual(requests, fixture("requests"))
        self.assertEqual(set(result["impact"]["stale_consumers"]), {"compiler", "editor"})
        self.assertEqual(result["state"]["consumers"]["title"]["status"], "current")

    def test_exact_replay_preserves_version(self):
        result, _, batch, requests = self.accepted()
        check = m8.Check()
        again = m8.accept(check, result["state"], batch, requests)
        self.assertFalse(check.failed, check.diagnostics)
        self.assertEqual(again["acceptance"], "idempotent_replay")
        self.assertEqual(again["state"], result["state"])

    def test_mutated_operation_id_rejected(self):
        result, _, batch, requests = self.accepted()
        requests[0]["inputs"]["policy_brief"] += " 改动"
        synchronize(requests[0], batch["proposals"][0])
        check = m8.Check()
        self.assertIsNone(m8.accept(check, result["state"], batch, requests))
        self.assertIn("idempotency_conflict", {d["code"] for d in check.diagnostics})

    def test_stale_base_rejected(self):
        result, _, batch, requests = self.accepted()
        for proposal in batch["proposals"]:
            proposal["proposal_id"] += "_new"
        check = m8.Check()
        self.assertIsNone(m8.accept(check, result["state"], batch, requests))
        self.assertIn("stale_base_version", {d["code"] for d in check.diagnostics})

    def test_source_id_cannot_rebind_on_new_revision(self):
        result, _, batch, requests = self.accepted()
        batch["base_version"] = 1
        for request, proposal in zip(requests, batch["proposals"]):
            request["base_version"] = proposal["base_version"] = 1
            request["sources"]["design"]["excerpt"] += " altered provenance"
            proposal["proposal_id"] += "_v2"
            synchronize(request, proposal)
        check = m8.Check()
        self.assertIsNone(m8.accept(check, result["state"], batch, requests))
        self.assertIn("source_collision", {d["code"] for d in check.diagnostics})

    def test_accepted_history_is_append_only(self):
        result, _, batch, requests = self.accepted()
        batch["base_version"] = 1
        for request, proposal in zip(requests, batch["proposals"]):
            request["base_version"] = proposal["base_version"] = 1
            proposal["proposal_id"] += "_v2"
            synchronize(request, proposal)
        # Removing a still-referenced chain is semantically possible as snapshots,
        # but must not erase an already accepted history record.
        batch["proposals"][1]["changes"]["StateLedger"]["chains"] = {}
        requests[2]["inputs"]["ledger_context"]["values"]["chains"] = {}
        synchronize(requests[2], batch["proposals"][2])
        check = m8.Check()
        self.assertIsNone(m8.accept(check, result["state"], batch, requests))
        self.assertIn("accepted_history_changed", {d["code"] for d in check.diagnostics})

    def test_missing_minimum_input_is_not_ready(self):
        request, proposal = pair(3)
        del request["inputs"]["prompt_context"]
        synchronize(request, proposal)
        self.checked(request, proposal, "missing_input")

    def test_parent_route_marks_missing_child_inputs(self):
        request, _ = pair(1)
        request["target"] = "M8"
        request["inputs"] = {"continuity_brief": "父级只声明目的"}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "parent.json"
            path.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
            proc = subprocess.run([sys.executable, "-B", str(PACKAGE / "scripts/m8_contract.py"), "route", str(path)], capture_output=True, text=True)
            result = json.loads(proc.stdout)
        self.assertEqual(proc.returncode, 0, result)
        self.assertEqual(result["route_status"], "requires_child_inputs")
        self.assertTrue(all(not x["call_ready"] and x["missing_inputs"] for x in result["routes"]))

    def test_original_request_required(self):
        request, proposal = pair(1)
        self.checked(None, proposal, "original_request_required")

    def test_proposal_cannot_forge_original_context(self):
        request, proposal = pair(3)
        proposal["context"]["handoff_brief"] = "forged replacement"
        self.checked(request, proposal, "request_fidelity")

    def test_proposal_cannot_forge_sources(self):
        request, proposal = pair(1)
        proposal["sources"]["design"]["excerpt"] = "forged provenance"
        self.checked(request, proposal, "request_fidelity")

    def test_owner_cannot_write_planned_ledger_from_m83(self):
        request, proposal = pair(3)
        proposal["changes"]["StateLedger"] = request["inputs"]["ledger_context"]["values"]
        self.checked(request, proposal, "write_scope")

    def test_missing_source_and_context_version(self):
        request, proposal = pair(2)
        request["inputs"]["policy_context"]["source_version"] = "99"
        synchronize(request, proposal)
        self.checked(request, proposal, "context_source_version")
        request, proposal = pair(2)
        proposal["changes"]["StateLedger"]["states"]["state_before"]["attributes"]["person.identity"]["source_refs"] = ["not_registered"]
        self.checked(request, proposal, "source_missing")

    def test_unknown_remains_unverified_and_never_zero(self):
        request, proposal = pair(3)
        request["inputs"]["ledger_context"]["values"]["states"]["state_after"]["attributes"]["person.holding"] = {"state": "unknown", "reason": "尚未确认持物"}
        reconcile_handoff(request, proposal)
        check = self.checked(request, proposal)
        self.assertIn("continuity_unverified", {d["code"] for d in check.diagnostics})
        proposal["changes"]["ContinuityHandoffs"]["items"]["handoff_contact"]["table"]["to"]["person.holding"] = 0
        self.checked(request, proposal, "schema")

    def test_hypothesis_cannot_be_known_or_authority(self):
        request, proposal = pair(2)
        request["sources"]["uncertain"] = {"kind": "hypothesis", "locator": "synthetic-test://unknown", "version": "1", "excerpt": "没有来源确认"}
        synchronize(request, proposal)
        proposal["changes"]["StateLedger"]["states"]["state_before"]["attributes"]["person.identity"]["source_refs"] = ["uncertain"]
        self.checked(request, proposal, "unconfirmed_fact")

    def test_identity_reference_does_not_authorize_pose(self):
        request, proposal = pair(2)
        proposal["changes"]["StateLedger"]["states"]["state_before"]["reference_uses"][0]["attributes"].append("person.support")
        self.checked(request, proposal, "identity_reference_pose")

    def test_policy_cannot_invent_m9_change_permission(self):
        request, proposal = pair(1)
        policy = proposal["changes"]["ContinuityPolicy"]["items"]["p_contact"]
        policy["allowed_changes"].append({"attribute": "person.holding", "reason": "伪造许可", "source_refs": ["design"]})
        policy["invariants"].remove("person.holding")
        self.checked(request, proposal, "change_permission_missing")

    def test_interval_n_plus_one_and_clock_unit(self):
        request, proposal = pair(2)
        ledger = proposal["changes"]["StateLedger"]
        ledger["chains"]["contact_chain"]["intervals"].pop()
        self.checked(request, proposal, "chain_interval_count")
        request, proposal = pair(2)
        proposal["changes"]["StateLedger"]["chains"]["contact_chain"]["intervals"][1]["unit"] = "frames"
        self.checked(request, proposal, "schema")

    def test_intervals_cannot_gap_overlap(self):
        request, proposal = pair(2)
        proposal["changes"]["StateLedger"]["chains"]["contact_chain"]["intervals"][1]["start"] = 1.1
        self.checked(request, proposal, "interval_gap_overlap")

    def test_repeated_state_value_is_valid(self):
        request, proposal = pair(2)
        ledger = proposal["changes"]["StateLedger"]
        ledger["states"]["state_return"] = copy.deepcopy(ledger["states"]["state_before"])
        ledger["states"]["state_return"]["state_id"] = "state_return"
        transition = copy.deepcopy(ledger["transitions"]["t_cut"])
        return_policy = copy.deepcopy(request["inputs"]["policy_context"]["values"]["items"]["p_contact"])
        return_policy.update(policy_id="p_return", boundary_id="cut_return", from_shot="shot_2", to_shot="shot_1")
        request["inputs"]["policy_context"]["values"]["items"]["p_return"] = return_policy
        transition.update(transition_id="t_return", from_state="state_after", to_state="state_return", policy_id="p_return")
        ledger["transitions"]["t_return"] = transition
        chain = ledger["chains"]["contact_chain"]
        chain["state_ids"].append("state_return")
        chain["transition_ids"].append("t_return")
        chain["intervals"].append({"interval_id": "i_return", "state_id": "state_return", "start": 2, "end": 3, "unit": "seconds", "clock_id": "design_clock", "source_refs": ["design"]})
        synchronize(request, proposal)
        self.checked(request, proposal)

    def test_transition_cannot_borrow_another_shots_policy(self):
        request, proposal = pair(2)
        states = proposal["changes"]["StateLedger"]["states"]
        states["state_before"]["shot_id"] = "unrelated_shot_a"
        states["state_after"]["shot_id"] = "unrelated_shot_b"
        self.checked(request, proposal, "transition_policy_shot_binding")

    def test_explicit_unresolved_policy_rejected_for_every_transition_mode(self):
        for mode in ("boundary", "hold", "process"):
            with self.subTest(mode=mode):
                request, proposal = pair(2)
                transition = proposal["changes"]["StateLedger"]["transitions"]["t_cut"]
                transition.update(mode=mode, policy_id="missing_policy")
                self.checked(request, proposal, "transition_policy_missing")

    def test_snapshots_do_not_claim_interval_coverage(self):
        request, proposal = pair(2)
        chain = proposal["changes"]["StateLedger"]["chains"]["contact_chain"]
        chain.update(coverage="snapshots", intervals=[], transition_ids=[])
        check = self.checked(request, proposal)
        self.assertIn("snapshot_coverage_unverified", {d["code"] for d in check.diagnostics})

    def test_authorized_montage_is_not_all_attribute_equality(self):
        self.checked(*boundary_variant("montage"))

    def test_authorized_ellipsis_and_unknown_cue(self):
        request, proposal = boundary_variant("ellipsis")
        self.checked(request, proposal)
        request["inputs"]["policy_context"]["values"]["items"]["p_contact"]["cue"] = {"state": "unknown", "reason": "省略线索待定"}
        synchronize(request, proposal)
        check = self.checked(request, proposal)
        self.assertIn("boundary_permission_unverified", {d["code"] for d in check.diagnostics})

    def test_match_cut_only_selected_attributes_must_match(self):
        request, proposal = boundary_variant("match_cut")
        self.checked(request, proposal)
        request["inputs"]["ledger_context"]["values"]["states"]["state_after"]["attributes"]["person.direction"] = fact("运动方向反转")
        request["inputs"]["ledger_context"]["values"]["transitions"]["t_cut"]["changed_attributes"].append("person.direction")
        reconcile_handoff(request, proposal)
        self.checked(request, proposal, "boundary_invariant_mismatch")

    def test_continuous_holding_reset_rejected_even_with_permission(self):
        request, proposal = pair(3)
        policy = request["inputs"]["policy_context"]["values"]["items"]["p_contact"]
        policy["invariants"].remove("person.holding")
        policy["allowed_changes"].append({"attribute": "person.holding", "reason": "不能代替过程", "source_refs": ["design"]})
        ledger = request["inputs"]["ledger_context"]["values"]
        ledger["states"]["state_after"]["attributes"]["person.holding"] = fact("右手握杯")
        ledger["transitions"]["t_cut"]["changed_attributes"].append("person.holding")
        reconcile_handoff(request, proposal)
        self.checked(request, proposal, "physical_reset")

    def test_actual_process_binding_and_unrelated_action_rejection(self):
        request, proposal = pair(3)
        policy = request["inputs"]["policy_context"]["values"]["items"]["p_contact"]
        policy["invariants"].remove("person.support")
        ledger = request["inputs"]["ledger_context"]["values"]
        ledger["states"]["state_after"]["attributes"]["person.stocking"] = fact("白色底袜")
        ledger["states"]["state_after"]["attributes"]["person.support"] = fact("近侧腿支撑")
        action = {"action_id": "support_transfer", "from_state": "state_before", "to_state": "state_after", "changed_attributes": ["person.support"], "steps": ["近侧脚承重，双脚短暂共同支撑", "重心移到近侧腿，后侧腿卸重"], "source_refs": ["design"]}
        request["inputs"]["action_context"] = context("M4", {"actions": {"support_transfer": action}})
        transition = ledger["transitions"]["t_cut"]
        transition.update(mode="process", changed_attributes=["person.support"], action_binding={"owner": "M4", "source_id": "design", "source_version": "1", "path": "/actions/support_transfer", "value": copy.deepcopy(action)})
        reconcile_handoff(request, proposal)
        self.checked(request, proposal)
        request["inputs"]["action_context"]["values"]["actions"]["support_transfer"]["to_state"] = "unrelated_state"
        transition["action_binding"]["value"]["to_state"] = "unrelated_state"
        synchronize(request, proposal)
        self.checked(request, proposal, "process_action_identity")

    def test_handoff_table_cannot_override_ledger(self):
        request, proposal = pair(3)
        proposal["changes"]["ContinuityHandoffs"]["items"]["handoff_contact"]["table"]["to"]["person.holding"] = fact("右手握杯")
        self.checked(request, proposal, "handoff_table_mismatch")

    def test_palm_closeup_cannot_be_table_only(self):
        request, proposal = pair(3)
        for state in request["inputs"]["ledger_context"]["values"]["states"].values():
            state["attributes"]["camera.framing"] = fact("手掌特写")
        handoff = proposal["changes"]["ContinuityHandoffs"]["items"]["handoff_contact"]
        for side in ("from", "to"):
            handoff["table"][side]["camera.framing"] = fact("手掌特写")
        for document in request["inputs"]["prompt_context"]["values"]["documents"].values():
            for declaration in document["declarations"].values():
                declaration["attributes"]["camera.framing"] = fact("手掌特写")
        synchronize(request, proposal)
        self.checked(request, proposal, "prompt_value_absent")

    def test_chinese_spans_are_codepoints_not_utf8_bytes(self):
        request, proposal = pair(3)
        self.checked(request, proposal)
        doc = request["inputs"]["prompt_context"]["values"]["documents"]["prompt_previous"]
        span = doc["declarations"]["decl_previous"]["spans"]["person.identity"]
        span["start"] = len(doc["text"][:span["start"]].encode("utf-8"))
        synchronize(request, proposal)
        self.checked(request, proposal, "prompt_span_mismatch")

    def observation_pair(self, verdict="deviation"):
        request, proposal = pair(3)
        state = request["inputs"]["ledger_context"]["values"]["states"]["state_before"]
        attrs = copy.deepcopy(state["attributes"])
        if verdict == "deviation":
            attrs["person.support"] = fact("近侧腿支撑")
        request["sources"]["mock_observation"] = {"kind": "media_observation", "locator": "synthetic-test://m8/not-real-media", "version": "1", "excerpt": "Only a synthetic contract test double; no video observed and no generated result claimed."}
        observation = {"observation_id": "obs_stub", "media_id": "synthetic_media_stub", "media_version": "1", "plan_work_id": request["work_id"], "plan_version": 0, "plan_state_digest": m8.digest(state), "state_id": state["state_id"], "attributes": attrs, "verdict": verdict, "method": "synthetic contract test double", "coverage": "hypothetical endpoint only", "locator": "synthetic-test://m8/not-real-media", "source_refs": ["mock_observation"]}
        request["inputs"]["actual_context"] = {"owner": "M12", "source_id": "mock_observation", "source_version": "1", "values": {"observations": {"obs_stub": observation}}}
        synchronize(request, proposal)
        return request, proposal

    def test_actual_deviation_cannot_silently_use_planned_end(self):
        self.checked(*self.observation_pair(), expected="actual_observation_ignored")

    def test_actual_replan_is_explicit_pending_and_observation_immutable(self):
        request, proposal = self.observation_pair()
        original = copy.deepcopy(request)
        proposal["changes"]["ContinuityHandoffs"]["items"]["handoff_contact"]["continuation"] = {"decision": "replan", "observation_id": "obs_stub"}
        check = self.checked(request, proposal)
        self.assertEqual(request, original)
        self.assertTrue({"continuation_pending", "actual_authenticity_unverified"} <= {d["code"] for d in check.diagnostics})

    def test_actual_unsafe_continue_is_rejected(self):
        request, proposal = self.observation_pair()
        proposal["changes"]["ContinuityHandoffs"]["items"]["handoff_contact"]["continuation"] = {"decision": "continue_from_observed", "observation_id": "obs_stub"}
        self.checked(request, proposal, "actual_continue_mismatch")

    def test_actual_consistent_metadata_never_certifies_media(self):
        request, proposal = self.observation_pair("consistent")
        proposal["changes"]["ContinuityHandoffs"]["items"]["handoff_contact"]["continuation"] = {"decision": "continue_from_observed", "observation_id": "obs_stub"}
        check = self.checked(request, proposal)
        self.assertIn("actual_authenticity_unverified", {d["code"] for d in check.diagnostics})

    def test_actual_plan_digest_tamper_rejected(self):
        request, proposal = self.observation_pair()
        request["inputs"]["actual_context"]["values"]["observations"]["obs_stub"]["plan_state_digest"] = "0" * 64
        synchronize(request, proposal)
        proposal["changes"]["ContinuityHandoffs"]["items"]["handoff_contact"]["continuation"] = {"decision": "replan", "observation_id": "obs_stub"}
        self.checked(request, proposal, "actual_plan_binding")

    def test_original_projection_must_match_real_parent(self):
        state, batch, requests = fixture("state-empty"), fixture("proposal-batch"), fixture("requests")
        requests[0]["inputs"]["readonly_projection"] = [{"path": "/content/ContinuityPolicy", "source_version": 0, "value": {"items": {"forged": {}}}}]
        synchronize(requests[0], batch["proposals"][0])
        check = m8.Check()
        self.assertIsNone(m8.accept(check, state, batch, requests))
        self.assertIn("readonly_projection_changed", {d["code"] for d in check.diagnostics})

    def test_parent_context_must_match_candidate_not_only_request(self):
        state, batch, requests = fixture("state-empty"), fixture("proposal-batch"), fixture("requests")
        requests[1]["inputs"]["policy_context"]["values"]["items"]["p_contact"]["cue"] = fact("异版本上下文")
        synchronize(requests[1], batch["proposals"][1])
        check = m8.Check()
        self.assertIsNone(m8.accept(check, state, batch, requests))
        self.assertIn("readonly_conflict", {d["code"] for d in check.diagnostics})

    def test_blocker_rejects_atomic_acceptance(self):
        state, batch, requests = fixture("state-empty"), fixture("proposal-batch"), fixture("requests")
        batch["proposals"][1]["issues"] = [{"issue_id": "block", "owner": "M8.2", "severity": "blocking", "message": "待修复状态", "status": "open", "source_refs": ["design"]}]
        check = m8.Check()
        self.assertIsNone(m8.accept(check, state, batch, requests))
        self.assertIn("open_blocker", {d["code"] for d in check.diagnostics})
        self.assertEqual(state, fixture("state-empty"))

    def test_display_change_only_invalidates_title_reader(self):
        before = fixture("state-empty")
        after = copy.deepcopy(before)
        after["display"]["title"] = "只改显示标题"
        self.assertEqual(set(m8.impact(before, after)["stale_consumers"]), {"title"})

    def test_readonly_context_changes_invalidate_registered_reader(self):
        result, _, _, _ = self.accepted()
        before = result["state"]
        before["consumers"]["observation_reader"] = {"module_id": "M12", "result_version": 1, "source_state_version": 1, "read_paths": ["/contexts/M8.3"], "status": "current"}
        after = copy.deepcopy(before)
        after["contexts"]["M8.3"]["handoff_brief"] += " changed"
        impact = m8.impact(before, after)
        self.assertIn("observation_reader", impact["stale_consumers"])
        self.assertTrue(any(p.startswith("/contexts/") for p in impact["changed_paths"]))

    def test_duplicate_json_nonfinite_and_version_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":1e999}'):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    m8.load_json(path)
        request, proposal = pair(1)
        proposal["contract_version"] = "2.0.0"
        self.checked(request, proposal, "schema")


if __name__ == "__main__":
    unittest.main(verbosity=2)
