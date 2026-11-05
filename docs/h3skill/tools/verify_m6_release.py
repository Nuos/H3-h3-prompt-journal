#!/usr/bin/env python3
"""Verify M6 release files and preserved sources; no network or media processing.

Run from a complete repository checkout. In a partial materialization, pass an
actual GitHub connector recursive-tree response with --tree-snapshot to verify
unmaterialized protected blobs by immutable Git object identity. A supplied
snapshot is evidence of that tree only, not of a later moving branch.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RELEASE = ROOT / "docs/h3skill"
PACKAGE = RELEASE / "h3-sound-music-dialogue"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def read_json(path: Path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate key {key!r}: {path}")
            result[key] = value
        return result

    def nonfinite(value):
        raise ValueError(f"nonfinite number {value}: {path}")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=nonfinite)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tree-snapshot", type=Path,
                        help="Fetched immutable recursive Git tree for absent protected files")
    parser.add_argument("--expected-tree-sha",
                        help="Expected fetched tree SHA; defaults to the recorded input base tree")
    args = parser.parse_args()
    checks = []

    def record(name, errors, **details):
        checks.append({"check": name, "status": "fail" if errors else "pass",
                       "errors": errors, **details})

    manifest = read_json(RELEASE / "release-manifest-m6.json")
    files = manifest["files"]
    expected = {item["path"]: item for item in files}
    errors = []
    if len(expected) != len(files):
        errors.append("duplicate manifest paths")
    for item in files:
        path = ROOT / item["path"]
        if not path.is_relative_to(ROOT) or ".." in Path(item["path"]).parts:
            errors.append(f"unsafe manifest path: {item['path']}")
        elif not path.is_file():
            errors.append(f"missing: {item['path']}")
        elif sha256(path) != item["sha256"] or path.stat().st_size != item["bytes"]:
            errors.append(f"changed: {item['path']}")
    record("release_manifest_hashes", errors, count=len(files),
           excludes="Manifest itself and the derived release-check output are excluded to avoid self-hash cycles.")

    allowed_roots = {"SKILL.md", "scripts", "references", "assets"}
    children = {p.name for p in PACKAGE.iterdir()}
    errors = [] if children == allowed_roots else [f"unexpected/missing package roots: {sorted(children ^ allowed_roots)}"]
    errors.extend(f"symlink in standalone package: {p.relative_to(PACKAGE)}"
                  for p in PACKAGE.rglob("*") if p.is_symlink())
    record("package_layout", errors, roots=sorted(children),
           scope="Chosen distribution layout; optional host metadata is not an official mandatory file.")

    skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
    fields = {}
    errors = []
    if not match:
        errors.append("missing YAML frontmatter")
    else:
        for line in match.group(1).splitlines():
            if ": " not in line:
                errors.append(f"unexpected frontmatter syntax: {line}")
                continue
            key, value = line.split(": ", 1)
            if key in fields:
                errors.append(f"duplicate frontmatter key: {key}")
            fields[key] = json.loads(value) if value.startswith('"') else value
    if set(fields) != {"name", "description"}:
        errors.append("this release declares exactly name and description")
    name = fields.get("name", "")
    desc = fields.get("description", "")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or not 1 <= len(name) <= 64:
        errors.append("invalid/nonempty name requirement")
    if name != PACKAGE.name:
        errors.append("name differs from directory")
    if not isinstance(desc, str) or not 1 <= len(desc.strip()) <= 1024 or "<" in desc or ">" in desc:
        errors.append("description fails formal nonempty/length or official validator compatibility")
    if len(skill.splitlines()) >= 500:
        errors.append("main skill exceeds chosen 500-line guidance")
    record("frontmatter_and_progressive_disclosure", errors,
           lines=len(skill.splitlines()), description_chars=len(desc),
           scope="Supplementary checks; official Anthropic quick_validate is recorded separately.")

    errors = []
    links = 0
    for path in [PACKAGE / "SKILL.md", *sorted((PACKAGE / "references").glob("*.md"))]:
        content = path.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", content):
            if re.match(r"[a-z][a-z0-9+.-]*:", link) or link.startswith("#"):
                continue
            links += 1
            target = (path.parent / link.split("#", 1)[0]).resolve()
            if not target.is_relative_to(PACKAGE.resolve()):
                errors.append(f"package-external resource: {path.name} -> {link}")
            elif not target.exists():
                errors.append(f"missing resource: {path.name} -> {link}")
    record("relative_resource_links", errors, count=links)

    errors = []
    references = sorted(p for p in (PACKAGE / "references").iterdir() if p.is_file())
    for path in references:
        if f"references/{path.name}" not in skill:
            errors.append(f"resource not directly routed by SKILL.md: {path.name}")
    record("single_hop_reference_routes", errors, count=len(references))

    package_files = [p for p in PACKAGE.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    errors = [f"unmanifested runtime file: {p.relative_to(ROOT)}" for p in package_files
              if p.relative_to(ROOT).as_posix() not in expected]
    record("complete_runtime_manifest", errors, count=len(package_files))

    errors = []
    imports = set()
    for path in (PACKAGE / "scripts").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    errors.append(f"relative runtime import: {path.name}")
                imports.add((node.module or "").split(".")[0])
    allowed_modules = set(getattr(sys, "stdlib_module_names", ())) | {"__future__"}
    if not allowed_modules - {"__future__"}:
        errors.append("release verification requires Python 3.10+ stdlib module registry")
    errors.extend(f"non-stdlib runtime import: {x}" for x in sorted(imports - allowed_modules))
    record("runtime_standard_library", errors, imports=sorted(imports))

    errors = []
    json_files = sorted(PACKAGE.rglob("*.json"))
    for path in json_files:
        try:
            read_json(path)
        except (ValueError, UnicodeError) as exc:
            errors.append(str(exc))
    record("strict_resource_json", errors, count=len(json_files))

    protocol = read_json(PACKAGE / "references/h3-protocol-source.json")
    errors = []
    count = 0
    for source in protocol["sources"]:
        if not source.get("offline_snapshot"):
            continue
        count += 1
        path = PACKAGE / "references" / source["offline_snapshot"]
        if sha256(path) != source["sha256"] or blob_sha(path) != source["git_blob_sha"]:
            errors.append(f"official source drift: {path.name}")
    record("official_protocol_exact_bytes", errors, count=count,
           source_commit=protocol["authority"]["commit"])

    errors = []
    if protocol["protocol"]["base_fields"] != ["integrated_multimodal_description", "overall_soundscape", "non_diegetic_music"]:
        errors.append("unexpected base field set")
    if protocol["protocol"]["reference_fields"] != ["subject_definitions", "summary", "retention_analysis", "detailed_description", "overall_soundscape", "non_diegetic_music"]:
        errors.append("unexpected reference field set")
    if protocol["m6_mapping"]["partitions"] != {"M6.1":"sources", "M6.2":"vocal_events", "M6.3":"music", "M6.4":"effects"}:
        errors.append("M6 mapping partitions drifted")
    record("documented_official_field_mapping", errors,
           scope="Mapping consistency, not execution of an H3 compiler.")

    case_index = read_json(PACKAGE / "references/case-index.json")
    case_files = case_index["files"]
    errors = []
    if len({item["path"] for item in case_files}) != len(case_files):
        errors.append("duplicate case-file entries")
    for item in case_files:
        relative = item["path"]
        path = ROOT / relative
        if not relative.startswith("case-studies/") or ".." in Path(relative).parts:
            errors.append(f"case source outside authorized boundary: {relative}")
            continue
        if not path.is_file():
            errors.append(f"case text not available: {relative}")
            continue
        if sha256(path) != item["sha256"] or blob_sha(path) != item["git_blob_sha1"]:
            errors.append(f"case source hash mismatch: {relative}")
        actual_lines = len(path.read_text(encoding="utf-8").splitlines())
        if item["line_count"] != actual_lines:
            errors.append(f"case source line count mismatch: {relative}")
        if not item.get("read_status") or not item.get("read_scope"):
            errors.append(f"missing honest read scope: {relative}")
        for span in item.get("line_ranges", []):
            if not 1 <= span["start"] <= span["end"] <= actual_lines:
                errors.append(f"case line range out of bounds: {relative}")
    record("case_text_identity_and_read_scope", errors, count=len(case_files),
           scope="Source identities and recorded reading ranges; no claim that keyword indexing equals full reading.")

    lock = read_json(ROOT / "docs/skillplan/baseline-lock.json")
    errors = []
    locked_files = lock["files"]
    if isinstance(locked_files, dict):
        locked_files = [{"path": p, **v} for p, v in locked_files.items()]
    for item in locked_files:
        relative = item.get("path", item.get("file", item.get("relative_path")))
        if not relative:
            errors.append("unrecognized lock entry")
            continue
        path = ROOT / relative if relative.startswith("docs/") else ROOT / "docs/skillplan" / relative
        if not path.is_file() or sha256(path) != item["sha256"]:
            errors.append(f"frozen source changed: {relative}")
    record("frozen_plan_sha256", errors, count=len(locked_files))

    protected = read_json(RELEASE / "validation/m6/protected-baseline.json")
    snapshot = read_json(args.tree_snapshot) if args.tree_snapshot else None
    snapshot_entries = snapshot.get("tree", []) if snapshot else []
    snapshot_map = {item["path"]: item for item in snapshot_entries if item.get("type") == "blob"}
    errors = []
    expected_tree_sha = args.expected_tree_sha or protected["base_tree"]
    if snapshot:
        if snapshot.get("sha") != expected_tree_sha:
            errors.append("supplied tree identity differs from expected immutable tree")
        if snapshot.get("truncated") is not False:
            errors.append("supplied recursive tree must explicitly be untruncated")
        if len(snapshot_map) != sum(item.get("type") == "blob" for item in snapshot_entries):
            errors.append("duplicate paths in supplied tree")
    elif args.expected_tree_sha:
        errors.append("--expected-tree-sha requires --tree-snapshot")
    protected_paths = {item["path"] for item in protected["files"]}
    initial_materialized = set(protected["initially_materialized_paths"])
    prefixes = protected["protected_prefixes"]
    for prefix in prefixes:
        for path in (ROOT / prefix).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                relative = path.relative_to(ROOT).as_posix()
                if relative not in protected_paths:
                    errors.append(f"new file in protected local scope: {relative}")
    if snapshot:
        errors.extend(f"new file in protected tree scope: {path}"
                      for path in snapshot_map
                      if any(path.startswith(prefix) for prefix in prefixes)
                      and path not in protected_paths)
    local_count = tree_count = 0
    for item in protected["files"]:
        path = ROOT / item["path"]
        if path.is_file():
            local_count += 1
            if blob_sha(path) != item["git_blob_sha1"]:
                errors.append(f"protected local drift: {item['path']}")
        elif item["path"] in initial_materialized:
            errors.append(f"previously materialized protected file deleted/non-file: {item['path']}")
        elif not snapshot:
            errors.append(f"protected file not materialized; use complete checkout or --tree-snapshot: {item['path']}")
        if snapshot:
            tree_count += 1
            candidate = snapshot_map.get(item["path"], {})
            if candidate.get("sha") != item["git_blob_sha1"] or candidate.get("mode") != item["mode"]:
                errors.append(f"protected tree drift/missing: {item['path']}")
    record("protected_sources", errors, count=len(protected["files"]),
           local_bytes_checked=local_count, immutable_tree_entries_checked=tree_count,
           snapshot_identity=snapshot.get("sha") if snapshot else None,
           expected_snapshot_identity=expected_tree_sha if snapshot else None,
           scope="Local source preservation plus the exact supplied immutable tree, if any. A base-tree check is not a publication-diff check; the final candidate tree must be checked separately. Media blobs were not semantically inspected.")

    failed = sum(check["status"] == "fail" for check in checks)
    result = {"kind":"M6ReleaseVerification", "status":"fail" if failed else "pass",
              "checks_passed":len(checks)-failed, "checks_failed":failed, "checks":checks,
              "limits":["No H3 inference or media evaluation.",
                        "Behavior and portable invocation tests are separate recorded runs.",
                        "A provided Git tree snapshot only establishes its own immutable state."]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"kind":"M6ReleaseVerification", "status":"error",
                          "error":str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
