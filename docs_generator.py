from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DOCS_ROOT = PROJECT_ROOT / "docs" / "modules"


EXCLUDED_DIRS = {
    ".venv",
    "__pycache__",
    "tests",
    "data",
    "logs",
    "tmp",
    "test_output",
}

EXCLUDED_FILES = {
    "docs_generator.py",
    "project_tree.py",
    "project_dependencies.py",
    "project_import_map.py",
    "test_environment.py",
}


def is_excluded(path: Path) -> bool:
    """Проверяет, должен ли файл или каталог быть исключён."""
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True

    if path.name in EXCLUDED_FILES:
        return True

    return False


def module_name(py_file: Path) -> str:
    """Возвращает Python module path относительно корня проекта."""
    relative = py_file.relative_to(PROJECT_ROOT)

    parts = list(relative.parts)
    parts[-1] = py_file.stem

    return ".".join(parts)


def module_page_content(module: str, title: str) -> str:
    """Формирует стандартное содержимое страницы модуля."""
    return f"""# {title}

## Архитектура

### Internal dependencies

<!-- import-map: {module}: internal_dependencies -->

### Python standard library

<!-- import-map: {module}: standard_library -->

### Third-party libraries

<!-- import-map: {module}: third_party -->

## API

::: {module}
"""


def is_old_module_page(content: str, module: str) -> bool:
    """
    Проверяет, является ли существующая Markdown-страница
    старой стандартной страницей модуля.
    """
    normalized = content.strip()

    expected_marker = f"::: {module}"

    if expected_marker not in normalized:
        return False

    if "## Архитектура" in normalized:
        return False

    lines = [
        line.strip()
        for line in normalized.splitlines()
        if line.strip()
    ]

    if len(lines) != 2:
        return False

    if not lines[0].startswith("# "):
        return False

    if lines[1] != expected_marker:
        return False

    return True


def create_module_page(py_file: Path) -> None:
    """Создаёт или обновляет стандартную страницу MkDocs."""
    relative = py_file.relative_to(PROJECT_ROOT)

    parts = list(relative.parts)
    parts[-1] = py_file.stem

    output_dir = DOCS_ROOT.joinpath(*parts[:-1])
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{py_file.stem}.md"

    module = module_name(py_file)
    title = py_file.stem.replace("_", " ").title()

    new_content = module_page_content(module, title)

    if not output_file.exists():
        output_file.write_text(
            new_content,
            encoding="utf-8",
        )

        print(
            f"Created: "
            f"{output_file.relative_to(PROJECT_ROOT)}"
        )

        return

    old_content = output_file.read_text(
        encoding="utf-8",
    )

    if is_old_module_page(old_content, module):
        output_file.write_text(
            new_content,
            encoding="utf-8",
        )

        print(
            f"Updated: "
            f"{output_file.relative_to(PROJECT_ROOT)}"
        )

        return

    print(
        f"Skipped: "
        f"{output_file.relative_to(PROJECT_ROOT)}"
    )


def main() -> None:
    """Создаёт и обновляет страницы документации Python-модулей."""
    for py_file in PROJECT_ROOT.rglob("*.py"):

        if is_excluded(py_file):
            continue

        if py_file.name == "__init__.py":
            continue

        create_module_page(py_file)


if __name__ == "__main__":
    main()