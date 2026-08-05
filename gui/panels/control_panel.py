import pygame
from pygame import surface

from core.config import Config 
from gui.layout import Layout
from gui.theme import Theme
from gui.widgets.image_button import ImageButton
from gui.widgets.horizontal_slider import HorizontalSlider
from gui.widgets.text_button import TextButton
from gui.widgets.check_box import CheckBox


class ControlPanel:

    def __init__(self, image_loader,font_manager):

        self.image_loader = image_loader
        self.font_manager = font_manager

        self.font = self.font_manager.load(10,   Config.FONT_BOLD)

        # --------------------------------------------------
        # Панель
        # --------------------------------------------------

        self.rect = Layout.CP_RECT
       
        self.sliders = {}
        self._create_sliders()
        
        self.buttons = {}
        self._create_buttons()

        self.checkboxes = {}
        self._create_checkboxes()
        

    #--------------------------------------------------
    # Создаем чекбоксы для управления отображением  и озвучкой текста и перевода
    #--------------------------------------------------
    def _create_checkboxes(self):    
        
        for i, (name, (caption, value)) in enumerate(Layout.CB_DEFS.items()):

            checkbox = CheckBox(
                rect=(
                    Layout.CB_X,
                    self.rect.y + Layout.CB_Y + i * Layout.CB_INTERVAL,
                    Theme.CB_SIZE,
                    Theme.CB_SIZE
                ),
                caption=caption,
                font=self.font_manager.load(
                    Layout.CB_FONT_SIZE,
                    Config.FONT_REGULAR
                ),
                checked=value   
            )

            self.checkboxes[name] = checkbox


    # --------------------------------------------------
    # Создание набора слайдеров 
    # --------------------------------------------------

    def _create_sliders(self):

        for i, slider_def in enumerate(Layout.SLIDER_DEFS):

            slider = HorizontalSlider(

                caption=slider_def["caption"],

                rect=(
                    self.rect.x + Layout.HSL_X,
                    self.rect.y + Layout.HSL_Y + i * (Theme.HSL_KNOB_HEIGHT*1.6),
                    Layout.HSL_TRACK_WIDTH,
                    Theme.HSL_KNOB_HEIGHT-7
                ),

                start_value=slider_def["start"],
                value_range=slider_def["range"],
                font=self.font_manager.load(
                    Layout.HSL_FONT_SIZE,
                    Config.FONT_REGULAR
                ),

                formatter=slider_def["formatter"]
            )

            self.sliders[slider_def["name"]] = slider

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

        for name, slider in self.sliders.items():

            if slider.handle_event(event):
                return f"{name}: {slider.value}"


        for name, button in self.buttons.items():

            if button.handle_event(event):
                return name
    
        for name, checkbox in self.checkboxes.items():

            if checkbox.handle_event(event) is not None:
                return f"{name}: {checkbox.checked}"

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

        for slider in self.sliders.values():
            slider.update()

        # self.test_button.update()

        for checkbox in self.checkboxes.values():
            checkbox.update()


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
        for slider in self.sliders.values():
            slider.draw(screen)    
        
        
        # Кнопки
        for button in self.buttons.values():
            button.draw(screen)

        # test button
        #self.test_button.draw(screen)    

        # Чек боксы прорисовка
        for checkbox in self.checkboxes.values():
            checkbox.draw(screen)   