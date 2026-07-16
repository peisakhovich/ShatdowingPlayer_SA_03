
from gui.panels.control_panel import ControlPanel

class MainWindow:

    def __init__(self, screen, gui, image_loader):

        self.screen = screen
        self.gui = gui

        self.background_color = (30, 30, 30)
        self.control_panel = ControlPanel(image_loader)

    def handle_event(self, event):
        command = self.control_panel.handle_event(event)
        if command:
            print("Команда:", command)
            
    def update(self):
        self.control_panel.update()

    def draw(self):

        self.screen.fill(self.background_color)
        self.control_panel.draw(self.screen)

        # Позже здесь будут вызываться панели:
        #
        # self.control_panel.draw(self.screen)
        # self.info_panel.draw(self.screen)
        # self.phrase_panel.draw(self.screen)