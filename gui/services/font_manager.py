"""
Sound Language Studio
---------------------

Module:
    gui.services.font_manager

Purpose:
    Loads and caches Pygame fonts used by the application interface.

ru:
    Загружает и кэширует шрифты Pygame, используемые
    интерфейсом приложения.
"""
import os
import pygame

from core.config import Config


class FontManager:

    def __init__(self):

        self._cache = {}

   
    def load(
        self,
        size,
        font_name=Config.FONT_REGULAR
    ):

        key = (font_name, size)

        if key in self._cache:
            return self._cache[key]

        full_path = os.path.abspath(
            os.path.join(
                Config.FONT_PATH,
                font_name
            )
        )

        font = pygame.font.Font(
            full_path,
            size
        )

        self._cache[key] = font

        return font