from pathlib import Path

from griffe import load


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "docs_audit.txt"


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
    "docs_nav_generator.py",
    "project_tree.py",
    "project_dependencies.py",
    "project_import_map.py",
    "test_environment.py",
    "docs_audit.py",
}


def is_excluded(path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True

    return path.name in EXCLUDED_FILES


def module_name(py_file: Path) -> str:
    relative = py_file.relative_to(PROJECT_ROOT)

    parts = list(relative.parts)
    parts[-1] = py_file.stem

    return ".".join(parts)


def has_docstring(obj) -> bool:
    return bool(
        obj.docstring
        and obj.docstring.value.strip()
    )


def audit_module(py_file: Path) -> list[str]:
    module = load(
        module_name(py_file),
        search_paths=[str(PROJECT_ROOT)],
        resolve_aliases=False,
    )

    problems = []

    for member in module.members.values():

        # Импортированные объекты не являются частью
        # документации данного модуля.
        if member.is_alias:
            continue

        # Проверяем только классы, объявленные
        # непосредственно в данном модуле.
        if member.is_class:

            if not has_docstring(member):
                problems.append(
                    f"  CLASS MISSING: {member.name}"
                )

            for child in member.members.values():

                # Импортированные объекты внутри класса
                # не проверяем.
                if child.is_alias:
                    continue

                if child.is_function:

                    # __init__ пока не считаем обязательным.
                    if child.name == "__init__":
                        continue

                    # Приватные методы пока не проверяем.
                    if child.name.startswith("_"):
                        continue

                    if not has_docstring(child):
                        problems.append(
                            f"  METHOD MISSING: "
                            f"{member.name}.{child.name}"
                        )

    return problems


def main() -> None:

    report = []

    total_modules = 0
    modules_with_problems = 0
    missing_classes = 0
    missing_methods = 0
    errors = 0

    for py_file in sorted(PROJECT_ROOT.rglob("*.py")):

        if is_excluded(py_file):
            continue

        if py_file.name == "__init__.py":
            continue

        total_modules += 1

        try:
            problems = audit_module(py_file)

        except Exception as exc:
            errors += 1

            report.append("")
            report.append(f"ERROR: {module_name(py_file)}")
            report.append(f"  {exc}")

            continue

        if problems:
            modules_with_problems += 1

            report.append("")
            report.append(module_name(py_file))

            for problem in problems:
                report.append(problem)

                if "CLASS MISSING:" in problem:
                    missing_classes += 1

                elif "METHOD MISSING:" in problem:
                    missing_methods += 1

    report.append("")
    report.append("=" * 60)
    report.append("Documentation Audit Summary")
    report.append("=" * 60)
    report.append(f"Modules checked:       {total_modules}")
    report.append(f"Modules with problems: {modules_with_problems}")
    report.append(f"Missing classes:       {missing_classes}")
    report.append(f"Missing methods:       {missing_methods}")
    report.append(f"Errors:                {errors}")
    report.append("=" * 60)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_FILE.write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    print("Documentation audit completed.")
    print()
    print(f"Report: {OUTPUT_FILE}")
    print()
    print(f"Modules checked:       {total_modules}")
    print(f"Modules with problems: {modules_with_problems}")
    print(f"Missing classes:       {missing_classes}")
    print(f"Missing methods:       {missing_methods}")
    print(f"Errors:                {errors}")


if __name__ == "__main__":
    main()