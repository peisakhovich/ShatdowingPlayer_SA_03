from __future__ import annotations

import pygame


class ListSelection:

    def __init__(
        self,
        rect,
        options,
        selected=0,
        max_visible_items=8,
    ):

        self.rect = pygame.Rect(rect)

        self.options = options

        self.selected = (
            selected
            if 0 <= selected < len(options)
            else 0
        )

        self.opened = False

        self.item_height = self.rect.height

        # Максимальное количество элементов,
        # одновременно видимых в dropdown.
        self.max_visible_items = max(
            1,
            max_visible_items
        )

        # Первый отображаемый элемент списка.
        self.scroll_index = 0

    # ==================================================
    # PROPERTIES
    # ==================================================

    @property
    def value(self):

        if not self.options:
            return ""

        if not 0 <= self.selected < len(self.options):
            self.selected = 0

        return self.options[self.selected][0]

    @property
    def caption(self):

        if not self.options:
            return ""

        if not 0 <= self.selected < len(self.options):
            self.selected = 0

        return self.options[self.selected][1]

    # ==================================================
    # INTERNAL
    # ==================================================

    def _visible_count(self):

        return min(
            len(self.options),
            self.max_visible_items
        )

    # --------------------------------------------------

    def _dropdown_height(self):

        return (
            self._visible_count()
            * self.item_height
        )

    # --------------------------------------------------

    def _get_dropdown_rect(self):

        return pygame.Rect(
            self.rect.x,
            self.rect.bottom,
            self.rect.width,
            self._dropdown_height()
        )

    # --------------------------------------------------

    def _ensure_selected_visible(self):

        visible_count = self._visible_count()

        if visible_count <= 0:
            self.scroll_index = 0
            return

        # Если выбранный элемент выше видимой области.
        if self.selected < self.scroll_index:

            self.scroll_index = self.selected

        # Если выбранный элемент ниже видимой области.
        elif (
            self.selected
            >= self.scroll_index + visible_count
        ):

            self.scroll_index = (
                self.selected
                - visible_count
                + 1
            )

        # Ограничиваем scroll_index.
        max_scroll = max(
            0,
            len(self.options) - visible_count
        )

        self.scroll_index = max(
            0,
            min(
                self.scroll_index,
                max_scroll
            )
        )

    # ==================================================
    # EVENT
    # ==================================================

    def handle_event(self, event):

        # --------------------------------------------------
        # Mouse wheel
        # --------------------------------------------------

        if (
            event.type == pygame.MOUSEWHEEL
            and self.opened
        ):

            mouse_pos = pygame.mouse.get_pos()

            dropdown_rect = self._get_dropdown_rect()

            # Колесо работает только над dropdown.
            if dropdown_rect.collidepoint(mouse_pos):

                max_scroll = max(
                    0,
                    len(self.options)
                    - self._visible_count()
                )

                # pygame:
                # y > 0 = wheel up
                # y < 0 = wheel down

                self.scroll_index -= event.y

                self.scroll_index = max(
                    0,
                    min(
                        self.scroll_index,
                        max_scroll
                    )
                )

                return None

            return None

        # --------------------------------------------------
        # Только mouse button
        # --------------------------------------------------

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        # ==================================================
        # LIST CLOSED
        # ==================================================

        if not self.opened:

            if self.rect.collidepoint(event.pos):

                self.opened = True

                # При открытии стараемся показать
                # выбранный элемент.
                self._ensure_selected_visible()

            return None

        # ==================================================
        # LIST OPENED
        # ==================================================

        dropdown_rect = self._get_dropdown_rect()

        # --------------------------------------------------
        # Выбор элемента
        # --------------------------------------------------

        if dropdown_rect.collidepoint(event.pos):

            relative_y = (
                event.pos[1]
                - dropdown_rect.top
            )

            visible_index = (
                relative_y
                // self.item_height
            )

            index = (
                self.scroll_index
                + visible_index
            )

            if (
                0 <= index
                < len(self.options)
            ):

                self.selected = index
                self.opened = False

                return (
                    "selection",
                    self.value
                )

            return None

        # --------------------------------------------------
        # Клик по самому control
        #
        # При открытом списке клик по верхнему
        # control закрывает список.
        # --------------------------------------------------

        if self.rect.collidepoint(event.pos):

            self.opened = False

            return None

        # --------------------------------------------------
        # Клик вне списка
        # --------------------------------------------------

        self.opened = False

        return None

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen, font):

        # ==================================================
        # SELECTED ITEM
        # ==================================================

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
                self.rect.centery
                - text.get_height() // 2
            )
        )

        # ==================================================
        # ARROW
        # ==================================================

        center_x = self.rect.right - 15
        center_y = self.rect.centery

        if self.opened:

            points = [
                (
                    center_x - 5,
                    center_y + 2
                ),
                (
                    center_x,
                    center_y - 3
                ),
                (
                    center_x + 5,
                    center_y + 2
                ),
            ]

        else:

            points = [
                (
                    center_x - 5,
                    center_y - 2
                ),
                (
                    center_x,
                    center_y + 3
                ),
                (
                    center_x + 5,
                    center_y - 2
                ),
            ]

        pygame.draw.polygon(
            screen,
            pygame.Color("#91E5FF"),
            points
        )

        # ==================================================
        # DROPDOWN
        # ==================================================

        if not self.opened:
            return

        visible_count = self._visible_count()

        if visible_count <= 0:
            return

        dropdown_rect = self._get_dropdown_rect()

        # --------------------------------------------------
        # Dropdown background
        # --------------------------------------------------

        pygame.draw.rect(
            screen,
            pygame.Color("#364049"),
            dropdown_rect
        )

        # --------------------------------------------------
        # Items
        # --------------------------------------------------

        for visible_index in range(
            visible_count
        ):

            index = (
                self.scroll_index
                + visible_index
            )

            if index >= len(self.options):
                break

            item_rect = pygame.Rect(
                dropdown_rect.x,
                dropdown_rect.y
                + visible_index * self.item_height,
                dropdown_rect.width,
                self.item_height
            )

            # Selected item
            if index == self.selected:

                pygame.draw.rect(
                    screen,
                    pygame.Color("#1085A8"),
                    item_rect
                )

            else:

                pygame.draw.rect(
                    screen,
                    pygame.Color("#364049"),
                    item_rect
                )

            _, caption = self.options[index]

            text = font.render(
                caption,
                True,
                pygame.Color("#91E5FF")
            )

            screen.blit(
                text,
                (
                    item_rect.x + 10,
                    item_rect.centery
                    - text.get_height() // 2
                )
            )

        # ==================================================
        # BORDER
        # ==================================================

        pygame.draw.rect(
            screen,
            pygame.Color("#1085A8"),
            dropdown_rect,
            width=1
        )

        # ==================================================
        # SCROLL INDICATORS
        # ==================================================

        max_scroll = max(
            0,
            len(self.options)
            - visible_count
        )

        if max_scroll <= 0:
            return

        # --------------------------------------------------
        # Up indicator
        # --------------------------------------------------

        if self.scroll_index > 0:

            center_x = (
                dropdown_rect.right - 12
            )

            center_y = (
                dropdown_rect.top + 8
            )

            points = [
                (
                    center_x - 4,
                    center_y + 2
                ),
                (
                    center_x,
                    center_y - 3
                ),
                (
                    center_x + 4,
                    center_y + 2
                ),
            ]

            pygame.draw.polygon(
                screen,
                pygame.Color("#91E5FF"),
                points
            )

        # --------------------------------------------------
        # Down indicator
        # --------------------------------------------------

        if self.scroll_index < max_scroll:

            center_x = (
                dropdown_rect.right - 12
            )

            center_y = (
                dropdown_rect.bottom - 8
            )

            points = [
                (
                    center_x - 4,
                    center_y - 2
                ),
                (
                    center_x,
                    center_y + 3
                ),
                (
                    center_x + 4,
                    center_y - 2
                ),
            ]

            pygame.draw.polygon(
                screen,
                pygame.Color("#91E5FF"),
                points
            )