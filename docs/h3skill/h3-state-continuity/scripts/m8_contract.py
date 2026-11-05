#!/usr/bin/env python3
"""Portable M8 draft contracts and explicit state/prompt continuity checks.

Pure JSON in/out. No media, NLP, H3 inference, hidden upstream calls or writes.
Python 3.10+, standard library. See references/contract-guide.md for limits.
"""
import argparse
import copy
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

from _schema import canonical, validate

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0"
OWNED = {"M8.1": "ContinuityPolicy", "M8.2": "StateLedger", "M8.3": "ContinuityHandoffs"}
EMPTY = {"ContinuityPolicy": {"items": {}}, "StateLedger": {"states": {}, "transitions": {}, "chains": {}}, "ContinuityHandoffs": {"items": {}}}
MINIMUM = {"M8": ("continuity_brief",), "M8.1": ("policy_brief", "edit_context"), "M8.2": ("ledger_brief", "policy_context"), "M8.3": ("handoff_brief", "policy_context", "ledger_context", "prompt_context")}
CONTEXTS = {"policy_context": ("M8.1", "ContinuityPolicy"), "ledger_context": ("M8.2", "StateLedger"), "task_context": ("M1", None), "reference_context": ("M2", "ReferenceValues"), "spatial_context": ("M3", None), "action_context": ("M4", None), "camera_context": ("M5", None), "sound_context": ("M6", None), "timing_context": ("M7", None), "edit_context": ("M9", "EditValues"), "prompt_context": ("M11", "PromptValues"), "actual_context": ("M12", "ActualValues")}
CONTINUOUS = {"continuous_shot", "continuous_action_cut"}
PHYSICAL = {"support", "holding", "prop_owner", "contact", "facing", "direction", "action_phase"}


def same(a, b):
    return canonical(a) == canonical(b)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def pointer(value, path):
    if path == "":
        return value
    if not path.startswith("/"):
        raise ValueError("JSON pointer must start with /")
    for part in path.split("/")[1:]:
        key = part.replace("~1", "/").replace("~0", "~")
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def known(fact):
    return isinstance(fact, dict) and fact.get("state") == "known"


def value_equal(a, b):
    return known(a) and known(b) and a["value"] == b["value"]


def physical(attribute):
    return attribute.rsplit(".", 1)[-1] in PHYSICAL


class Check:
    def __init__(self):
        self.schema = load_json(ROOT / "references/contracts.json")
        self.diagnostics = []

    @property
    def failed(self):
        return any(x["severity"] == "error" for x in self.diagnostics)

    def add(self, code, path, message, owner="M8", severity="error"):
        item = {"code": code, "path": path, "message": message, "repair_target": owner, "severity": severity}
        if item not in self.diagnostics:
            self.diagnostics.append(item)

    def shape(self, obj, kind=None, path=""):
        schema = self.schema["$defs"][kind] if kind else self.schema
        errors = validate(obj, schema, self.schema, path)
        for where, message in errors:
            self.add("schema", where, message)
        return not errors

    def refs(self, obj, sources, path=""):
        if isinstance(obj, dict):
            if "source_refs" in obj:
                refs = obj["source_refs"]
                if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs):
                    self.add("source_refs_shape", path, "Source references must be an array of registered IDs")
                    refs = []
                for ref in refs:
                    if ref not in sources:
                        self.add("source_missing", path, "Unregistered source: " + ref)
                    elif obj.get("state") == "known" and sources[ref]["kind"] == "hypothesis":
                        self.add("unconfirmed_fact", path, "Hypothesis cannot be asserted as known; use unknown and retain the reason")
            if obj.get("state") == "unknown":
                self.add("unknown", path, str(obj.get("reason", "Opaque input declares unknown")), severity="unverified")
            for key, child in obj.items():
                self.refs(child, sources, path + "/" + key)
        elif isinstance(obj, list):
            for i, child in enumerate(obj):
                self.refs(child, sources, path + "/" + str(i))

    def inputs(self, inputs, sources, base, target, path="/inputs", accepted=False):
        for key in MINIMUM[target]:
            if key not in inputs:
                self.add("missing_input", path + "/" + key, "Public minimum input is required", target)
        self.refs(inputs, sources, path)
        for name, (owner, kind) in CONTEXTS.items():
            if name not in inputs:
                continue
            context = inputs[name]
            if context["owner"] not in (owner, "external"):
                self.add("context_owner", path + "/" + name, "Expected readonly owner " + owner, target)
            source = sources.get(context["source_id"])
            if source is None or source["version"] != context["source_version"]:
                self.add("context_source_version", path + "/" + name, "Source ID/version must match the original registered source", target)
            elif source["kind"] == "hypothesis":
                self.add("unconfirmed_context", path + "/" + name, "Hypothesis cannot supply an authorized readonly context", target)
            if kind:
                self.shape(context["values"], kind, path + "/" + name + "/values")
        for projection in inputs.get("readonly_projection", []):
            if (not accepted and projection["source_version"] != base) or projection["source_version"] > base:
                self.add("projection_version", path + "/readonly_projection", "Projection must cite the request base version", target)

    def request(self, request, path=""):
        if not self.shape(request, "M8Request", path):
            return False
        self.inputs(request["inputs"], request["sources"], request["base_version"], request["target"], path + "/inputs")
        return not self.failed

    def binding(self, binding, inputs, where, owner):
        candidates = [c for c in inputs.values() if isinstance(c, dict) and all(k in c for k in ("owner", "source_id", "source_version", "values")) and all(c[k] == binding[k] for k in ("owner", "source_id", "source_version"))]
        for context in candidates:
            try:
                if same(pointer(context["values"], binding["path"]), binding["value"]):
                    return
            except (KeyError, IndexError, TypeError, ValueError):
                pass
        self.add("readonly_binding_changed", where, "Binding must resolve to the exact readonly record in the original request", owner)

    def policies(self, policies, inputs, where="/content/ContinuityPolicy"):
        edits = inputs.get("edit_context", {}).get("values", {}).get("boundaries")
        for key, policy in policies["items"].items():
            path = where + "/items/" + key
            if key != policy["policy_id"]:
                self.add("record_identity", path, "Policy key differs from policy_id", "M8.1")
            allowed = [x["attribute"] for x in policy["allowed_changes"]]
            if len(set(allowed)) != len(allowed) or set(allowed) & set(policy["invariants"]):
                self.add("permission_conflict", path, "Allowed changes must be unique and cannot also be invariant", "M8.1")
            if policy["boundary_type"] == "match_cut" and not policy["match_attributes"]:
                self.add("match_basis_missing", path, "Match cut requires explicit selected matching attributes", "M8.1")
            if policy["boundary_type"] == "continuous_shot" and policy["from_shot"] != policy["to_shot"]:
                self.add("single_shot_boundary", path, "Continuous-shot policy must refer to one shot", "M9")
            if set(policy["match_attributes"]) & set(allowed):
                self.add("match_permission_conflict", path, "A matching attribute cannot simultaneously be allowed to differ", "M8.1")
            if policy["boundary_type"] in ("montage", "ellipsis") and not known(policy["cue"]):
                self.add("boundary_permission_unverified", path, "Montage/ellipsis cue is unknown; the intended change cannot be confirmed", "M9", "unverified")
            if edits is not None:
                edit = edits.get(policy["boundary_id"])
                if edit is None:
                    self.add("edit_boundary_missing", path, "Policy must refer to an original M9 boundary", "M9")
                    continue
                for field in ("boundary_type", "from_shot", "to_shot", "match_attributes", "cue"):
                    if not same(policy[field], edit[field]):
                        self.add("edit_intent_changed", path + "/" + field, "M8 cannot rewrite the readonly boundary intent", "M9")
                if not set(edit["invariants"]) <= set(policy["invariants"]):
                    self.add("invariant_removed", path, "Readonly required invariants were dropped", "M8.1")
                if not set(allowed) <= set(edit["approved_changes"]):
                    self.add("change_permission_missing", path, "Change lacks explicit M9/task authorization", "M8.1")

    def ledger(self, ledger, policies, inputs, where="/content/StateLedger"):
        states, transitions = ledger["states"], ledger["transitions"]
        references = inputs.get("reference_context", {}).get("values", {}).get("references", {})
        for key, state in states.items():
            path = where + "/states/" + key
            if state["state_id"] != key or not state["attributes"]:
                self.add("state_identity_or_empty", path, "Planned state needs matching ID and explicit attributes", "M8.2")
            for binding in state.get("bindings", []):
                self.binding(binding, inputs, path + "/bindings", "M8.2")
            for use in state.get("reference_uses", []):
                reference = references.get(use["reference_id"])
                if reference is None:
                    self.add("reference_permission_missing", path, "Reference use requires a source-bound M2 adapter", "M2")
                    continue
                attrs = set(use["attributes"])
                if not attrs <= set(reference["allowed_attributes"]) or attrs & set(reference["denied_attributes"]):
                    self.add("reference_permission_denied", path, "State inherited an attribute outside the reference's allowed scope", "M2")
                if reference["role"] == "identity" and any(a.rsplit(".", 1)[-1] not in ("identity", "face") for a in attrs):
                    self.add("identity_reference_pose", path, "Identity-only reference cannot set pose/support/orientation/composition", "M2")
                if not attrs <= set(state["attributes"]):
                    self.add("reference_attribute_missing", path, "Reference use names an absent state attribute", "M8.2")
        for key, transition in transitions.items():
            path = where + "/transitions/" + key
            if transition["transition_id"] != key:
                self.add("record_identity", path, "Transition key differs from ID", "M8.2")
            before, after = states.get(transition["from_state"]), states.get(transition["to_state"])
            if before is None or after is None:
                self.add("state_reference", path, "Transition refers to an absent planned state", "M8.2")
                continue
            changed = {a for a in set(before["attributes"]) | set(after["attributes"]) if known(before["attributes"].get(a)) and known(after["attributes"].get(a)) and not value_equal(before["attributes"][a], after["attributes"][a])}
            if not changed <= set(transition["changed_attributes"]):
                self.add("unrecorded_change", path, "Changed state attributes are missing from this transition", "M8.2")
            for attr in set(transition["changed_attributes"]) - changed:
                if known(before["attributes"].get(attr)) and known(after["attributes"].get(attr)):
                    self.add("spurious_change", path, "A declared changed attribute has equal endpoint values; use a hold or name the actual change", "M8.2")
            if set(before["attributes"]) != set(after["attributes"]):
                self.add("state_attribute_dropped", path, "Transition endpoints must track the same attribute keys; absence is not unknown", "M8.2")
            if not known(transition["cause"]):
                self.add("transition_cause_unknown", path, "Transition cause remains unverified", "M4", "unverified")
            if transition["mode"] == "process":
                if "action_binding" not in transition or transition["action_binding"]["owner"] not in ("M4", "external"):
                    self.add("process_binding_missing", path, "Visible process requires an exact source-bound M4 action record", "M4")
                else:
                    self.binding(transition["action_binding"], inputs, path + "/action_binding", "M4")
                    action = transition["action_binding"]["value"]
                    if self.shape(action, "ActionAdapter", path + "/action_binding/value"):
                        if (action["from_state"], action["to_state"]) != (transition["from_state"], transition["to_state"]) or not changed <= set(action["changed_attributes"]):
                            self.add("process_action_identity", path, "Readonly action must explicitly account for these endpoints and changed attributes", "M4")
            if transition["mode"] == "hold" and changed:
                self.add("hold_changed", path, "A hold cannot reset tracked state", "M8.2")
            policy = policies["items"].get(transition.get("policy_id"))
            if policy is None and ("policy_id" in transition or transition["mode"] == "boundary"):
                self.add("transition_policy_missing", path, "An explicit policy reference must resolve; boundary transitions require a policy", "M8.1")
            if policy:
                if (before["shot_id"], after["shot_id"]) != (policy["from_shot"], policy["to_shot"]):
                    self.add("transition_policy_shot_binding", path, "Scoped policy permission belongs to different endpoint shots", "M8.1")
                if changed & set(policy["invariants"]):
                    self.add("invariant_changed", path, "Transition violates scoped invariants", "M8.2")
                if transition["mode"] == "boundary":
                    if not changed <= {x["attribute"] for x in policy["allowed_changes"]}:
                        self.add("change_permission_missing", path, "Boundary changed an attribute without permission", "M8.1")
                    if policy["boundary_type"] in CONTINUOUS and any(physical(a) for a in changed):
                        self.add("physical_reset", path, "Continuous support/contact/holding/direction changes require a represented process, not a boundary reset", "M4")
        for key, chain in ledger["chains"].items():
            path = where + "/chains/" + key
            if key != chain["chain_id"]:
                self.add("record_identity", path, "Chain key differs from ID", "M8.2")
            if any(x not in states for x in chain["state_ids"]) or any(x not in transitions for x in chain["transition_ids"]):
                self.add("chain_reference", path, "Chain contains an unknown state or transition", "M8.2")
                continue
            if chain["coverage"] == "snapshots":
                if chain["intervals"]:
                    self.add("snapshot_interval_claim", path, "Snapshots do not prove continuous interval coverage", "M8.2")
                self.add("snapshot_coverage_unverified", path, "Discrete snapshots are not a complete continuous chain", "M8.2", "unverified")
                continue
            ids, tids, intervals = chain["state_ids"], chain["transition_ids"], chain["intervals"]
            if len(ids) != len(tids) + 1 or len(intervals) != len(ids):
                self.add("chain_interval_count", path, "Initial state plus N transitions requires N+1 traceable intervals", "M8.2")
                continue
            if len({x["interval_id"] for x in intervals}) != len(intervals):
                self.add("duplicate_interval", path, "Each interval needs its own traceable ID; values may repeat", "M8.2")
            for i, interval in enumerate(intervals):
                if interval["state_id"] != ids[i] or interval["start"] >= interval["end"]:
                    self.add("interval_binding", path, "Interval needs the ordered state and positive extent", "M8.2")
                if i and (interval["start"] != intervals[i-1]["end"] or interval["clock_id"] != intervals[i-1]["clock_id"]):
                    self.add("interval_gap_overlap", path, "Complete intervals must be adjacent on one declared clock", "M7")
                if i < len(tids):
                    transition = transitions[tids[i]]
                    if (transition["from_state"], transition["to_state"]) != (ids[i], ids[i+1]):
                        self.add("chain_transition_order", path, "Transition endpoints do not follow the ordered state intervals", "M8.2")

    def endpoint(self, endpoint, state, edge, prompts, where):
        document = prompts.get(endpoint["document_id"])
        if document is None:
            self.add("prompt_document_missing", where, "Readonly prompt document is absent", "M11")
            return
        declaration = document["declarations"].get(endpoint["declaration_id"])
        if declaration is None:
            self.add("prompt_declaration_missing", where, "Explicit prompt state declaration is absent", "M11")
            return
        if document["document_id"] != endpoint["document_id"] or document["shot_id"] != state["shot_id"]:
            self.add("prompt_shot_binding", where, "Prompt belongs to a different shot", "M11")
        if declaration["declaration_id"] != endpoint["declaration_id"] or declaration["edge"] != edge or declaration["state_id"] != state["state_id"]:
            self.add("prompt_endpoint_binding", where, "Declaration must identify the exact final/initial state", "M11")
        if not same(declaration["attributes"], state["attributes"]):
            self.add("prompt_state_mismatch", where, "Readonly prompt declaration differs from the planned endpoint state", "M8.2")
        for attr, fact in declaration["attributes"].items():
            if not known(fact):
                continue
            span = declaration["spans"].get(attr)
            if span is None:
                self.add("prompt_attribute_unsubstantiated", where + "/" + attr, "Table/declaration alone is insufficient; each known value needs a literal body span", "M11")
                continue
            start, end, quote = span["start"], span["end"], span["quote"]
            if start >= end or end > len(document["text"]) or document["text"][start:end] != quote:
                self.add("prompt_span_mismatch", where + "/" + attr, "Unicode code-point span/quote does not match the readonly body", "M11")
            elif fact["value"] not in quote:
                self.add("prompt_value_absent", where + "/" + attr, "The declared literal state value does not occur in its cited body span", "M11")

    def actual(self, handoff, before, after, policy, inputs, work_id, base, where):
        observations = inputs.get("actual_context", {}).get("values", {}).get("observations", {})
        related = {k: v for k, v in observations.items() if v["state_id"] == before["state_id"]}
        continuation = handoff["continuation"]
        decision = continuation["decision"]
        ident = continuation.get("observation_id")
        if decision == "planned_only":
            if ident is not None or related:
                self.add("actual_observation_ignored", where, "Available actual observations require an explicit continuation decision; planned end cannot be silently reused", "M8.3")
            return
        if ident not in related:
            self.add("actual_observation_missing", where, "Continuation must link the applicable immutable M12 observation", "M12")
            return
        observation = related[ident]
        if observation["observation_id"] != ident or observation["plan_work_id"] != work_id or observation["plan_version"] > base or observation["plan_state_digest"] != digest(before):
            self.add("actual_plan_binding", where, "Observation must bind this work, an existing plan version and the exact planned state digest", "M12")
        self.add("actual_authenticity_unverified", where, "Only declared M12 metadata/binding is checked; observation truth and generated-media quality are not verified", "M12", "unverified")
        observed = observation["attributes"]
        differing = {a for a in set(observed) & set(before["attributes"]) if known(observed[a]) and known(before["attributes"][a]) and not value_equal(observed[a], before["attributes"][a])}
        if observation["verdict"] == "consistent" and differing:
            self.add("actual_verdict_conflict", where, "Declared consistent observation contains a state difference", "M12")
        if observation["verdict"] == "deviation" and not differing:
            self.add("actual_deviation_unsubstantiated", where, "Deviation needs a declared differing attribute; do not invent an actual result", "M12")
        if decision == "continue_from_observed":
            if observation["verdict"] == "unknown":
                self.add("unknown_actual_continue", where, "Unknown observation cannot authorize actual-state continuation", "M12")
            required = set(policy["invariants"]) | set(policy["match_attributes"])
            if policy["boundary_type"] in CONTINUOUS:
                required |= {a for a in before["attributes"] if physical(a)}
            for attr in required:
                if not known(observed.get(attr)):
                    self.add("actual_attribute_unknown", where + "/" + attr, "Actual continuation requires the relevant observed attribute", "M12")
                elif not value_equal(observed[attr], after["attributes"].get(attr)):
                    self.add("actual_continue_mismatch", where + "/" + attr, "Next planned start fails to follow the declared observed state; return a revision to M8.2", "M8.2")
        else:
            self.add("continuation_pending", where, "Explicit decision is " + decision + "; continuation remains pending and is not production approval", "M8.2" if decision == "replan" else "M12", "unverified")

    def handoffs(self, handoffs, policies, ledger, inputs, work_id, base, where="/content/ContinuityHandoffs"):
        prompts = inputs.get("prompt_context", {}).get("values", {}).get("documents", {})
        for key, handoff in handoffs["items"].items():
            path = where + "/items/" + key
            policy = policies["items"].get(handoff["policy_id"])
            before, after = ledger["states"].get(handoff["from_state"]), ledger["states"].get(handoff["to_state"])
            if key != handoff["handoff_id"]:
                self.add("record_identity", path, "Handoff key differs from ID", "M8.3")
            if policy is None or before is None or after is None:
                self.add("handoff_reference", path, "Policy or planned endpoint state is absent", "M8.2")
                continue
            if (before["shot_id"], after["shot_id"]) != (policy["from_shot"], policy["to_shot"]):
                self.add("handoff_shot_binding", path, "Planned endpoint shots do not match the boundary policy", "M8.3")
            if before["phase"] != "final" or after["phase"] != "initial":
                self.add("handoff_phase", path, "Boundary requires the previous final and next initial planned states", "M8.2")
            for side, state in (("from", before), ("to", after)):
                if not same(handoff["table"][side], state["attributes"]):
                    self.add("handoff_table_mismatch", path + "/table/" + side, "Handoff table differs from the readonly planned ledger", "M8.3")
            self.endpoint(handoff["previous_prompt"], before, "final", prompts, path + "/previous_prompt")
            self.endpoint(handoff["next_prompt"], after, "initial", prompts, path + "/next_prompt")
            attrs = set(before["attributes"]) | set(after["attributes"])
            required = set(policy["invariants"]) | (set(policy["match_attributes"]) if policy["boundary_type"] == "match_cut" else set())
            if policy["boundary_type"] in CONTINUOUS:
                required |= {a for a in attrs if physical(a)}
            changed = set()
            for attr in attrs | required:
                left, right = before["attributes"].get(attr), after["attributes"].get(attr)
                if left is None or right is None:
                    self.add("handoff_attribute_missing", path + "/" + attr, "Tracked endpoint attribute is missing; use explicit unknown when unavailable", "M8.2")
                elif not known(left) or not known(right):
                    self.add("continuity_unverified", path + "/" + attr, "Unknown endpoint cannot establish this continuity relation", "M8.3", "unverified")
                elif not value_equal(left, right):
                    changed.add(attr)
                    if attr in set(policy["invariants"]) or (policy["boundary_type"] == "match_cut" and attr in policy["match_attributes"]):
                        self.add("boundary_invariant_mismatch", path + "/" + attr, "Scoped invariant or selected match attribute differs", "M8.2")
            transitions = [t for t in ledger["transitions"].values() if (t["from_state"], t["to_state"]) == (before["state_id"], after["state_id"])]
            allowed = {p["attribute"] for p in policy["allowed_changes"]}
            for attr in changed - set(policy["invariants"]):
                if policy["boundary_type"] in CONTINUOUS:
                    represented = any(attr in t["changed_attributes"] and (t["mode"] == "process" or (not physical(attr) and t["mode"] == "boundary" and t.get("policy_id") == policy["policy_id"] and attr in allowed)) for t in transitions)
                    if not represented:
                        self.add("continuous_reset", path + "/" + attr, "Continuous change requires a traceable process or an explicitly allowed nonphysical boundary transition", "M8.2")
                elif attr not in allowed:
                    self.add("boundary_change_permission", path + "/" + attr, "Match/montage/ellipsis changed an attribute outside scoped permission", "M8.1")
            self.actual(handoff, before, after, policy, inputs, work_id, base, path + "/continuation")

    def domain(self, content, sources, inputs, module, work_id, base):
        self.refs(content, sources, "/content")
        policies = content.get("ContinuityPolicy") or inputs.get("policy_context", {}).get("values") or EMPTY["ContinuityPolicy"]
        ledger = content.get("StateLedger") or inputs.get("ledger_context", {}).get("values") or EMPTY["StateLedger"]
        self.policies(policies, inputs)
        if module in ("M8.2", "M8.3"):
            # External ledger adapters are checked too: standalone does not mean unchecked.
            self.ledger(ledger, policies, inputs)
        if module == "M8.3":
            observations = inputs.get("actual_context", {}).get("values", {}).get("observations", {})
            for key, observation in observations.items():
                if not any(sources.get(s, {}).get("kind") == "media_observation" for s in observation["source_refs"]):
                    self.add("actual_source_kind", "/inputs/actual_context/" + key, "Actual observation requires a media_observation source", "M12")
            self.handoffs(content["ContinuityHandoffs"], policies, ledger, inputs, work_id, base)

    def proposal(self, proposal, request=None, path=""):
        if not self.shape(proposal, "M8Proposal", path):
            return False
        module = proposal["module_id"]
        if request is None:
            self.add("original_request_required", path, "Supply the actual original request; a proposal's self-reported context is not sufficient", module)
            return False
        if not self.request(request, path + "/original_request"):
            return False
        if (request["request_id"], request["target"], request["work_id"], request["base_version"]) != (proposal["source_request_id"], module, proposal["work_id"], proposal["base_version"]):
            self.add("request_identity", path, "Request ID, exact target, work and base version must match", module)
        if not same(request["sources"], proposal["sources"]) or not same(request["inputs"], proposal["context"]):
            self.add("request_fidelity", path, "Proposal sources and readonly context differ from the actual original request", module)
        if set(proposal["changes"]) != {OWNED[module]}:
            self.add("write_scope", path + "/changes", "Child may write exactly its own public partition", module)
        for issue in proposal["issues"]:
            if issue["owner"] != module or issue["status"] != "open":
                self.add("issue_ownership", path + "/issues", "Child can only create its own open issues", module)
        self.refs(proposal["issues"], proposal["sources"], path + "/issues")
        self.refs(proposal["resolutions"], proposal["sources"], path + "/resolutions")
        if self.failed:
            return False
        self.domain(proposal["changes"], proposal["sources"], proposal["context"], module, proposal["work_id"], proposal["base_version"])
        return not self.failed

    def state(self, state, reject_blockers=True):
        if not self.shape(state, "M8State"):
            return False
        self.refs(state["content"], state["sources"], "/content")
        self.refs(state["issues"], state["sources"], "/issues")
        for module, context in state["contexts"].items():
            self.inputs(context, state["sources"], state["version"], module, "/contexts/" + module, accepted=True)
        if self.failed:
            return False
        for module, part in OWNED.items():
            populated = any(state["content"][part].values())
            if populated and module not in state["contexts"]:
                self.add("accepted_context_missing", "/contexts/" + module, "Accepted records require their readonly input snapshot", module)
            elif populated:
                self.domain(state["content"], state["sources"], state["contexts"][module], module, state["work_id"], state["version"])
        for key, receipt in state["accepted_proposals"].items():
            if receipt["accepted_version"] > state["version"]:
                self.add("receipt_version", "/accepted_proposals/" + key, "Receipt claims a future parent version")
        for key, issue in state["issues"].items():
            if key != issue["issue_id"] or (issue["status"] == "resolved") != ("resolution" in issue):
                self.add("issue_identity", "/issues/" + key, "Issue key/status/resolution are inconsistent")
            if reject_blockers and issue["status"] == "open" and issue["severity"] == "blocking":
                self.add("open_blocker", "/issues/" + key, issue["message"], issue["owner"])
        for key, consumer in state["consumers"].items():
            if consumer["source_state_version"] > state["version"]:
                self.add("consumer_version", "/consumers/" + key, "Consumer cites a future source version")
            for path in consumer["read_paths"]:
                try:
                    pointer(state, path)
                except (KeyError, ValueError, IndexError, TypeError):
                    self.add("consumer_path", "/consumers/" + key, "Unresolved registered read path: " + path)
        return not self.failed


def changed_paths(before, after, path=""):
    if isinstance(before, dict) and isinstance(after, dict):
        result = []
        for key in sorted(set(before) | set(after)):
            child = path + "/" + key.replace("~", "~0").replace("/", "~1")
            result += [child] if key not in before or key not in after else changed_paths(before[key], after[key], child)
        return result
    return [] if same(before, after) else [path]


def overlaps(a, b):
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def impact(before, after):
    paths = [p for p in changed_paths(before, after) if any(overlaps(p, root) for root in ("/content", "/sources", "/contexts", "/issues", "/display"))]
    stale = {}
    for key, consumer in before["consumers"].items():
        touched = [p for p in paths if any(overlaps(p, r) for r in consumer["read_paths"])]
        if touched or consumer["status"] == "stale":
            stale[key] = {"module_id": consumer["module_id"], "status": "stale", "changed_paths": touched, "already_stale": consumer["status"] == "stale"}
    return {"changed_paths": paths, "stale_consumers": stale, "scope": "Registered read-path intersections; hidden semantic dependencies remain unverified"}


def request_index(check, requests):
    if not isinstance(requests, list):
        check.add("requests_array", "/requests", "Original requests must be a JSON array")
        return {}
    result = {}
    for i, request in enumerate(requests):
        if check.request(request, "/requests/" + str(i)):
            if request["request_id"] in result:
                check.add("duplicate_request", "/requests/" + str(i), "Duplicate request ID")
            result[request["request_id"]] = request
    return result


def accept(check, state, batch, requests):
    state_ok = check.state(state, reject_blockers=False)
    batch_ok = check.shape(batch, "M8ProposalBatch", "/batch")
    index = request_index(check, requests)
    if not state_ok or not batch_ok or check.failed:
        return None
    proposals = batch["proposals"]
    if batch["work_id"] != state["work_id"]:
        check.add("work_identity", "/batch", "Batch addresses a different parent state")
    if len({p["proposal_id"] for p in proposals}) != len(proposals) or len({p["module_id"] for p in proposals}) != len(proposals):
        check.add("partition_conflict", "/batch", "Each proposal ID and child partition must be unique in an atomic batch")
    replays = []
    for i, proposal in enumerate(proposals):
        path = "/batch/proposals/" + str(i)
        request = index.get(proposal["source_request_id"])
        check.proposal(proposal, request, path)
        if (proposal["work_id"], proposal["base_version"]) != (batch["work_id"], batch["base_version"]):
            check.add("batch_binding", path, "Proposal work/base does not match batch")
        receipt = state["accepted_proposals"].get(proposal["proposal_id"])
        replays.append(receipt is not None)
        if receipt and (receipt["digest"] != digest(proposal) or request is None or receipt["request_digest"] != digest(request) or receipt["module_id"] != proposal["module_id"] or receipt["source_request_id"] != proposal["source_request_id"]):
            check.add("idempotency_conflict", path, "Accepted operation ID was reused with changed content or original request")
    if check.failed:
        return None
    if all(replays):
        check.state(state)
        return None if check.failed else {"state": copy.deepcopy(state), "acceptance": "idempotent_replay", "impact": impact(state, state)}
    if any(replays):
        check.add("mixed_replay", "/batch", "Do not mix exact retries with new writes")
    if batch["base_version"] != state["version"]:
        check.add("stale_base_version", "/batch", "Refresh the original requests against the current parent version")
    if check.failed:
        return None
    candidate = copy.deepcopy(state)
    for proposal in proposals:
        module = proposal["module_id"]
        part = OWNED[module]
        replacement = proposal["changes"][part]
        for group, records in state["content"][part].items():
            for key, record in records.items():
                if key not in replacement[group] or not same(record, replacement[group][key]):
                    check.add("accepted_history_changed", "/content/" + part + "/" + group + "/" + key, "Accepted records are immutable; append a new ID and retain prior plans/observations", module)
        candidate["content"][part] = copy.deepcopy(replacement)
        candidate["contexts"][module] = copy.deepcopy(proposal["context"])
        for key, source in proposal["sources"].items():
            if key in candidate["sources"] and not same(candidate["sources"][key], source):
                check.add("source_collision", "/sources/" + key, "Source ID/version/provenance cannot be rebound", module)
            candidate["sources"][key] = copy.deepcopy(source)
        for issue in proposal["issues"]:
            key = issue["issue_id"]
            if key in candidate["issues"] and not same(issue, candidate["issues"][key]):
                check.add("issue_collision", "/issues/" + key, "Existing issue cannot be overwritten", module)
            candidate["issues"][key] = copy.deepcopy(issue)
        for resolution in proposal["resolutions"]:
            key = resolution["issue_id"]
            issue = candidate["issues"].get(key)
            if issue is None or issue["owner"] != module or issue["status"] != "open":
                check.add("resolution_ownership", "/issues/" + key, "Only the owner may resolve its existing open issue", module)
            else:
                issue["status"] = "resolved"
                issue["resolution"] = {"state": "known", "value": resolution["rationale"], "source_refs": resolution["source_refs"]}
    for proposal in proposals:
        for field, part in (("policy_context", "ContinuityPolicy"), ("ledger_context", "StateLedger")):
            if field in proposal["context"] and not same(proposal["context"][field]["values"], candidate["content"][part]):
                check.add("readonly_conflict", "/context/" + field, "Standalone adapters are valid for checks; parent acceptance requires the exact current/batched owned partition", proposal["module_id"])
        for projection in proposal["context"].get("readonly_projection", []):
            try:
                if not same(pointer(state, projection["path"]), projection["value"]):
                    check.add("readonly_projection_changed", projection["path"], "Projection does not match the real parent at its declared base", proposal["module_id"])
            except (KeyError, ValueError, TypeError, IndexError):
                check.add("readonly_projection_missing", projection["path"], "Projection path is absent from the real parent", proposal["module_id"])
    if check.failed:
        return None
    candidate["version"] += 1
    for proposal in proposals:
        request = index[proposal["source_request_id"]]
        candidate["accepted_proposals"][proposal["proposal_id"]] = {"digest": digest(proposal), "request_digest": digest(request), "source_request_id": proposal["source_request_id"], "module_id": proposal["module_id"], "accepted_version": candidate["version"]}
    result_impact = impact(state, candidate)
    for key in result_impact["stale_consumers"]:
        candidate["consumers"][key]["status"] = "stale"
    check.state(candidate)
    return None if check.failed else {"state": candidate, "acceptance": "accepted_draft", "impact": result_impact}


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    def finite(value):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("Non-finite JSON number")
        return number
    def invalid(value):
        raise ValueError("Non-finite JSON constant: " + value)
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs, parse_float=finite, parse_constant=invalid)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("route", "check"):
        sub = commands.add_parser(command)
        sub.add_argument("artifact")
        sub.add_argument("--request")
        sub.add_argument("--requests")
    sub = commands.add_parser("accept")
    sub.add_argument("state")
    sub.add_argument("batch")
    sub.add_argument("--requests", required=True)
    sub = commands.add_parser("impact")
    sub.add_argument("--before", required=True)
    sub.add_argument("--after", required=True)
    args = parser.parse_args(argv)
    check = Check()
    payload = {}
    resources = {}
    identities = {"work_ids": set(), "request_ids": set(), "module_ids": set(), "proposal_ids": set(), "base_versions": set()}
    source_versions = {}
    def record_identity(data):
        if isinstance(data, list):
            for item in data:
                record_identity(item)
        elif isinstance(data, dict):
            for field, target in (("work_id", "work_ids"), ("request_id", "request_ids"), ("source_request_id", "request_ids"), ("target", "module_ids"), ("module_id", "module_ids"), ("proposal_id", "proposal_ids"), ("base_version", "base_versions")):
                value = data.get(field)
                if type(value) in (str, int):
                    identities[target].add(value)
            for key, source in data.get("sources", {}).items() if isinstance(data.get("sources"), dict) else []:
                if isinstance(source, dict) and isinstance(source.get("version"), str):
                    source_versions.setdefault(key, set()).add(source["version"])
            if isinstance(data.get("proposals"), list):
                record_identity(data["proposals"])
    def read(path):
        data = load_json(path)
        resources[str(path)] = digest(data)
        record_identity(data)
        return data
    try:
        if args.command == "route":
            request = read(args.artifact)
            check.request(request)
            if not check.failed:
                registry = load_json(ROOT / "references/module-registry.json")
                modules = list(OWNED) if request["target"] == "M8" else [request["target"]]
                routes = [{"module_id": module, "resources": registry["modules"][module]["resources"], "write_scope": "/content/" + OWNED[module], "minimum_inputs": list(MINIMUM[module]), "missing_inputs": [key for key in MINIMUM[module] if key not in request["inputs"]], "return_to": "M8", "repair_target": module} for module in modules]
                for route in routes:
                    route["call_ready"] = not route["missing_inputs"]
                payload = {"routes": routes, "route_status": "requires_child_inputs" if any(r["missing_inputs"] for r in routes) else ("ready_with_unverified_inputs" if check.diagnostics else "ready_for_call"), "invocation": "not_invoked"}
        elif args.command == "check":
            artifact = read(args.artifact)
            request = read(args.request) if args.request else None
            index = request_index(check, read(args.requests)) if args.requests else {}
            if check.shape(artifact):
                kind = artifact["kind"]
                if kind == "M8Request":
                    check.request(artifact)
                elif kind == "M8State":
                    check.state(artifact)
                elif kind == "M8Proposal":
                    check.proposal(artifact, request or index.get(artifact["source_request_id"]))
                else:
                    proposals = artifact["proposals"]
                    if len({p["module_id"] for p in proposals}) != len(proposals) or len({p["proposal_id"] for p in proposals}) != len(proposals):
                        check.add("partition_conflict", "/proposals", "Duplicate child/operation ID")
                    for proposal in proposals:
                        if (proposal["work_id"], proposal["base_version"]) != (artifact["work_id"], artifact["base_version"]):
                            check.add("batch_binding", "/proposals", "Proposal work/base differs from batch")
                        check.proposal(proposal, index.get(proposal["source_request_id"]))
        elif args.command == "accept":
            payload = accept(check, read(args.state), read(args.batch), read(args.requests)) or {}
        else:
            before, after = read(args.before), read(args.after)
            check.state(before, reject_blockers=False)
            check.state(after, reject_blockers=False)
            if before.get("work_id") != after.get("work_id"):
                check.add("work_identity", "", "Impact comparison must use one work")
            if not check.failed:
                payload = {"impact": impact(before, after)}
    except (OSError, ValueError, KeyError, IndexError, TypeError, OverflowError) as exc:
        check.add("execution_error", "", type(exc).__name__ + ": " + str(exc))
    status = "failed" if check.failed else ("passed_with_unverified" if check.diagnostics else "passed")
    result = {"kind": "M8ToolResult", "contract_version": VERSION, "command": args.command, "status": status, "diagnostics": check.diagnostics, **payload,
              "trace": {"parent_module": "M8", "route_version": VERSION, "contract_version": VERSION, "contract_digest": digest(check.schema), "timestamp_utc": datetime.now(timezone.utc).isoformat(), "resource_digests": resources, **{key: sorted(values, key=str) for key, values in identities.items()}, "source_versions": {key: sorted(values) for key, values in source_versions.items()}, "operation_id": digest({"command": args.command, "resources": resources}), "status": status, "repair_targets": sorted({d["repair_target"] for d in check.diagnostics}), "recheck": "not_automatically_invoked", "operation_effect": "pure_json_output", "media_verification": "not_performed", "text_semantics": "explicit_literal_declarations_only"}}
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 2 if check.failed else 0


if __name__ == "__main__":
    sys.exit(main())
