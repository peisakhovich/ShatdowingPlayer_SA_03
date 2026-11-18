"""
Sound Language Studio

Module:
    gui.widgets.busy_indicator

Purpose:
    Displays a busy overlay with an animated spinner, a status message,
    and optional progress details for mobile audio preparation.
"""
import math
import pygame

from gui.theme import Theme


class BusyIndicator:

    def __init__(self, rect, font):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.visible = False
        self.message = "Working..."
        self.progress = None

        self.angle = 0.0
        self.rotation_speed = 180.0
        self.last_update = pygame.time.get_ticks()

    def show(self, message="Working..."):
        self.message = message
        self.visible = True
        self.angle = 0.0
        self.last_update = pygame.time.get_ticks()

    def set_progress(self, progress):
        self.progress = dict(progress) if progress else None

    def clear_progress(self):
        self.progress = None

    def hide(self):
        self.visible = False
        self.clear_progress()

    def update(self):
        if not self.visible:
            return
        now = pygame.time.get_ticks()
        dt = (now - self.last_update) / 1000.0
        self.last_update = now
        self.angle += self.rotation_speed * dt
        if self.angle >= 360.0:
            self.angle -= 360.0

    def draw(self, surface):
        if not self.visible:
            return

        overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        surface.blit(overlay, self.rect.topleft)

        center_x = self.rect.centerx
        center_y = self.rect.centery

        # Сохраняем прежний вращающийся индикатор.
        spinner_radius = 18
        spinner_length = 10
        for i in range(8):
            angle = self.angle + i * 45
            radians = math.radians(angle)
            x1 = center_x + math.cos(radians) * spinner_radius
            y1 = center_y + math.sin(radians) * spinner_radius
            x2 = center_x + math.cos(radians) * (spinner_radius - spinner_length)
            y2 = center_y + math.sin(radians) * (spinner_radius - spinner_length)
            alpha = int(255 * (1.0 - i / 8))
            line_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            pygame.draw.line(
                line_surface,
                (255, 255, 255, alpha),
                (x2 - self.rect.x, y2 - self.rect.y),
                (x1 - self.rect.x, y1 - self.rect.y),
                4,
            )
            surface.blit(line_surface, self.rect.topleft)

        message = self.font.render(self.message, True, Theme.TW_TEXT_COLOR)
        message_rect = message.get_rect(
            midtop=(center_x, center_y + spinner_radius + 15)
        )
        surface.blit(message, message_rect)

        if self.progress is not None:
            self._draw_progress(surface, center_x, message_rect.bottom + 18)

    def _draw_progress(self, surface, center_x, top):
        progress = self.progress
        item_index = progress.get("item_index", 0)
        items_total = progress.get("items_total", 0)
        si_id = progress.get("si_id")
        phase = progress.get("phase", "")
        completed = progress.get("completed_steps", 0)
        total_steps = progress.get("total_steps", 0)
        percent = max(0, min(100, int(progress.get("percent", 0))))

        panel_width = min(self.rect.width - 48, 460)
        panel_height = 138
        panel = pygame.Rect(
            center_x - panel_width // 2, top, panel_width, panel_height
        )
        pygame.draw.rect(
            surface, pygame.Color("#202B3A"), panel, border_radius=8
        )
        pygame.draw.rect(
            surface, pygame.Color("#6EAEDB"), panel,
            width=1, border_radius=8
        )

        y = panel.top + 10
        for detail in (
            f"Item: {item_index}/{items_total}",
            f"si_id: {si_id if si_id is not None else '-'}",
            f"Phase: {phase}",
        ):
            rendered = self.font.render(detail, True, Theme.TW_TEXT_COLOR)
            surface.blit(rendered, (panel.left + 12, y))
            y += self.font.get_linesize() + 1

        bar = pygame.Rect(
            panel.left + 12, panel.bottom - 24, panel_width - 24, 9
        )
        pygame.draw.rect(
            surface, pygame.Color("#4A5966"), bar, border_radius=5
        )
        fill_width = int(bar.width * percent / 100)
        if fill_width:
            fill = pygame.Rect(bar.left, bar.top, fill_width, bar.height)
            pygame.draw.rect(
                surface, pygame.Color("#3B82F6"), fill, border_radius=5
            )

        label = self.font.render(
            f"{percent}%  ({completed}/{total_steps} steps)",
            True, Theme.TW_TEXT_COLOR
        )
        surface.blit(label, label.get_rect(midbottom=(center_x, bar.top - 3)))
