import pygame

from gui.theme import Theme


class TextButton:

    def __init__(
        self,
        rect,
        caption,
        font,
        auto_width
    ):


        # -------------------------
        # Параметры
        # -------------------------
        self.caption = caption
        self.font = font
        self.auto_width = auto_width

        # -------------------------
        # Состояние покоя
        # -------------------------
        self.state = "normal"

        # -------------------------
        # Геометрия начальная
        # -------------------------
        self.rect = pygame.Rect(rect)
        self._update_geometry()

    # --------------------------------------------------
    def _update_geometry(self):
        """
        Вычисляет геометрию кнопки.

        Ширина заданная при создании экземпляра кнопки остается 
        без изменений в случае auto_width=False.
        В противном случае вычисляется ширина по рендерингу capiton
        """
        if not self.auto_width:
            return

        text_width, _ = self.font.size(
            self.caption
        )
 
        self.rect.width =  text_width + Theme.TB_PADDING_X * 2

    def handle_event(self, event):
       
        # Нажатие ЛКМ
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.rect.collidepoint(event.pos):

                    self.state = "pressed"

        # Отпускание ЛКМ
        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:
                if self.state == "pressed":
                    self.state = "hover"
                    if self.rect.collidepoint(event.pos):
                        return True

        return False
    # --------------------------------------------------

    def update(self):
    
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # определяем состояние кнопки по отношениею к тому что делает мышь 
        if self.rect.collidepoint(mouse_pos):

            if mouse_pressed:
                self.state = "pressed"
            else:
                self.state = "hover"
        else:
            self.state = "normal"

    # --------------------------------------------------

    def draw(self, screen): 

        if self.state == "normal":

            background = Theme.TB_BACKGROUND_COLOR
            text_color = Theme.TB_TEXT_COLOR

        elif self.state == "hover":

            background = Theme.TB_BACKGROUND_HOVER_COLOR
            text_color = Theme.TB_TEXT_COLOR

        else:

            background = Theme.TB_BACKGROUND_PRESSED_COLOR
            text_color = Theme.TB_TEXT_PRESSED_COLOR    

        #
        # Надпись рендерим
        #

        text = self.font.render(
            self.caption,
            True,
            text_color
        )
        # выравниваем геометрию ао центру
        text_rect = text.get_rect(
            center=self.rect.center
        )
        # адаптируем ширину клавили по надписи
        #self.rect.width=min( self.rect.width , text_rect.width+Theme.TB_PADDING_X*2  )

        # Отрисовка Фона
        pygame.draw.rect(

            screen,
            background,
            self.rect,
            border_radius=Theme.TB_RADIUS
        )

        # Отрисовка Рамки
        pygame.draw.rect(

            screen,
            Theme.TB_BORDER_COLOR,
            self.rect,
            width=Theme.TB_BORDER_WIDTH,
            border_radius=Theme.TB_RADIUS
        )
        # выводим на экран
        screen.blit(
            text,
            text_rect
        )