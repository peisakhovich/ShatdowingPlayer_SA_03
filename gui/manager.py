import pygame_gui


class GUIManager:

    def __init__(self, size):

        self.manager = pygame_gui.UIManager(
            size,
            "gui/theme.json"
        )