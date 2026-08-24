
import os

import pygame
    

from gui.manager import GUIManager
from gui.layout import Layout
from gui.main_window import MainWindow
from core.config import Config
from gui.services.image_loader import ImageLoader
from gui.services.font_manager import FontManager

from session.providers.guest_provider import GuestProvider
from session.session import Session
from audio.player import Player
from audio.scenario_provider import ScenarioProvider
from core.logger import logger


class Application:

    def __init__(self):

        logger.info("Start Application")
        pygame.init()

        if not Config.PLAN_SESSION_FILE.exists():
            GuestProvider.build(Config.PLAN_SESSION_FILE)
        
        self.session = Session.load(Config.PLAN_SESSION_FILE)

        self.scenario_provider = ScenarioProvider("audio/scenarios.json")

        self.player = Player(self.session,self.scenario_provider)

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
            self.font_manager,
            self.session,
            self.player,
            self.scenario_provider
        )

    def run(self):

        self.running = True

        while self.running:

            dt = self.clock.tick(Config.FPS)

            time_delta = dt / 1000.0

            for event in pygame.event.get():

                self.gui.process_events(event)

                command = self.window.handle_event(event)

                if command == "quit":

                    self.running = False

            self.gui.update(time_delta)

            self.window.update()

            # Обновление состояния Player
            self.player.update(dt)
            #settings_window.update()

            self.window.draw()

            self.gui.draw(self.screen)

            pygame.display.flip()

        logger.info("Finsh Application")
        pygame.quit()