#!/usr/bin/env python3
"""Traceability and CI-policy auditing for the Chezmoi pilot."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class AuditError(RuntimeError):
    """A review declaration is incomplete or stale."""


AUTOMATED_CHECKS = {
    "UT-CONTAINMENT-MATRIX": "experiments/chezmoi-pilot/tests/test_pilot.py::test_negative_matrix",
    "UT-ENV-ALLOWLIST": "experiments/chezmoi-pilot/tests/test_pilot.py::test_host_secrets_and_agent_are_not_inherited",
    "UT-BWRAP-PREFIX": "experiments/chezmoi-pilot/tests/test_pilot.py::test_bubblewrap_uses_private_dev_and_one_host_backed_write_root",
    "UT-PROJECTION-VOLATILE": "experiments/chezmoi-pilot/tests/test_pilot.py::test_timestamps_do_not_change_projection",
    "UT-PROJECTION-PUBLICATION": "experiments/chezmoi-pilot/tests/test_pilot.py::test_publication_git_and_compatible_python_do_not_change_projection",
    "UT-PROJECTION-CHEZMOI-PROVENANCE": "experiments/chezmoi-pilot/tests/test_pilot.py::test_chezmoi_build_provenance_does_not_change_exact_version_projection",
    "UT-PROJECTION-SENSITIVE": "experiments/chezmoi-pilot/tests/test_pilot.py::test_deterministic_evidence_changes_projection",
    "UT-OUTCOME-REJECT": "experiments/chezmoi-pilot/tests/test_pilot.py::test_outcome_selector_rejects_critical_failure",
    "UT-OUTCOME-CONTINUE": "experiments/chezmoi-pilot/tests/test_pilot.py::test_outcome_selector_continues_without_native_windows",
    "UT-OUTCOME-INCOMPLETE": "experiments/chezmoi-pilot/tests/test_pilot.py::test_outcome_selector_continues_on_incomplete_mandatory",
    "UT-OUTCOME-RECOMMEND": "experiments/chezmoi-pilot/tests/test_pilot.py::test_outcome_selector_can_recommend_only_when_all_gates_pass",
    "UT-OUTCOME-NATIVE-INVARIANT": "experiments/chezmoi-pilot/tests/test_pilot.py::test_recommendation_without_native_windows_violates_invariant",
    "UT-AMBIENT-HOME-REJECT": "experiments/chezmoi-pilot/tests/test_pilot.py::test_ambient_home_template_is_rejected",
    "UT-SECRET-FIXTURE-REJECT": "experiments/chezmoi-pilot/tests/test_pilot.py::test_secret_like_fixture_data_is_rejected",
    "UT-TEMPLATE-GUARDRAIL": "experiments/chezmoi-pilot/tests/test_pilot.py::test_template_key_guardrail_is_rejected",
    "UT-MISSING-GIT-DATA": "experiments/chezmoi-pilot/tests/test_pilot.py::test_missing_git_data_fails_render",
    "UT-PREVIEW-DIGEST": "experiments/chezmoi-pilot/tests/test_pilot.py::test_source_change_changes_preview_digest",
    "UT-SEMANTIC-FALSE-MAPPING": "experiments/chezmoi-pilot/tests/test_pilot.py::test_false_os_window_mapping_is_rejected",
    "UT-SEMANTIC-COLLISION": "experiments/chezmoi-pilot/tests/test_pilot.py::test_semantic_chord_collision_is_rejected",
    "CHK-CANONICAL-MODEL": "experiments/chezmoi-pilot/scripts/pilot.py::validate_repository",
    "CHK-CANONICAL-SEMANTICS": "experiments/chezmoi-pilot/scripts/pilot.py::validate_semantics",
    "CHK-WINDOWS-FIXTURE": "experiments/chezmoi-pilot/scripts/pilot.py::validate_windows_fixture",
    "CHK-STATIC-SOURCE": "experiments/chezmoi-pilot/scripts/pilot.py::static_validate_source",
    "CHK-GENERATED-DOCS": "experiments/chezmoi-pilot/scripts/pilot.py::generate_documents",
    "CHK-TRACEABILITY": "experiments/chezmoi-pilot/scripts/pilot.py::validate_traceability",
    "UT-TRACEABILITY-STALE-ID": "experiments/chezmoi-pilot/tests/test_pilot.py::test_traceability_rejects_stale_check_id",
    "UT-TRACEABILITY-MISSING": "experiments/chezmoi-pilot/tests/test_pilot.py::test_traceability_rejects_missing_scenario",
    "CHK-CI-POLICY": "experiments/chezmoi-pilot/scripts/pilot.py::validate_ci_workflow",
    "CHK-TOOL-VERSIONS": "experiments/chezmoi-pilot/scripts/pilot.py::expected_versions",
    "CHK-OUTCOME-INVARIANT": "experiments/chezmoi-pilot/scripts/pilot_policy.py::assert_outcome_invariants",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def json_pointer(value: Any, pointer: str) -> Any:
    if not pointer.startswith("/"):
        raise AuditError(f"invalid JSON pointer: {pointer}")
    current = value
    for raw_part in pointer.split("/")[1:]:
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(part)]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise AuditError(f"JSON pointer traverses a scalar: {pointer}")
    return current


def declared_scenarios(change_root: Path) -> set[tuple[str, str]]:
    scenarios: set[tuple[str, str]] = set()
    for spec_path in sorted((change_root / "specs").glob("*/spec.md")):
        capability = spec_path.parent.name
        for line in spec_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#### Scenario: "):
                scenarios.add((capability, line.removeprefix("#### Scenario: ")))
    return scenarios


def validate_traceability(
    repo_root: Path,
    pilot_root: Path,
    change_root: Path,
    evidence: dict[str, Any] | None = None,
    declaration_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    declaration = declaration_override or load_json(pilot_root / "traceability.json")
    entries = declaration.get("entries", [])
    expected = declared_scenarios(change_root)
    declared: set[tuple[str, str]] = set()
    kinds: dict[str, int] = {}
    for entry in entries:
        key = (entry["capability"], entry["scenario"])
        if key in declared:
            raise AuditError(f"duplicate traceability entry: {key}")
        declared.add(key)
        coverage = entry["coverage"]
        kind = coverage["kind"]
        kinds[kind] = kinds.get(kind, 0) + 1
        if kind == "automated-check":
            check_id = coverage["id"]
            locator = AUTOMATED_CHECKS.get(check_id)
            if locator is None:
                raise AuditError(f"unknown automated traceability check: {check_id}")
            path_text, symbol = locator.split("::", 1)
            if symbol not in (repo_root / path_text).read_text(encoding="utf-8"):
                raise AuditError(f"traceability check locator is stale: {check_id}")
        elif kind == "generated-evidence":
            pointer = coverage["pointer"]
            if evidence is not None:
                try:
                    json_pointer(evidence, pointer)
                except (KeyError, IndexError, ValueError) as exc:
                    raise AuditError(f"unresolved traceability evidence pointer: {pointer}") from exc
        elif kind in {"native-blocked", "human-review-gate"}:
            if not coverage.get("reason"):
                raise AuditError(f"traceability {kind} lacks rationale: {key}")
        else:
            raise AuditError(f"unsupported traceability coverage kind: {kind}")
    if declared != expected:
        missing = sorted(expected - declared)
        extra = sorted(declared - expected)
        raise AuditError(f"traceability scenario mismatch: missing={missing}, extra={extra}")
    return {"scenarios": len(expected), "entries": len(entries), "coverageKinds": kinds}


def validate_ci_workflow(repo_root: Path) -> dict[str, Any]:
    workflow = (repo_root / ".github/workflows/chezmoi-pilot.yml").read_text(encoding="utf-8")
    required = (
        "paths:",
        "workflow_dispatch:",
        "runs-on: ubuntu-22.04",
        "actions/setup-python@v6",
        'python-version: "3.11"',
        "actions/setup-node@v6",
        'node-version: "26.7.0"',
        "npm@12.0.2 @fission-ai/openspec@1.9.0",
        "https://github.com/twpayne/chezmoi/releases/download/v2.72.0/chezmoi-linux-amd64",
        "ba563f716d5c00a2e91d4aeb199b417c6b219db2896f890fd422fc72610b2d90",
        "bwrap --die-with-parent",
        "--ro-bind / /",
        "--proc /proc",
        "--dev /dev",
        "experiments/chezmoi-pilot/scripts/validate",
        "openspec validate evaluate-chezmoi-pilot --strict",
        "scripts/test-profile-resolve",
        "scripts/validate-profiles",
        "scripts/lint-shell",
        "native-windows-gate",
    )
    missing = [value for value in required if value not in workflow]
    if missing:
        raise AuditError(f"CI workflow policy is incomplete: {missing}")
    if re.search(r"^\s+container:\s*", workflow, re.MULTILINE):
        raise AuditError("CI must run Bubblewrap directly on the pinned host, not in a job container")
    forbidden = (
        "seccomp=unconfined",
        "--security-opt",
        "--privileged",
        "--cap-add",
        "apparmor=unconfined",
        "unprivileged_userns_clone",
        "max_user_namespaces",
        "sysctl ",
        "continue-on-error",
    )
    present = [value for value in forbidden if value in workflow]
    if present:
        raise AuditError(f"CI contains a forbidden security relaxation: {present}")
    main_push = re.compile(
        r"(?m)^  push:\n    branches:\n      - main\n    paths:\n"
    )
    if not main_push.search(workflow) or "  pull_request:\n" not in workflow:
        raise AuditError("CI triggers must use pull_request plus path-filtered push on main")
    smoke = workflow.index("bwrap --die-with-parent")
    checkout = workflow.index("actions/checkout@v6")
    harness = workflow.index("experiments/chezmoi-pilot/scripts/validate")
    if not smoke < checkout < harness:
        raise AuditError("strict Bubblewrap smoke must precede checkout and the pilot harness")
    return {
        "requiredChecks": len(required),
        "pathFiltered": True,
        "pushBranches": ["main"],
        "runner": "ubuntu-22.04",
        "evidenceClass": "portable-linux",
        "jobContainer": False,
        "nativeArch": False,
        "nativeWindowsJob": "disabled",
    }
