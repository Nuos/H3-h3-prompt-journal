#!/usr/bin/env python3
"""Verify this M1 delivery, its source snapshots and the frozen plan.

The official Anthropic validator is run separately. This supplementary verifier
uses only the standard library. It does not validate semantic or media quality.
--write-manifest updates only docs/h3skill/release-manifest.json.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

BASE = "0ce8b7b1890052bf1d4dd233ef20e68817b38f28"
DELIVERY = Path(__file__).resolve().parents[1]
REPO = DELIVERY.parents[1]
SKILL = DELIVERY / "h3-work-intent"
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def delivered_files():
    return sorted(p for p in DELIVERY.rglob("*") if p.is_file()
                  and not EXCLUDED_PARTS.intersection(p.parts)
                  and p.suffix not in {".pyc", ".pyo"}
                  and p.name != "release-manifest.json")


def manifest():
    entries = [{"path": p.relative_to(DELIVERY).as_posix(),
                "bytes": p.stat().st_size, "sha256": sha256(p)}
               for p in delivered_files()]
    return {"schema_version": "1.0.0", "package": "h3-work-intent",
            "package_version": "0.1.0", "base_commit": BASE,
            "scope": "docs/h3skill", "file_count_excluding_manifest": len(entries),
            "self_hash_policy": "The manifest is fixed by its Git commit, not self-hashed.",
            "excluded_generated_content": sorted(EXCLUDED_PARTS) + ["*.pyc", "*.pyo"],
            "files": entries}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args(argv)
    findings = []

    def check(name, condition, detail=""):
        findings.append({"check": name, "passed": bool(condition), "detail": detail})

    entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.+)\Z", entry, re.S)
    check("frontmatter_and_body", match is not None)
    if match:
        pairs = dict(re.findall(r"^([a-z-]+):\s*(.+)$", match[1], re.M))
        name = pairs.get("name", "")
        description = pairs.get("description", "")
        if description.startswith('"'):
            try:
                description = json.loads(description)
            except json.JSONDecodeError:
                description = ""
        check("name_exact_directory_and_ascii", name == SKILL.name
              and bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name))
              and 1 <= len(name) <= 64)
        check("description_nonempty_and_bounded", 1 <= len(description.strip()) <= 1024)
        check("minimal_metadata", set(pairs) == {"name", "description"})
        check("entry_under_500_lines", len(entry.splitlines()) < 500,
              "Official recommendation, not an inferred hard format limit.")

    broken_links = []
    outside_links = []
    for path in sorted(SKILL.rglob("*.md")):
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "#")):
                continue
            local = (path.parent / target.split("#", 1)[0]).resolve()
            if not local.is_relative_to(SKILL.resolve()):
                outside_links.append(f"{path.relative_to(SKILL)} -> {target}")
            if not local.exists():
                broken_links.append(f"{path.relative_to(SKILL)} -> {target}")
    check("all_skill_local_markdown_links_resolve", not broken_links, broken_links)
    check("skill_no_sibling_runtime_link", not outside_links, outside_links)

    delivery_docs = [DELIVERY / "README.md", DELIVERY / "20261104-development-m1-v001.md",
                     DELIVERY / "validation/semantic-review.md",
                     DELIVERY / "validation/narrative-trial/README.md",
                     DELIVERY / "validation/mv-trial/README.md"]
    broken_delivery_links = []
    for path in delivery_docs:
        if not path.is_file():
            broken_delivery_links.append(str(path.relative_to(DELIVERY)))
            continue
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
            if not target.startswith(("https://", "http://", "#")):
                if not (path.parent / target.split("#", 1)[0]).exists():
                    broken_delivery_links.append(f"{path.relative_to(DELIVERY)} -> {target}")
    check("delivery_documentation_links_resolve", not broken_delivery_links,
          broken_delivery_links)

    json_errors = []
    python_errors = []
    for path in delivered_files():
        try:
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            elif path.suffix == ".py":
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (ValueError, SyntaxError) as exc:
            (json_errors if path.suffix == ".json" else python_errors).append(
                {"path": str(path.relative_to(DELIVERY)), "error": str(exc)})
    check("json_files_parse", not json_errors, json_errors)
    check("python_files_parse", not python_errors, python_errors)

    test_record = json.loads((DELIVERY / "tests/test-results.json").read_text(encoding="utf-8"))
    changed_tested_files = [path for path, digest in test_record["tested_file_sha256"].items()
                            if sha256(DELIVERY / path) != digest]
    check("current_runtime_and_fixtures_match_tested_versions", not changed_tested_files,
          changed_tested_files)
    format_record = json.loads((DELIVERY / "validation/official-format-check.json").read_text(encoding="utf-8"))
    check("current_entry_matches_official_validated_version",
          sha256(SKILL / "SKILL.md") == format_record["skill_entry_sha256"]
          and format_record["exit_code"] == 0)

    required = ["references/contracts.json", "references/module-registry.json",
                "references/contract-guide.md", "references/h3-label-mapping.md",
                "references/case-evidence.md", "scripts/m1_contract.py"]
    check("declared_core_resources_present", all((SKILL / p).is_file() for p in required))
    registry = SKILL / "references/module-registry.json"
    if registry.exists():
        content = registry.read_text(encoding="utf-8")
        check("four_declared_nodes", all(f'"{node}"' in content
                                         for node in ["M1", "M1.1", "M1.2", "M1.3"]))
        missing = [p for p in set(re.findall(r'"((?:references|scripts|assets)/[^"#]+)"', content))
                   if not (SKILL / p).exists()]
        check("registry_resources_present", not missing, missing)

    lock = json.loads((REPO / "docs/skillplan/baseline-lock.json").read_text(encoding="utf-8"))
    mismatches = []
    for item in lock["files"] + lock["control_files"]:
        path = REPO / item["path"]
        if not path.is_file() or sha256(path) != item["sha256"]:
            mismatches.append(item["path"])
    check("nine_frozen_plan_and_two_control_files_unchanged", not mismatches, mismatches)

    standard = DELIVERY / "_standards"
    std_record = json.loads((standard / "source-files.json").read_text(encoding="utf-8"))
    mismatches = [i["local_path"] for i in std_record["files"]
                  if sha256(standard / i["local_path"]) != i["sha256"]]
    check("official_standard_snapshot_integrity", not mismatches, mismatches)

    index_path = SKILL / "references/case-index.json"
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
        mismatches = []
        for item in index["source_inventory"]:
            path = REPO / item["path"]
            if not path.is_file() or sha256(path) != item["sha256"]:
                mismatches.append(item["path"])
        check("98_case_text_source_hashes", len(index["source_inventory"]) == 98
              and not mismatches, mismatches)
        check("29_case_roles_registered", len(index["case_roles"]) == 29)
        excerpt_mismatches = []
        for evidence in index["evidence"]:
            lines = (REPO / evidence["path"]).read_text(encoding="utf-8").splitlines()
            actual = "\n".join(lines[n - 1] for n in evidence["excerpt_lines"])
            if actual != evidence["excerpt"]:
                excerpt_mismatches.append(evidence["id"])
        check("38_case_excerpts_match_original_lines", len(index["evidence"]) == 38
              and not excerpt_mismatches, excerpt_mismatches)

    h3_hashes = {
        "h3-base-official.txt": "2cfebc096a6e08370f288d468d90b60f7f9bcb938f94bf090816e910e48e75fc",
        "h3-ref-official.txt": "1e574f356716ad55612247ffb7bbccbcdb484ad96599d63c7dca1af186b1fab7",
    }
    bad_h3 = [name for name, digest in h3_hashes.items()
              if not (SKILL / "references" / name).is_file()
              or sha256(SKILL / "references" / name) != digest]
    check("official_h3_guides_exact_bytes", not bad_h3, bad_h3)

    git = subprocess.run(["git", "diff", "--name-only", BASE, "--"], cwd=REPO,
                         text=True, capture_output=True, check=False)
    changed = [s for s in git.stdout.splitlines() if s]
    check("tracked_changes_confined_to_delivery", git.returncode == 0
          and all(p.startswith("docs/h3skill/") for p in changed), changed)

    if args.write_manifest:
        (DELIVERY / "release-manifest.json").write_text(
            json.dumps(manifest(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    target = DELIVERY / "release-manifest.json"
    check("release_manifest_matches_current_files", target.is_file()
          and json.loads(target.read_text(encoding="utf-8")) == manifest())
    result = {"kind": "M1DeliveryIntegrityCheck", "base_commit": BASE,
              "passed": all(item["passed"] for item in findings),
              "checks": findings,
              "scope_limit": "Integrity and structural checks only; no semantic or media pass."}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
