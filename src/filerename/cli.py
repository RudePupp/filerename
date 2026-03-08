"""Command-line interface for filerename."""

from __future__ import annotations

import click

from .renamer import rename_files


@click.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False, path_type=str))
@click.option(
    "--no-recursive",
    is_flag=True,
    help="Only rename files in the top-level directory.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Print planned renames without changing any files.",
)
def main(directory: str, no_recursive: bool, dry_run: bool) -> None:
    """Rename files by replacing spaces with underscores."""
    try:
        renamed = rename_files(directory, recursive=not no_recursive, dry_run=dry_run)
    except (NotADirectoryError, FileExistsError) as exc:
        raise click.ClickException(str(exc)) from exc

    if not renamed:
        click.echo("No files needed renaming.")
        return

    if not dry_run:
        click.echo(f"Renamed {len(renamed)} file(s):")

    for old_path, new_path in renamed:
        click.echo(f"{old_path} -> {new_path}")


if __name__ == "__main__":
    main()
