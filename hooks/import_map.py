from __future__ import annotations

from pathlib import Path
import re


IMPORT_MAP_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "import_map.txt"
)


def _get_internal_dependencies(module_name: str) -> str:
    """Возвращает внутренние зависимости модуля из import_map.txt."""

    if not IMPORT_MAP_FILE.exists():
        return (
            f"> **import_map.txt not found:** "
            f"`{IMPORT_MAP_FILE}`"
        )

    text = IMPORT_MAP_FILE.read_text(
        encoding="utf-8"
    )

    lines = text.splitlines()

    # Находим начало секции INTERNAL DEPENDENCIES.
    try:
        section_start = lines.index(
            "INTERNAL DEPENDENCIES"
        )
    except ValueError:
        return (
            "> **INTERNAL DEPENDENCIES section not found.**"
        )

    # Пропускаем заголовок секции и строки =====.
    index = section_start + 1

    while index < len(lines):
        if lines[index].strip() == "":
            index += 1
            continue

        if set(lines[index].strip()) == {"="}:
            index += 1
            continue

        break

    # Ищем нужный модуль.
    while index < len(lines):

        line = lines[index]

        # Следующая секция import_map.txt.
        if (
            line.strip()
            and not line.startswith(" ")
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
                    dependencies.append(
                        dependency_line
                    )
                    index += 1
                    continue

                # Начался следующий модуль.
                break

            if not dependencies:
                return (
                    f"`{module_name}` "
                    "has no internal dependencies."
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

        if section_name == "internal_dependencies":
            return _get_internal_dependencies(module_name)

        return (
            f"> **Unknown import-map section:** "
            f"`{section_name}`"
        )

    return pattern.sub(replace, markdown)