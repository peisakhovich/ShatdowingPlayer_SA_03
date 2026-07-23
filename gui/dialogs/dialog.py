import pygame

from core.config import Config
from gui.theme import Theme
from gui.widgets.text_button import TextButton


class Dialog:

    def __init__(
        self,
        parent_rect,
        font_manager,
        title,
        message,
        buttons,
        default_button=0
    ):

        # ---------------------------------------
        # Родительское окно
        # ---------------------------------------

        self.parent_rect = pygame.Rect(parent_rect)

        # ---------------------------------------
        # Текст
        # ---------------------------------------

        self.title = title
        self.message = message

        # ---------------------------------------
        # Подписи кнопок
        # ---------------------------------------

        self.button_captions = buttons
        self.buttons = []

        # Индекс кнопки, имеющей клавиатурный фокус
        self.focus_index = default_button

        # ---------------------------------------
        # Шрифты
        # ---------------------------------------

        self.title_font = font_manager.load(
            18,
            Config.FONT_BOLD
        )

        self.text_font = font_manager.load(
            14,
            Config.FONT_REGULAR
        )

        # ---------------------------------------
        # Состояние
        # ---------------------------------------

        self.visible = False
        self.result = None

        # ---------------------------------------

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
            
        #
        # Управление клавиатурой
        #

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:

                self._set_focus(
                    self.focus_index - 1
                )

                return None

            elif event.key == pygame.K_RIGHT:

                self._set_focus(
                    self.focus_index + 1
                )

                return None

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER
            ):

                return self.focus_index

        #
        # Управление мышью
        #

        for index, button in enumerate(self.buttons):

            if button.handle_event(event):

                self.result = index
                return index

        return None

    # --------------------------------------------------

    def update(self):

        if not self.visible:
            return

        for button in self.buttons:

            button.update()

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
    def _calculate_geometry(self):
        """
        Вычисляет размеры и положение окна диалога.
        """

        # Ширина заголовка
        #

        title_width = self.title_font.size(
            self.title
        )[0]

        # Ширина сообщения
        #

        message_width = self.text_font.size(
            self.message
        )[0]


        # Ширина будущих кнопок
        #

        buttons_width = 0

        for caption in self.button_captions:

            text_width = self.text_font.size(
                caption
            )[0]

            buttons_width += (
                text_width +
                Theme.TB_PADDING_X * 2
            )

        if len(self.button_captions) > 1:

            buttons_width += (

                len(self.button_captions) - 1

            ) * Theme.DIALOG_BUTTON_INTERVAL


        # Максимальная ширина содержимого
        #

        content_width = max(

            title_width,

            message_width,

            buttons_width
        )


        # Размер окна
        #

        dialog_width = max(

            Theme.DIALOG_MIN_WIDTH,

            content_width +

            Theme.DIALOG_PADDING_X * 2
        )

        self.rect = pygame.Rect(
            0,
            0,
            dialog_width,
            Theme.DIALOG_HEIGHT
        )

        self.rect.center = self.parent_rect.center
    # --------------------------------------------------

    def _create_buttons(self):
        """
        Создает кнопки и размещает их в нижней части диалога.
        """
        self.buttons.clear()
        #
        # Создание кнопок
        #
        for caption in self.button_captions:

            button = TextButton(

                rect=(
                    0,
                    0,
                    0,
                    Theme.TB_HEIGHT
                ),
                caption=caption,
                font=self.text_font,
                auto_width=True
            )

            self.buttons.append(button)

        #
        # Общая ширина кнопок
        #

        total_width = sum(

            button.rect.width

            for button in self.buttons
        )

        if len(self.buttons) > 1:

            total_width += (

                len(self.buttons) - 1

            ) * Theme.DIALOG_BUTTON_INTERVAL
    
        # Начальная позиция
    
        x = self.rect.centerx - total_width // 2

        y = (  self.rect.bottom -
            Theme.DIALOG_PADDING_Y -
            Theme.TB_HEIGHT
        )

        # Размещение кнопок

        for button in self.buttons:

            button.rect.topleft = (x, y)
  
            x += ( button.rect.width +
                Theme.DIALOG_BUTTON_INTERVAL
            )

        # Устанавливаем фокус на кнопку
        #
        if self.buttons:

            self.focus_index = max(
                0,
                min(self.focus_index, len(self.buttons) - 1)
            )

            self.buttons[self.focus_index].focused = True
    # --------------------------------------------------
    
    def _set_focus(self, index):
        """
        Передает клавиатурный фокус
        указанной кнопке.
        """

        if not self.buttons:
            return

        #
        # Снимаем старый фокус
        #

        self.buttons[self.focus_index].focused = False

        #
        # Новый индекс
        #

        self.focus_index = index % len(self.buttons)

        #
        # Новый фокус
        #

        self.buttons[self.focus_index].focused = True



    def _draw_overlay(self, screen):

        overlay = pygame.Surface(
            self.parent_rect.size,
            pygame.SRCALPHA
        )

        overlay.fill(
            (
                Theme.DIALOG_OVERLAY_COLOR.r,
                Theme.DIALOG_OVERLAY_COLOR.g,
                Theme.DIALOG_OVERLAY_COLOR.b,
                Theme.DIALOG_OVERLAY_ALPHA
            )
        )

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
                self.rect.left + Theme.DIALOG_PADDING_X,

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

        for button in self.buttons:

            button.draw(screen)           

