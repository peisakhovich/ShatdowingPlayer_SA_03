"""
Sound Language Studio

---------------------

Module:

    project_dependencies

Purpose:

    Scans Python source files and creates an inventory of standard-library,
    third-party, and project modules imported by the application.

ru:

    Сканирует исходные Python-файлы и формирует инвентаризацию модулей
    стандартной библиотеки, сторонних библиотек и внутренних модулей проекта.

"""
from __future__ import annotations

import ast
from pathlib import Path
import sys


# ==================================================
# CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "dependency_inventory.txt"
)

EXCLUDED_DIRS = {
    ".git",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".vscode",
    ".venv",
    "venv",
    "__pycache__",
}

PROJECT_PACKAGES = {
    "ai",
    "api",
    "audio",
    "core",
    "gui",
    "session",
    "utils",
}


# ==================================================
# FIND PYTHON FILES
# ==================================================

def find_python_files():

    files = []

    for path in BASE_DIR.rglob("*.py"):

        if any(
            part in EXCLUDED_DIRS
            for part in path.parts
        ):
            continue

        files.append(path)

    return sorted(files)


# ==================================================
# EXTRACT IMPORTS
# ==================================================

def extract_imports(path):

    imports = set()

    try:

        source = path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(source)

    except (
        OSError,
        SyntaxError,
        UnicodeDecodeError,
    ):

        return imports

    for node in ast.walk(tree):

        # import pygame
        # import pygame_gui

        if isinstance(node, ast.Import):

            for alias in node.names:

                imports.add(
                    alias.name.split(".")[0]
                )

        # from pathlib import Path
        # from gui.theme import Theme

        elif isinstance(node, ast.ImportFrom):

            # Relative imports:
            #
            # from .something import ...
            # from ..something import ...
            #
            # Они относятся к проекту и отдельно
            # в inventory не рассматриваются.

            if node.level > 0:
                continue

            if node.module:

                imports.add(
                    node.module.split(".")[0]
                )

    return imports


# ==================================================
# STANDARD LIBRARY
# ==================================================

def get_stdlib_modules():

    return set(sys.stdlib_module_names)


# ==================================================
# CLASSIFICATION
# ==================================================

def classify_import(
    name,
    stdlib_modules,
):

    if name in PROJECT_PACKAGES:

        return "project"

    if name in stdlib_modules:

        return "standard"

    return "third_party"


# ==================================================
# BUILD INVENTORY
# ==================================================

def build_inventory():

    python_files = find_python_files()

    stdlib_modules = get_stdlib_modules()

    standard = {}
    third_party = {}
    project = {}

    for path in python_files:

        relative_path = path.relative_to(
            BASE_DIR
        )

        imports = extract_imports(path)

        for name in imports:

            category = classify_import(
                name,
                stdlib_modules
            )

            if category == "standard":

                standard.setdefault(
                    name,
                    set()
                ).add(
                    str(relative_path)
                )

            elif category == "third_party":

                third_party.setdefault(
                    name,
                    set()
                ).add(
                    str(relative_path)
                )

            else:

                project.setdefault(
                    name,
                    set()
                ).add(
                    str(relative_path)
                )

    return (
        python_files,
        standard,
        third_party,
        project,
    )


# ==================================================
# REPORT
# ==================================================

def add_section(
    lines,
    title,
    data,
):

    lines.append("")
    lines.append("=" * 70)
    lines.append(title)
    lines.append("=" * 70)

    if not data:

        lines.append("")
        lines.append("None")
        return

    for name in sorted(data):

        lines.append("")
        lines.append(name)

        for path in sorted(data[name]):

            lines.append(
                f"    {path}"
            )


# ==================================================
# WRITE REPORT
# ==================================================

def write_report(
    python_files,
    standard,
    third_party,
    project,
):

    lines = []

    lines.append(
        "SOUND LANGUAGE STUDIO"
    )

    lines.append(
        "DEPENDENCY INVENTORY"
    )

    lines.append(
        "=" * 70
    )

    lines.append("")

    lines.append(
        f"Project root: {BASE_DIR}"
    )

    lines.append(
        f"Python files scanned: {len(python_files)}"
    )

    lines.append("")

    lines.append(
        "This report contains modules imported by the Python source files."
    )

    lines.append(
        "Modules are classified as standard library, third-party,"
    )

    lines.append(
        "or project modules."
    )

    add_section(
        lines,
        "PYTHON STANDARD LIBRARY",
        standard,
    )

    add_section(
        lines,
        "THIRD-PARTY LIBRARIES",
        third_party,
    )

    add_section(
        lines,
        "PROJECT MODULES",
        project,
    )

    lines.append("")
    lines.append("=" * 70)
    lines.append("SUMMARY")
    lines.append("=" * 70)

    lines.append(
        f"Python files scanned       : {len(python_files)}"
    )

    lines.append(
        f"Standard library modules  : {len(standard)}"
    )

    lines.append(
        f"Third-party libraries     : {len(third_party)}"
    )

    lines.append(
        f"Project packages          : {len(project)}"
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )


# ==================================================
# MAIN
# ==================================================

def main():

    (
        python_files,
        standard,
        third_party,
        project,
    ) = build_inventory()

    write_report(
        python_files,
        standard,
        third_party,
        project,
    )

    print()
    print(
        "SOUND LANGUAGE STUDIO"
    )
    print(
        "Dependency inventory completed."
    )
    print()
    print(
        f"Python files scanned      : {len(python_files)}"
    )
    print(
        f"Standard library modules : {len(standard)}"
    )
    print(
        f"Third-party libraries    : {len(third_party)}"
    )
    print(
        f"Project packages         : {len(project)}"
    )
    print()
    print(
        f"Report: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()