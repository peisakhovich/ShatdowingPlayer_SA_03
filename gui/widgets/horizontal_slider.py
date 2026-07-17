import pygame

from gui.theme import Theme


class HorizontalSlider:

    def __init__(
        self,
        rect,
        caption,
        start_value,
        value_range,
        font,
        formatter=None
    ):

        # -------------------------
        # Общая область виджета
        # -------------------------

        self.rect = pygame.Rect(rect)

        # -------------------------
        # Параметры
        # -------------------------

        self.caption = caption

        self.min_value = value_range[0]
        self.max_value = value_range[1]

        self.value = start_value

        self.font = font

        if formatter is None:
            self.formatter = str
        else:
            self.formatter = formatter

        # -------------------------
        # Состояние
        # -------------------------

        self.dragging = False

        # -------------------------
        # Дорожка
        # -------------------------

        self.track_rect = pygame.Rect(0, 0, 0, 0)

        # -------------------------
        # Бегунок
        # -------------------------

        self.knob_rect = pygame.Rect(
            0,
            0,
            Theme.HSL_KNOB_WIDTH,
            Theme.HSL_KNOB_HEIGHT
        )

        self._update_geometry()

    # --------------------------------------------------

    def _update_geometry(self):
        #
        # Дорожка
        #
        self.track_rect = pygame.Rect(

            self.rect.x,

            self.rect.centery -
            Theme.HSL_TRACK_HEIGHT // 2,

            self.rect.width,

            Theme.HSL_TRACK_HEIGHT
        )

        #
        # Положение бегунка
        #

        k = (
            (self.value - self.min_value) /
            (self.max_value - self.min_value)
        )

        knob_x = (
            self.track_rect.left +
            k * self.track_rect.width
        )

        self.knob_rect.center = (
            int(knob_x),
            self.track_rect.centery
        )

    # --------------------------------------------------

    def handle_event(self, event):
        pass

    # --------------------------------------------------

    def update(self):
        pass

    # --------------------------------------------------

    def draw(self, screen):

        #
        # Дорожка
        #

        pygame.draw.rect(

            screen,

            Theme.HSL_TRACK_COLOR,

            self.track_rect,

            border_radius=Theme.HSL_TRACK_RADIUS
        )

        #
        # Заполненная часть
        #

        progress_rect = pygame.Rect(

            self.track_rect.left,

            self.track_rect.top,

            self.knob_rect.centerx -
            self.track_rect.left,

            self.track_rect.height
        )

        pygame.draw.rect(

            screen,

            Theme.HSL_PROGRESS_COLOR,

            progress_rect,

            border_radius=Theme.HSL_TRACK_RADIUS
        )

        #
        # Бегунок
        #

        pygame.draw.rect(

            screen,

            Theme.HSL_KNOB_COLOR,

            self.knob_rect,

            border_radius=Theme.HSL_KNOB_RADIUS
        )

        pygame.draw.rect(

            screen,

            Theme.HSL_KNOB_BORDER_COLOR,

            self.knob_rect,

            width=Theme.HSL_KNOB_BORDER_WIDTH,

            border_radius=Theme.HSL_KNOB_RADIUS
        )

        #
        # Подпись
        #

        caption = self.font.render(

            self.caption,

            True,

            Theme.HSL_TEXT_COLOR
        )

        screen.blit(
            caption,
            (self.rect.left, self.rect.top - 22)
        )

        #
        # Значение
        #

        value = self.font.render(

            self.formatter(self.value),

            True,

            Theme.HSL_TEXT_COLOR
        )

        screen.blit(

            value,

            (
                self.rect.right + 10,
                self.rect.top - 2
            )
        )