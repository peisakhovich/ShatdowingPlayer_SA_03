import pygame
import os


class ImageLoader:
    def __init__(self):
        self._cache = {}

    
    def load(self, path, alpha=True):

        #print(f"Загрузка изображения: {path}")
        full_path = os.path.abspath(path)
        #print(f"Полный путь: {full_path}")

        if full_path in self._cache:
            return self._cache[full_path]

        image = pygame.image.load(full_path)

        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()

        self._cache[full_path] = image

        return image

    def clear_cache(self):
        self._cache.clear()