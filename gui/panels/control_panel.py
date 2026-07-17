import pygame
from core.config import Config 
from gui.layout import Layout
from gui.theme import Theme
from gui.widgets.image_button import ImageButton

from gui.widgets.horizontal_slider import HorizontalSlider



class ControlPanel:

    def __init__(self, image_loader):

        self.image_loader = image_loader

        self.font = pygame.font.SysFont("Segoe UI", 18)
       

        # --------------------------------------------------
        # Панель
        # --------------------------------------------------

        self.rect = Layout.CP_RECT

        self.buttons = {}

        self.speed_slider = HorizontalSlider(

            caption="Speed",

            rect=(20, 28, 220, 24),

            start_value=1.0,

            value_range=(0.2, 2.0),

            font=self.font,

            formatter=lambda v: f"{v:.2f}x"
        )

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
                f"{Config.ICON_PATH}/{name}.png",
                default=Config.APP_ICON
            ),

            image_hover=self.image_loader.load(
                f"{Config.ICON_PATH}/{name}_hover.png",
                default=Config.APP_ICON
            ),

            image_pressed=self.image_loader.load(
                f"{Config.ICON_PATH}/{name}_pressed.png",
                default=Config.APP_ICON
            )
        )

    # --------------------------------------------------
    # Обработка событий
    # --------------------------------------------------

    def handle_event(self, event):

        self.speed_slider.handle_event(event)

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

        self.speed_slider.update()
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

        # Гор.Слайдеры
        self.speed_slider.draw(screen)
        
        # Кнопки
        for button in self.buttons.values():
            button.draw(screen)