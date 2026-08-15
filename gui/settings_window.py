import pygame

from gui.theme import Theme
from gui.widgets.list_selection import ListSelection
from audio.scenario_provider import ScenarioProvider


class SettingsWindow:
    """Модальное окно настроек."""

    def __init__(self, rect):

        self.scenario_provider = ScenarioProvider("audio/scenarios.json")
        
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
        

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def handle_event(self, event):

        if not self.visible:
            return

        result = self.list_selection.handle_event(event)
        if result is not None:
            print("ListSelection:", result)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_rect.collidepoint(event.pos):
                self.hide()

    def draw(self, screen):

        if not self.visible:
            return

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

        font = pygame.font.Font(None, 28)

        title = font.render(
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

        caption_font = pygame.font.Font(None, 22)

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
        # ListSelection
        # --------------------------------------------------

        font = pygame.font.Font(None, 24)

        self.list_selection.draw(
            screen,
            font
        )