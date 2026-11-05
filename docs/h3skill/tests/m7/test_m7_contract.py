#!/usr/bin/env python3
"""D-class behavioral/negative tests. No fixture is a media observation."""
from __future__ import annotations
import copy
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

PACKAGE = Path(__file__).resolve().parents[2] / "h3-time-synchronization"
SCRIPT = PACKAGE / "scripts/m7_contract.py"
spec = importlib.util.spec_from_file_location("m7_contract_under_test", SCRIPT)
m7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m7)
DEFS = json.loads((PACKAGE / "references/contracts.json").read_text())["$defs"]


def fixture(name):
    return json.loads((PACKAGE / "assets" / name).read_text())


def pair(n):
    return (fixture(f"proposal-standalone-m7-{n}.json"), fixture(f"request-standalone-m7-{n}.json"))


def checked(proposal, request):
    check = m7.Check(DEFS)
    check.proposal(proposal, request)
    return check


def codes(check):
    return {d["code"] for d in check.diagnostics if d["blocking"]}


def accepted(state=None, batch=None, requests=None):
    check = m7.Check(DEFS)
    result = m7.accept(check, state if state is not None else fixture("state-empty.json"),
                       batch if batch is not None else fixture("proposal-batch.json"),
                       requests if requests is not None else fixture("requests.json"))
    return check, result


def cli(*args):
    process = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True, check=False)
    return process.returncode, json.loads(process.stdout)


class ExactMath(unittest.TestCase):
    def test_rational_values_and_booleans(self):
        self.assertEqual(m7.rational("0.5"), Fraction(1, 2))
        self.assertEqual(m7.rational("30000/1001"), Fraction(30000, 1001))
        for value in (True, False, float("nan"), float("inf"), "1/0", "NaN", "Infinity"):
            with self.subTest(value=repr(value)), self.assertRaises(ValueError):
                m7.rational(value)

    def test_seconds_milliseconds_are_exact(self):
        self.assertEqual(m7.convert_value("1500", "ms", "s"), Fraction(3, 2))
        self.assertEqual(m7.convert_value("1/3", "s", "ms"), Fraction(1000, 3))

    def test_2997_is_not_30(self):
        self.assertEqual(m7.convert_value(30000, "frames", "s", fps="30000/1001"), 1001)
        self.assertEqual(m7.convert_value(30000, "frames", "s", fps=30), 1000)
        self.assertNotEqual(m7.convert_value(30000, "frames", "s", fps="29.97"), 1001)

    def test_beat_origin_is_never_inferred(self):
        with self.assertRaises(m7.MissingBasis):
            m7.convert_value(2, "beats", "s", bpm=120)
        self.assertEqual(m7.convert_value(2, "beats", "s", bpm=120, origin="1/4"), Fraction(5, 4))

    def test_nearest_half_tie_later_not_bankers(self):
        n, tq, error = m7.quantize_value("1/48", 24, "nearest")
        self.assertEqual((n, tq, error), (1, Fraction(1, 24), Fraction(1, 48)))
        self.assertEqual(m7.quantize_value("1/48", 24, "floor")[0], 0)
        self.assertEqual(m7.quantize_value("1/48", 24, "ceil")[0], 1)

    def test_nonzero_frame_zero_origin(self):
        self.assertEqual(m7.quantize_value(11, 24, "nearest", origin=10), (24, Fraction(11), Fraction(0)))
        with self.assertRaises(ValueError):
            m7.quantize_value(9, 24, "nearest", origin=10)

    def test_vfr_uses_pts_and_refuses_extrapolation(self):
        pts=[0,"1/25","9/100","3/20"]
        self.assertEqual(m7.quantize_value("1/10", 999, "nearest", pts=pts), (2, Fraction(9,100), Fraction(-1,100)))
        self.assertEqual(m7.quantize_value("1/10", 999, "ceil", pts=pts)[0], 3)
        with self.assertRaises(ValueError): m7.quantize_value("1/5", 30, "floor", pts=pts)
        with self.assertRaises(ValueError): m7.quantize_value(0, 30, "floor", pts=[0,0])

    def test_full_domain_chain_and_edit_quantization(self):
        work=m7.map_value(5,2,10,2)
        generation=m7.map_value(work,10,0,1)
        edit=m7.map_value(generation,0,5,1)
        self.assertEqual((work,generation,edit),(Fraction(23,2),Fraction(3,2),Fraction(13,2)))
        self.assertEqual(m7.quantize_value(edit,30,"nearest"),(195,Fraction(13,2),Fraction(0)))

    def test_linear_does_not_divide_by_zero_or_reverse(self):
        for speed in (0,-1):
            with self.subTest(speed=speed), self.assertRaises(ValueError):
                m7.map_value(5,2,10,speed)

    def test_cli_rational_error_and_tolerance(self):
        code,result=cli("quantize","--value","1","--fps","30000/1001","--rule","nearest","--tolerance","0.002")
        self.assertEqual(code,0)
        self.assertEqual((result["frame_index"],result["error_seconds"],result["within_tolerance"]),(30,"1/1000",True))
        self.assertFalse(result["media_verified"])
        code,result=cli("quantize","--value","1","--fps","30000/1001","--rule","nearest","--require-exact")
        self.assertEqual(code,1)
        self.assertEqual(result["validation"]["numeric_precision"],"fail")

    def test_cli_unknown_basis_no_fabricated_result(self):
        for args in [("quantize","--value","1","--fps","unknown","--rule","nearest"),
                     ("quantize","--value","1","--fps","30","--rate-mode","vfr","--rule","nearest"),
                     ("convert","--value","2","--from-unit","beats","--to-unit","s","--bpm","120")]:
            with self.subTest(args=args):
                code,result=cli(*args)
                self.assertEqual(code,0)
                self.assertEqual(result["numeric_status"],"unverified")
                self.assertNotIn("frame_index",result)
                self.assertNotIn("value",result)

    def test_cli_window_boundary_and_authority(self):
        code,result=cli("map","--value","5","--source-start","2","--source-end","8","--destination-start","10","--speed","2")
        self.assertEqual((code,result["value"],result["edit_authorized"]),(0,"23/2",False))
        code,result=cli("map","--value","8","--source-start","2","--source-end","8","--destination-start","10","--speed","2")
        self.assertEqual(code,2)
        self.assertIn("half-open",result["error"])


class TimingContracts(unittest.TestCase):
    def test_all_three_standalone_proposals(self):
        for n in (1,2,3):
            with self.subTest(module=n):
                proposal,request=pair(n)
                check=checked(proposal,request)
                self.assertFalse(check.failed,check.diagnostics)
                code,result=cli("route","--request",str(PACKAGE/f"assets/request-standalone-m7-{n}.json"))
                self.assertEqual(code,0)
                self.assertEqual([r["module_id"] for r in result["routes"]],[f"M7.{n}"])
                self.assertEqual(result["invocation"],"not_invoked")

    def test_external_typed_clock_context(self):
        proposal,request=pair(3)
        request["inputs"]["timebase_context"]={"owner":"external","source_id":"design","source_version":"1","values":request["inputs"]["timebase_context"]}
        proposal["context"]=copy.deepcopy(request["inputs"])
        self.assertFalse(checked(proposal,request).failed)
        request["inputs"]["timebase_context"]["values"]["items"]["edit_clock"]["fps"]=False
        proposal["context"]=copy.deepcopy(request["inputs"])
        self.assertIn("external_partition_shape",codes(checked(proposal,request)))

    def test_clock_fps_and_invalid_rational(self):
        for value,code in [(False,"contract_shape"),(0,"fps_positive"),(-24,"fps_positive"),("1/0","invalid_rational")]:
            with self.subTest(value=value):
                proposal,request=pair(1)
                proposal["changes"]["timebase"]["items"]["source_clock"]["fps"]=value
                self.assertIn(code,codes(checked(proposal,request)))

    def test_frame_count_duration_and_last_frame_distinction(self):
        proposal,request=pair(1)
        clock=proposal["changes"]["timebase"]["items"]["source_clock"]
        clock.update(fps=24,extent=9,frame_count=124)
        self.assertIn("frame_count_duration",codes(checked(proposal,request)))
        clock["extent"]="31/6"
        self.assertFalse(checked(proposal,request).failed)
        self.assertEqual(m7.quantize_value("123/24",24,"nearest")[0],123)
        clock["frame_count"]=True
        self.assertIn("contract_shape",codes(checked(proposal,request)))

    def test_claimed_measurement_requires_metadata(self):
        proposal,request=pair(1)
        clock=proposal["changes"]["timebase"]["items"]["source_clock"]
        clock["evidence"]["basis"]="reported_measurement"
        self.assertIn("measurement_evidence",codes(checked(proposal,request)))
        observation={"asset_id":"clip","asset_version":"v1","method":"declared frame inspection","observer":"design fixture author","scope":"entire synthetic clip","locator":"synthetic-design-fixture://not-real-measurement"}
        clock["evidence"]["observation"]=observation
        proposal["sources"]["design"]["kind"]="media_observation"
        request["sources"]["design"]["kind"]="media_observation"
        check=checked(proposal,request)
        self.assertFalse(check.failed)
        self.assertTrue(any(d["code"]=="measurement_authenticity_unverified" and d["status"]=="unverified" for d in check.diagnostics))
        self.assertTrue(any(d["code"]=="beat_grid_candidate" for d in check.diagnostics))

    def test_unknown_precision_is_legal_but_never_passes_precision(self):
        proposal=fixture("proposal-unknown-precision.json")
        request=fixture("request-unknown-precision.json")
        self.assertFalse(checked(proposal,request).failed)
        code,result=cli("check","--proposal",str(PACKAGE/"assets/proposal-unknown-precision.json"),"--request",str(PACKAGE/"assets/request-unknown-precision.json"))
        self.assertEqual(code,0)
        self.assertEqual(result["validation"]["numeric_precision"],"unverified")
        self.assertEqual(result["validation"]["overall"],"unverified")
        proposal["changes"]["mappings"]["items"]["unknown_anchor"]["frame_index"]=24
        self.assertIn("fabricated_precision",codes(checked(proposal,request)))

    def test_sample_end_is_not_existing_frame(self):
        proposal,request=pair(3)
        q=proposal["changes"]["mappings"]["items"]["edit_anchor"]
        q.update(time=8,frame_index=240,quantized_time=8,error_seconds=0)
        self.assertIn("sample_outside_coverage",codes(checked(proposal,request)))
        q["position_kind"]="boundary"
        self.assertFalse(checked(proposal,request).failed)
        q.update(time="799/100",error_seconds="1/100",requirement="candidate",position_kind="sample")
        self.assertIn("sample_outside_coverage",codes(checked(proposal,request)))

    def test_quantization_false_frame_rejected(self):
        proposal,request=pair(3)
        proposal["changes"]["mappings"]["items"]["edit_anchor"]["frame_index"]=156
        self.assertIn("quantization_result",codes(checked(proposal,request)))

    def test_mapping_changes_cannot_invent_m9_speed(self):
        proposal,request=pair(3)
        mapping=proposal["changes"]["mappings"]["items"]["source_to_work"]
        mapping["speed"]=3
        check=checked(proposal,request)
        self.assertIn("edit_intent_changed",codes(check))
        self.assertIn("mapping_duration",codes(check))
        mapping["edit_binding"]={"state":"unknown","reason":"no edit choice given"}
        self.assertIn("edit_intent_missing",codes(checked(proposal,request)))

    def test_freeze_is_multivalued_not_division(self):
        proposal,request=pair(3)
        edit=request["inputs"]["edit_context"]["values"]["mappings"]["source_to_work"]
        edit.update(mode="freeze",source_start=5,source_end=5,speed=0)
        proposal["context"]=copy.deepcopy(request["inputs"])
        mapping=proposal["changes"]["mappings"]["items"]["source_to_work"]
        mapping.update(edit)
        mapping["edit_binding"]["value"]=copy.deepcopy(edit)
        check=checked(proposal,request)
        self.assertFalse(check.failed,check.diagnostics)
        self.assertTrue(any(d["code"]=="freeze_multivalued" for d in check.diagnostics))

    def test_required_two_second_action_cannot_be_compressed(self):
        proposal,request=pair(2)
        proposal["changes"]["schedule"]["items"]["gesture_timing"]["end"]="21/2"
        self.assertIn("event_duration_requirement",codes(checked(proposal,request)))

    def test_freeze_cannot_take_half_open_source_end_as_frame(self):
        proposal,request=pair(3)
        edit=request["inputs"]["edit_context"]["values"]["mappings"]["source_to_work"]
        edit.update(mode="freeze",source_start=10,source_end=10,speed=0)
        proposal["context"]=copy.deepcopy(request["inputs"])
        mapping=proposal["changes"]["mappings"]["items"]["source_to_work"]
        mapping.update(edit)
        mapping["edit_binding"]["value"]=copy.deepcopy(edit)
        self.assertIn("freeze_source_outside_coverage",codes(checked(proposal,request)))

    def test_sequential_duration_budget_is_not_concurrency(self):
        proposal,request=pair(2)
        items=proposal["changes"]["schedule"]["items"]
        items["three_second_budget"]["window"]["end"]=12
        self.assertIn("duration_budget_exceeded",codes(checked(proposal,request)))
        self.assertIn("duration_window_range",codes(checked(proposal,request)))

    def test_half_open_capacity_and_overlap(self):
        proposal,request=pair(2)
        items=proposal["changes"]["schedule"]["items"]
        cap=copy.deepcopy(items["after_gesture"])
        cap.update(constraint_id="single_lane",relation="capacity",capacity=1)
        items["single_lane"]=cap
        self.assertFalse(checked(proposal,request).failed)
        items.pop("after_gesture")
        items["line_timing"].update(start=11,end=12)
        self.assertIn("capacity_exceeded",codes(checked(proposal,request)))

    def test_overlap_requires_positive_intersection(self):
        proposal,request=pair(2)
        item=proposal["changes"]["schedule"]["items"]["after_gesture"]
        item.update(relation="overlap",offset=0)
        self.assertIn("timing_constraint",codes(checked(proposal,request)))

    def test_typed_owner_and_domain_not_short_id(self):
        proposal,request=pair(2)
        ref=request["inputs"]["sound_context"]["values"]["events"]["line1"]["event_ref"]
        ref["id"]="gesture"
        proposal["context"]=copy.deepcopy(request["inputs"])
        items=proposal["changes"]["schedule"]["items"]
        items["line_timing"]["event_ref"]=copy.deepcopy(ref)
        items["line_timing"]["binding"]["value"]["event_ref"]=copy.deepcopy(ref)
        for key in ("after_gesture","three_second_budget"):
            items[key]["event_refs"][1]=copy.deepcopy(ref)
        self.assertFalse(checked(proposal,request).failed)
        items["after_gesture"]["event_refs"][1]["domain_id"]="another_work"
        self.assertIn("dangling_event",codes(checked(proposal,request)))

    def test_event_clock_domain_mismatch(self):
        proposal,request=pair(2)
        proposal["changes"]["schedule"]["items"]["gesture_timing"]["clock_id"]="generation_clock"
        self.assertIn("event_domain",codes(checked(proposal,request)))

    def camera_pair(self):
        proposal,request=pair(2)
        action=proposal["changes"]["schedule"]["items"]["gesture_timing"]
        ref={"owner":"M5","kind":"camera","id":"camera_move","domain":"work","domain_id":"work_main"}
        value={"event_ref":ref,"payload":{"movement":"approved camera move only"}}
        policy={"mode":"early","offset":"-1/2"}
        request["inputs"]["camera_context"]={"owner":"M5","source_id":"design","source_version":"1","values":{"events":{"camera_move":value},"policy":policy}}
        proposal["context"]=copy.deepcopy(request["inputs"])
        def bind(path, val): return {"owner":"M5","source_id":"design","source_version":"1","path":path,"value":copy.deepcopy(val)}
        event={"record_type":"event","timing_id":"camera_timing","event_ref":ref,"clock_id":"work_clock","start":"19/2","end":"23/2","extent_kind":"interval","timing_basis":"planned","binding":bind("/events/camera_move",value),"source_refs":["design"]}
        constraint={"record_type":"constraint","constraint_id":"camera_offset","relation":"offset","event_refs":[action["event_ref"],ref],"left_edge":"start","right_edge":"start","offset":"-1/2","tolerance":0,"policy_binding":bind("/policy",policy),"source_refs":["design"]}
        proposal["changes"]["schedule"]["items"].update(camera_timing=event,camera_offset=constraint)
        return proposal,request

    def test_camera_policy_is_readonly_m5(self):
        proposal,request=self.camera_pair()
        self.assertFalse(checked(proposal,request).failed)
        items=proposal["changes"]["schedule"]["items"]
        items["camera_timing"].update(start="21/2",end="25/2")
        items["camera_offset"]["offset"]="1/2"
        self.assertIn("camera_policy_changed",codes(checked(proposal,request)))

    def test_camera_policy_not_implicitly_invented(self):
        proposal,request=self.camera_pair()
        del proposal["changes"]["schedule"]["items"]["camera_offset"]["policy_binding"]
        self.assertIn("camera_policy_missing",codes(checked(proposal,request)))


class ParentProtocol(unittest.TestCase):
    def test_atomic_acceptance_and_input_immutability(self):
        state,batch,requests=fixture("state-empty.json"),fixture("proposal-batch.json"),fixture("requests.json")
        before=copy.deepcopy((state,batch,requests))
        check,result=accepted(state,batch,requests)
        self.assertFalse(check.failed,check.diagnostics)
        self.assertEqual(result["state"]["version"],1)
        self.assertEqual((state,batch,requests),before)
        self.assertEqual(set(result["impact"]["stale_consumers"]),{"timeline_consumer","compiler_consumer"})

    def test_exact_replay_is_idempotent(self):
        _,first=accepted()
        check,second=accepted(first["state"])
        self.assertFalse(check.failed)
        self.assertEqual(second["acceptance"],"idempotent_replay")
        self.assertEqual(second["state"],first["state"])

    def test_reused_id_changed_bytes_rejected(self):
        _,first=accepted()
        batch=fixture("proposal-batch.json")
        batch["proposals"][0]["changes"]["timebase"]["items"]["beat_candidates"]["bpm"]=121
        check,result=accepted(first["state"],batch)
        self.assertIsNone(result)
        self.assertIn("idempotency_conflict",codes(check))

    def test_stale_base_cannot_accept_new_proposal(self):
        _,first=accepted()
        batch=fixture("proposal-batch.json")
        for proposal in batch["proposals"]: proposal["proposal_id"]+="_new"
        check,result=accepted(first["state"],batch)
        self.assertIsNone(result)
        self.assertIn("stale_base_version",codes(check))

    def test_mixed_retry_and_new_proposal_rejected(self):
        _,first=accepted()
        batch=fixture("proposal-batch.json")
        batch["proposals"][0]["proposal_id"]+="_new"
        check,result=accepted(first["state"],batch)
        self.assertIsNone(result)
        self.assertIn("mixed_replay",codes(check))

    def test_foreign_partition_and_extra_property_rejected(self):
        proposal,request=pair(1)
        proposal["changes"]["schedule"]={"items":{}}
        self.assertIn("write_ownership",codes(checked(proposal,request)))
        proposal,request=pair(1)
        proposal["delete_action"]=True
        self.assertIn("contract_shape",codes(checked(proposal,request)))

    def test_wrong_version_and_parent_as_child_request(self):
        proposal,request=pair(1)
        proposal["contract_version"]="2.0.0"
        self.assertIn("contract_shape",codes(checked(proposal,request)))
        proposal,request=pair(1)
        request["target"]="M7"
        request["inputs"]["timing_brief"]="parent request is not child authorization"
        self.assertIn("request_target",codes(checked(proposal,request)))

    def test_original_sources_and_context_cannot_be_rewritten(self):
        proposal,request=pair(2)
        proposal["sources"]["design"]["excerpt"]="rewritten evidence"
        self.assertIn("request_fidelity",codes(checked(proposal,request)))
        proposal,request=pair(2)
        proposal["context"]["schedule_brief"]="different task"
        self.assertIn("request_fidelity",codes(checked(proposal,request)))

    def test_dialogue_payload_cannot_be_rewritten_in_binding(self):
        proposal,request=pair(2)
        proposal["changes"]["schedule"]["items"]["line_timing"]["binding"]["value"]["payload"]["text"]="偷偷改掉对白"
        self.assertIn("readonly_binding_changed",codes(checked(proposal,request)))

    def test_source_version_binding_and_source_collision(self):
        proposal,request=pair(3)
        proposal["changes"]["mappings"]["items"]["source_to_work"]["edit_binding"]["source_version"]="999"
        self.assertIn("context_version",codes(checked(proposal,request)))
        state=fixture("state-empty.json")
        state["sources"]["design"]={**fixture("requests.json")[0]["sources"]["design"],"version":"older"}
        check,result=accepted(state)
        self.assertIsNone(result)
        self.assertIn("source_collision",codes(check))

    def test_readonly_projection_checked_against_candidate(self):
        batch,requests=fixture("proposal-batch.json"),fixture("requests.json")
        projection={"path":"/content/schedule","source_version":0,"value":{"items":{}}}
        requests[0]["inputs"]["readonly_projection"]=[projection]
        batch["proposals"][0]["context"]=copy.deepcopy(requests[0]["inputs"])
        check,result=accepted(batch=batch,requests=requests)
        self.assertIsNone(result)
        self.assertIn("readonly_conflict",codes(check))

    def test_original_requests_required_and_blockers_atomic(self):
        check,result=accepted(requests=[])
        self.assertIsNone(result)
        self.assertIn("original_request_required",codes(check))
        batch=fixture("proposal-batch.json")
        batch["proposals"][0]["issues"]=[{"issue_id":"blocker","owner":"M7.1","status":"open","severity":"blocking","message":"missing decisive basis","source_refs":["design"]}]
        check,result=accepted(batch=batch)
        self.assertIsNone(result)
        self.assertIn("open_blocker",codes(check))

    def test_accepted_record_cannot_be_deleted(self):
        _,first=accepted()
        proposal,request=pair(1)
        proposal.update(base_version=1,proposal_id="new_timebase",source_request_id="new_request")
        request.update(base_version=1,request_id="new_request")
        proposal["changes"]["timebase"]["items"].pop("beat_candidates")
        batch={"kind":"M7ProposalBatch","contract_version":"1.0.0","work_id":request["work_id"],"base_version":1,"batch_id":"revision","proposals":[proposal]}
        check,result=accepted(first["state"],batch,[request])
        self.assertIsNone(result)
        self.assertIn("accepted_record_deleted",codes(check))

    def test_impact_uses_real_read_paths_and_preserves_stale(self):
        _,first=accepted()
        before=first["state"]
        for consumer in before["consumers"].values(): consumer["status"]="current"
        after=copy.deepcopy(before)
        after["version"]+=1
        after["display"]["title"]="Only presentation changed"
        result=m7.impact(before,after)
        self.assertEqual(set(result["stale_consumers"]),{"title_consumer"})
        before["consumers"]["timeline_consumer"]["status"]="stale"
        result=m7.impact(before,after)
        self.assertTrue(result["stale_consumers"]["timeline_consumer"]["already_stale"])
        self.assertEqual(result["stale_consumers"]["timeline_consumer"]["changed_paths"],[])

    def test_duplicate_nonfinite_json_and_bool_are_not_smuggled(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"bad.json"
            for text in ('{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}','{"a":1e9999}'):
                with self.subTest(text=text):
                    path.write_text(text)
                    with self.assertRaises(ValueError): m7.load_json(path)
        self.assertFalse(m7.same(True,1))
        with self.assertRaises((ValueError,KeyError)): m7.read_pointer({"a":[]},"/a/01")


if __name__ == "__main__":
    unittest.main(verbosity=2)
