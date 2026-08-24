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
        # Layout сообщения
        # ---------------------------------------

        self.message_lines = []
        self.message_line_height = self.text_font.get_linesize()

        self.message_width = 0
        self.message_height = 0

        # ---------------------------------------
        # Геометрия
        # ---------------------------------------

        self.rect = pygame.Rect(
            0,
            0,
            0,
            0
        )

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

                self.result = self.focus_index

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
        Рассчитывает layout сообщения и размеры окна.
        """

        # ---------------------------------------
        # Максимальная ширина окна
        #
        # Не позволяем длинному сообщению
        # раздвигать dialog до ширины всего parent.
        # ---------------------------------------

        max_dialog_width = min(
            self.parent_rect.width - 20,
            600
        )

        max_message_width = (
            max_dialog_width -
            Theme.DIALOG_PADDING_X * 2
        )

        # ---------------------------------------
        # Формируем строки сообщения
        # ---------------------------------------

        self.message_lines = self._wrap_message(
            self.message,
            max_message_width
        )

        # ---------------------------------------
        # Размер блока сообщения
        # ---------------------------------------

        if self.message_lines:

            self.message_width = max(
                self.text_font.size(line)[0]
                for line in self.message_lines
            )

            self.message_height = (
                len(self.message_lines) *
                self.message_line_height
            )

        else:

            self.message_width = 0
            self.message_height = 0

        # ---------------------------------------
        # Ширина заголовка
        # ---------------------------------------

        title_width = self.title_font.size(
            self.title
        )[0]

        # ---------------------------------------
        # Ширина будущих кнопок
        # ---------------------------------------

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

        # ---------------------------------------
        # Ширина содержимого
        # ---------------------------------------

        content_width = max(
            title_width,
            self.message_width,
            buttons_width
        )

        # ---------------------------------------
        # Ширина окна
        # ---------------------------------------

        dialog_width = max(
            Theme.DIALOG_MIN_WIDTH,
            content_width +
            Theme.DIALOG_PADDING_X * 2
        )

        dialog_width = min(
            dialog_width,
            max_dialog_width
        )

        # ---------------------------------------
        # Высота окна
        #
        # header
        # + message
        # + spacing
        # + buttons
        # + padding
        # ---------------------------------------

        message_spacing = 14

        buttons_height = (
            Theme.TB_HEIGHT
            if self.button_captions
            else 0
        )

        buttons_spacing = (
            18
            if self.button_captions
            else 0
        )

        dialog_height = (
            Theme.DIALOG_PADDING_Y
            +
            Theme.DIALOG_HEADER_HEIGHT
            +
            self.message_height
            +
            message_spacing
            +
            buttons_spacing
            +
            buttons_height
            +
            Theme.DIALOG_PADDING_Y
        )

        # Минимальная высота
        dialog_height = max(
            dialog_height,
            Theme.DIALOG_HEIGHT
        )

        # ---------------------------------------
        # Rect
        # ---------------------------------------

        self.rect = pygame.Rect(
            0,
            0,
            dialog_width,
            dialog_height
        )

        self.rect.center = self.parent_rect.center

    # --------------------------------------------------

    def _wrap_message(self, message, max_width):
        """
        Разбивает сообщение на строки.

        Учитывает:
            - явные \\n;
            - пустые строки;
            - перенос по словам;
            - очень длинные слова.
        """

        if not message:
            return []

        result = []

        # Сначала учитываем явные переносы.
        paragraphs = message.split("\n")

        for paragraph in paragraphs:

            # Пустая строка.
            if paragraph == "":
                result.append("")
                continue

            words = paragraph.split()

            current_line = ""

            for word in words:

                # -----------------------------------
                # Пробуем добавить слово к текущей
                # строке.
                # -----------------------------------

                if current_line:

                    candidate = (
                        current_line +
                        " " +
                        word
                    )

                else:

                    candidate = word

                candidate_width = self.text_font.size(
                    candidate
                )[0]

                # -----------------------------------
                # Слово помещается
                # -----------------------------------

                if candidate_width <= max_width:

                    current_line = candidate
                    continue

                # -----------------------------------
                # Текущую строку сохраняем.
                # -----------------------------------

                if current_line:

                    result.append(
                        current_line
                    )

                # -----------------------------------
                # Если само слово слишком длинное,
                # режем его по ширине.
                # -----------------------------------

                if self.text_font.size(word)[0] > max_width:

                    chunks = self._split_long_word(
                        word,
                        max_width
                    )

                    if chunks:

                        result.extend(
                            chunks[:-1]
                        )

                        current_line = chunks[-1]

                    else:

                        current_line = ""

                else:

                    current_line = word

            # ---------------------------------------
            # Последняя строка абзаца.
            # ---------------------------------------

            if current_line:

                result.append(
                    current_line
                )

        return result

    # --------------------------------------------------

    def _split_long_word(self, word, max_width):
        """
        Разбивает очень длинное слово на части,
        если оно само шире допустимой области.
        """

        chunks = []
        current = ""

        for char in word:

            candidate = current + char

            if (
                current and
                self.text_font.size(candidate)[0] > max_width
            ):

                chunks.append(current)
                current = char

            else:

                current = candidate

        if current:
            chunks.append(current)

        return chunks

    # --------------------------------------------------

    def _create_buttons(self):
        """
        Создает кнопки и размещает их
        непосредственно под сообщением.
        """

        self.buttons.clear()

        # ---------------------------------------
        # Создание кнопок
        # ---------------------------------------

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

        if not self.buttons:
            return

        # ---------------------------------------
        # Общая ширина кнопок
        # ---------------------------------------

        total_width = sum(
            button.rect.width
            for button in self.buttons
        )

        if len(self.buttons) > 1:

            total_width += (
                len(self.buttons) - 1
            ) * Theme.DIALOG_BUTTON_INTERVAL

        # ---------------------------------------
        # Позиция кнопок
        # ---------------------------------------

        x = (
            self.rect.centerx -
            total_width // 2
        )

        y = (
            self.rect.bottom -
            Theme.DIALOG_PADDING_Y -
            Theme.TB_HEIGHT
        )

        # ---------------------------------------
        # Размещение
        # ---------------------------------------

        for button in self.buttons:

            button.rect.topleft = (
                x,
                y
            )

            x += (
                button.rect.width +
                Theme.DIALOG_BUTTON_INTERVAL
            )

        # ---------------------------------------
        # Фокус
        # ---------------------------------------

        self.focus_index = max(
            0,
            min(
                self.focus_index,
                len(self.buttons) - 1
            )
        )

        for button in self.buttons:
            button.focused = False

        self.buttons[
            self.focus_index
        ].focused = True

    # --------------------------------------------------

    def _set_focus(self, index):
        """
        Передает клавиатурный фокус
        указанной кнопке.
        """

        if not self.buttons:
            return

        # Снимаем старый фокус
        self.buttons[
            self.focus_index
        ].focused = False

        # Новый индекс
        self.focus_index = (
            index % len(self.buttons)
        )

        # Новый фокус
        self.buttons[
            self.focus_index
        ].focused = True

    # ==================================================
    # Drawing
    # ==================================================

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
                self.rect.left +
                Theme.DIALOG_PADDING_X,

                self.rect.top + 10
            )
        )

    # --------------------------------------------------

    def _draw_message(self, screen):
        """
        Отображает сообщение построчно.
        """

        if not self.message_lines:
            return

        # ---------------------------------------
        # Верхняя координата блока сообщения
        # ---------------------------------------

        y = (
            self.rect.top +
            Theme.DIALOG_PADDING_Y +
            Theme.DIALOG_HEADER_HEIGHT
        )

        # ---------------------------------------
        # Каждая строка отдельным Surface
        # ---------------------------------------

        for line in self.message_lines:

            surface = self.text_font.render(
                line,
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            rect = surface.get_rect(
                midtop=(
                    self.rect.centerx,
                    y
                )
            )

            screen.blit(
                surface,
                rect
            )

            y += self.message_line_height

    # --------------------------------------------------

    def _draw_buttons(self, screen):

        for button in self.buttons:

            button.draw(screen)