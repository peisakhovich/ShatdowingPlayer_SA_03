import pygame
from gui.theme import Theme

class Hint:

    def __init__(self, font_manager, delay=500):

        self.font = font_manager.load(12)

        self.delay = delay

        self.text = None
        self.button_rect = None

        self._start_time = None
        self._visible = False

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(self, text, button_rect):

        now = pygame.time.get_ticks()

        # Нет подсказки
        if not text or button_rect is None:
            self.hide()
            return

        button_rect = pygame.Rect(button_rect)

        # Курсор перешёл на другую кнопку
        if (
            self.text != text
            or self.button_rect != button_rect
        ):
            self.text = text
            self.button_rect = button_rect

            self._start_time = now
            self._visible = False

            return

        # Задержка перед появлением
        if (
            not self._visible
            and now - self._start_time >= self.delay
        ):
            self._visible = True

    # --------------------------------------------------
    # HIDE
    # --------------------------------------------------

    def hide(self):

        self.text = None
        self.button_rect = None

        self._start_time = None
        self._visible = False

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self, surface):

        if not self._visible:
            return

        text_surface = self.font.render(
            self.text,
            True,
            Theme.HINT_TEXT_COLOR
        )

        padding_x = 8
        padding_y = 5

        rect = text_surface.get_rect()

        rect.width += padding_x * 2
        rect.height += padding_y * 2

        rect.midtop = (
            self.button_rect.centerx,
            self.button_rect.bottom + 8
        )

        pygame.draw.rect(
            surface,
            Theme.HINT_BACKGROUND_COLOR,
            rect,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            Theme.HINT_BORDER_COLOR,
            rect,
            width=1,
            border_radius=4
        )

        text_rect = text_surface.get_rect(
            center=rect.center
        )

        surface.blit(
            text_surface,
            text_rect
        )