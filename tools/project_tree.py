"""
Sound Language Studio

---------------------

Module:

    project_tree

Purpose:

    Generates a project structure report, including file sizes,
    empty files, empty directories, and Python source files.

ru:

    Формирует отчёт о структуре проекта, включая размеры файлов,
    пустые файлы, пустые каталоги и Python-файлы.
"""
from pathlib import Path
from tools.project_paths import PROJECT_ROOT


EXCLUDED_DIRS = {
    ".venv",
    "venv",
    ".vscode",
    ".git",
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
}


# Files that should not be included in the report.
EXCLUDED_FILES = {
    ".gitignore",
    ".gitattributes",
}


OUTPUT_FILE = "docs/project_structure.txt"


def is_excluded(path: Path) -> bool:
    """Return True if path belongs to an excluded directory."""

    return any(part in EXCLUDED_DIRS for part in path.parts)


def format_size(size: int) -> str:
    """
    Format file size in a human-readable form.

    RU:
    Преобразует размер файла в удобный для чтения формат.

    EN:
    Converts file size to a human-readable format.
    """

    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"

    if size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"

    return f"{size / (1024 * 1024 * 1024):.1f} GB"


def build_tree(root: Path, prefix: str = "") -> list[str]:
    """Build a formatted project tree."""

    lines = []

    try:
        entries = sorted(
            [
                p for p in root.iterdir()
                if not is_excluded(p)
                and p.name not in EXCLUDED_FILES
            ],
            key=lambda p: (p.is_file(), p.name.lower()),
        )
    except PermissionError:
        return [prefix + "[ACCESS DENIED]"]

    for index, path in enumerate(entries):

        is_last = index == len(entries) - 1

        branch = "└── " if is_last else "├── "

        if path.is_file():

            try:
                size = path.stat().st_size
                size_text = format_size(size)

            except OSError:
                size_text = "?"

            lines.append(
                f"{prefix}{branch}{path.name:<35} [{size_text}]"
            )

        else:

            lines.append(
                f"{prefix}{branch}{path.name}"
            )

            extension = "    " if is_last else "│   "

            lines.extend(
                build_tree(
                    path,
                    prefix + extension
                )
            )

    return lines


def find_empty_directories(root: Path) -> list[Path]:
    """
    Find directories that contain no non-excluded entries.
    """

    result = []

    for path in root.rglob("*"):

        if not path.is_dir():
            continue

        if is_excluded(path):
            continue

        try:

            entries = [
                p for p in path.iterdir()
                if not is_excluded(p)
                and p.name not in EXCLUDED_FILES
            ]

            if not entries:
                result.append(path)

        except PermissionError:
            pass

    return sorted(result)


def find_empty_files(root: Path) -> list[Path]:
    """
    Find zero-byte files outside excluded directories.
    """

    result = []

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        if is_excluded(path):
            continue

        if path.name in EXCLUDED_FILES:
            continue

        try:

            if path.stat().st_size == 0:
                result.append(path)

        except OSError:
            pass

    return sorted(result)


def find_python_files(root: Path) -> list[Path]:
    """Find all Python source files."""

    result = []

    for path in root.rglob("*.py"):

        if is_excluded(path):
            continue

        result.append(path)

    return sorted(result)


def main():

    root = PROJECT_ROOT

    print()
    print("=" * 70)
    print("Sound Language Studio - Project Structure Analyzer")
    print("=" * 70)
    print()

    print(f"Project root: {root}")
    print()

    tree = build_tree(root)

    empty_dirs = find_empty_directories(root)
    empty_files = find_empty_files(root)
    python_files = find_python_files(root)

    lines = []

    # --------------------------------------------------------
    # Project tree
    # --------------------------------------------------------

    lines.append("SOUND LANGUAGE STUDIO")
    lines.append("PROJECT STRUCTURE")
    lines.append("=" * 70)
    lines.append("")
    lines.append(root.name)

    lines.extend(tree)

    # --------------------------------------------------------
    # Excluded directories
    # --------------------------------------------------------

    lines.append("")
    lines.append("")
    lines.append("EXCLUDED DIRECTORIES")
    lines.append("=" * 70)

    for name in sorted(EXCLUDED_DIRS):
        lines.append(f"- {name}")

    # --------------------------------------------------------
    # Empty directories
    # --------------------------------------------------------

    lines.append("")
    lines.append("")
    lines.append("EMPTY DIRECTORIES")
    lines.append("=" * 70)

    if empty_dirs:

        for path in empty_dirs:
            lines.append(
                f"- {path.relative_to(root)}"
            )

    else:

        lines.append("None")

    # --------------------------------------------------------
    # Empty files
    # --------------------------------------------------------

    lines.append("")
    lines.append("")
    lines.append("EMPTY FILES")
    lines.append("=" * 70)

    if empty_files:

        for path in empty_files:
            lines.append(
                f"- {path.relative_to(root)}"
            )

    else:

        lines.append("None")

    # --------------------------------------------------------
    # Python files
    # --------------------------------------------------------

    lines.append("")
    lines.append("")
    lines.append("PYTHON FILES")
    lines.append("=" * 70)

    lines.append(
        f"Total: {len(python_files)}"
    )

    lines.append("")

    for path in python_files:

        lines.append(
            str(path.relative_to(root))
        )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    lines.append("")
    lines.append("")
    lines.append("SUMMARY")
    lines.append("=" * 70)

    lines.append(
        f"Python files      : {len(python_files)}"
    )

    lines.append(
        f"Empty files       : {len(empty_files)}"
    )

    lines.append(
        f"Empty directories : {len(empty_dirs)}"
    )

    # --------------------------------------------------------
    # Write report
    # --------------------------------------------------------

    output_path = root / OUTPUT_FILE

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # Console output
    # --------------------------------------------------------

    print("Report created:")
    print(output_path)
    print()

    print(
        f"Python files      : {len(python_files)}"
    )

    print(
        f"Empty files       : {len(empty_files)}"
    )

    print(
        f"Empty directories : {len(empty_dirs)}"
    )

    print()


if __name__ == "__main__":
    main()