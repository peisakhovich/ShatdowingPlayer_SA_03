import asyncio
from pathlib import Path

import pygame

from gui.theme import Theme
from gui.widgets.list_selection import ListSelection
from gui.file_dialog import FileDialog
from gui.widgets.text_edit import TextEdit

from audio.tts import TTS
from audio.async_runner import AsyncRunner
from ai.dictation_segmenter import DictationSegmenter
from ai.dictation_plan import DictationPlanBuilder


class SettingsWindow:
    """Модальное окно настроек."""

    def __init__(self, rect, scenario, session):

        # --------------------------------------------------
        # Основные данные
        # --------------------------------------------------

        # цепляем наш AI генератор 
        self._locale_task = None
        self._voice_task = None
        self._generate_task = None
        

        self.rect = pygame.Rect(rect)
        self.visible = False

        self.scenario_provider = scenario
        self.session = session

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

        self._locale_task = None
        self._voice_task = None

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
            self.rect.x + 30,
            self.rect.y + 180,
            120,
            32
        )

        # --------------------------------------------------
        # Source text
        # --------------------------------------------------

        self.text_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 240,
                self.rect.width - 60,
                130
            ),
            pygame.font.Font(None, 24)
        )

        # --------------------------------------------------
        # Language
        # --------------------------------------------------

        self.language_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 405,
                120,
                30
            ),
            [("", "Loading...")],
            0
        )

        # --------------------------------------------------
        # Voice
        # --------------------------------------------------

        self.voice_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 170,
                self.rect.y + 405,
                self.rect.width - 200,
                30
            ),
            [("", "Loading...")],
            0
        )

        # --------------------------------------------------
        # Repeat count
        # --------------------------------------------------

        self.repeat_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 475,
                100,
                30
            ),
            pygame.font.Font(None, 24)
        )

        # --------------------------------------------------
        # Pause factor
        # --------------------------------------------------

        self.pause_factor_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 240,
                self.rect.y + 475,
                100,
                30
            ),
            pygame.font.Font(None, 24)
        )

        # --------------------------------------------------
        # Generate button
        # --------------------------------------------------

        self.generate_button_rect = pygame.Rect(
            self.rect.x + 30,
            self.rect.y + 530,
            120,
            32
        )

        # --------------------------------------------------
        # Initial parameters
        # --------------------------------------------------

        self._load_current_item_parameters()

    # ==================================================
    # INITIAL PARAMETERS
    # ==================================================

    def _load_current_item_parameters(self):

        item = self.session.current_item

        if not item:
            return

        # --------------------------------------------------
        # Language
        # --------------------------------------------------

        locale = item.get("phrase_locale", "")

        if locale:

            language = locale.split("-")[0].lower()

            self.language_selection.options = [
                (language, language)
            ]

            self.language_selection.selected = 0

            self._load_locales(language)

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

        self.pause_factor_edit.set_text("1.0")

    # ==================================================
    # TTS
    # ==================================================

    def _load_locales(self, language):

        if not language:
            return

        if self._locale_task is not None:
            if not self._locale_task.done():
                self._locale_task.cancel()

        self._locale_task = self._async_runner.submit(
            self._tts.get_locales_for_language(
                language
            )
        )

    # --------------------------------------------------

    def _load_voices(self, locale):

        if not locale:
            return

        if self._voice_task is not None:
            if not self._voice_task.done():
                self._voice_task.cancel()

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
            print("TTS locale error:", e)
            return

        if not locales:
            self.voice_selection.options = [
                ("", "No voices")
            ]
            self.voice_selection.selected = 0
            return

        options = [
            (locale, locale)
            for locale in locales
        ]

        self.language_selection.options = options

        # --------------------------------------------------
        # Стараемся сохранить текущий locale
        # --------------------------------------------------

        current_locale = (
            self.language_selection.value
            if self.language_selection.options
            else ""
        )

        index = 0

        for i, (value, _) in enumerate(options):

            if value == current_locale:
                index = i
                break

        self.language_selection.selected = index

        self._load_voices(
            options[index][0]
        )

    # --------------------------------------------------

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
            print("TTS voice error:", e)
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
                caption += f" | {gender}"

            options.append(
                (
                    short_name,
                    caption
                )
            )

        self.voice_selection.options = options

        # --------------------------------------------------
        # Пытаемся сохранить голос текущего item
        # --------------------------------------------------

        current_voice = ""

        item = self.session.current_item

        if item:
            current_voice = item.get(
                "phrase_voice",
                ""
            )

        index = 0

        for i, (value, _) in enumerate(options):

            if value == current_voice:
                index = i
                break

        self.voice_selection.selected = index

    # ==================================================
    # VISIBILITY
    # ==================================================

    def show(self):

        self.visible = True

        self._load_current_item_parameters()

    # --------------------------------------------------

    def hide(self):

        self.visible = False

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

        self._process_locale_task()
        self._process_voice_task()
        self._process_generate_task()

    # process_generate_task
    def _process_generate_task(self):

        if self._generate_task is None:
            return

        if not self._generate_task.done():
            return

        task = self._generate_task
        self._generate_task = None

        try:

            plan = task.result()

        except Exception as e:

            print("Dictation generation error:", e)
            return

        print()
        print("==============================")
        print("DICTATION PLAN GENERATED")
        print("==============================")
        print("Items:", len(plan["items"]))
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

                    if edit.rect.collidepoint(event.pos):

                        clicked_edit = edit
                        break

                # Снимаем фокус со всех
                for edit in text_edits:

                    if edit is not clicked_edit:

                        edit.focused = False
                        edit.repeat_key = None

                # Передаём событие только выбранному
                if clicked_edit is not None:

                    clicked_edit.handle_event(event)

                else:

                    # Клик вне всех TextEdit
                    for edit in text_edits:
                        edit.handle_event(event)

            else:

                for edit in text_edits:
                    edit.handle_event(event)

        else:

            # KEYDOWN / TEXTINPUT / MOUSEWHEEL
            # Передаём событие всем, но только один
            # TextEdit имеет focus.
            for edit in text_edits:
                edit.handle_event(event)

        # --------------------------------------------------
        # Scenario
        # --------------------------------------------------

        result = self.scenario_selection.handle_event(event)

        if result is not None:

            self.scenario_provider.set_current(
                result[1]
            )

            print(
                "Scenario:",
                result[1]
            )

        # --------------------------------------------------
        # Language
        # --------------------------------------------------

        result = self.language_selection.handle_event(
            event
        )

        if result is not None:

            language = result[1]

            print(
                "Language:",
                language
            )

            self._load_locales(language)

        # --------------------------------------------------
        # Voice
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
        # Mouse
        # --------------------------------------------------

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button != 1:
            return

        # --------------------------------------------------
        # Close
        # --------------------------------------------------

        if self.close_rect.collidepoint(event.pos):

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

            print("Source text is empty")
            return

        # --------------------------------------------------
        # Current item
        # --------------------------------------------------

        item = self.session.current_item

        if not item:

            print("Current session item is missing")
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

            print("Invalid repeat count")
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

            print("Invalid pause factor")
            return

        # --------------------------------------------------
        # Current item parameters
        # --------------------------------------------------

        phrase_code = item.get(
            "phrase_code",
            ""
        )

        phrase_locale = item.get(
            "phrase_locale",
            ""
        )

        phrase_voice = item.get(
            "phrase_voice",
            ""
        )

        phrase_voice_gender = item.get(
            "phrase_voice_gender",
            ""
        )

        if not phrase_code or not phrase_locale or not phrase_voice:

            print("Incomplete voice parameters")
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

            print("Generation already in progress")
            return

        # --------------------------------------------------
        # Generate
        # --------------------------------------------------

        self._generate_task = self._async_runner.submit(
            self._generate_plan(
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

        print("Generating dictation plan...")


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
    ):

        # --------------------------------------------------
        # AI segmentation
        # --------------------------------------------------

        segmenter = DictationSegmenter()

        result = segmenter.segment(
            text
        )

        # --------------------------------------------------
        # Convert Pydantic model
        # to DictationPlanBuilder format
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Build plan
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Store scenario information
        # --------------------------------------------------

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
                self.rect.x + 30,
                self.rect.y + 145
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

        self.text_edit.draw(screen)

        # --------------------------------------------------
        # Language
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

        self.repeat_edit.draw(screen)

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

        self.pause_factor_edit.draw(screen)

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
        # --------------------------------------------------
        # ListSelection dropdowns
        #
        # Draw LAST so dropdowns are above other controls.
        # --------------------------------------------------

        self.language_selection.draw(
            screen,
            list_font
        )

        self.voice_selection.draw(
            screen,
            list_font
        )

        self.scenario_selection.draw(
            screen,
            list_font
        )
