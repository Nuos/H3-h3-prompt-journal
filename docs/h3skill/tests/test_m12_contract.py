"""Behavior tests for M12's declaration contract, not real media observations.

The declared_actual branches below simulate attestations. No test decodes, watches,
hears or certifies media. Public examples must retain the synthetic fixture origin.
"""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "h3-audit-repair/scripts/m12_contract.py"
spec = importlib.util.spec_from_file_location("m12_contract", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def reference(name, version="v1", owner="M11", kind="CompilationResult"):
    return {"id": name, "version": version,
            "digest": m.digest({"fixture": "synthetic", "id": name, "version": version, "kind": kind}),
            "owner": owner, "kind": kind}


def make_plan(media=False, gate=None):
    gate = gate or ("G3" if media else "G2")
    media = gate in ("G3", "G4")
    target = reference("FILM" if gate == "G4" else "CLIP", owner="external",
                       kind="assembled_media" if gate == "G4" else "generated_media") if media else reference("PROMPT")
    return {"scope_id": "SCOPE_MEDIA" if media else "SCOPE_PROTOCOL", "scope_version": "v1",
            "plan_ref": reference("PLAN", owner="M8", kind="StateLedger"),
            "scope_sources": [reference("BRIEF", owner="M1", kind="WorkBrief")],
            "gates": [gate], "requirement_ids": ["REQ_CONTINUITY" if media else "REQ_PROTOCOL"],
            "checks": [{"id": "CHK_MEDIA" if media else "CHK_PROTOCOL",
                        "requirement_id": "REQ_CONTINUITY" if media else "REQ_PROTOCOL", "gate": gate,
                        "expected": "The red cup remains in the right hand throughout the required window." if media else "The approved summary is retained in the compiled prompt.",
                        "method": "human_video_review" if media else "compare_approved_summary",
                        "targets": [target], "channels": ["video"] if media else [],
                        "time_window_ms": [0, 4000] if media else None,
                        "coverage": "full_window" if media else "document"}]}


def make_observation(p=None, origin="synthetic", verdict="satisfies", oid="OBS_SYNTHETIC"):
    p = p or make_plan(True)
    c = p["checks"][0]
    return {"id": oid, "media_ref": deepcopy(c["targets"][0]), "plan_ref": deepcopy(p["plan_ref"]),
            "observer": "synthetic_fixture_observer", "observed_at": "2026-11-01T10:00:00Z",
            "method": c["method"], "time_domain": "media_ms", "channels": deepcopy(c["channels"]),
            "coverage": {"mode": "full", "windows_ms": [[0, 4000]], "duration_ms": 4000},
            "origin": origin,
            "facts": [{"check_id": c["id"], "expected": c["expected"],
                       "observed": "Synthetic fixture assertion; no real video has been observed.",
                       "assessment": verdict, "location": "Synthetic fixture media window 0–4000 ms",
                       "time_window_ms": [0, 4000]}]}


def make_audit(media=False, origin="synthetic", result="pass", gate=None):
    p = make_plan(media, gate)
    c = p["checks"][0]
    media = c["gate"] in ("G3", "G4")
    e = {"id": "EV_MEDIA" if media else "EV_DOCUMENT", "kind": "media_observation" if media else "document",
         "origin": origin, "source_ref": deepcopy(c["targets"][0]), "check_ids": [c["id"]],
         "locator": "fixture:declared-evidence-only", "content": "Synthetic supplied evidence for the declared check; no file is read."}
    observations = []
    if media:
        observations = [make_observation(p, origin, "violates" if result == "fail" else "satisfies")]
        e["observation_id"] = observations[0]["id"]
    return {"plan": p, "current_refs": deepcopy(m.all_plan_refs(p)),
            "results": [{"check_id": c["id"], "result": result, "evidence_ids": [e["id"]],
                         "reason": "Synthetic example of a supplied reviewer declaration."}],
            "evidence": [e], "observations": observations}


def make_repair(applied=True, retest=False):
    audit = make_audit(result="fail")
    c = audit["plan"]["checks"][0]
    causal = deepcopy(audit["evidence"][0])
    causal.update({"id": "EV_CAUSE", "kind": "causal_analysis", "content": "Synthetic comparison identifies summary serialization in the M11-owned compilation as the cause."})
    audit["evidence"].append(causal)
    before, after = deepcopy(c["targets"][0]), reference("PROMPT", "v2")
    clip = reference("CLIP", owner="external", kind="generated_media")
    film = reference("FILM", owner="external", kind="assembled_media")
    other = reference("UNRELATED_LOOK", owner="M10", kind="LookPlan")
    nodes = deepcopy(audit["current_refs"]) + [clip, film, other]
    value = {"audit": audit,
             "issues": [{"id": "ISSUE_SUMMARY", "check_id": c["id"], "object_ref": before,
                         "location": "Synthetic compiled summary field", "expected": c["expected"],
                         "actual": "Synthetic fixture: approved summary is missing.",
                         "evidence_ids": ["EV_DOCUMENT"], "owner": "M11",
                         "attribution_basis": "Synthetic semantic review attributes a missing serialized field to its M11 owner.",
                         "causal_evidence_ids": ["EV_CAUSE"], "requested_action": "Return the summary correction to M11; preserve the approved plan."}],
             "changes": [{"id": "CHANGE_SUMMARY", "issue_ids": ["ISSUE_SUMMARY"], "owner": "M11",
                          "before": before, "after": after, "reason": "Synthetic supplied version transition; this program executes no edit.",
                          "status": "reported_applied" if applied else "proposed"}],
             "dependencies": {"nodes": nodes, "edges": [{"upstream": "PROMPT", "downstream": "CLIP"}, {"upstream": "CLIP", "downstream": "FILM"}], "complete": True},
             "retests": []}
    if retest:
        new = make_audit()
        new["plan"]["scope_version"] = "v2"
        new["plan"]["checks"][0]["targets"] = [deepcopy(after)]
        new["current_refs"] = deepcopy(m.all_plan_refs(new["plan"]))
        new["evidence"][0].update({"id": "EV_RETEST", "source_ref": deepcopy(after), "content": "Synthetic fresh comparison of v2 includes the formerly omitted summary."})
        new["results"][0]["evidence_ids"] = ["EV_RETEST"]
        value["retests"] = [{"issue_id": "ISSUE_SUMMARY", "audit": new}]
    return value


def make_request(target="M12.1", inputs=None, base=0, rid=None):
    if inputs is None:
        inputs = {"M12.1": make_plan, "M12.2": make_audit,
                  "M12.3": lambda: {"observations": [make_observation()]}, "M12.4": make_repair}[target]()
    return {"kind": "M12Request", "contract_version": "1.0.0", "route_version": "1.0.0",
            "work_id": "WORK_SYNTHETIC", "base_version": base, "request_id": rid or "REQUEST_" + target.replace(".", "_"),
            "target": target, "inputs": inputs}


def make_media_repair():
    """Simulated actual-attestation inputs; never evidence of an observed video."""
    old = make_audit(True, "declared_actual", "fail")
    p = old["plan"]
    causal = {"id": "EV_MEDIA_CAUSE", "kind": "causal_analysis", "origin": "user_report",
              "source_ref": deepcopy(p["plan_ref"]), "check_ids": ["CHK_MEDIA"],
              "locator": "fixture:causal-review", "content": "Simulated attribution to an M8 plan revision; no actual media was reviewed."}
    old["evidence"].append(causal)
    after = reference("PLAN", "v2", "M8", "StateLedger")
    new = make_audit(True, "declared_actual")
    new["plan"]["scope_version"] = "v2"; new["plan"]["plan_ref"] = deepcopy(after)
    new["current_refs"] = deepcopy(m.all_plan_refs(new["plan"]))
    new["observations"][0].update({"id": "OBS_REVIEW_NEW", "plan_ref": deepcopy(after), "observed_at": "2026-11-02T10:00:00Z"})
    new["evidence"][0].update({"id": "EV_MEDIA_NEW", "observation_id": "OBS_REVIEW_NEW", "content": "Simulated fresh re-observation of the same media under the revised plan."})
    new["results"][0]["evidence_ids"] = ["EV_MEDIA_NEW"]
    return {"audit": old,
            "issues": [{"id": "ISSUE_MEDIA", "check_id": "CHK_MEDIA", "object_ref": deepcopy(p["checks"][0]["targets"][0]),
                        "location": "Fixture 0–4000 ms", "expected": p["checks"][0]["expected"],
                        "actual": "Simulated old reviewer violation", "evidence_ids": ["EV_MEDIA"],
                        "owner": "M8", "attribution_basis": "Simulated evidence-based attribution to the plan owner.",
                        "causal_evidence_ids": ["EV_MEDIA_CAUSE"], "requested_action": "Request a plan revision and fresh media observation."}],
            "changes": [{"id": "CHANGE_PLAN", "issue_ids": ["ISSUE_MEDIA"], "owner": "M8",
                         "before": deepcopy(p["plan_ref"]), "after": after, "reason": "Simulated externally reported plan revision.", "status": "reported_applied"}],
            "dependencies": {"nodes": deepcopy(old["current_refs"]), "edges": [{"upstream": "PLAN", "downstream": "CLIP"}], "complete": True},
            "retests": [{"issue_id": "ISSUE_MEDIA", "audit": new}]}


class M12ContractTests(unittest.TestCase):
    def assert_error(self, code, fn, *args):
        with self.assertRaises(m.ContractError) as caught:
            fn(*args)
        self.assertEqual(caught.exception.code, code)

    def accepted(self, request, state=None):
        return m.accept([m.propose(request)], [request], state or m.empty_state(request["work_id"]))

    def test_four_independent_targets_and_boundaries(self):
        for target in m.PARTS:
            with self.subTest(target=target):
                q = make_request(target)
                self.assertEqual(m.route(q)["status"], "ready")
                p = m.propose(q)
                self.assertEqual(p["record"]["kind"], m.PARTS[target])
                self.assertEqual(m.check(p, q)["status"], "valid")
                self.assertFalse(self.accepted(q)["verification_boundary"]["media_observed_by_this_program"])

    def test_no_evidence_never_passes(self):
        a = make_audit(); a["results"][0]["evidence_ids"] = []; a["evidence"] = []
        result = m.build_audit(a)
        self.assertEqual(result["scope_result"], "unverified")
        self.assertIn("no_supporting_evidence", result["checks"][0]["gaps"])

    def test_omitted_result_remains_in_required_scope(self):
        a = make_audit(); a["results"] = []
        self.assertEqual(m.build_audit(a)["checks"][0]["effective_result"], "unverified")

    def test_supported_fail_survives_irrelevant_extra_evidence(self):
        a = make_audit(result="fail")
        e = deepcopy(a["evidence"][0]); e["id"] = "EV_IRRELEVANT"; e["source_ref"] = reference("OTHER")
        a["evidence"].append(e); a["results"][0]["evidence_ids"].append(e["id"])
        result = m.build_audit(a)
        self.assertEqual(result["scope_result"], "fail")
        self.assertTrue(result["checks"][0]["gaps"])

    def test_g2_scoped_pass_does_not_certify_task(self):
        result = m.build_audit(make_audit())
        self.assertEqual(result["gate_results"], {"G2": "pass"})
        self.assertIn("G3", result["unassessed_gates"])
        self.assertFalse(result["verification_boundary"]["whole_task_certified"])

    def test_not_applicable_needs_rule_and_evidence(self):
        a = make_audit(result="not_applicable")
        self.assert_error("type", m.build_audit, a)
        a["results"][0]["applicability"] = {"rule": "Synthetic mode-specific field does not apply and has no downstream dependency.", "basis_ref": deepcopy(a["evidence"][0]["source_ref"]), "no_downstream_dependents": True}
        self.assertEqual(m.build_audit(a)["scope_result"], "unverified")
        a["evidence"][0]["kind"] = "applicability"
        self.assertEqual(m.build_audit(a)["scope_result"], "not_applicable")

    def test_synthetic_and_user_report_cannot_certify_media(self):
        a = make_audit(True)
        self.assertEqual(m.build_audit(a)["scope_result"], "unverified")
        a["evidence"][0]["origin"] = "user_report"
        a["observations"][0]["origin"] = "declared_actual"
        self.assertEqual(m.build_audit(a)["scope_result"], "unverified")

    def test_simulated_actual_attestation_branch_is_not_observation(self):
        result = m.build_audit(make_audit(True, "declared_actual"))
        self.assertEqual(result["scope_result"], "pass")
        self.assertTrue(result["verification_boundary"]["declared_actual_is_attestation"])
        self.assertFalse(result["verification_boundary"]["media_observed_by_this_program"])

    def test_sampled_and_partial_coverage_cannot_pass_full_window(self):
        for mode, windows in (("sampled", [[0, 4000]]), ("intervals", [[0, 1000]])):
            a = make_audit(True, "declared_actual")
            a["observations"][0]["coverage"].update({"mode": mode, "windows_ms": windows})
            a["observations"][0]["facts"][0]["time_window_ms"] = windows[0]
            self.assertEqual(m.build_audit(a)["scope_result"], "unverified")

    def test_observation_requires_audio_and_video_when_requested(self):
        a = make_audit(True, "declared_actual")
        a["plan"]["checks"][0]["channels"].append("audio")
        self.assertEqual(m.build_audit(a)["scope_result"], "unverified")

    def test_plan_and_media_versions_both_bound(self):
        for key in ("plan_ref", "media_ref"):
            a = make_audit(True, "declared_actual")
            a["observations"][0][key]["version"] = "v2"
            a["observations"][0][key]["digest"] = "2" * 64
            self.assertEqual(m.build_audit(a)["scope_result"], "unverified")

    def test_g3_observation_cannot_be_used_as_g4(self):
        a = make_audit(gate="G4", origin="declared_actual")
        o = make_observation(make_plan(True), "declared_actual")
        a["observations"] = [o]
        self.assertEqual(m.build_audit(a)["scope_result"], "unverified")

    def test_failure_time_must_be_inside_check_window(self):
        a = make_audit(True, "declared_actual", "fail")
        o = a["observations"][0]
        o["coverage"] = {"mode": "full", "windows_ms": [[0, 10000]], "duration_ms": 10000}
        o["facts"][0]["time_window_ms"] = [8000, 9000]
        self.assertEqual(m.build_audit(a)["scope_result"], "unverified")
        o["facts"][0]["time_window_ms"] = [2000, 2500]
        self.assertEqual(m.build_audit(a)["scope_result"], "fail")

    def test_fact_window_cannot_exceed_observation(self):
        o = make_observation(); o["facts"][0]["time_window_ms"] = [3000, 5000]
        self.assert_error("fact_coverage", m.observation, o)

    def test_stale_is_not_a_fifth_historical_result(self):
        a = make_audit()
        a["current_refs"][-1] = reference("PROMPT", "v2")
        result = m.build_audit(a)
        self.assertEqual(result["checks"][0]["result"], "pass")
        self.assertEqual(result["checks"][0]["current_validity"], "stale")
        self.assertEqual(result["scope_result"], "unverified")

    def test_missing_current_version_is_unverified(self):
        a = make_audit(); a["current_refs"] = []
        self.assertEqual(m.build_audit(a)["checks"][0]["current_validity"], "unverified")

    def test_proposal_tampering_and_wrong_original_request_fail(self):
        q = make_request(); p = m.propose(q); p["record"]["owner"] = "M12.4"
        self.assert_error("proposal_mismatch", m.check, p, q)
        p = m.propose(q); q["inputs"]["checks"][0]["expected"] = "Weaker requirement"
        self.assert_error("proposal_mismatch", m.check, p, q)

    def test_accept_is_atomic_and_does_not_mutate_input(self):
        q1, q2 = make_request(), make_request("M12.2")
        p1, p2 = m.propose(q1), m.propose(q2); p2["record"]["digest"] = "0" * 64
        state = m.empty_state(q1["work_id"]); before = deepcopy(state)
        self.assert_error("proposal_mismatch", m.accept, [p1, p2], [q1, q2], state)
        self.assertEqual(state, before)

    def test_atomic_sibling_accept_and_idempotent_replay(self):
        qs = [make_request(), make_request("M12.2")]; ps = [m.propose(q) for q in qs]
        result = m.accept(ps, qs, m.empty_state(qs[0]["work_id"]))
        self.assertEqual(result["state"]["version"], 1)
        self.assertEqual(len(result["state"]["records"]), 2)
        again = m.accept(ps, qs, result["state"])
        self.assertTrue(again["idempotent"])
        self.assertEqual(again["state"], result["state"])

    def test_stale_base_and_request_id_reuse_rejected(self):
        q = make_request(); state = self.accepted(q)["state"]
        other = make_request("M12.3")
        self.assert_error("stale_base_version", m.accept, [m.propose(other)], [other], state)
        q["base_version"] = 1
        self.assert_error("request_id_reuse", m.accept, [m.propose(q)], [q], state)

    def test_scope_cannot_remove_or_weaken_a_check(self):
        q = make_request(); state = self.accepted(q)["state"]
        for field, replacement in (("expected", "A weaker expectation"), ("method", "different_method")):
            new = make_request(base=1, rid="REQ_NEXT")
            new["inputs"]["scope_version"] = "v2"
            new["inputs"]["checks"][0][field] = replacement
            self.assert_error("scope_shrink", m.accept, [m.propose(new)], [new], state)
        new = make_request(base=1, rid="REQ_NEXT"); new["inputs"]["checks"][0]["required"] = False
        self.assert_error("unknown_key", m.propose, new)

    def test_scope_can_expand_with_new_version(self):
        q = make_request(); state = self.accepted(q)["state"]
        new = make_request(base=1, rid="REQ_EXPANDED")
        new["inputs"]["scope_version"] = "v2"
        new["inputs"]["requirement_ids"].append("REQ_ADDED")
        c = deepcopy(new["inputs"]["checks"][0]); c.update({"id": "CHK_ADDED", "requirement_id": "REQ_ADDED", "expected": "Additional requirement"})
        new["inputs"]["checks"].append(c)
        self.assertEqual(self.accepted(new, state)["state"]["version"], 2)

    def test_expanded_scope_stales_old_scope_and_rejects_new_audit_using_it(self):
        state = self.accepted(make_request("M12.2"))["state"]
        expanded = make_request(base=1, rid="REQ_EXPANDED")
        p = expanded["inputs"]; p["scope_version"] = "v2"
        p["requirement_ids"].append("REQ_EXTRA")
        c = deepcopy(p["checks"][0]); c.update({"id": "CHK_EXTRA", "requirement_id": "REQ_EXTRA", "expected": "Additional required assertion"})
        p["checks"].append(c)
        result = self.accepted(expanded, state)
        old = result["current_view"]["audit_ledgers"][0]
        self.assertEqual(old["scope_current_validity"], "stale")
        self.assertEqual(old["scope_result"], "unverified")
        self.assertEqual(old["checks"][0]["historical_result"], "pass")
        q = make_request("M12.2", base=2, rid="REQ_OLD_SCOPE")
        self.assert_error("stale_scope", m.accept, [m.propose(q)], [q], result["state"])

    def test_history_rewrite_detected(self):
        state = self.accepted(make_request())["state"]
        state["records"][0]["content"]["plan"]["checks"][0]["expected"] = "Edited history"
        self.assert_error("state_history", m.validate_state, state)

    def test_same_object_version_cannot_have_two_digests(self):
        a = make_audit(); a["evidence"][0]["source_ref"]["digest"] = "1" * 64
        self.assert_error("reference_version_reuse", m.build_audit, a)

    def test_m12_3_observation_ids_are_immutable(self):
        q = make_request("M12.3"); state = self.accepted(q)["state"]
        q2 = make_request("M12.3", base=1, rid="NEW_OBS")
        q2["inputs"]["observations"][0]["observer"] = "Different observer"
        self.assert_error("immutable_record", m.accept, [m.propose(q2)], [q2], state)

    def test_explicit_transitive_closure_excludes_unrelated_object(self):
        result = m.build_repair(make_repair())
        self.assertEqual(result["affected_ids"], ["CLIP", "FILM", "PROMPT"])
        self.assertNotIn("UNRELATED_LOOK", result["affected_ids"])
        self.assertFalse(result["repair_executed"])
        self.assertEqual(result["issues"][0]["status"], "open")

    def test_proposed_change_does_not_invalidate_current_records(self):
        result = m.build_repair(make_repair(applied=False))
        self.assertEqual(result["affected_ids"], [])
        self.assertEqual(result["planned_affected_ids"], ["CLIP", "FILM", "PROMPT"])

    def test_unknown_dependencies_keep_impact_partial_and_issue_open(self):
        r = make_repair(retest=True); r["dependencies"]["complete"] = False
        result = m.build_repair(r)
        self.assertEqual(result["impact_status"], "partial")
        self.assertIn("dependency_impact_incomplete", result["issues"][0]["reasons"])

    def test_dependency_graph_must_match_declared_versions(self):
        r = make_repair()
        r["dependencies"]["nodes"][2] = reference("PROMPT", "v0")
        self.assert_error("dependency_version", m.build_repair, r)

    def test_dependency_graph_must_match_accepted_current_versions(self):
        q = make_request("M12.2"); q["inputs"]["current_refs"].append(reference("CLIP", "v2", "external", "generated_media"))
        state = self.accepted(q)["state"]
        r = make_request("M12.4", base=1, rid="REQ_STALE_GRAPH")
        self.assert_error("stale_dependency_graph", m.accept, [m.propose(r)], [r], state)

    def test_owner_needs_causal_evidence_not_symptom(self):
        r = make_repair(); r["issues"][0]["causal_evidence_ids"] = []; r["changes"] = []
        self.assertEqual(m.build_repair(r)["issues"][0]["owner"], "unresolved")
        r = make_repair(); r["changes"][0]["owner"] = "M4"
        self.assert_error("change_ownership", m.build_repair, r)

    def test_plan_repair_alone_cannot_close_issue(self):
        self.assertFalse(m.build_repair(make_repair())["all_issues_closed"])
        r = make_repair(applied=False, retest=True)
        self.assertIn("repair_only_proposed", m.build_repair(r)["issues"][0]["reasons"])

    def test_full_scope_fresh_current_retest_closes_declared_document_issue(self):
        result = m.build_repair(make_repair(retest=True))
        self.assertEqual(result["issues"][0]["status"], "closed_by_retest")
        self.assertTrue(result["all_issues_closed"])
        self.assertFalse(result["verification_boundary"]["whole_task_certified"])

    def test_retest_cannot_weaken_same_check_id(self):
        r = make_repair(retest=True)
        r["retests"][0]["audit"]["plan"]["checks"][0]["expected"] = "Weaker test"
        self.assert_error("scope_shrink", m.build_repair, r)

    def test_fresh_reobservation_can_reuse_media_after_plan_change(self):
        r = make_media_repair()
        result = m.build_repair(r)
        self.assertEqual(result["issues"][0]["status"], "closed_by_retest")
        self.assertEqual(r["audit"]["plan"]["checks"][0]["targets"], r["retests"][0]["audit"]["plan"]["checks"][0]["targets"])
        self.assertFalse(result["verification_boundary"]["media_observed_by_this_program"])

    def test_old_observation_timestamp_cannot_be_reused_for_retest(self):
        r = make_media_repair()
        r["retests"][0]["audit"]["observations"][0]["observed_at"] = r["audit"]["observations"][0]["observed_at"]
        result = m.build_repair(r)
        self.assertEqual(result["issues"][0]["status"], "open")
        self.assertIn("fresh_evidence_missing", result["issues"][0]["reasons"])

    def test_reobservation_keeps_old_history_stale_and_new_observation_current(self):
        r = make_media_repair()
        q1 = make_request("M12.2", r["audit"], rid="REQ_OLD_OBSERVATION")
        state = self.accepted(q1)["state"]
        q2 = make_request("M12.4", r, base=1, rid="REQ_REOBSERVE_CHANGE")
        state = self.accepted(q2, state)["state"]
        q3 = make_request("M12.2", r["retests"][0]["audit"], base=2, rid="REQ_NEW_OBSERVATION")
        result = self.accepted(q3, state)
        old, new = result["current_view"]["audit_ledgers"]
        self.assertEqual(old["checks"][0]["historical_result"], "fail")
        self.assertEqual(old["checks"][0]["current_validity"], "stale")
        self.assertEqual(new["checks"][0]["historical_result"], "pass")
        self.assertEqual(new["checks"][0]["current_validity"], "current")
        self.assertEqual(new["scope_result"], "pass")

    def test_external_media_transition_requires_new_version_and_new_observation(self):
        # This simulates a provider report; no media is generated or observed.
        r = make_media_repair()
        old = r["audit"]
        before = deepcopy(old["plan"]["checks"][0]["targets"][0])
        after = reference("CLIP", "v2", "external", "generated_media")
        old["evidence"][1]["source_ref"] = deepcopy(before)
        r["issues"][0]["owner"] = "external"
        r["issues"][0]["attribution_basis"] = "Simulated provider report attributes the media artifact transition to its external owner."
        r["changes"][0].update({"owner": "external", "before": before, "after": after})
        new = r["retests"][0]["audit"]
        new["plan"]["plan_ref"] = deepcopy(old["plan"]["plan_ref"])
        new["plan"]["checks"][0]["targets"] = [deepcopy(after)]
        new["current_refs"] = deepcopy(m.all_plan_refs(new["plan"]))
        new["observations"] = deepcopy(old["observations"])
        new["evidence"][0].update({"source_ref": deepcopy(after), "observation_id": new["observations"][0]["id"]})
        result = m.build_repair(r)
        self.assertEqual(result["issues"][0]["owner"], "external")
        self.assertEqual(result["issues"][0]["status"], "open")
        self.assertIn("retest_not_current_pass", result["issues"][0]["reasons"])
        self.assertFalse(result["repair_executed"])
        self.assertEqual(self.accepted(make_request("M12.4", r))["status"], "accepted")
        invalid = deepcopy(r); invalid["changes"][0]["after"]["version"] = before["version"]
        self.assert_error("change_version", m.build_repair, invalid)
        observation = new["observations"][0]
        observation.update({"id": "OBS_EXTERNAL_V2", "media_ref": deepcopy(after), "observed_at": "2026-11-03T10:00:00Z"})
        observation["facts"][0].update({"assessment": "satisfies", "observed": "Simulated new provider artifact review satisfies the original check."})
        new["evidence"][0]["observation_id"] = observation["id"]
        fresh = m.build_repair(r)
        self.assertEqual(fresh["issues"][0]["status"], "closed_by_retest")
        self.assertFalse(fresh["verification_boundary"]["media_observed_by_this_program"])

    def test_old_evidence_renaming_is_not_fresh_retest(self):
        r = make_repair(retest=True)
        r["changes"] = []
        new = r["retests"][0]["audit"]
        new["plan"] = deepcopy(r["audit"]["plan"])
        new["current_refs"] = deepcopy(r["audit"]["current_refs"])
        new["evidence"][0] = deepcopy(r["audit"]["evidence"][0]); new["evidence"][0]["id"] = "EV_RENAMED"
        new["results"][0]["evidence_ids"] = ["EV_RENAMED"]
        self.assertIn("fresh_evidence_missing", m.build_repair(r)["issues"][0]["reasons"])

    def test_history_retains_pass_while_current_view_stales(self):
        q = make_request("M12.2"); state = self.accepted(q)["state"]
        original = deepcopy(state["records"][0])
        repair = make_request("M12.4", make_repair(), base=1, rid="REQ_CHANGE")
        # Evidence IDs are globally immutable; use distinct failure-evidence IDs.
        a = repair["inputs"]["audit"]
        a["evidence"][0]["id"] = "EV_FAILURE"
        a["results"][0]["evidence_ids"] = ["EV_FAILURE"]
        repair["inputs"]["issues"][0]["evidence_ids"] = ["EV_FAILURE"]
        result = self.accepted(repair, state)
        self.assertEqual(result["state"]["records"][0], original)
        view = result["current_view"]["audit_ledgers"][0]["checks"][0]
        self.assertEqual(view["historical_result"], "pass")
        self.assertEqual(view["current_validity"], "stale")

    def test_json_schema_request_and_output_shapes(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is a development-only optional checker")
        schema = json.loads((ROOT / "h3-audit-repair/references/contracts.json").read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        for target in m.PARTS:
            q = make_request(target)
            jsonschema.Draft202012Validator(schema).validate(q)
            for name, value in (("Proposal", m.propose(q)), ("State", self.accepted(q)["state"])):
                alternate = deepcopy(schema); alternate["$ref"] = "#/$defs/" + name
                jsonschema.Draft202012Validator(alternate).validate(value)

    def test_strict_json_unknown_keys_duplicate_keys_and_nonfinite(self):
        q = make_request(); q["inputs"]["script_to_execute"] = "forbidden"
        self.assert_error("unknown_key", m.propose, q)
        q = make_request(); q["base_version"] = True
        self.assert_error("type", m.propose, q)
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "input.json"
            file.write_text('{"x":1,"x":2}')
            self.assert_error("duplicate_json_key", m.load, file)
            file.write_text('{"x":NaN}')
            self.assert_error("non_finite_number", m.load, file)

    def test_cli_works_in_isolated_directory_and_never_reads_locator(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            copied = temp / "m12_contract.py"; copied.write_text(SCRIPT.read_text())
            q = make_request("M12.2")
            q["inputs"]["evidence"][0]["locator"] = "file:///definitely-not-readable-evidence"
            file = temp / "request.json"; file.write_text(json.dumps(q))
            process = subprocess.run([sys.executable, str(copied), "propose", str(file)], cwd=temp, text=True, capture_output=True)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            self.assertEqual(json.loads(process.stdout)["record"]["kind"], "AuditLedger")
            self.assertEqual({p.name for p in temp.iterdir()}, {"m12_contract.py", "request.json"})


if __name__ == "__main__":
    unittest.main()
