"""
Sound Language Studio
---------------------

Project utility:
    project_import_map.py

Purpose:
    Scans the Python project and generates an import dependency map.

ru:
    Сканирует Python-проект и создаёт карту зависимостей
    между модулями и библиотеками.
"""

from __future__ import annotations

import ast
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "import_map.txt"
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
    "site",
}


APPLICATION_PACKAGES = {
    "ai",
    "api",
    "audio",
    "core",
    "gui",
    "session",
    "utils",
}


DEVELOPMENT_MODULES = {
    "tests",
    "test_environment",
    "project_dependencies",
    "project_import_map",
    "project_statistics",
    "project_tree",
}


STANDARD_LIBRARY = {
    "__future__",
    "argparse",
    "ast",
    "asyncio",
    "base64",
    "collections",
    "contextlib",
    "copy",
    "csv",
    "datetime",
    "enum",
    "functools",
    "getpass",
    "glob",
    "hashlib",
    "inspect",
    "io",
    "itertools",
    "json",
    "logging",
    "math",
    "os",
    "pathlib",
    "random",
    "re",
    "shlex",
    "shutil",
    "socket",
    "sqlite3",
    "statistics",
    "string",
    "subprocess",
    "sys",
    "tempfile",
    "textwrap",
    "threading",
    "time",
    "tkinter",
    "traceback",
    "types",
    "typing",
    "unittest",
    "urllib",
    "uuid",
    "warnings",
    "weakref",
}


def find_python_files():
    """Return all Python files belonging to the project."""

    files = []

    for path in BASE_DIR.rglob("*.py"):
        relative = path.relative_to(BASE_DIR)
        relative_parts = relative.parts

        # Exclude generated MkDocs module sources.
        if (
            len(relative_parts) >= 2
            and relative_parts[0] == "docs"
            and relative_parts[1] == "modules"
        ):
            continue

        if any(
            directory in EXCLUDED_DIRS
            for directory in relative_parts
        ):
            continue

        files.append(path)

    return sorted(files)

def get_module_name(path):
    """Convert a Python file path into a project module name."""

    relative = path.relative_to(BASE_DIR)

    parts = list(relative.parts)

    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = path.stem

    return ".".join(parts)


def get_module_category(module_name):
    """Return the logical category of a project module."""

    root = module_name.split(".", 1)[0]

    if root in APPLICATION_PACKAGES:
        return "application"

    if (
        root in DEVELOPMENT_MODULES
        or module_name in DEVELOPMENT_MODULES
    ):
        return "development"

    return "other"


def build_module_map(files):
    """Build a mapping of module names to Python files."""

    return {
        get_module_name(path): path
        for path in files
    }


def resolve_project_import(import_name, project_modules):
    """Resolve an absolute import to a project module."""

    if import_name in project_modules:
        return import_name

    parts = import_name.split(".")

    while parts:
        candidate = ".".join(parts)

        if candidate in project_modules:
            return candidate

        parts.pop()

    return None


def resolve_relative_import(
    current_module,
    level,
    import_name,
    project_modules,
):
    """Resolve a relative import to a project module."""

    current_parts = current_module.split(".")

    if level > len(current_parts):
        return None

    base_parts = current_parts[:-level]

    if import_name:
        base_parts.extend(import_name.split("."))

    candidate = ".".join(base_parts)

    return resolve_project_import(
        candidate,
        project_modules,
    )


def extract_imports(
    path,
    current_module,
    project_modules,
):
    """Extract internal and external imports from a Python file."""

    try:
        source = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        tree = ast.parse(
            source,
            filename=str(path),
        )

    except (OSError, SyntaxError):
        return set(), set(), set()

    internal = set()
    standard = set()
    third_party = set()

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:
                imported = alias.name

                project_module = resolve_project_import(
                    imported,
                    project_modules,
                )

                if project_module:
                    internal.add(project_module)
                    continue

                root = imported.split(".")[0]

                if root in STANDARD_LIBRARY:
                    standard.add(root)
                else:
                    third_party.add(root)

        elif isinstance(node, ast.ImportFrom):

            if node.level > 0:

                project_module = resolve_relative_import(
                    current_module,
                    node.level,
                    node.module or "",
                    project_modules,
                )

                if project_module:
                    internal.add(project_module)

                continue

            if not node.module:
                continue

            imported = node.module

            project_module = resolve_project_import(
                imported,
                project_modules,
            )

            if project_module:
                internal.add(project_module)
                continue

            root = imported.split(".")[0]

            if root in STANDARD_LIBRARY:
                standard.add(root)
            else:
                third_party.add(root)

    return internal, standard, third_party


def build_import_map(files, project_modules):
    """Build internal and external dependency maps."""

    internal = {}
    standard = {}
    third_party = {}

    for path in files:

        module_name = get_module_name(path)

        (
            module_internal,
            module_standard,
            module_third_party,
        ) = extract_imports(
            path,
            module_name,
            project_modules,
        )

        if module_internal:
            internal[module_name] = module_internal

        if module_standard:
            standard[module_name] = module_standard

        if module_third_party:
            third_party[module_name] = module_third_party

    return internal, standard, third_party


def build_reverse_map(internal):
    """Build reverse internal dependency map."""

    reverse = {}

    for module, dependencies in internal.items():

        for dependency in dependencies:
            reverse.setdefault(
                dependency,
                set(),
            ).add(module)

    return reverse


def find_architectural_roots(
    internal,
    project_modules,
):
    """
    Find modules that are not imported by another project module.
    """

    imported_modules = set()

    for dependencies in internal.values():
        imported_modules.update(dependencies)

    roots = set(project_modules) - imported_modules

    return sorted(roots)


def build_library_usage(libraries):
    """Build library -> modules usage mapping."""

    usage = {}

    for module_name, module_libraries in libraries.items():

        for library in module_libraries:

            if library == "__future__":
                continue

            usage.setdefault(
                library,
                set(),
            ).add(module_name)

    return usage


def add_library_summary(
    lines,
    title,
    libraries,
):
    """Add a simple library summary section."""

    lines.append("")
    lines.append(title)
    lines.append("")

    if not libraries:
        lines.append("None")
        lines.append("")
        return

    for library in sorted(libraries):
        lines.append(
            f"- `{library}`"
        )

    lines.append("")


def add_library_usage_section(
    lines,
    title,
    libraries,
):
    """Add library usage statistics."""

    lines.append("")
    lines.append(title)
    lines.append("")

    usage = build_library_usage(libraries)

    if not usage:
        lines.append("None")
        lines.append("")
        return

    ordered = sorted(
        usage.items(),
        key=lambda item: (
            -len(item[1]),
            item[0],
        ),
    )

    for library, modules in ordered:

        lines.append(
            f"- `{library}` — "
            f"{len(modules)} modules"
        )

    lines.append("")


def add_dependency_section(
    lines,
    title,
    dependencies,
):
    """Add a dependency mapping section."""

    lines.append("")
    lines.append(title)
    lines.append("")

    if not dependencies:
        lines.append("None")
        lines.append("")
        return

    for module in sorted(dependencies):

        lines.append(
            f"### `{module}`"
        )

        for dependency in sorted(
            dependencies[module]
        ):
            lines.append(
                f"- `{dependency}`"
            )

        lines.append("")


def add_section(
    lines,
    title,
):
    """Add a Markdown-style section heading."""

    lines.append("")
    lines.append(title)
    lines.append("")


def add_module_list(
    lines,
    title,
    modules,
):
    """Add a sorted module list."""

    add_section(
        lines,
        title,
    )

    if not modules:
        lines.append("None")
        lines.append("")
        return

    for module in sorted(modules):
        lines.append(
            f"- `{module}`"
        )

    lines.append("")


def write_report(
    files,
    project_modules,
    internal,
    standard,
    third_party,
    reverse,
    roots,
):
    """Write the complete import analysis report."""

    application_modules = [
        module
        for module in project_modules
        if get_module_category(module)
        == "application"
    ]

    development_modules = [
        module
        for module in project_modules
        if get_module_category(module)
        == "development"
    ]

    other_modules = [
        module
        for module in project_modules
        if get_module_category(module)
        == "other"
    ]

    modules_with_internal_imports = set(internal)

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

    lines = []

    lines.append(
        "Sound Language Studio"
    )

    lines.append(
        "PROJECT IMPORT MAP"
    )

    lines.append(
        "==================="
    )

    add_section(
        lines,
        "PROJECT STATISTICS",
    )

    lines.append(
        f"Python files: "
        f"{len(files)}"
    )

    lines.append(
        f"Project modules: "
        f"{len(project_modules)}"
    )

    lines.append(
        f"Application modules: "
        f"{len(application_modules)}"
    )

    lines.append(
        f"Development / test modules: "
        f"{len(development_modules)}"
    )

    lines.append(
        f"Other modules: "
        f"{len(other_modules)}"
    )

    lines.append(
        f"Modules with internal imports: "
        f"{len(modules_with_internal_imports)}"
    )

    lines.append(
        f"Modules without internal imports: "
        f"{len(modules_without_internal_imports)}"
    )

    lines.append(
        f"Standard-library libraries: "
        f"{len(standard_usage)}"
    )

    lines.append(
        f"Third-party libraries: "
        f"{len(third_party_usage)}"
    )

    lines.append(
        f"Architectural roots: "
        f"{len(roots)}"
    )

    add_module_list(
        lines,
        "APPLICATION MODULES",
        application_modules,
    )

    add_module_list(
        lines,
        "DEVELOPMENT / TEST MODULES",
        development_modules,
    )

    if other_modules:
        add_module_list(
            lines,
            "OTHER MODULES",
            other_modules,
        )

    add_dependency_section(
        lines,
        "MODULES WITH INTERNAL IMPORTS",
        internal,
    )

    add_module_list(
        lines,
        "MODULES WITHOUT INTERNAL IMPORTS",
        modules_without_internal_imports,
    )

    add_dependency_section(
        lines,
        "INTERNAL DEPENDENCIES",
        internal,
    )

    add_dependency_section(
        lines,
        "REVERSE INTERNAL DEPENDENCIES",
        reverse,
    )

    add_library_summary(
        lines,
        "PYTHON STANDARD LIBRARY",
        standard_usage,
    )

    add_library_summary(
        lines,
        "THIRD-PARTY LIBRARIES",
        third_party_usage,
    )

    add_library_usage_section(
        lines,
        "STANDARD LIBRARY USAGE",
        standard,
    )

    add_library_usage_section(
        lines,
        "THIRD-PARTY LIBRARY USAGE",
        third_party,
    )

    add_module_list(
        lines,
        "ARCHITECTURAL ROOTS",
        roots,
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"Python files: "
        f"{len(files)}"
    )

    print(
        f"Project modules: "
        f"{len(project_modules)}"
    )

    print(
        f"Application modules: "
        f"{len(application_modules)}"
    )

    print(
        f"Development / test modules: "
        f"{len(development_modules)}"
    )

    print(
        f"Other modules: "
        f"{len(other_modules)}"
    )

    print(
        f"Modules with internal imports: "
        f"{len(modules_with_internal_imports)}"
    )

    print(
        f"Modules without internal imports: "
        f"{len(modules_without_internal_imports)}"
    )

    print(
        f"Standard-library libraries: "
        f"{len(standard_usage)}"
    )

    print(
        f"Third-party libraries: "
        f"{len(third_party_usage)}"
    )

    print(
        f"Architectural roots: "
        f"{len(roots)}"
    )

    print()
    print(
        "Import map generated:"
    )
    print(OUTPUT_FILE)


def main():
    """Run the project import analysis."""

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

    write_report(
        files,
        project_modules,
        internal,
        standard,
        third_party,
        reverse,
        roots,
    )


if __name__ == "__main__":
    main()