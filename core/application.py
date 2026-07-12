import pygame

from gui.manager import GUIManager
from gui.main_window import MainWindow


class Application:

    def __init__(self):

        pygame.init()

        self.size = (900, 600)

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("SA_03")

        self.clock = pygame.time.Clock()

        # GUI
        self.gui = GUIManager(self.size)

        # Главное окно
        self.window = MainWindow(
            self.screen,
            self.gui
        )

    def run(self):

        running = True

        while running:

            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                self.gui.process_events(event)
                self.window.handle_event(event)

            self.gui.update(time_delta)

            self.window.update()

            self.window.draw()

            self.gui.draw(self.screen)

            pygame.display.flip()

        pygame.quit()