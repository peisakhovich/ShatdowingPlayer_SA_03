"""
Sound Language Studio

---------------------

Module:

    gui.widgets.status_message

Purpose:

    Provides a reusable status message widget with
    INFO, SUCCESS, WARNING and ERROR message types.

ru:

    Предоставляет универсальный виджет статусного сообщения
    с типами INFO, SUCCESS, WARNING и ERROR.
"""

import pygame

from gui.theme import Theme


class StatusMessage:

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

    def __init__(
        self,
        message,
        message_type,
        position,
        font,
        color=None
    ):

        self.message = message
        self.message_type = message_type
        self.position = position
        self.font = font

        self.color = (
            color
            if color is not None
            else self._get_default_color()
        )

    # ==================================================
    # COLOR
    # ==================================================

    def _get_default_color(self):

        if self.message_type == self.INFO:
            return Theme.DIALOG_INFO_COLOR

        if self.message_type == self.SUCCESS:
            return Theme.DIALOG_SUCCESS_COLOR

        if self.message_type == self.WARNING:
            return Theme.DIALOG_WARNING_COLOR

        if self.message_type == self.ERROR:
            return Theme.DIALOG_ERROR_COLOR

        return Theme.DIALOG_TEXT_COLOR

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        x, y = self.position

        self._draw_icon(
            screen,
            x,
            y
        )

        text_surface = self.font.render(
            self.message,
            True,
            self.color
        )

        screen.blit(
            text_surface,
            (x + 20, y - text_surface.get_height() // 2)
        )

    # ==================================================
    # ICON
    # ==================================================

    def _draw_icon(self, screen, x, y):

        if self.message_type == self.INFO:

            pygame.draw.circle(
                screen,
                self.color,
                (x, y),
                8
            )

            pygame.draw.line(
                screen,
                Theme.DIALOG_BACKGROUND_COLOR,
                (x-1, y - 3),
                (x-1, y + 4),
                2
            )

            pygame.draw.circle(
                screen,
                Theme.DIALOG_BACKGROUND_COLOR,
                (x, y - 5),
                1
            )

        elif self.message_type == self.SUCCESS:

            pygame.draw.circle(
                screen,
                self.color,
                (x, y),
                8
            )

            pygame.draw.line(
                screen,
                Theme.DIALOG_BACKGROUND_COLOR,
                (x - 3, y),
                (x , y + 3),
                2
            )

            pygame.draw.line(
                screen,
                Theme.DIALOG_BACKGROUND_COLOR,
                (x , y + 3),
                (x + 4, y - 4),
                2
            )

        elif self.message_type == self.WARNING:

            triangle = [
                (x, y - 9),
                (x + 9, y + 8),
                (x - 9, y + 8),
            ]

            pygame.draw.polygon(
                screen,
                self.color,
                triangle
            )

            pygame.draw.line(
                screen,
                Theme.DIALOG_BACKGROUND_COLOR,
                (x, y - 5),
                (x, y + 3),
                2
            )

            pygame.draw.circle(
                screen,
                Theme.DIALOG_BACKGROUND_COLOR,
                (x+1, y + 6),
                1
            )

        elif self.message_type == self.ERROR:

            pygame.draw.circle(
                screen,
                self.color,
                (x, y),
                8
            )

            pygame.draw.line(
                screen,
                Theme.DIALOG_BACKGROUND_COLOR,
                (x - 4, y - 4),
                (x + 4, y + 4),
                2
            )

            pygame.draw.line(
                screen,
                Theme.DIALOG_BACKGROUND_COLOR,
                (x + 4, y - 4),
                (x - 4, y + 4),
                2
            )