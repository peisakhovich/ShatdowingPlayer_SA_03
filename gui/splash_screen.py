"""
Sound Language Studio
---------------------

Module:
    gui.splash_screen

Purpose:
    Displays the application splash screen with optional intro audio
    and handles startup completion or cancellation.

ru:
    Отображает заставку приложения с дополнительной звуковой дорожкой
    и обрабатывает завершение или отмену запуска.
"""
from pathlib import Path

import pygame

from core.config import Config


class SplashScreen:

    @staticmethod
    def show(screen, duration: float) -> bool:
        """
        Display the application splash screen.

        Returns:
            True  - splash completed normally
            False - application should quit
        """

        image_path = Path(Config.SPLASH_IMAGE)

        try:
            image = pygame.image.load(image_path).convert()
        except (pygame.error, FileNotFoundError) as exc:
            print(f"Unable to load splash image: {image_path}")
            print(exc)
            return True

        # Scale image proportionally to fit the window
        screen_width, screen_height = screen.get_size()
        image_width, image_height = image.get_size()

        scale = min(
            screen_width / image_width,
            screen_height / image_height
        )

        new_size = (
            int(image_width * scale),
            int(image_height * scale)
        )

        image = pygame.transform.smoothscale(image, new_size)

        image_rect = image.get_rect(
            center=screen.get_rect().center
        )

        # Start splash sound
        if Config.SPLASH_SOUND_ENABLED:
            try:
                pygame.mixer.music.load(Config.SPLASH_SOUND)
                pygame.mixer.music.play()
            except pygame.error as exc:
                print(f"Unable to play splash sound: {exc}")

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while True:

            elapsed = (
                pygame.time.get_ticks() - start_time
            ) / 1000.0

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return False

                if event.type in (
                    pygame.KEYDOWN,
                    pygame.MOUSEBUTTONDOWN,
                ):
                    pygame.mixer.music.stop()
                    return True

            screen.fill((0, 0, 0))
            screen.blit(image, image_rect)

            pygame.display.flip()

            if elapsed >= duration:
                pygame.mixer.music.stop()
                return True

            clock.tick(Config.FPS)