import pygame
from gui.manager import GUIManager
from gui.main_window import MainWindow


class App:


    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (900,600)
        )

        self.manager = GUIManager(
            (900,600)
        )

        self.window = MainWindow(
            self.manager
        )

        self.running = True



    def run(self):

        clock = pygame.time.Clock()


        while self.running:

            time_delta = clock.tick(60)/1000


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running=False


                self.manager.manager.process_events(event)



            self.manager.manager.update(
                time_delta
            )


            self.screen.fill(
                pygame.Color("#202020")
            )


            self.manager.manager.draw_ui(
                self.screen
            )


            pygame.display.update()


        pygame.quit()