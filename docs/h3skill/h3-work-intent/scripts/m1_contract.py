#!/usr/bin/env python3
"""Offline, explicit M1 contracts. This program does not interpret creative prose.

Commands read JSON and write a new JSON result to stdout; input files are never
modified. A successful structural check is not a semantic or media-quality pass.
Only the Python standard library is required. See ../references/contracts.json.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

CONTRACT_VERSION = "1.0.0"
PACKAGE_VERSION = "0.1.0"
OWNED = {
    "M1.1": ("intent", "constraints", "must_keep_events"),
    "M1.2": ("paragraphs",),
    "M1.3": ("emotion_energy", "motifs"),
}
FIELDS = tuple(field for fields in OWNED.values() for field in fields)
OWNER = {field: module for module, fields in OWNED.items() for field in fields}
MODULES = ("M1",) + tuple(OWNED)
REPAIR_MODULES = ("user",) + MODULES + tuple(f"M{i}" for i in range(2, 13))
INPUTS = {
    "M1": ("work_type", "creative_request"),
    "M1.1": ("work_type", "creative_request"),
    "M1.2": ("work_type", "intent_context", "paragraph_material"),
    "M1.3": ("work_type", "intent_context", "emotion_material"),
}
OPTIONAL_INPUTS = ("delivery_use", "notes")
SOURCE_KINDS = (
    "user_requirement", "case_text", "design_decision", "external_input",
    "official_document", "hypothesis",
)
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,63}$")
ROOT = Path(__file__).resolve().parents[1]
STRUCTURAL_CODES = {
    "invalid_type", "missing_field", "undeclared_field", "invalid_text", "invalid_id",
    "invalid_version_or_order", "invalid_enum", "empty_array", "duplicate_value",
    "missing_source", "unresolved_source", "incompatible_contract", "undeclared_input",
    "scope_mismatch", "invalid_duration", "invalid_batch", "empty_change", "out_of_scope",
    "duplicate_issue_id", "duplicate_resolution", "invalid_history_version", "future_history",
    "duplicate_proposal_id", "history_out_of_scope", "future_dependency", "duplicate_consumer_id",
    "invalid_dependency_path", "unresolved_dependency_path", "unknown_artifact_kind",
    "input_or_resource_error", "wrong_result_kind",
}


def pointer_escape(value):
    return str(value).replace("~", "~0").replace("/", "~1")


def at(path, key):
    return path + "/" + pointer_escape(key)


def is_unknown(value):
    return isinstance(value, dict) and value.get("state") == "unknown"


def fields_for(module):
    return FIELDS if module == "M1" else OWNED.get(module, ())


def pointer_value(document, pointer):
    """Read a standard JSON Pointer, rejecting invalid escapes and indices."""
    if pointer == "":
        return document
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise KeyError(pointer)
    node = document
    for token in pointer[1:].split("/"):
        if re.search(r"~(?:[^01]|$)", token):
            raise KeyError(pointer)
        key = token.replace("~1", "/").replace("~0", "~")
        if isinstance(node, dict):
            node = node[key]
        elif isinstance(node, list) and re.fullmatch(r"0|[1-9][0-9]*", key):
            node = node[int(key)]
        else:
            raise KeyError(pointer)
    return node


class Validation:
    """Explicit validators for named contract types, not a JSON Schema engine."""

    def __init__(self):
        self.diagnostics = []

    def add(self, code, path, message, owner="M1", status="fail", blocking=True):
        self.diagnostics.append({
            "code": code, "path": path, "message": message,
            "status": status, "blocking": blocking, "repair_target": owner,
            "recheck": "Resubmit the corrected input to the same command.",
        })

    def obj(self, value, path, required=(), optional=()):
        if not isinstance(value, dict):
            self.add("invalid_type", path, "Expected a JSON object.")
            return False
        for key in required:
            if key not in value:
                self.add("missing_field", at(path, key), "Required field is missing.")
        for key in value.keys() - set(required) - set(optional):
            self.add("undeclared_field", at(path, key), "Field is not in this contract.")
        return True

    def text(self, value, path, unknown=False):
        if unknown and is_unknown(value):
            self.obj(value, path, ("state", "reason"))
            self.text(value.get("reason"), at(path, "reason"))
            self.add("unknown_value", path, "Explicitly unknown; not treated as not applicable.",
                     status="unverified", blocking=False)
            return False
        if not isinstance(value, str) or not value.strip():
            self.add("invalid_text", path, "Expected a non-empty string.")
            return False
        return True

    def ident(self, value, path):
        if not isinstance(value, str) or not ID_RE.fullmatch(value):
            self.add("invalid_id", path, "Use 1–64 ASCII letters, digits, dots, underscores or hyphens; start with a letter.")
            return False
        return True

    def integer(self, value, path, minimum=0):
        if type(value) is not int or value < minimum:
            self.add("invalid_version_or_order", path, f"Expected an integer >= {minimum}.")
            return False
        return True

    def enum(self, value, path, choices, unknown=False):
        if unknown and is_unknown(value):
            return self.text(value, path, unknown=True)
        if not isinstance(value, str) or value not in choices:
            self.add("invalid_enum", path, "Allowed values: " + ", ".join(choices))
            return False
        return True

    def sequence(self, value, path, identifiers=False, nonempty=False):
        if not isinstance(value, list):
            self.add("invalid_type", path, "Expected an array.")
            return []
        if nonempty and not value:
            self.add("empty_array", path, "At least one item is required.")
        seen = set()
        for index, item in enumerate(value):
            valid = self.ident(item, at(path, index)) if identifiers else self.text(item, at(path, index))
            if valid:
                if item in seen:
                    self.add("duplicate_value", at(path, index), "Duplicate array item.")
                seen.add(item)
        return value

    def sources(self, value, path, nonempty=True):
        if not isinstance(value, dict):
            self.add("invalid_type", path, "Expected a source-ID keyed object.")
            return {}
        if nonempty and not value:
            self.add("missing_source", path, "At least one versioned source is required.", "user")
        for source_id, record in value.items():
            self.ident(source_id, at(path, source_id))
            p = at(path, source_id)
            if self.obj(record, p, ("kind", "locator", "version", "excerpt")):
                self.enum(record.get("kind"), at(p, "kind"), SOURCE_KINDS)
                for key in ("locator", "version", "excerpt"):
                    self.text(record.get(key), at(p, key))
        return value

    def refs(self, value, path, sources):
        refs = self.sequence(value, path, identifiers=True, nonempty=True)
        for index, reference in enumerate(refs):
            if isinstance(reference, str) and reference not in sources:
                self.add("unresolved_source", at(path, index), "Source ID does not resolve in this artifact.", "user")

    def header(self, value, path, kind, required, optional=()):
        if not self.obj(value, path, ("kind", "contract_version") + tuple(required), optional):
            return False
        self.enum(value.get("kind"), at(path, "kind"), (kind,))
        if value.get("contract_version") != CONTRACT_VERSION:
            self.add("incompatible_contract", at(path, "contract_version"),
                     "Only contract 1.0.0 is supported; migrate explicitly.")
        return True

    def work_type(self, value, path):
        self.enum(value, path, ("drama", "mv", "hybrid"), unknown=True)

    def request(self, value, path=""):
        if not self.header(value, path, "M1Request",
                           ("request_id", "target", "work_id", "base_version", "sources", "inputs"),
                           ("requested_fields",)):
            return
        self.ident(value.get("request_id"), at(path, "request_id"))
        self.ident(value.get("work_id"), at(path, "work_id"))
        self.integer(value.get("base_version"), at(path, "base_version"))
        self.enum(value.get("target"), at(path, "target"), MODULES)
        self.sources(value.get("sources"), at(path, "sources"))
        target = value.get("target")
        required_inputs = INPUTS.get(target, ()) if isinstance(target, str) else ()
        inputs = value.get("inputs")
        if isinstance(inputs, dict):
            for key in inputs.keys() - set(required_inputs) - set(OPTIONAL_INPUTS):
                self.add("undeclared_input", at(at(path, "inputs"), key), "Not in the target module's input projection.")
            for key in required_inputs:
                p = at(at(path, "inputs"), key)
                if key not in inputs:
                    self.add("missing_input", p, "Required task input is missing.", "user", "unverified")
                elif is_unknown(inputs[key]):
                    self.text(inputs[key], p, unknown=True)
                    self.add("unknown_input", p, "Provide the missing information before this node's semantic work.",
                             "user", "unverified")
                elif key == "work_type":
                    self.work_type(inputs[key], p)
                else:
                    self.text(inputs[key], p)
            for key in OPTIONAL_INPUTS:
                if key in inputs:
                    self.text(inputs[key], at(at(path, "inputs"), key), unknown=True)
        else:
            self.add("invalid_type", at(path, "inputs"), "Expected an object of projected inputs.")
        if "requested_fields" in value:
            names = self.sequence(value["requested_fields"], at(path, "requested_fields"), nonempty=True)
            allowed = fields_for(target) if isinstance(target, str) else ()
            for name in names:
                if name not in allowed:
                    self.add("out_of_scope", at(path, "requested_fields"), "Requested field is outside the target's ownership.")

    def scope(self, value, path):
        if self.obj(value, path, ("kind", "paragraph_ids")):
            self.enum(value.get("kind"), at(path, "kind"), ("work", "paragraph"))
            ids = self.sequence(value.get("paragraph_ids"), at(path, "paragraph_ids"), identifiers=True)
            if value.get("kind") == "work" and ids:
                self.add("scope_mismatch", path, "Work scope must use an empty paragraph_ids list.")
            if value.get("kind") == "paragraph" and not ids:
                self.add("scope_mismatch", path, "Paragraph scope requires at least one paragraph ID.")

    def content(self, value, path, sources):
        if not self.obj(value, path, (), FIELDS):
            return
        for field, data in value.items():
            p = at(path, field)
            if field == "intent":
                if self.obj(data, p, ("work_type", "creative_goal", "audience_takeaway", "delivery_use", "source_refs"),
                            ("target_duration",)):
                    self.work_type(data.get("work_type"), at(p, "work_type"))
                    for key in ("creative_goal", "audience_takeaway", "delivery_use"):
                        self.text(data.get(key), at(p, key), unknown=True)
                    self.refs(data.get("source_refs"), at(p, "source_refs"), sources)
                    if "target_duration" in data:
                        duration = data["target_duration"]
                        dp = at(p, "target_duration")
                        if is_unknown(duration):
                            self.text(duration, dp, unknown=True)
                        elif self.obj(duration, dp, ("seconds", "domain", "basis", "source_refs")):
                            n = duration.get("seconds")
                            if type(n) not in (int, float) or not math.isfinite(n) or n <= 0:
                                self.add("invalid_duration", at(dp, "seconds"), "Duration must be a positive finite requested value.")
                            self.enum(duration.get("domain"), at(dp, "domain"), ("final_work", "generation_request"))
                            self.enum(duration.get("basis"), at(dp, "basis"), ("requested",))
                            self.refs(duration.get("source_refs"), at(dp, "source_refs"), sources)
                continue
            if field not in FIELDS:
                continue
            if not isinstance(data, dict):
                self.add("invalid_type", p, "Expected an ID-keyed object.")
                continue
            for record_id, record in data.items():
                rp = at(p, record_id)
                self.ident(record_id, rp)
                if field == "constraints":
                    if self.obj(record, rp, ("text", "priority", "scope", "source_refs")):
                        self.text(record.get("text"), at(rp, "text"), unknown=True)
                        self.enum(record.get("priority"), at(rp, "priority"), ("must", "should", "may"))
                        self.scope(record.get("scope"), at(rp, "scope"))
                        self.refs(record.get("source_refs"), at(rp, "source_refs"), sources)
                elif field == "must_keep_events":
                    if self.obj(record, rp, ("description", "source_refs")):
                        self.text(record.get("description"), at(rp, "description"), unknown=True)
                        self.refs(record.get("source_refs"), at(rp, "source_refs"), sources)
                elif field == "paragraphs":
                    required = ("order", "function", "audience_information_before", "audience_information_after",
                                "must_keep_event_ids", "information_predecessors", "source_refs")
                    if self.obj(record, rp, required, ("character_objectives", "performance_focus")):
                        self.integer(record.get("order"), at(rp, "order"), 1)
                        self.text(record.get("function"), at(rp, "function"), unknown=True)
                        for key in ("audience_information_before", "audience_information_after"):
                            self.sequence(record.get(key), at(rp, key))
                        for key in ("must_keep_event_ids", "information_predecessors"):
                            self.sequence(record.get(key), at(rp, key), identifiers=True)
                        self.refs(record.get("source_refs"), at(rp, "source_refs"), sources)
                        if "character_objectives" in record:
                            objectives = record["character_objectives"]
                            if not isinstance(objectives, dict):
                                self.add("invalid_type", at(rp, "character_objectives"), "Expected a supplied character-label to goal mapping.")
                            else:
                                for label, goal in objectives.items():
                                    self.text(label, at(rp, "character_objectives"))
                                    self.text(goal, at(at(rp, "character_objectives"), label), unknown=True)
                        if "performance_focus" in record:
                            self.text(record["performance_focus"], at(rp, "performance_focus"), unknown=True)
                elif field == "emotion_energy":
                    if self.obj(record, rp, ("emotion_start", "emotion_end", "energy_intent", "source_refs")):
                        for key in ("emotion_start", "emotion_end", "energy_intent"):
                            self.text(record.get(key), at(rp, key), unknown=True)
                        self.refs(record.get("source_refs"), at(rp, "source_refs"), sources)
                elif field == "motifs":
                    if self.obj(record, rp, ("description", "paragraph_ids", "development", "source_refs")):
                        self.text(record.get("description"), at(rp, "description"), unknown=True)
                        self.text(record.get("development"), at(rp, "development"), unknown=True)
                        self.sequence(record.get("paragraph_ids"), at(rp, "paragraph_ids"), identifiers=True, nonempty=True)
                        self.refs(record.get("source_refs"), at(rp, "source_refs"), sources)

    def issue(self, value, path, sources):
        if self.obj(value, path, ("id", "code", "status", "message", "owner_module", "field", "blocking", "source_refs")):
            self.ident(value.get("id"), at(path, "id"))
            for key in ("code", "message", "field"):
                self.text(value.get(key), at(path, key))
            self.enum(value.get("status"), at(path, "status"), ("fail", "unverified", "conflict"))
            self.enum(value.get("owner_module"), at(path, "owner_module"), REPAIR_MODULES)
            if type(value.get("blocking")) is not bool:
                self.add("invalid_type", at(path, "blocking"), "Expected a boolean.")
            self.refs(value.get("source_refs"), at(path, "source_refs"), sources)

    def issues(self, value, path, sources):
        if not isinstance(value, list):
            self.add("invalid_type", path, "Expected an issues array.")
            return
        seen = set()
        for i, issue in enumerate(value):
            self.issue(issue, at(path, i), sources)
            if isinstance(issue, dict) and isinstance(issue.get("id"), str):
                if issue["id"] in seen:
                    self.add("duplicate_issue_id", at(at(path, i), "id"), "Issue IDs must be unique.")
                seen.add(issue["id"])

    def proposal(self, value, path=""):
        required = ("proposal_id", "module_id", "work_id", "base_version", "source_request_id",
                    "sources", "changes", "issues", "resolutions")
        if not self.header(value, path, "M1Proposal", required):
            return
        for key in ("proposal_id", "work_id", "source_request_id"):
            self.ident(value.get(key), at(path, key))
        self.enum(value.get("module_id"), at(path, "module_id"), tuple(OWNED))
        self.integer(value.get("base_version"), at(path, "base_version"))
        sources = self.sources(value.get("sources"), at(path, "sources"))
        changes = value.get("changes")
        self.content(changes, at(path, "changes"), sources)
        if isinstance(changes, dict):
            if not changes:
                self.add("empty_change", at(path, "changes"), "A proposal must explicitly replace at least one owned partition.")
            module = value.get("module_id")
            allowed = OWNED.get(module, ()) if isinstance(module, str) else ()
            for field in changes:
                if field not in allowed:
                    self.add("out_of_scope", at(at(path, "changes"), field), "This child does not own the partition.",
                             OWNER.get(field, "M1"))
        self.issues(value.get("issues"), at(path, "issues"), sources)
        resolutions = value.get("resolutions")
        if not isinstance(resolutions, list):
            self.add("invalid_type", at(path, "resolutions"), "Expected an explicit resolutions array.")
        else:
            seen = set()
            for i, resolution in enumerate(resolutions):
                p = at(at(path, "resolutions"), i)
                if self.obj(resolution, p, ("issue_id", "reason", "source_refs")):
                    self.ident(resolution.get("issue_id"), at(p, "issue_id"))
                    self.text(resolution.get("reason"), at(p, "reason"))
                    self.refs(resolution.get("source_refs"), at(p, "source_refs"), sources)
                    issue_id = resolution.get("issue_id")
                    if isinstance(issue_id, str):
                        if issue_id in seen:
                            self.add("duplicate_resolution", p, "Resolve each issue once.")
                        seen.add(issue_id)
        self.cross_checks(changes, at(path, "changes"), partial=True)

    def batch(self, value, path=""):
        if not self.header(value, path, "M1ProposalBatch", ("proposals",)):
            return
        items = value.get("proposals")
        if not isinstance(items, list) or not items:
            self.add("invalid_batch", at(path, "proposals"), "A non-empty proposals array is required.")
            return
        for i, item in enumerate(items):
            self.proposal(item, at(at(path, "proposals"), i))

    def history(self, value, path, sources, work_version):
        if not isinstance(value, list):
            self.add("invalid_type", path, "Expected accepted_proposals array.")
            return
        seen = set()
        for index, record in enumerate(value):
            p = at(path, index)
            fields = ("proposal_id", "module_id", "source_request_id", "from_version", "to_version",
                      "changed_fields", "source_ids", "resolved_issues")
            if not self.obj(record, p, fields):
                continue
            self.ident(record.get("proposal_id"), at(p, "proposal_id"))
            self.ident(record.get("source_request_id"), at(p, "source_request_id"))
            self.enum(record.get("module_id"), at(p, "module_id"), tuple(OWNED))
            self.integer(record.get("from_version"), at(p, "from_version"))
            self.integer(record.get("to_version"), at(p, "to_version"), 1)
            if type(record.get("from_version")) is int and type(record.get("to_version")) is int:
                if record["to_version"] != record["from_version"] + 1:
                    self.add("invalid_history_version", p, "Each acceptance increments the WorkBrief version by one.")
                if type(work_version) is int and record["to_version"] > work_version:
                    self.add("future_history", p, "History cannot refer to a future WorkBrief version.")
            proposed_id = record.get("proposal_id")
            if isinstance(proposed_id, str):
                if proposed_id in seen:
                    self.add("duplicate_proposal_id", p, "A proposal cannot be accepted twice.")
                seen.add(proposed_id)
            names = self.sequence(record.get("changed_fields"), at(p, "changed_fields"), nonempty=True)
            module = record.get("module_id")
            allowed = OWNED.get(module, ()) if isinstance(module, str) else ()
            for name in names:
                if name not in allowed:
                    self.add("history_out_of_scope", at(p, "changed_fields"), "History records an unauthorized write.")
            self.refs(record.get("source_ids"), at(p, "source_ids"), sources)
            resolved = record.get("resolved_issues")
            if not isinstance(resolved, list):
                self.add("invalid_type", at(p, "resolved_issues"), "Expected an array.")
            else:
                for i, resolution in enumerate(resolved):
                    rp = at(at(p, "resolved_issues"), i)
                    if self.obj(resolution, rp, ("issue", "reason", "source_refs")):
                        self.issue(resolution.get("issue"), at(rp, "issue"), sources)
                        self.text(resolution.get("reason"), at(rp, "reason"))
                        self.refs(resolution.get("source_refs"), at(rp, "source_refs"), sources)

    def consumers(self, value, path, work):
        if not isinstance(value, list):
            self.add("invalid_type", path, "Expected a registered consumers array.")
            return
        seen = set()
        for i, consumer in enumerate(value):
            p = at(path, i)
            fields = ("consumer_id", "module_id", "version", "source_work_version", "read_paths")
            if not self.obj(consumer, p, fields):
                continue
            self.ident(consumer.get("consumer_id"), at(p, "consumer_id"))
            self.enum(consumer.get("module_id"), at(p, "module_id"), REPAIR_MODULES[1:])
            self.integer(consumer.get("version"), at(p, "version"), 1)
            self.integer(consumer.get("source_work_version"), at(p, "source_work_version"))
            if type(consumer.get("source_work_version")) is int and type(work.get("version")) is int:
                if consumer["source_work_version"] > work["version"]:
                    self.add("future_dependency", p, "Consumer cannot depend on a future version.")
            cid = consumer.get("consumer_id")
            if isinstance(cid, str):
                if cid in seen:
                    self.add("duplicate_consumer_id", p, "Consumer IDs must be unique.")
                seen.add(cid)
            for reference in self.sequence(consumer.get("read_paths"), at(p, "read_paths"), nonempty=True):
                if not isinstance(reference, str):
                    continue
                if not any(reference == prefix or reference.startswith(prefix + "/")
                           for prefix in ("/content", "/sources", "/issues")):
                    self.add("invalid_dependency_path", at(p, "read_paths"),
                             "Register exact content, source or issue dependencies, not display/version fields.")
                    continue
                try:
                    pointer_value(work, reference)
                except (KeyError, IndexError, TypeError):
                    # Historical consumers can legitimately refer to deleted fields.
                    if consumer.get("source_work_version") == work.get("version"):
                        self.add("unresolved_dependency_path", at(p, "read_paths"), "Dependency path does not resolve at its stated version.")

    def work(self, value, path="", cross=True):
        fields = ("work_id", "version", "owner_module", "status", "display", "sources", "content",
                  "issues", "accepted_proposals", "consumers")
        if not self.header(value, path, "WorkBrief", fields):
            return
        self.ident(value.get("work_id"), at(path, "work_id"))
        self.integer(value.get("version"), at(path, "version"))
        self.enum(value.get("owner_module"), at(path, "owner_module"), ("M1",))
        self.enum(value.get("status"), at(path, "status"), ("draft",))
        display = value.get("display")
        if self.obj(display, at(path, "display"), (), ("title",)):
            if "title" in display:
                self.text(display["title"], at(at(path, "display"), "title"))
        sources = self.sources(value.get("sources"), at(path, "sources"), nonempty=False)
        self.content(value.get("content"), at(path, "content"), sources)
        self.issues(value.get("issues"), at(path, "issues"), sources)
        self.history(value.get("accepted_proposals"), at(path, "accepted_proposals"), sources, value.get("version"))
        self.consumers(value.get("consumers"), at(path, "consumers"), value)
        if cross:
            self.cross_checks(value.get("content"), at(path, "content"), partial=False)

    def cross_checks(self, content, path, partial=False):
        if not isinstance(content, dict):
            return
        if not partial:
            missing = [field for field in FIELDS if field not in content]
            if missing:
                self.add("partial_workbrief", path, "This is a partial draft; missing M1 partitions: " + ", ".join(missing),
                         "M1", "unverified", False)
        paragraphs = content.get("paragraphs")
        keeps = content.get("must_keep_events")
        if not isinstance(paragraphs, dict):
            if any(content.get(name) for name in ("must_keep_events", "emotion_energy", "motifs")):
                self.add("paragraph_context_unverified", path, "Paragraph references need an M1.2 projection at acceptance.",
                         "M1.2", "unverified", False)
            return
        orders = {}
        kept = set()
        graph = {}
        for pid, paragraph in paragraphs.items():
            if not isinstance(paragraph, dict):
                continue
            pp = at(at(path, "paragraphs"), pid)
            order = paragraph.get("order")
            if type(order) is int:
                if order in orders:
                    self.add("duplicate_paragraph_order", at(pp, "order"), "Paragraph orders must be unique.", "M1.2")
                orders[order] = pid
            event_ids = paragraph.get("must_keep_event_ids", [])
            if isinstance(event_ids, list):
                for event_id in event_ids:
                    if not isinstance(event_id, str):
                        continue
                    kept.add(event_id)
                    if isinstance(keeps, dict) and event_id not in keeps:
                        self.add("unknown_keep_event", at(pp, "must_keep_event_ids"), "Required-event ID does not exist.", "M1.2")
                    elif keeps is None:
                        self.add("keep_context_unverified", at(pp, "must_keep_event_ids"),
                                 "Resolve this reference against M1.1's required events.", "M1.1", "unverified", False)
            predecessors = paragraph.get("information_predecessors", [])
            graph[pid] = []
            if isinstance(predecessors, list):
                for previous in predecessors:
                    if not isinstance(previous, str):
                        continue
                    if previous not in paragraphs:
                        self.add("unknown_information_predecessor", at(pp, "information_predecessors"),
                                 "Information predecessor does not exist in this paragraph projection.", "M1.2")
                    else:
                        graph[pid].append(previous)
                        before = paragraphs[previous].get("order") if isinstance(paragraphs[previous], dict) else None
                        if type(order) is int and type(before) is int and before >= order:
                            self.add("information_order_conflict", at(pp, "information_predecessors"),
                                     "An explicitly declared predecessor must occur earlier in the information order.", "M1.2")
        # Iterative topological elimination also catches cycles without recursion limits.
        pending = {key: set(values) for key, values in graph.items()}
        while pending:
            ready = {key for key, values in pending.items() if not values}
            if not ready:
                self.add("information_dependency_cycle", at(path, "paragraphs"),
                         "Information dependencies contain a cycle: " + ", ".join(sorted(pending)), "M1.2")
                break
            pending = {key: values - ready for key, values in pending.items() if key not in ready}
        if isinstance(keeps, dict):
            for event_id in keeps.keys() - kept:
                self.add("uncovered_keep_event", at(at(path, "must_keep_events"), event_id),
                         "A required event has no declared paragraph coverage.", "M1.2")
        elif not partial:
            self.add("keep_inventory_unverified", path, "Required-event inventory is absent, so completeness is unverified.",
                     "M1.1", "unverified", False)
        emotion = content.get("emotion_energy", {})
        if isinstance(emotion, dict):
            for pid in emotion:
                if pid not in paragraphs:
                    self.add("unknown_emotion_paragraph", at(at(path, "emotion_energy"), pid), "Unknown paragraph ID.", "M1.3")
        motifs = content.get("motifs", {})
        if isinstance(motifs, dict):
            for mid, motif in motifs.items():
                if isinstance(motif, dict) and isinstance(motif.get("paragraph_ids"), list):
                    for pid in motif["paragraph_ids"]:
                        if isinstance(pid, str) and pid not in paragraphs:
                            self.add("unknown_motif_paragraph", at(at(path, "motifs"), mid), "Unknown paragraph ID.", "M1.3")
        constraints = content.get("constraints", {})
        if isinstance(constraints, dict):
            for cid, constraint in constraints.items():
                scope = constraint.get("scope", {}) if isinstance(constraint, dict) else {}
                for pid in scope.get("paragraph_ids", []) if isinstance(scope, dict) and isinstance(scope.get("paragraph_ids", []), list) else []:
                    if isinstance(pid, str) and pid not in paragraphs:
                        self.add("unknown_constraint_paragraph", at(at(path, "constraints"), cid), "Unknown paragraph ID.", "M1.1")

    def artifact(self, value, path=""):
        if not isinstance(value, dict):
            self.add("invalid_type", path, "Expected a contract object.")
            return
        kind = value.get("kind")
        handler = {"M1Request": self.request, "M1Proposal": self.proposal,
                   "M1ProposalBatch": self.batch, "WorkBrief": self.work}.get(kind) if isinstance(kind, str) else None
        if handler is None:
            self.add("unknown_artifact_kind", at(path, "kind"), "Supported kinds: M1Request, M1Proposal, M1ProposalBatch, WorkBrief.")
        else:
            handler(value, path)

    def failed(self):
        return any(d["status"] in ("fail", "stale", "conflict") for d in self.diagnostics)

    def blocked(self):
        return any(d["blocking"] for d in self.diagnostics)


def declared_issues(artifact):
    if not isinstance(artifact, dict):
        return []
    if artifact.get("kind") == "M1ProposalBatch":
        proposals = artifact.get("proposals")
        return [issue for proposal in proposals if isinstance(proposal, dict)
                for issue in declared_issues(proposal)] if isinstance(proposals, list) else []
    value = artifact.get("issues")
    return value if isinstance(value, list) else []


def issue_diagnostics(validator, artifact):
    for issue in declared_issues(artifact):
        if isinstance(issue, dict):
            validator.add("declared_issue", issue.get("field", "/issues"), issue.get("message", "Unresolved issue."),
                          issue.get("owner_module", "M1"), issue.get("status", "unverified"),
                          issue.get("blocking", True))


def envelope(command, validator, outcome):
    deterministic = "fail" if validator.failed() else ("unverified" if validator.diagnostics else "pass")
    return {
        "kind": "M1ToolResult", "contract_version": CONTRACT_VERSION,
        "package_version": PACKAGE_VERSION, "command": command,
        "execution_status": "completed", "outcome": outcome,
        "audit": {"structure": "fail" if any(d["code"] in STRUCTURAL_CODES and d["status"] == "fail" for d in validator.diagnostics) else "pass",
                  "deterministic": deterministic, "semantic": "unverified",
                  "media": "unverified", "overall": "fail" if validator.failed() else "unverified"},
        "diagnostics": validator.diagnostics,
        "limitations": ["No natural-language meaning, H3 execution, media, or undeclared dependency was verified."],
    }


def route(request):
    validation = Validation()
    validation.request(request)
    result = envelope("route", validation, "needs_input" if validation.blocked() else "routed")
    if validation.failed():
        result["outcome"] = "rejected"
        return result, 1
    if isinstance(request, dict) and request.get("target") in MODULES:
        target = request["target"]
        registry = json.loads((ROOT / "references" / "module-registry.json").read_text(encoding="utf-8"))
        if not isinstance(registry, dict) or registry.get("contract_version") != CONTRACT_VERSION:
            raise ValueError("Bundled module registry is missing or incompatible.")
        nodes = registry.get("nodes")
        node = nodes.get(target) if isinstance(nodes, dict) else None
        if not isinstance(node, dict) or any(key not in node for key in ("route_id", "resources", "return_to")):
            raise ValueError("Bundled route definition is incomplete: " + target)
        selected = request.get("requested_fields", list(fields_for(target)))
        result["dispatch"] = {
            "route_id": node["route_id"], "route_version": CONTRACT_VERSION,
            "request_id": request.get("request_id"), "target": target,
            "work_id": request.get("work_id"), "base_version": request.get("base_version"),
            "input_projection": copy.deepcopy(request.get("inputs", {})),
            "requested_fields": selected, "resources": node["resources"],
            "return_to": node["return_to"], "semantic_execution": "not_started",
            "eligible_children": sorted({OWNER[f] for f in selected if f in OWNER}) if isinstance(selected, list) and target == "M1" else [],
            "child_inputs_verified": False,
        }
        if target == "M1":
            result["limitations"].append("M1 entry inputs do not establish the M1.2 or M1.3 projected inputs; the agent must prepare them explicitly.")
    return result, 1 if validation.blocked() else 0


def match_request(validation, artifact, request):
    validation.request(request, "/request")
    if validation.failed() or not isinstance(request, dict) or not isinstance(artifact, dict):
        return
    target = request.get("target")
    expected = request.get("requested_fields", list(fields_for(target)) if isinstance(target, str) else [])
    proposals = artifact.get("proposals", []) if artifact.get("kind") == "M1ProposalBatch" else [artifact]
    if not isinstance(proposals, list):
        return
    written = set()
    for index, item in enumerate(proposals):
        if not isinstance(item, dict):
            continue
        p = "/artifact/" + str(index)
        for source_id, source in item.get("sources", {}).items():
            request_source = request["sources"].get(source_id)
            if request_source is not None and request_source != source:
                validation.add("source_identity_conflict", at(at(p, "sources"), source_id),
                               "A request source ID cannot be rebound to different content, kind, locator or version.", "M1", "conflict")
        if item.get("work_id") != request.get("work_id"):
            validation.add("work_id_mismatch", p, "Output and request work IDs differ.")
        if item.get("kind") == "WorkBrief":
            if item.get("version") != request.get("base_version", -1) + 1:
                validation.add("request_version_mismatch", p, "Accepted output must be based on the request version plus one.")
            if target != "M1":
                validation.add("wrong_result_kind", p, "A child returns a proposal; only M1 publishes WorkBrief.")
            changes = item.get("content", {})
        else:
            if item.get("source_request_id") != request.get("request_id"):
                validation.add("request_id_mismatch", p, "Proposal was produced for another request.")
            if item.get("base_version") != request.get("base_version"):
                validation.add("request_version_mismatch", p, "Proposal and request base versions differ.")
            if target != "M1" and item.get("module_id") != target:
                validation.add("wrong_result_module", p, "The response module does not match the requested node.")
            changes = item.get("changes", {})
        if isinstance(changes, dict):
            written.update(changes)
            intent = changes.get("intent")
            requested_type = request.get("inputs", {}).get("work_type")
            if isinstance(intent, dict) and isinstance(requested_type, str):
                actual_type = intent.get("work_type")
                if isinstance(actual_type, str) and actual_type != requested_type:
                    validation.add("work_type_mismatch", at(at(p, "intent"), "work_type"),
                                   "The declared work type differs from the request; do not silently switch strategy.", "M1.1")
                elif is_unknown(actual_type):
                    validation.add("known_work_type_lost", at(at(p, "intent"), "work_type"),
                                   "The request provides a known work type; the response must preserve or explicitly resolve it.",
                                   "M1.1", "unverified")
    if isinstance(expected, list):
        for field in expected:
            if isinstance(field, str) and field not in written:
                validation.add("missing_requested_output", "/artifact", "Requested partition missing: " + field,
                               OWNER.get(field, "M1"), "unverified")
        if artifact.get("kind") != "WorkBrief":
            for field in written - set(f for f in expected if isinstance(f, str)):
                validation.add("unrequested_write", "/artifact", "Proposal writes a partition outside this request: " + field)


def check(artifact, request=None):
    validation = Validation()
    validation.artifact(artifact)
    if request is not None:
        match_request(validation, artifact, request)
    issue_diagnostics(validation, artifact)
    incomplete = validation.blocked() or any(d["code"] == "partial_workbrief" for d in validation.diagnostics)
    outcome = "invalid" if validation.failed() else ("incomplete" if incomplete else "structurally_valid")
    result = envelope("check", validation, outcome)
    result["checked_kind"] = artifact.get("kind") if isinstance(artifact, dict) else None
    result["request_match_checked"] = request is not None
    return result, 1 if validation.failed() or validation.blocked() else 0


def accept(current, proposed):
    validation = Validation()
    validation.work(current, "/current", cross=False)
    validation.artifact(proposed, "/proposal")
    if not isinstance(proposed, dict) or proposed.get("kind") not in ("M1Proposal", "M1ProposalBatch"):
        validation.add("wrong_result_kind", "/proposal", "Accept expects M1Proposal or M1ProposalBatch.")
    if validation.failed():
        return envelope("accept", validation, "rejected"), 1
    # Cross-projection unknowns are allowed in an explicitly draft WorkBrief.
    proposals = proposed["proposals"] if proposed["kind"] == "M1ProposalBatch" else [proposed]
    seen = {item["proposal_id"] for item in current["accepted_proposals"]}
    fields = set()
    issue_ids = {issue["id"] for issue in current["issues"]}
    candidate = copy.deepcopy(current)
    old_issues = {issue["id"]: issue for issue in current["issues"]}
    all_resolutions = set()
    accepted = []
    for index, proposal in enumerate(proposals):
        p = f"/proposal/proposals/{index}"
        module = proposal["module_id"]
        if proposal["work_id"] != current["work_id"]:
            validation.add("work_id_mismatch", p, "Proposal targets a different work.", module)
        if proposal["base_version"] != current["version"]:
            validation.add("stale_base_version", p, "Rebase against the current WorkBrief; do not silently replace the base.", module, "stale")
        if proposal["proposal_id"] in seen:
            validation.add("duplicate_proposal_id", p, "Already accepted or duplicated in this batch.", module)
        seen.add(proposal["proposal_id"])
        for field, new_value in proposal["changes"].items():
            if field in fields:
                validation.add("competing_partition_write", at(p, field), "Multiple proposals write the same partition; parent must return the conflict.", "M1", "conflict")
            fields.add(field)
            candidate["content"][field] = copy.deepcopy(new_value)
        for source_id, source in proposal["sources"].items():
            if source_id in candidate["sources"] and candidate["sources"][source_id] != source:
                validation.add("source_identity_conflict", at(p, source_id), "A source ID is immutable; use a new ID for a changed source/version.", module, "conflict")
            else:
                candidate["sources"][source_id] = copy.deepcopy(source)
        for issue in proposal["issues"]:
            if issue["id"] in issue_ids:
                validation.add("duplicate_issue_id", p, "Do not overwrite an existing issue; submit an explicit authorized resolution.", module)
            issue_ids.add(issue["id"])
            candidate["issues"].append(copy.deepcopy(issue))
        resolved = []
        for resolution in proposal["resolutions"]:
            issue_id = resolution["issue_id"]
            issue = old_issues.get(issue_id)
            if issue is None:
                validation.add("unknown_resolution", p, "Resolution must reference an issue in the current WorkBrief.", module)
            elif issue["owner_module"] != module:
                validation.add("resolution_out_of_scope", p,
                               "This child cannot resolve a parent, sibling, user or external module's issue.", issue["owner_module"])
            elif issue_id in all_resolutions:
                validation.add("competing_resolution", p, "An issue cannot be resolved twice in the same batch.", "M1", "conflict")
            else:
                all_resolutions.add(issue_id)
                resolved.append({"issue": copy.deepcopy(issue), "reason": resolution["reason"],
                                 "source_refs": copy.deepcopy(resolution["source_refs"])})
        accepted.append({
            "proposal_id": proposal["proposal_id"], "module_id": module,
            "source_request_id": proposal["source_request_id"],
            "from_version": current["version"], "to_version": current["version"] + 1,
            "changed_fields": sorted(proposal["changes"]), "source_ids": sorted(proposal["sources"]),
            "resolved_issues": resolved,
        })
    candidate["issues"] = [issue for issue in candidate["issues"] if issue["id"] not in all_resolutions]
    candidate["version"] = current["version"] + 1
    candidate["status"] = "draft"
    candidate["accepted_proposals"].extend(accepted)
    merged_validation = Validation()
    merged_validation.work(candidate, "/candidate")
    # Recheck the combined candidate: unresolved child-only context is not a failure.
    validation.diagnostics = [d for d in validation.diagnostics if d["status"] != "unverified"]
    validation.diagnostics.extend(merged_validation.diagnostics)
    issue_diagnostics(validation, candidate)
    if validation.failed() or validation.blocked():
        result = envelope("accept", validation, "rejected")
        result["rejected_proposal_ids"] = [p["proposal_id"] for p in proposals]
        result["unresolved_issues"] = copy.deepcopy(candidate["issues"])
        return result, 1
    result = envelope("accept", validation, "accepted")
    result["work_brief"] = candidate
    result["authority"] = "M1 accepted declared child proposals; no prose was rewritten or semantically certified."
    return result, 0


def diff_paths(before, after, path=""):
    if type(before) is not type(after):
        return [path]
    if isinstance(before, dict):
        paths = []
        for key in sorted(before.keys() | after.keys()):
            p = at(path, key)
            paths.extend([p] if key not in before or key not in after else diff_paths(before[key], after[key], p))
        return paths
    if isinstance(before, list):
        if len(before) != len(after):
            return [path]
        return [changed for i, (left, right) in enumerate(zip(before, after))
                for changed in diff_paths(left, right, at(path, i))]
    return [] if before == after else [path]


def overlaps(left, right):
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def impact(previous, current):
    validation = Validation()
    validation.work(previous, "/previous")
    validation.work(current, "/current")
    if isinstance(previous, dict) and isinstance(current, dict):
        if previous.get("work_id") != current.get("work_id"):
            validation.add("work_id_mismatch", "/current/work_id", "Compare snapshots of the same WorkBrief.")
        pv, cv = previous.get("version"), current.get("version")
        if type(pv) is int and type(cv) is int and cv <= pv:
            validation.add("non_increasing_version", "/current/version", "Current version must be newer than previous.")
    if validation.failed():
        return envelope("impact", validation, "rejected"), 1
    all_changes = diff_paths(previous, current)
    changed = [p for p in all_changes if any(overlaps(p, prefix) for prefix in ("/content", "/sources", "/issues"))]
    affected, unaffected, uncertain = [], [], []
    for consumer in previous["consumers"]:
        watched = consumer["read_paths"]
        hits = [p for p in changed if any(overlaps(p, watch) for watch in watched)]
        entry = {"consumer_id": consumer["consumer_id"], "module_id": consumer["module_id"],
                 "consumer_version": consumer["version"], "source_work_version": consumer["source_work_version"],
                 "changed_dependencies": hits}
        if hits:
            entry["status"] = "stale"
            entry["repair_target"] = consumer["module_id"]
            entry["recheck"] = "Review only the declared changed dependencies against the new WorkBrief."
            affected.append(entry)
        elif consumer["source_work_version"] != previous["version"]:
            entry["status"] = "unverified"
            entry["reason"] = "Consumer predates the comparison baseline; its original input snapshot is unavailable."
            uncertain.append(entry)
        else:
            entry["status"] = "unaffected_in_this_comparison"
            unaffected.append(entry)
    result = envelope("impact", validation, "impact_reported")
    result.update({"work_id": current["work_id"], "from_version": previous["version"],
                   "to_version": current["version"], "changed_dependency_paths": changed,
                   "ignored_metadata_paths": [p for p in all_changes if p not in changed],
                   "stale_consumers": affected, "unaffected_consumers": unaffected,
                   "preexisting_unverified_consumers": uncertain,
                   "unregistered_consumer_coverage": "unknown", "transitive_discovery": "not_implemented",
                   "scope": "Only consumers explicitly registered in the previous snapshot; declarations do not prove those modules ran."})
    return result, 0


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def load_json(path):
    def invalid_constant(value):
        raise ValueError("Non-finite JSON constant is not allowed: " + value)
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=reject_duplicate_keys, parse_constant=invalid_constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("route", help="Check the minimum input and return a route, without semantic execution.")
    p.add_argument("request")
    p = commands.add_parser("check", help="Validate declared structure and deterministic references; semantic review remains unverified.")
    p.add_argument("artifact")
    p.add_argument("--request")
    p = commands.add_parser("accept", help="Accept owned, version-compatible child proposals into a new draft WorkBrief.")
    p.add_argument("current")
    p.add_argument("proposal")
    p = commands.add_parser("impact", help="Report only explicitly registered consumers affected by this snapshot change.")
    p.add_argument("previous")
    p.add_argument("current")
    args = parser.parse_args(argv)
    started = datetime.now(timezone.utc).isoformat()
    try:
        if args.command == "route":
            result, code = route(load_json(args.request))
        elif args.command == "check":
            result, code = check(load_json(args.artifact), load_json(args.request) if args.request else None)
        elif args.command == "accept":
            result, code = accept(load_json(args.current), load_json(args.proposal))
        else:
            result, code = impact(load_json(args.previous), load_json(args.current))
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        validation = Validation()
        validation.add("input_or_resource_error", "", str(error), "user")
        result, code = envelope(args.command, validation, "rejected"), 2
    result["execution"] = {"invocation_id": "m1tool-" + uuid.uuid4().hex,
                           "started_at": started, "finished_at": datetime.now(timezone.utc).isoformat(),
                           "operation_effect": "read_inputs_and_emit_new_result", "input_files_modified": False}
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
