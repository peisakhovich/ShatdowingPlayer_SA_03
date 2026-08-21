from __future__ import annotations

import asyncio
from pathlib import Path
import inspect

import pygame

from gui.theme import Theme
from gui.layout import Layout
from gui.widgets.list_selection import ListSelection
from gui.file_dialog import FileDialog
from gui.widgets.text_edit import TextEdit
from gui.widgets.busy_indicator import BusyIndicator

from audio.tts import TTS
from audio.async_runner import AsyncRunner

from ai.language_detector import LanguageDetector
from ai.generators.generator_router import GeneratorRouter

from core.config import Config


class SettingsWindow:
    """Модальное окно настроек."""

    # ==================================================
    # INIT
    # ==================================================

    def __init__(self, rect, scenario, session):

        # --------------------------------------------------
        # Основные данные
        # --------------------------------------------------

        self.rect = pygame.Rect(rect)
        self.visible = False

        self.scenario_provider = scenario
        self.session = session

        # --------------------------------------------------
        # Async tasks
        # --------------------------------------------------

        self._languages_task = None

        self._source_locale_task = None
        self._target_locale_task = None

        self._source_voice_task = None
        self._target_voice_task = None

        self._language_task = None
        self._generate_task = None

        # --------------------------------------------------
        # Source
        # --------------------------------------------------

        self.source_file = ""
        self.source_text = ""

        # --------------------------------------------------
        # Services
        # --------------------------------------------------

        self._tts = TTS()
        self._async_runner = AsyncRunner()

        self._language_detector = LanguageDetector()
        self._generator_router = GeneratorRouter()

        # --------------------------------------------------
        # Close
        # --------------------------------------------------

        self.close_rect = pygame.Rect(
            self.rect.right - 35,
            self.rect.top + 12,
            22,
            22,
        )

        # ==================================================
        # SCENARIO
        # ==================================================

        self.scenario_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 90,
                self.rect.width - 60,
                34,
            ),
            self.scenario_provider.get_scenario_list(),
            self.scenario_provider.get_current_scenario_index(),
            max_visible_items=6,
        )

        # ==================================================
        # SOURCE FILE
        # ==================================================

        self.file_button_rect = pygame.Rect(
            self.rect.x + 30,
            self.rect.y + 175,
            125,
            34,
        )

        # ==================================================
        # SOURCE TEXT
        # ==================================================

        self.text_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 240,
                self.rect.width - 60,
                135,
            ),
            pygame.font.Font(None, 24),
        )

        # ==================================================
        # SOURCE LANGUAGE
        # ==================================================

        self.source_language_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 415,
                self.rect.width - 60,
                34,
            ),
            [("", "Loading...")],
            0,
            max_visible_items=8,
        )

        # ==================================================
        # TARGET LANGUAGE
        # ==================================================

        self.target_language_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 480,
                self.rect.width - 60,
                34,
            ),
            [("", "Loading...")],
            0,
            max_visible_items=8,
        )

        # ==================================================
        # SOURCE VOICE
        # ==================================================

        self.source_voice_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 545,
                self.rect.width - 60,
                34,
            ),
            [("", "Loading...")],
            0,
            max_visible_items=8,
        )

        # ==================================================
        # TARGET VOICE
        # ==================================================

        self.target_voice_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 610,
                self.rect.width - 60,
                34,
            ),
            [("", "Loading...")],
            0,
            max_visible_items=8,
        )

        # ==================================================
        # REPEAT COUNT
        # ==================================================

        self.repeat_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 680,
                100,
                34,
            ),
            pygame.font.Font(None, 24),
        )

        # ==================================================
        # PAUSE FACTOR
        # ==================================================

        self.pause_factor_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 240,
                self.rect.y + 680,
                100,
                34,
            ),
            pygame.font.Font(None, 24),
        )

        # ==================================================
        # GENERATE
        # ==================================================

        self.generate_button_rect = pygame.Rect(
            self.rect.x + 30,
            self.rect.y + 730,
            125,
            34,
        )

        # ==================================================
        # BUSY
        # ==================================================

        self.busy_indicator = BusyIndicator(
            self.rect,
            pygame.font.Font(None, 22),
        )

        # ==================================================
        # INITIAL DATA
        # ==================================================

        self._load_current_item_parameters()

        self._load_languages()

    # ==================================================
    # SCENARIO
    # ==================================================

    def _get_scenario(self):

        return self.scenario_provider.get_current()

    # --------------------------------------------------

    def _is_shadowing(self):

        return self._get_scenario() == "shadowing"

    # --------------------------------------------------

    def _is_dictation(self):

        return self._get_scenario() == "dictation"

    # ==================================================
    # LANGUAGE LIST
    # ==================================================

    def _load_languages(self):

        if self._languages_task is not None:

            if not self._languages_task.done():
                self._languages_task.cancel()

        self.source_language_selection.options = [
            ("", "Loading...")
        ]

        self.source_language_selection.selected = 0

        self.target_language_selection.options = [
            ("", "Loading...")
        ]

        self.target_language_selection.selected = 0

        self.busy_indicator.show(
            "Loading languages..."
        )

        self._languages_task = (
            self._async_runner.submit(
                self._tts.get_languages()
            )
        )

    # --------------------------------------------------

    def _process_languages_task(self):

        if self._languages_task is None:
            return

        if not self._languages_task.done():
            return

        task = self._languages_task
        self._languages_task = None

        try:

            languages = task.result()

        except asyncio.CancelledError:

            return

        except Exception as e:

            print(
                "TTS language error:",
                e
            )

            self.source_language_selection.options = [
                ("", "Error")
            ]

            self.target_language_selection.options = [
                ("", "Error")
            ]

            self.busy_indicator.hide()

            return

        if not languages:

            self.source_language_selection.options = [
                ("", "No languages")
            ]

            self.target_language_selection.options = [
                ("", "No languages")
            ]

            self.busy_indicator.hide()

            return

        options = []

        for language in languages:

            options.append(
                (
                    language,
                    language
                )
            )

        # --------------------------------------------------
        # Source language
        # --------------------------------------------------

        self.source_language_selection.options = options

        source_code = self._get_current_source_language()

        self.source_language_selection.selected = (
            self._find_option_index(
                options,
                source_code
            )
        )

        # --------------------------------------------------
        # Target language
        # --------------------------------------------------

        self.target_language_selection.options = options

        target_code = self._get_current_target_language()

        self.target_language_selection.selected = (
            self._find_option_index(
                options,
                target_code
            )
        )

        # --------------------------------------------------
        # Load source locale
        # --------------------------------------------------

        source_language = (
            self.source_language_selection.value
        )

        if source_language:

            self._load_source_locales(
                source_language
            )

        # --------------------------------------------------
        # Load target locale
        # --------------------------------------------------

        if self._is_shadowing():

            target_language = (
                self.target_language_selection.value
            )

            if target_language:

                self._load_target_locales(
                    target_language
                )

        else:

            self.busy_indicator.hide()

    # ==================================================
    # CURRENT PARAMETERS
    # ==================================================

    def _load_current_item_parameters(self):

        item = self.session.current_item

        if not item:
            return

        # --------------------------------------------------
        # Repeat
        # --------------------------------------------------

        repeat_count = item.get(
            "repeat_count",
            1
        )

        self.repeat_edit.set_text(
            str(repeat_count)
        )

        # --------------------------------------------------
        # Pause
        # --------------------------------------------------

        self.pause_factor_edit.set_text(
            "1.0"
        )

    # --------------------------------------------------

    def _get_current_source_language(self):

        item = self.session.current_item

        if not item:
            return ""

        language = item.get(
            "phrase_code",
            ""
        )

        return language.lower()

    # --------------------------------------------------

    def _get_current_target_language(self):

        item = self.session.current_item

        if not item:
            return ""

        language = item.get(
            "translate_code",
            ""
        )

        return language.lower()

    # --------------------------------------------------

    def _find_option_index(
        self,
        options,
        value,
    ):

        for index, (option_value, _) in enumerate(
            options
        ):

            if option_value.lower() == value.lower():

                return index

        return 0

    # ==================================================
    # LANGUAGE DETECTION
    # ==================================================

    def _detect_language(self, text):

        if not text.strip():
            return

        sample = text[:1000]

        if self._language_task is not None:

            if not self._language_task.done():
                self._language_task.cancel()

        self.busy_indicator.show(
            "Detecting language..."
        )

        self._language_task = (
            self._async_runner.submit(
                self._detect_language_async(
                    sample
                )
            )
        )

    # --------------------------------------------------

    async def _detect_language_async(
        self,
        text,
    ):

        return self._language_detector.detect(
            text
        )

    # --------------------------------------------------

    def _process_language_task(self):

        if self._language_task is None:
            return

        if not self._language_task.done():
            return

        task = self._language_task
        self._language_task = None

        try:

            language = task.result()

        except asyncio.CancelledError:

            return

        except Exception as e:

            print(
                "AI language detection error:",
                e
            )

            self.busy_indicator.hide()

            return

        if not language:
            self.busy_indicator.hide()
            return

        language = language.lower()

        print(
            "Detected source language:",
            language
        )

        # --------------------------------------------------
        # Выбираем обнаруженный язык
        # --------------------------------------------------

        self._select_language(
            self.source_language_selection,
            language
        )

        # --------------------------------------------------
        # Загружаем locale
        # --------------------------------------------------

        self._load_source_locales(
            language
        )

    # --------------------------------------------------

    def _select_language(
        self,
        selection,
        language,
    ):

        for index, (value, _) in enumerate(
            selection.options
        ):

            if value.lower() == language.lower():

                selection.selected = index
                return

    # ==================================================
    # SOURCE LOCALES
    # ==================================================

    def _load_source_locales(
        self,
        language,
    ):

        if not language:
            return

        if self._source_locale_task is not None:

            if not self._source_locale_task.done():
                self._source_locale_task.cancel()

        if self._source_voice_task is not None:

            if not self._source_voice_task.done():
                self._source_voice_task.cancel()

        self.source_voice_selection.options = [
            ("", "No voice")
        ]

        self.source_voice_selection.selected = 0

        self.source_language_selection.opened = False

        self._source_locale_task = (
            self._async_runner.submit(
                self._tts.get_locales_for_language(
                    language
                )
            )
        )

    # --------------------------------------------------

    def _process_source_locale_task(self):

        if self._source_locale_task is None:
            return

        if not self._source_locale_task.done():
            return

        task = self._source_locale_task
        self._source_locale_task = None

        try:

            locales = task.result()

        except asyncio.CancelledError:

            return

        except Exception as e:

            print(
                "Source locale error:",
                e
            )

            self.source_voice_selection.options = [
                ("", "Error")
            ]

            self.busy_indicator.hide()

            return

        if not locales:

            self.source_voice_selection.options = [
                ("", "No locales")
            ]

            self.busy_indicator.hide()

            return

        options = [
            (locale, locale)
            for locale in locales
        ]

        current_locale = ""

        item = self.session.current_item

        if item:

            current_locale = item.get(
                "phrase_locale",
                ""
            )

        selected = self._find_option_index(
            options,
            current_locale
        )

        self.source_language_selection.opened = False

        # Locale is stored separately from language.
        self._source_locale_options = options

        # Load voices.
        self._load_source_voice_for_locale(
            options[selected][0]
        )

    # --------------------------------------------------

    def _load_source_voice_for_locale(
        self,
        locale,
    ):

        if self._source_voice_task is not None:

            if not self._source_voice_task.done():
                self._source_voice_task.cancel()

        self.source_voice_selection.options = [
            ("", "Loading...")
        ]

        self.source_voice_selection.selected = 0

        self._source_voice_task = (
            self._async_runner.submit(
                self._tts.get_voices_for_locale(
                    locale
                )
            )
        )

    # --------------------------------------------------

    def _process_source_voice_task(self):

        if self._source_voice_task is None:
            return

        if not self._source_voice_task.done():
            return

        task = self._source_voice_task
        self._source_voice_task = None

        try:

            voices = task.result()

        except asyncio.CancelledError:

            return

        except Exception as e:

            print(
                "Source voice error:",
                e
            )

            self.source_voice_selection.options = [
                ("", "Error")
            ]

            self.busy_indicator.hide()

            return

        self._set_voice_options(
            self.source_voice_selection,
            voices,
            "phrase_voice"
        )

        if not self._is_shadowing():

            self.busy_indicator.hide()

    # ==================================================
    # TARGET LOCALES
    # ==================================================

    def _load_target_locales(
        self,
        language,
    ):

        if not language:
            return

        if self._target_locale_task is not None:

            if not self._target_locale_task.done():
                self._target_locale_task.cancel()

        if self._target_voice_task is not None:

            if not self._target_voice_task.done():
                self._target_voice_task.cancel()

        self.target_voice_selection.options = [
            ("", "No voice")
        ]

        self.target_voice_selection.selected = 0

        self._target_locale_task = (
            self._async_runner.submit(
                self._tts.get_locales_for_language(
                    language
                )
            )
        )

    # --------------------------------------------------

    def _process_target_locale_task(self):

        if self._target_locale_task is None:
            return

        if not self._target_locale_task.done():
            return

        task = self._target_locale_task
        self._target_locale_task = None

        try:

            locales = task.result()

        except asyncio.CancelledError:

            return

        except Exception as e:

            print(
                "Target locale error:",
                e
            )

            self.target_voice_selection.options = [
                ("", "Error")
            ]

            self.busy_indicator.hide()

            return

        if not locales:

            self.target_voice_selection.options = [
                ("", "No locales")
            ]

            self.busy_indicator.hide()

            return

        options = [
            (locale, locale)
            for locale in locales
        ]

        current_locale = ""

        item = self.session.current_item

        if item:

            current_locale = item.get(
                "translate_locale",
                ""
            )

        selected = self._find_option_index(
            options,
            current_locale
        )

        self._target_locale_options = options

        self._load_target_voice_for_locale(
            options[selected][0]
        )

    # --------------------------------------------------

    def _load_target_voice_for_locale(
        self,
        locale,
    ):

        if self._target_voice_task is not None:

            if not self._target_voice_task.done():
                self._target_voice_task.cancel()

        self.target_voice_selection.options = [
            ("", "Loading...")
        ]

        self.target_voice_selection.selected = 0

        self._target_voice_task = (
            self._async_runner.submit(
                self._tts.get_voices_for_locale(
                    locale
                )
            )
        )

    # --------------------------------------------------

    def _process_target_voice_task(self):

        if self._target_voice_task is None:
            return

        if not self._target_voice_task.done():
            return

        task = self._target_voice_task
        self._target_voice_task = None

        try:

            voices = task.result()

        except asyncio.CancelledError:

            return

        except Exception as e:

            print(
                "Target voice error:",
                e
            )

            self.target_voice_selection.options = [
                ("", "Error")
            ]

            self.busy_indicator.hide()

            return

        self._set_voice_options(
            self.target_voice_selection,
            voices,
            "translate_voice"
        )

        self.busy_indicator.hide()

    # ==================================================
    # VOICE OPTIONS
    # ==================================================

    def _set_voice_options(
        self,
        selection,
        voices,
        item_key,
    ):

        if not voices:

            selection.options = [
                ("", "No voices")
            ]

            selection.selected = 0

            return

        options = []

        for voice in voices:

            short_name = voice.get(
                "short_name",
                ""
            )

            gender = voice.get(
                "gender",
                ""
            )

            caption = short_name

            if gender:

                caption += (
                    f" | {gender}"
                )

            options.append(
                (
                    short_name,
                    caption
                )
            )

        selection.options = options

        current_voice = ""

        item = self.session.current_item

        if item:

            current_voice = item.get(
                item_key,
                ""
            )

        selection.selected = (
            self._find_option_index(
                options,
                current_voice
            )
        )

    # ==================================================
    # VISIBILITY
    # ==================================================

    def show(self):

        self.visible = True

        self._load_current_item_parameters()

        self._load_languages()

    # --------------------------------------------------

    def hide(self):

        self._cancel_tasks()

        self.visible = False

    # --------------------------------------------------

    def _cancel_tasks(self):

        tasks = (
            self._languages_task,
            self._source_locale_task,
            self._target_locale_task,
            self._source_voice_task,
            self._target_voice_task,
            self._language_task,
            self._generate_task,
        )

        for task in tasks:

            if task is not None:

                if not task.done():
                    task.cancel()

        self._languages_task = None
        self._source_locale_task = None
        self._target_locale_task = None
        self._source_voice_task = None
        self._target_voice_task = None
        self._language_task = None
        self._generate_task = None

        self.busy_indicator.hide()

    # ==================================================
    # TEXT FIT
    # ==================================================

    def _fit_text(
        self,
        text,
        font,
        max_width,
    ):

        if font.size(text)[0] <= max_width:
            return text

        while len(text) > 3:

            text = text[1:]

            candidate = "..." + text

            if font.size(candidate)[0] <= max_width:
                return candidate

        return "..."

    # ==================================================
    # GENERATOR RUNNER
    # ==================================================

    async def _run_generator(
        self,
        generator,
        kwargs,
    ):

        result = generator.generate(
            **kwargs
        )

        if inspect.isawaitable(result):

            result = await result

        return result

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.visible:
            return

        self.text_edit.update()

        self.repeat_edit.update()

        self.pause_factor_edit.update()

        self._process_languages_task()

        self._process_language_task()

        self._process_source_locale_task()

        self._process_target_locale_task()

        self._process_source_voice_task()

        self._process_target_voice_task()

        self._process_generate_task()

        self.busy_indicator.update()

    # ==================================================
    # GENERATE TASK
    # ==================================================

    def _process_generate_task(self):

        if self._generate_task is None:
            return

        if not self._generate_task.done():
            return

        task = self._generate_task
        self._generate_task = None

        try:

            plan = task.result()

        except asyncio.CancelledError:

            return

        except Exception as e:

            print(
                "Generation error:",
                e
            )

            self.busy_indicator.hide()

            return

        if not plan:

            print(
                "Generator returned empty plan"
            )

            self.busy_indicator.hide()

            return

        # --------------------------------------------------
        # Session
        # --------------------------------------------------

        self.session.load_data(
            plan
        )

        self.session.save(
            Config.PLAN_SESSION_FILE
        )

        self.busy_indicator.hide()

        print()
        print("==============================")
        print("PLAN GENERATED")
        print("==============================")
        print(
            "Scenario:",
            self._get_scenario()
        )
        print(
            "Items:",
            len(plan.get("items", []))
        )
        print("==============================")
        print()

    # ==================================================
    # EVENTS
    # ==================================================

    def handle_event(self, event):

        if not self.visible:
            return

        # --------------------------------------------------
        # Close while busy
        # --------------------------------------------------

        if (
            self.busy_indicator.visible
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.close_rect.collidepoint(event.pos)
        ):

            self.hide()
            return

        # --------------------------------------------------
        # Block interaction while busy
        # --------------------------------------------------

        if self.busy_indicator.visible:
            return

        # ==================================================
        # TEXT EDITS
        # ==================================================

        text_edits = (
            self.text_edit,
            self.repeat_edit,
            self.pause_factor_edit,
        )

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                clicked_edit = None

                for edit in text_edits:

                    if edit.rect.collidepoint(
                        event.pos
                    ):

                        clicked_edit = edit
                        break

                for edit in text_edits:

                    if edit is not clicked_edit:

                        edit.focused = False
                        edit.repeat_key = None

                if clicked_edit is not None:

                    clicked_edit.handle_event(
                        event
                    )

                else:

                    for edit in text_edits:

                        edit.handle_event(
                            event
                        )

            else:

                for edit in text_edits:

                    edit.handle_event(
                        event
                    )

        else:

            for edit in text_edits:

                edit.handle_event(
                    event
                )

        # ==================================================
        # SCENARIO
        # ==================================================

        result = self.scenario_selection.handle_event(
            event
        )

        if result is not None:

            self.scenario_provider.set_current(
                result[1]
            )

            print(
                "Scenario:",
                result[1]
            )

            self._load_current_item_parameters()

            # Перезагружаем языковые данные,
            # чтобы интерфейс соответствовал сценарию.
            self._load_languages()

            return

        # ==================================================
        # SOURCE LANGUAGE
        # ==================================================

        result = (
            self.source_language_selection.handle_event(
                event
            )
        )

        if result is not None:

            language = result[1]

            print(
                "Source language:",
                language
            )

            self._load_source_locales(
                language
            )

            return

        # ==================================================
        # TARGET LANGUAGE
        # ==================================================

        if self._is_shadowing():

            result = (
                self.target_language_selection.handle_event(
                    event
                )
            )

            if result is not None:

                language = result[1]

                print(
                    "Target language:",
                    language
                )

                self._load_target_locales(
                    language
                )

                return

        # ==================================================
        # SOURCE VOICE
        # ==================================================

        result = (
            self.source_voice_selection.handle_event(
                event
            )
        )

        if result is not None:

            print(
                "Source voice:",
                result[1]
            )

            return

        # ==================================================
        # TARGET VOICE
        # ==================================================

        if self._is_shadowing():

            result = (
                self.target_voice_selection.handle_event(
                    event
                )
            )

            if result is not None:

                print(
                    "Target voice:",
                    result[1]
                )

                return

        # ==================================================
        # MOUSE BUTTONS
        # ==================================================

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button != 1:
            return

        # --------------------------------------------------
        # Close
        # --------------------------------------------------

        if self.close_rect.collidepoint(
            event.pos
        ):

            self.hide()
            return

        # --------------------------------------------------
        # File
        # --------------------------------------------------

        if self.file_button_rect.collidepoint(
            event.pos
        ):

            filename = FileDialog.open_file(
                title="Choose source text",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*"),
                ]
            )

            if filename:

                self.source_file = filename

                try:

                    text = Path(
                        filename
                    ).read_text(
                        encoding="utf-8"
                    )

                except UnicodeDecodeError:

                    text = Path(
                        filename
                    ).read_text(
                        encoding="utf-16"
                    )

                self.source_text = text

                self.text_edit.set_text(
                    text
                )

                self._detect_language(
                    text
                )

            return

        # --------------------------------------------------
        # Generate
        # --------------------------------------------------

        if self.generate_button_rect.collidepoint(
            event.pos
        ):

            self._generate()

    # ==================================================
    # GENERATE
    # ==================================================

    def _generate(self):

        # --------------------------------------------------
        # Duplicate generation
        # --------------------------------------------------

        if self._generate_task is not None:

            print(
                "Generation already in progress"
            )

            return

        # --------------------------------------------------
        # Text
        # --------------------------------------------------

        text = (
            self.text_edit.get_text()
            .strip()
        )

        if not text:

            print(
                "Source text is empty"
            )

            return

        # --------------------------------------------------
        # Session item
        # --------------------------------------------------

        item = self.session.current_item

        if not item:

            print(
                "Current session item is missing"
            )

            return

        # --------------------------------------------------
        # Repeat
        # --------------------------------------------------

        try:

            repeat_count = int(
                self.repeat_edit.get_text()
            )

            if repeat_count < 1:
                raise ValueError

        except ValueError:

            print(
                "Invalid repeat count"
            )

            return

        # --------------------------------------------------
        # Pause factor
        # --------------------------------------------------

        try:

            pause_factor = float(
                self.pause_factor_edit.get_text()
            )

            if pause_factor <= 0:
                raise ValueError

        except ValueError:

            print(
                "Invalid pause factor"
            )

            return

        # --------------------------------------------------
        # Scenario
        # --------------------------------------------------

        scenario = self._get_scenario()

        # --------------------------------------------------
        # Source language
        # --------------------------------------------------

        source_language = (
            self.source_language_selection.value
        )

        # --------------------------------------------------
        # Source locale / voice
        # --------------------------------------------------

        phrase_locale = self._get_selected_locale(
            source_language,
            source=True
        )

        phrase_voice = (
            self.source_voice_selection.value
        )

        phrase_code = (
            phrase_locale.split("-")[0].lower()
            if phrase_locale
            else source_language
        )

        phrase_voice_gender = (
            item.get(
                "phrase_voice_gender",
                ""
            )
        )

        # --------------------------------------------------
        # Basic validation
        # --------------------------------------------------

        if (
            not source_language
            or not phrase_locale
            or not phrase_voice
        ):

            print(
                "Incomplete source voice parameters"
            )

            return

        # ==================================================
        # DICTATION
        # ==================================================

        if scenario == "dictation":

            kwargs = {
                "text": text,
                "scenario": scenario,

                "phrase_code": phrase_code,
                "phrase_locale": phrase_locale,
                "phrase_voice": phrase_voice,
                "phrase_voice_gender": (
                    phrase_voice_gender
                ),

                "repeat_count": repeat_count,
                "pause_factor": pause_factor,
            }

        # ==================================================
        # SHADOWING
        # ==================================================

        elif scenario == "shadowing":

            target_language = (
                self.target_language_selection.value
            )

            translate_locale = (
                self._get_selected_locale(
                    target_language,
                    source=False
                )
            )

            translate_voice = (
                self.target_voice_selection.value
            )

            translate_code = (
                translate_locale
                .split("-")[0]
                .lower()
                if translate_locale
                else target_language
            )

            translate_voice_gender = (
                item.get(
                    "translate_voice_gender",
                    ""
                )
            )

            if (
                not target_language
                or not translate_locale
                or not translate_voice
            ):

                print(
                    "Incomplete target voice parameters"
                )

                return

            kwargs = {
                "text": text,

                "source_language": source_language,
                "target_language": target_language,

                "phrase_code": phrase_code,
                "phrase_locale": phrase_locale,
                "phrase_voice": phrase_voice,
                "phrase_voice_gender": (
                    phrase_voice_gender
                ),

                "translate_code": translate_code,
                "translate_locale": translate_locale,
                "translate_voice": translate_voice,
                "translate_voice_gender": (
                    translate_voice_gender
                ),

                "speed": 1.0,
                "repeat_count": repeat_count,

                "pause_factor": pause_factor,

                "pause_min": 500,
                "pause_max": 5000,

                "set_name": "Shadowing",
                "set_description": (
                    "Generated shadowing session"
                ),
            }

        else:

            print(
                f"Unsupported scenario: {scenario}"
            )

            return

        # ==================================================
        # ROUTER
        # ==================================================

        try:

            generator = (
                self._generator_router.get_generator(
                    scenario
                )
            )

        except ValueError as e:

            print(e)

            return

        # ==================================================
        # START
        # ==================================================

        print(
            "Generating:",
            scenario
        )

        self.busy_indicator.show(
            f"Generating {scenario}..."
        )

        self._generate_task = (
            self._async_runner.submit(
                self._run_generator(
                    generator,
                    kwargs
                )
            )
        )

    # ==================================================
    # SELECTED LOCALE
    # ==================================================

    def _get_selected_locale(
        self,
        language,
        source=True,
    ):

        if source:

            options = getattr(
                self,
                "_source_locale_options",
                []
            )

        else:

            options = getattr(
                self,
                "_target_locale_options",
                []
            )

        if not options:
            return ""

        # --------------------------------------------------
        # Try current session locale
        # --------------------------------------------------

        item = self.session.current_item

        key = (
            "phrase_locale"
            if source
            else "translate_locale"
        )

        current_locale = ""

        if item:

            current_locale = item.get(
                key,
                ""
            )

        for value, _ in options:

            if value == current_locale:

                return value

        # --------------------------------------------------
        # Otherwise first locale
        # --------------------------------------------------

        return options[0][0]

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        if not self.visible:
            return

        # --------------------------------------------------
        # Fonts
        # --------------------------------------------------

        title_font = pygame.font.Font(
            None,
            28
        )

        caption_font = pygame.font.Font(
            None,
            22
        )

        list_font = pygame.font.Font(
            None,
            22
        )

        button_font = pygame.font.Font(
            None,
            22
        )

        # ==================================================
        # BACKGROUND
        # ==================================================

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BACKGROUND_COLOR,
            self.rect,
            border_radius=Theme.DIALOG_RADIUS,
        )

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BORDER_COLOR,
            self.rect,
            width=Theme.TB_BORDER_WIDTH,
            border_radius=Theme.DIALOG_RADIUS,
        )

        # ==================================================
        # TITLE
        # ==================================================

        title = title_font.render(
            "Settings",
            True,
            Theme.DIALOG_TITLE_COLOR
        )

        screen.blit(
            title,
            (
                self.rect.x + 15,
                self.rect.y + 12
            )
        )

        # ==================================================
        # CLOSE
        # ==================================================

        x = self.close_rect

        pygame.draw.line(
            screen,
            Theme.DIALOG_TITLE_COLOR,
            (x.left + 5, x.top + 5),
            (x.right - 5, x.bottom - 5),
            2,
        )

        pygame.draw.line(
            screen,
            Theme.DIALOG_TITLE_COLOR,
            (x.right - 5, x.top + 5),
            (x.left + 5, x.bottom - 5),
            2,
        )

        # ==================================================
        # SCENARIO
        # ==================================================

        self._draw_caption(
            screen,
            caption_font,
            "Playback scenario",
            self.scenario_selection.rect
        )

        # ==================================================
        # SOURCE FILE
        # ==================================================

        self._draw_caption(
            screen,
            caption_font,
            "Source text",
            pygame.Rect(
                self.file_button_rect.x,
                self.file_button_rect.y,
                self.file_button_rect.width,
                self.file_button_rect.height
            )
        )

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BORDER_COLOR,
            self.file_button_rect,
            border_radius=5
        )

        button_text = button_font.render(
            "Choose file...",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            button_text,
            (
                self.file_button_rect.x + 10,
                self.file_button_rect.y + 7
            )
        )

        if self.source_file:

            filename = Path(
                self.source_file
            ).name

            filename = self._fit_text(
                filename,
                caption_font,
                self.rect.right
                - self.file_button_rect.right
                - 45
            )

            file_text = caption_font.render(
                filename,
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            screen.blit(
                file_text,
                (
                    self.file_button_rect.right + 15,
                    self.file_button_rect.y + 7
                )
            )

        # ==================================================
        # TEXT
        # ==================================================

        self._draw_caption(
            screen,
            caption_font,
            "Text",
            self.text_edit.rect
        )

        self.text_edit.draw(
            screen
        )

        # ==================================================
        # SOURCE LANGUAGE
        # ==================================================

        self._draw_caption(
            screen,
            caption_font,
            "Source language",
            self.source_language_selection.rect
        )

        # ==================================================
        # TARGET LANGUAGE
        # ==================================================

        if self._is_shadowing():

            self._draw_caption(
                screen,
                caption_font,
                "Target language",
                self.target_language_selection.rect
            )

        # ==================================================
        # SOURCE VOICE
        # ==================================================

        self._draw_caption(
            screen,
            caption_font,
            "Source voice",
            self.source_voice_selection.rect
        )

        # ==================================================
        # TARGET VOICE
        # ==================================================

        if self._is_shadowing():

            self._draw_caption(
                screen,
                caption_font,
                "Target voice",
                self.target_voice_selection.rect
            )

        # ==================================================
        # REPEAT
        # ==================================================

        self._draw_caption(
            screen,
            caption_font,
            "Repeat count",
            self.repeat_edit.rect
        )

        self.repeat_edit.draw(
            screen
        )

        # ==================================================
        # PAUSE
        # ==================================================

        self._draw_caption(
            screen,
            caption_font,
            "Pause factor",
            self.pause_factor_edit.rect
        )

        self.pause_factor_edit.draw(
            screen
        )

        # ==================================================
        # GENERATE
        # ==================================================

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BORDER_COLOR,
            self.generate_button_rect,
            border_radius=5
        )

        button_text = button_font.render(
            "Generate",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            button_text,
            (
                self.generate_button_rect.x + 10,
                self.generate_button_rect.y + 7
            )
        )

        # ==================================================
        # DROPDOWNS
        # ==================================================

        # Рисуем dropdown последними.
        # Это важно, чтобы они были поверх остальных
        # элементов интерфейса.

        self.source_language_selection.draw(
            screen,
            list_font
        )

        if self._is_shadowing():

            self.target_language_selection.draw(
                screen,
                list_font
            )

        self.source_voice_selection.draw(
            screen,
            list_font
        )

        if self._is_shadowing():

            self.target_voice_selection.draw(
                screen,
                list_font
            )

        self.scenario_selection.draw(
            screen,
            list_font
        )

        # ==================================================
        # BUSY
        # ==================================================

        self.busy_indicator.draw(
            screen
        )

    # ==================================================
    # DRAW CAPTION
    # ==================================================

    def _draw_caption(
        self,
        screen,
        font,
        text,
        rect,
    ):

        caption = font.render(
            text,
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                rect.x,
                rect.y - 25
            )
        )