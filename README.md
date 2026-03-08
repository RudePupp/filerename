# filerename

A small Python CLI project that renames files by replacing spaces in filenames with underscores.

## Installation

```bash
python -m pip install -e .
```

## Usage

Rename files recursively in a directory:

```bash
filerename "/path/to/input directory"
```

Rename only top-level files (non-recursive):

```bash
filerename "/path/to/input directory" --no-recursive
```

Preview changes without renaming files:

```bash
filerename "/path/to/input directory" --dry-run
```

### Windows examples

PowerShell:

```powershell
filerename "C:\Users\you\My Files" --dry-run
```

Command Prompt:

```bat
filerename "C:\Users\you\My Files" --no-recursive
```

## Behavior notes

- Existing destination files are never overwritten.
- On Windows, collisions are handled with case-insensitive path comparison to match Windows filesystem behavior.
- `--dry-run` prints one planned rename per line as `old -> new` and does not modify the filesystem.

## Example

Before:

- `my report.txt`
- `family photo.jpg`

After:

- `my_report.txt`
- `family_photo.jpg`
