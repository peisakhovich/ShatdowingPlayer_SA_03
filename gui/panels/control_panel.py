"""
Sound Language Studio
---------------------

Module:
    gui.panels.control_panel

Purpose:
    Provides the main control panel for playback, sliders,
    checkboxes, buttons, and interaction hints.

ru:
    Предоставляет основную панель управления воспроизведением,
    слайдерами, флажками, кнопками и подсказками.
"""
import pygame
from pygame import surface

from core.config import Config 
from gui.layout import Layout
from gui.theme import Theme
from gui.widgets.image_button import ImageButton
from gui.widgets.horizontal_slider import HorizontalSlider
from gui.widgets.text_button import TextButton
from gui.widgets.check_box import CheckBox
from gui.widgets.hint import Hint


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

        self.hint = Hint(self.font_manager)

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


        for index, button_def in enumerate(Layout.BTN_DEFS):

            name = button_def["name"]
            hint = button_def["hint"]

            x = Layout.BTN_START_X + index * (
                Layout.BTN_WIDTH +
                Layout.BTN_INTERVAL
            )

            self.buttons[name] = self._create_button(
                name,
                hint,
                x,
                Layout.BTN_START_Y
            )

    # --------------------------------------------------

    def _create_button(self, name, hint, x, y):

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
            ),

            hint=hint
        )

    # --------------------------------------------------
    # Обработка событий
    # --------------------------------------------------

    def handle_event(self, event):

        for name, slider in self.sliders.items():

            if slider.handle_event(event):
                return ("slider", name, slider.value)


        for name, button in self.buttons.items():

            if button.handle_event(event):
                return ("button", name)
    
        for name, checkbox in self.checkboxes.items():

            if checkbox.handle_event(event) is not None:
                return ("checkbox", name, checkbox.checked)

    # --------------------------------------------------
    # Обновление
    # --------------------------------------------------

    def update(self):

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        hovered_button = None

        for button in self.buttons.values():

            button.update(
                mouse_pos,
                mouse_pressed
            )

            if button.is_hovered:
                hovered_button = button

        if hovered_button:
            self.hint.update(
                hovered_button.hint,
                hovered_button.rect
            )
        else:
            self.hint.hide()

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

        # Hint
        self.hint.draw(screen)

        # Чек боксы прорисовка
        for checkbox in self.checkboxes.values():
            checkbox.draw(screen)   