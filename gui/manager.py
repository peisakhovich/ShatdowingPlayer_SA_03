"""
Sound Language Studio
---------------------

Module:
    gui.manager

Purpose:
    Manages the pygame_gui interface, including event processing,
    UI updates, and rendering.

ru:
    Управляет интерфейсом pygame_gui, включая обработку событий,
    обновление элементов интерфейса и их отображение.
"""
import pygame_gui


class GUIManager:

    def __init__(self, size):

        self.manager = pygame_gui.UIManager(
            size,
            "gui/theme.json"
        )

    def process_events(self, event):
        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self, screen):
        self.manager.draw_ui(screen)