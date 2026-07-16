import pygame


class ImageButton:
    def __init__(self, rect, image_normal, image_hover=None, image_pressed=None):
        self.rect = pygame.Rect(rect)

        self.image_normal = image_normal
        self.image_hover = image_hover or image_normal
        self.image_pressed = image_pressed or self.image_hover

        self.image = self.image_normal

        self.is_hovered = False
        self.is_pressed = False
        self._clicked = False

    # -------------------------
    # INPUT
    # -------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._clicked = True
                return True
        return False

    # -------------------------
    # UPDATE STATE
    # -------------------------
    def update(self, mouse_pos, mouse_pressed):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if self.is_hovered and mouse_pressed[0]:
            self.is_pressed = True
        else:
            self.is_pressed = False

        # выбор текстуры
        if self.is_pressed:
            self.image = self.image_pressed
        elif self.is_hovered:
            self.image = self.image_hover
        else:
            self.image = self.image_normal

    # -------------------------
    # RENDER
    # -------------------------
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # -------------------------
    # CLICK FLAG (optional polling)
    # -------------------------
    def was_clicked(self):
        if self._clicked:
            self._clicked = False
            return True
        return False