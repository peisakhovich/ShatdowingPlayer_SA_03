import pygame


class MainWindow:

    def __init__(self, screen, manager):
        """
        Главное окно приложения.

        screen  - поверхность pygame.display
        manager - pygame_gui.UIManager
        """

        self.screen = screen
        self.manager = manager

        # Цвет фона (пока временный)
        self.background_color = (30, 30, 30)

    def handle_event(self, event):
        """
        Обработка событий приложения.
        Пока пусто.
        """
        pass

    def update(self):
        """
        Обновление состояния окна.
        Пока пусто.
        """
        pass

    def draw(self):
        """
        Отрисовка окна.
        """

        self.screen.fill(self.background_color)

        self.manager.draw(self.screen)

        # Когда появятся элементы pygame_gui,
        # они будут рисоваться здесь.
        self.manager.draw(self.screen)

        pygame.display.flip()