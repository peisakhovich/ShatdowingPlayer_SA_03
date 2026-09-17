# Project Statistics

Automatically generated statistics for **Sound Language Studio**.

The data is generated from the current Python project structure and import analysis.


## Project Overview

| Metric | Value |
|---|---:|
| Python files | 100 |
| Project modules | 100 |
| Application modules | 66 |
| Development / test modules | 29 |
| Other modules | 5 |
| Modules with internal imports | 53 |
| Modules without internal imports | 47 |
| Standard-library libraries | 17 |
| Third-party libraries | 9 |
| Architectural roots | 47 |


## Python Standard Library Usage

Number of project modules importing each standard-library module.

| Library | Modules using it |
|---|---:|
| `pathlib` | 22 |
| `asyncio` | 12 |
| `json` | 5 |
| `os` | 5 |
| `time` | 4 |
| `re` | 3 |
| `ast` | 2 |
| `threading` | 2 |
| `datetime` | 1 |
| `hashlib` | 1 |
| `logging` | 1 |
| `math` | 1 |
| `random` | 1 |
| `shutil` | 1 |
| `sys` | 1 |
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
| `pygame_gui` | 2 |
| `griffe` | 1 |
| `httpx` | 1 |
| `openai` | 1 |
| `pydantic` | 1 |


## Architectural Roots

Project modules identified as architectural roots by the import analysis.

- `ai`
- `ai.generators`
- `api`
- `audio`
- `core`
- `docs_audit`
- `docs_generator`
- `docs_nav_generator`
- `gui`
- `gui.dialogs`
- `gui.panels`
- `gui.services`
- `gui.widgets`
- `gui.widgets.label`
- `hooks.import_map`
- `main`
- `project_dependencies`
- `project_statistics`
- `project_tree`
- `session`
- `session.providers`
- `test_environment`
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
- `gui.widgets.text_button`
- `gui.widgets.text_edit`
- `gui.widgets.text_window`
- `session`
- `session.providers`
- `session.providers.guest_provider`
- `session.session`
- `session.session_excel`
- `utils`
- `utils.paths`


## Development / Test Modules

- `project_dependencies`
- `project_import_map`
- `project_statistics`
- `project_tree`
- `test_environment`
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


## Modules Without Internal Dependencies

These modules do not import another project module.

- `ai`
- `ai.dictation_pause`
- `ai.generators`
- `ai.models`
- `ai.openai_client`
- `ai.shadowing_pause`
- `api`
- `api.client`
- `audio`
- `audio.async_runner`
- `audio.mixer`
- `audio.tts`
- `core`
- `docs_audit`
- `docs_generator`
- `docs_nav_generator`
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
- `project_dependencies`
- `project_import_map`
- `project_tree`
- `session`
- `session.providers`
- `session.providers.guest_provider`
- `session.session`
- `session.session_excel`
- `test_environment`
- `tests`
- `tests.test_asyncio`
- `tests.test_asyncio_loop`
- `tests.test_database`
- `tests.test_franch_voice`
- `tests.test_state`
- `utils`
- `utils.paths`

---

*Generated automatically by `project_statistics.py`.*
