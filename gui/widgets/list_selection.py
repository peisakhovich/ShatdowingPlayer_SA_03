import pygame


class ListSelection:

    def __init__(self, rect, options, selected=0):

        self.rect = pygame.Rect(rect)

        self.options = options
        self.selected = selected

        self.opened = False

        self.item_height = self.rect.height

    # --------------------------------------------------
    # properties
    # --------------------------------------------------

    @property
    def value(self):
        return self.options[self.selected][0]

    @property
    def caption(self):
        return self.options[self.selected][1]

    # --------------------------------------------------
    # event
    # --------------------------------------------------

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        # ----------------------------------------------
        # список закрыт
        # ----------------------------------------------

        if not self.opened:

            if self.rect.collidepoint(event.pos):
                self.opened = True

            return None

        # ----------------------------------------------
        # список открыт
        # ----------------------------------------------

        # область выпадающего списка
        dropdown_rect = pygame.Rect(
            self.rect.x,
            self.rect.bottom,
            self.rect.width,
            len(self.options) * self.item_height
        )

        # выбор элемента
        if dropdown_rect.collidepoint(event.pos):

            index = (
                event.pos[1] - dropdown_rect.top
            ) // self.item_height

            if 0 <= index < len(self.options):

                self.selected = index
                self.opened = False

                return (
                    "selection",
                    self.value
                )

        # ----------------------------------------------
        # клик вне списка
        # ----------------------------------------------

        self.opened = False

        return None

    # --------------------------------------------------
    # draw
    # --------------------------------------------------

    def draw(self, screen, font):

        # ----------------------------------------------
        # выбранный элемент
        # ----------------------------------------------

        pygame.draw.rect(
            screen,
            pygame.Color("#364049"),
            self.rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            pygame.Color("#1085A8"),
            self.rect,
            width=1,
            border_radius=6
        )

        text = font.render(
            self.caption,
            True,
            pygame.Color("#91E5FF")
        )

        screen.blit(
            text,
            (
                self.rect.x + 10,
                self.rect.centery - text.get_height() // 2
            )
        )

        # ----------------------------------------------
        # стрелка
        # ----------------------------------------------

        center_x = self.rect.right - 15
        center_y = self.rect.centery

        if self.opened:

            points = [
                (center_x - 5, center_y + 2),
                (center_x,     center_y - 3),
                (center_x + 5, center_y + 2),
            ]

        else:

            points = [
                (center_x - 5, center_y - 2),
                (center_x,     center_y + 3),
                (center_x + 5, center_y - 2),
            ]

        pygame.draw.polygon(
            screen,
            pygame.Color("#91E5FF"),
            points
        )

        # ----------------------------------------------
        # dropdown
        # ----------------------------------------------

        if not self.opened:
            return

        for index, (_, caption) in enumerate(self.options):

            item_rect = pygame.Rect(
                self.rect.x,
                self.rect.bottom + index * self.item_height,
                self.rect.width,
                self.item_height
            )

            pygame.draw.rect(
                screen,
                pygame.Color("#364049"),
                item_rect
            )

            text = font.render(
                caption,
                True,
                pygame.Color("#91E5FF")
            )

            screen.blit(
                text,
                (
                    item_rect.x + 10,
                    item_rect.centery - text.get_height() // 2
                )
            )