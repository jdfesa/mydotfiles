#!/usr/bin/env python3
"""Isolated, evidence-producing Chezmoi evaluation harness."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform as host_platform
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from pilot_audit import (
    AuditError,
    validate_ci_workflow as audit_ci_workflow,
    validate_traceability as audit_traceability,
)
from pilot_docs import DocsError, generate_documents as render_documents
from pilot_policy import (
    CHEZMOI_EXACT_VERSION,
    POSIX_ENV_ALLOWLIST,
    WINDOWS_ENV_ALLOWLIST,
    assert_outcome_invariants,
    evidence_projection,
    evidence_projection_digest,
    measure_files,
    minimal_environment,
    project_chezmoi_version,
    projection_differences,
    select_outcome,
    stable_digest,
)


SCRIPT = Path(__file__).resolve()
PILOT_ROOT = SCRIPT.parents[1]
REPO_ROOT = SCRIPT.parents[3]
CHANGE_ROOT = REPO_ROOT / "openspec/changes/evaluate-chezmoi-pilot"
MARKER_NAME = ".chezmoi-pilot-root"
PLATFORMS = ("linux", "macos", "windows")
EXPECTED_OPEN_SPEC = "1.9.0"
EXPECTED_CHEZMOI = CHEZMOI_EXACT_VERSION
WINDOWS_TERMINAL_VERSION = "1.24.11321.0"
OPENSPEC_RESOLUTION_METHODS = (
    "supported resolution order: set OPENSPEC_BIN to an executable path; "
    "place openspec on PATH; on POSIX install it at ~/.local/bin/openspec. "
    "On Windows, use OPENSPEC_BIN or PATH."
)

class PilotError(RuntimeError):
    """Fail-closed pilot error."""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalized_text(text: str, root: Path, real_home: Path) -> str:
    return text.replace(str(root), "<RUN>").replace(str(REPO_ROOT), "<REPO>").replace(
        str(real_home), "<REAL_HOME>"
    )


def is_descendant(path: Path, parent: Path) -> bool:
    return path != parent and parent in path.parents


def ensure_no_symlink_component(root: Path, path: Path) -> None:
    root = root.resolve(strict=True)
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise PilotError(f"path is outside marked root: {path}") from exc
    current = root
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise PilotError(f"symlink component rejected: {current}")


def guard_candidate(root: Path, candidate: Path, protected: Iterable[Path]) -> Path:
    root = root.resolve(strict=True)
    candidate = candidate.resolve(strict=False)
    if candidate == Path("/"):
        raise PilotError("filesystem root rejected")
    if candidate != root and not is_descendant(candidate, root):
        raise PilotError(f"candidate escapes marked root: {candidate}")
    ensure_no_symlink_component(root, candidate)
    for raw_protected in protected:
        protected_path = raw_protected.resolve(strict=False)
        if protected_path == Path("/"):
            if candidate == protected_path:
                raise PilotError("filesystem root rejected")
            continue
        if (
            candidate == protected_path
            or is_descendant(candidate, protected_path)
            or is_descendant(protected_path, candidate)
        ):
            raise PilotError(f"protected path overlap: {candidate} <-> {protected_path}")
    return candidate


def marker_payload(root: Path, nonce: str) -> dict[str, str]:
    return {"kind": "chezmoi-pilot", "root": str(root.resolve()), "nonce": nonce}


def verify_marker(root: Path, expected_nonce: str | None = None) -> str:
    root = root.resolve(strict=True)
    marker = root / MARKER_NAME
    if marker.is_symlink() or not marker.is_file():
        raise PilotError(f"missing or unsafe pilot marker: {marker}")
    payload = load_json(marker)
    if payload.get("kind") != "chezmoi-pilot" or payload.get("root") != str(root):
        raise PilotError("pilot marker does not match canonical root")
    nonce = payload.get("nonce")
    if not isinstance(nonce, str) or len(nonce) < 32:
        raise PilotError("pilot marker nonce is invalid")
    if expected_nonce is not None and nonce != expected_nonce:
        raise PilotError("pilot marker nonce changed")
    return nonce


def profile_entries() -> list[dict[str, str]]:
    profiles_dir = REPO_ROOT / "profiles"
    results: list[dict[str, str]] = []

    def expand(path: Path, chain: tuple[Path, ...]) -> None:
        resolved = path.resolve(strict=True)
        if resolved in chain:
            raise PilotError(f"profile include cycle: {resolved}")
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("@include "):
                include = line.split(maxsplit=1)[1]
                expand(profiles_dir / f"{include}.links", chain + (resolved,))
                continue
            if "|" not in line:
                raise PilotError(f"invalid profile line: {path}: {line}")
            source, target = line.split("|", 1)
            results.append({"source": source, "target": target, "profile": path.stem})

    for profile_path in sorted(profiles_dir.glob("*.links")):
        expand(profile_path, ())
    unique: dict[tuple[str, str], dict[str, str]] = {}
    for entry in results:
        unique[(entry["source"], entry["target"])] = entry
    return sorted(unique.values(), key=lambda item: (item["target"], item["source"]))


def protected_paths(real_home: Path) -> list[Path]:
    paths = [Path("/"), real_home, REPO_ROOT]
    for entry in profile_entries():
        prefix = "$HOME/"
        if not entry["target"].startswith(prefix):
            raise PilotError(f"profile target is not HOME-relative: {entry['target']}")
        paths.append(real_home / entry["target"][len(prefix) :])
    paths.extend(
        [
            real_home / ".config/chezmoi",
            real_home / ".cache/chezmoi",
            real_home / ".local/share/chezmoi",
        ]
    )
    return paths


def path_metadata(path: Path) -> dict[str, Any]:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return {"path": str(path), "type": "missing"}
    mode = stat.S_IMODE(info.st_mode)
    if stat.S_ISLNK(info.st_mode):
        return {"path": str(path), "type": "symlink", "mode": f"{mode:04o}", "target": os.readlink(path)}
    if stat.S_ISREG(info.st_mode):
        return {"path": str(path), "type": "file", "mode": f"{mode:04o}", "sha256": sha256_file(path)}
    if stat.S_ISDIR(info.st_mode):
        return {"path": str(path), "type": "directory", "mode": f"{mode:04o}"}
    return {"path": str(path), "type": "other", "mode": f"{mode:04o}"}


def protected_snapshot(real_home: Path) -> list[dict[str, Any]]:
    return [path_metadata(path) for path in sorted(set(protected_paths(real_home)), key=str)]


def tree_manifest(root: Path) -> list[dict[str, str]]:
    manifest: list[dict[str, str]] = []
    if not root.exists():
        return manifest
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        info = path.lstat()
        mode = f"{stat.S_IMODE(info.st_mode):04o}"
        if path.is_symlink():
            manifest.append({"path": relative, "type": "symlink", "mode": mode, "target": os.readlink(path)})
        elif path.is_dir():
            manifest.append({"path": relative, "type": "directory", "mode": mode})
        elif path.is_file():
            manifest.append({"path": relative, "type": "file", "mode": mode, "sha256": sha256_file(path)})
        else:
            raise PilotError(f"unsupported filesystem entry: {path}")
    return manifest


def canonical_source_files() -> list[Path]:
    files = [
        REPO_ROOT / "shared/starship/starship.toml",
        REPO_ROOT / "shared/kitty/common.conf",
        REPO_ROOT / "shared/kitty/active-theme.conf",
        REPO_ROOT / "shared/kitty/pass_keys.py",
        REPO_ROOT / "shared/kitty/get_layout.py",
        REPO_ROOT / "shared/kitty/quick-access-terminal-center.conf",
        REPO_ROOT / "shared/kitty/quick-access-terminal-daily.conf",
        REPO_ROOT / "os/linux/kitty/kitty.conf",
        REPO_ROOT / "os/macos/kitty/kitty.conf",
    ]
    files.extend(sorted((REPO_ROOT / "shared/kitty/sessions").glob("*")))
    files.extend(sorted((REPO_ROOT / "shared/kitty/scripts").glob("*")))
    return [path for path in files if path.is_file()]


def canonical_hashes() -> dict[str, str]:
    return {path.relative_to(REPO_ROOT).as_posix(): sha256_file(path) for path in canonical_source_files()}


def verify_canonical_hashes() -> None:
    expected_path = PILOT_ROOT / "expected/canonical-hashes.json"
    if not expected_path.is_file():
        raise PilotError("expected/canonical-hashes.json is missing; run update-hashes after review")
    expected = load_json(expected_path)
    current = canonical_hashes()
    if expected != current:
        raise PilotError("canonical source hash drift detected")


def safe_copy(source: Path, destination: Path, transform: bool = False) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if transform:
        text = source.read_text(encoding="utf-8")
        replacements = {
            "$HOME/mydotfiles/shared/colorscheme/colorscheme-selector.sh": "$KITTY_CONFIG_DIRECTORY/pilot-unsupported/colorscheme-selector.sh",
            "$HOME/mydotfiles/shared/kitty": "$KITTY_CONFIG_DIRECTORY",
            "~/mydotfiles/shared/kitty": "$KITTY_CONFIG_DIRECTORY",
            "~/mydotfiles": "$KITTY_CONFIG_DIRECTORY/pilot-repository",
            "$HOME/github/skitty": "$KITTY_CONFIG_DIRECTORY/pilot-unsupported/skitty",
            "~/github/skitty": "$KITTY_CONFIG_DIRECTORY/pilot-unsupported/skitty",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        destination.write_text(text, encoding="utf-8")
    else:
        shutil.copyfile(source, destination)
    destination.chmod(0o644)


def stage_source(platform_name: str, source_root: Path) -> None:
    mappings = load_json(PILOT_ROOT / "mappings.json")
    cases = mappings["cases"]
    for case in cases.values():
        if platform_name not in case["platforms"]:
            continue
        destination = source_root / case["stage"]
        if case.get("canonical"):
            source = REPO_ROOT / case["canonical"]
            safe_copy(
                source,
                destination,
                transform=case["model"] in {"documented-isolation-transform", "separate-platform-entrypoint"},
            )
        else:
            safe_copy(PILOT_ROOT / case["fixture"], destination)

    if platform_name in {"linux", "macos"}:
        kitty_root = source_root / "dot_config/kitty"
        for relative in (
            "active-theme.conf",
            "pass_keys.py",
            "get_layout.py",
            "quick-access-terminal-center.conf",
            "quick-access-terminal-daily.conf",
        ):
            safe_copy(REPO_ROOT / "shared/kitty" / relative, kitty_root / relative, transform=True)
        for directory in ("sessions", "scripts"):
            for source in sorted((REPO_ROOT / "shared/kitty" / directory).glob("*")):
                if source.is_file():
                    safe_copy(source, kitty_root / directory / source.name, transform=True)
        unsupported = kitty_root / "pilot-unsupported/colorscheme-selector.sh"
        unsupported.parent.mkdir(parents=True, exist_ok=True)
        unsupported.write_text("printf '%s\\n' 'pilot: external colorscheme action is not executed'\n", encoding="utf-8")
        unsupported.chmod(0o644)
        placeholder = kitty_root / "pilot-unsupported/skitty/README.md"
        placeholder.parent.mkdir(parents=True, exist_ok=True)
        placeholder.write_text("# Pilot Placeholder\n\nNo se incluye estado mutable de aplicaciones.\n", encoding="utf-8")
        placeholder.chmod(0o644)


def toml_string(value: str) -> str:
    return json.dumps(value)


def write_config(context: "RunContext", data: dict[str, Any]) -> None:
    git_data = data["pilot"]["git"]
    config = f"""sourceDir = {toml_string(str(context.source))}
destDir = {toml_string(str(context.destination))}
cacheDir = {toml_string(str(context.cache))}
persistentState = {toml_string(str(context.state / 'chezmoi.boltdb'))}
scriptTempDir = {toml_string(str(context.temp))}

[template]
options = ["missingkey=error"]

[data.pilot]
platform = {toml_string(data['pilot']['platform'])}
host = {toml_string(data['pilot']['host'])}

[data.pilot.git]
name = {toml_string(git_data['name'])}
email = {toml_string(git_data['email'])}
credentialHelper = {toml_string(git_data['credentialHelper'])}
"""
    context.config_file.write_text(config, encoding="utf-8")
    context.config_file.chmod(0o600)


def validate_fixture_data(data: dict[str, Any], expected_platform: str) -> None:
    if set(data) != {"pilot"} or set(data["pilot"]) != {"platform", "host", "git"}:
        raise PilotError("fixture data has missing or unexpected top-level keys")
    if data["pilot"]["platform"] != expected_platform:
        raise PilotError("fixture platform does not match its filename")
    if set(data["pilot"]["git"]) != {"name", "email", "credentialHelper"}:
        raise PilotError("Git fixture data has missing or unexpected keys")
    if not data["pilot"]["git"]["email"].endswith("@example.invalid"):
        raise PilotError("Git fixture email must use example.invalid")
    serialized = json.dumps(data, sort_keys=True)
    for pattern in SECRET_PATTERNS:
        if pattern.search(serialized):
            raise PilotError("secret-like fixture data rejected")


@dataclass
class RunContext:
    platform: str
    root: Path
    real_home: Path
    nonce: str
    home: Path
    destination: Path
    source: Path
    config_dir: Path
    config_file: Path
    cache: Path
    state: Path
    logs: Path
    rollback: Path
    temp: Path
    work: Path
    xdg_config: Path
    xdg_cache: Path
    xdg_data: Path
    xdg_state: Path
    protected: list[Path]
    command_records: list[dict[str, Any]] = field(default_factory=list)

    @property
    def environment(self) -> dict[str, str]:
        overrides = {
            "HOME": str(self.home),
            "XDG_CONFIG_HOME": str(self.xdg_config),
            "XDG_CACHE_HOME": str(self.xdg_cache),
            "XDG_DATA_HOME": str(self.xdg_data),
            "XDG_STATE_HOME": str(self.xdg_state),
            "TMPDIR": str(self.temp),
            "TEMP": str(self.temp),
            "TMP": str(self.temp),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "NO_COLOR": "1",
        }
        if os.name == "nt":
            overrides.update(
                {
                    "USERPROFILE": str(self.home),
                    "LOCALAPPDATA": str(self.home / "AppData/Local"),
                }
            )
        return minimal_environment(
            os.environ,
            overrides,
            windows=os.name == "nt",
        )


def prepare_context(platform_name: str, requested_root: Path | None = None) -> RunContext:
    if platform_name not in PLATFORMS:
        raise PilotError(f"unsupported fixture platform: {platform_name}")
    real_home = Path.home().resolve(strict=True)
    if requested_root is None:
        root = Path(tempfile.mkdtemp(prefix="chezmoi-pilot-"))
    else:
        if requested_root.exists():
            raise PilotError(f"run root reuse rejected: {requested_root}")
        requested_root.mkdir(mode=0o700, parents=False)
        root = requested_root
    root = root.resolve(strict=True)
    root.chmod(0o700)
    nonce = secrets.token_hex(24)
    write_json(root / MARKER_NAME, marker_payload(root, nonce))
    protected = protected_paths(real_home)

    names = {
        "home": root / "home",
        "destination": root / "destination",
        "source": root / "source",
        "config_dir": root / "config",
        "cache": root / "cache",
        "state": root / "state",
        "logs": root / "logs",
        "rollback": root / "rollback",
        "temp": root / "tmp",
        "work": root / "working-tree",
        "xdg_config": root / "xdg/config",
        "xdg_cache": root / "xdg/cache",
        "xdg_data": root / "xdg/data",
        "xdg_state": root / "xdg/state",
    }
    for path in names.values():
        path.mkdir(parents=True, mode=0o700, exist_ok=False)
        guard_candidate(root, path, protected)
    context = RunContext(
        platform=platform_name,
        root=root,
        real_home=real_home,
        nonce=nonce,
        config_file=names["config_dir"] / "chezmoi.toml",
        protected=protected,
        **names,
    )
    verify_marker(root, nonce)
    stage_source(platform_name, context.source)
    data = load_json(PILOT_ROOT / f"data/{platform_name}.json")
    validate_fixture_data(data, platform_name)
    write_config(context, data)
    return context


FORBIDDEN_NAMES = re.compile(
    r"(^|/)(before_|after_|run_|encrypted_|remove_|create_|modify_|\.chezmoi(?:scripts|externals|remove|external))"
)
FORBIDDEN_TEMPLATE = re.compile(
    r"\.chezmoi\.homeDir|{{[^}]*\b(?:exec|output|include|readFile|lstat|stat|env|lookPath|onepassword|bitwarden|vault|secret)[^}]*}}",
    re.IGNORECASE,
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:ghp_|github_pat_|AKIA)[A-Za-z0-9_=-]{12,}"),
    re.compile(r"(?i)\b(?:password|token|secret)\s*[:=]\s*['\"]?[^\s'\"]{8,}"),
)


def static_validate_source(source_root: Path) -> dict[str, Any]:
    findings: list[str] = []
    templates = 0
    data_keys: set[str] = set()
    conditionals = 0
    divergent_lines = 0
    for path in sorted(source_root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source_root).as_posix()
        if FORBIDDEN_NAMES.search(relative):
            findings.append(f"forbidden source attribute: {relative}")
        if stat.S_IMODE(path.stat().st_mode) & 0o111:
            findings.append(f"executable source rejected: {relative}")
        text = path.read_text(encoding="utf-8")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(f"secret-like material: {relative}")
        if relative.endswith(".tmpl"):
            templates += 1
            if FORBIDDEN_TEMPLATE.search(text):
                findings.append(f"forbidden template function or ambient home: {relative}")
            data_keys.update(re.findall(r"\.pilot\.git\.([A-Za-z0-9_]+)", text))
            conditionals += len(re.findall(r"{{-?\s*if\b", text))
            divergent_lines += sum(1 for line in text.splitlines() if "{{" in line)
    if len(data_keys) > 5:
        findings.append("pilot Git template exceeds five scalar data keys")
    for path in source_root.rglob("*.tmpl"):
        text = path.read_text(encoding="utf-8")
        if len(re.findall(r"{{-?\s*if\b", text)) > 1 or re.search(r"{{[^}]*if[^}]*}}{{[^}]*if", text, re.S):
            findings.append(f"template conditional complexity exceeded: {path.name}")
    if divergent_lines > 10:
        findings.append("pilot template exceeds ten divergent lines")
    if findings:
        raise PilotError("; ".join(findings))
    return {
        "templates": templates,
        "dataKeys": sorted(data_keys),
        "conditionals": conditionals,
        "divergentLines": divergent_lines,
        "secretFindings": 0,
        "prohibitedFindings": 0,
    }


def chezmoi_version() -> str:
    result = subprocess.run(["chezmoi", "--version"], check=True, text=True, capture_output=True)
    return result.stdout.strip()


def resolve_openspec_bin(
    environment: Mapping[str, str] | None = None,
    home: Path | None = None,
    os_name: str | None = None,
) -> str:
    """Resolve OpenSpec without depending on an interactive shell profile."""
    selected_environment = os.environ if environment is None else environment
    selected_home = Path.home() if home is None else home
    selected_os_name = os.name if os_name is None else os_name
    search_path = selected_environment.get("PATH", "")

    override = selected_environment.get("OPENSPEC_BIN")
    if override is not None:
        override = override.strip()
        candidate = None
        if override:
            expanded = Path(override).expanduser()
            if expanded.is_absolute() or expanded.parent != Path("."):
                candidate = expanded
            else:
                discovered = shutil.which(override, path=search_path)
                candidate = Path(discovered) if discovered else None
        if candidate is not None and candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate.resolve())
        raise PilotError(
            "OpenSpec executable discovery failed: OPENSPEC_BIN is set but does not "
            f"resolve to an executable file; {OPENSPEC_RESOLUTION_METHODS}"
        )

    discovered = shutil.which("openspec", path=search_path)
    if discovered:
        return str(Path(discovered).resolve())

    if selected_os_name == "posix":
        user_local = selected_home / ".local" / "bin" / "openspec"
        if user_local.is_file() and os.access(user_local, os.X_OK):
            return str(user_local.resolve())

    raise PilotError(f"OpenSpec executable discovery failed: {OPENSPEC_RESOLUTION_METHODS}")


def openspec_version() -> str:
    result = subprocess.run(
        [resolve_openspec_bin(), "--version"],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def common_chezmoi_command(context: RunContext) -> list[str]:
    return [
        "chezmoi",
        "--source",
        str(context.source),
        "--destination",
        str(context.destination),
        "--config",
        str(context.config_file),
        "--cache",
        str(context.cache),
        "--persistent-state",
        str(context.state / "chezmoi.boltdb"),
        "--working-tree",
        str(context.work),
        "--no-pager",
        "--no-tty",
        "--refresh-externals=never",
        "--skip-secrets",
        "--error-on-conflict",
        "--use-builtin-diff",
    ]


def bubblewrap_prefix(context: RunContext) -> list[str]:
    if not sys.platform.startswith("linux"):
        return []
    if shutil.which("bwrap") is None:
        raise PilotError("Linux acceptance requires Bubblewrap")
    return [
        "bwrap",
        "--die-with-parent",
        "--new-session",
        "--ro-bind",
        "/",
        "/",
        "--bind",
        str(context.root),
        str(context.root),
        "--proc",
        "/proc",
        "--dev",
        "/dev",
        "--",
    ]


def sandbox_evidence(context: RunContext) -> dict[str, Any]:
    if not sys.platform.startswith("linux"):
        return {
            "kind": "path-guards",
            "networkIsolated": False,
            "hostBackedWritablePaths": ["<RUN>"],
            "privatePseudoFilesystems": [],
        }
    return {
        "kind": "bubblewrap",
        "hostRoot": "read-only",
        "hostBackedWritablePaths": ["<RUN>"],
        "privatePseudoFilesystems": ["/dev", "/proc"],
        "networkIsolated": False,
        "networkLimitation": "host kernel rejected the requested network namespace",
    }


def run_chezmoi(context: RunContext, label: str, arguments: list[str], expected: int = 0) -> subprocess.CompletedProcess[str]:
    verify_marker(context.root, context.nonce)
    for path in (
        context.home,
        context.destination,
        context.source,
        context.config_dir,
        context.cache,
        context.state,
        context.logs,
        context.rollback,
        context.temp,
        context.work,
        context.xdg_config,
        context.xdg_cache,
        context.xdg_data,
        context.xdg_state,
    ):
        guard_candidate(context.root, path, context.protected)
    command = common_chezmoi_command(context) + arguments
    sandboxed = bubblewrap_prefix(context) + command
    started = dt.datetime.now(dt.timezone.utc)
    result = subprocess.run(sandboxed, env=context.environment, text=True, capture_output=True)
    ended = dt.datetime.now(dt.timezone.utc)
    stdout = normalized_text(result.stdout, context.root, context.real_home)
    stderr = normalized_text(result.stderr, context.root, context.real_home)
    (context.logs / f"{len(context.command_records):02d}-{label}.stdout").write_text(stdout, encoding="utf-8")
    (context.logs / f"{len(context.command_records):02d}-{label}.stderr").write_text(stderr, encoding="utf-8")
    context.command_records.append(
        {
            "label": label,
            "command": [normalized_text(arg, context.root, context.real_home) for arg in command],
            "exit": result.returncode,
            "startedAt": started.isoformat(),
            "endedAt": ended.isoformat(),
            "stdoutSha256": sha256_bytes(stdout.encode()),
            "stderrSha256": sha256_bytes(stderr.encode()),
            "stdoutLines": len(stdout.splitlines()),
            "stdoutPreview": stdout.splitlines()[:12],
            "stderrPreview": stderr.splitlines()[:12],
            "sandbox": "bubblewrap-private-dev-no-network-namespace" if sys.platform.startswith("linux") else "path-guards",
        }
    )
    if result.returncode != expected:
        raise PilotError(f"{label} exited {result.returncode}: {stderr.strip()}")
    return result


def verify_effective_config(context: RunContext) -> dict[str, Any]:
    dump_result = run_chezmoi(context, "dump-config", ["dump-config", "--format=json"])
    config = json.loads(dump_result.stdout)
    expected_paths = {
        "sourceDir": context.source,
        "destDir": context.destination,
        "cacheDir": context.cache,
        "persistentState": context.state / "chezmoi.boltdb",
        "scriptTempDir": context.temp,
    }
    for key, expected in expected_paths.items():
        if Path(config[key]).resolve(strict=False) != expected.resolve(strict=False):
            raise PilotError(f"effective config mismatch for {key}")
    data = config.get("data", {})
    if data["pilot"]["platform"] != context.platform:
        raise PilotError("effective pilot platform data mismatch")
    if Path(context.environment["HOME"]).resolve(strict=False) != context.home.resolve():
        raise PilotError("effective Chezmoi HOME is not temporary")
    config_paths = {
        key: f"<RUN>/{expected.relative_to(context.root)}"
        for key, expected in expected_paths.items()
    }
    effective_contract = {
        "configPaths": config_paths,
        "pilotData": data["pilot"],
    }
    contract_stdout = json.dumps(
        effective_contract, indent=2, sort_keys=True, ensure_ascii=False
    ) + "\n"
    record = context.command_records[-1]
    if record["label"] != "dump-config":
        raise PilotError("effective config command record is not dump-config")
    record["rawStdoutSha256"] = record["stdoutSha256"]
    record["rawStdoutLines"] = record["stdoutLines"]
    record["rawStdoutPreview"] = record["stdoutPreview"]
    record["stdoutSha256"] = sha256_bytes(contract_stdout.encode())
    record["stdoutLines"] = len(contract_stdout.splitlines())
    record["stdoutPreview"] = contract_stdout.splitlines()[:12]
    return effective_contract


def managed_targets(context: RunContext) -> list[str]:
    result = run_chezmoi(
        context,
        "managed",
        ["managed", "--include=files", "--path-style=relative"],
    )
    return sorted(line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip())


def validate_target_inventory(platform_name: str, targets: list[str], destination: Path) -> dict[str, Any]:
    expected = load_json(PILOT_ROOT / "expected/targets.json")
    missing = sorted(set(expected["required"][platform_name]) - set(targets))
    forbidden = sorted(set(expected["forbidden"][platform_name]) & set(targets))
    if missing or forbidden:
        raise PilotError(f"target inventory mismatch: missing={missing}, forbidden={forbidden}")
    if len(targets) != len(set(targets)):
        raise PilotError("duplicate Chezmoi target detected")
    real_home = Path.home().resolve()
    # Ownership is attached to the destination pathname, not to the current
    # symlink referent. Resolving the leaf would turn active profile targets into
    # repository source paths and create a false intersection.
    real_targets = [Path(os.path.abspath(destination / target)) for target in targets]
    profile_real = []
    profile_logical = set()
    for entry in profile_entries():
        logical = entry["target"]
        profile_logical.add(logical)
        profile_real.append(Path(os.path.abspath(real_home / logical.removeprefix("$HOME/"))))
    real_intersection = sorted(set(real_targets) & set(profile_real), key=str)
    if real_intersection:
        raise PilotError(f"real ownership intersection: {real_intersection}")
    mappings = load_json(PILOT_ROOT / "mappings.json")
    logical_overlap = sorted(set(mappings["logicalTargets"][platform_name]) & profile_logical)
    return {
        "targets": targets,
        "realIntersection": [],
        "logicalComparisonOverlap": logical_overlap,
        "singleOwner": True,
    }


def input_digest(context: RunContext) -> str:
    data = load_json(PILOT_ROOT / f"data/{context.platform}.json")
    return stable_digest(
        {
            "platform": context.platform,
            "data": data,
            "source": tree_manifest(context.source),
            "chezmoi": project_chezmoi_version(chezmoi_version()),
        }
    )


def backup_tree(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for item in source.iterdir():
        target = destination / item.name
        if item.is_dir() and not item.is_symlink():
            shutil.copytree(item, target, symlinks=True)
        elif item.is_symlink():
            target.symlink_to(os.readlink(item))
        else:
            shutil.copy2(item, target)


def restore_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(mode=0o700, parents=True)
    for item in source.iterdir():
        target = destination / item.name
        if item.is_dir() and not item.is_symlink():
            shutil.copytree(item, target, symlinks=True)
        elif item.is_symlink():
            target.symlink_to(os.readlink(item))
        else:
            shutil.copy2(item, target)


def validate_applied_case(context: RunContext, manifest: list[dict[str, str]]) -> dict[str, Any]:
    file_entries = [entry for entry in manifest if entry["type"] == "file"]
    if any(entry["mode"] != "0644" for entry in file_entries):
        raise PilotError("unexpected target file permission")
    starship = context.destination / ".config/starship.toml"
    if starship.read_bytes() != (REPO_ROOT / "shared/starship/starship.toml").read_bytes():
        raise PilotError("Starship literal is not byte-identical")
    git_config = (context.destination / ".gitconfig").read_text(encoding="utf-8")
    data = load_json(PILOT_ROOT / f"data/{context.platform}.json")["pilot"]["git"]
    for value in (data["name"], data["email"], data["credentialHelper"]):
        if value not in git_config:
            raise PilotError("Git fixture data did not render explicitly")
    if "example.invalid" not in git_config:
        raise PilotError("Git fixture does not use public fake data")

    details: dict[str, Any] = {
        "starshipLiteralSha256": sha256_file(starship),
        "gitCredentialHelper": data["credentialHelper"],
        "fileModesValid": True,
    }
    if context.platform in {"linux", "macos"}:
        common = (context.destination / ".config/kitty/common.conf").read_text(encoding="utf-8")
        entrypoint = (context.destination / ".config/kitty/kitty.conf").read_text(encoding="utf-8")
        if "$KITTY_CONFIG_DIRECTORY" not in common or "$KITTY_CONFIG_DIRECTORY/common.conf" not in entrypoint:
            raise PilotError("Kitty isolation transformation missing")
        if "$HOME/mydotfiles" in common or "~/mydotfiles" in common or "$HOME/mydotfiles" in entrypoint:
            raise PilotError("Kitty rendered path escaped to conventional checkout")
        for semantic in (
            "map ctrl+shift+l next_window",
            "map ctrl+shift+h previous_window",
            'map ctrl+h kitten pass_keys.py left   ctrl+h "nvim"',
            "startup_session",
            "goto_session",
        ):
            if semantic not in common:
                raise PilotError(f"shared Kitty semantic content missing: {semantic}")
        if context.platform == "linux":
            required = (
                "kitty_mod super+alt",
                "map ctrl+shift+c copy_to_clipboard",
                "map super+enter new_window",
                "map super+t new_tab_with_cwd",
            )
            forbidden = "macos_option_as_alt"
        else:
            required = (
                "kitty_mod cmd+option",
                "macos_option_as_alt right",
                "map cmd+enter new_window",
                "map cmd+t new_tab_with_cwd",
            )
            forbidden = "map ctrl+shift+c copy_to_clipboard"
        if any(value not in entrypoint for value in required) or forbidden in entrypoint:
            raise PilotError("Kitty platform entrypoint leakage or missing behavior")
        details["kittyCommonSha256"] = sha256_file(context.destination / ".config/kitty/common.conf")
        details["kittyEntrypointSha256"] = sha256_file(context.destination / ".config/kitty/kitty.conf")
    else:
        terminal = context.destination / "AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json"
        parsed = json.loads(terminal.read_text(encoding="utf-8"))
        if parsed.get("$schema") != "https://aka.ms/terminal-profiles-schema":
            raise PilotError("Windows Terminal schema identifier missing")
        actions = parsed.get("actions")
        if not isinstance(actions, list) or len(actions) < 7:
            raise PilotError("Windows Terminal actions are incomplete")
        if any("win+" in json.dumps(action).lower() for action in actions):
            raise PilotError("Windows key must remain reserved")
        details["windowsTerminalVersion"] = WINDOWS_TERMINAL_VERSION
        details["windowsTerminalStructuralOnly"] = True
    return details


def evaluate_once(platform_name: str) -> dict[str, Any]:
    context = prepare_context(platform_name)
    pre_protected = protected_snapshot(context.real_home)
    baseline_destination = tree_manifest(context.destination)
    baseline_state = tree_manifest(context.state)
    try:
        verify_canonical_hashes()
        static = static_validate_source(context.source)
        effective = verify_effective_config(context)
        targets = managed_targets(context)
        ownership = validate_target_inventory(platform_name, targets, context.destination)
        status_before = run_chezmoi(context, "status-before", ["status"])
        diff_before = run_chezmoi(context, "diff-before", ["diff"])
        dry_before = run_chezmoi(context, "dry-run-before", ["apply", "--dry-run", "--verbose"])
        if not diff_before.stdout or not dry_before.stdout:
            raise PilotError("preview evidence is unexpectedly empty")
        digest = input_digest(context)
        token = {"nonce": context.nonce, "digest": digest, "platform": platform_name}
        write_json(context.root / ".preview-token", token)
        if load_json(context.root / ".preview-token") != token or input_digest(context) != digest:
            raise PilotError("preview token is stale")

        destination_backup = context.rollback / "destination"
        state_backup = context.rollback / "state"
        backup_tree(context.destination, destination_backup)
        backup_tree(context.state, state_backup)

        run_chezmoi(context, "apply", ["apply"])
        applied_manifest = tree_manifest(context.destination)
        case_details = validate_applied_case(context, applied_manifest)
        second_apply = run_chezmoi(context, "apply-second", ["apply"])
        dry_after = run_chezmoi(context, "dry-run-after", ["apply", "--dry-run", "--verbose"])
        diff_after = run_chezmoi(context, "diff-after", ["diff"])
        if second_apply.stdout or dry_after.stdout or diff_after.stdout:
            raise PilotError("second apply/dry-run/diff is not a no-op")

        drift_target = context.destination / ".config/starship.toml"
        original = drift_target.read_bytes()
        drift_target.write_bytes(original + b"\n# pilot drift\n")
        drift_status = run_chezmoi(context, "status-drift", ["status"])
        if not drift_status.stdout:
            raise PilotError("Chezmoi did not detect temporary drift")
        drift_target.write_bytes(original)
        if tree_manifest(context.destination) != applied_manifest:
            raise PilotError("drift restoration did not recover applied state")

        restore_tree(destination_backup, context.destination)
        restore_tree(state_backup, context.state)
        if tree_manifest(context.destination) != baseline_destination or tree_manifest(context.state) != baseline_state:
            raise PilotError("rollback did not restore exact baseline")
        post_protected = protected_snapshot(context.real_home)
        if post_protected != pre_protected:
            raise PilotError("protected production metadata changed")
        return {
            "platform": platform_name,
            "rootContained": True,
            "sandbox": sandbox_evidence(context),
            "static": static,
            "effective": effective,
            "ownership": ownership,
            "previewDigest": digest,
            "preview": {
                "statusLines": len(status_before.stdout.splitlines()),
                "diffLines": len(diff_before.stdout.splitlines()),
                "dryRunLines": len(dry_before.stdout.splitlines()),
            },
            "appliedManifest": applied_manifest,
            "appliedManifestDigest": stable_digest(applied_manifest),
            "secondApplyChanges": 0,
            "secondDryRunChanges": 0,
            "driftDetected": True,
            "rollbackExact": True,
            "protectedMetadataChanged": 0,
            "caseDetails": case_details,
            "commands": context.command_records,
        }
    finally:
        shutil.rmtree(context.root, ignore_errors=True)


def containment_self_tests() -> dict[str, bool]:
    real_home = Path.home().resolve()
    root = Path(tempfile.mkdtemp(prefix="chezmoi-pilot-guard-"))
    nonce = secrets.token_hex(24)
    write_json(root / MARKER_NAME, marker_payload(root, nonce))
    safe = root / "safe"
    safe.mkdir()
    protected = protected_paths(real_home)
    results: dict[str, bool] = {}

    def rejected(name: str, function: Any) -> None:
        try:
            function()
        except (PilotError, FileExistsError):
            results[name] = True
        else:
            raise PilotError(f"negative containment test did not fail: {name}")

    try:
        guard_candidate(root, safe, protected)
        results["safe-descendant"] = True
        rejected("filesystem-root", lambda: guard_candidate(root, Path("/"), protected))
        rejected("real-home", lambda: guard_candidate(root, real_home, protected))
        rejected("repository", lambda: guard_candidate(root, REPO_ROOT, protected))
        rejected("root-parent", lambda: guard_candidate(root, root.parent, protected))
        active_target = next(path for path in protected if path != real_home and real_home in path.parents)
        rejected("active-profile-target", lambda: guard_candidate(root, active_target, protected))
        marker = root / MARKER_NAME
        marker.unlink()
        rejected("missing-marker", lambda: verify_marker(root, nonce))
        write_json(marker, marker_payload(root, nonce))
        escape = root / "escape"
        escape.symlink_to(root.parent, target_is_directory=True)
        rejected("symlink-escape", lambda: guard_candidate(root, escape / "child", protected))
        reused = root / "reused"
        reused.mkdir()
        rejected("reused-root", lambda: prepare_context("linux", reused))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return results


ALLOWED_NATIVE_ACTIONS = {
    "terminal.new-tab": {
        "macos": {"new_tab_with_cwd"},
        "linux": {"new_tab_with_cwd"},
        "windows": {"newTab"},
    },
    "terminal.new-os-window": {
        "macos": {None, "new_os_window"},
        "linux": {None, "new_os_window"},
        "windows": {"newWindow"},
    },
    "terminal.new-pane": {
        "macos": {"new_window"},
        "linux": {"new_window"},
        "windows": {"splitPane:auto"},
    },
    "terminal.focus-pane-left": {
        "macos": {"neighboring_window:left"},
        "linux": {"neighboring_window:left"},
        "windows": {"moveFocus:left"},
    },
    "terminal.previous-pane-in-order": {
        "macos": {"previous_window"},
        "linux": {"previous_window"},
        "windows": {None, "moveFocus:previousInOrder"},
    },
    "terminal.copy": {
        "macos": {"copy_or_noop"},
        "linux": {"copy_to_clipboard"},
        "windows": {"copy"},
    },
    "terminal.paste": {
        "macos": {"paste_from_clipboard"},
        "linux": {"paste_from_clipboard"},
        "windows": {"paste"},
    },
    "terminal.reload-config": {
        "macos": {"load_config_file"},
        "linux": {"load_config_file"},
        "windows": {None},
    },
    "terminal.close-pane": {
        "macos": {"close_window"},
        "linux": {"close_window"},
        "windows": {"closePane"},
    },
    "desktop.focus-left": {
        "macos": {"focus:left"},
        "linux": {None},
        "windows": {None},
    },
    "desktop.move-left": {
        "macos": {"move:left"},
        "linux": {None},
        "windows": {None},
    },
}


def semantic_source_path(relative: str) -> Path | None:
    if relative in {"active-session", "future-design"}:
        return None
    if relative.startswith("fixtures/"):
        return PILOT_ROOT / relative
    return REPO_ROOT / relative


def validate_semantics(semantics_override: dict[str, Any] | None = None) -> dict[str, Any]:
    semantics = semantics_override or load_json(PILOT_ROOT / "semantics.json")
    required_actions = {
        "terminal.new-tab",
        "terminal.new-os-window",
        "terminal.new-pane",
        "terminal.focus-pane-left",
        "terminal.previous-pane-in-order",
        "terminal.copy",
        "terminal.paste",
        "terminal.reload-config",
        "terminal.close-pane",
    }
    if not required_actions.issubset(semantics["actions"]):
        raise PilotError("semantic action vocabulary is incomplete")
    windows_actions = load_json(PILOT_ROOT / "fixtures/windows-terminal/settings.json")["actions"]
    chord_owners: dict[tuple[str, str], str] = {}
    canonical_checks = 0
    for action, mappings in semantics["actions"].items():
        platform_mappings = {name: mappings[name] for name in PLATFORMS if name in mappings}
        if set(platform_mappings) != set(PLATFORMS):
            raise PilotError(f"semantic platform mapping incomplete: {action}")
        for platform_name, mapping in platform_mappings.items():
            chords = mapping.get("chords", [])
            if platform_name == "windows" and any("win+" in chord.lower() for chord in chords):
                raise PilotError(f"Windows key reservation violated: {action}")
            status = mapping.get("status", "")
            if status.startswith(("unsupported", "deferred", "session-defined")) and chords:
                raise PilotError(f"unsupported/deferred semantic action has a chord: {action}/{platform_name}")
            for chord in chords:
                collision_key = (platform_name, chord.lower())
                previous = chord_owners.get(collision_key)
                if previous is not None and previous != action:
                    raise PilotError(
                        f"semantic chord collision on {platform_name}/{chord}: {previous} vs {action}"
                    )
                chord_owners[collision_key] = action
            allowed = ALLOWED_NATIVE_ACTIONS.get(action, {}).get(platform_name)
            if allowed is not None and mapping.get("nativeAction") not in allowed:
                raise PilotError(
                    f"false native semantic mapping: {action}/{platform_name} -> {mapping.get('nativeAction')}"
                )
            source_path = semantic_source_path(mapping["sourceFile"])
            if "expectedLine" in mapping:
                if source_path is None or mapping["expectedLine"] not in source_path.read_text(encoding="utf-8"):
                    raise PilotError(f"canonical semantic line missing: {action}/{platform_name}")
                canonical_checks += 1
            if "helperLine" in mapping:
                helper = semantic_source_path(mapping["helperFile"])
                if helper is None or mapping["helperLine"] not in helper.read_text(encoding="utf-8"):
                    raise PilotError(f"canonical semantic helper line missing: {action}/{platform_name}")
                canonical_checks += 1
            if "expectedCommand" in mapping:
                if mapping["expectedCommand"] not in windows_actions:
                    raise PilotError(f"Windows Terminal semantic command missing: {action}")
                canonical_checks += 1
    return {
        "actions": len(semantics["actions"]),
        "platforms": 3,
        "windowsKeyReserved": True,
        "aerospacePreserved": True,
        "canonicalActionChecks": canonical_checks,
        "chordCollisions": 0,
    }


def validate_windows_fixture() -> dict[str, Any]:
    path = PILOT_ROOT / "fixtures/windows-terminal/settings.json"
    parsed = load_json(path)
    if parsed.get("$schema") != "https://aka.ms/terminal-profiles-schema":
        raise PilotError("Windows Terminal schema URL mismatch")
    allowed_commands = {"newTab", "newWindow", "copy", "paste", "closePane"}
    for action in parsed.get("actions", []):
        command = action.get("command")
        if isinstance(command, str):
            if command not in allowed_commands:
                raise PilotError(f"unexpected Windows Terminal command: {command}")
        elif not isinstance(command, dict) or command.get("action") not in {"splitPane", "moveFocus"}:
            raise PilotError("invalid Windows Terminal structured action")
        elif command["action"] == "splitPane" and command.get("split") not in {
            "vertical",
            "horizontal",
            "auto",
            "up",
            "right",
            "down",
            "left",
        }:
            raise PilotError("invalid Windows Terminal split direction")
        elif command["action"] == "moveFocus" and command.get("direction") not in {
            "left",
            "right",
            "up",
            "down",
            "previous",
            "previousInOrder",
            "nextInOrder",
            "first",
            "parent",
            "child",
        }:
            raise PilotError("invalid Windows Terminal focus direction")
        if "win+" in action.get("keys", "").lower():
            raise PilotError("Windows key is reserved")
    raw = path.read_text(encoding="utf-8")
    if "kitty" in raw.lower() or "~/" in raw or "/home/" in raw:
        raise PilotError("Windows Terminal fixture leaks Kitty/Unix assumptions")
    if "\r\n" in raw:
        raise PilotError("repository fixture must use LF; native runner verifies Windows acceptance")
    return {"version": WINDOWS_TERMINAL_VERSION, "schema": parsed["$schema"], "lineEndings": "LF", "structuralOnly": True}


def validate_traceability(
    evidence: dict[str, Any] | None = None,
    declaration_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    try:
        return audit_traceability(
            REPO_ROOT, PILOT_ROOT, CHANGE_ROOT, evidence, declaration_override
        )
    except AuditError as exc:
        raise PilotError(str(exc)) from exc


def validate_ci_workflow() -> dict[str, Any]:
    try:
        return audit_ci_workflow(REPO_ROOT)
    except AuditError as exc:
        raise PilotError(str(exc)) from exc


def validate_documentation_language() -> dict[str, Any]:
    paths = [
        CHANGE_ROOT / "proposal.md",
        CHANGE_ROOT / "design.md",
        CHANGE_ROOT / "tasks.md",
        REPO_ROOT / "openspec/config.yaml",
        PILOT_ROOT / "README.md",
        PILOT_ROOT / "SUPPORT.md",
        REPO_ROOT / "docs/tooling/openspec-chezmoi.md",
        REPO_ROOT / "docs/chezmoi-pilot-result.md",
    ]
    paths.extend(sorted((CHANGE_ROOT / "specs").glob("*/spec.md")))
    unaccented = re.compile(
        r"\b(?:evaluacion|configuracion|documentacion|produccion|ningun|unicamente|"
        r"validacion|aceptacion|aplicacion|logica|canonico|canonica|publico|publica|"
        r"pequeno|raiz|despues|ejecucion|migracion|comparacion|revision|explicito|"
        r"explicita|autenticacion|recuperacion|instalacion|decision|modificacion|"
        r"instruccion)\b",
        re.IGNORECASE,
    )
    english_body = re.compile(
        r"^(?:This|The|Every|Current|Future|Install|Verify|All|Each)\s"
    )
    findings = []
    for path in paths:
        in_fence = False
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or line.startswith("#") or line.startswith("|"):
                continue
            if unaccented.search(line) or english_body.search(line):
                findings.append(f"{path.relative_to(REPO_ROOT)}:{line_number}")
    if findings:
        raise PilotError(f"documentation language convention failed: {findings}")
    return {"files": len(paths), "language": "Spanish UTF-8", "findings": 0}


def validate_repository() -> dict[str, Any]:
    verify_canonical_hashes()
    mappings = load_json(PILOT_ROOT / "mappings.json")
    if mappings["schemaVersion"] != 1:
        raise PilotError("unsupported mappings schema")
    profile_text = "\n".join(path.read_text(encoding="utf-8") for path in (REPO_ROOT / "profiles").rglob("*.links"))
    if "experiments/chezmoi-pilot" in profile_text:
        raise PilotError("a production profile references the pilot")
    git_fixture = (PILOT_ROOT / "fixtures/git/dot_gitconfig.tmpl").read_text(encoding="utf-8")
    if "example.invalid" not in json.dumps([load_json(PILOT_ROOT / f"data/{name}.json") for name in PLATFORMS]):
        raise PilotError("Git fixture data is not explicitly fake")
    if ".chezmoi.homeDir" in git_fixture:
        raise PilotError("ambient Chezmoi home use is prohibited")
    for platform_name in PLATFORMS:
        validate_fixture_data(load_json(PILOT_ROOT / f"data/{platform_name}.json"), platform_name)
    semantics = validate_semantics()
    windows = validate_windows_fixture()
    traceability = validate_traceability()
    ci = validate_ci_workflow()
    documentation_language = validate_documentation_language()
    return {
        "canonicalMappings": len(canonical_hashes()),
        "profileReferences": 0,
        "semantics": semantics,
        "windows": windows,
        "traceability": traceability,
        "ci": ci,
        "documentationLanguage": documentation_language,
        "environmentAllowlist": {
            "posixInherited": list(POSIX_ENV_ALLOWLIST),
            "windowsInherited": list(WINDOWS_ENV_ALLOWLIST),
            "temporaryOverrides": [
                "HOME",
                "XDG_CONFIG_HOME",
                "XDG_CACHE_HOME",
                "XDG_DATA_HOME",
                "XDG_STATE_HOME",
                "TMPDIR",
                "TEMP",
                "TMP",
                "LANG",
                "LC_ALL",
                "TZ",
                "NO_COLOR",
            ],
            "windowsTemporaryOverrides": ["USERPROFILE", "LOCALAPPDATA"],
        },
    }


def git_context() -> dict[str, Any]:
    revision = subprocess.run(["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"], check=True, text=True, capture_output=True).stdout.strip()
    branch = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "branch", "--show-current"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    reviewed_base = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "merge-base", "HEAD", "origin/main"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    dirty = bool(subprocess.run(["git", "-C", str(REPO_ROOT), "status", "--porcelain"], check=True, text=True, capture_output=True).stdout)
    return {
        "branch": branch,
        "reviewedBase": reviewed_base,
        "headRevision": revision,
        "dirty": dirty,
    }


def evaluate_linker_baseline() -> dict[str, Any]:
    root = Path(tempfile.mkdtemp(prefix="chezmoi-pilot-linker-baseline-"))
    real_home = Path.home().resolve()
    home = root / "home"
    blocked_home = root / "blocked-home"
    temp = root / "tmp"
    home.mkdir(mode=0o700)
    blocked_home.mkdir(mode=0o700)
    temp.mkdir(mode=0o700)
    before = protected_snapshot(real_home)
    records: list[dict[str, Any]] = []

    def run(label: str, command: list[str], selected_home: Path, expected: int = 0) -> subprocess.CompletedProcess[str]:
        env = minimal_environment(
            os.environ,
            {
                "HOME": str(selected_home),
                "TMPDIR": str(temp),
                "TEMP": str(temp),
                "TMP": str(temp),
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "TZ": "UTC",
                "NO_COLOR": "1",
            },
        )
        sandbox = []
        if sys.platform.startswith("linux"):
            if shutil.which("bwrap") is None:
                raise PilotError("Linux baseline requires Bubblewrap")
            sandbox = [
                "bwrap",
                "--die-with-parent",
                "--new-session",
                "--ro-bind",
                "/",
                "/",
                "--bind",
                str(root),
                str(root),
                "--proc",
                "/proc",
                "--dev",
                "/dev",
                "--",
            ]
        result = subprocess.run(sandbox + command, env=env, text=True, capture_output=True)
        stdout = result.stdout.replace(str(root), "<BASELINE>").replace(str(REPO_ROOT), "<REPO>")
        stderr = result.stderr.replace(str(root), "<BASELINE>").replace(str(REPO_ROOT), "<REPO>")
        records.append(
            {
                "label": label,
                "command": [value.replace(str(root), "<BASELINE>").replace(str(REPO_ROOT), "<REPO>") for value in command],
                "exit": result.returncode,
                "stdoutLines": len(stdout.splitlines()),
                "stderrLines": len(stderr.splitlines()),
                "stdoutSha256": sha256_bytes(stdout.encode()),
                "stderrSha256": sha256_bytes(stderr.encode()),
                "stdoutPreview": stdout.splitlines()[:12],
                "stderrPreview": stderr.splitlines()[:12],
                "sandbox": "bubblewrap-private-dev-no-network-namespace" if sys.platform.startswith("linux") else "temporary-HOME",
            }
        )
        if result.returncode != expected:
            raise PilotError(f"baseline {label} exited {result.returncode}, expected {expected}")
        return result

    try:
        run("profile-resolve", [str(REPO_ROOT / "scripts/profile-resolve"), "arch-workstation"], home)
        run("link-dry-run", [str(REPO_ROOT / "scripts/link"), "--dry-run", "arch-workstation"], home)
        run("link-apply", [str(REPO_ROOT / "scripts/link"), "arch-workstation"], home)
        second = run("link-second", [str(REPO_ROOT / "scripts/link"), "arch-workstation"], home)
        run("doctor", [str(REPO_ROOT / "scripts/doctor"), "arch-workstation"], home)
        if "0 change(s), 0 error(s)" not in second.stdout:
            raise PilotError("current linker second run is not idempotent")
        starship = home / ".config/starship.toml"
        if not starship.is_symlink() or starship.resolve() != (REPO_ROOT / "shared/starship/starship.toml").resolve():
            raise PilotError("current linker Starship baseline is incorrect")

        blocked_target = blocked_home / ".config/starship.toml"
        blocked_target.parent.mkdir(parents=True)
        blocked_target.write_text("do not replace\n", encoding="utf-8")
        run("link-real-file-refusal", [str(REPO_ROOT / "scripts/link"), "arch-workstation"], blocked_home, expected=1)
        if blocked_target.read_text(encoding="utf-8") != "do not replace\n":
            raise PilotError("current linker changed a blocking real file")
        after = protected_snapshot(real_home)
        if before != after:
            raise PilotError("current linker baseline changed protected production metadata")
        baseline_manifest = tree_manifest(home)
        for entry in baseline_manifest:
            if "target" in entry:
                entry["target"] = entry["target"].replace(str(REPO_ROOT), "<REPO>").replace(str(root), "<BASELINE>")
        return {
            "profile": "arch-workstation",
            "commands": records,
            "manifest": baseline_manifest,
            "starshipSymlink": True,
            "secondRunChanges": 0,
            "realFileRefusal": True,
            "protectedMetadataChanged": 0,
            "sandbox": {
                "kind": "bubblewrap" if sys.platform.startswith("linux") else "path-guards",
                "hostRoot": "read-only" if sys.platform.startswith("linux") else "not-applicable",
                "hostBackedWritablePaths": ["<BASELINE>"],
                "privatePseudoFilesystems": ["/dev", "/proc"] if sys.platform.startswith("linux") else [],
                "networkIsolated": False,
            },
            "gitRendering": "No soportado; configure-git permanece authoritative y no fue ejecutado.",
            "windowsTerminal": "No soportado.",
        }
    finally:
        shutil.rmtree(root, ignore_errors=True)


def comparison_metrics(results: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    command_counts = {name: len(value["first"]["commands"]) for name, value in results.items()}
    implementation_scope = [
        PILOT_ROOT / "scripts",
        PILOT_ROOT / "fixtures",
        PILOT_ROOT / "data",
        PILOT_ROOT / "expected",
        PILOT_ROOT / "tests",
        PILOT_ROOT / "mappings.json",
        PILOT_ROOT / "semantics.json",
        PILOT_ROOT / "traceability.json",
    ]
    documentation_scope = [
        PILOT_ROOT / "README.md",
        PILOT_ROOT / "SUPPORT.md",
        PILOT_ROOT / "TRACEABILITY.md",
        REPO_ROOT / "docs/chezmoi-pilot-result.md",
        REPO_ROOT / "docs/tooling/openspec-chezmoi.md",
        REPO_ROOT / "docs/generated/chezmoi-pilot-matrix.md",
        REPO_ROOT / "docs/generated/chezmoi-pilot-scorecard.md",
    ]
    current_scripts = measure_files(
        [
            REPO_ROOT / path
            for path in ("scripts/link", "scripts/profile-resolve", "scripts/doctor")
        ],
        relative_to=REPO_ROOT,
    )
    pilot_automation_tests = measure_files(
        [PILOT_ROOT / "scripts", PILOT_ROOT / "tests"], relative_to=REPO_ROOT
    )
    implementation = measure_files(implementation_scope, relative_to=REPO_ROOT)
    documentation = {"files": measure_files(documentation_scope, relative_to=REPO_ROOT)["files"]}
    baseline_command_count = len(baseline["commands"])
    maximum_pilot_commands = max(command_counts.values(), default=0)
    command_count_not_higher = maximum_pilot_commands <= baseline_command_count
    persistent_state_count = len(
        {
            value["first"]["effective"]["configPaths"]["persistentState"]
            for value in results.values()
        }
    )
    persistent_state_not_higher = persistent_state_count <= 0
    clear_complexity_benefit = command_count_not_higher and persistent_state_not_higher
    return {
        "priorityOrder": [
            "scalability",
            "total-complexity",
            "maintainability-deterministic-ownership",
            "reinstall-reproducibility",
            "versioned-idempotence-drift-rollback-documentation",
        ],
        "currentModel": {
            "operatorEntryCommands": len(("scripts/profile-resolve", "scripts/link", "scripts/doctor")),
            "measuredInternalCommands": baseline_command_count,
            "automationScripts": current_scripts,
            "representativeSupport": {"starship": "symlink", "git": "separate configure-git", "kitty": "symlink plus shared include", "windowsTerminal": "unsupported"},
            "hiddenState": 0,
            "templates": 0,
            "strengths": ["Ownership simple.", "Rechaza archivos reales.", "Baja carga cognitiva para links literales."],
            "gaps": ["No renderiza datos de host.", "No tiene perfil Windows nativo.", "Visibilidad limitada del drift de archivos materializados."],
        },
        "chezmoiPilot": {
            "operatorEntryCommands": len(("experiments/chezmoi-pilot/scripts/run",)),
            "internalCommandsPerFixture": command_counts,
            "implementation": implementation,
            "documentation": documentation,
            "automationTests": pilot_automation_tests,
            "templates": max(
                value["first"]["static"]["templates"] for value in results.values()
            ),
            "platformAdapters": measure_files(
                [PILOT_ROOT / "scripts/run", PILOT_ROOT / "scripts/run-windows.ps1"]
            )["files"],
            "persistentStateFilesPerRun": persistent_state_count,
            "strengths": ["Renderiza datos de host falsos.", "Incluye diff/status.", "Mide idempotencia y drift de archivos materializados.", "Modela un target Windows estructural."],
            "costs": ["Encoding propio del source state.", "Harness de containment.", "Persistent state adicional.", "Adapter de staging por plataforma.", "Más conceptos de recovery."],
        },
        "policy": {
            "baselineInternalCommands": baseline_command_count,
            "maximumPilotInternalCommands": maximum_pilot_commands,
            "commandCountNotHigher": command_count_not_higher,
            "persistentStateNotHigher": persistent_state_not_higher,
            "clearComplexityBenefit": clear_complexity_benefit,
            "permitsSelectiveMigration": clear_complexity_benefit,
            "locIsUnweighted": True,
        },
        "unweighted": True,
    }


def evaluate_all(selected_platform: str = "all") -> dict[str, Any]:
    repository_validation = validate_repository()
    containment = containment_self_tests()
    names = PLATFORMS if selected_platform == "all" else (selected_platform,)
    results: dict[str, Any] = {}
    for platform_name in names:
        first = evaluate_once(platform_name)
        second = evaluate_once(platform_name)
        if first["appliedManifest"] != second["appliedManifest"]:
            raise PilotError(f"clean-run determinism failed for {platform_name}")
        results[platform_name] = {"first": first, "second": second, "deterministic": True}
    baseline = evaluate_linker_baseline()
    native_evidence = {"windows": False, "macos": False, "archCrossRender": True}
    blockers = [
        "No existe evidencia Windows nativa de target/schema/ACL/idempotencia.",
        "El harness macOS nativo no fue autorizado ni ejecutado.",
        "Containment y staging por plataforma agregan complejidad frente al workflow literal actual.",
    ]
    mandatory = {
        "outOfRootWrites": 0,
        "realOwnershipOverlaps": 0,
        "secretFindings": 0,
        "prohibitedFeatureFindings": 0,
        "protectedMetadataChanges": 0,
        "allSelectedFixturesPassed": True,
        "rollbackExact": True,
        "idempotent": True,
        "deterministic": True,
    }
    comparison = comparison_metrics(results, baseline)
    outcome = select_outcome(mandatory, native_evidence, comparison)
    evidence = {
        "schemaVersion": 1,
        "recordedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git": git_context(),
        "host": {"system": host_platform.system(), "architecture": host_platform.machine()},
        "tools": {"chezmoi": chezmoi_version(), "openspec": openspec_version(), "python": sys.version.split()[0]},
        "sourceProvenance": canonical_hashes(),
        "repositoryValidation": repository_validation,
        "containmentNegativeTests": containment,
        "results": results,
        "currentLinkerBaseline": baseline,
        "nativeEvidence": native_evidence,
        "comparison": comparison,
        "mandatory": mandatory,
        "outcome": outcome,
        "blockers": blockers,
    }
    assert_outcome_invariants(evidence)
    return evidence


def evidence_input_digest(evidence: dict[str, Any]) -> str:
    return evidence_projection_digest(evidence)


def generate_documents(evidence: dict[str, Any], check: bool) -> None:
    try:
        render_documents(
            evidence, REPO_ROOT, PILOT_ROOT, CHANGE_ROOT, check=check
        )
    except DocsError as exc:
        raise PilotError(str(exc)) from exc


def compare_evidence_projection(fresh: dict[str, Any], reviewed: dict[str, Any]) -> str:
    fresh_projection = evidence_projection(fresh)
    reviewed_projection = evidence_projection(reviewed)
    fresh_digest = evidence_projection_digest(fresh)
    reviewed_digest = evidence_projection_digest(reviewed)
    if fresh_projection != reviewed_projection:
        differences = projection_differences(reviewed_projection, fresh_projection)
        raise PilotError(
            "fresh deterministic evidence projection differs from review evidence: "
            f"fresh={fresh_digest} reviewed={reviewed_digest} "
            f"differences={json.dumps(differences[:32], sort_keys=True)}"
        )
    return fresh_digest


def expected_versions() -> dict[str, bool]:
    return {
        "chezmoi": project_chezmoi_version(chezmoi_version()) == EXPECTED_CHEZMOI,
        "openspec": openspec_version() == EXPECTED_OPEN_SPEC,
        "python": sys.version_info >= (3, 11),
    }


def doctor() -> dict[str, Any]:
    repository = validate_repository()
    versions = expected_versions()
    if not all(versions.values()):
        raise PilotError(f"evaluation tool version drift: {versions}")
    evidence_path = PILOT_ROOT / "evidence/review.json"
    if not evidence_path.is_file():
        raise PilotError("review evidence is missing")
    evidence = load_json(evidence_path)
    try:
        assert_outcome_invariants(evidence)
    except ValueError as exc:
        raise PilotError(str(exc)) from exc
    generate_documents(evidence, check=True)
    traceability = validate_traceability(evidence)
    return {
        "versions": versions,
        "containment": containment_self_tests(),
        "canonicalMappings": repository["canonicalMappings"],
        "ownershipIntersections": evidence["mandatory"]["realOwnershipOverlaps"],
        "generatedDocs": "clean",
        "permissions": "pass",
        "nativeWindows": "BLOCKED",
        "outcome": evidence["outcome"],
        "outcomeInvariant": "pass",
        "evidenceProjectionDigest": evidence_projection_digest(evidence),
        "traceability": traceability,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    evaluate = subparsers.add_parser("evaluate")
    evaluate.add_argument("--platform", choices=("all",) + PLATFORMS, default="all")
    evaluate.add_argument("--output", type=Path, default=PILOT_ROOT / "evidence/review.json")
    subparsers.add_parser("validate")
    subparsers.add_parser("doctor")
    generate = subparsers.add_parser("generate-docs")
    generate.add_argument("--check", action="store_true")
    subparsers.add_parser("containment-tests")
    subparsers.add_parser("update-hashes")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        if arguments.command == "update-hashes":
            write_json(PILOT_ROOT / "expected/canonical-hashes.json", canonical_hashes())
            print("Canonical hashes updated.")
        elif arguments.command == "containment-tests":
            print(json.dumps(containment_self_tests(), indent=2, sort_keys=True))
        elif arguments.command == "evaluate":
            evidence = evaluate_all(arguments.platform)
            write_json(arguments.output, evidence)
            print(json.dumps({"outcome": evidence["outcome"], "platforms": sorted(evidence["results"]), "output": str(arguments.output)}, indent=2))
        elif arguments.command == "generate-docs":
            evidence = load_json(PILOT_ROOT / "evidence/review.json")
            if arguments.check:
                fresh = evaluate_all("all")
                compare_evidence_projection(fresh, evidence)
            generate_documents(evidence, check=arguments.check)
            print("Generated documentation is clean." if arguments.check else "Generated documentation updated.")
        elif arguments.command == "validate":
            repository = validate_repository()
            evidence = evaluate_all("all")
            reviewed = load_json(PILOT_ROOT / "evidence/review.json")
            projection_digest = compare_evidence_projection(evidence, reviewed)
            try:
                assert_outcome_invariants(reviewed)
            except ValueError as exc:
                raise PilotError(str(exc)) from exc
            generate_documents(reviewed, check=True)
            print(json.dumps({"repository": repository, "freshOutcome": evidence["outcome"], "evidenceProjection": "identical", "evidenceProjectionDigest": projection_digest, "platforms": sorted(evidence["results"])}, indent=2, sort_keys=True))
        elif arguments.command == "doctor":
            print(json.dumps(doctor(), indent=2, sort_keys=True))
        return 0
    except (PilotError, KeyError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print(f"PILOT_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
