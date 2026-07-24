import pygame

from gui.theme import Theme


class CheckBox:

    def __init__(
        self,
        rect,
        caption,
        font,
        checked=False
    ):

        # ---------------------------------------
        # Геометрия
        # ---------------------------------------

        self.rect = pygame.Rect(rect)

        # ---------------------------------------
        # Параметры
        # ---------------------------------------

        self.caption = caption
        self.font = font

        # ---------------------------------------
        # Состояние
        # ---------------------------------------

        self.checked = checked
        self.state = "normal"
        self.pressed = False

    # ==================================================
    # Public
    # ==================================================

    def handle_event(self, event):

        #
        # Нажатие ЛКМ
        #

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.rect.collidepoint(event.pos):

                    self.pressed = True
                    self.state = "pressed"

        #
        # Отпускание ЛКМ
        
        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                if self.pressed :

                    self.pressed = False
                    self.state = "hover"

                    if self.rect.collidepoint(event.pos):

                        # Меняем состояние
                        self.checked = not self.checked

                        # Возвращаем новое состояние
                        return self.checked

        return None

    # --------------------------------------------------

    def update(self):

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):

            self.state = "hover"

        else:

            self.state = "normal"

    # --------------------------------------------------

    def draw(self, screen):

        #
        # Цвет фона
        #

        if self.state == "hover":

            background = Theme.CB_BACKGROUND_HOVER_COLOR

        else:

            background = Theme.CB_BACKGROUND_COLOR

        #
        # Корпус CheckBox
        #

        pygame.draw.rect(

            screen,

            background,

            self.rect,

            border_radius=Theme.CB_RADIUS
        )

        pygame.draw.rect(

            screen,

            Theme.CB_BORDER_COLOR,

            self.rect,

            width=Theme.CB_BORDER_WIDTH,

            border_radius=Theme.CB_RADIUS
        )

        #
        # Галочка
        #

        if self.checked:

            p = Theme.CB_CHECK_PADDING

            x1 = self.rect.left + p
            y1 = self.rect.centery

            x2 = self.rect.centerx - 1
            y2 = self.rect.bottom - p

            x3 = self.rect.right - p
            y3 = self.rect.top + p

            pygame.draw.line(

                screen,

                Theme.CB_CHECK_COLOR,

                (x1, y1),

                (x2, y2),

                Theme.CB_CHECK_WIDTH
            )

            pygame.draw.line(

                screen,

                Theme.CB_CHECK_COLOR,

                (x2, y2),

                (x3, y3),

                Theme.CB_CHECK_WIDTH
            )

        #
        # Подпись
        #

        text = self.font.render(

            self.caption,

            True,

            Theme.CB_TEXT_COLOR
        )

        text_rect = text.get_rect(

            midleft=(

                self.rect.right +

                Theme.CB_INTERVAL,

                self.rect.centery
            )
        )

        screen.blit(

            text,

            text_rect
        )