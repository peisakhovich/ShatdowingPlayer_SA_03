import pygame


from gui.panels.control_panel import ControlPanel
from gui.dialogs.dialog import Dialog
from gui.widgets.check_box import CheckBox
from gui.widgets.text_window import TextWindow
from gui.theme import Theme
from core.config import Config 
from gui.layout import Layout
from gui.settings_window import SettingsWindow


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

        
        # self.text=self.session.current_item.get("phrase_text")
        # self.translate=self.session.current_item.get("translate_text")
        # self.info=self.session.description+" | "+self.session.name+" | "+str(self.session.current_index+1)+"/"+str(self.session.items_count) 
        self.text=self.player.get_msg_top()
        self.translate=self.player.get_msg_bottom()
        player.update_info(0)
        
        self.info=self.player.get_msg_info()


        Height_Texts = Layout.HEIGHT - Layout.CP_HEIGHT - 40


        self.tw_top = TextWindow(

            rect=(20, 20, Layout.WIDTH-40, Height_Texts*60/100),
            font=font_manager.load(
                32,
                Config.FONT_REGULAR
            ),
            text=self.text,
            align="left"
        )    

        self.tw_bottom = TextWindow(
        
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

    
        self.settings_window = SettingsWindow(Layout.SETTINGS_RECT)

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

        if self.settings_window.visible:
            self.settings_window.handle_event(event)
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

                    elif name == "pause":
                        self.player.pause()

                    elif name == "stop":
                        self.player.stop()                            

                    elif name == "next":
                        self.player.next()

                    elif name == "prev":
                        self.player.prev()

                    elif name == "first":
                        self.player.first()

                    elif name == "last":
                        self.player.last()

                    elif name == "quit":
                        self.show_exit_dialog()
                        return None        
                    elif name == "settings":
                        self.settings_window.show()

                case ("slider", name, value):

                    print(f"Slider: {name} = {value}")

                    if name == "voice_speed":
                        self.player.set_speed(value)

                    elif name == "factor_pause_before_translation":
                        self.player.set_factor_pause_before_translation(float(value))

                    elif name == "pause_between_sentences":
                        self.player.set_pause_between_sentences(int(value))

                case ("checkbox", name, checked):

                    print(f"Checkbox: {name} = {checked}")
                    self.player.set_option(name, checked)

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


            self.tw_top.text=self.player.get_msg_top()
            self.tw_bottom.text=self.player.get_msg_bottom()
            self.tw_info.text=self.player.get_msg_info()


            # self.tw_info.text=self.session.description+" | "+self.session.name+" | " \
            #     +str(self.session.current_index+1)+"/"+str(self.session.items_count) + "|  " \
            #     + "translate_voice: " + self.session.current_item.get("translate_voice") \
            #     + " | translate_voice_gender: " + self.session.current_item.get("translate_voice_gender") \
            #     + " | pause_ms: " + str(self.session.current_item.get("pause_ms")) \
            #     + " | speed: " + str(self.session.current_item.get("speed")) \
            #     + " | repeat_count: " + str(self.session.current_item.get("repeat_count"))   

            

    # --------------------------------------------------
    # Отрисовка
    # --------------------------------------------------

    def draw(self):

        self.screen.fill(
            self.background_color
        )

        # Прорисовка TextWindows
        self.tw_top.draw(self.screen)

        self.tw_bottom.draw(self.screen)
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

        self.settings_window.draw(self.screen)