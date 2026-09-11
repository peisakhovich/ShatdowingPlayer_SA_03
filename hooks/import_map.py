from __future__ import annotations

from pathlib import Path
import re


IMPORT_MAP_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "import_map.txt"
)


SECTION_NAMES = {
    "internal_dependencies": "INTERNAL DEPENDENCIES",
    "standard_library": "PYTHON STANDARD LIBRARY",
    "third_party": "THIRD-PARTY LIBRARIES",
}


def _get_module_section(
    module_name: str,
    section_name: str,
) -> str:
    """Возвращает зависимости модуля из указанной секции import_map.txt."""

    if not IMPORT_MAP_FILE.exists():
        return (
            f"> **import_map.txt not found:** "
            f"`{IMPORT_MAP_FILE}`"
        )

    text = IMPORT_MAP_FILE.read_text(
        encoding="utf-8"
    )

    lines = text.splitlines()

    section_title = SECTION_NAMES.get(section_name)

    if section_title is None:
        return (
            f"> **Unknown import-map section:** "
            f"`{section_name}`"
        )

    # Находим начало нужной секции.
    try:
        section_start = lines.index(section_title)
    except ValueError:
        return (
            f"> **Section not found:** "
            f"`{section_title}`"
        )

    index = section_start + 1

    # Пропускаем пустые строки и линии =====.
    while index < len(lines):
        line = lines[index].strip()

        if not line:
            index += 1
            continue

        if set(line) == {"="}:
            index += 1
            continue

        break

    # Ищем нужный модуль.
    while index < len(lines):

        line = lines[index]

        # Началась следующая секция.
        if (
            line.strip()
            and set(line.strip()) == {"="}
        ):
            break

        if line.strip() == module_name:

            dependencies = []

            index += 1

            while index < len(lines):
                dependency_line = lines[index]

                # Пустая строка завершает блок.
                if not dependency_line.strip():
                    break

                # Строки с отступом являются зависимостями.
                if dependency_line.startswith("    "):
                    dependency = dependency_line.strip()

                    # None означает отсутствие зависимостей.
                    if dependency != "→ None":
                        dependencies.append(
                            dependency
                        )

                    index += 1
                    continue

                # Начался следующий модуль.
                break

            if not dependencies:
                return (
                    f"`{module_name}` "
                    "has no dependencies."
                )

            return (
                "```text\n"
                f"{module_name}\n"
                + "\n".join(dependencies)
                + "\n```"
            )

        index += 1

    return (
        f"> **Module not found:** `{module_name}`"
    )


def on_page_markdown(
    markdown,
    page,
    config,
    files,
):
    pattern = re.compile(
        r"<!--\s*import-map:\s*"
        r"(.+?)\s*:\s*"
        r"(.+?)\s*-->"
    )

    def replace(match):
        module_name = match.group(1).strip()
        section_name = match.group(2).strip()

        return _get_module_section(
            module_name,
            section_name,
        )

    return pattern.sub(
        replace,
        markdown,
    )