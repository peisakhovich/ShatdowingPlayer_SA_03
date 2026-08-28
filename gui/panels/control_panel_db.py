import pygame
from pygame import surface

from core.config import Config 
from gui.layout import Layout
from gui.theme import Theme
from gui.widgets.image_button import ImageButton
# from gui.widgets.horizontal_slider import HorizontalSlider
# from gui.widgets.text_button import TextButton
# from gui.widgets.check_box import CheckBox


class ControlPanel:

    def __init__(self, image_loader,font_manager):

        self.image_loader = image_loader
        self.font_manager = font_manager

        self.font = self.font_manager.load(10,   Config.FONT_BOLD)

        # --------------------------------------------------
        # Панель
        # --------------------------------------------------

        self.rect = Layout.DB_CP_RECT
       
        
        self.buttons = {}
        self._create_buttons()


    # --------------------------------------------------
    # Создание набора кнопок
    # --------------------------------------------------

    def _create_buttons(self):


        for index, name in enumerate(Layout.DB_BTN_DEFS):
  
            x = Layout.DB_BTN_START_X + index * (
                Layout.DB_BTN_WIDTH +
                Layout.DB_BTN_INTERVAL
            )

            self.buttons[name] = self._create_button(
                name,
                x,
                Layout.DB_BTN_START_Y
            )

    # --------------------------------------------------

    def _create_button(self, name, x, y):

        return ImageButton(

            rect=(
                x,
                y,
                Layout.DB_BTN_WIDTH,
                Layout.DB_BTN_HEIGHT
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
    

        for name, button in self.buttons.items():

            if button.handle_event(event):
                return ("button", name)
    
     
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

