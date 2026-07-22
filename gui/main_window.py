import pygame

from gui.panels.control_panel import ControlPanel
from gui.dialogs.dialog import Dialog


class MainWindow:

    def __init__(
        self,
        screen,
        gui,
        image_loader,
        font_manager
    ):

        self.screen = screen
        self.gui = gui

        self.background_color = (30, 30, 30)

        self.control_panel = ControlPanel(
            image_loader,
            font_manager
        )

        self.font_manager = font_manager

        # Активный модальный диалог
        self.active_dialog = None

    # --------------------------------------------------
    # Показать диалог выхода
    # --------------------------------------------------

    def show_exit_dialog(self):

        self.active_dialog = Dialog(

            parent_rect=self.screen.get_rect(),

            font_manager=self.font_manager,

            title="Exit",

            message="Хотите завершить приложение \n Или еще немного поработаете ",

            buttons=[
                "Yes",
                "No",
                                 
                ]
        )

        self.active_dialog.show()

    # --------------------------------------------------
    # Обработка событий
    # --------------------------------------------------

    def handle_event(self, event):

        #
        # Если открыт модальный диалог,
        # он получает события первым.
        #

        if self.active_dialog:

            result = self.active_dialog.handle_event(event)

            if result == 0:

                return "quit"

            elif result == 1:

                self.active_dialog = None

            return None

        #
        # Если диалогов нет
        #

        if event.type == pygame.QUIT:

            self.show_exit_dialog()

            return None

        #
        # Передаем событие панели управления
        #

        command = self.control_panel.handle_event(event)

        if command == "quit":

            self.show_exit_dialog()
            return None

        if command:

            print("Команда:", command)

    # --------------------------------------------------
    # Обновление
    # --------------------------------------------------

    def update(self):

        if self.active_dialog:

            self.active_dialog.update()

        else:

            self.control_panel.update()

    # --------------------------------------------------
    # Отрисовка
    # --------------------------------------------------

    def draw(self):

        self.screen.fill(
            self.background_color
        )

        #
        # Основной интерфейс
        #

        self.control_panel.draw(
            self.screen
        )

        #
        # Модальный диалог
        #

        if self.active_dialog:

            self.active_dialog.draw(
                self.screen
            )