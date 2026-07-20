import pygame

from core.config import Config
from gui.theme import Theme


class Dialog:

    def __init__(
        self,
        parent_rect,
        font_manager,
        title,
        message,
        buttons
    ):

        # --------------------------------------------------
        # Геометрия
        # --------------------------------------------------

        self.parent_rect = pygame.Rect(parent_rect)

        self.rect = pygame.Rect(
            0,
            0,
            Theme.DIALOG_WIDTH,
            Theme.DIALOG_HEIGHT
        )

        self.rect.center = self.parent_rect.center

        # --------------------------------------------------
        # Текст
        # --------------------------------------------------

        self.title = title
        self.message = message

        # --------------------------------------------------
        # Кнопки
        # --------------------------------------------------

        self.button_captions = buttons
        self.button_rects = []

        # --------------------------------------------------
        # Шрифты
        # --------------------------------------------------

        self.title_font = font_manager.load(
            18,
            Config.FONT_BOLD
        )

        self.text_font = font_manager.load(
            14,
            Config.FONT_REGULAR
        )

        # --------------------------------------------------
        # Состояние
        # --------------------------------------------------

        self.visible = False
        self.result = None

        # --------------------------------------------------

        self._create_buttons()

    # ==================================================
    # Public
    # ==================================================

    def show(self):

        self.visible = True
        self.result = None

    # --------------------------------------------------

    def hide(self):

        self.visible = False

    # --------------------------------------------------

    def handle_event(self, event):

        if not self.visible:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                for index, rect in enumerate(self.button_rects):

                    if rect.collidepoint(event.pos):

                        self.result = index

                        return index

        return None

    # --------------------------------------------------

    def update(self):

        pass

    # --------------------------------------------------

    def draw(self, screen):

        if not self.visible:
            return

        self._draw_overlay(screen)
        self._draw_window(screen)
        self._draw_title(screen)
        self._draw_message(screen)
        self._draw_buttons(screen)

    # ==================================================
    # Private
    # ==================================================

    def _create_buttons(self):

        self.button_rects.clear()

        button_width = 90
        button_height = 30
        spacing = 12

        count = len(self.button_captions)

        total_width = (

            count * button_width +

            (count - 1) * spacing
        )

        start_x = (

            self.rect.centerx -

            total_width // 2
        )

        y = (

            self.rect.bottom -

            Theme.DIALOG_PADDING -

            button_height
        )

        for i in range(count):

            rect = pygame.Rect(

                start_x +

                i * (button_width + spacing),

                y,

                button_width,

                button_height
            )

            self.button_rects.append(rect)

    # --------------------------------------------------

    def _draw_overlay(self, screen):

        overlay = pygame.Surface(
            self.parent_rect.size,
            pygame.SRCALPHA
        )

        overlay.fill((
            Theme.DIALOG_OVERLAY_COLOR.r,
            Theme.DIALOG_OVERLAY_COLOR.g,
            Theme.DIALOG_OVERLAY_COLOR.b,
            Theme.DIALOG_OVERLAY_ALPHA
        ))

        screen.blit(
            overlay,
            (0, 0)
        )

    # --------------------------------------------------

    def _draw_window(self, screen):

        pygame.draw.rect(

            screen,

            Theme.DIALOG_BACKGROUND_COLOR,

            self.rect,

            border_radius=Theme.DIALOG_RADIUS
        )

        pygame.draw.rect(

            screen,

            Theme.DIALOG_BORDER_COLOR,

            self.rect,

            width=2,

            border_radius=Theme.DIALOG_RADIUS
        )

        pygame.draw.line(

            screen,

            Theme.DIALOG_SEPARATOR_COLOR,

            (
                self.rect.left,
                self.rect.top +
                Theme.DIALOG_HEADER_HEIGHT
            ),

            (
                self.rect.right,
                self.rect.top +
                Theme.DIALOG_HEADER_HEIGHT
            )
        )

    # --------------------------------------------------

    def _draw_title(self, screen):

        surface = self.title_font.render(

            self.title,

            True,

            Theme.DIALOG_TITLE_COLOR
        )

        screen.blit(

            surface,

            (
                self.rect.left +
                Theme.DIALOG_PADDING,

                self.rect.top + 10
            )
        )

    # --------------------------------------------------

    def _draw_message(self, screen):

        surface = self.text_font.render(

            self.message,

            True,

            Theme.DIALOG_TEXT_COLOR
        )

        rect = surface.get_rect(

            center=(

                self.rect.centerx,

                self.rect.centery - 20
            )
        )

        screen.blit(
            surface,
            rect
        )

    # --------------------------------------------------

    def _draw_buttons(self, screen):

        for rect, caption in zip(

            self.button_rects,

            self.button_captions
        ):

            pygame.draw.rect(

                screen,

                Theme.DIALOG_BORDER_COLOR,

                rect,

                border_radius=6
            )

            text = self.text_font.render(

                caption,

                True,

                Theme.DIALOG_TEXT_COLOR
            )

            text_rect = text.get_rect(
                center=rect.center
            )

            screen.blit(
                text,
                text_rect
            )