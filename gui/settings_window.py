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

from ai.language_detector import LanguageDetector
from ai.generators.generator_router import GeneratorRouter

from core.config import Config
from gui.dialogs.dialog import Dialog
from core.logger import logger


class SettingsWindow:
    """Модальное окно настроек."""

    def __init__(self, rect, scenario_provider, session, font_manager):

        # --------------------------------------------------
        # Основные данные
        # --------------------------------------------------

        self.rect = pygame.Rect(rect)
        self.visible = False

        self.active_dialog = None


        self.scenario_provider = scenario_provider
        self.session = session
        self.font_manager = font_manager

        # --------------------------------------------------
        # Async tasks
        # --------------------------------------------------

        self._locale_task = None
        self._voice_task = None
        self._language_task = None
        self._generate_task = None

        self._target_language_task = None
        self._target_locale_task = None
        self._target_voice_task = None

        self._language_check_for_generate = False
        self._detected_generate_language = ""


        # --------------------------------------------------
        # Source text
        # --------------------------------------------------

        self.source_file = ""

        self.source_text = ( #Initial help in the text window
            'You can type text here or load text from a file. '
            'To do this, press the "Choose file..." button. '
            'After loading, the source locale and voice will be detected automatically. '
            'For some scenarios, you can generate a training session from the text. '
            'Press "Generate" to create the plan.'
        )

        self.source_language = "en"
        self.phrase_locale = "en-US"
        


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
                300,
                30
            ),
            self.scenario_provider.get_scenario_list(),
            self.scenario_provider.get_current_scenario_index()
        )


        # --------------------------------------------------
        # Source file
        # --------------------------------------------------

        self.file_button_rect = pygame.Rect(
            self.rect.x + self.rect.width-150,
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
                self.rect.height -500
            ),
            pygame.font.Font(None, 24)
        )
        self.text_edit.set_text(self.source_text) # Inserting help as first one text

        # --------------------------------------------------
        # Source locale / voice
        # --------------------------------------------------

        # --------------------------------------------------
        # SOURCE LOCALE
        # --------------------------------------------------

        self.source_locale_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + self.rect.height - 300,
                100,
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
                self.rect.x + 150,
                self.rect.y + self.rect.height - 300,
                self.rect.width - 180,
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
                self.rect.y + self.rect.height - 220,
                100,
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
                self.rect.x + 150,
                self.rect.y + self.rect.height - 220,
                100 ,
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
                self.rect.y + self.rect.height - 140,
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
                self.rect.y + self.rect.height - 60,
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
                self.rect.y + self.rect.height - 60,
                100,
                30
            ),
            pygame.font.Font(None, 24)
        )

        # --------------------------------------------------
        # GENERATE BUTTON
        # --------------------------------------------------

        self.generate_button_rect = pygame.Rect(
            self.rect.x + 410,
            self.rect.y + self.rect.height - 60,
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

    # ==================================================
    # LANGUAGE mismatch dialog
    # ==================================================

    def _show_language_mismatch_dialog(
        self,
        detected_language,
    ):

        self._detected_generate_language = (
            detected_language
        )

        self.active_dialog = Dialog(

            parent_rect=self.rect,

            font_manager=self.font_manager,

            title="Language mismatch",

            message=(
                f"The current text language is: {detected_language}, "
                f"but the current language is: {self.source_language}.\n\n"
                "Do you want to change the current language to the text language?"
            ),

            buttons=[
                "Yes",
                "No",
            ],

            default_button=1,
        )

        self.active_dialog.show()


    # ==================================================
    # LANGUAGE DETECTION
    # ==================================================

    def _detect_language(self, text):

        if not text.strip():
            return

        # --------------------------------------------------
        # Берём только начало текста
        # --------------------------------------------------

        sample = text[:1000]

        # --------------------------------------------------
        # Отменяем предыдущий запрос
        # --------------------------------------------------

        if self._language_task is not None:

            if not self._language_task.done():
                self._language_task.cancel()

        # --------------------------------------------------
        # Запускаем AI в фоне
        # --------------------------------------------------

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

            self._language_check_for_generate = False
            self.busy_indicator.hide()
            return

        except Exception as e:

            logger.error(
                "AI language detection error:",
                e
            )

            self._language_check_for_generate = False
            self.busy_indicator.hide()
            return

        if not language:
            self._language_check_for_generate = False
            self.busy_indicator.hide()
            return

        logger.info(
            "Detected language:",
            language
        )

        # ==================================================
        # Generate language check
        # ==================================================

        if self._language_check_for_generate:

            logger.debug(
                "Generate language check:",
                "source =", self.source_language,
                "detected =", language
            )

            # --------------------------------------------------
            # Язык не совпадает
            # --------------------------------------------------

            if language != self.source_language:

                self._language_check_for_generate = False

                self.busy_indicator.hide()

                self._show_language_mismatch_dialog(
                    language
                )

                return

            # --------------------------------------------------
            # Язык совпадает
            # --------------------------------------------------

            logger.debug(
                "Source language matches."
            )

            # _generate() при повторном входе
            # сбросит этот флаг и продолжит генерацию.

            self._generate()

            return

        # ==================================================
        # Обычное определение языка
        # ==================================================

        self.source_language = language

        self._load_locales(
            language
        )

    
    # ==================================================
    # INITIAL PARAMETERS
    # ==================================================

    def _load_current_item_parameters(self):

        item = self.session.current_item

        if not item:
            return

        logger.debug(
            "INITIAL ITEM:",
            "phrase_code =", item.get("phrase_code", ""),
            "phrase_locale =", item.get("phrase_locale", ""),
            "phrase_voice =", item.get("phrase_voice", "")
        )




        # --------------------------------------------------
        # Language / Locale
        # --------------------------------------------------

        locale = item.get(
            "phrase_locale",
            ""
        )


        if locale:

            self.source_language = (
                locale.split("-")[0].lower()
            )

            # Показываем текущий locale.
            self.source_locale_selection.options = [
                (locale, locale)
            ]

            self.source_locale_selection.selected = 0

            # Загружаем голоса именно этого locale.
            self._load_voices(locale)

        logger.debug(
            "INITIAL SOURCE:",
            "language =", self.source_language,
            "locale =", self.source_locale_selection.value,
            "voice =", self.voice_selection.value
        )


        # --------------------------------------------------
        # Repeat count
        # --------------------------------------------------

        repeat_count = item.get(
            "repeat_count",
            1
        )

        self.repeat_edit.set_text(
            str(repeat_count)
        )

        # --------------------------------------------------
        # Pause factor
        # --------------------------------------------------

        self.pause_factor_edit.set_text(
            "1.0"
        )

    # ==================================================
    # TTS
    # ==================================================

    def _load_locales(self, language):

        if not language:
            return

        # --------------------------------------------------
        # Отменяем предыдущую загрузку locale
        # --------------------------------------------------

        if self._locale_task is not None:

            if not self._locale_task.done():
                self._locale_task.cancel()

        # --------------------------------------------------
        # Очищаем voice.
        # --------------------------------------------------

        if self._voice_task is not None:

            if not self._voice_task.done():
                self._voice_task.cancel()

        self.voice_selection.options = [
            ("", "No voice")
        ]

        self.voice_selection.selected = 0

        # --------------------------------------------------
        # Показываем Loading...
        # --------------------------------------------------

        self.source_locale_selection.options = [
            ("", "Loading...")
        ]

        self.source_locale_selection.selected = 0

        # --------------------------------------------------
        # Загружаем locale
        # --------------------------------------------------
        
        self.busy_indicator.show(
            "Loading locales..."
        )

        self._locale_task = self._async_runner.submit(
            self._tts.get_locales_for_language(
                language
            )
        )

    # --------------------------------------------------
    
    def _load_target_languages(self):

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

            logger.error(
                "TTS target language error:",
                e
            )

            self.target_language_selection.options = [
                ("", "Error")
            ]

            self.target_language_selection.selected = 0

            return

        if not languages:

            self.target_language_selection.options = [
                ("", "No languages")
            ]

            self.target_language_selection.selected = 0

            return

        options = [
            (language, language)
            for language in languages
        ]

        self.target_language_selection.options = options

        # --------------------------------------------------
        # По умолчанию TARGET LANGUAGE = en
        # --------------------------------------------------

        selected_index = 0

        for index, (value, _) in enumerate(options):

            if value == "en":

                selected_index = index
                break

        self.target_language_selection.selected = selected_index

        # --------------------------------------------------
        # После выбора языка загружаем TARGET LOCALE
        # --------------------------------------------------

        selected_language = (
            self.target_language_selection.value
        )

        logger.debug(
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

            logger.error(
                "TTS target locale error:",
                e
            )

            self.target_locale_selection.options = [
                ("", "Error")
            ]

            self.target_locale_selection.selected = 0

            return

        if not locales:

            self.target_locale_selection.options = [
                ("", "No locales")
            ]

            self.target_locale_selection.selected = 0

            return

        options = [
            (locale, locale)
            for locale in locales
        ]

        self.target_locale_selection.options = options

        # --------------------------------------------------
        # По умолчанию TARGET LOCALE = en-US
        # --------------------------------------------------

        selected_index = 0

        for index, (value, _) in enumerate(options):

            if value == "en-US":

                selected_index = index
                break

        self.target_locale_selection.selected = selected_index

        selected_locale = (
            self.target_locale_selection.value
        )

        logger.debug(
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

            logger.error(
                "TTS target voice error:",
                e
            )

            self.target_voice_selection.options = [
                ("", "Error")
            ]

            self.target_voice_selection.selected = 0

            return

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
                caption += f" | {gender}"

            options.append(
                (
                    short_name,
                    caption
                )
            )

        self.target_voice_selection.options = options
        self.target_voice_selection.selected = 0


    def _load_voices(self, locale):

        if not locale:
            return

        # --------------------------------------------------
        # Отменяем предыдущий запрос
        # --------------------------------------------------

        if self._voice_task is not None:

            if not self._voice_task.done():
                self._voice_task.cancel()

        # --------------------------------------------------
        # Показываем Loading...
        # --------------------------------------------------

        self.voice_selection.options = [
            ("", "Loading...")
        ]

        self.voice_selection.selected = 0
        
        self.busy_indicator.show(
            "Loading voices..."
        )

        # --------------------------------------------------
        # Запускаем загрузку голосов
        # --------------------------------------------------

        self._voice_task = self._async_runner.submit(
            self._tts.get_voices_for_locale(
                locale
            )
        )

    # --------------------------------------------------
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

            logger.error(
                "TTS locale error:",
                e
            )

            self.source_locale_selection.options = [
                ("", "Error")
            ]

            self.source_locale_selection.selected = 0

            return

        # --------------------------------------------------
        # Нет locale
        # --------------------------------------------------

        if not locales:

            self.source_locale_selection.options = [
                ("", "No locales")
            ]

            self.source_locale_selection.selected = 0

            return

        # --------------------------------------------------
        # Создаём список SOURCE LOCALE
        # --------------------------------------------------

        options = [
            (locale, locale)
            for locale in locales
        ]

        self.source_locale_selection.options = options

        # --------------------------------------------------
        # По умолчанию выбираем первый locale
        # --------------------------------------------------

        selected_index = 0

        # --------------------------------------------------
        # Если текущий item имеет такой locale,
        # сохраняем его.
        # --------------------------------------------------

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

        self.source_locale_selection.selected = selected_index

        # --------------------------------------------------
        # Сразу загружаем голоса выбранного SOURCE LOCALE
        # --------------------------------------------------

        selected_locale = (
            self.source_locale_selection.value
        )

        logger.debug(
            "Source locale:",
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

            logger.error(
                "TTS voice error:",
                e
            )

            self.voice_selection.options = [
                ("", "Error")
            ]

            self.voice_selection.selected = 0

            self.busy_indicator.hide()

            return

        # --------------------------------------------------
        # Нет голосов
        # --------------------------------------------------

        if not voices:

            self.voice_selection.options = [
                ("", "No voices")
            ]

            self.voice_selection.selected = 0

            return

        # --------------------------------------------------
        # Формируем список голосов
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Пытаемся сохранить текущий голос
        # --------------------------------------------------

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
    # VISIBILITY
    # ==================================================

    def show(self):

        self.visible = True

        self._load_current_item_parameters()

        self._load_target_languages()

    # --------------------------------------------------

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

        if self.active_dialog:
            self.active_dialog.update()


        self.text_edit.update()
        self.repeat_edit.update()
        self.pause_factor_edit.update()

        self._process_language_task()
        self._process_locale_task()
        self._process_voice_task()
                
        self._process_target_language_task()
        self._process_target_locale_task()
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

            logger.error(
                "Generation error:",
                e
            )
            self.busy_indicator.hide()
            return

        # --------------------------------------------------
        # Привязываем новый plan к текущему пользователю
        # --------------------------------------------------

        current_set = self.session.get_data().get(
            "set",
            {}
        )

        plan["set"]["user_id"] = current_set.get(
            "user_id",
            0
        )

        plan["set"]["user_nickname"] = current_set.get(
            "user_nickname",
            "guest"
        )

        # --------------------------------------------------
        # Обновляем текущую Session
        # --------------------------------------------------

        self.session.load_data(plan)
        self.busy_indicator.hide()

        self.session.save(
            Config.PLAN_SESSION_FILE
        )

        logger.info()
        logger.info("==============")
        logger.info("PLAN GENERATED")
        logger.info("==============")
        logger.info(
            "Items:",
            len(plan["items"])
        )
        logger.info("--------------")

        for item in plan["items"]:

            logger.info(
                item["item_order"],
                item["phrase_text"],
                "| pause:",
                item["pause_ms"],
                "| repeat:",
                item["repeat_count"]
            )

        logger.info("==============================")
        logger.info()

    # ==================================================
    # EVENTS
    # ==================================================

    def handle_event(self, event):

        if not self.visible:
            return

        if self.active_dialog:

            result = self.active_dialog.handle_event(event)

            if result == 0:
                # Yes
                self.active_dialog = None

                self.source_language = (
                    self._detected_generate_language
                )

                self._detected_generate_language = ""

                self._load_locales(
                    self.source_language
                )

            elif result == 1:
                # No
                self.active_dialog = None
                self._detected_generate_language = ""

            return
        

        # --------------------------------------------------
        # Close button must remain available while busy
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
        # Block all other interaction while busy
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

                # Снимаем фокус со всех остальных
                for edit in text_edits:

                    if edit is not clicked_edit:

                        edit.focused = False
                        edit.repeat_key = None

                # Передаём событие выбранному TextEdit
                if clicked_edit is not None:

                    clicked_edit.handle_event(
                        event
                    )

                else:

                    # Клик вне TextEdit
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

            # KEYDOWN / TEXTINPUT / MOUSEWHEEL
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

            logger.debug(
                "Scenario:",
                result[1]
            )


        # --------------------------------------------------
        # Voice
        # --------------------------------------------------

        result = self.voice_selection.handle_event(
            event
        )

        if result is not None:

            logger.debug(
                "Voice:",
                result[1]
            )

        # --------------------------------------------------
        # Locale
        # --------------------------------------------------

        result = self.source_locale_selection.handle_event(
            event
        )

        if result is not None:

            locale = result[1]

            self.source_language = (
                locale.split("-")[0].lower()
            )

            logger.debug(
                "Locale:",
                locale,
                "Language:",
                self.source_language
            )

            self._load_voices( locale )

        # --------------------------------------------------
        # Target language
        # --------------------------------------------------

        if self.scenario_provider.get_current() == "shadowing":

            result = self.target_language_selection.handle_event(
                event
            )

            if result is not None:

                language = result[1]

                logger.debug(
                    "Target language:",
                    language
                )

                # --------------------------------------------------
                # При изменении TARGET LANGUAGE
                # заново загружаем TARGET LOCALE.
                # TARGET VOICE будет обновлён
                # автоматически после загрузки locale.
                # --------------------------------------------------

                self._load_target_locales(
                    language
                )


        # --------------------------------------------------
        # Target locale
        # --------------------------------------------------

        if self.scenario_provider.get_current() == "shadowing":

            result = self.target_locale_selection.handle_event(
                event
            )

            if result is not None:

                locale = result[1]

                logger.debug(
                    "Target locale:",
                    locale
                )

                # --------------------------------------------------
                # При изменении TARGET LOCALE
                # загружаем соответствующие TARGET VOICES.
                # --------------------------------------------------

                self._load_target_voices(
                    locale
                )

        # --------------------------------------------------
        # Target voice
        # --------------------------------------------------

        if self.scenario_provider.get_current() == "shadowing":

            result = self.target_voice_selection.handle_event(
                event
            )

            if result is not None:

                logger.debug(
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

                # --------------------------------------------------
                # AI определяет язык текста
                # --------------------------------------------------

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
        # Source text
        # --------------------------------------------------

        text = self.text_edit.get_text().strip()

        if not text:
            logger.debug(
                "Source text is empty"
            )
            return

        # --------------------------------------------------
        # Check source language before generation
        # --------------------------------------------------

        if not self._language_check_for_generate:

            logger.error(
                "Checking source language before generation..."
            )

            self._language_check_for_generate = True

            self._detect_language(
                text
            )

            return

        # Проверка уже выполнена успешно.
        self._language_check_for_generate = False

        # --------------------------------------------------
        # Current item
        # --------------------------------------------------

        item = self.session.current_item

        if not item:
            logger.error(
                "Current session item is missing"
            )
            return

        # --------------------------------------------------
        # Repeat count
        # --------------------------------------------------

        try:

            repeat_count = int(
                self.repeat_edit.get_text()
            )

            if repeat_count < 1:
                raise ValueError

        except ValueError:

            logger.error(
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

            logger.error(
                "Invalid pause factor"
            )
            return

        # --------------------------------------------------
        # Scenario
        # --------------------------------------------------

        scenario = (
            self.scenario_provider.get_current()
        )

        # --------------------------------------------------
        # Prevent duplicate generation
        # --------------------------------------------------

        if self._generate_task is not None:

            logger.debug(
                "Generation already in progress"
            )

            return

        # --------------------------------------------------
        # Source parameters
        # --------------------------------------------------

        phrase_locale = (
            self.source_locale_selection.value
        )

        phrase_voice = (
            self.voice_selection.value
        )

        phrase_code = (
            self.source_language
            if self.source_language
            else (
                phrase_locale.split("-")[0].lower()
                if phrase_locale
                else ""
            )
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

            logger.error(
                "Incomplete source voice parameters"
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

            logger.error(e)
            return

        logger.info(
            "Generator:",
            type(generator).__name__
        )



        # ==================================================
        # DICTATION
        # ==================================================

        if scenario == "dictation":

            self.busy_indicator.show(
                "Generating plan..."
            )

            self._generate_task = (
                self._async_runner.submit(
                    generator.generate(
                        text=text,
                        scenario=scenario,

                        phrase_code=phrase_code,
                        phrase_locale=phrase_locale,
                        phrase_voice=phrase_voice,
                        phrase_voice_gender=phrase_voice_gender,

                        repeat_count=repeat_count,
                        pause_factor=pause_factor,
                    )
                )
            )

        # ==================================================
        # SHADOWING
        # ==================================================

        elif scenario == "shadowing":

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

                logger.error(
                    "Incomplete target voice parameters"
                )

                return

            # --------------------------------------------------
            # Target parameters
            # --------------------------------------------------

            translate_code = target_language
            translate_locale = target_locale
            translate_voice = target_voice

            translate_voice_gender = ""

            # --------------------------------------------------
            # Generate
            # --------------------------------------------------

            self.busy_indicator.show(
                "Generating plan..."
            )

            self._generate_task = (
                self._async_runner.submit(
                    generator.generate(
                        text=text,

                        source_language=self.source_language,
                        target_language=target_language,

                        phrase_code=phrase_code,
                        phrase_locale=phrase_locale,
                        phrase_voice=phrase_voice,
                        phrase_voice_gender=phrase_voice_gender,

                        translate_code=translate_code,
                        translate_locale=translate_locale,
                        translate_voice=translate_voice,
                        translate_voice_gender=translate_voice_gender,

                        repeat_count=repeat_count,
                        pause_factor=pause_factor,
                    )
                )
            )

        else:

            logger.info(
                f"Unsupported generation scenario: {scenario}"
            )
            self.busy_indicator.hide()
            return

        logger.info(
            "Generating plan..."
        )    

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
        # Close button
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
                self.file_button_rect.x ,
                self.file_button_rect.y - 25

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
                300
            )

            file_text = caption_font.render(
                "of file:  "+filename,
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            screen.blit(
                file_text,
                (
                    self.text_edit.rect.x + 35,
                    self.text_edit.rect.y - 25
                    #self.file_button_rect.right - 400,
                    #self.file_button_rect.y + 45
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

        # -----------------
        # Source Locale
        # -----------------

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
        # Voice
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
        # Generate button
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

        if self.scenario_provider.get_current() == "shadowing":

            caption = caption_font.render(
                "Target lang.",
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
        # Dropdowns Рисуем последними, чтобы они были поверх остальных элементов.
        # --------------------------------------------------

        self.scenario_selection.draw(
            screen,
            list_font
        )

        if self.scenario_provider.get_current() == "shadowing":

            self.target_voice_selection.draw(
                screen,
                list_font
            )

            self.target_language_selection.draw(
                screen,
                list_font
            )

            self.target_locale_selection.draw(
                screen,
                list_font
            )


        self.voice_selection.draw(
            screen,
            list_font
        )


        self.source_locale_selection.draw(
            screen,
            list_font
        )

        # --------------------------------------------------
        # Busy indicator  Рисуем последним, чтобы overlay был поверх всего окна.
        # --------------------------------------------------

        self.busy_indicator.draw(
            screen
        )

        if self.active_dialog:
            self.active_dialog.draw(screen)