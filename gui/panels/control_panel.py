import pygame
from core.config import Config 
from gui.layout import Layout
from gui.theme import Theme

from gui.widgets.image_button import ImageButton


class ControlPanel:

    def __init__(self, image_loader):

        self.image_loader = image_loader

        # --------------------------------------------------
        # Панель
        # --------------------------------------------------

        self.rect = Layout.CP_RECT

        self.buttons = {}

        self._create_buttons()

    # --------------------------------------------------
    # Создание кнопок
    # --------------------------------------------------

    def _create_buttons(self):


        for index, name in enumerate(Layout.BTN_DEFS):

            x = Layout.BTN_START_X + index * (
                Layout.BTN_WIDTH +
                Layout.BTN_INTERVAL
            )

            self.buttons[name] = self._create_button(
                name,
                x,
                Layout.BTN_START_Y
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
            Theme.TCP_BACKGROUND_COLOR,
            self.rect,
            border_radius=Theme.TCP_BORDER_LINE_RADIUS
        )

        # Рамка панели
        pygame.draw.rect(
            screen,
            Theme.TCP_BORDER_LINE_COLOR,
            self.rect,
            Theme.TCP_BORDER_LINE_WIDTH,
            Theme.TCP_BORDER_LINE_RADIUS
        )

        # Кнопки
        for button in self.buttons.values():
            button.draw(screen)