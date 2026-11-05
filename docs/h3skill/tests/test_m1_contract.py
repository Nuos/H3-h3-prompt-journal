#!/usr/bin/env python3
"""Behavioral checks for M1's public contract and deterministic support only.

Run: python -m unittest discover -s docs/h3skill/tests -p 'test_m1_contract.py' -v
No model, audio measurement, video inspection or semantic-quality claim is made.
"""

import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent / "h3-work-intent"
SCRIPT = SKILL / "scripts" / "m1_contract.py"
spec = importlib.util.spec_from_file_location("m1_contract", SCRIPT)
m1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m1)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def codes(result):
    return {item["code"] for item in result["diagnostics"]}


class M1ContractTests(unittest.TestCase):
    def setUp(self):
        self.empty = read(SKILL / "assets" / "workbrief-empty.json")
        self.batch = read(HERE / "fixtures" / "water-batch.json")
        self.request = read(SKILL / "assets" / "request-m1.json")

    def full(self):
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 0, result)
        return result["work_brief"]

    def test_all_four_nodes_route_independently(self):
        for target, filename in (("M1", "request-m1.json"), ("M1.1", "request-m1-1.json"),
                                 ("M1.2", "request-m1-2.json"), ("M1.3", "request-m1-3.json")):
            with self.subTest(target=target):
                result, code = m1.route(read(SKILL / "assets" / filename))
                self.assertEqual(code, 0, result)
                self.assertEqual(result["dispatch"]["target"], target)
                self.assertEqual(result["dispatch"]["semantic_execution"], "not_started")
                self.assertEqual(result["audit"]["semantic"], "unverified")

    def test_parent_route_does_not_certify_child_inputs(self):
        result, code = m1.route(self.request)
        self.assertEqual(code, 0)
        self.assertFalse(result["dispatch"]["child_inputs_verified"])
        self.assertEqual(result["dispatch"]["eligible_children"], ["M1.1", "M1.2", "M1.3"])
        self.assertNotIn("paragraph_material", result["dispatch"]["input_projection"])

    def test_each_child_proposal_checks_against_its_request(self):
        for suffix in ("1", "2", "3"):
            with self.subTest(child=suffix):
                proposal = read(SKILL / "assets" / f"proposal-m1-{suffix}.json")
                request = read(SKILL / "assets" / f"request-m1-{suffix}.json")
                result, code = m1.check(proposal, request)
                self.assertEqual(code, 0, result)
                self.assertEqual(result["audit"]["structure"], "pass")

    def test_minimum_input_is_enough_without_unrelated_upstream(self):
        request = read(SKILL / "assets" / "request-m1-2.json")
        self.assertEqual(set(request["inputs"]), {"work_type", "intent_context", "paragraph_material"})
        result, code = m1.route(request)
        self.assertEqual(code, 0, result)
        self.assertNotIn("AssetRegistry", result["dispatch"]["input_projection"])

    def test_missing_input_is_returned_to_user(self):
        request = read(SKILL / "assets" / "request-m1-2.json")
        del request["inputs"]["paragraph_material"]
        result, code = m1.route(request)
        self.assertEqual(code, 1)
        self.assertEqual(result["outcome"], "needs_input")
        missing = [item for item in result["diagnostics"] if item["code"] == "missing_input"]
        self.assertEqual(missing[0]["repair_target"], "user")
        self.assertEqual(missing[0]["status"], "unverified")

    def test_unknown_input_does_not_become_not_applicable(self):
        self.request["inputs"]["work_type"] = {"state": "unknown", "reason": "Task type has not been supplied."}
        result, code = m1.route(self.request)
        self.assertEqual(code, 1)
        self.assertIn("unknown_input", codes(result))
        self.assertNotIn("not_applicable", [d["status"] for d in result["diagnostics"]])

    def test_wrong_node_id_and_version_are_rejected(self):
        for key, value, expected in (("target", "M5", "invalid_enum"),
                                     ("work_id", "wrong id", "invalid_id"),
                                     ("contract_version", "2.0.0", "incompatible_contract"),
                                     ("base_version", True, "invalid_version_or_order")):
            with self.subTest(key=key):
                request = copy.deepcopy(self.request)
                request[key] = value
                result, code = m1.route(request)
                self.assertEqual(code, 1)
                self.assertIn(expected, codes(result))

    def test_empty_workbrief_is_explicitly_partial(self):
        result, code = m1.check(self.empty)
        self.assertEqual(code, 0)
        self.assertEqual(result["outcome"], "incomplete")
        self.assertIn("partial_workbrief", codes(result))
        self.assertEqual(result["audit"]["overall"], "unverified")

    def test_combined_parent_result_checks_against_parent_request(self):
        result, code = m1.check(self.batch, self.request)
        self.assertEqual(code, 0, result)
        final_result, final_code = m1.check(self.full(), self.request)
        self.assertEqual(final_code, 0, final_result)
        self.assertEqual(final_result["audit"]["deterministic"], "pass")
        self.assertEqual(final_result["audit"]["overall"], "unverified")

    def test_batch_acceptance_preserves_all_child_partitions(self):
        work = self.full()
        self.assertEqual(set(work["content"]), set(m1.FIELDS))
        self.assertEqual(work["version"], 1)
        self.assertEqual(len(work["accepted_proposals"]), 3)
        for proposal in self.batch["proposals"]:
            for field, value in proposal["changes"].items():
                self.assertEqual(work["content"][field], value)

    def test_sequential_acceptance_preserves_siblings(self):
        work = self.empty
        first_intent = copy.deepcopy(self.batch["proposals"][0]["changes"]["intent"])
        for index, original in enumerate(self.batch["proposals"]):
            proposal = copy.deepcopy(original)
            proposal["base_version"] = index
            result, code = m1.accept(work, proposal)
            self.assertEqual(code, 0, result)
            work = result["work_brief"]
        self.assertEqual(work["version"], 3)
        self.assertEqual(work["content"]["intent"], first_intent)
        self.assertEqual(len(work["content"]["paragraphs"]), 3)

    def test_accept_does_not_mutate_input_objects(self):
        old, proposed = copy.deepcopy(self.empty), copy.deepcopy(self.batch)
        m1.accept(self.empty, self.batch)
        self.assertEqual(self.empty, old)
        self.assertEqual(self.batch, proposed)

    def test_cli_result_wrapper_is_not_mistaken_for_workbrief(self):
        wrapper, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 0)
        checked, checked_code = m1.check(wrapper)
        self.assertEqual(checked_code, 1)
        self.assertIn("unknown_artifact_kind", codes(checked))
        correct, correct_code = m1.check(wrapper["work_brief"])
        self.assertEqual(correct_code, 0, correct)

    def test_child_cannot_write_sibling_partition(self):
        proposal = self.batch["proposals"][0]
        proposal["changes"]["paragraphs"] = self.batch["proposals"][1]["changes"]["paragraphs"]
        result, code = m1.accept(self.empty, proposal)
        self.assertEqual(code, 1)
        self.assertIn("out_of_scope", codes(result))
        self.assertNotIn("work_brief", result)

    def test_cross_module_plan_and_h3_fields_are_rejected(self):
        for name in ("CameraPlan", "TimingMap", "CompilationResult", "summary", "detailed_description"):
            with self.subTest(field=name):
                proposal = copy.deepcopy(self.batch["proposals"][0])
                proposal["changes"][name] = {}
                result, code = m1.accept(self.empty, proposal)
                self.assertEqual(code, 1)
                self.assertIn("out_of_scope", codes(result))

    def test_competing_partition_writes_are_atomic_rejection(self):
        extra = copy.deepcopy(self.batch["proposals"][1])
        extra["proposal_id"] = "PROP-COMPETING"
        self.batch["proposals"].append(extra)
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 1)
        self.assertIn("competing_partition_write", codes(result))
        self.assertNotIn("work_brief", result)

    def test_duplicate_proposals_do_not_apply_twice(self):
        work = self.full()
        proposal = copy.deepcopy(self.batch["proposals"][0])
        proposal["base_version"] = work["version"]
        result, code = m1.accept(work, proposal)
        self.assertEqual(code, 1)
        self.assertIn("duplicate_proposal_id", codes(result))

    def test_stale_version_does_not_silently_rebase(self):
        result, code = m1.accept(self.full(), self.batch["proposals"][0])
        self.assertEqual(code, 1)
        self.assertIn("stale_base_version", codes(result))

    def test_work_id_mismatch_is_rejected(self):
        self.batch["proposals"][0]["work_id"] = "WORK-OTHER"
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 1)
        self.assertIn("work_id_mismatch", codes(result))

    def test_source_ids_are_immutable(self):
        self.batch["proposals"][1]["sources"]["SRC-WATER-CASE"]["excerpt"] = "Changed source text."
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 1)
        self.assertIn("source_identity_conflict", codes(result))

    def test_unresolved_source_reference_is_rejected(self):
        self.batch["proposals"][0]["changes"]["intent"]["source_refs"] = ["SRC-NOT-PROVIDED"]
        result, code = m1.check(self.batch)
        self.assertEqual(code, 1)
        self.assertIn("unresolved_source", codes(result))

    def test_required_event_coverage_is_checked(self):
        self.batch["proposals"][1]["changes"]["paragraphs"]["P03"]["must_keep_event_ids"].remove("KEEP-7")
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 1)
        self.assertIn("uncovered_keep_event", codes(result))

    def test_unknown_required_event_id_is_rejected(self):
        self.batch["proposals"][1]["changes"]["paragraphs"]["P03"]["must_keep_event_ids"].append("KEEP-NOT-EXIST")
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 1)
        self.assertIn("unknown_keep_event", codes(result))

    def test_information_cycle_is_reported(self):
        self.batch["proposals"][1]["changes"]["paragraphs"]["P01"]["information_predecessors"] = ["P03"]
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 1)
        self.assertIn("information_dependency_cycle", codes(result))

    def test_information_order_violation_is_reported(self):
        self.batch["proposals"][1]["changes"]["paragraphs"]["P02"]["order"] = 4
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 1)
        self.assertIn("information_order_conflict", codes(result))

    def test_unknown_motif_paragraph_is_rejected(self):
        self.batch["proposals"][2]["changes"]["motifs"]["MOTIF-PROGRESS"]["paragraph_ids"].append("P99")
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 1)
        self.assertIn("unknown_motif_paragraph", codes(result))

    def issue(self, owner="M1.1", blocking=True, status="conflict"):
        return {"id": "ISSUE-1", "code": "decision_needed", "status": status,
                "message": "A recorded decision is unresolved.", "owner_module": owner,
                "field": "/content/intent", "blocking": blocking, "source_refs": ["SRC-WATER-CASE"]}

    def test_declared_conflict_is_not_swallowed_by_aggregation(self):
        self.batch["proposals"][0]["issues"] = [self.issue()]
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 1)
        self.assertIn("declared_issue", codes(result))
        self.assertEqual(result["unresolved_issues"][0]["id"], "ISSUE-1")

    def test_conflict_cannot_be_downgraded_with_nonblocking_flag(self):
        self.batch["proposals"][0]["issues"] = [self.issue(blocking=False)]
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 1)
        self.assertNotIn("work_brief", result)

    def test_nonblocking_unknown_issue_is_retained_in_draft(self):
        self.batch["proposals"][0]["issues"] = [self.issue(blocking=False, status="unverified")]
        result, code = m1.accept(self.empty, self.batch)
        self.assertEqual(code, 0, result)
        self.assertEqual(result["work_brief"]["issues"][0]["status"], "unverified")
        self.assertEqual(result["audit"]["overall"], "unverified")

    def test_child_cannot_clear_external_parent_or_sibling_blocker(self):
        for owner in ("M2", "M12", "M1", "user", "M1.2"):
            with self.subTest(owner=owner):
                current = copy.deepcopy(self.empty)
                current["issues"] = [self.issue(owner=owner)]
                proposal = copy.deepcopy(self.batch["proposals"][0])
                proposal["resolutions"] = [{"issue_id": "ISSUE-1", "reason": "Claimed fixed.", "source_refs": ["SRC-WATER-CASE"]}]
                result, code = m1.accept(current, proposal)
                self.assertEqual(code, 1)
                self.assertIn("resolution_out_of_scope", codes(result))
                self.assertEqual(result["unresolved_issues"][0]["owner_module"], owner)

    def test_owner_resolution_keeps_historical_issue_and_evidence(self):
        self.empty["issues"] = [self.issue()]
        proposal = copy.deepcopy(self.batch["proposals"][0])
        proposal["resolutions"] = [{"issue_id": "ISSUE-1", "reason": "The owner explicitly records its revised decision.",
                                   "source_refs": ["SRC-WATER-CASE"]}]
        result, code = m1.accept(self.empty, proposal)
        self.assertEqual(code, 0, result)
        self.assertEqual(result["work_brief"]["issues"], [])
        historical = result["work_brief"]["accepted_proposals"][0]["resolved_issues"][0]
        self.assertEqual(historical["issue"]["status"], "conflict")
        self.assertTrue(historical["reason"])

    def test_resolution_requires_a_real_existing_issue(self):
        proposal = self.batch["proposals"][0]
        proposal["resolutions"] = [{"issue_id": "ISSUE-MISSING", "reason": "Claimed fixed.", "source_refs": ["SRC-WATER-CASE"]}]
        result, code = m1.accept(self.empty, proposal)
        self.assertEqual(code, 1)
        self.assertIn("unknown_resolution", codes(result))

    def test_repair_of_existing_consistency_failure_returns_to_owner(self):
        current = self.full()
        current["content"]["paragraphs"]["P03"]["must_keep_event_ids"].remove("KEEP-7")
        broken, code = m1.check(current)
        self.assertEqual(code, 1)
        item = next(d for d in broken["diagnostics"] if d["code"] == "uncovered_keep_event")
        self.assertEqual(item["repair_target"], "M1.2")
        proposal = copy.deepcopy(self.batch["proposals"][1])
        proposal["proposal_id"] = "PROP-REPAIR-PARAGRAPHS"
        proposal["base_version"] = current["version"]
        repaired, repaired_code = m1.accept(current, proposal)
        self.assertEqual(repaired_code, 0, repaired)
        self.assertIn("KEEP-7", repaired["work_brief"]["content"]["paragraphs"]["P03"]["must_keep_event_ids"])

    def test_partial_request_does_not_allow_extra_owned_writes(self):
        request = read(SKILL / "assets" / "request-m1-1.json")
        request["requested_fields"] = ["constraints"]
        proposal = self.batch["proposals"][0]
        result, code = m1.check(proposal, request)
        self.assertEqual(code, 1)
        self.assertIn("unrequested_write", codes(result))
        proposal["changes"] = {"constraints": proposal["changes"]["constraints"]}
        result, code = m1.check(proposal, request)
        self.assertEqual(code, 0, result)

    def test_request_and_output_identity_are_checked(self):
        request = read(SKILL / "assets" / "request-m1-1.json")
        proposal = self.batch["proposals"][0]
        proposal["source_request_id"] = "REQ-OTHER"
        result, code = m1.check(proposal, request)
        self.assertEqual(code, 1)
        self.assertIn("request_id_mismatch", codes(result))

    def test_request_source_id_cannot_be_rebound(self):
        request = read(SKILL / "assets" / "request-m1-1.json")
        for field in ("version", "excerpt", "locator"):
            with self.subTest(source_field=field):
                proposal = copy.deepcopy(self.batch["proposals"][0])
                proposal["sources"]["SRC-WATER-CASE"][field] = "different"
                result, code = m1.check(proposal, request)
                self.assertEqual(code, 1)
                self.assertIn("source_identity_conflict", codes(result))

    def test_parent_request_checks_each_child_source(self):
        self.batch["proposals"][2]["sources"]["SRC-WATER-CASE"]["version"] = "another-version"
        result, code = m1.check(self.batch, self.request)
        self.assertEqual(code, 1)
        self.assertIn("source_identity_conflict", codes(result))

    def test_unused_request_sources_can_be_omitted(self):
        request = read(SKILL / "assets" / "request-m1-1.json")
        request["sources"]["SRC-UNUSED"] = {
            "kind": "external_input", "locator": "user:unused-context", "version": "1", "excerpt": "Not used by this scope."
        }
        result, code = m1.check(self.batch["proposals"][0], request)
        self.assertEqual(code, 0, result)

    def test_new_design_source_is_allowed_with_request(self):
        request = read(SKILL / "assets" / "request-m1-1.json")
        proposal = self.batch["proposals"][0]
        proposal["sources"]["SRC-NEW-DESIGN"] = {
            "kind": "design_decision", "locator": "fixture:additional-review", "version": "1", "excerpt": "Explicitly recorded design interpretation."
        }
        proposal["changes"]["intent"]["source_refs"].append("SRC-NEW-DESIGN")
        result, code = m1.check(proposal, request)
        self.assertEqual(code, 0, result)

    def test_known_request_work_type_cannot_be_switched(self):
        request = read(SKILL / "assets" / "request-m1-1.json")
        self.batch["proposals"][0]["changes"]["intent"]["work_type"] = "mv"
        result, code = m1.check(self.batch["proposals"][0], request)
        self.assertEqual(code, 1)
        self.assertIn("work_type_mismatch", codes(result))

    def test_known_request_work_type_cannot_be_lost_as_unknown(self):
        request = read(SKILL / "assets" / "request-m1-1.json")
        self.batch["proposals"][0]["changes"]["intent"]["work_type"] = {"state": "unknown", "reason": "Ignored supplied type."}
        result, code = m1.check(self.batch["proposals"][0], request)
        self.assertEqual(code, 1)
        self.assertIn("known_work_type_lost", codes(result))

    def consumers(self, work):
        work["consumers"] = [
            {"consumer_id": "ACTION-P01", "module_id": "M4", "version": 1,
             "source_work_version": work["version"], "read_paths": ["/content/paragraphs/P01"]},
            {"consumer_id": "ACTION-P02", "module_id": "M4", "version": 1,
             "source_work_version": work["version"], "read_paths": ["/content/paragraphs/P02"]},
            {"consumer_id": "AUDIT-WORK", "module_id": "M12", "version": 1,
             "source_work_version": work["version"], "read_paths": ["/content"]},
        ]
        return work

    def test_impact_marks_only_declared_overlapping_dependencies(self):
        previous = self.consumers(self.full())
        current = copy.deepcopy(previous)
        current["version"] += 1
        current["content"]["paragraphs"]["P01"]["function"] += " 强调目标建立。"
        result, code = m1.impact(previous, current)
        self.assertEqual(code, 0, result)
        self.assertEqual({x["consumer_id"] for x in result["stale_consumers"]}, {"ACTION-P01", "AUDIT-WORK"})
        self.assertEqual({x["consumer_id"] for x in result["unaffected_consumers"]}, {"ACTION-P02"})
        self.assertEqual(result["unregistered_consumer_coverage"], "unknown")

    def test_display_rename_does_not_invalidate_semantic_consumers(self):
        previous = self.consumers(self.full())
        current = copy.deepcopy(previous)
        current["version"] += 1
        current["display"]["title"] = "同一作品的新展示名称"
        result, code = m1.impact(previous, current)
        self.assertEqual(code, 0)
        self.assertEqual(result["stale_consumers"], [])
        self.assertEqual(result["changed_dependency_paths"], [])
        self.assertIn("/display/title", result["ignored_metadata_paths"])

    def test_internal_child_dependencies_are_registered_and_invalidated(self):
        previous = self.full()
        previous["consumers"] = [
            {"consumer_id": "M1-PARENT", "module_id": "M1", "version": 1, "source_work_version": 1, "read_paths": ["/content/intent"]},
            {"consumer_id": "M1-INTENT", "module_id": "M1.1", "version": 1, "source_work_version": 1, "read_paths": ["/content/constraints"]},
            {"consumer_id": "M1-PARAGRAPHS", "module_id": "M1.2", "version": 1, "source_work_version": 1, "read_paths": ["/content/intent"]},
            {"consumer_id": "M1-EMOTION", "module_id": "M1.3", "version": 1, "source_work_version": 1, "read_paths": ["/content/intent"]},
        ]
        current = copy.deepcopy(previous)
        current["version"] += 1
        current["content"]["intent"]["creative_goal"] += " 强调原案的因果反转。"
        result, code = m1.impact(previous, current)
        self.assertEqual(code, 0, result)
        self.assertEqual({x["module_id"] for x in result["stale_consumers"]}, {"M1", "M1.2", "M1.3"})
        self.assertEqual(result["unaffected_consumers"][0]["module_id"], "M1.1")

    def test_undeclared_consumers_are_not_invented(self):
        previous = self.full()
        current = copy.deepcopy(previous)
        current["version"] += 1
        current["content"]["intent"]["creative_goal"] += " 保持原案。"
        result, code = m1.impact(previous, current)
        self.assertEqual(code, 0)
        self.assertEqual(result["stale_consumers"], [])
        self.assertEqual(result["transitive_discovery"], "not_implemented")

    def test_old_dependency_baseline_is_unverified(self):
        previous = self.consumers(self.full())
        previous["consumers"][0]["source_work_version"] = 0
        current = copy.deepcopy(previous)
        current["version"] += 1
        current["display"]["title"] += "改名"
        result, code = m1.impact(previous, current)
        self.assertEqual(code, 0)
        self.assertEqual(result["preexisting_unverified_consumers"][0]["consumer_id"], "ACTION-P01")

    def test_invalid_dependency_pointer_is_rejected(self):
        work = self.consumers(self.full())
        work["consumers"][0]["read_paths"] = ["/content/paragraphs/P99"]
        result, code = m1.check(work)
        self.assertEqual(code, 1)
        self.assertIn("unresolved_dependency_path", codes(result))

    def test_mv_fixture_preserves_unknown_audio_and_has_no_new_story(self):
        empty = read(HERE / "fixtures" / "mv-empty.json")
        batch = read(HERE / "fixtures" / "mv-batch.json")
        request = read(HERE / "fixtures" / "mv-request.json")
        result, code = m1.accept(empty, batch)
        self.assertEqual(code, 0, result)
        work = result["work_brief"]
        self.assertEqual(work["content"]["intent"]["work_type"], "mv")
        self.assertEqual(work["content"]["emotion_energy"]["P01"]["energy_intent"]["state"], "unknown")
        checked, checked_code = m1.check(work, request)
        self.assertEqual(checked_code, 0, checked)
        self.assertEqual(checked["audit"]["media"], "unverified")
        self.assertNotIn("target_duration", work["content"]["intent"])

    def test_malformed_field_types_return_diagnostics(self):
        for original in (self.empty, self.request, self.batch["proposals"][0], self.batch):
            for key in original:
                with self.subTest(kind=original["kind"], field=key):
                    malformed = copy.deepcopy(original)
                    malformed[key] = ["wrong", {"type": True}]
                    result, code = m1.check(malformed)
                    self.assertEqual(code, 1, result)
                    self.assertEqual(result["audit"]["overall"], "fail")

    def test_public_registry_matches_implemented_permissions(self):
        registry = read(SKILL / "references" / "module-registry.json")
        self.assertEqual(registry["contract_version"], m1.CONTRACT_VERSION)
        self.assertEqual(set(registry["nodes"]), set(m1.MODULES))
        for node in m1.MODULES:
            self.assertEqual(registry["nodes"][node]["minimum_input"]["projected_inputs"], list(m1.INPUTS[node]))
            self.assertEqual(registry["nodes"][node]["owned_content_partitions"], list(m1.fields_for(node)))

    def test_copied_skill_runs_without_repository_siblings(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            cloned = base / "h3-work-intent"
            shutil.copytree(SKILL, cloned, ignore=shutil.ignore_patterns("__pycache__"))
            cli = cloned / "scripts" / "m1_contract.py"
            paths = [cloned / "assets" / "workbrief-empty.json", cloned / "assets" / "proposal-m1-1.json"]
            before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]
            routed = subprocess.run([sys.executable, str(cli), "route", str(cloned / "assets" / "request-m1-2.json")],
                                    cwd=base, text=True, capture_output=True, check=False)
            self.assertEqual(routed.returncode, 0, routed.stderr + routed.stdout)
            accepted = subprocess.run([sys.executable, str(cli), "accept", *(str(p) for p in paths)],
                                      cwd=base, text=True, capture_output=True, check=False)
            self.assertEqual(accepted.returncode, 0, accepted.stderr + accepted.stdout)
            work = json.loads(accepted.stdout)["work_brief"]
            result_path = base / "new-workbrief.json"
            result_path.write_text(json.dumps(work), encoding="utf-8")
            checked = subprocess.run([sys.executable, str(cli), "check", str(result_path)],
                                     cwd=base, text=True, capture_output=True, check=False)
            self.assertEqual(checked.returncode, 0, checked.stderr + checked.stdout)
            self.assertEqual(before, [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths])
            self.assertFalse(json.loads(accepted.stdout)["execution"]["input_files_modified"])

    def test_duplicate_json_keys_and_nonfinite_numbers_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.json"
            for content in ('{"kind":"WorkBrief","kind":"M1Request"}', '{"version":NaN}'):
                with self.subTest(content=content):
                    path.write_text(content, encoding="utf-8")
                    result = subprocess.run([sys.executable, str(SCRIPT), "check", str(path)],
                                            text=True, capture_output=True, check=False)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("input_or_resource_error", codes(json.loads(result.stdout)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
