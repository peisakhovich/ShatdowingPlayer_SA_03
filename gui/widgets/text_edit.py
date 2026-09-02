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
        self._last_cursor_position = self.cursor_position

        # -------------------------
        # Желаемая колонка
        #
        # Используется при движении
        # Up / Down
        # -------------------------
        self.cursor_column = None

        # -------------------------
        # Вертикальная прокрутка
        # -------------------------
        self.scroll_y = 0
        self.scroll_speed = 30

        # -------------------------
        # Выделение текста
        # -------------------------
        self.selection_start = None
        self.selection_end = None

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
        # Mouse wheel
        # --------------------------------------------------

        if event.type == pygame.MOUSEWHEEL:

            mouse_pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(mouse_pos):

                self.scroll_y -= (
                    event.y * self.scroll_speed
                )

                self._limit_scroll()

            return


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

                    #return
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

                self._select_all()
                return

            # Ctrl+C
            if event.key == pygame.K_c and (
                event.mod & pygame.KMOD_CTRL
            ):

                self._copy_selection()
                return

            # Ctrl+X
            if event.key == pygame.K_x and (
                event.mod & pygame.KMOD_CTRL
            ):

                self._cut_selection()
                return

            # Ctrl+V
            if event.key == pygame.K_v and (
                event.mod & pygame.KMOD_CTRL
            ):

                self._paste()
                return



            # -------------------------
            # Navigation / editing
            # -------------------------

            if event.key == pygame.K_LEFT:

                self._clear_selection()
                self._move_left()
                self._start_repeat(event.key)

            elif event.key == pygame.K_RIGHT:

                self._clear_selection()
                self._move_right()
                self._start_repeat(event.key)

            elif event.key == pygame.K_UP:

                self._clear_selection()
                self._move_up()
                self._start_repeat(event.key)

            elif event.key == pygame.K_DOWN:

                self._clear_selection()
                self._move_down()
                self._start_repeat(event.key)

            elif event.key == pygame.K_HOME:

                self._clear_selection()
                self._move_home()
                self._start_repeat(event.key)

            elif event.key == pygame.K_END:

                self._clear_selection()
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

        if self.focused:

            if self.repeat_key is not None:

                keys = pygame.key.get_pressed()

                if not keys[self.repeat_key]:

                    self.repeat_key = None

                else:

                    now = pygame.time.get_ticks()

                    if now - self.repeat_start_time >= self.repeat_delay:

                        if (
                            now - self.repeat_last_time
                            >= self.repeat_interval
                        ):

                            self.repeat_last_time = now

                            self._repeat_action(
                                self.repeat_key
                            )

        if self.cursor_position != self._last_cursor_position:

            self._ensure_cursor_visible()

            self._last_cursor_position = self.cursor_position

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

        if self._delete_selection():
            return

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

        if self._delete_selection():
            return

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
            + Theme.TE_PADDING_Y - self.scroll_y
        )

        line_height = self.font.get_linesize()

        # -------------------------
        # Clip text area
        # -------------------------

        old_clip = screen.get_clip()

        screen.set_clip(
            pygame.Rect(
                self.rect.x + Theme.TE_BORDER_WIDTH,
                self.rect.y + Theme.TE_BORDER_WIDTH,
                self.rect.width - Theme.TE_BORDER_WIDTH * 2,
                self.rect.height - Theme.TE_BORDER_WIDTH * 2
            )
        )


        # -------------------------
        # Selection
        # -------------------------

        self._draw_selection(
            screen,
            visual_lines,
            x,
            line_height
        )

        # -------------------------
        # Visual lines
        # -------------------------        

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

        # -------------------------
        # Restore clip
        # -------------------------

        screen.set_clip(old_clip)

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
            + cursor_line * line_height - self.scroll_y
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
            - Theme.TE_PADDING_Y + self.scroll_y
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

    #---------------
    # Selection
    #---------------
    def _has_selection(self):

        return (
            self.selection_start is not None
            and self.selection_end is not None
            and self.selection_start != self.selection_end
        )

    # --------------------------------------------------

    def _selection_bounds(self):

        if not self._has_selection():
            return None, None

        return (
            min(self.selection_start, self.selection_end),
            max(self.selection_start, self.selection_end)
        )

    # --------------------------------------------------

    def _clear_selection(self):

        self.selection_start = None
        self.selection_end = None

    # --------------------------------------------------

    def _select_all(self):

        self.selection_start = 0
        self.selection_end = len(self.text)

        self.cursor_position = len(self.text)
        self.cursor_column = None

    #---------------
    # Deletation
    #---------------
    def _delete_selection(self):

        start, end = self._selection_bounds()

        if start is None:
            return False

        self.text = (
            self.text[:start]
            + self.text[end:]
        )

        self.cursor_position = start
        self.cursor_column = None

        self._clear_selection()

        return True
    
    #---------------
    # Draw selection
    #---------------
    def _draw_selection(
        self,
        screen,
        visual_lines,
        x,
        line_height
    ):

        start, end = self._selection_bounds()

        if start is None:
            return

        for line_index, line in enumerate(visual_lines):

            line_start = line["start"]
            line_end = line["end"]

            # Нет пересечения с выделением
            if end <= line_start or start >= line_end:
                continue

            selection_start = max(
                start,
                line_start
            )

            selection_end = min(
                end,
                line_end
            )

            start_column = (
                selection_start - line_start
            )

            end_column = (
                selection_end - line_start
            )

            line_text = self.text[
                line_start:line_end
            ]

            before = line_text[
                :start_column
            ]

            selected = line_text[
                start_column:end_column
            ]

            start_x = (
                x
                + self.font.size(before)[0]
            )

            selection_width = self.font.size(
                selected
            )[0]

            y = (
                self.rect.y
                + Theme.TE_PADDING_Y
                + line_index * line_height - self.scroll_y
            )

            pygame.draw.rect(
                screen,
                Theme.TE_SELECTION_COLOR,
                pygame.Rect(
                    start_x,
                    y,
                    max(selection_width, 2),
                    line_height
                )
            )    
    def _copy_selection(self):

        start, end = self._selection_bounds()

        if start is None:
            return

        selected_text = self.text[start:end]

        pygame.scrap.put_text(
            selected_text
        )

    # --------------------------------------------------

    def _cut_selection(self):

        if not self._has_selection():
            return

        self._copy_selection()
        self._delete_selection()

    # --------------------------------------------------

    def _paste(self):

        try:
            text = pygame.scrap.get_text()

        except pygame.error:
            return

       
        if not text:
            return

        # Нормализуем окончания строк
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Если есть выделение,
        # сначала его удаляем.
        self._delete_selection()

        self._insert_text(text)    

    def _limit_scroll(self):

        visual_lines = self._build_visual_lines()

        line_height = self.font.get_linesize()

        content_height = (
            len(visual_lines) * line_height
            + Theme.TE_PADDING_Y * 2
        )

        visible_height = self.rect.height

        max_scroll = max(
            0,
            content_height - visible_height
        )

        self.scroll_y = max(
            0,
            min(
                self.scroll_y,
                max_scroll
            )
        )

    # автоматическое перемещение к курсору
    def _ensure_cursor_visible(self):

        visual_lines = self._build_visual_lines()

        cursor_line = 0

        for index, line in enumerate(visual_lines):

            if (
                line["start"]
                <= self.cursor_position
                <= line["end"]
            ):

                cursor_line = index
                break

        line_height = self.font.get_linesize()

        cursor_top = (
            Theme.TE_PADDING_Y
            + cursor_line * line_height
        )

        cursor_bottom = (
            cursor_top
            + line_height
        )

        visible_top = self.scroll_y

        visible_bottom = (
            self.scroll_y
            + self.rect.height
            - Theme.TE_PADDING_Y * 2
        )

        if cursor_top < visible_top:

            self.scroll_y = cursor_top

        elif cursor_bottom > visible_bottom:

            self.scroll_y = (
                cursor_bottom
                - (
                    self.rect.height
                    - Theme.TE_PADDING_Y * 2
                )
            )

        self._limit_scroll()