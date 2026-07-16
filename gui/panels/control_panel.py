import pygame
from core.config import Config 
from gui.layout import Layout
from gui.widgets.image_button import ImageButton


class ControlPanel:

    def __init__(self, image_loader):

        self.image_loader = image_loader

        # --------------------------------------------------
        # Панель
        # --------------------------------------------------

        self.rect = pygame.Rect(
            0,
            Layout.HEIGHT - 80,
            Layout.WIDTH,
            80
        )

        self.buttons = {}

        self._create_buttons()

    # --------------------------------------------------
    # Создание кнопок
    # --------------------------------------------------

    def _create_buttons(self):

        count = len(Layout.BUTTON_DEFS)

        total_width = (
            count * Layout.BTN_WIDTH +
            (count - 1) * Layout.BTN_INTERVAL
        )

        start_x = self.rect.centerx - total_width // 2
        y = self.rect.centery - Layout.BTN_HEIGHT // 2

        for index, name in enumerate(Layout.BUTTON_DEFS):

            x = start_x + index * (
                Layout.BTN_WIDTH +
                Layout.BTN_INTERVAL
            )

            self.buttons[name] = self._create_button(
                name,
                x,
                y
            )

    # --------------------------------------------------

    def _create_button(self, name, x, y):

        return ImageButton(

            rect=(
                x,
                y,
                Layout.BTN_WIDTH,
                Layout.BTN_HEIGHT
            ),

            image_normal=self.image_loader.load(
                f"{Config.ICON_PATH}/{name}.png"
            ),

            image_hover=self.image_loader.load(
                f"{Config.ICON_PATH}/{name}_hover.png"
            ),

            image_pressed=self.image_loader.load(
                f"{Config.ICON_PATH}/{name}_pressed.png"
            )
        )

    # --------------------------------------------------
    # Обработка событий
    # --------------------------------------------------

    def handle_event(self, event):

        for name, button in self.buttons.items():

            if button.handle_event(event):
                return name

        return None

    # --------------------------------------------------
    # Обновление
    # --------------------------------------------------

    def update(self):

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for button in self.buttons.values():
            button.update(
                mouse_pos,
                mouse_pressed
            )

    # --------------------------------------------------
    # Отрисовка
    # --------------------------------------------------

    def draw(self, screen):

        # Фон панели
        pygame.draw.rect(
            screen,
            (45, 45, 45),
            self.rect
        )

        # Рамка панели
        pygame.draw.rect(
            screen,
            (110, 110, 110),
            self.rect,
            2
        )

        # Кнопки
        for button in self.buttons.values():
            button.draw(screen)