#!/usr/bin/env python3
"""Check the M8 release manifest, portable resources and protected source bytes.

Run from a full checkout. This verifier does not execute H3 or inspect media.
Behavior tests and isolated invocation records are separate evidence.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[3]
RELEASE = ROOT / "docs/h3skill"
PACKAGE = RELEASE / "h3-state-continuity"


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    def nonfinite(value):
        raise ValueError(f"nonfinite JSON in {path}: {value}")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=nonfinite)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main():
    checks = []

    def record(name, errors, **details):
        checks.append({"check": name, "status": "fail" if errors else "pass",
                       "errors": errors, **details})

    manifest = read_json(RELEASE / "release-manifest-m8.json")
    files = manifest["files"]
    expected = {item["path"]: item for item in files}
    errors = [] if len(expected) == len(files) else ["duplicate manifest paths"]
    for item in files:
        path = ROOT / item["path"]
        if Path(item["path"]).is_absolute() or ".." in Path(item["path"]).parts:
            errors.append("unsafe release path: " + item["path"])
        elif not path.is_file():
            errors.append("missing release file: " + item["path"])
        elif sha256(path) != item["sha256"] or path.stat().st_size != item["bytes"]:
            errors.append("release file drift: " + item["path"])
    record("release_file_hashes", errors, count=len(files))

    roots = {p.name for p in PACKAGE.iterdir()}
    errors = [] if roots == {"SKILL.md", "scripts", "references", "assets"} else ["package roots differ from declared distribution layout"]
    errors.extend("symlink: " + str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob("*") if p.is_symlink())
    errors.extend("generated cache: " + str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob("*")
                  if p.name == "__pycache__" or p.suffix == ".pyc")
    record("package_layout", errors, roots=sorted(roots),
           note="Optional resource folders are used by this skill, not mandatory for all Agent Skills.")

    skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
    fields, errors = {}, []
    if not match:
        errors.append("missing frontmatter")
    else:
        for line in match.group(1).splitlines():
            key, value = line.split(": ", 1)
            if key in fields:
                errors.append("duplicate frontmatter key: " + key)
            fields[key] = json.loads(value) if value.startswith('"') else value
    name, description = fields.get("name", ""), fields.get("description", "")
    if set(fields) != {"name", "description"}:
        errors.append("release expects name and description only")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or not 1 <= len(name) <= 64 or name != PACKAGE.name:
        errors.append("invalid name or directory mismatch")
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024 or "<" in description or ">" in description:
        errors.append("invalid description")
    if len(skill.splitlines()) >= 500:
        errors.append("entry exceeds chosen progressive-disclosure guidance")
    record("frontmatter_and_entry_length", errors, lines=len(skill.splitlines()),
           description_chars=len(description))

    errors, links, asset_paths = [], 0, set()
    for path in [PACKAGE / "SKILL.md", *sorted((PACKAGE / "references").glob("*.md"))]:
        text = path.read_text(encoding="utf-8")
        for asset in re.findall(r"(?<![\w./-])assets/[A-Za-z0-9_./-]+\.(?:json|py|txt)", text):
            asset_paths.add(asset)
            if not (PACKAGE / asset).is_file():
                errors.append(f"missing documented fixture: {path.name} -> {asset}")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if re.match(r"[a-z][a-z0-9+.-]*:", link) or link.startswith("#"):
                continue
            links += 1
            dest = (path.parent / link.split("#", 1)[0]).resolve()
            if not dest.is_relative_to(PACKAGE.resolve()) or not dest.exists():
                errors.append(f"invalid package resource: {path.name} -> {link}")
    record("relative_links", errors, count=links, documented_asset_paths=len(asset_paths))

    references = sorted(p for p in (PACKAGE / "references").iterdir() if p.is_file())
    record("single_hop_reference_routes",
           ["unrouted reference: " + p.name for p in references if f"references/{p.name}" not in skill],
           count=len(references))

    package_files = [p for p in PACKAGE.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    record("complete_runtime_manifest", ["unmanifested file: " + str(p.relative_to(ROOT))
           for p in package_files if p.relative_to(ROOT).as_posix() not in expected], count=len(package_files))

    imports, errors = set(), []
    for path in (PACKAGE / "scripts").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add((node.module or "").split(".")[0])
                if node.level:
                    errors.append("relative external import in " + path.name)
    bundled = {path.stem for path in (PACKAGE / "scripts").glob("*.py")}
    allowed = set(sys.stdlib_module_names) | {"__future__"} | bundled
    errors.extend("unbundled non-stdlib import: " + name for name in sorted(imports - allowed))
    record("standard_library_runtime", errors, imports=sorted(imports),
           bundled_modules=sorted(imports & bundled))

    errors = []
    json_files = sorted(PACKAGE.rglob("*.json"))
    for path in json_files:
        try:
            read_json(path)
        except (ValueError, UnicodeError) as exc:
            errors.append(str(exc))
    record("strict_json_resources", errors, count=len(json_files))

    protocol = read_json(PACKAGE / "references/h3-protocol-source.json")
    errors, count = [], 0
    for source in protocol["sources"]:
        if source.get("offline_snapshot"):
            count += 1
            path = PACKAGE / "references" / source["offline_snapshot"]
            if sha256(path) != source["sha256"] or blob_sha(path) != source["git_blob_sha"]:
                errors.append("official source drift: " + path.name)
    record("official_protocol_exact_bytes", errors, count=count)

    errors = []
    if protocol["protocol"]["base_fields"] != ["integrated_multimodal_description", "overall_soundscape", "non_diegetic_music"]:
        errors.append("base fields mismatch")
    if protocol["protocol"]["reference_fields"] != ["subject_definitions", "summary", "retention_analysis", "detailed_description", "overall_soundscape", "non_diegetic_music"]:
        errors.append("Ref2VA fields mismatch")
    if protocol["m8_mapping"]["partitions"] != {"M8.1": "ContinuityPolicy", "M8.2": "StateLedger", "M8.3": "ContinuityHandoffs"}:
        errors.append("M8 partitions mismatch")
    record("official_field_mapping", errors, note="Documented mapping, not an H3 compiler run.")

    case_index = read_json(PACKAGE / "references/case-index.json")
    errors = []
    case_files = case_index["files"]
    if len({item["path"] for item in case_files}) != len(case_files):
        errors.append("duplicate case sources")
    for item in case_files:
        relative = item["path"]
        path = ROOT / relative
        if not relative.startswith("case-studies/") or ".." in Path(relative).parts:
            errors.append("source outside case boundary: " + relative)
            continue
        if not path.is_file() or sha256(path) != item["sha256"] or blob_sha(path) != item["git_blob_sha1"]:
            errors.append("case source drift: " + relative)
            continue
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if item["line_count"] != line_count or not item.get("read_status") or not item.get("read_scope"):
            errors.append("case read metadata mismatch: " + relative)
        for span in item.get("line_ranges", []):
            if not 1 <= span["start"] <= span["end"] <= line_count:
                errors.append("case range outside file: " + relative)
    record("case_text_identity_and_read_scope", errors, count=len(case_files),
           note="Recorded reading scope; indexing does not mean full-text or media evaluation.")

    lock = read_json(ROOT / "docs/skillplan/baseline-lock.json")
    locked = lock["files"]
    if isinstance(locked, dict):
        locked = [{"path": path, **entry} for path, entry in locked.items()]
    errors = []
    for item in locked:
        relative = item.get("path", item.get("file", item.get("relative_path")))
        path = ROOT / relative if relative.startswith("docs/") else ROOT / "docs/skillplan" / relative
        if not path.is_file() or sha256(path) != item["sha256"]:
            errors.append("frozen plan drift: " + relative)
    record("frozen_plan", errors, count=len(locked))

    protected = read_json(RELEASE / "validation/m8/protected-baseline.json")
    errors = []
    for item in protected["files"]:
        path = ROOT / item["path"]
        if not path.is_file() or sha256(path) != item["sha256"] or blob_sha(path) != item["git_blob_sha1"]:
            errors.append("protected file drift: " + item["path"])
    record("protected_sources", errors, count=len(protected["files"]),
           source_commit=protected["source_commit"])

    failed = sum(check["status"] == "fail" for check in checks)
    print(json.dumps({"kind": "M8ReleaseVerification", "status": "fail" if failed else "pass",
                      "checks_passed": len(checks)-failed, "checks_failed": failed, "checks": checks,
                      "limits": ["No H3 inference, audio/video decoding or media-quality certification; structured state comparisons are not free-text semantic analysis.",
                                 "Behavior and isolated-use tests are separately recorded.",
                                 "The final publication diff must also be checked against the base commit."]},
                     ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"kind": "M8ReleaseVerification", "status": "error", "error": str(exc)},
                         ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
