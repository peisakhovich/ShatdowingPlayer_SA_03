from __future__ import annotations

import asyncio
from pathlib import Path

import pygame

from gui.theme import Theme
from gui.widgets.list_selection import ListSelection
from gui.file_dialog import FileDialog
from gui.widgets.text_edit import TextEdit
from gui.widgets.busy_indicator import BusyIndicator

from audio.tts import TTS
from audio.async_runner import AsyncRunner

from ai.dictation_segmenter import DictationSegmenter
from ai.dictation_plan import DictationPlanBuilder
from ai.language_detector import LanguageDetector
from ai.generators.generator_router import GeneratorRouter

from core.config import Config


class SettingsWindow:
    """Модальное окно настроек."""

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

        self._locale_task = None
        self._voice_task = None
        self._language_task = None
        self._generate_task = None

        # TARGET tasks
        self._target_language_task = None
        self._target_locale_task = None
        self._target_voice_task = None

        # --------------------------------------------------
        # Source text
        # --------------------------------------------------

        self.source_file = ""
        self.source_text = ""

        # --------------------------------------------------
        # TTS
        # --------------------------------------------------

        self._tts = TTS()
        self._async_runner = AsyncRunner()

        # --------------------------------------------------
        # AI language detection
        # --------------------------------------------------

        self._language_detector = LanguageDetector()
        self._generator_router = GeneratorRouter()

        # --------------------------------------------------
        # Close button
        # --------------------------------------------------

        self.close_rect = pygame.Rect(
            self.rect.right - 30,
            self.rect.top + 10,
            20,
            20,
        )

        # --------------------------------------------------
        # Playback scenario
        # --------------------------------------------------

        self.scenario_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 80,
                400,
                30
            ),
            self.scenario_provider.get_scenario_list(),
            self.scenario_provider.get_current_scenario_index()
        )

        # --------------------------------------------------
        # Source file
        # --------------------------------------------------

        self.file_button_rect = pygame.Rect(
            self.rect.x + 450,
            self.rect.y + 80,
            120,
            32
        )

        # --------------------------------------------------
        # Source text
        # --------------------------------------------------

        self.text_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 150,
                self.rect.width - 60,
                200
            ),
            pygame.font.Font(None, 24)
        )

        # --------------------------------------------------
        # SOURCE LANGUAGE
        # --------------------------------------------------

        self.language_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 405,
                170,
                30
            ),
            [("", "Loading...")],
            0
        )

        # --------------------------------------------------
        # SOURCE LOCALE
        # --------------------------------------------------

        self.source_locale_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 215,
                self.rect.y + 405,
                self.rect.width - 245,
                30
            ),
            [("", "Loading...")],
            0
        )

        # --------------------------------------------------
        # SOURCE VOICE
        # --------------------------------------------------

        self.voice_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 470,
                self.rect.width - 60,
                30
            ),
            [("", "Loading...")],
            0
        )

        # --------------------------------------------------
        # TARGET LANGUAGE
        # --------------------------------------------------

        self.target_language_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 565,
                170,
                30
            ),
            [("", "Loading...")],
            0
        )

        # --------------------------------------------------
        # TARGET LOCALE
        # --------------------------------------------------

        self.target_locale_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 215,
                self.rect.y + 565,
                self.rect.width - 245,
                30
            ),
            [("", "Loading...")],
            0
        )

        # --------------------------------------------------
        # TARGET VOICE
        # --------------------------------------------------

        self.target_voice_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 630,
                self.rect.width - 60,
                30
            ),
            [("", "Loading...")],
            0
        )

        # --------------------------------------------------
        # REPEAT COUNT
        # --------------------------------------------------

        self.repeat_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 700,
                100,
                30
            ),
            pygame.font.Font(None, 24)
        )

        # --------------------------------------------------
        # PAUSE FACTOR
        # --------------------------------------------------

        self.pause_factor_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 240,
                self.rect.y + 700,
                100,
                30
            ),
            pygame.font.Font(None, 24)
        )

        # --------------------------------------------------
        # GENERATE BUTTON
        # --------------------------------------------------

        self.generate_button_rect = pygame.Rect(
            self.rect.x + 440,
            self.rect.y + 700,
            100,
            30
        )

        # --------------------------------------------------
        # Busy indicator
        # --------------------------------------------------

        self.busy_indicator = BusyIndicator(
            self.rect,
            pygame.font.Font(None, 22)
        )

        # --------------------------------------------------
        # Initial parameters
        # --------------------------------------------------

        self._load_current_item_parameters()

        # --------------------------------------------------
        # TARGET defaults
        # --------------------------------------------------

        self._load_target_languages()

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

        self._language_task = self._async_runner.submit(
            self._detect_language_async(sample)
        )

    async def _detect_language_async(self, text):

        return self._language_detector.detect(text)

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

            return

        if not language:
            return

        print(
            "Detected language:",
            language
        )

        self._load_locales(language)

    # ==================================================
    # INITIAL PARAMETERS
    # ==================================================

    def _load_current_item_parameters(self):

        item = self.session.current_item

        if not item:
            return

        locale = item.get(
            "phrase_locale",
            ""
        )

        if locale:

            self.language_selection.options = [
                (locale, locale)
            ]

            self.language_selection.selected = 0

            self._load_voices(locale)

        repeat_count = item.get(
            "repeat_count",
            1
        )

        self.repeat_edit.set_text(
            str(repeat_count)
        )

        self.pause_factor_edit.set_text(
            "1.0"
        )

    # ==================================================
    # TTS - SOURCE
    # ==================================================

    def _load_locales(self, language):

        if not language:
            return

        if self._locale_task is not None:

            if not self._locale_task.done():
                self._locale_task.cancel()

        if self._voice_task is not None:

            if not self._voice_task.done():
                self._voice_task.cancel()

        self.voice_selection.options = [
            ("", "No voice")
        ]

        self.voice_selection.selected = 0

        self.language_selection.options = [
            ("", "Loading...")
        ]

        self.language_selection.selected = 0

        self.busy_indicator.show(
            "Loading locales..."
        )

        self._locale_task = self._async_runner.submit(
            self._tts.get_locales_for_language(
                language
            )
        )

    def _load_voices(self, locale):

        if not locale:
            return

        if self._voice_task is not None:

            if not self._voice_task.done():
                self._voice_task.cancel()

        self.voice_selection.options = [
            ("", "Loading...")
        ]

        self.voice_selection.selected = 0

        self.busy_indicator.show(
            "Loading voices..."
        )

        self._voice_task = self._async_runner.submit(
            self._tts.get_voices_for_locale(
                locale
            )
        )

    def _process_locale_task(self):

        if self._locale_task is None:
            return

        if not self._locale_task.done():
            return

        task = self._locale_task
        self._locale_task = None

        try:

            locales = task.result()

        except asyncio.CancelledError:

            return

        except Exception as e:

            print(
                "TTS locale error:",
                e
            )

            self.language_selection.options = [
                ("", "Error")
            ]

            self.language_selection.selected = 0

            return

        if not locales:

            self.language_selection.options = [
                ("", "No locales")
            ]

            self.language_selection.selected = 0

            return

        options = [
            (locale, locale)
            for locale in locales
        ]

        self.language_selection.options = options

        selected_index = 0

        current_locale = ""

        item = self.session.current_item

        if item:

            current_locale = item.get(
                "phrase_locale",
                ""
            )

        for index, (value, _) in enumerate(options):

            if value == current_locale:

                selected_index = index
                break

        self.language_selection.selected = selected_index

        selected_locale = (
            self.language_selection.value
        )

        print(
            "Locale:",
            selected_locale
        )

        self._load_voices(
            selected_locale
        )

    def _process_voice_task(self):

        if self._voice_task is None:
            return

        if not self._voice_task.done():
            return

        task = self._voice_task
        self._voice_task = None

        try:

            voices = task.result()

        except asyncio.CancelledError:

            return

        except Exception as e:

            print(
                "TTS voice error:",
                e
            )

            self.voice_selection.options = [
                ("", "Error")
            ]

            self.voice_selection.selected = 0

            self.busy_indicator.hide()

            return

        if not voices:

            self.voice_selection.options = [
                ("", "No voices")
            ]

            self.voice_selection.selected = 0

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

        self.voice_selection.options = options

        current_voice = ""

        item = self.session.current_item

        if item:

            current_voice = item.get(
                "phrase_voice",
                ""
            )

        selected_index = 0

        for index, (value, _) in enumerate(options):

            if value == current_voice:

                selected_index = index
                break

        self.voice_selection.selected = selected_index

        self.busy_indicator.hide()

    # ==================================================
    # TTS - TARGET
    # ==================================================

    def _load_target_languages(self):

        print("TARGET: start loading languages")

        if self._target_language_task is not None:

            if not self._target_language_task.done():
                self._target_language_task.cancel()

        self.target_language_selection.options = [
            ("", "Loading...")
        ]

        self.target_language_selection.selected = 0

        self._target_language_task = (
            self._async_runner.submit(
                self._tts.get_languages()
            )
        )

    def _process_target_language_task(self):

        print(">>> PROCESS TARGET LANGUAGE TASK")

        if self._target_language_task is None:
            return

        if not self._target_language_task.done():
            return

        task = self._target_language_task
        self._target_language_task = None

        try:

            languages = task.result()

        except asyncio.CancelledError:

            return

        except Exception as e:

            print(
                "Target language error:",
                e
            )


            self.target_language_selection.options = [
                ("", "Error")
            ]

            self.target_language_selection.selected = 0

            return
        print("TARGET LANGUAGES:", languages)

        if not languages:

            self.target_language_selection.options = [
                ("", "No languages")
            ]

            self.target_language_selection.selected = 0

            return

        options = [
            (
                language,
                language
            )
            for language in languages
        ]

        self.target_language_selection.options = options

        # --------------------------------------------------
        # По умолчанию TARGET = English
        # --------------------------------------------------

        selected_index = 0

        for index, (value, _) in enumerate(options):

            if value.lower() == "en":

                selected_index = index
                break

        self.target_language_selection.selected = selected_index

        selected_language = (
            self.target_language_selection.value
        )

        print(
            "Target language:",
            selected_language
        )

        self._load_target_locales(
            selected_language
        )

    def _load_target_locales(self, language):

        if not language:
            return

        if self._target_locale_task is not None:

            if not self._target_locale_task.done():
                self._target_locale_task.cancel()

        if self._target_voice_task is not None:

            if not self._target_voice_task.done():
                self._target_voice_task.cancel()

        self.target_locale_selection.options = [
            ("", "Loading...")
        ]

        self.target_locale_selection.selected = 0

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

            self.target_locale_selection.options = [
                ("", "Error")
            ]

            self.target_locale_selection.selected = 0

            return

        print("TARGET LOCALES:", locales)

        if not locales:

            self.target_locale_selection.options = [
                ("", "No locales")
            ]

            self.target_locale_selection.selected = 0

            return

        options = [
            (
                locale,
                locale
            )
            for locale in locales
        ]

        self.target_locale_selection.options = options

        # --------------------------------------------------
        # Первый locale
        # --------------------------------------------------

        self.target_locale_selection.selected = 0

        selected_locale = (
            self.target_locale_selection.value
        )

        print(
            "Target locale:",
            selected_locale
        )

        self._load_target_voices(
            selected_locale
        )

    def _load_target_voices(self, locale):

        if not locale:
            return

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

            self.target_voice_selection.selected = 0

            return

        print("TARGET VOICES:", voices)

        if not voices:

            self.target_voice_selection.options = [
                ("", "No voices")
            ]

            self.target_voice_selection.selected = 0

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

        self.target_voice_selection.options = options

        # --------------------------------------------------
        # Первый голос
        # --------------------------------------------------

        self.target_voice_selection.selected = 0

        print(
            "Target voice:",
            self.target_voice_selection.value
        )

    # ==================================================
    # VISIBILITY
    # ==================================================

    def show(self):

        self.visible = True

        self._load_current_item_parameters()

        # TARGET всегда имеет свои независимые параметры.
        # При каждом открытии окна гарантируем наличие
        # цепочки language -> locale -> voice.
        self._load_target_languages()

    def hide(self):

        self._cancel_tasks()
        self.visible = False

    def _cancel_tasks(self):

        tasks = (
            self._locale_task,
            self._voice_task,
            self._language_task,
            self._generate_task,
            self._target_language_task,
            self._target_locale_task,
            self._target_voice_task,
        )

        for task in tasks:

            if task is not None:

                if not task.done():
                    task.cancel()

        self._locale_task = None
        self._voice_task = None
        self._language_task = None
        self._generate_task = None

        self._target_language_task = None
        self._target_locale_task = None
        self._target_voice_task = None

        self.busy_indicator.hide()

    # ==================================================
    # TEXT FIT
    # ==================================================

    def _fit_text(
        self,
        text,
        font,
        max_width
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
    # UPDATE
    # ==================================================

    def update(self):

        if not self.visible:
            return

        self.text_edit.update()
        self.repeat_edit.update()
        self.pause_factor_edit.update()

        self._process_language_task()
        self._process_locale_task()
        self._process_voice_task()
        self._process_generate_task()

        self._process_target_language_task()
        self._process_target_locale_task()
        self._process_target_voice_task()

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
                "Dictation generation error:",
                e
            )

            self.busy_indicator.hide()
            return

        self.session.load_data(plan)

        self.busy_indicator.hide()

        self.session.save(
            Config.PLAN_SESSION_FILE
        )

        print()
        print("==============================")
        print("DICTATION PLAN GENERATED")
        print("==============================")
        print(
            "Items:",
            len(plan["items"])
        )
        print("------------------------------")

        for item in plan["items"]:

            print(
                item["item_order"],
                item["phrase_text"],
                "| pause:",
                item["pause_ms"],
                "| repeat:",
                item["repeat_count"]
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

        # --------------------------------------------------
        # TextEdit
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Scenario
        # --------------------------------------------------

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

            # --------------------------------------------------
            # При переходе на Shadowing TARGET уже должен
            # быть заполнен. Если нет — запускаем цепочку.
            # --------------------------------------------------

            if result[1] == "shadowing":

                if (
                    not self.target_language_selection.options
                    or self.target_language_selection.value == ""
                ):

                    self._load_target_languages()

        # --------------------------------------------------
        # SOURCE language / locale
        # --------------------------------------------------

        result = self.language_selection.handle_event(
            event
        )

        if result is not None:

            locale = result[1]

            print(
                "Locale:",
                locale
            )

            self._load_voices(
                locale
            )

        # --------------------------------------------------
        # SOURCE voice
        # --------------------------------------------------

        result = self.voice_selection.handle_event(
            event
        )

        if result is not None:

            print(
                "Voice:",
                result[1]
            )

        # --------------------------------------------------
        # SOURCE locale
        # --------------------------------------------------

        result = self.source_locale_selection.handle_event(
            event
        )

        if result is not None:

            print(
                "Locale:",
                result[1]
            )

        # --------------------------------------------------
        # TARGET language
        # --------------------------------------------------

        if self.scenario_provider.get_current() == "shadowing":

            result = self.target_language_selection.handle_event(
                event
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

        # --------------------------------------------------
        # TARGET locale
        # --------------------------------------------------

        if self.scenario_provider.get_current() == "shadowing":

            result = self.target_locale_selection.handle_event(
                event
            )

            if result is not None:

                locale = result[1]

                print(
                    "Target locale:",
                    locale
                )

                self._load_target_voices(
                    locale
                )

        # --------------------------------------------------
        # TARGET voice
        # --------------------------------------------------

        if self.scenario_provider.get_current() == "shadowing":

            result = self.target_voice_selection.handle_event(
                event
            )

            if result is not None:

                print(
                    "Target voice:",
                    result[1]
                )

        # --------------------------------------------------
        # Mouse
        # --------------------------------------------------

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
        # Choose source file
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

        text = self.text_edit.get_text().strip()

        if not text:

            print(
                "Source text is empty"
            )

            return

        item = self.session.current_item

        if not item:

            print(
                "Current session item is missing"
            )

            return

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
        # SOURCE parameters
        # --------------------------------------------------

        phrase_locale = (
            self.language_selection.value
        )

        phrase_voice = (
            self.voice_selection.value
        )

        phrase_code = (
            phrase_locale.split("-")[0].lower()
            if phrase_locale
            else ""
        )

        phrase_voice_gender = (
            item.get(
                "phrase_voice_gender",
                ""
            )
        )

        if (
            not phrase_code
            or not phrase_locale
            or not phrase_voice
        ):

            print(
                "Incomplete voice parameters"
            )

            return

        # --------------------------------------------------
        # Scenario
        # --------------------------------------------------

        scenario = (
            self.scenario_provider.get_current()
        )

        # --------------------------------------------------
        # TARGET parameters
        # --------------------------------------------------

        target_language = ""
        target_locale = ""
        target_voice = ""

        if scenario == "shadowing":

            target_language = (
                self.target_language_selection.value
            )

            target_locale = (
                self.target_locale_selection.value
            )

            target_voice = (
                self.target_voice_selection.value
            )

            if (
                not target_language
                or not target_locale
                or not target_voice
            ):

                print(
                    "Incomplete target voice parameters"
                )

                return

        # --------------------------------------------------
        # Prevent duplicate generation
        # --------------------------------------------------

        if self._generate_task is not None:

            print(
                "Generation already in progress"
            )

            return

        # --------------------------------------------------
        # Generator Router
        # --------------------------------------------------

        try:

            generator = self._generator_router.get_generator(
                scenario
            )

        except ValueError as e:

            print(e)
            return

        print(
            "Generator:",
            type(generator).__name__
        )

        self.busy_indicator.show(
            "Generating dictation..."
        )

        self._generate_task = (
            self._async_runner.submit(
                self._generate_plan(
                    text=text,
                    scenario=scenario,
                    phrase_code=phrase_code,
                    phrase_locale=phrase_locale,
                    phrase_voice=phrase_voice,
                    phrase_voice_gender=phrase_voice_gender,
                    repeat_count=repeat_count,
                    pause_factor=pause_factor,
                    target_language=target_language,
                    target_locale=target_locale,
                    target_voice=target_voice,
                )
            )
        )

        print(
            "Generating dictation plan..."
        )

    # ==================================================
    # GENERATE PLAN
    # ==================================================

    async def _generate_plan(
        self,
        *,
        text,
        scenario,
        phrase_code,
        phrase_locale,
        phrase_voice,
        phrase_voice_gender,
        repeat_count,
        pause_factor,
        target_language="",
        target_locale="",
        target_voice="",
    ):

        # --------------------------------------------------
        # Пока сохраняем существующую рабочую реализацию
        # генерации Dictation.
        # --------------------------------------------------

        segmenter = DictationSegmenter()

        result = segmenter.segment(
            text
        )

        validated_data = {
            "original_text": result.original_text,

            "chunks": [
                {
                    "text": chunk.text,
                    "ends_sentence": chunk.ends_sentence,
                }

                for chunk in result.chunks
            ],

            "total_chunks": result.total_chunks,
        }

        builder = DictationPlanBuilder(

            phrase_code=phrase_code,
            phrase_locale=phrase_locale,
            phrase_voice=phrase_voice,
            phrase_voice_gender=phrase_voice_gender,

            speed=1.0,
            repeat_count=repeat_count,

            pause_factor=pause_factor,

            set_name="Dictation",
            set_description="Generated dictation session",
        )

        plan = builder.build(
            validated_data
        )

        plan["set"]["set_name"] = (
            f"Dictation - {scenario}"
        )

        return plan

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        if not self.visible:
            return

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

        # --------------------------------------------------
        # Background
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Close
        # --------------------------------------------------

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BACKGROUND_COLOR,
            self.close_rect
        )

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

        # --------------------------------------------------
        # Scenario
        # --------------------------------------------------

        caption = caption_font.render(
            "Playback scenario",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.scenario_selection.rect.x,
                self.scenario_selection.rect.y - 25
            )
        )

        # --------------------------------------------------
        # Source text
        # --------------------------------------------------

        caption = caption_font.render(
            "Source text",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.scenario_selection.rect.x + 425,
                self.scenario_selection.rect.y - 25
            )
        )

        # --------------------------------------------------
        # File button
        # --------------------------------------------------

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

        # --------------------------------------------------
        # File name
        # --------------------------------------------------

        if self.source_file:

            filename = Path(
                self.source_file
            ).name

            filename = self._fit_text(
                filename,
                caption_font,
                self.rect.right
                - self.file_button_rect.right
                - 30
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

        # --------------------------------------------------
        # TextEdit
        # --------------------------------------------------

        caption = caption_font.render(
            "Text",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.text_edit.rect.x,
                self.text_edit.rect.y - 25
            )
        )

        self.text_edit.draw(
            screen
        )

        # --------------------------------------------------
        # SOURCE Language
        # --------------------------------------------------

        caption = caption_font.render(
            "Language",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.language_selection.rect.x,
                self.language_selection.rect.y - 25
            )
        )

        # --------------------------------------------------
        # SOURCE Locale
        # --------------------------------------------------

        caption = caption_font.render(
            "Locale",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.source_locale_selection.rect.x,
                self.source_locale_selection.rect.y - 25
            )
        )

        # --------------------------------------------------
        # SOURCE Voice
        # --------------------------------------------------

        caption = caption_font.render(
            "Voice",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.voice_selection.rect.x,
                self.voice_selection.rect.y - 25
            )
        )

        # --------------------------------------------------
        # Repeat count
        # --------------------------------------------------

        caption = caption_font.render(
            "Repeat count",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.repeat_edit.rect.x,
                self.repeat_edit.rect.y - 25
            )
        )

        self.repeat_edit.draw(
            screen
        )

        # --------------------------------------------------
        # Pause factor
        # --------------------------------------------------

        caption = caption_font.render(
            "Pause factor",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.pause_factor_edit.rect.x,
                self.pause_factor_edit.rect.y - 25
            )
        )

        self.pause_factor_edit.draw(
            screen
        )

        # --------------------------------------------------
        # Generate
        # --------------------------------------------------

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

        # --------------------------------------------------
        # TARGET captions
        # --------------------------------------------------

        if self.scenario_provider.get_current() == "shadowing":

            caption = caption_font.render(
                "Target language",
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            screen.blit(
                caption,
                (
                    self.target_language_selection.rect.x,
                    self.target_language_selection.rect.y - 25
                )
            )

            caption = caption_font.render(
                "Target locale",
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            screen.blit(
                caption,
                (
                    self.target_locale_selection.rect.x,
                    self.target_locale_selection.rect.y - 25
                )
            )

            caption = caption_font.render(
                "Target voice",
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            screen.blit(
                caption,
                (
                    self.target_voice_selection.rect.x,
                    self.target_voice_selection.rect.y - 25
                )
            )

        # --------------------------------------------------
        # Dropdowns
        #
        # Рисуем последними.
        # --------------------------------------------------

        self.scenario_selection.draw(
            screen,
            list_font
        )

        if self.scenario_provider.get_current() == "shadowing":

            self.target_language_selection.draw(
                screen,
                list_font
            )

            self.target_locale_selection.draw(
                screen,
                list_font
            )

            self.target_voice_selection.draw(
                screen,
                list_font
            )

        self.voice_selection.draw(
            screen,
            list_font
        )

        self.language_selection.draw(
            screen,
            list_font
        )

        self.source_locale_selection.draw(
            screen,
            list_font
        )

        # --------------------------------------------------
        # Busy indicator
        # --------------------------------------------------

        self.busy_indicator.draw(
            screen
        )