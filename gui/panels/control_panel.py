import pygame
from core.config import Config 
from gui.layout import Layout
from gui.theme import Theme
from gui.widgets.image_button import ImageButton

from gui.widgets.horizontal_slider import HorizontalSlider
from gui.widgets.text_button import TextButton



class ControlPanel:

    def __init__(self, image_loader,font_manager):

        self.image_loader = image_loader
        self.font_manager = font_manager

        self.font = self.font_manager.load(10,   Config.FONT_BOLD)
        #self.font = pygame.font.SysFont("Segoe UI", 12)
       

        # --------------------------------------------------
        # Панель
        # --------------------------------------------------

        self.rect = Layout.CP_RECT
       
        self.sliders = []
        self._create_sliders()
        
        self.buttons = {}
        self._create_buttons()

        self.test_button = TextButton(

            rect=(250, self.rect.y + 25, 120, Theme.TB_HEIGHT),
            caption="TEST",
            font=self.font
            )

    # --------------------------------------------------
    # Создание набора слайдеров 
    # --------------------------------------------------

    def _create_sliders(self):
        self.speed_slider = HorizontalSlider(

            caption="Speed",
            rect=(self.rect.x + 10, self.rect.y + 24, 180, 12),
            start_value=1.0,
            value_range=(0.1, 1.2),
            font=self.font,
            formatter=lambda v: f"{v:.2f} x"
        )

        self.pause_slider = HorizontalSlider(

            caption="Pause",
            rect=(self.rect.x + 10, self.rect.y + 56, 180, 12),
            start_value=1.0,
            value_range=(0.5, 5.0),
            font=self.font,
            formatter=lambda v: f"{v:.2f} s"
        )        
        self.sliders.extend(
        [
            self.speed_slider,
            self.pause_slider
        ]
        )

    # --------------------------------------------------
    # Создание набора кнопок
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

        for slider in self.sliders:
            slider.handle_event(event)

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

        for slider in self.sliders:
            slider.update()

        self.test_button.update()

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
        for slider in self.sliders:
            slider.draw(screen)
        
        
        # Кнопки
        for button in self.buttons.values():
            button.draw(screen)

        # test button
        self.test_button.draw(screen)            