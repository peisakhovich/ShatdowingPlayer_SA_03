import pygame


from gui.panels.control_panel import ControlPanel
from gui.dialogs.dialog import Dialog
from gui.widgets.check_box import CheckBox
from gui.widgets.text_window import TextWindow
from gui.theme import Theme
from core.config import Config 
from gui.layout import Layout


class MainWindow:

    def __init__(
        self,
        screen,
        gui,
        image_loader,
        font_manager,
        session,
        player

    ):
        self.session = session
        self.player = player


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

       
        self.text=self.session.current_item.get("phrase_text")
        self.translate=self.session.current_item.get("translate_text")
        self.info=self.session.description


        Height_Texts = Layout.HEIGHT - Layout.CP_HEIGHT - 40


        self.tw_text = TextWindow(

            rect=(20, 20, Layout.WIDTH-40, Height_Texts*60/100),
            font=font_manager.load(
                32,
                Config.FONT_REGULAR
            ),
            text=self.text,
            align="left"
        )    

        self.tw_translate = TextWindow(
        
            rect=(20, 20+Height_Texts*60/100+10, Layout.WIDTH*0.6, Height_Texts*40/100),
            font=font_manager.load(
                23,
                Config.FONT_REGULAR
            ),
            text=self.translate,
            align="left"
            )

        self.tw_info = TextWindow(
        
            rect=(35+Layout.WIDTH*0.6, 20+Height_Texts*60/100+10, Layout.WIDTH*0.4-55, Height_Texts*40/100),
            font=font_manager.load(
                14,
                Config.FONT_REGULAR
            ),
            text=self.info,
            align="left"
            )    

    

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
                "Later",
                "Early",

                ],
            default_button=1     
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

        if command is not None:

            match command:

                case ("button", name):

                    print(f"Button: {name}")

                    if name == "play":
                        self.player.play()
                        

                    elif name == "next":
                        self.player.next()

                case ("slider", name, value):

                    print(f"Slider: {name} = {value}")

                    if name == "voice_speed":
                        self.player.set_speed(value)

                    elif name == "pause_before_translation":
                        self.player.set_pause_before_translation(int(value))

                    elif name == "pause_between_sentences":
                        self.player.set_pause_between_sentences(int(value))

                case ("checkbox", name, checked):

                    print(f"Checkbox: {name} = {checked}")

                    # Пока просто выводим.
                    # Позже Player будет менять режим воспроизведения.

       

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

        # Прорисовка TextWindows
        self.tw_text.draw(self.screen)

        self.tw_translate.draw(self.screen)
        self.tw_info.draw(self.screen)
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