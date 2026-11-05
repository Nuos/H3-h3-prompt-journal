#!/usr/bin/env python3
"""Verify M3 release structure, immutable sources, scope and manifest.

Requires Python 3.10+ and Git. Does not certify spatial semantics or media.
Only --write-manifest writes a file; normal verification is read-only.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

DELIVERY = Path(__file__).resolve().parents[1]
REPO = DELIVERY.parents[1]
SKILL = DELIVERY / "h3-scene-blocking"
BASE = "91e6ed0b09d17e13cf5f58cccfe0df588c5b1d8a"
MANIFEST = DELIVERY / "release-manifest-m3.json"
SCOPES = ("h3-scene-blocking", "tests/m3", "validation/m3")
SINGLES = ("README.md", "20261105-development-m3-v001.md", "tools/verify_m3_release.py")
EXCLUDE = {"validation/m3/release-check.json"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def inventory():
    paths = {DELIVERY / p for p in SINGLES}
    for folder in SCOPES:
        paths.update(p for p in (DELIVERY / folder).rglob("*") if p.is_file())
    rows = []
    for path in sorted(paths):
        rel = path.relative_to(DELIVERY).as_posix()
        if rel in EXCLUDE or "__pycache__" in path.parts or path.suffix in (".pyc", ".pyo"):
            continue
        if path.is_file():
            data = path.read_bytes()
            rows.append({"path": rel, "bytes": len(data), "sha256": sha(data), "git_blob_sha": blob(data)})
    return {"kind": "M3ReleaseManifest", "version": "1.0.0", "package": SKILL.name,
            "package_version": "0.1.0", "repository_base": BASE,
            "plan_baseline": "skillplan-v0.1.2-608813b", "scope": list(SCOPES) + list(SINGLES),
            "self_hash_policy": "Manifest and excluded final report are fixed by the Git commit; no self hash.",
            "excluded_report": sorted(EXCLUDE), "files": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()
    checks = []

    def check(name, ok, detail=None):
        checks.append({"check": name, "passed": bool(ok), "detail": detail})

    check("required_release_scopes_and_documents_exist",
          all((DELIVERY / p).is_dir() for p in SCOPES)
          and all((DELIVERY / p).is_file() for p in SINGLES))
    entry = (SKILL / "SKILL.md").read_text()
    front = re.match(r'\A---\nname: ([^\n]+)\ndescription: ("[^\n]+")\n---\n', entry)
    valid = bool(front)
    if front:
        name, desc = front[1], json.loads(front[2])
        valid = (name == SKILL.name and len(name) <= 64
                 and bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)) and 1 <= len(desc) <= 1024)
    check("minimal_name_description_frontmatter", valid)
    check("entry_below_recommended_500_lines", len(entry.splitlines()) < 500, len(entry.splitlines()))
    roots = {p.name for p in SKILL.iterdir() if p.name != "__pycache__"}
    check("only_declared_runtime_roots", roots == {"SKILL.md", "references", "scripts", "assets"}, sorted(roots))
    check("runtime_has_no_symlink_dependencies", not any(p.is_symlink() for p in SKILL.rglob("*")))
    missing, outside = [], []
    for p in SKILL.rglob("*.md"):
        for link in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", p.read_text()):
            if link.startswith(("https://", "http://", "#")):
                continue
            target = (p.parent / link.split("#")[0]).resolve()
            if not target.is_file():
                missing.append(f"{p.relative_to(SKILL)} -> {link}")
            if not target.is_relative_to(SKILL.resolve()):
                outside.append(f"{p.relative_to(SKILL)} -> {link}")
    check("runtime_links_exist", not missing, missing)
    check("no_sibling_runtime_links", not outside, outside)
    linked = set(re.findall(r"\]\((references/[^)#]+)", entry))
    resources = {p.relative_to(SKILL).as_posix() for p in (SKILL / "references").iterdir() if p.is_file()}
    check("every_reference_routed_from_entry", resources <= linked, sorted(resources - linked))

    parse_errors = []
    for row in inventory()["files"]:
        p = DELIVERY / row["path"]
        try:
            if p.suffix == ".json":
                json.loads(p.read_text())
            elif p.suffix == ".py":
                ast.parse(p.read_text())
        except (ValueError, SyntaxError) as exc:
            parse_errors.append({"path": row["path"], "error": str(exc)})
    check("json_and_python_parse", not parse_errors, parse_errors)
    registry = json.loads((SKILL / "references/module-registry.json").read_text())
    check("parent_and_three_public_children", set(registry["modules"]) == {"M3", "M3.1", "M3.2", "M3.3"})
    absent = [r for group in list(registry["resources"].values()) + [n["resources"] for n in registry["modules"].values()]
              for r in group if not (SKILL / r).is_file()]
    check("registered_resources_available", not absent, absent)

    lock = json.loads((REPO / "docs/skillplan/baseline-lock.json").read_text())
    drift = [r["path"] for r in lock["files"] + lock["control_files"]
             if sha((REPO / r["path"]).read_bytes()) != r["sha256"]]
    check("frozen_plan_and_controls_unchanged", not drift, drift)
    for folder in ("h3-work-intent", "h3-asset-reference"):
        tree = subprocess.run(["git", "ls-tree", "-r", BASE, "--", "docs/h3skill/" + folder],
                              cwd=REPO, text=True, capture_output=True, check=True).stdout
        changed = []
        for line in tree.splitlines():
            info, name = line.split("\t", 1)
            p = REPO / name
            if not p.is_file() or blob(p.read_bytes()) != info.split()[2]:
                changed.append(name)
        check(folder + "_byte_unchanged", bool(tree) and not changed, changed)

    changed = subprocess.run(["git", "diff", "--name-only", BASE, "--"], cwd=REPO,
                             text=True, capture_output=True, check=True).stdout.splitlines()
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=REPO,
                               text=True, capture_output=True, check=True).stdout.splitlines()
    allowed = {"docs/h3skill/" + p for p in SINGLES} | {"docs/h3skill/release-manifest-m3.json"}
    scope_drift = [p for p in sorted(set(changed + untracked))
                   if p not in allowed and not any(p.startswith("docs/h3skill/" + s + "/") for s in SCOPES)]
    check("only_authorized_m3_release_paths_changed", not scope_drift, scope_drift)

    index = json.loads((SKILL / "references/case-index.json").read_text())
    source_errors = [r["path"] for r in index["files"]
                     if not (REPO / r["path"]).is_file()
                     or sha((REPO / r["path"]).read_bytes()) != r["sha256"]]
    check("case_text_hashes_match_sources", not source_errors, source_errors)
    check("case_inventory_covers_current_text_corpus", len(index["files"]) == 98 and len(index["cases"]) == 29,
          {"files": len(index["files"]), "cases": len(index["cases"])})
    for name, digest in {
        "h3-base-official.txt": "2cfebc096a6e08370f288d468d90b60f7f9bcb938f94bf090816e910e48e75fc",
        "h3-ref-official.txt": "1e574f356716ad55612247ffb7bbccbcdb484ad96599d63c7dca1af186b1fab7",
    }.items():
        check("immutable_official_" + name, sha((SKILL / "references" / name).read_bytes()) == digest)
    standard = DELIVERY / "_standards"
    records = json.loads((standard / "source-files.json").read_text())
    check("official_standard_snapshots_unchanged", all(sha((standard / r["local_path"]).read_bytes()) == r["sha256"]
                                                      for r in records["files"]))

    delivery_path = DELIVERY / "validation/m3/delivery-checks.json"
    delivery = json.loads(delivery_path.read_text()) if delivery_path.is_file() else {}
    runtime_drift = [p for p, digest in delivery.get("file_sha256", {}).items()
                     if not (DELIVERY / p).is_file() or sha((DELIVERY / p).read_bytes()) != digest]
    check("recorded_delivery_checks_pass_and_match_runtime", delivery.get("ok") is True
          and bool(delivery.get("file_sha256")) and not runtime_drift, runtime_drift)
    long_without_navigation = [p.relative_to(SKILL).as_posix() for p in (SKILL / "references").glob("*.md")
                               if len(p.read_text().splitlines()) > 100
                               and not any(title in p.read_text() for title in ("## 导航", "## 目录"))]
    check("long_reference_documents_have_navigation", not long_without_navigation, long_without_navigation)

    behavior_path = DELIVERY / "tests/m3/test-results.json"
    behavior = json.loads(behavior_path.read_text()) if behavior_path.is_file() else {}
    behavior_drift = [p for p, digest in behavior.get("file_sha256", {}).items()
                      if not (DELIVERY / p).is_file() or sha((DELIVERY / p).read_bytes()) != digest]
    check("recorded_m3_tests_match_tested_inputs", behavior.get("tests_run", 0) > 0
          and behavior.get("failures") == 0 and behavior.get("errors") == 0
          and bool(behavior.get("file_sha256")) and not behavior_drift, behavior_drift)
    trial_path = DELIVERY / "validation/m3/narrative-final-check.json"
    trial = json.loads(trial_path.read_text()) if trial_path.is_file() else {}
    trial_manifest_path = DELIVERY / "validation/m3/forward-use/narrative/read-manifest.json"
    trial_manifest = json.loads(trial_manifest_path.read_text()) if trial_manifest_path.is_file() else {}
    trial_drift = [r["path"] for r in trial_manifest.get("files", [])
                   if not (REPO / r["path"]).is_file() or sha((REPO / r["path"]).read_bytes()) != r["sha256"]]
    check("independent_m3_1_trial_matches_final_resources", trial.get("ok") is True
          and bool(trial_manifest.get("files")) and not trial_drift, trial_drift)

    expected = inventory()
    if args.write_manifest:
        MANIFEST.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n")
    actual = json.loads(MANIFEST.read_text()) if MANIFEST.is_file() else None
    check("release_manifest_matches_exact_deliverables", expected == actual, {"files": len(expected["files"])})
    result = {"kind": "M3ReleaseVerification", "repository_base": BASE,
              "checks": checks, "passed": sum(c["passed"] for c in checks), "total": len(checks),
              "ok": all(c["passed"] for c in checks),
              "scope": "Structure, source integrity, frozen baseline, change scope and release inventory only.",
              "not_certified": ["spatial semantic correctness", "geometry collision", "actual visibility",
                                "M7 timing", "H3 inference", "generated media", "G2-G4 full gates"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
