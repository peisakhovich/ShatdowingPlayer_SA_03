"""
Sound Language Studio

---------------------

Module:

    project_import_map

Purpose:

    Scans Python source files and creates a structured map of application
    modules, internal dependencies, standard-library and third-party imports.

ru:

    Сканирует исходные Python-файлы и формирует структурированную карту
    модулей приложения, внутренних зависимостей и внешних библиотек.

"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


# ==================================================
# CONFIGURATION
# ==================================================

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
    "project_tree",
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
# MODULE NAME
# ==================================================

def get_module_name(path):

    relative_path = path.relative_to(BASE_DIR)

    parts = list(relative_path.parts)

    if parts[-1] == "__init__.py":

        parts = parts[:-1]

    else:

        parts[-1] = Path(
            parts[-1]
        ).stem

    return ".".join(parts)


# ==================================================
# MODULE CATEGORY
# ==================================================

def get_module_category(module_name):

    top_level = module_name.split(".")[0]

    if top_level in APPLICATION_PACKAGES:

        return "application"

    if (
        top_level in DEVELOPMENT_MODULES
        or module_name.startswith("tests.")
    ):

        return "development"

    if top_level == "main":

        return "application"

    return "other"


# ==================================================
# BUILD MODULE MAP
# ==================================================

def build_module_map(
    python_files,
):

    modules = {}

    for path in python_files:

        module_name = get_module_name(path)

        if module_name:

            modules[module_name] = path

    return modules


# ==================================================
# RESOLVE PROJECT IMPORT
# ==================================================

def resolve_project_import(
    name,
    project_modules,
):

    if name in project_modules:

        return name

    candidates = [
        module
        for module in project_modules
        if module.startswith(
            name + "."
        )
    ]

    if candidates:

        return name

    top_level = name.split(".")[0]

    candidates = [
        module
        for module in project_modules
        if module == top_level
        or module.startswith(
            top_level + "."
        )
    ]

    if candidates:

        parts = name.split(".")

        for index in range(
            len(parts),
            0,
            -1
        ):

            candidate = ".".join(
                parts[:index]
            )

            if candidate in project_modules:

                return candidate

        return top_level

    return None


# ==================================================
# RESOLVE RELATIVE IMPORT
# ==================================================

def resolve_relative_import(
    current_module,
    node,
    project_modules,
):

    if node.level <= 0:

        return None

    current_parts = current_module.split(".")

    # Current module itself is a module, not a package.
    # For a file inside a package, remove the module name.

    if current_parts:

        current_parts = current_parts[:-1]

    level = node.level - 1

    if level > len(current_parts):

        return None

    if level == 0:

        base_parts = current_parts

    else:

        base_parts = current_parts[
            :len(current_parts) - level
        ]

    if node.module:

        imported_parts = node.module.split(".")

        candidate_parts = (
            base_parts
            + imported_parts
        )

    else:

        candidate_parts = base_parts

    candidate = ".".join(
        candidate_parts
    )

    resolved = resolve_project_import(
        candidate,
        project_modules,
    )

    if resolved:

        return resolved

    return None


# ==================================================
# EXTRACT IMPORTS
# ==================================================

def extract_imports(
    path,
    project_modules,
):

    internal = set()
    standard = set()
    third_party = set()

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

        return (
            internal,
            standard,
            third_party,
        )

    current_module = get_module_name(path)

    for node in ast.walk(tree):

        # ------------------------------------------
        # import ...
        # ------------------------------------------

        if isinstance(node, ast.Import):

            for alias in node.names:

                name = alias.name

                project_name = (
                    resolve_project_import(
                        name,
                        project_modules,
                    )
                )

                if project_name:

                    internal.add(
                        project_name
                    )

                    continue

                top_level = name.split(".")[0]

                if (
                    top_level
                    in sys.stdlib_module_names
                ):

                    standard.add(
                        top_level
                    )

                else:

                    third_party.add(
                        top_level
                    )

        # ------------------------------------------
        # from ... import ...
        # ------------------------------------------

        elif isinstance(
            node,
            ast.ImportFrom,
        ):

            # Relative import

            if node.level > 0:

                project_name = (
                    resolve_relative_import(
                        current_module,
                        node,
                        project_modules,
                    )
                )

                if project_name:

                    internal.add(
                        project_name
                    )

                continue

            if not node.module:

                continue

            name = node.module

            project_name = (
                resolve_project_import(
                    name,
                    project_modules,
                )
            )

            if project_name:

                internal.add(
                    project_name
                )

                continue

            top_level = name.split(".")[0]

            if (
                top_level
                in sys.stdlib_module_names
            ):

                standard.add(
                    top_level
                )

            else:

                third_party.add(
                    top_level
                )

    internal.discard(
        current_module
    )

    return (
        internal,
        standard,
        third_party,
    )


# ==================================================
# BUILD IMPORT MAP
# ==================================================

def build_import_map():

    python_files = find_python_files()

    project_modules = build_module_map(
        python_files
    )

    internal = {}
    standard = {}
    third_party = {}

    for path in python_files:

        module_name = get_module_name(path)

        (
            internal_modules,
            standard_modules,
            third_party_modules,
        ) = extract_imports(
            path,
            project_modules,
        )

        internal[module_name] = (
            internal_modules
        )

        standard[module_name] = (
            standard_modules
        )

        third_party[module_name] = (
            third_party_modules
        )

    return (
        python_files,
        project_modules,
        internal,
        standard,
        third_party,
    )


# ==================================================
# REVERSE MAP
# ==================================================

def build_reverse_map(
    internal,
):

    reverse = {}

    for module, dependencies in internal.items():

        for dependency in dependencies:

            reverse.setdefault(
                dependency,
                set()
            ).add(
                module
            )

    return reverse


# ==================================================
# ARCHITECTURAL ROOTS
# ==================================================

def find_architectural_roots(
    internal,
    application_modules,
):

    imported_modules = set()

    for module in application_modules:

        dependencies = internal.get(
            module,
            set()
        )

        for dependency in dependencies:

            if dependency in application_modules:

                imported_modules.add(
                    dependency
                )

    roots = []

    for module in application_modules:

        if module not in imported_modules:

            roots.append(module)

    return sorted(roots)


# ==================================================
# REPORT HELPERS
# ==================================================

def add_dependency_section(
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

        values = data[name]

        if not values:

            lines.append(
                "    → None"
            )

            continue

        for value in sorted(values):

            lines.append(
                f"    → {value}"
            )


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

        values = data[name]

        if not values:

            lines.append(
                "    → None"
            )

            continue

        for value in sorted(values):

            lines.append(
                f"    → {value}"
            )


def add_module_list(
    lines,
    title,
    modules,
):

    lines.append("")
    lines.append("=" * 70)
    lines.append(title)
    lines.append("=" * 70)

    for module in sorted(modules):

        lines.append(
            f"    {module}"
        )


# ==================================================
# WRITE REPORT
# ==================================================

def write_report(
    python_files,
    project_modules,
    internal,
    standard,
    third_party,
):

    reverse = build_reverse_map(
        internal
    )

    application_modules = [
        module
        for module in project_modules
        if get_module_category(module)
        == "application"
    ]

    roots = find_architectural_roots(
        internal,
        application_modules,
    )

    development_modules = [
        module
        for module in project_modules
        if get_module_category(module)
        == "development"
    ]

    lines = []

    lines.append(
        "SOUND LANGUAGE STUDIO"
    )

    lines.append(
        "PROJECT IMPORT MAP"
    )

    lines.append(
        "=" * 70
    )

    lines.append("")

    lines.append(
        f"Project root: {BASE_DIR}"
    )

    lines.append(
        f"Python files scanned: "
        f"{len(python_files)}"
    )

    lines.append(
        f"Project modules found: "
        f"{len(project_modules)}"
    )

    add_module_list(
        lines,
        "APPLICATION MODULES",
        application_modules,
    )

    add_dependency_section(
        lines,
        "INTERNAL DEPENDENCIES",
        internal,
    )

    add_dependency_section(
        lines,
        "PYTHON STANDARD LIBRARY",
        standard,
    )

    add_dependency_section(
        lines,
        "THIRD-PARTY LIBRARIES",
        third_party,
    )

    add_dependency_section(
        lines,
        "MODULE USAGE",
        reverse,
    )

    add_module_list(
        lines,
        "ARCHITECTURAL ROOTS",
        roots,
    )

    add_module_list(
        lines,
        "DEVELOPMENT / TEST MODULES",
        development_modules,
    )

    lines.append("")
    lines.append("=" * 70)
    lines.append("SUMMARY")
    lines.append("=" * 70)

    lines.append(
        f"Python files scanned       : "
        f"{len(python_files)}"
    )

    lines.append(
        f"Project modules found      : "
        f"{len(project_modules)}"
    )

    lines.append(
        f"Application modules        : "
        f"{len(application_modules)}"
    )

    lines.append(
        f"Development modules        : "
        f"{len(development_modules)}"
    )

    lines.append(
        f"Modules with internal "
        f"imports                   : "
        f"{sum(bool(value) for value in internal.values())}"
    )

    lines.append(
        f"Modules without internal "
        f"imports                   : "
        f"{sum(not value for value in internal.values())}"
    )

    standard_libraries = set()

    for libraries in standard.values():

        standard_libraries.update(
            libraries
        )

    third_party_libraries = set()

    for libraries in third_party.values():

        third_party_libraries.update(
            libraries
        )

    lines.append(
        f"Standard-library modules   : "
        f"{len(standard_libraries)}"
    )

    lines.append(
        f"Third-party libraries      : "
        f"{len(third_party_libraries)}"
    )

    lines.append(
        f"Architectural roots        : "
        f"{len(roots)}"
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
        project_modules,
        internal,
        standard,
        third_party,
    ) = build_import_map()

    write_report(
        python_files,
        project_modules,
        internal,
        standard,
        third_party,
    )

    print()
    print(
        "SOUND LANGUAGE STUDIO"
    )

    print(
        "Project import map completed."
    )

    print()

    print(
        f"Python files scanned : "
        f"{len(python_files)}"
    )

    print(
        f"Project modules      : "
        f"{len(project_modules)}"
    )

    print()

    print(
        f"Report: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()