import pygame

from gui.theme import Theme


class TextWindow:

    def __init__(
        self,
        rect,
        font,
        text="",
        align="left"
    ):

        # ---------------------------------------
        # Геометрия
        # ---------------------------------------

        self.rect = pygame.Rect(rect)

        # ---------------------------------------
        # Параметры
        # ---------------------------------------

        self.font = font
        self.text = text
        self.align = align

    # ==================================================
    # Public
    # ==================================================

    def handle_event(self, event):

        return None

    # --------------------------------------------------

    def update(self):

        pass

    # --------------------------------------------------

    def draw(self, screen):

        #
        # Фон
        #

        pygame.draw.rect(

            screen,

            Theme.TW_BACKGROUND_COLOR,

            self.rect,

            border_radius=Theme.TW_RADIUS
        )

        #
        # Рамка
        #

        pygame.draw.rect(

            screen,

            Theme.TW_BORDER_COLOR,

            self.rect,

            width=Theme.TW_BORDER_WIDTH,

            border_radius=Theme.TW_RADIUS
        )

        #
        # Получаем готовые строки
        #

        lines = self._wrap_text()

        #
        # Высота строки
        #

        line_height = self.font.get_height()

        #
        # Начальная координата Y
        #

        y = self.rect.top + Theme.TW_PADDING_Y

        #
        # Рисуем строки
        #

        for line in lines:

            surface = self.font.render(

                line,

                True,

                Theme.TW_TEXT_COLOR
            )

            #
            # Горизонтальное выравнивание
            #

            if self.align == "center":

                text_rect = surface.get_rect(

                    midtop=(

                        self.rect.centerx,

                        y
                    )
                )

            elif self.align == "right":

                text_rect = surface.get_rect(

                    topright=(

                        self.rect.right -

                        Theme.TW_PADDING_X,

                        y
                    )
                )

            else:

                text_rect = surface.get_rect(

                    topleft=(

                        self.rect.left +

                        Theme.TW_PADDING_X,

                        y
                    )
                )

            screen.blit(

                surface,

                text_rect
            )

            #
            # Следующая строка
            #

            y += line_height

            #
            # Если дошли до нижней границы —
            # прекращаем рисование.
            #

            if y > self.rect.bottom - Theme.TW_PADDING_Y:

                break


    def set_text(self, text):

        self.text = text

    # --------------------------------------------------

    def get_text(self):

        return self.text
    
    # --------------------------------------------------
    # Выравнивание текста
    #     
    def _wrap_text(self):

        #
        # Максимальная ширина текста
        #

        max_width = (

            self.rect.width -

            Theme.TW_PADDING_X * 2
        )

        #
        # Разбиваем текст на слова
        #

        words = self.text.split()

        #
        # Результат
        #

        lines = []

        current_line = ""

        #
        # Формируем строки
        #

        for word in words:

            #
            # Проверяем строку с новым словом
            #

            if current_line:

                test_line = current_line + " " + word

            else:

                test_line = word

            #
            # Измеряем ширину
            #

            text_width, _ = self.font.size(test_line)

            if text_width <= max_width:

                current_line = test_line

            else:

                #
                # Сохраняем предыдущую строку
                #

                if current_line:

                    lines.append(current_line)

                #
                # Начинаем новую
                #

                current_line = word

        #
        # Последняя строка
        #

        if current_line:

            lines.append(current_line)

        return lines