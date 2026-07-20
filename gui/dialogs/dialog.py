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

        self.button_widths = []
        self.button_rects = []

        self._calculate_geometry()

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

        total_width = sum(self.button_widths)

        if len(self.button_widths) > 1:

            total_width += (

                len(self.button_widths) - 1

            ) * Theme.DIALOG_BUTTON_INTERVAL

        x = self.rect.centerx - total_width // 2

        y = (

            self.rect.bottom -

            Theme.DIALOG_PADDING_Y -

            Theme.DIALOG_BUTTON_HEIGHT
        )

        for width in self.button_widths:

            rect = pygame.Rect(

                x,

                y,

                width,

                Theme.DIALOG_BUTTON_HEIGHT
            )

            self.button_rects.append(rect)

            x += (

                width +

                Theme.DIALOG_BUTTON_INTERVAL
            )
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
                Theme.DIALOG_PADDING_X,

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
    def _calculate_geometry(self):

        #
        # Ширина заголовка
        #

        title_width = self.title_font.size(
            self.title
        )[0]

        #
        # Ширина сообщения
        #

        message_width = self.text_font.size(
            self.message
        )[0]

        #
        # Ширина кнопок
        #

        self.button_widths = []

        buttons_width = 0

        for caption in self.button_captions:

            text_width = self.text_font.size(
                caption
            )[0]

            button_width = (

                text_width +

                Theme.DIALOG_BUTTON_PADDING_X * 2
            )

            self.button_widths.append(
                button_width
            )

            buttons_width += button_width

        #
        # Интервалы между кнопками
        #

        if len(self.button_widths) > 1:

            buttons_width += (

                len(self.button_widths) - 1

            ) * Theme.DIALOG_BUTTON_INTERVAL

        #
        # Максимальная ширина содержимого
        #

        content_width = max(

            title_width,

            message_width,

            buttons_width
        )

        #
        # Итоговая ширина окна
        #

        dialog_width = max(

            Theme.DIALOG_MIN_WIDTH,

            content_width +

            Theme.DIALOG_PADDING_X  * 2
        )

        print("title_width:",title_width)
        print("message_width:",message_width)
        print("buttons_width:",buttons_width)

        #
        # Создаем окно
        #

        self.rect = pygame.Rect(

            0,

            0,

            dialog_width,

            Theme.DIALOG_HEIGHT
        )

        self.rect.center = self.parent_rect.center