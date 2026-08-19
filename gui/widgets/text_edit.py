import pygame

from gui.theme import Theme


class TextEdit:

    def __init__(
        self,
        rect,
        font,
        text=""
    ):

        # -------------------------
        # Параметры
        # -------------------------
        self.font = font
        self.rect = pygame.Rect(rect)

        # -------------------------
        # Текст
        # -------------------------
        self.text = text

        # -------------------------
        # Фокус клавиатуры
        # -------------------------
        self.focused = False

        # -------------------------
        # Позиция курсора
        # -------------------------
        self.cursor_position = len(self.text)

        # -------------------------
        # Желаемая колонка
        #
        # Используется при движении
        # Up / Down
        # -------------------------
        self.cursor_column = None

        # -------------------------
        # Состояние мыши
        # -------------------------
        self.mouse_over = False

        # -------------------------
        # Удержание клавиши
        # -------------------------
        self.repeat_key = None
        self.repeat_start_time = 0
        self.repeat_last_time = 0

        self.repeat_delay = 400
        self.repeat_interval = 40

        # -------------------------
        # Многострочный текст
        # -------------------------
        self.lines = []

    # ==================================================
    # TEXT
    # ==================================================

    def set_text(self, text):

        self.text = text
        self.cursor_position = len(text)
        self.cursor_column = None

    # --------------------------------------------------

    def get_text(self):

        return self.text

    # --------------------------------------------------

    def clear(self):

        self.text = ""
        self.cursor_position = 0
        self.cursor_column = None

    # ==================================================
    # EVENT
    # ==================================================

    def handle_event(self, event):

        # --------------------------------------------------
        # Mouse
        # --------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.rect.collidepoint(event.pos):

                    self.focused = True

                    self._set_cursor_from_mouse(
                        event.pos
                    )

                    pygame.key.start_text_input()

                else:

                    self.focused = False
                    self.repeat_key = None

                    pygame.key.stop_text_input()

        # --------------------------------------------------
        # Text input
        # --------------------------------------------------

        elif event.type == pygame.TEXTINPUT:

            if self.focused:

                self.text = (
                    self.text[:self.cursor_position]
                    + event.text
                    + self.text[self.cursor_position:]
                )

                self.cursor_position += len(event.text)
                self.cursor_column = None

        # --------------------------------------------------
        # Key down
        # --------------------------------------------------

        elif event.type == pygame.KEYDOWN:

            if not self.focused:
                return

            # Ctrl+A
            if event.key == pygame.K_a and (
                event.mod & pygame.KMOD_CTRL
            ):

                self.cursor_position = len(self.text)
                self.cursor_column = None
                return

            # -------------------------
            # Navigation / editing
            # -------------------------

            if event.key == pygame.K_LEFT:

                self._move_left()
                self._start_repeat(event.key)

            elif event.key == pygame.K_RIGHT:

                self._move_right()
                self._start_repeat(event.key)

            elif event.key == pygame.K_UP:

                self._move_up()
                self._start_repeat(event.key)

            elif event.key == pygame.K_DOWN:

                self._move_down()
                self._start_repeat(event.key)

            elif event.key == pygame.K_HOME:

                self._move_home()
                self._start_repeat(event.key)

            elif event.key == pygame.K_END:

                self._move_end()
                self._start_repeat(event.key)

            elif event.key == pygame.K_BACKSPACE:

                self._backspace()
                self._start_repeat(event.key)

            elif event.key == pygame.K_DELETE:

                self._delete()
                self._start_repeat(event.key)

            elif event.key == pygame.K_RETURN:

                self._insert_text("\n")

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        self.mouse_over = self.rect.collidepoint(
            pygame.mouse.get_pos()
        )

        if not self.focused:
            return

        if self.repeat_key is None:
            return

        keys = pygame.key.get_pressed()

        if not keys[self.repeat_key]:
            self.repeat_key = None
            return

        now = pygame.time.get_ticks()

        # Ждём задержку перед началом повтора
        if now - self.repeat_start_time < self.repeat_delay:
            return

        # Проверяем интервал между повторениями
        if now - self.repeat_last_time >= self.repeat_interval:

            self.repeat_last_time = now

            self._repeat_action(
                self.repeat_key
            )

    # ==================================================
    # REPEAT
    # ==================================================

    def _start_repeat(self, key):

        self.repeat_key = key

        now = pygame.time.get_ticks()

        self.repeat_start_time = now
        self.repeat_last_time = now

    # --------------------------------------------------

    def _repeat_action(self, key):

        if key == pygame.K_LEFT:
            self._move_left()

        elif key == pygame.K_RIGHT:
            self._move_right()

        elif key == pygame.K_UP:
            self._move_up()

        elif key == pygame.K_DOWN:
            self._move_down()

        elif key == pygame.K_HOME:
            self._move_home()

        elif key == pygame.K_END:
            self._move_end()

        elif key == pygame.K_BACKSPACE:
            self._backspace()

        elif key == pygame.K_DELETE:
            self._delete()

    # ==================================================
    # TEXT EDITING
    # ==================================================

    def _insert_text(self, text):

        self.text = (
            self.text[:self.cursor_position]
            + text
            + self.text[self.cursor_position:]
        )

        self.cursor_position += len(text)
        self.cursor_column = None

    # --------------------------------------------------

    def _backspace(self):

        if self.cursor_position <= 0:
            return

        self.text = (
            self.text[:self.cursor_position - 1]
            + self.text[self.cursor_position:]
        )

        self.cursor_position -= 1
        self.cursor_column = None

    # --------------------------------------------------

    def _delete(self):

        if self.cursor_position >= len(self.text):
            return

        self.text = (
            self.text[:self.cursor_position]
            + self.text[self.cursor_position + 1:]
        )

        self.cursor_column = None

    # ==================================================
    # NAVIGATION
    # ==================================================

    def _move_left(self):

        if self.cursor_position > 0:
            self.cursor_position -= 1

        self.cursor_column = None

    # --------------------------------------------------

    def _move_right(self):

        if self.cursor_position < len(self.text):
            self.cursor_position += 1

        self.cursor_column = None

    # --------------------------------------------------

    def _move_home(self):

        line_start, _ = self._get_line_bounds(
            self.cursor_position
        )

        self.cursor_position = line_start

        self.cursor_column = 0

    # --------------------------------------------------

    def _move_end(self):

        _, line_end = self._get_line_bounds(
            self.cursor_position
        )

        self.cursor_position = line_end

        self.cursor_column = (
            line_end
            - self._get_line_bounds(self.cursor_position)[0]
        )

    # --------------------------------------------------

    def _move_up(self):

        self._move_vertical(-1)

    # --------------------------------------------------

    def _move_down(self):

        self._move_vertical(1)

    # --------------------------------------------------

    def _move_vertical(self, direction):

        visual_lines = self._build_visual_lines()

        current_line = None
        current_column = None

        for index, line in enumerate(visual_lines):

            if (
                line["start"]
                <= self.cursor_position
                <= line["end"]
            ):

                current_line = index
                current_column = (
                    self.cursor_position
                    - line["start"]
                )

                break

        if current_line is None:
            return

        # Первая вертикальная команда
        # запоминает исходную колонку.
        if self.cursor_column is None:

            self.cursor_column = current_column

        target_line = current_line + direction

        if target_line < 0:
            target_line = 0

        if target_line >= len(visual_lines):
            target_line = len(visual_lines) - 1

        target = visual_lines[target_line]

        column = min(
            self.cursor_column,
            target["end"] - target["start"]
        )

        self.cursor_position = (
            target["start"] + column
        )

    # ==================================================
    # LINE INFORMATION
    # ==================================================

    def _get_line_bounds(self, position):

        start = self.text.rfind(
            "\n",
            0,
            position
        )

        if start == -1:
            start = 0
        else:
            start += 1

        end = self.text.find(
            "\n",
            position
        )

        if end == -1:
            end = len(self.text)

        return start, end

    # ==================================================
    # WORD WRAP
    # ==================================================

    def _build_visual_lines(self):

        result = []

        padding = (
            Theme.TE_PADDING_X * 2
        )

        max_width = (
            self.rect.width - padding
        )

        paragraphs = self.text.split("\n")

        global_position = 0

        for paragraph in paragraphs:

            # Пустая строка
            if paragraph == "":

                result.append({
                    "start": global_position,
                    "end": global_position
                })

                global_position += 1
                continue

            start = 0

            while start < len(paragraph):

                remaining = paragraph[start:]

                width = self.font.size(
                    remaining
                )[0]

                if width <= max_width:

                    end = len(paragraph)

                else:

                    end = start + 1

                    while end <= len(paragraph):

                        candidate = paragraph[
                            start:end
                        ]

                        if self.font.size(
                            candidate
                        )[0] > max_width:
                            break

                        end += 1

                    end -= 1

                    # Пытаемся переносить по пробелу
                    space = paragraph.rfind(
                        " ",
                        start,
                        end
                    )

                    if space > start:
                        end = space

                result.append({
                    "start": global_position + start,
                    "end": global_position + end
                })

                start = end

                # Пропускаем пробел,
                # по которому сделали перенос.
                if (
                    start < len(paragraph)
                    and paragraph[start] == " "
                ):
                    start += 1

            global_position += len(paragraph) + 1

        if not result:

            result.append({
                "start": 0,
                "end": 0
            })

        return result

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        # -------------------------
        # Background
        # -------------------------

        pygame.draw.rect(
            screen,
            Theme.TE_BACKGROUND_COLOR,
            self.rect,
            border_radius=Theme.TE_RADIUS
        )

        # -------------------------
        # Border
        # -------------------------

        pygame.draw.rect(
            screen,
            Theme.TE_BORDER_COLOR,
            self.rect,
            width=Theme.TE_BORDER_WIDTH,
            border_radius=Theme.TE_RADIUS
        )

        # -------------------------
        # Focus border
        # -------------------------

        if self.focused:

            pygame.draw.rect(
                screen,
                Theme.TE_FOCUS_BORDER_COLOR,
                self.rect,
                width=Theme.TE_FOCUS_BORDER_WIDTH,
                border_radius=Theme.TE_RADIUS
            )

        # -------------------------
        # Visual lines
        # -------------------------

        visual_lines = self._build_visual_lines()

        x = (
            self.rect.x
            + Theme.TE_PADDING_X
        )

        y = (
            self.rect.y
            + Theme.TE_PADDING_Y
        )

        line_height = self.font.get_linesize()

        for line in visual_lines:

            line_text = self.text[
                line["start"]:line["end"]
            ]

            text_surface = self.font.render(
                line_text,
                True,
                Theme.TE_TEXT_COLOR
            )

            screen.blit(
                text_surface,
                (x, y)
            )

            y += line_height

        # -------------------------
        # Cursor
        # -------------------------

        if self.focused:

            self._draw_cursor(
                screen,
                visual_lines,
                x,
                y,
                line_height
            )

    # ==================================================
    # CURSOR
    # ==================================================

    def _draw_cursor(
        self,
        screen,
        visual_lines,
        x,
        y,
        line_height
    ):

        cursor_line = 0
        cursor_column = 0

        for index, line in enumerate(visual_lines):

            if (
                line["start"]
                <= self.cursor_position
                <= line["end"]
            ):

                cursor_line = index

                cursor_column = (
                    self.cursor_position
                    - line["start"]
                )

                break

        line_text = self.text[
            visual_lines[cursor_line]["start"]
            :
            visual_lines[cursor_line]["start"]
            + cursor_column
        ]

        cursor_x = (
            x
            + self.font.size(line_text)[0]
        )

        cursor_y = (
            self.rect.y
            + Theme.TE_PADDING_Y
            + cursor_line * line_height
        )

        pygame.draw.line(
            screen,
            Theme.TE_CURSOR_COLOR,
            (cursor_x, cursor_y),
            (cursor_x, cursor_y + line_height),
            2
        )

    def _set_cursor_from_mouse(self, mouse_pos):

        visual_lines = self._build_visual_lines()

        x = (
            mouse_pos[0]
            - self.rect.x
            - Theme.TE_PADDING_X
        )

        y = (
            mouse_pos[1]
            - self.rect.y
            - Theme.TE_PADDING_Y
        )

        line_height = self.font.get_linesize()

        # -------------------------
        # Определяем визуальную строку
        # -------------------------

        line_index = int(
            y // line_height
        )

        if line_index < 0:
            line_index = 0

        if line_index >= len(visual_lines):
            line_index = len(visual_lines) - 1

        line = visual_lines[line_index]

        line_text = self.text[
            line["start"]:line["end"]
        ]

        # -------------------------
        # Курсор левее текста
        # -------------------------

        if x <= 0:

            self.cursor_position = line["start"]
            self.cursor_column = 0

            return

        # -------------------------
        # Ищем ближайшую позицию
        # -------------------------

        best_position = 0
        best_distance = float("inf")

        for i in range(len(line_text) + 1):

            candidate = line_text[:i]

            candidate_width = self.font.size(
                candidate
            )[0]

            distance = abs(
                x - candidate_width
            )

            if distance < best_distance:

                best_distance = distance
                best_position = i

        self.cursor_position = (
            line["start"] + best_position
        )

        self.cursor_column = best_position