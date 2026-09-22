"""
Sound Language Studio

---------------------

Module:

    docs_nav_generator

Purpose:

    Generates the MkDocs navigation structure from
    the project documentation tree.

ru:

    Формирует структуру навигации MkDocs на основе
    дерева документации проекта.
"""
from pathlib import Path

from tools.project_paths import PROJECT_ROOT


DOCS_MODULES = PROJECT_ROOT / "docs" / "modules"
MKDOCS_FILE = PROJECT_ROOT / "mkdocs.yml"
DOCS_NAV_FILE = PROJECT_ROOT / "docs" / "docs_nav.yml"


EXCLUDED_DIRS = {
    "hooks",
}

EXCLUDED_FILES = {
    "test_environment.md",
}


def make_title(name: str) -> str:
    special_titles = {
        "ai": "AI",
        "api": "API",
        "gui": "GUI",
        "tts": "TTS",
        "openai_client": "OpenAI Client",
    }

    return special_titles.get(
        name,
        name.replace("_", " ").title(),
    )


def build_tree(path: Path, indent: int = 0) -> list[str]:
    lines = []

    directories = sorted(
        item
        for item in path.iterdir()
        if item.is_dir()
        and item.name not in EXCLUDED_DIRS
    )

    files = sorted(
        item
        for item in path.iterdir()
        if item.is_file()
        and item.suffix == ".md"
        and item.name not in EXCLUDED_FILES
    )

    for directory in directories:
        title = make_title(directory.name)

        lines.append(
            " " * indent + f"- {title}:"
        )

        lines.extend(
            build_tree(directory, indent + 4)
        )

    for file in files:
        title = make_title(file.stem)

        relative = file.relative_to(
            PROJECT_ROOT / "docs"
        )

        lines.append(
            " " * indent
            + f"- {title}: {relative.as_posix()}"
        )

    return lines


def build_nav() -> list[str]:
    lines = [
        "  - Sound Language Studio: index.md",
        "  - Architecture: architecture.md",
        "  - Project Statistics: project_statistics.md",
        "  - Application Modes & API Configuration: application_modes.md",
        "  - Modules:",
    ]

    lines.extend(
        build_tree(
            DOCS_MODULES,
            indent=6,
        )
    )

    lines.append(
        "  - Tools Architecture: tools_architecture.md"
    )

    return lines


def update_mkdocs(nav_lines: list[str]) -> None:
    content = MKDOCS_FILE.read_text(
        encoding="utf-8"
    )

    lines = content.splitlines()

    nav_start = None

    for index, line in enumerate(lines):
        if line == "nav:":
            nav_start = index
            break

    if nav_start is None:
        if lines and lines[-1] != "":
            lines.append("")

        lines.append("nav:")
        lines.extend(nav_lines)

    else:
        nav_end = len(lines)

        for index in range(nav_start + 1, len(lines)):
            line = lines[index]

            if line and not line.startswith(" "):
                nav_end = index
                break

        lines[nav_start:nav_end] = [
            "nav:",
            *nav_lines,
        ]

    MKDOCS_FILE.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    nav_lines = build_nav()

    DOCS_NAV_FILE.write_text(
        "\n".join(
            ["nav:", *nav_lines]
        ) + "\n",
        encoding="utf-8",
    )

    update_mkdocs(nav_lines)

    print(f"Updated: {MKDOCS_FILE}")
    print(f"Created: {DOCS_NAV_FILE}")


if __name__ == "__main__":
    main()