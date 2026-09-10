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
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True

    if path.name in EXCLUDED_FILES:
        return True

    return False

def module_name(py_file: Path) -> str:
    relative = py_file.relative_to(PROJECT_ROOT)

    parts = list(relative.parts)
    parts[-1] = py_file.stem

    return ".".join(parts)


def create_module_page(py_file: Path) -> None:
    relative = py_file.relative_to(PROJECT_ROOT)

    parts = list(relative.parts)
    parts[-1] = py_file.stem

    output_dir = DOCS_ROOT.joinpath(*parts[:-1])
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{py_file.stem}.md"

    module = module_name(py_file)

    title = py_file.stem.replace("_", " ").title()

    content = f"""# {title}

::: {module}
"""

    if not output_file.exists():
        output_file.write_text(content, encoding="utf-8")
        print(f"Created: {output_file.relative_to(PROJECT_ROOT)}")


def main() -> None:
    for py_file in PROJECT_ROOT.rglob("*.py"):

        if is_excluded(py_file):
            continue

        if py_file.name == "__init__.py":
            continue

        create_module_page(py_file)


if __name__ == "__main__":
    main()