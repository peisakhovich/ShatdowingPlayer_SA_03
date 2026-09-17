"""
Sound Language Studio
---------------------

Project utility:
    project_statistics.py

Purpose:
    Generates a Markdown project statistics page for MkDocs
    using the same project analysis as project_import_map.py.
"""

from __future__ import annotations

from pathlib import Path

from project_import_map import (
    build_import_map,
    build_library_usage,
    build_module_map,
    build_reverse_map,
    find_architectural_roots,
    find_python_files,
    get_module_category,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_FILE = (
    BASE_DIR
    / "docs"
    / "project_statistics.md"
)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_number(value):
    """Format an integer for Markdown output."""

    return f"{value:,}".replace(",", " ")


def add_heading(lines, title, level=2):
    """Add a Markdown heading."""

    lines.append("")
    lines.append(f'{"#" * level} {title}')
    lines.append("")


def add_statistics_table(lines, statistics):
    """Add the main project statistics table."""

    lines.append("| Metric | Value |")
    lines.append("|---|---:|")

    for name, value in statistics:
        lines.append(
            f"| {name} | {format_number(value)} |"
        )

    lines.append("")


def add_library_table(lines, usage):
    """Add a library usage table."""

    lines.append("| Library | Modules using it |")
    lines.append("|---|---:|")

    ordered = sorted(
        usage.items(),
        key=lambda item: (
            -len(item[1]),
            item[0],
        ),
    )

    for library, modules in ordered:
        lines.append(
            f"| `{library}` | {len(modules)} |"
        )

    lines.append("")


def add_module_list(lines, modules):
    """Add a sorted Markdown list of modules."""

    if not modules:
        lines.append("- None")
        lines.append("")
        return

    for module in sorted(modules):
        lines.append(
            f"- `{module}`"
        )

    lines.append("")


# ---------------------------------------------------------------------------
# Page generation
# ---------------------------------------------------------------------------

def generate_statistics_page():
    """Generate the MkDocs project statistics page."""

    files = find_python_files()

    project_modules = build_module_map(
        files
    )

    (
        internal,
        standard,
        third_party,
    ) = build_import_map(
        files,
        project_modules,
    )

    reverse = build_reverse_map(
        internal
    )

    roots = find_architectural_roots(
        internal,
        project_modules,
    )

    application_modules = []
    development_modules = []
    other_modules = []

    for module in project_modules:

        category = get_module_category(
            module
        )

        if category == "application":
            application_modules.append(module)

        elif category == "development":
            development_modules.append(module)

        else:
            other_modules.append(module)

    modules_with_internal_imports = set(
        internal
    )

    modules_without_internal_imports = (
        set(project_modules)
        - modules_with_internal_imports
    )

    standard_usage = build_library_usage(
        standard
    )

    third_party_usage = build_library_usage(
        third_party
    )

    # ------------------------------------------------------------------
    # Markdown
    # ------------------------------------------------------------------

    lines = []

    lines.append("# Project Statistics")
    lines.append("")
    lines.append(
        "Automatically generated statistics for "
        "**Sound Language Studio**."
    )
    lines.append("")
    lines.append(
        "The data is generated from the current Python "
        "project structure and import analysis."
    )
    lines.append("")

    # ------------------------------------------------------------------
    # Overview
    # ------------------------------------------------------------------

    add_heading(
        lines,
        "Project Overview",
    )

    statistics = [
        (
            "Python files",
            len(files),
        ),
        (
            "Project modules",
            len(project_modules),
        ),
        (
            "Application modules",
            len(application_modules),
        ),
        (
            "Development / test modules",
            len(development_modules),
        ),
        (
            "Other modules",
            len(other_modules),
        ),
        (
            "Modules with internal imports",
            len(modules_with_internal_imports),
        ),
        (
            "Modules without internal imports",
            len(modules_without_internal_imports),
        ),
        (
            "Standard-library libraries",
            len(standard_usage),
        ),
        (
            "Third-party libraries",
            len(third_party_usage),
        ),
        (
            "Architectural roots",
            len(roots),
        ),
    ]

    add_statistics_table(
        lines,
        statistics,
    )

    # ------------------------------------------------------------------
    # Standard library
    # ------------------------------------------------------------------

    add_heading(
        lines,
        "Python Standard Library Usage",
    )

    lines.append(
        "Number of project modules importing each "
        "standard-library module."
    )
    lines.append("")

    add_library_table(
        lines,
        standard_usage,
    )

    # ------------------------------------------------------------------
    # Third-party libraries
    # ------------------------------------------------------------------

    add_heading(
        lines,
        "Third-Party Library Usage",
    )

    lines.append(
        "Number of project modules importing each "
        "third-party library."
    )
    lines.append("")

    add_library_table(
        lines,
        third_party_usage,
    )

    # ------------------------------------------------------------------
    # Architectural roots
    # ------------------------------------------------------------------

    add_heading(
        lines,
        "Architectural Roots",
    )

    lines.append(
        "Project modules identified as architectural roots "
        "by the import analysis."
    )
    lines.append("")

    add_module_list(
        lines,
        roots,
    )

    # ------------------------------------------------------------------
    # Application modules
    # ------------------------------------------------------------------

    add_heading(
        lines,
        "Application Modules",
    )

    add_module_list(
        lines,
        application_modules,
    )

    # ------------------------------------------------------------------
    # Development modules
    # ------------------------------------------------------------------

    add_heading(
        lines,
        "Development / Test Modules",
    )

    add_module_list(
        lines,
        development_modules,
    )

    # ------------------------------------------------------------------
    # Modules without internal dependencies
    # ------------------------------------------------------------------

    add_heading(
        lines,
        "Modules Without Internal Dependencies",
    )

    lines.append(
        "These modules do not import another project module."
    )
    lines.append("")

    add_module_list(
        lines,
        modules_without_internal_imports,
    )

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------

    lines.append(
        "---"
    )
    lines.append("")
    lines.append(
        "*Generated automatically by "
        "`project_statistics.py`.*"
    )
    lines.append("")

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"Project statistics generated:"
    )
    print(
        OUTPUT_FILE
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Generate the project statistics Markdown page."""

    generate_statistics_page()


if __name__ == "__main__":
    main()