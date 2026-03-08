"""Core logic for renaming files."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

RenameRecord = Tuple[Path, Path]


def _sanitized_name(name: str) -> str:
    """Return filename with spaces replaced by underscores."""
    return name.replace(" ", "_")


def _iter_files(directory: Path, recursive: bool) -> Iterable[Path]:
    pattern = "**/*" if recursive else "*"
    yield from (path for path in directory.glob(pattern) if path.is_file())


def _norm_for_fs(path: Path) -> str:
    """Normalize a path string for filesystem-style comparisons."""
    return os.path.normcase(str(path))


def rename_files(
    directory: str | Path,
    recursive: bool = True,
    dry_run: bool = False,
) -> List[RenameRecord]:
    """
    Rename files inside a directory by replacing spaces in names with underscores.

    Args:
        directory: Path to the directory containing files to rename.
        recursive: Whether to process files in subdirectories.
        dry_run: If True, only report planned renames without changing files.

    Returns:
        A list of (old_path, new_path) tuples for every planned or applied rename.

    Raises:
        FileNotFoundError: If directory doesn't exist.
        NotADirectoryError: If provided path is not a directory.
    """
    directory_path = Path(directory).expanduser()

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory_path}")
    if not directory_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory_path}")

    planned: List[RenameRecord] = []
    planned_targets: Dict[str, Path] = {}

    for old_path in sorted(_iter_files(directory_path, recursive)):
        new_name = _sanitized_name(old_path.name)

        if new_name == old_path.name:
            continue

        new_path = old_path.with_name(new_name)
        normalized_target = _norm_for_fs(new_path)

        existing_target = planned_targets.get(normalized_target)
        if existing_target is not None:
            raise FileExistsError(
                f"Cannot rename '{old_path}' to '{new_path}': "
                f"target collides with planned rename '{existing_target}'"
            )

        if new_path.exists():
            raise FileExistsError(
                f"Cannot rename '{old_path}' to '{new_path}': destination already exists"
            )

        planned.append((old_path, new_path))
        planned_targets[normalized_target] = old_path

    if dry_run:
        return planned

    renamed: List[RenameRecord] = []
    for old_path, new_path in planned:
        old_path.rename(new_path)
        renamed.append((old_path, new_path))

    return renamed
