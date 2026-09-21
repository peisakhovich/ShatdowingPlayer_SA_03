# Project Statistics

Automatically generated statistics for **Sound Language Studio**.

The data is generated from the current Python project structure and import analysis.


## Project Overview

| Metric | Value |
|---|---:|
| Python files | 104 |
| Project modules | 104 |
| Application modules | 68 |
| Development / test modules | 24 |
| Tools | 8 |
| Other modules | 12 |
| Modules with internal imports | 61 |
| Modules without internal imports | 43 |
| Standard-library libraries | 18 |
| Third-party libraries | 9 |
| Architectural roots | 15 |


## Python Standard Library Usage

Number of project modules importing each standard-library module.

| Library | Modules using it |
|---|---:|
| `pathlib` | 24 |
| `__future__` | 17 |
| `asyncio` | 12 |
| `json` | 5 |
| `os` | 5 |
| `time` | 4 |
| `re` | 3 |
| `ast` | 2 |
| `shutil` | 2 |
| `sys` | 2 |
| `threading` | 2 |
| `datetime` | 1 |
| `hashlib` | 1 |
| `logging` | 1 |
| `math` | 1 |
| `random` | 1 |
| `tempfile` | 1 |
| `tkinter` | 1 |


## Third-Party Library Usage

Number of project modules importing each third-party library.

| Library | Modules using it |
|---|---:|
| `pygame` | 24 |
| `dotenv` | 8 |
| `openpyxl` | 3 |
| `edge_tts` | 2 |
| `griffe` | 1 |
| `httpx` | 1 |
| `openai` | 1 |
| `pydantic` | 1 |
| `pygame_gui` | 1 |


## Architectural Roots

Project modules identified as architectural roots by the import analysis.

- `ai`
- `ai.generators`
- `api`
- `audio`
- `core`
- `gui`
- `gui.dialogs`
- `gui.panels`
- `gui.services`
- `gui.widgets`
- `gui.widgets.label`
- `main`
- `session`
- `session.providers`
- `utils`


## Application Modules

- `ai`
- `ai.dictation_pause`
- `ai.dictation_plan`
- `ai.dictation_segmenter`
- `ai.dictation_validator`
- `ai.generators`
- `ai.generators.dictation_generator`
- `ai.generators.generator_router`
- `ai.generators.shadowing_generator`
- `ai.language_detector`
- `ai.models`
- `ai.openai_client`
- `ai.shadowing_pause`
- `ai.shadowing_plan`
- `ai.shadowing_segmenter`
- `ai.shadowing_validator`
- `api`
- `api.client`
- `audio`
- `audio.async_runner`
- `audio.cache`
- `audio.mixer`
- `audio.player`
- `audio.provider`
- `audio.scenario_provider`
- `audio.tts`
- `core`
- `core.application`
- `core.config`
- `core.logger`
- `gui`
- `gui.database_window`
- `gui.dialogs`
- `gui.dialogs.dialog`
- `gui.file_dialog`
- `gui.layout`
- `gui.login_register_window`
- `gui.main_window`
- `gui.manager`
- `gui.panels`
- `gui.panels.control_panel`
- `gui.panels.control_panel_db`
- `gui.services`
- `gui.services.font_manager`
- `gui.services.image_loader`
- `gui.settings_window`
- `gui.splash_screen`
- `gui.theme`
- `gui.widgets`
- `gui.widgets.busy_indicator`
- `gui.widgets.check_box`
- `gui.widgets.hint`
- `gui.widgets.horizontal_slider`
- `gui.widgets.image_button`
- `gui.widgets.label`
- `gui.widgets.list_selection`
- `gui.widgets.status_message`
- `gui.widgets.text_button`
- `gui.widgets.text_edit`
- `gui.widgets.text_window`
- `main`
- `session`
- `session.providers`
- `session.providers.guest_provider`
- `session.session`
- `session.session_excel`
- `utils`
- `utils.paths`


## Development / Test Modules

- `tests`
- `tests.test_api_client`
- `tests.test_async_runner`
- `tests.test_asyncio`
- `tests.test_asyncio_loop`
- `tests.test_audio`
- `tests.test_auth`
- `tests.test_database`
- `tests.test_dictation_pause`
- `tests.test_dictation_plan`
- `tests.test_dictation_segmentation`
- `tests.test_dictation_validator`
- `tests.test_franch_voice`
- `tests.test_generator_router`
- `tests.test_import_to_session`
- `tests.test_openai`
- `tests.test_real_session_excel`
- `tests.test_session_excel`
- `tests.test_shadowing_generator`
- `tests.test_shadowing_pause`
- `tests.test_shadowing_segmenter`
- `tests.test_state`
- `tests.test_tts_languages`
- `tests.test_tts_voices`


## Tools

Project utility modules used for analysis, documentation generation, and project maintenance.

- `tools.docs_audit`
- `tools.docs_generator`
- `tools.docs_nav_generator`
- `tools.project_dependencies`
- `tools.project_import_map`
- `tools.project_paths`
- `tools.project_statistics`
- `tools.project_tree`


## Modules Without Internal Dependencies

These modules do not import another project module.

- `ai`
- `ai.dictation_pause`
- `ai.generators`
- `ai.models`
- `ai.shadowing_pause`
- `api`
- `api.client`
- `audio`
- `audio.async_runner`
- `audio.mixer`
- `audio.tts`
- `core`
- `docs.modules.gui.services`
- `gui`
- `gui.dialogs`
- `gui.file_dialog`
- `gui.layout`
- `gui.manager`
- `gui.panels`
- `gui.services`
- `gui.services.image_loader`
- `gui.theme`
- `gui.widgets`
- `gui.widgets.image_button`
- `gui.widgets.label`
- `gui.widgets.list_selection`
- `hooks.import_map`
- `session`
- `session.providers`
- `session.providers.guest_provider`
- `session.session`
- `session.session_excel`
- `site.modules.gui.services`
- `tests`
- `tests.test_asyncio`
- `tests.test_asyncio_loop`
- `tests.test_database`
- `tests.test_franch_voice`
- `tests.test_state`
- `tools`
- `tools.project_paths`
- `utils`
- `utils.paths`

---

*Generated automatically by `project_statistics.py`.*
