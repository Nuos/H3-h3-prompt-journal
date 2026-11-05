"""M3 contract regression tests. Fixtures are D-class designs, not media evidence."""
import copy
import importlib.util
import itertools
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / "h3-scene-blocking"
SPEC = importlib.util.spec_from_file_location("m3_contract", SKILL / "scripts/m3_contract.py")
m3 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m3)
DEFS = json.loads((SKILL / "references/contracts.json").read_text())["$defs"]


def fixture(name):
    return json.loads((SKILL / "assets" / name).read_text())


class M3Contracts(unittest.TestCase):
    def setUp(self):
        self.state = fixture("state-empty.json")
        self.batch = fixture("proposal-batch.json")
        self.requests = fixture("requests.json")
        self.check = m3.Check(DEFS)

    def codes(self, checker=None):
        return {d["code"] for d in (checker or self.check).diagnostics}

    def proposal(self, n):
        return self.batch["proposals"][n - 1]

    def accept(self, state=None, batch=None, requests=None):
        return m3.accept(self.check, state or self.state, batch or self.batch, self.requests if requests is None else requests)

    def assert_clean(self):
        self.assertFalse(self.check.failed, json.dumps(self.check.diagnostics, ensure_ascii=False, indent=2))

    def cli(self, *args, skill=None):
        result = subprocess.run([sys.executable, str((skill or SKILL) / "scripts/m3_contract.py"), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def test_all_public_inputs_and_standalone_children(self):
        for artifact in [self.state, self.batch, fixture("request-m3.json"), *self.requests, *self.batch["proposals"]]:
            with self.subTest(kind=artifact["kind"], id=artifact.get("module_id", artifact.get("target"))):
                checker = m3.Check(DEFS)
                checker.artifact(artifact)
                self.assertFalse(checker.failed, checker.diagnostics)
        for p, r in zip(self.batch["proposals"], self.requests):
            m3.request_match(self.check, p, r)
        self.assert_clean()

    def test_atomic_combination_and_no_input_mutation(self):
        original = copy.deepcopy((self.state, self.batch, self.requests))
        accepted, status = self.accept()
        self.assert_clean()
        self.assertEqual(status, "accepted_draft")
        self.assertEqual(accepted["version"], 1)
        self.assertEqual(len(accepted["accepted_proposals"]), 3)
        self.assertEqual((self.state, self.batch, self.requests), original)
        self.assertEqual(accepted["status"], "draft")

    def test_scene_only_and_static_no_routes(self):
        self.batch["proposals"] = [self.proposal(1)]
        accepted, status = self.accept(requests=self.requests[:1])
        self.assert_clean()
        self.assertEqual(status, "accepted_draft")
        self.assertEqual(accepted["content"]["blocking"], m3.EMPTY["blocking"])
        self.check = m3.Check(DEFS)
        p = fixture("proposal-m3-2.json")
        p["changes"]["blocking"]["routes"] = {}
        self.check.artifact(p)
        self.assert_clean()

    def test_registry_routing_all_targets_and_flags(self):
        for suffix in ("", "-1", "-2", "-3"):
            path = SKILL / ("assets/request-m3" + suffix + ".json")
            code, result = self.cli("route", path)
            self.assertEqual(code, 0)
            self.assertEqual(result["route"]["execution"], "not_invoked")
            self.assertIn("module-registry.json", result["trace"]["resources"])
            self.assertTrue(result["route"]["input_mapping"])
            self.assertIn("references/contract-guide.md", result["route"]["resources"])
            self.assertIn("references/contracts.json", result["route"]["machine_dependencies"])
        code, result = self.cli("route", "--request", SKILL / "assets/request-m3-1.json")
        self.assertEqual(code, 0)
        self.assertEqual(result["route"]["target"], "M3.1")

    def test_missing_minimum_and_unknown_brief(self):
        request = self.requests[1]
        del request["inputs"]["topology_context"]
        self.check.artifact(request)
        self.assertIn("missing_minimum_input", self.codes())
        self.check = m3.Check(DEFS)
        request = self.requests[0]
        request["inputs"]["scene_brief"] = {"state": "unknown", "reason": "等待场景说明"}
        self.check.artifact(request)
        self.assert_clean()
        self.assertIn("unknown_brief", self.codes())

    def test_unknown_fields_bad_ids_and_boolean_integer_rejected(self):
        mutations = [lambda r: r.update(extra="forbidden"), lambda r: r.update(base_version=True), lambda r: r.update(request_id="1bad"), lambda r: r.update(kind=[])]
        for change in mutations:
            r = copy.deepcopy(self.requests[0]); change(r)
            checker = m3.Check(DEFS); checker.artifact(r)
            self.assertTrue(checker.failed)

    def test_large_integer_and_nonfinite_vectors(self):
        p = self.proposal(2)
        p["changes"]["blocking"]["placements"]["P_b"]["position"][0] = 10 ** 400
        self.check.artifact(p)
        self.assert_clean()
        self.check = m3.Check(DEFS)
        p["changes"]["blocking"]["placements"]["P_b"]["position"][0] = float("inf")
        self.check.artifact(p)
        self.assertTrue(self.check.failed)

    def test_strict_json_loader(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            for text in ('{"a":1,"a":2}', '{"n":NaN}', '{"n":Infinity}'):
                path.write_text(text)
                code, value = self.cli("check", path)
                self.assertEqual(code, 2)
                self.assertEqual(value["execution"], "failed")

    def test_owner_boundary_and_duplicate_partition(self):
        p = self.proposal(1)
        p["changes"]["blocking"] = copy.deepcopy(m3.EMPTY["blocking"])
        self.check.artifact(p)
        self.assertIn("cross_owner_write", self.codes())
        self.check = m3.Check(DEFS)
        self.batch = fixture("proposal-batch.json")
        duplicate = copy.deepcopy(self.proposal(1)); duplicate["proposal_id"] = "PROP_competitor"
        self.batch["proposals"].append(duplicate)
        self.accept()
        self.assertIn("competing_partition_proposals", self.codes())

    def test_actual_request_fidelity_and_sources(self):
        for field in ("context", "sources", "source_request_id", "work_id", "base_version", "module_id"):
            p = fixture("proposal-m3-2.json")
            if field == "context": p[field]["blocking_brief"] = "偷偷改变请求"
            elif field == "sources": p[field]["S_fixture"]["excerpt"] = "被改写的证据"
            elif field == "base_version": p[field] = 3
            elif field == "module_id": p[field] = "M3.1"
            else: p[field] = "DIFFERENT"
            checker = m3.Check(DEFS); m3.request_match(checker, p, self.requests[1])
            self.assertIn("request_mismatch", self.codes(checker), field)
        self.check = m3.Check(DEFS)
        self.accept(requests=[])
        self.assertIn("missing_original_request", self.codes())

    def test_standalone_dependencies_cannot_disappear_at_acceptance(self):
        for n in (2, 3):
            checker = m3.Check(DEFS)
            p = fixture(f"proposal-m3-{n}.json")
            checker.artifact(p)
            self.assertFalse(checker.failed)
            batch = fixture("proposal-batch.json"); batch["proposals"] = [p]
            m3.accept(checker, self.state, batch, [self.requests[n - 1]])
            self.assertIn("composition_projection_mismatch", self.codes(checker))

    def test_candidate_projection_mutation_is_rejected(self):
        self.proposal(1)["changes"]["topology"]["regions"]["R_north"]["description"] = "候选不同于消费者所读"
        self.accept()
        self.assertIn("composition_projection_mismatch", self.codes())

    def test_entity_projection_cannot_be_rewritten(self):
        self.proposal(2)["changes"]["blocking"]["entities"]["E_a"]["description"] = "另一身份"
        self.check.artifact(self.proposal(2))
        self.assertIn("entity_projection_changed", self.codes())
        self.assertIn("/changes/blocking/entities", [d["path"] for d in self.check.diagnostics])

    def test_unknown_frame_region_entity_and_source(self):
        for field, code in (("frame_id", "unresolved_frame"), ("region_id", "unresolved_region"), ("entity_id", "unresolved_entity")):
            p = fixture("proposal-m3-2.json"); p["changes"]["blocking"]["placements"]["P_b"][field] = "MISSING"
            checker = m3.Check(DEFS); checker.artifact(p)
            self.assertIn(code, self.codes(checker))
        p = fixture("proposal-m3-1.json"); p["changes"]["topology"]["regions"]["R_north"]["source_refs"] = ["MISSING"]
        self.check.artifact(p)
        self.assertIn("unresolved_source", self.codes())

    def test_path_connectivity_direction_and_closed_region(self):
        for mutation in ("disconnect", "reverse", "closed"):
            p = fixture("proposal-m3-2.json"); topology = p["context"]["topology_context"]
            if mutation == "disconnect": topology["connections"] = {}
            elif mutation == "reverse": topology["connections"]["C_walk"].update(direction="forward", from_region="R_north", to_region="R_south")
            else: topology["regions"]["R_north"]["traversable"] = False
            checker = m3.Check(DEFS); checker.artifact(p)
            self.assertIn("nontraversable_route" if mutation == "closed" else "disconnected_route", self.codes(checker))

    def test_route_can_revisit_a_region(self):
        p = self.proposal(2)
        p["changes"]["blocking"]["routes"]["RT_a"]["region_path"] = ["R_south", "R_north", "R_south", "R_north"]
        self.check.artifact(p)
        self.assert_clean()

    def test_same_phase_conflicts_are_order_independent(self):
        base = fixture("proposal-m3-2.json")
        known = copy.deepcopy(base["changes"]["blocking"]["placements"]["P_b"])
        other = copy.deepcopy(known); other["position"] = [9, 3, 0]
        unknown = copy.deepcopy(known); unknown["position"] = {"state": "unknown", "reason": "未提供"}; unknown["facing"] = {"state": "unknown", "reason": "未提供"}
        for order in itertools.permutations([unknown, known, other]):
            p = copy.deepcopy(base); p["changes"]["blocking"]["routes"] = {}
            p["changes"]["blocking"]["placements"] = {f"P_{i}": v for i, v in enumerate(order)}
            checker = m3.Check(DEFS); checker.artifact(p)
            self.assertIn("same_phase_placement_conflict", self.codes(checker))

    def test_distinct_scopes_shared_regions_and_scaled_directions(self):
        for field in ("phase", "shot_id"):
            p = fixture("proposal-m3-2.json"); placements = p["changes"]["blocking"]["placements"]
            other = copy.deepcopy(placements["P_b"]); other["scope"][field] = "OTHER"; other["position"] = [9, 0, 0]
            placements["P_other"] = other
            checker = m3.Check(DEFS); checker.artifact(p)
            self.assertFalse(checker.failed, checker.diagnostics)
        p = fixture("proposal-m3-2.json"); placements = p["changes"]["blocking"]["placements"]
        other = copy.deepcopy(placements["P_b"]); other["facing"] = [0, 9, 0]; placements["P_same"] = other
        placements["P_b"]["position"] = placements["P_a_end"]["position"]
        other["position"] = placements["P_b"]["position"]
        self.check.artifact(p)
        self.assert_clean()

    def test_screen_frame_view_and_body_anchor(self):
        for space, code in (("screen", "missing_view_context"), ("entity_local", "missing_frame_anchor")):
            p = fixture("proposal-m3-1.json"); p["changes"]["topology"]["frames"]["F_world"]["space"] = space
            checker = m3.Check(DEFS); checker.artifact(p)
            self.assertIn(code, self.codes(checker))
        p = self.proposal(1); frame = p["changes"]["topology"]["frames"]["F_world"]
        frame.update(space="screen", view_context={"state":"unknown","reason":"M5 未选观看条件"})
        self.check.artifact(p)
        self.assert_clean()
        self.assertIn("screen_projection_unverified", self.codes())

    def test_interaction_route_entity_region_and_scope(self):
        for case, code in (("route", "unresolved_route"), ("participant", "interaction_route_entity_mismatch"), ("region", "interaction_route_region_mismatch"), ("scope", "interaction_route_scope_mismatch")):
            p = fixture("proposal-m3-3.json"); interaction = p["changes"]["interactions"]["relations"]["I_contact"]
            if case == "route": interaction["route_ids"] = ["MISSING"]
            elif case == "participant":
                p["context"]["blocking_context"]["entities"]["E_other"] = copy.deepcopy(p["context"]["blocking_context"]["entities"]["E_a"])
                interaction["participants"] = ["E_b", "E_other"]
            elif case == "region":
                topology = p["context"]["topology_context"]; topology["regions"]["R_other"] = copy.deepcopy(topology["regions"]["R_north"]); interaction["region_id"] = "R_other"
            else: interaction["scope"]["shot_id"] = "SH_other"
            checker = m3.Check(DEFS); checker.artifact(p)
            self.assertIn(code, self.codes(checker))

    def test_unknown_interaction_timing_is_not_hard_failure(self):
        p = self.proposal(3)
        p["changes"]["interactions"]["relations"]["I_contact"]["scope"]["phase"] = {"state":"unknown","reason":"排时未定"}
        self.check.artifact(p)
        self.assert_clean()
        self.assertIn("scope_unverified", self.codes())

    def test_explicit_region_exclusion_and_occlusion_conflicts(self):
        p = fixture("proposal-m3-3.json")
        p["context"]["topology_context"]["regions"]["R_north"]["exclusive_with"] = ["R_south"]
        p["context"]["blocking_context"]["placements"]["P_b"]["region_id"] = "R_south"
        self.check.artifact(p)
        self.assertIn("interaction_placement_conflict", self.codes())
        self.check = m3.Check(DEFS)
        p = self.proposal(3); relations = p["changes"]["interactions"]["relations"]
        relations["I_contact"].update(occlusion="allowed", view_context="正面中景", occlusion_target={"occluder_id":"E_a","occluded_id":"E_b","part":"face"})
        other = copy.deepcopy(relations["I_contact"]); other["occlusion"] = "forbidden"; relations["I_other"] = other
        self.check.artifact(p)
        self.assertIn("conflicting_occlusion_policy", self.codes())

    def test_occlusion_targets_keep_parts_and_directions_separate(self):
        for variant in ("part", "direction", "unknown"):
            p = fixture("proposal-m3-3.json")
            relations = p["changes"]["interactions"]["relations"]
            first = relations["I_contact"]
            first.update(occlusion="allowed", view_context="front", occlusion_target={"occluder_id":"E_a", "occluded_id":"E_b", "part":"hand"})
            other = copy.deepcopy(first); other["occlusion"] = "forbidden"
            if variant == "part": other["occlusion_target"]["part"] = "face"
            elif variant == "direction": other["occlusion_target"].update(occluder_id="E_b", occluded_id="E_a")
            else: other.pop("occlusion_target")
            relations["I_other"] = other
            checker = m3.Check(DEFS); checker.artifact(p)
            self.assertFalse(checker.failed, checker.diagnostics)
            if variant == "unknown": self.assertIn("occlusion_target_unverified", self.codes(checker))
        other["occlusion_target"] = {"occluder_id":"E_a", "occluded_id":"UNDECLARED", "part":"face"}
        checker = m3.Check(DEFS); checker.artifact(p)
        self.assertIn("invalid_occlusion_target", self.codes(checker))

    def test_batch_check_rejects_nonrequest_in_original_request_array(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mixed.json"
            path.write_text(json.dumps([*self.requests, self.state]))
            code, result = self.cli("check", SKILL / "assets/proposal-batch.json", "--requests", path)
            self.assertEqual(code, 1)
            self.assertIn("wrong_request_kind", {d["code"] for d in result["diagnostics"]})

    def test_new_issue_cannot_be_immediately_resolved_by_same_proposal(self):
        proposal = self.proposal(1)
        proposal["issues"]["ISS_new"] = {"owner":"M3.1", "state":"open", "blocking":True, "description":"unresolved conflict", "source_refs":["S_fixture"]}
        proposal["resolutions"] = [{"issue_id":"ISS_new", "description":"claimed resolved immediately", "source_refs":["S_fixture"]}]
        state, status = self.accept()
        self.assertIsNone(state)
        self.assertEqual(status, "rejected")
        self.assertIn("invalid_issue_resolution", self.codes())

    def test_version_replay_id_reuse_and_stale_revision(self):
        accepted, _ = self.accept(); self.assert_clean()
        checker = m3.Check(DEFS); replay, status = m3.accept(checker, accepted, self.batch, self.requests)
        self.assertEqual(status, "idempotent_replay"); self.assertEqual(replay, accepted)
        changed = copy.deepcopy(self.batch); changed["proposals"][0]["changes"]["topology"]["regions"]["R_north"]["description"] += " 修改"
        checker = m3.Check(DEFS); m3.accept(checker, accepted, changed, self.requests)
        self.assertIn("proposal_id_reused", self.codes(checker))
        changed = copy.deepcopy(self.batch)
        for p in changed["proposals"]: p["proposal_id"] += "_new"
        checker = m3.Check(DEFS); m3.accept(checker, accepted, changed, self.requests)
        self.assertIn("stale_base_version", self.codes(checker))

    def test_source_immutability_and_accepted_id_retention(self):
        accepted, _ = self.accept(); self.assert_clean()
        for case, code in (("source", "source_identity_mutation"), ("delete", "accepted_id_deletion")):
            batch = fixture("proposal-batch.json"); p = batch["proposals"][0]; batch["proposals"] = [p]
            batch["base_version"] = p["base_version"] = 1; p["proposal_id"] = "PROP_revision"
            request = fixture("request-m3-1.json"); request["base_version"] = 1
            if case == "source":
                p["sources"]["S_fixture"]["version"] = request["sources"]["S_fixture"]["version"] = "mutated"
            else: del p["changes"]["topology"]["connections"]["C_walk"]
            checker = m3.Check(DEFS); m3.accept(checker, accepted, batch, [request])
            self.assertIn(code, self.codes(checker))

    def test_issue_owner_and_open_blocker(self):
        issue = {"owner":"M3.1","state":"open","blocking":True,"description":"空间要求冲突待澄清","source_refs":["S_fixture"]}
        self.proposal(1)["issues"]["ISS_conflict"] = issue
        self.accept()
        self.assertIn("open_blocking_issue", self.codes())
        self.check = m3.Check(DEFS); issue["owner"] = "M3.2"
        self.check.artifact(self.proposal(1))
        self.assertIn("issue_owner_violation", self.codes())

    def test_impact_only_actual_scoped_reads(self):
        accepted, _ = self.accept(); self.assert_clean()
        accepted["display"] = {"title":"初稿"}
        accepted["consumers"] = {
            "C_motion":{"module_id":"M4","result_version":1,"source_state_version":1,"read_paths":["/content/blocking/routes"]},
            "C_display":{"module_id":"M11","result_version":1,"source_state_version":1,"read_paths":["/display"]},
            "C_old":{"module_id":"M8","result_version":1,"source_state_version":0,"read_paths":["/content/topology"]}}
        after = copy.deepcopy(accepted); after["version"] = 2; after["display"]["title"] = "改标题"
        checker = m3.Check(DEFS); report = m3.impact(checker, accepted, after)
        self.assertFalse(checker.failed, checker.diagnostics)
        self.assertEqual(report["consumers"]["C_motion"]["status"], "unaffected_by_declared_changes")
        self.assertEqual(report["consumers"]["C_display"]["status"], "stale")
        self.assertEqual(report["consumers"]["C_old"]["status"], "stale")
        self.assertEqual(report["unregistered_consumers"], "unverified")

    def test_copy_has_no_sibling_or_repository_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "standalone-skill"
            shutil.copytree(SKILL, copied)
            code, result = self.cli("accept", copied / "assets/state-empty.json", copied / "assets/proposal-batch.json", "--requests", copied / "assets/requests.json", skill=copied)
            self.assertEqual(code, 0, result)
            self.assertEqual(result["disposition"], "accepted_draft")
            self.assertEqual(result["validation"]["overall"], "unverified")
            self.assertIn("geometric_collision_and_contact", result["validation"]["unverified"])
            (copied / "references/module-registry.json").unlink()
            code, result = self.cli("route", copied / "assets/request-m3.json", skill=copied)
            self.assertEqual(code, 2)

    def test_optional_full_schema_cross_check(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is not installed; standard-library checks are the required runtime.")
        schema = json.loads((SKILL / "references/contracts.json").read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        validator = jsonschema.Draft202012Validator(schema)
        for artifact in [self.state, self.batch, *self.requests, *self.batch["proposals"]]:
            validator.validate(artifact)


if __name__ == "__main__":
    unittest.main(verbosity=2)
