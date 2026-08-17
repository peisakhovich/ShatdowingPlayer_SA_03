import pygame
from pathlib import Path

from gui.theme import Theme
from gui.widgets.list_selection import ListSelection
from gui.file_dialog import FileDialog


class SettingsWindow:
    """Модальное окно настроек."""

    def __init__(self, rect, scenario):

        self.scenario_provider = scenario

        self.rect = pygame.Rect(rect)
        self.visible = False

        self.close_rect = pygame.Rect(
            self.rect.right - 30,
            self.rect.top + 10,
            20,
            20,
        )

        self.list_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 80,
                400,
                30
            ),
            self.scenario_provider.get_scenario_list(),
            self.scenario_provider.get_current_scenario_index()
        )

        self.source_file = ""

        self.file_button_rect = pygame.Rect(
            self.rect.x + 30,
            self.rect.y + 180,
            120,
            32
        )

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def _fit_text(self, text, font, max_width):

        if font.size(text)[0] <= max_width:
            return text

        while len(text) > 3:

            text = text[1:]
            candidate = "..." + text

            if font.size(candidate)[0] <= max_width:
                return candidate

        return "..."

    def handle_event(self, event):

        if not self.visible:
            return

        # --------------------------------------------------
        # Playback scenario
        # --------------------------------------------------

        result = self.list_selection.handle_event(event)

        if result is not None:
            self.scenario_provider.set_current(result[1])
            print("ListSelection:", result[1])

        # --------------------------------------------------
        # Mouse buttons
        # --------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Close button
            if self.close_rect.collidepoint(event.pos):

                self.hide()

            # Choose source file
            elif self.file_button_rect.collidepoint(event.pos):

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
                        text = Path(filename).read_text(
                            encoding="utf-8"
                        )

                    except UnicodeDecodeError:

                        text = Path(filename).read_text(
                            encoding="utf-16"
                        )
                    self.source_text = text


    def draw(self, screen):

        if not self.visible:
            return

        # --------------------------------------------------
        # Fonts
        # --------------------------------------------------

        title_font = pygame.font.Font(None, 28)
        caption_font = pygame.font.Font(None, 22)
        list_font = pygame.font.Font(None, 24)
        button_font = pygame.font.Font(None, 22)

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
            (self.rect.x + 15, self.rect.y + 12)
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
        # Playback scenario caption
        # --------------------------------------------------

        caption = caption_font.render(
            "Playback scenario",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.list_selection.rect.x,
                self.list_selection.rect.y - 25
            )
        )

        # --------------------------------------------------
        # Source text caption
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
        # Choose file button
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
        # Selected file name
        # --------------------------------------------------

        if self.source_file:

            filename = Path(self.source_file).name

            filename = self._fit_text(
                filename,
                caption_font,
                self.rect.right - self.file_button_rect.right - 30
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
        # ListSelection
        #
        # Draw LAST so the dropdown is above other controls.
        # --------------------------------------------------

        self.list_selection.draw(
            screen,
            list_font
        )