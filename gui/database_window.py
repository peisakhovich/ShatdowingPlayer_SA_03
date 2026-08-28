from __future__ import annotations

import asyncio

import pygame

from api.client import ApiClient
from core.config import Config
from core.logger import logger
from gui.theme import Theme
from gui.widgets.busy_indicator import BusyIndicator
from gui.widgets.list_selection import ListSelection
from audio.async_runner import AsyncRunner
from gui.panels.control_panel_db import ControlPanel


class DatabaseWindow:
    """Окно работы с базой данных."""

    def __init__(self, rect, font_manager,image_loader):

        # --------------------------------------------------
        # Основные данные
        # --------------------------------------------------

        self.rect = pygame.Rect(rect)
        self.font_manager = font_manager

        self.visible = False


        self.control_panel = ControlPanel(
            font_manager,
            image_loader
        )

        # --------------------------------------------------
        # Async
        # --------------------------------------------------

        self._async_runner = AsyncRunner()
        self._sets_task = None

        # --------------------------------------------------
        # Data
        # --------------------------------------------------

        self.sets = []
        self.selected_set = None

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
        # Busy indicator
        # --------------------------------------------------

        self.busy_indicator = BusyIndicator(
            self.rect,
            pygame.font.Font(None, 22)
        )

        # --------------------------------------------------
        # API client
        # --------------------------------------------------

        self.api_client = ApiClient(
            Config.API_BASE_URL
        )

        # --------------------------------------------------
        # Sets selection
        # --------------------------------------------------

        self.set_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 70,
                self.rect.width - 60,
                30
            ),
            [("", "Loading...")],
            0
        )

    # ==================================================
    # VISIBILITY
    # ==================================================

    def show(self):

        self.visible = True

        self._load_sets()

    # --------------------------------------------------

    def hide(self):

        self._cancel_tasks()

        self.visible = False

    # ==================================================
    # API
    # ==================================================

    def _load_sets(self):

        if self._sets_task is not None:

            if not self._sets_task.done():
                return

        self.busy_indicator.show(
            "Loading sets..."
        )

        self.set_selection.options = [
            ("", "Loading...")
        ]

        self.set_selection.selected = 0

        self.selected_set = None

        self._sets_task = self._async_runner.submit(
            self._get_sets_async()
        )

    # --------------------------------------------------

    async def _get_sets_async(self):

        return await asyncio.to_thread(
            self.api_client.get_sets
        )

    # ==================================================
    # PROCESS API RESULT
    # ==================================================

    def _process_sets_task(self):

        if self._sets_task is None:
            return

        if not self._sets_task.done():
            return

        task = self._sets_task
        self._sets_task = None

        try:

            self.sets = task.result()

            logger.info(
                "Database sets loaded:",
                len(self.sets)
            )

        except asyncio.CancelledError:

            return

        except Exception as e:

            logger.error(
                "Database API error:",
                e
            )

            self.sets = []

            self.set_selection.options = [
                ("", "Error loading sets")
            ]

            self.set_selection.selected = 0

            self.selected_set = None

            return

        finally:

            self.busy_indicator.hide()

        # --------------------------------------------------
        # Нет sets
        # --------------------------------------------------

        if not self.sets:

            self.set_selection.options = [
                ("", "No sets")
            ]

            self.set_selection.selected = 0

            self.selected_set = None

            return

        # --------------------------------------------------
        # Формируем ListSelection
        # --------------------------------------------------

        options = []

        for item in self.sets:

            set_id = item.get(
                "set_id",
                ""
            )

            set_index = item.get(
                "set_index",
                ""
            )

            set_name = item.get(
                "set_name",
                ""
            )

            set_description = item.get(
                "set_description",
                ""
            )

            items_count = item.get(
                "items_count",
                0
            )

            caption = (
                f"{set_index}  |  "
                f"{set_name}  |  "
                f"{set_description}  |  "
                f"{items_count} items"
            )

            options.append(
                (
                    set_id,
                    caption
                )
            )

        self.set_selection.options = options
        self.set_selection.selected = 0

        # --------------------------------------------------
        # Выбираем первый set
        # --------------------------------------------------

        self._update_selected_set(
            options[0][0]
        )

    # ==================================================
    # SELECTED SET
    # ==================================================

    def _update_selected_set(self, set_id):

        self.selected_set = None

        for item in self.sets:

            if item.get("set_id") == set_id:

                self.selected_set = item
                break

        if self.selected_set:

            logger.debug(
                "Selected set:",
                self.selected_set.get(
                    "set_name",
                    ""
                )
            )

    # ==================================================
    # TASKS
    # ==================================================

    def _cancel_tasks(self):

        if self._sets_task is not None:

            if not self._sets_task.done():
                self._sets_task.cancel()

        self._sets_task = None

        self.busy_indicator.hide()

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.visible:
            return

        self._process_sets_task()

        self.control_panel.update()

        self.busy_indicator.update()

    # ==================================================
    # EVENTS
    # ==================================================

    def handle_event(self, event):

        if not self.visible:
            return


        # Передаем событие панели управления
        #

        command = self.control_panel.handle_event(event)

        if command is not None:

            match command:

                case ("button", name):

                    logger.debug(f"Button: {name}")

                    # if name == "settodb":
                        # "settodb","dbtoset","settoexcel","exceltoset","dropset","login"

                    # elif name == "pause":
                        



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
        # Block interaction while loading
        # --------------------------------------------------

        if self.busy_indicator.visible:
            return

        # --------------------------------------------------
        # Set selection
        # --------------------------------------------------

        result = self.set_selection.handle_event(
            event
        )

        if result is not None:

            set_id = result[1]

            self._update_selected_set(
                set_id
            )

            return

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
            20
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
            "Database",
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

        x = self.close_rect

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BACKGROUND_COLOR,
            self.close_rect
        )

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
        # Caption
        # --------------------------------------------------

        caption = caption_font.render(
            "Training sets",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.set_selection.rect.x,
                self.set_selection.rect.y - 25
            )
        )

        # --------------------------------------------------
        # Set information
        # --------------------------------------------------

        if self.selected_set:

            set_index = self.selected_set.get(
                "set_index",
                ""
            )

            set_name = self.selected_set.get(
                "set_name",
                ""
            )

            set_description = self.selected_set.get(
                "set_description",
                ""
            )

            items_count = self.selected_set.get(
                "items_count",
                0
            )

            info_y = self.set_selection.rect.bottom + 35

            # --------------------------------------------------
            # Selected set
            # --------------------------------------------------

            text = caption_font.render(
                f"Set: {set_index}  |  {set_name}",
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            screen.blit(
                text,
                (
                    self.rect.x + 30,
                    info_y
                )
            )

            # --------------------------------------------------
            # Items count
            # --------------------------------------------------

            text = caption_font.render(
                f"Items: {items_count}",
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            screen.blit(
                text,
                (
                    self.rect.x + 30,
                    info_y + 35
                )
            )

            # --------------------------------------------------
            # Description
            # --------------------------------------------------

            text = caption_font.render(
                "Description:",
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            screen.blit(
                text,
                (
                    self.rect.x + 30,
                    info_y + 75
                )
            )

            # --------------------------------------------------
            # Description text
            # --------------------------------------------------

            text = caption_font.render(
                set_description,
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            screen.blit(
                text,
                (
                    self.rect.x + 30,
                    info_y + 110
                )
            )


        self.control_panel.draw(
            screen
        )

        # --------------------------------------------------
        # ListSelection
        # --------------------------------------------------
        # Рисуем последним, чтобы раскрытый список
        # был поверх остальных элементов.

        self.set_selection.draw(
            screen,
            list_font
        )

        # --------------------------------------------------
        # Busy indicator
        # --------------------------------------------------

        self.busy_indicator.draw(
            screen
        )