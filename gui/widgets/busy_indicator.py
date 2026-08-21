import math
import pygame

from gui.theme import Theme


class BusyIndicator:

    def __init__(self, rect, font):
        self.rect = pygame.Rect(rect)
        self.font = font

        self.visible = False
        self.message = "Working..."

        # Анимация крутилки
        self.angle = 0.0
        self.rotation_speed = 180.0  # degrees / second

        # Время последнего обновления
        self.last_update = pygame.time.get_ticks()

    # ---------------------------------------------------------
    # Show / Hide
    # ---------------------------------------------------------

    def show(self, message="Working..."):
        self.message = message
        self.visible = True

        self.angle = 0.0
        self.last_update = pygame.time.get_ticks()

    def hide(self):
        self.visible = False

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    def update(self):
        if not self.visible:
            return

        now = pygame.time.get_ticks()

        dt = (now - self.last_update) / 1000.0
        self.last_update = now

        self.angle += self.rotation_speed * dt

        if self.angle >= 360.0:
            self.angle -= 360.0

    # ---------------------------------------------------------
    # Draw
    # ---------------------------------------------------------

    def draw(self, surface):

        if not self.visible:
            return

        # -----------------------------------------------------
        # Overlay
        # -----------------------------------------------------

        overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))

        surface.blit(
            overlay,
            self.rect.topleft
        )

        # -----------------------------------------------------
        # Center
        # -----------------------------------------------------

        center_x = self.rect.centerx
        center_y = self.rect.centery

        # -----------------------------------------------------
        # Spinner
        # -----------------------------------------------------

        spinner_radius = 18
        spinner_length = 10
        spinner_width = 4

        for i in range(8):

            angle = self.angle + i * 45

            radians = math.radians(angle)

            # Внешняя точка
            x1 = center_x + math.cos(radians) * spinner_radius
            y1 = center_y + math.sin(radians) * spinner_radius

            # Внутренняя точка
            x2 = center_x + math.cos(radians) * (
                spinner_radius - spinner_length
            )
            y2 = center_y + math.sin(radians) * (
                spinner_radius - spinner_length
            )

            # Чем дальше от текущей позиции, тем прозрачнее
            alpha = int(255 * (1.0 - i / 8))

            line_surface = pygame.Surface(
                self.rect.size,
                pygame.SRCALPHA
            )

            pygame.draw.line(
                line_surface,
                (255, 255, 255, alpha),
                (x2 - self.rect.x, y2 - self.rect.y),
                (x1 - self.rect.x, y1 - self.rect.y),
                spinner_width
            )

            surface.blit(
                line_surface,
                self.rect.topleft
            )

        # -----------------------------------------------------
        # Message
        # -----------------------------------------------------

        text_surface = self.font.render(
            self.message,
            True,
            Theme.TW_TEXT_COLOR
        )

        text_rect = text_surface.get_rect(
            midtop=(
                center_x,
                center_y + spinner_radius + 15
            )
        )

        surface.blit(
            text_surface,
            text_rect
        )