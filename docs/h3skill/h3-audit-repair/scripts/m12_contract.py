#!/usr/bin/env python3
"""Portable M12 audit record contract. Reads explicit JSON paths; writes JSON to stdout.

This program validates declarations, references and ledger consistency. It never reads
an evidence locator, observes media, proves authenticity or executes a repair.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
VERSION = "1.0.0"
PARTS = {"M12.1": "AuditPlan", "M12.2": "AuditLedger",
         "M12.3": "MediaObservationLedger", "M12.4": "ChangeSet"}
GATES = ("G0", "G1", "G2", "G3", "G4")
RESULTS = ("pass", "fail", "not_applicable", "unverified")
OWNERS = tuple("M" + str(i) for i in range(1, 13))
BOUNDARY = {
    "checked": "supplied_declarations_and_record_consistency",
    "independent_source_verification": False,
    "media_observed_by_this_program": False,
    "whole_task_certified": False,
    "declared_actual_is_attestation": True,
    "not_run": ["evidence_locator_read", "media_decode", "semantic_truth_verification",
                "owner_module_execution", "h3_inference", "media_regeneration", "file_write"],
}
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class ContractError(ValueError):
    def __init__(self, code, message, path="", owner="M12"):
        super().__init__(message)
        self.code, self.message, self.path, self.owner = code, message, path, owner

    def as_dict(self):
        return {"code": self.code, "detail": self.message, "path": self.path, "owner": self.owner}


def fail(code, message, path=""):
    raise ContractError(code, message, path)


def canonical(value):
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError, RecursionError) as exc:
        fail("json_value", str(exc))


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def same(left, right):
    return canonical(left) == canonical(right)


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            fail("duplicate_json_key", "Duplicate JSON key: " + key)
        value[key] = item
    return value


def load(path):
    def bad_constant(value):
        fail("non_finite_number", "Non-finite JSON number: " + value)
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                          parse_constant=bad_constant)
    except ContractError:
        raise
    except (OSError, ValueError, RecursionError) as exc:
        fail("json_read", str(exc), str(path))


def obj(value, required, optional=(), path=""):
    if not isinstance(value, dict):
        fail("type", "Expected an object", path)
    missing, extra = set(required) - set(value), set(value) - set(required) - set(optional)
    if missing:
        fail("required", "Missing keys: " + ", ".join(sorted(missing)), path)
    if extra:
        fail("unknown_key", "Unknown keys: " + ", ".join(sorted(extra)), path)
    return value


def string(value, path=""):
    if not isinstance(value, str) or not value.strip():
        fail("type", "Expected a non-empty string", path)
    if any(ord(c) < 32 and c not in "\n\t\r" for c in value):
        fail("control_character", "Control characters are not allowed", path)
    return value


def identifier(value, path=""):
    string(value, path)
    if not ID_RE.fullmatch(value):
        fail("identifier", "Expected a stable ASCII identifier", path)
    return value


def integer(value, path="", minimum=0):
    if type(value) is not int or value < minimum:
        fail("type", "Expected integer >= " + str(minimum), path)
    return value


def enum(value, values, path=""):
    if not isinstance(value, str) or value not in values:
        fail("enum", "Expected one of: " + ", ".join(values), path)
    return value


def array(value, path="", minimum=0):
    if not isinstance(value, list) or len(value) < minimum:
        fail("type", "Expected array with at least " + str(minimum) + " items", path)
    return value


def unique(values, path=""):
    if len({canonical(x) for x in values}) != len(values):
        fail("duplicate", "Duplicate values are not allowed", path)


def indexed(values, key="id", path=""):
    result = {}
    for item in values:
        if item[key] in result:
            fail("duplicate_id", "Duplicate " + key + ": " + item[key], path)
        result[item[key]] = item
    return result


def ref(value, path=""):
    obj(value, ("id", "version", "digest", "owner", "kind"), path=path)
    identifier(value["id"], path + "/id")
    string(value["version"], path + "/version")
    if not isinstance(value["digest"], str) or not SHA_RE.fullmatch(value["digest"]):
        fail("digest", "Expected lowercase SHA-256 hex digest", path)
    enum(value["owner"], OWNERS + ("external",), path)
    identifier(value["kind"], path + "/kind")
    return value


def refs(values, path="", minimum=0):
    for item in array(values, path, minimum):
        ref(item, path)
    indexed(values, path=path)
    return values


def identity(value):
    return {key: value[key] for key in ("id", "kind", "owner")}


def interval(value, path=""):
    array(value, path, 2)
    if len(value) != 2:
        fail("time_window", "A window has exactly two integer millisecond endpoints", path)
    integer(value[0], path); integer(value[1], path)
    if value[0] >= value[1]:
        fail("time_window", "Window end must be greater than start", path)
    return value


def channels(value, path=""):
    for item in array(value, path):
        enum(item, ("video", "audio"), path)
    unique(value, path)


def plan(value):
    obj(value, ("scope_id", "scope_version", "plan_ref", "scope_sources", "gates", "requirement_ids", "checks"))
    identifier(value["scope_id"]); string(value["scope_version"])
    ref(value["plan_ref"]); refs(value["scope_sources"])
    for gate in array(value["gates"], minimum=1):
        enum(gate, GATES)
    unique(value["gates"])
    for req in array(value["requirement_ids"], minimum=1):
        identifier(req)
    unique(value["requirement_ids"])
    for item in array(value["checks"], minimum=1):
        obj(item, ("id", "requirement_id", "gate", "expected", "method", "targets", "channels", "time_window_ms", "coverage"))
        identifier(item["id"]); identifier(item["requirement_id"])
        if item["requirement_id"] not in value["requirement_ids"]:
            fail("requirement", "Check refers to an undeclared requirement")
        enum(item["gate"], value["gates"])
        string(item["expected"]); string(item["method"]); refs(item["targets"], minimum=1)
        channels(item["channels"])
        enum(item["coverage"], ("document", "full_window"))
        if item["gate"] in ("G3", "G4"):
            interval(item["time_window_ms"])
            if not item["channels"] or item["coverage"] != "full_window":
                fail("media_scope", "Media checks require channels and full_window coverage")
            kind = "generated_media" if item["gate"] == "G3" else "assembled_media"
            if not any(r["kind"] == kind for r in item["targets"]):
                fail("media_kind", item["gate"] + " requires a " + kind + " target")
        elif item["time_window_ms"] is not None or item["channels"] or item["coverage"] != "document":
            fail("document_scope", "G0/G1/G2 checks use null time window, no media channels and document coverage")
    indexed(value["checks"])
    if set(value["requirement_ids"]) != {c["requirement_id"] for c in value["checks"]}:
        fail("unchecked_requirement", "Every declared requirement needs at least one check")
    if set(value["gates"]) != {c["gate"] for c in value["checks"]}:
        fail("unchecked_gate", "Every declared gate needs at least one check")
    check_ref_consistency(all_plan_refs(value))
    return value


def all_plan_refs(value):
    return [value["plan_ref"]] + value["scope_sources"] + [r for c in value["checks"] for r in c["targets"]]


def check_shape(value):
    out = deepcopy(value)
    out["targets"] = sorted([identity(r) for r in value["targets"]], key=lambda r: r["id"])
    out["channels"] = sorted(out["channels"])
    return out


def preserve_scope(before, after):
    if before["scope_id"] != after["scope_id"]:
        fail("scope_changed", "Retest must retain the original scope_id")
    if not set(before["gates"]) <= set(after["gates"]) or not set(before["requirement_ids"]) <= set(after["requirement_ids"]):
        fail("scope_shrink", "Cannot remove original gates or requirements")
    if not same(identity(before["plan_ref"]), identity(after["plan_ref"])):
        fail("scope_shrink", "Cannot replace the original plan identity")
    old_sources = {canonical(identity(r)) for r in before["scope_sources"]}
    if not old_sources <= {canonical(identity(r)) for r in after["scope_sources"]}:
        fail("scope_shrink", "Cannot remove original scope sources")
    after_checks = indexed(after["checks"])
    for check in before["checks"]:
        if check["id"] not in after_checks or not same(check_shape(check), check_shape(after_checks[check["id"]])):
            fail("scope_shrink", "Original check semantics, targets, channels, method and coverage must remain: " + check["id"])


def check_ref_consistency(values):
    seen, identities = {}, {}
    for value in values:
        ref(value)
        key = (value["id"], value["version"])
        if key in seen and not same(seen[key], value):
            fail("reference_version_reuse", "Same object/version has conflicting content: " + value["id"])
        if value["id"] in identities and not same(identities[value["id"]], identity(value)):
            fail("reference_identity", "Object ID cannot change owner or kind: " + value["id"])
        seen[key], identities[value["id"]] = value, identity(value)


def observation(value):
    obj(value, ("id", "media_ref", "plan_ref", "observer", "observed_at", "method", "time_domain", "channels", "coverage", "origin", "facts"))
    identifier(value["id"]); ref(value["media_ref"]); ref(value["plan_ref"])
    enum(value["media_ref"]["kind"], ("generated_media", "assembled_media"))
    string(value["observer"]); string(value["method"]); string(value["observed_at"])
    try:
        stamp = datetime.fromisoformat(value["observed_at"].replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise ValueError("timezone required")
    except ValueError:
        fail("observation_time", "observed_at must be an ISO-8601 timestamp with timezone")
    enum(value["time_domain"], ("media_ms",))
    channels(value["channels"])
    if not value["channels"]:
        fail("observation_channels", "An observation must declare video and/or audio")
    enum(value["origin"], ("synthetic", "declared_actual"))
    cover = obj(value["coverage"], ("mode", "windows_ms", "duration_ms"))
    enum(cover["mode"], ("full", "intervals", "sampled"))
    integer(cover["duration_ms"], minimum=1)
    previous_end = -1
    for window in array(cover["windows_ms"], minimum=1):
        interval(window)
        if window[1] > cover["duration_ms"] or window[0] < previous_end:
            fail("coverage_windows", "Coverage windows must be sorted, non-overlapping and within duration")
        previous_end = window[1]
    if cover["mode"] == "full" and cover["windows_ms"] != [[0, cover["duration_ms"]]]:
        fail("coverage_full", "Full coverage must explicitly cover [0, duration_ms]")
    for fact in array(value["facts"], minimum=1):
        obj(fact, ("check_id", "expected", "observed", "assessment", "location", "time_window_ms"))
        identifier(fact["check_id"]); string(fact["expected"]); string(fact["observed"]); string(fact["location"])
        enum(fact["assessment"], ("satisfies", "violates", "inconclusive"))
        interval(fact["time_window_ms"])
        if not covers(cover["windows_ms"], fact["time_window_ms"]):
            fail("fact_coverage", "Fact time window must be inside the declared observation coverage")
    indexed(value["facts"], "check_id")
    return value


def evidence(value):
    obj(value, ("id", "kind", "origin", "source_ref", "check_ids", "locator", "content"), ("observation_id",))
    identifier(value["id"]); ref(value["source_ref"])
    enum(value["kind"], ("document", "media_observation", "applicability", "causal_analysis"))
    enum(value["origin"], ("synthetic", "user_report", "declared_actual"))
    string(value["locator"]); string(value["content"])
    for check_id in array(value["check_ids"], minimum=1):
        identifier(check_id)
    unique(value["check_ids"])
    if value["kind"] == "media_observation":
        if "observation_id" not in value:
            fail("observation_link", "Media evidence needs observation_id")
        identifier(value["observation_id"])
    elif "observation_id" in value:
        fail("observation_link", "Only media evidence may link an observation")


def aggregation_input(value):
    obj(value, ("plan", "current_refs", "results", "evidence", "observations"))
    plan(value["plan"]); refs(value["current_refs"])
    for item in array(value["evidence"]):
        evidence(item)
    evidence_by_id = indexed(value["evidence"])
    for item in array(value["observations"]):
        observation(item)
    observations = indexed(value["observations"])
    check_ids = {c["id"] for c in value["plan"]["checks"]}
    for item in value["evidence"]:
        if not set(item["check_ids"]) <= check_ids:
            fail("unknown_check", "Evidence names a check outside the plan")
        if item.get("observation_id") and item["observation_id"] not in observations:
            fail("observation_link", "Media evidence refers to a missing observation")
    for item in array(value["results"]):
        obj(item, ("check_id", "result", "evidence_ids", "reason"), ("applicability",))
        identifier(item["check_id"]); enum(item["result"], RESULTS); string(item["reason"])
        if item["check_id"] not in check_ids:
            fail("unknown_check", "Result is outside the approved scope")
        for eid in array(item["evidence_ids"]):
            identifier(eid)
            if eid not in evidence_by_id:
                fail("missing_evidence", "Unknown evidence_id: " + eid)
        unique(item["evidence_ids"])
        if item["result"] == "not_applicable":
            basis = obj(item.get("applicability"), ("rule", "basis_ref", "no_downstream_dependents"))
            string(basis["rule"]); ref(basis["basis_ref"])
            if basis["no_downstream_dependents"] is not True:
                fail("applicability", "N/A needs an explicit no-downstream-dependents declaration")
        elif "applicability" in item:
            fail("applicability", "Applicability basis is only valid for not_applicable")
    indexed(value["results"], "check_id")
    check_ref_consistency(all_plan_refs(value["plan"]) + value["current_refs"] +
                          [e["source_ref"] for e in value["evidence"]] +
                          [r for o in value["observations"] for r in (o["media_ref"], o["plan_ref"])])
    return value


def covers(windows, wanted):
    end = wanted[0]
    for start, stop in windows:
        if stop <= end:
            continue
        if start > end:
            return False
        end = max(end, stop)
        if end >= wanted[1]:
            return True
    return False


def summarize(results):
    if not results or "unverified" in results:
        return "fail" if "fail" in results else "unverified"
    if "fail" in results:
        return "fail"
    return "not_applicable" if all(x == "not_applicable" for x in results) else "pass"


def build_audit(value):
    aggregation_input(value)
    p = value["plan"]
    current = indexed(value["current_refs"])
    evs, obs = indexed(value["evidence"]), indexed(value["observations"])
    supplied = indexed(value["results"], "check_id")
    out = []
    for c in p["checks"]:
        basis_refs = [p["plan_ref"]] + p["scope_sources"] + c["targets"]
        basis_refs = list({canonical(r): r for r in basis_refs}.values())
        stale = [r["id"] for r in basis_refs if r["id"] in current and not same(current[r["id"]], r)]
        missing = [r["id"] for r in basis_refs if r["id"] not in current]
        result = supplied.get(c["id"])
        gaps, eligible = [], []
        if not result:
            gaps.append("check_not_executed")
        else:
            if not result["evidence_ids"] and result["result"] != "unverified":
                gaps.append("no_supporting_evidence")
            for eid in result["evidence_ids"]:
                e = evs[eid]
                if c["id"] not in e["check_ids"] or not any(same(e["source_ref"], r) for r in basis_refs):
                    gaps.append("evidence_scope_mismatch:" + eid); continue
                if c["gate"] in ("G3", "G4") and result["result"] in ("pass", "fail"):
                    o = obs.get(e.get("observation_id", ""))
                    if e["kind"] != "media_observation" or e["origin"] != "declared_actual" or not o or o["origin"] != "declared_actual":
                        gaps.append("actual_media_observation_missing:" + eid); continue
                    kind = "generated_media" if c["gate"] == "G3" else "assembled_media"
                    if o["media_ref"]["kind"] != kind or not same(o["media_ref"], e["source_ref"]) or not any(same(o["media_ref"], r) for r in c["targets"]) or not same(o["plan_ref"], p["plan_ref"]):
                        gaps.append("observation_version_or_kind_mismatch:" + eid); continue
                    fact = indexed(o["facts"], "check_id").get(c["id"])
                    wanted = "satisfies" if result["result"] == "pass" else "violates"
                    if not fact or fact["expected"] != c["expected"] or fact["assessment"] != wanted or o["method"] != c["method"]:
                        gaps.append("observation_method_or_fact_mismatch:" + eid); continue
                    if not set(c["channels"]) <= set(o["channels"]):
                        gaps.append("observation_channel_gap:" + eid); continue
                    cov = o["coverage"]
                    if result["result"] == "pass" and (cov["mode"] == "sampled" or not covers(cov["windows_ms"], c["time_window_ms"]) or not covers([fact["time_window_ms"]], c["time_window_ms"])):
                        gaps.append("observation_coverage_gap:" + eid); continue
                    if result["result"] == "fail" and not (c["time_window_ms"][0] <= fact["time_window_ms"][0] < fact["time_window_ms"][1] <= c["time_window_ms"][1]):
                        gaps.append("observation_location_gap:" + eid); continue
                elif result["result"] == "not_applicable":
                    if e["kind"] != "applicability" or not same(e["source_ref"], result["applicability"]["basis_ref"]):
                        gaps.append("applicability_evidence_missing:" + eid); continue
                elif e["kind"] not in ("document", "causal_analysis"):
                    gaps.append("document_evidence_missing:" + eid); continue
                eligible.append(eid)
        verdict = result["result"] if result and eligible and (not gaps or result["result"] == "fail") else "unverified"
        if result and result["result"] == "unverified":
            verdict = "unverified"
        # Preserve an evidence-backed historical verdict; staleness is a separate axis.
        validity = "stale" if stale else "unverified" if missing else "current"
        out.append({"check_id": c["id"], "requirement_id": c["requirement_id"], "gate": c["gate"],
                    "requested_result": result["result"] if result else "unverified", "result": verdict,
                    "current_validity": validity, "effective_result": verdict if validity == "current" else "unverified",
                    "evidence_ids": eligible, "basis_refs": deepcopy(basis_refs),
                    "gaps": gaps + ["current_version_missing:" + x for x in missing], "stale_ids": stale,
                    "reason": result["reason"] if result else "No result supplied for this required check"})
    gate_results = {g: summarize([c["effective_result"] for c in out if c["gate"] == g]) for g in p["gates"]}
    return {"scope_id": p["scope_id"], "scope_version": p["scope_version"], "plan": deepcopy(p),
            "checks": out, "gate_results": gate_results, "scope_result": summarize(list(gate_results.values())),
            "unassessed_gates": [g for g in GATES if g not in p["gates"]],
            "verification_boundary": deepcopy(BOUNDARY)}


def build_observations(value):
    obj(value, ("observations",))
    for item in array(value["observations"], minimum=1):
        observation(item)
    indexed(value["observations"])
    check_ref_consistency([r for o in value["observations"] for r in (o["media_ref"], o["plan_ref"])])
    return {"observations": deepcopy(value["observations"]), "verification_boundary": deepcopy(BOUNDARY)}


def repair_input(value):
    obj(value, ("audit", "issues", "changes", "dependencies", "retests"))
    aggregation_input(value["audit"])
    p = value["audit"]["plan"]
    checks = indexed(p["checks"])
    evs = indexed(value["audit"]["evidence"])
    for issue in array(value["issues"], minimum=1):
        obj(issue, ("id", "check_id", "object_ref", "location", "expected", "actual", "evidence_ids", "owner", "attribution_basis", "causal_evidence_ids", "requested_action"))
        identifier(issue["id"]); identifier(issue["check_id"]); ref(issue["object_ref"])
        enum(issue["owner"], OWNERS + ("external", "unresolved"))
        for key in ("location", "expected", "actual", "attribution_basis", "requested_action"):
            string(issue[key])
        check = checks.get(issue["check_id"])
        if not check or issue["expected"] != check["expected"] or not any(same(issue["object_ref"], r) for r in check["targets"]):
            fail("issue_scope", "Issue must retain an original check, expectation and target version")
        for key in ("evidence_ids", "causal_evidence_ids"):
            for eid in array(issue[key]):
                if eid not in evs or issue["check_id"] not in evs[eid]["check_ids"]:
                    fail("issue_evidence", "Issue evidence must belong to its original check")
            unique(issue[key])
    issues = indexed(value["issues"])
    graph = obj(value["dependencies"], ("nodes", "edges", "complete"))
    refs(graph["nodes"])
    if type(graph["complete"]) is not bool:
        fail("type", "Dependency completeness must be a boolean")
    nodes = indexed(graph["nodes"])
    declared_current = indexed(value["audit"]["current_refs"])
    for node in nodes.values():
        if node["id"] in declared_current and not same(node, declared_current[node["id"]]):
            fail("dependency_version", "Dependency node must match its declared current object version")
    for edge in array(graph["edges"]):
        obj(edge, ("upstream", "downstream"))
        identifier(edge["upstream"]); identifier(edge["downstream"])
        if edge["upstream"] not in nodes or edge["downstream"] not in nodes:
            fail("dependency_node", "Every edge endpoint needs an explicit versioned node")
        if edge["upstream"] == edge["downstream"]:
            fail("dependency_self", "Self dependencies add no impact information")
    unique(graph["edges"])
    for change in array(value["changes"]):
        obj(change, ("id", "issue_ids", "owner", "before", "after", "reason", "status"))
        identifier(change["id"]); enum(change["owner"], OWNERS + ("external",)); string(change["reason"])
        enum(change["status"], ("proposed", "reported_applied"))
        ref(change["before"]); ref(change["after"])
        if not same(identity(change["before"]), identity(change["after"])) or change["owner"] != change["before"]["owner"]:
            fail("change_ownership", "Change must retain object identity and its semantic owner")
        if change["before"]["version"] == change["after"]["version"]:
            fail("change_version", "A change needs a new object version")
        if change["before"]["id"] in declared_current and not same(change["before"], declared_current[change["before"]["id"]]):
            fail("change_before_version", "Change.before must match the declared current object version")
        if change["before"]["id"] in nodes and not same(nodes[change["before"]["id"]], change["before"]):
            fail("dependency_version", "Changed object must match its dependency graph version")
        for iid in array(change["issue_ids"], minimum=1):
            if iid not in issues:
                fail("change_issue", "Change names an unknown issue")
        unique(change["issue_ids"])
    indexed(value["changes"])
    if len({c["before"]["id"] for c in value["changes"]}) != len(value["changes"]):
        fail("change_conflict", "Only one proposed transition per object is allowed in a ChangeSet")
    for item in array(value["retests"]):
        obj(item, ("issue_id", "audit"))
        if item["issue_id"] not in issues:
            fail("retest_issue", "Retest names an unknown issue")
        aggregation_input(item["audit"])
        preserve_scope(p, item["audit"]["plan"])
    indexed(value["retests"], "issue_id")
    check_ref_consistency([r for change in value["changes"] for r in (change["before"], change["after"])] + graph["nodes"])
    return value


def closure(seeds, edges):
    found, pending = set(seeds), list(seeds)
    while pending:
        current = pending.pop()
        for edge in edges:
            if edge["upstream"] == current and edge["downstream"] not in found:
                found.add(edge["downstream"]); pending.append(edge["downstream"])
    return found


def fresh_evidence(eid, new, original):
    old_evs = indexed(original["evidence"])
    if eid in old_evs:
        return False
    item = indexed(new["evidence"])[eid]
    comparable = {k: v for k, v in item.items() if k != "id"}
    if any(same(comparable, {k: v for k, v in old.items() if k != "id"}) for old in original["evidence"]):
        return False
    if item["kind"] != "media_observation":
        return True
    old_obs, new_obs = indexed(original["observations"]), indexed(new["observations"])
    oid = item["observation_id"]
    if oid in old_obs:
        return False
    newer = new_obs[oid]
    stamp = datetime.fromisoformat(newer["observed_at"].replace("Z", "+00:00"))
    for older in old_obs.values():
        if older["media_ref"]["id"] == newer["media_ref"]["id"] and stamp <= datetime.fromisoformat(older["observed_at"].replace("Z", "+00:00")):
            return False
    return True


def build_repair(value):
    repair_input(value)
    original = build_audit(value["audit"])
    checks, evs = indexed(original["checks"], "check_id"), indexed(value["audit"]["evidence"])
    current = indexed(value["audit"]["current_refs"])
    graph, changes = value["dependencies"], value["changes"]
    nodes = indexed(graph["nodes"])
    applied = [c for c in changes if c["status"] == "reported_applied"]
    directly_changed = {c["before"]["id"] for c in applied}
    planned_ids = closure([c["before"]["id"] for c in changes], graph["edges"])
    affected_ids = closure([c["before"]["id"] for c in applied], graph["edges"])
    unknown = sorted(({c["before"]["id"] for c in changes} | set(current)) - set(nodes))
    impact_status = "complete" if graph["complete"] and not unknown else "partial"
    retests, issue_results = indexed(value["retests"], "issue_id"), []
    for issue in value["issues"]:
        check = checks[issue["check_id"]]
        if check["effective_result"] in ("pass", "not_applicable"):
            fail("issue_without_failure", "Issues require a failed or unverified original check")
        causal = [evs[eid] for eid in issue["causal_evidence_ids"]]
        supported = bool(causal) and issue["owner"] != "unresolved" and all(
            e["kind"] == "causal_analysis" and any(same(e["source_ref"], r) for r in check["basis_refs"])
            and same(current.get(e["source_ref"]["id"]), e["source_ref"]) for e in causal)
        routed_owner = issue["owner"] if supported else "unresolved"
        linked = [c for c in changes if issue["id"] in c["issue_ids"]]
        if any(c["owner"] != routed_owner for c in linked):
            fail("unsupported_owner", "A ChangeSet needs evidence-supported attribution to the declared object owner")
        reasons, status = [], "open"
        retest = retests.get(issue["id"])
        retest_result = None
        if retest:
            retest_result = build_audit(retest["audit"])
            new_check = indexed(retest_result["checks"], "check_id")[issue["check_id"]]
            new_current = indexed(retest["audit"]["current_refs"])
            if new_check["effective_result"] != "pass":
                reasons.append("retest_not_current_pass")
            if impact_status != "complete":
                reasons.append("dependency_impact_incomplete")
            if linked and not any(c["status"] == "reported_applied" for c in linked):
                reasons.append("repair_only_proposed")
            for change in applied:
                if not same(new_current.get(change["after"]["id"]), change["after"]):
                    reasons.append("changed_version_not_current:" + change["after"]["id"])
            for basis in new_check["basis_refs"]:
                if basis["id"] in affected_ids and basis["id"] in nodes and same(basis, nodes[basis["id"]]):
                    # A changed plan can invalidate an observation without changing
                    # the media bytes. A new, compatible observation may revalidate
                    # that same media; a direct media change still needs a new version.
                    new_evidence = indexed(retest["audit"]["evidence"])
                    reobserved = basis["kind"] in ("generated_media", "assembled_media") and basis["id"] not in directly_changed and any(
                        new_evidence[eid]["kind"] == "media_observation" and same(new_evidence[eid]["source_ref"], basis)
                        and fresh_evidence(eid, retest["audit"], value["audit"]) for eid in new_check["evidence_ids"])
                    if not reobserved:
                        reasons.append("affected_version_not_refreshed:" + basis["id"])
            if not any(fresh_evidence(eid, retest["audit"], value["audit"]) for eid in new_check["evidence_ids"]):
                reasons.append("fresh_evidence_missing")
            status = "closed_by_retest" if not reasons else "open"
        else:
            reasons.append("retest_missing")
        issue_results.append({"issue_id": issue["id"], "check_id": issue["check_id"], "owner": routed_owner,
                              "attribution_status": "supported_declaration" if supported else "unresolved",
                              "status": status, "reasons": sorted(set(reasons)),
                              "requested_action": issue["requested_action"], "retest": retest_result})
    affected_refs = [nodes[i] for i in sorted(affected_ids) if i in nodes]
    affected_refs += [c["before"] for c in applied if c["before"]["id"] not in nodes]
    affected_checks = [c["check_id"] for c in original["checks"] if any(r["id"] in affected_ids for r in c["basis_refs"])]
    return {"scope_id": original["scope_id"], "original_audit": original,
            "issues": issue_results, "changes": deepcopy(changes),
            "planned_affected_ids": sorted(planned_ids), "affected_ids": sorted(affected_ids),
            "invalidated_refs": deepcopy(affected_refs), "affected_check_ids": affected_checks,
            "impact_status": impact_status, "unknown_dependency_ids": unknown,
            "repair_executed": False, "all_issues_closed": bool(issue_results) and all(i["status"] == "closed_by_retest" for i in issue_results),
            "verification_boundary": deepcopy(BOUNDARY)}


def validate_request(request):
    canonical(request)
    obj(request, ("kind", "contract_version", "route_version", "work_id", "base_version", "request_id", "target", "inputs"))
    enum(request["kind"], ("M12Request",)); enum(request["contract_version"], (VERSION,)); enum(request["route_version"], (VERSION,))
    identifier(request["work_id"]); integer(request["base_version"]); identifier(request["request_id"])
    enum(request["target"], tuple(PARTS))
    if request["target"] == "M12.1":
        plan(request["inputs"])
        content = {"plan": deepcopy(request["inputs"]), "verification_boundary": deepcopy(BOUNDARY)}
    elif request["target"] == "M12.2":
        content = build_audit(request["inputs"])
    elif request["target"] == "M12.3":
        content = build_observations(request["inputs"])
    else:
        content = build_repair(request["inputs"])
    check_ref_consistency(collect_refs(request["inputs"]))
    immutable_items([request])
    return content


def collect_refs(value):
    found = []
    if isinstance(value, dict):
        if set(value) == {"id", "version", "digest", "owner", "kind"}:
            found.append(value)
        else:
            for item in value.values():
                found.extend(collect_refs(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(collect_refs(item))
    return found


def request_plans(request):
    value = request["inputs"]
    if request["target"] == "M12.1":
        return [value]
    if request["target"] == "M12.2":
        return [value["plan"]]
    if request["target"] == "M12.4":
        return [value["audit"]["plan"]] + [r["audit"]["plan"] for r in value["retests"]]
    return []


def request_audits(request):
    if request["target"] == "M12.2":
        return [request["inputs"]]
    if request["target"] == "M12.4":
        return [request["inputs"]["audit"]] + [r["audit"] for r in request["inputs"]["retests"]]
    return []


def immutable_items(requests):
    registries = {"evidence": {}, "observations": {}}
    for request in requests:
        audits = request_audits(request)
        batches = {"evidence": [e for a in audits for e in a["evidence"]],
                   "observations": [o for a in audits for o in a["observations"]]}
        if request["target"] == "M12.3":
            batches["observations"] += request["inputs"]["observations"]
        for key, values in batches.items():
            for value in values:
                old = registries[key].get(value["id"])
                if old is not None and not same(old, value):
                    fail("immutable_record", key + " ID cannot be edited in place: " + value["id"])
                registries[key][value["id"]] = value


def route(request):
    validate_request(request)
    return {"status": "ready", "target": request["target"], "owned_record_kind": PARTS[request["target"]],
            "work_id": request["work_id"], "request_id": request["request_id"],
            "read_only": True, "verification_boundary": deepcopy(BOUNDARY)}


def propose(request):
    content = validate_request(request)
    record = {"kind": PARTS[request["target"]], "id": request["request_id"],
              "version": str(request["base_version"] + 1), "owner": request["target"],
              "work_id": request["work_id"], "content": content}
    record["digest"] = digest(record)
    return {"kind": "M12Proposal", "contract_version": VERSION, "route_version": VERSION,
            "proposal_id": "P_" + digest(request), "request_id": request["request_id"],
            "request_digest": digest(request), "work_id": request["work_id"],
            "base_version": request["base_version"], "module_id": request["target"], "record": record}


def check(proposal, request):
    expected = propose(request)
    if not same(proposal, expected):
        fail("proposal_mismatch", "Proposal must exactly match recomputation from the original trusted request")
    return {"status": "valid", "module_id": request["target"], "proposal_id": proposal["proposal_id"],
            "verification_boundary": deepcopy(BOUNDARY)}


def empty_state(work_id):
    identifier(work_id)
    return {"kind": "M12State", "contract_version": VERSION, "work_id": work_id,
            "version": 0, "records": [], "receipts": []}


def current_updates(request):
    if request["target"] == "M12.1":
        return all_plan_refs(request["inputs"])
    if request["target"] == "M12.2":
        return request["inputs"]["current_refs"]
    if request["target"] == "M12.4":
        # Original audits are historical reads. Only explicitly reported changes
        # and fresh retest snapshots advance an existing current-version register.
        return [c["after"] for c in request["inputs"]["changes"] if c["status"] == "reported_applied"] + [r for rt in request["inputs"]["retests"] for r in rt["audit"]["current_refs"]]
    return []


def derive_current(requests):
    current, seen = {}, {}
    for request in requests:
        if request["target"] == "M12.4":
            for r in request["inputs"]["audit"]["current_refs"]:
                if r["id"] not in current:
                    current[r["id"]] = r; seen[(r["id"], r["version"])] = r
        batch = {}
        for r in current_updates(request):
            if r["id"] in batch and not same(batch[r["id"]], r):
                fail("current_version_conflict", "One request cannot declare two current versions of " + r["id"])
            batch[r["id"]] = r
        for r in batch.values():
            key = (r["id"], r["version"])
            if key in seen and r["id"] in current and not same(current[r["id"]], r):
                fail("version_rollback", "Cannot restore a previously superseded object version as current: " + r["id"])
            current[r["id"]] = r; seen[key] = r
    return current


def scope_history(requests):
    previous, versions = {}, {}
    for request in requests:
        for index, p in enumerate(request_plans(request)):
            historical_read = request["target"] == "M12.4" and index == 0
            key = (p["scope_id"], p["scope_version"])
            if key in versions and not same(versions[key], p):
                fail("scope_version_reuse", "Changed audit plan needs a new scope_version")
            if p["scope_id"] in previous:
                if key in versions:
                    if p["scope_version"] != previous[p["scope_id"]]["scope_version"] and not historical_read:
                        fail("stale_scope", "A new audit/retest must use the current expanded scope snapshot")
                    preserve_scope(p, previous[p["scope_id"]])
                else:
                    preserve_scope(previous[p["scope_id"]], p)
            if key not in versions:
                previous[p["scope_id"]] = p
            versions[key] = p
    return previous


def _apply_batch(proposals, requests, state):
    if len(proposals) != len(requests) or not proposals:
        fail("batch_size", "Supply equally sized, non-empty proposal and original-request arrays")
    if len({p["module_id"] for p in proposals}) != len(proposals):
        fail("partition_conflict", "An atomic batch has at most one proposal per child-owned partition")
    previous_requests = [r["request"] for r in state["receipts"]]
    ids = {r["request_id"] for r in previous_requests}
    for proposal, request in zip(proposals, requests):
        check(proposal, request)
        if request["work_id"] != state["work_id"]:
            fail("work_id", "All proposals must belong to the parent work")
        if request["base_version"] != state["version"]:
            fail("stale_base_version", "Proposal base_version must equal the current parent state version")
        if request["request_id"] in ids:
            fail("request_id_reuse", "New records need new request IDs")
        ids.add(request["request_id"])
    combined = previous_requests + requests
    check_ref_consistency([r for q in combined for r in collect_refs(q["inputs"])])
    immutable_items(combined); latest_scopes = scope_history(combined); derive_current(combined)
    prior_current = derive_current(previous_requests)
    for request in requests:
        for index, p in enumerate(request_plans(request)):
            if not (request["target"] == "M12.4" and index == 0) and p["scope_version"] != latest_scopes[p["scope_id"]]["scope_version"]:
                fail("batch_scope_conflict", "Atomic siblings must use the same current scope snapshot")
        if request["target"] == "M12.4":
            for node in request["inputs"]["dependencies"]["nodes"]:
                if node["id"] in prior_current and not same(node, prior_current[node["id"]]):
                    fail("stale_dependency_graph", "Dependency graph does not match accepted current versions")
            for change in request["inputs"]["changes"]:
                before = change["before"]
                if before["id"] in prior_current and not same(before, prior_current[before["id"]]):
                    fail("stale_change", "Change.before does not match accepted current versions")
    # Atomic siblings cannot disagree about a newly declared current version.
    batch_refs = {}
    for request in requests:
        for r in current_updates(request):
            if r["id"] in batch_refs and not same(batch_refs[r["id"]], r):
                fail("batch_version_conflict", "Atomic siblings disagree about current object version: " + r["id"])
            batch_refs[r["id"]] = r
    updated = deepcopy(state)
    updated["version"] += 1
    for proposal, request in zip(proposals, requests):
        updated["records"].append(deepcopy(proposal["record"]))
        updated["receipts"].append({"accepted_version": updated["version"], "proposal_id": proposal["proposal_id"],
                                    "request": deepcopy(request), "proposal": deepcopy(proposal)})
    return updated


def validate_state(state):
    obj(state, ("kind", "contract_version", "work_id", "version", "records", "receipts"))
    enum(state["kind"], ("M12State",)); enum(state["contract_version"], (VERSION,))
    identifier(state["work_id"]); integer(state["version"]); array(state["records"]); array(state["receipts"])
    for receipt in state["receipts"]:
        obj(receipt, ("accepted_version", "proposal_id", "request", "proposal"))
        integer(receipt["accepted_version"], minimum=1)
    replay = empty_state(state["work_id"])
    pos = 0
    while pos < len(state["receipts"]):
        group, accepted = [], replay["version"] + 1
        while pos < len(state["receipts"]) and state["receipts"][pos].get("accepted_version") == accepted:
            item = obj(state["receipts"][pos], ("accepted_version", "proposal_id", "request", "proposal"))
            integer(item["accepted_version"], minimum=1)
            if item["proposal_id"] != item["proposal"].get("proposal_id"):
                fail("receipt", "Receipt proposal identity mismatch")
            group.append(item); pos += 1
        if not group:
            fail("history_sequence", "Accepted versions must form consecutive non-empty atomic batches")
        replay = _apply_batch([r["proposal"] for r in group], [r["request"] for r in group], replay)
    if not same(replay, state):
        fail("state_history", "State must exactly equal replay of immutable accepted receipts")
    return state


def current_view(state):
    requests = [r["request"] for r in state["receipts"]]
    current = derive_current(requests)
    latest_scopes = scope_history(requests)
    events, partial = [], False
    old_evidence, old_observations = {}, {}
    for record, request in zip(state["records"], requests):
        # A repair's original audit belongs to the pre-change evidence history;
        # its fresh retest observations belong to the post-change history.
        before_audits = request_audits(request)[:1] if request["target"] == "M12.4" else request_audits(request)
        for audit in before_audits:
            old_evidence.update(indexed(audit["evidence"]))
            old_observations.update(indexed(audit["observations"]))
        if request["target"] == "M12.3":
            old_observations.update(indexed(request["inputs"]["observations"]))
        if record["kind"] == "ChangeSet":
            events.append({"invalidated": {canonical(r) for r in record["content"]["invalidated_refs"]},
                           "direct": {c["before"]["id"] for c in record["content"]["changes"] if c["status"] == "reported_applied"},
                           "old": {"evidence": list(old_evidence.values()), "observations": list(old_observations.values())}})
            partial = partial or record["content"]["impact_status"] == "partial"
            for audit in request_audits(request)[1:]:
                old_evidence.update(indexed(audit["evidence"]))
                old_observations.update(indexed(audit["observations"]))
    ledgers = []
    for record, request in zip(state["records"], requests):
        if record["kind"] != "AuditLedger":
            continue
        audit = request["inputs"]
        evs = indexed(audit["evidence"])
        checks = []
        for item in record["content"]["checks"]:
            stale = []
            for basis in item["basis_refs"]:
                invalidated = False
                for event in events:
                    if canonical(basis) not in event["invalidated"]:
                        continue
                    reobserved = basis["kind"] in ("generated_media", "assembled_media") and basis["id"] not in event["direct"] and item["result"] in ("pass", "fail") and any(
                        evs[eid]["kind"] == "media_observation" and same(evs[eid]["source_ref"], basis)
                        and fresh_evidence(eid, audit, event["old"]) for eid in item["evidence_ids"])
                    if not reobserved:
                        invalidated = True
                if invalidated or basis["id"] in current and not same(current[basis["id"]], basis):
                    stale.append(basis["id"])
            missing = [r["id"] for r in item["basis_refs"] if r["id"] not in current]
            validity = "stale" if stale else "unverified" if missing else "current"
            checks.append({"check_id": item["check_id"], "historical_result": item["result"],
                           "current_validity": validity, "effective_result": item["result"] if validity == "current" else "unverified",
                           "stale_ids": sorted(set(stale)), "missing_current_ids": sorted(set(missing))})
        scope_validity = "current" if record["content"]["scope_version"] == latest_scopes[record["content"]["scope_id"]]["scope_version"] else "stale"
        ledgers.append({"record_id": record["id"], "scope_id": record["content"]["scope_id"], "checks": checks,
                        "scope_current_validity": scope_validity,
                        "scope_result": summarize([c["effective_result"] for c in checks]) if scope_validity == "current" else "unverified"})
    return {"current_refs": [deepcopy(current[k]) for k in sorted(current)], "audit_ledgers": ledgers,
            "dependency_impact": "partial" if partial else "no_known_incomplete_impact", "whole_task_certified": False}


def accept(proposals, requests, state):
    array(proposals, minimum=1); array(requests, minimum=1); validate_state(state)
    if len(proposals) != len(requests):
        fail("batch_size", "Supply one original request for every proposal")
    for proposal, request in zip(proposals, requests):
        check(proposal, request)
    old = {r["proposal_id"]: r for r in state["receipts"]}
    repeated = [p["proposal_id"] in old for p in proposals]
    if any(repeated):
        if not all(repeated):
            fail("mixed_replay", "Cannot mix idempotent retries with new proposals")
        unique([p["proposal_id"] for p in proposals])
        for proposal, request in zip(proposals, requests):
            receipt = old[proposal["proposal_id"]]
            if not same(receipt["proposal"], proposal) or not same(receipt["request"], request):
                fail("replay_mutation", "Replay must exactly match accepted request and proposal")
        updated, idempotent = deepcopy(state), True
    else:
        updated, idempotent = _apply_batch(proposals, requests, state), False
    return {"status": "accepted", "idempotent": idempotent, "state": updated,
            "current_view": current_view(updated), "verification_boundary": deepcopy(BOUNDARY)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("route", "propose"):
        p = sub.add_parser(command); p.add_argument("request")
    p = sub.add_parser("check"); p.add_argument("proposal"); p.add_argument("--request", required=True)
    p = sub.add_parser("accept"); p.add_argument("proposals"); p.add_argument("--requests", required=True); p.add_argument("--state", required=True)
    try:
        args = parser.parse_args(argv)
        if args.command in ("route", "propose"):
            result = globals()[args.command](load(args.request))
        elif args.command == "check":
            result = check(load(args.proposal), load(args.request))
        else:
            result = accept(load(args.proposals), load(args.requests), load(args.state))
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except ContractError as exc:
        print(json.dumps({"status": "invalid", "errors": [exc.as_dict()], "verification_boundary": BOUNDARY}, ensure_ascii=False, indent=2))
        return 2
    except (KeyError, TypeError, ValueError, OverflowError, RecursionError) as exc:
        print(json.dumps({"status": "invalid", "errors": [{"code": "malformed_input", "detail": str(exc)}], "verification_boundary": BOUNDARY}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
