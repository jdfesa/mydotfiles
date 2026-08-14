#!/usr/bin/env python3
"""Report exact non-empty file matches against an external reference tree."""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter, defaultdict
from pathlib import Path


SKIPPED_NAMES = {".git", ".venv", "node_modules", "__pycache__"}


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(
        description=(
            "Compara contenido exacto no vacio. Una coincidencia no demuestra "
            "autoria ni compatibilidad de licencia."
        )
    )
    parser.add_argument("source", type=Path, help="arbol externo a comparar")
    parser.add_argument(
        "--repository",
        type=Path,
        default=repo_root,
        help=f"repositorio local (default: {repo_root})",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="mostrar cada coincidencia ademas del resumen",
    )
    return parser.parse_args()


def iter_files(root: Path, *, repository: bool) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in SKIPPED_NAMES for part in relative.parts):
            continue
        if repository and relative.parts[:2] == ("references", "inbox"):
            continue
        if not path.is_file() or path.is_symlink() or path.stat().st_size == 0:
            continue
        files.append(path)
    return files


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> int:
    args = parse_args()
    source = args.source.expanduser().resolve()
    repository = args.repository.expanduser().resolve()

    if not source.is_dir():
        raise SystemExit(f"Source directory not found: {source}")
    if not repository.is_dir():
        raise SystemExit(f"Repository directory not found: {repository}")

    source_hashes: dict[str, list[Path]] = defaultdict(list)
    for path in iter_files(source, repository=False):
        source_hashes[digest(path)].append(path)

    matches: list[tuple[Path, Path]] = []
    counts: Counter[str] = Counter()
    for local_path in iter_files(repository, repository=True):
        for source_path in source_hashes.get(digest(local_path), []):
            local_relative = local_path.relative_to(repository)
            source_relative = source_path.relative_to(source)
            matches.append((local_relative, source_relative))
            counts[local_relative.parts[0]] += 1

    print(f"Repository files: {len(iter_files(repository, repository=True))}")
    print(f"Source files: {sum(len(paths) for paths in source_hashes.values())}")
    print(f"Exact pairs: {len(matches)}")
    print("\nExact pairs by local top-level directory:")
    for area, count in sorted(counts.items()):
        print(f"  {area}: {count}")

    if args.details:
        print("\nExact matches:")
        for local_relative, source_relative in sorted(matches):
            print(f"  {local_relative} <- {source_relative}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

