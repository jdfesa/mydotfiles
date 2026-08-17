#!/usr/bin/env python3
"""Pure policy helpers for the isolated Chezmoi pilot."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Iterable, Mapping


CRITICAL_ZERO_FIELDS = (
    "outOfRootWrites",
    "realOwnershipOverlaps",
    "secretFindings",
    "prohibitedFeatureFindings",
    "protectedMetadataChanges",
)
CRITICAL_TRUE_FIELDS = ("rollbackExact", "idempotent")
MANDATORY_TRUE_FIELDS = ("allSelectedFixturesPassed", "deterministic")
POSIX_ENV_ALLOWLIST = ("PATH",)
WINDOWS_ENV_ALLOWLIST = ("PATH", "SystemRoot", "WINDIR", "ComSpec", "PATHEXT")
PYTHON_COMPATIBILITY_CONTRACT = ">=3.11"
CHEZMOI_EXACT_VERSION = "2.72.0"


def stable_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _project_python_runtime(version: Any) -> str:
    """Project an exact audit version onto the declared compatibility contract."""

    try:
        major, minor = (int(part) for part in str(version).split(".", 2)[:2])
    except (TypeError, ValueError):
        return f"unsupported:{version}"
    if (major, minor) >= (3, 11):
        return PYTHON_COMPATIBILITY_CONTRACT
    return f"unsupported:{version}"


def project_chezmoi_version(version: Any) -> str:
    """Keep the exact semantic version while excluding distributor build banners."""

    match = re.search(r"\bv?(\d+\.\d+\.\d+)\b", str(version))
    if match and match.group(1) == CHEZMOI_EXACT_VERSION:
        return CHEZMOI_EXACT_VERSION
    return f"unsupported:{version}"


def _project(value: Any) -> Any:
    if isinstance(value, list):
        return [_project(item) for item in value]
    if not isinstance(value, dict):
        return value
    projected = {}
    for key, item in value.items():
        if key in {
            "recordedAt",
            "startedAt",
            "endedAt",
            "rawStdoutSha256",
            "rawStdoutLines",
            "rawStdoutPreview",
        }:
            continue
        projected[key] = _project(item)
    return projected


def evidence_projection(evidence: Mapping[str, Any]) -> dict[str, Any]:
    """Return the complete deterministic review projection.

    Wall-clock timestamps and all dynamic Git publication provenance are
    removed. Raw dump-config shape/hash provenance is excluded after its
    validated effective contract is recorded. The exact raw Python runtime is
    projected to the declared >=3.11 compatibility contract. Chezmoi
    distributor build banners are projected to
    the exact 2.72.0 semantic version, while OpenSpec remains exact. Commands,
    paths, hashes, manifests, modes, metrics, blockers, native evidence, and
    outcomes remain visible.
    """

    projected = copy.deepcopy(dict(evidence))
    # Raw top-level Git publication provenance remains reviewable in
    # review.json, but branch/rebase/commit/dirty transitions are not behavior.
    projected.pop("git", None)
    tools = projected.get("tools")
    if isinstance(tools, dict):
        if "python" in tools:
            tools["python"] = _project_python_runtime(tools["python"])
        if "chezmoi" in tools:
            tools["chezmoi"] = project_chezmoi_version(tools["chezmoi"])
    return _project(projected)


def evidence_projection_digest(evidence: Mapping[str, Any]) -> str:
    return stable_digest(evidence_projection(evidence))


def projection_differences(
    reviewed: Any, fresh: Any, path: str = "$"
) -> list[dict[str, Any]]:
    """Return deterministic leaf differences for reviewable validation errors."""

    if type(reviewed) is not type(fresh):
        return [{"path": path, "reviewed": reviewed, "fresh": fresh}]
    if isinstance(reviewed, dict):
        differences: list[dict[str, Any]] = []
        for key in sorted(set(reviewed) | set(fresh)):
            child_path = f"{path}/{key}"
            if key not in reviewed:
                differences.append({"path": child_path, "reviewed": "<missing>", "fresh": fresh[key]})
            elif key not in fresh:
                differences.append({"path": child_path, "reviewed": reviewed[key], "fresh": "<missing>"})
            else:
                differences.extend(projection_differences(reviewed[key], fresh[key], child_path))
        return differences
    if isinstance(reviewed, list):
        differences = []
        if len(reviewed) != len(fresh):
            differences.append({"path": path, "reviewedLength": len(reviewed), "freshLength": len(fresh)})
        for index, (reviewed_item, fresh_item) in enumerate(zip(reviewed, fresh)):
            differences.extend(
                projection_differences(reviewed_item, fresh_item, f"{path}/{index}")
            )
        return differences
    if reviewed != fresh:
        return [{"path": path, "reviewed": reviewed, "fresh": fresh}]
    return []


def select_outcome(
    mandatory: Mapping[str, Any],
    native_evidence: Mapping[str, Any],
    comparison: Mapping[str, Any],
) -> str:
    if any(mandatory.get(field) != 0 for field in CRITICAL_ZERO_FIELDS):
        return "reject"
    if any(mandatory.get(field) is not True for field in CRITICAL_TRUE_FIELDS):
        return "reject"
    if any(mandatory.get(field) is not True for field in MANDATORY_TRUE_FIELDS):
        return "keep-and-continue-evaluation"
    if native_evidence.get("windows") is not True:
        return "keep-and-continue-evaluation"
    policy = comparison.get("policy", {})
    if policy.get("permitsSelectiveMigration") is not True:
        return "keep-and-continue-evaluation"
    return "recommend-selective-migration"


def assert_outcome_invariants(evidence: Mapping[str, Any]) -> None:
    expected = select_outcome(
        evidence["mandatory"], evidence["nativeEvidence"], evidence["comparison"]
    )
    if evidence.get("outcome") != expected:
        raise ValueError(
            f"evidence outcome {evidence.get('outcome')!r} does not match selector {expected!r}"
        )
    if (
        evidence.get("outcome") == "recommend-selective-migration"
        and evidence["nativeEvidence"].get("windows") is not True
    ):
        raise ValueError("selective migration requires native Windows evidence")


def minimal_environment(
    host_environment: Mapping[str, str],
    overrides: Mapping[str, str],
    *,
    windows: bool = False,
) -> dict[str, str]:
    allowlist = WINDOWS_ENV_ALLOWLIST if windows else POSIX_ENV_ALLOWLIST
    environment = {
        key: host_environment[key]
        for key in allowlist
        if key in host_environment and host_environment[key]
    }
    environment.setdefault("PATH", os.defpath)
    environment.update(overrides)
    return environment


def measure_files(paths: Iterable[Path], *, relative_to: Path | None = None) -> dict[str, Any]:
    files: set[Path] = set()
    for raw_path in paths:
        path = raw_path.resolve()
        if path.is_file():
            files.add(path)
        elif path.is_dir():
            files.update(
                candidate.resolve()
                for candidate in path.rglob("*")
                if candidate.is_file() and "__pycache__" not in candidate.parts
            )
    raw_lines = 0
    by_file: dict[str, int] = {}
    for path in files:
        try:
            lines = len(path.read_text(encoding="utf-8").splitlines())
        except UnicodeDecodeError:
            continue
        raw_lines += lines
        label = path.relative_to(relative_to.resolve()).as_posix() if relative_to else path.name
        by_file[label] = lines
    return {"files": len(files), "rawLines": raw_lines, "byFile": dict(sorted(by_file.items()))}
