import os

import pygame
    
from gui.manager import GUIManager
from gui.layout import Layout
from gui.main_window import MainWindow
from core.config import Config
from gui.services.image_loader import ImageLoader
from gui.services.font_manager import FontManager


class Application:

    def __init__(self):

        pygame.init()

        self.size = Layout.WINDOW_SIZE

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_icon(pygame.image.load( os.path.join(Config.ICON_PATH, Config.ICON_APP)))
        pygame.display.set_caption(Config.TITLE)

        self.clock = pygame.time.Clock()

        # GUI
        self.gui = GUIManager(self.size)

        self.image_loader = ImageLoader()
        self.font_manager  = FontManager()

        # Главное окно
        self.window = MainWindow(
            self.screen,
            self.gui,
            self.image_loader,
            self.font_manager

        )

    def run(self):

        self.running = True

        while self.running:

            time_delta = self.clock.tick(Config.FPS) / 1000.0

            for event in pygame.event.get():

                self.gui.process_events(event)

                command = self.window.handle_event(event)

                if command == "quit":

                    self.running = False

            self.gui.update(time_delta)

            self.window.update()

            self.window.draw()

            self.gui.draw(self.screen)

            pygame.display.flip()

        pygame.quit()