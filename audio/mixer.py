import pygame


class AudioMixer:
    """Низкоуровневое управление воспроизведением MP3."""

    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    def load(self, path):
        """Загружает аудиофайл."""

        pygame.mixer.music.load(str(path))

    def play(self):
        """Начинает воспроизведение."""

        pygame.mixer.music.play()

    def pause(self):
        """Приостанавливает воспроизведение."""

        pygame.mixer.music.pause()

    def resume(self):
        """Продолжает воспроизведение."""

        pygame.mixer.music.unpause()

    def stop(self):
        """Останавливает воспроизведение."""

        pygame.mixer.music.stop()

    def is_playing(self):
        """Возвращает True, если музыка сейчас проигрывается."""

        return pygame.mixer.music.get_busy()