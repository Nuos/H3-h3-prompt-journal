#!/usr/bin/env python3
"""Reproduce M12 release identity, package closure and recorded validation checks.

This verifier does not infer H3 quality or the truth of external observation logs.
Run at the M12 release snapshot; later authorized README edits have a new scope.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
RELEASE = ROOT / "docs/h3skill"
PACKAGE = RELEASE / "h3-audit-repair"
VALIDATION = RELEASE / "validation/m12"


def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"Duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    def nonfinite(value):
        raise ValueError(f"Nonfinite JSON in {path}: {value}")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=nonfinite)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main():
    checks = []

    def record(name, errors, **details):
        checks.append({"check": name, "status": "fail" if errors else "pass",
                       "errors": errors, **details})

    manifest = load(RELEASE / "release-manifest-m12.json")
    errors, paths = [], set()
    for row in manifest["files"]:
        rel = row["path"]
        if Path(rel).is_absolute() or ".." in Path(rel).parts or rel in paths:
            errors.append("Unsafe or duplicate manifest path: " + rel)
            continue
        path = ROOT / rel
        if not path.is_file() or path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
            errors.append("Release file drift: " + rel)
        paths.add(rel)
    record("release_file_hashes", errors, file_count=len(paths))

    roots = {p.name for p in PACKAGE.iterdir()}
    errors = []
    if roots != {"SKILL.md", "scripts", "references", "assets", "agents"}:
        errors.append("Unexpected package roots: " + repr(sorted(roots)))
    for path in PACKAGE.rglob("*"):
        if path.is_symlink() or path.name == "__pycache__" or path.suffix == ".pyc":
            errors.append("Symlink or cache: " + str(path.relative_to(PACKAGE)))
        if path.is_file() and str(path.relative_to(ROOT)) not in paths:
            errors.append("Unlisted package file: " + str(path.relative_to(ROOT)))
    record("package_layout", errors, roots=sorted(roots),
           note="Only SKILL.md is universally required; resource directories are this package's choices.")

    text = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    fields, errors = {}, []
    if not match:
        errors.append("Missing YAML frontmatter")
    else:
        for line in match[1].splitlines():
            key, value = line.split(": ", 1)
            if key in fields:
                errors.append("Duplicate frontmatter: " + key)
            fields[key] = json.loads(value) if value.startswith('"') else value
    name, description = fields.get("name", ""), fields.get("description", "")
    if set(fields) != {"name", "description"}:
        errors.append("This entry uses name and description only")
    if name != PACKAGE.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("Invalid skill name or directory mismatch")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        errors.append("Description must contain 1–1024 characters")
    if len(text.splitlines()) >= 500 or "[TODO" in text:
        errors.append("Oversized entry or unfinished initialization template")
    record("frontmatter_and_entry", errors, lines=len(text.splitlines()),
           description_characters=len(description))

    errors, entry_refs, link_count = [], set(), 0
    for path in [PACKAGE / "SKILL.md", *sorted((PACKAGE / "references").glob("*.md"))]:
        for ref in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+://|#", ref):
                continue
            link_count += 1
            if not (path.parent / ref.split("#")[0]).resolve().exists():
                errors.append(f"Broken resource link in {path.name}: {ref}")
            if path.name == "SKILL.md":
                entry_refs.add(ref)
    for path in (PACKAGE / "references").iterdir():
        if path.is_file() and "references/" + path.name not in entry_refs:
            errors.append("Reference lacks direct entry route: " + path.name)
    record("progressive_resource_routes", errors, link_count=link_count)

    errors, json_count, py_count = [], 0, 0
    for path in PACKAGE.rglob("*"):
        try:
            if path.suffix == ".json":
                load(path)
                json_count += 1
            elif path.suffix == ".py":
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                py_count += 1
        except (ValueError, SyntaxError) as exc:
            errors.append(str(exc))
    record("json_and_python_syntax", errors, json_files=json_count, python_files=py_count)

    registry = load(PACKAGE / "references/module-registry.json")
    schema = load(PACKAGE / "references/contracts.json")
    modules = {row["module_id"]: row for row in registry["modules"]}
    errors = []
    if len(modules) != len(registry["modules"]) or set(modules) != {"M12", "M12.1", "M12.2", "M12.3", "M12.4"}:
        errors.append("Module tree must contain the parent and all four public responsibilities")
    for mid, row in modules.items():
        for key in ("responsibility", "input_contract", "output_contract", "readonly", "write_permissions",
                    "forbidden_writes", "dependencies", "resources", "route", "consumers", "invalidation"):
            if key not in row:
                errors.append(f"Missing node contract {mid}.{key}")
        if mid != "M12" and (row.get("parent_id") != "M12" or row.get("route", {}).get("explicit_target") != mid):
            errors.append("Child parent or route mismatch: " + mid)
        for resource in row.get("resources", []):
            if not (PACKAGE / resource).is_file():
                errors.append("Missing declared resource: " + resource)
    record("module_tree_and_routes", errors, module_count=len(modules))

    refs, errors = [], []

    def visit(value):
        if isinstance(value, dict):
            if "$ref" in value:
                refs.append(value["$ref"])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(schema)
    for ref in refs:
        if not isinstance(ref, str) or not ref.startswith("#/"):
            errors.append("Non-local schema reference: " + str(ref))
            continue
        cursor = schema
        try:
            for part in ref[2:].split("/"):
                cursor = cursor[part.replace("~1", "/").replace("~0", "~")]
        except (KeyError, TypeError):
            errors.append("Unresolved schema reference: " + ref)
    record("schema_reference_closure", errors, definitions=len(schema.get("$defs", {})), local_references=len(refs),
           note="Syntax/reference closure; runtime semantic conditions are tested by the contract implementation.")

    index = load(PACKAGE / "references/case-index.json")
    errors, lines = [], 0
    for row in index["files"]:
        rel = row["path"]
        if not rel.startswith("case-studies/") or ".." in Path(rel).parts:
            errors.append("Source outside case boundary: " + rel)
            continue
        path = ROOT / rel
        data = path.read_bytes()
        count = len(data.decode("utf-8").splitlines())
        if (sha(path) != row["sha256"] or len(data) != row["byte_count"]
                or count != row["line_count"] or blob(data) != row["git_blob_sha1"]):
            errors.append("Case identity drift: " + rel)
        if row["read_status"] == "full_text":
            lines += count
            if row["line_ranges"] != [{"start": 1, "end": count}]:
                errors.append("Full-text reading range mismatch: " + rel)
        elif row["read_status"] != "structured_projection":
            errors.append("Unknown reading scope: " + rel)
    indexed_paths = {row["path"] for row in index["files"]}
    for case in index["cases"]:
        tracked = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", index["source_commit"], "--", case["path"]],
            cwd=ROOT, text=True).splitlines()
        texts = {p for p in tracked if Path(p).suffix.lower() in index["index_extensions"]}
        media = set(tracked) - texts
        if texts != set(case["text_files"]) or not texts <= indexed_paths:
            errors.append("Selected case text inventory incomplete: " + case["path"])
        if media != set(case["excluded_media_files"]):
            errors.append("Excluded media inventory differs from fixed Git tree: " + case["path"])
    if lines != index["coverage"]["full_text_read_lines"]:
        errors.append("Full-text reading total differs from file records")
    record("case_source_identity", errors, files=len(index["files"]), full_text_lines=lines,
           note="Source identity does not establish the truth of author-reported media outcomes.")

    baseline = load(VALIDATION / "protected-baseline.json")
    errors = []
    for row in baseline["files"]:
        path = ROOT / row["path"]
        if not path.is_file() or sha(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
            errors.append("Protected file changed: " + row["path"])
    record("protected_existing_text", errors, files=len(baseline["files"]), base_commit=baseline["base_commit"])

    changed = set(subprocess.check_output(
        ["git", "diff", "--name-only", baseline["base_commit"], "--"],
        cwd=ROOT, text=True).splitlines())
    added = set(subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=ROOT, text=True).splitlines())
    allowed = paths | {"docs/h3skill/release-manifest-m12.json",
                       "docs/h3skill/validation/m12/release-verification.json"}
    errors = ["Change outside this release: " + p for p in sorted((changed | added) - allowed)]
    record("git_change_scope", errors, changed_or_added_paths=len(changed | added),
           note="Checks all tracked paths, including non-materialized media; only the release files and shared README may differ.")

    frozen = load(ROOT / "docs/skillplan/baseline-lock.json")
    errors = []
    for row in frozen["files"]:
        if sha(ROOT / row["path"]) != row["sha256"]:
            errors.append("Frozen design changed: " + row["path"])
    record("frozen_plan_identity", errors, files=len(frozen["files"]), baseline=frozen["baseline_id"])

    source = load(PACKAGE / "references/h3-protocol-source.json")
    errors, count = [], 0
    for row in source["sources"]:
        name = row.get("offline_snapshot")
        if name not in {"h3-base-official.txt", "h3-ref-official.txt"}:
            continue
        count += 1
        path = PACKAGE / "references" / name
        if sha(path) != row["sha256"] or blob(path.read_bytes()) != row["git_blob_sha"]:
            errors.append("Official protocol drift: " + name)
    if count != 2:
        errors.append("Both official protocol snapshots must be pinned")
    record("official_protocol_identity", errors, snapshots=count, commit=source["authority"]["commit"])

    standards = load(VALIDATION / "standards-verification.json")
    errors = []
    for row in standards["existing_standard_snapshots"]:
        path = RELEASE / "_standards" / row["path"]
        if (sha(path) != row["sha256"] or blob(path.read_bytes()) != row["git_blob_sha1"]
                or path.stat().st_size != row["bytes"] or row["local_snapshot_integrity"] != "pass"):
            errors.append("Fixed standard snapshot drift: " + row["path"])
    record("format_standard_snapshots", errors, files=len(standards["existing_standard_snapshots"]),
           note="Existing snapshots checked locally; fresh Anthropic creator retrieval recorded separately.")

    validation = load(VALIDATION / "validation-results.json")
    actual = {str(p.relative_to(PACKAGE)): sha(p) for p in PACKAGE.rglob("*") if p.is_file()}
    errors = ["Validation not passed: " + row["check"] for row in validation["checks"] if row["status"] != "pass"]
    if actual != validation["package_snapshot_sha256"]:
        errors.append("Package changed after the recorded verification")
    behavior = load(VALIDATION / "behavior-tests.json")
    if (behavior["exit_code"] != 0 or behavior["tests_run"] != behavior["passed"] + behavior["skipped"]
            or behavior["contract_script_sha256"] != actual["scripts/m12_contract.py"]
            or behavior["test_file_sha256"] != sha(RELEASE / "tests/test_m12_contract.py")):
        errors.append("Behavior execution record does not match the released program/tests")
    isolation = load(VALIDATION / "isolation-verification.json")
    if (isolation["status"] != "pass" or isolation["package_snapshot_sha256"] != actual
            or any(c["status"] != "pass" for c in isolation["checks"])):
        errors.append("Isolated calls do not match the released package")
    forward = load(VALIDATION / "forward-use/review.json")
    if (forward["final_package_sha256"] != actual
            or not forward["source_task_and_initial_output_preserved"]):
        errors.append("Forward review does not match the released package or preserved inputs")
    original_snapshot = load(VALIDATION / "forward-use/before-snapshot.json")
    for name, expected in original_snapshot.items():
        if name.startswith("h3-audit-repair/"):
            rel = name.removeprefix("h3-audit-repair/")
            original = (VALIDATION / "forward-use/initial-package-delta/evidence-and-gates.md"
                        if rel == "references/evidence-and-gates.md" else PACKAGE / rel)
        else:
            original = VALIDATION / "forward-use" / name
        if not original.is_file() or sha(original) != expected:
            errors.append("Initial forward input/package identity drift: " + name)
    for row in validation["integrity_files"]:
        if Path(row["path"]).is_absolute() or ".." in Path(row["path"]).parts:
            errors.append("Unsafe validation artifact path: " + row["path"])
            continue
        path = VALIDATION / row["path"]
        if not path.is_file() or sha(path) != row["sha256"]:
            errors.append("Validation artifact drift: " + row["path"])
    record("recorded_validation_and_package", errors, checks=len(validation["checks"]),
           note="Format, contract, portability and text-use records; no H3/media certification.")

    result = {"kind": "M12ReleaseVerification", "status": "pass" if all(r["status"] == "pass" for r in checks) else "fail",
              "checks": checks, "h3_inference": "not_run", "real_media_acceptance": "not_run"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps({"kind": "M12ReleaseVerification", "status": "fail", "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
