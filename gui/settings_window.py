import pygame

from gui.theme import Theme


class SettingsWindow:
    """Модальное окно настроек."""

    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.visible = False

        self.close_rect = pygame.Rect(
            self.rect.right - 30,
            self.rect.top + 10,
            20,
            20,
        )

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def handle_event(self, event):
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_rect.collidepoint(event.pos):
                self.hide()

    def draw(self, screen):
        if not self.visible:
            return

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

        # Draw the close button (X)
        pygame.draw.rect(screen, Theme.DIALOG_BACKGROUND_COLOR, self.close_rect)
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



        font = pygame.font.Font(None, 28)
        title = font.render("Settings", True, Theme.DIALOG_TITLE_COLOR)

        screen.blit(
            title,
            (self.rect.x + 15, self.rect.y + 12)
        )