"""
Sound Language Studio
---------------------

Module:
    gui.login_register_window

Purpose:
    Provides the Login, Register and Change Password window
    for user authentication and account management.

ru:
    Предоставляет окно Login, Register и Change Password
    для авторизации пользователя, создания учётной записи
    и изменения пароля.
"""
import pygame

from gui.theme import Theme
from gui.widgets.text_edit import TextEdit
from gui.widgets.status_message import StatusMessage

class LoginRegisterWindow:
    """Общее окно Login / Register / Change Password."""

    def __init__(
        self,
        rect,
        font_manager,
        session,
        api_client,
        mode="login"
    ):
        # ==================================================
        # Основные данные
        # ==================================================

        self.rect = pygame.Rect(rect)

        self.font_manager = font_manager
        self.session = session
        self.api_client = api_client

        self.visible = False

        if mode not in (
            "login",
            "register",
            "change_password"
        ):
            raise ValueError(
                "Invalid LoginRegisterWindow mode"
            )

        self.mode = mode

        # ==================================================
        # Result
        # ==================================================

        self.result = None

        # ==================================================
        # Message
        # ==================================================

        self.message = ""
        self.message_type = StatusMessage.INFO

        # ==================================================
        # Fonts
        # ==================================================

        self.title_font = self.font_manager.load(
            28
        )

        self.caption_font = self.font_manager.load(
            20
        )

        self.message_font = self.font_manager.load(
            18
        )

        self.edit_font = self.font_manager.load(
            20
        )

        # ==================================================
        # Close button
        # ==================================================

        self.close_rect = pygame.Rect(
            self.rect.right - 35,
            self.rect.top + 10,
            25,
            25
        )

        # ==================================================
        # TextEdit
        # ==================================================

        self.nickname_edit = None
        self.password_edit = None
        self.repeat_password_edit = None
        self.first_name_edit = None
        self.last_name_edit = None

        # ==================================================
        # Buttons
        # ==================================================

        self.action_rect = pygame.Rect(
            0,
            0,
            140,
            36
        )

        self.switch_rect = pygame.Rect(
            0,
            0,
            240,
            30
        )

        # ==================================================
        # Build
        # ==================================================

        self._build()

    # ==================================================
    # MODE
    # ==================================================

    def set_mode(self, mode):

        if mode not in (
            "login",
            "register",
            "change_password"
        ):
            raise ValueError(
                "Invalid LoginRegisterWindow mode"
            )

        self.mode = mode
        self.message = ""
        self.result = None
        self.message_type = StatusMessage.INFO

        self._clear_focus()
        self._build()

    # ==================================================
    # BUILD
    # ==================================================

    def _build(self):

        left = self.rect.x + 30
        width = self.rect.width - 60

        y = self.rect.y + 85

        edit_height = 36
        gap = 70

        # ==================================================
        # Clear fields from previous mode
        # ==================================================

        self.nickname_rect = None
        self.nickname_edit = None

        self.password_rect = None
        self.password_edit = None

        self.repeat_password_rect = None
        self.repeat_password_edit = None

        self.first_name_rect = None
        self.first_name_edit = None

        self.last_name_rect = None
        self.last_name_edit = None

        # ==================================================
        # CHANGE PASSWORD
        # ==================================================

        if self.mode == "change_password":

            # --------------------------------------------------
            # Current password
            # --------------------------------------------------

            self.password_rect = pygame.Rect(
                left,
                y,
                width,
                edit_height
            )

            self.password_edit = TextEdit(
                self.password_rect,
                self.edit_font,
                password=True


            )

            y += gap

            # --------------------------------------------------
            # New password
            # --------------------------------------------------

            self.repeat_password_rect = pygame.Rect(
                left,
                y,
                width,
                edit_height
            )

            self.repeat_password_edit = TextEdit(
                self.repeat_password_rect,
                self.edit_font,
                password=True

            )

            y += gap

            # --------------------------------------------------
            # Repeat new password
            # --------------------------------------------------

            self.first_name_rect = pygame.Rect(
                left,
                y,
                width,
                edit_height
            )

            self.first_name_edit = TextEdit(
                self.first_name_rect,
                self.edit_font,
                password=True
            )

            y += 55

        else:

            # ==================================================
            # Nickname
            # ==================================================

            self.nickname_rect = pygame.Rect(
                left,
                y,
                width,
                edit_height
            )

            self.nickname_edit = TextEdit(
                self.nickname_rect,
                self.edit_font
            )

            y += gap

            # ==================================================
            # Password
            # ==================================================

            self.password_rect = pygame.Rect(
                left,
                y,
                width,
                edit_height
            )

            self.password_edit = TextEdit(
                self.password_rect,
                self.edit_font,
                password=True
            )

            y += gap

            # ==================================================
            # REGISTER FIELDS
            # ==================================================

            if self.mode == "register":

                # --------------------------------------------------
                # Repeat password
                # --------------------------------------------------

                self.repeat_password_rect = pygame.Rect(
                    left,
                    y,
                    width,
                    edit_height
                )

                self.repeat_password_edit = TextEdit(
                    self.repeat_password_rect,
                    self.edit_font,
                    password=True
                )

                y += gap

                # --------------------------------------------------
                # First name
                # --------------------------------------------------

                self.first_name_rect = pygame.Rect(
                    left,
                    y,
                    width,
                    edit_height
                )

                self.first_name_edit = TextEdit(
                    self.first_name_rect,
                    self.edit_font
                )

                y += gap

                # --------------------------------------------------
                # Last name
                # --------------------------------------------------

                self.last_name_rect = pygame.Rect(
                    left,
                    y,
                    width,
                    edit_height
                )

                self.last_name_edit = TextEdit(
                    self.last_name_rect,
                    self.edit_font
                )

                y += 55

            else:

                # Login
                y += 15

        # ==================================================
        # Action button
        # ==================================================

        self.action_rect = pygame.Rect(
            self.rect.centerx - 120,
            y,
            240,
            36
        )

        # ==================================================
        # Switch button
        # ==================================================

        self.switch_rect = pygame.Rect(
            self.rect.centerx - 120,
            y + 50,
            240,
            30
        )

    # ==================================================
    # VISIBILITY
    # ==================================================

    def show(self, mode=None):

        if mode is not None:
            self.set_mode(mode)

        self.visible = True

        self.message = ""
        self.message_type = StatusMessage.INFO
        self.result = None

        pygame.key.stop_text_input()

    # --------------------------------------------------

    def hide(self):

        self.visible = False

        self.result = None

        self._clear_focus()

    # ==================================================
    # FOCUS
    # ==================================================

    def _clear_focus(self):

        edits = [
            self.nickname_edit,
            self.password_edit,
            self.repeat_password_edit,
            self.first_name_edit,
            self.last_name_edit
        ]

        for edit in edits:

            if edit is not None:
                edit.focused = False

        pygame.key.stop_text_input()

    # ==================================================
    # GET EDITS
    # ==================================================

    def _get_edits(self):

        return [
            self.nickname_edit,
            self.password_edit,
            self.repeat_password_edit,
            self.first_name_edit,
            self.last_name_edit
        ]

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.visible:
            return

        for edit in self._get_edits():

            if edit is not None:
                edit.update()

    # ==================================================
    # EVENTS
    # ==================================================

    def handle_event(self, event):

        if not self.visible:
            return

        # --------------------------------------------------
        # Mouse button
        # --------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:
                return

            # --------------------------------------------------
            # Close
            # --------------------------------------------------

            if self.close_rect.collidepoint(event.pos):

                self.hide()
                return

            # --------------------------------------------------
            # Action button
            # --------------------------------------------------

            if self.action_rect.collidepoint(event.pos):

                if self.mode == "login":

                    self._login()

                elif self.mode == "register":

                    self._register()

                else:

                    self._change_password()

                return

            # --------------------------------------------------
            # Switch
            # --------------------------------------------------

            if self.switch_rect.collidepoint(event.pos):

                if self.mode == "login":

                    self.set_mode("register")

                elif self.mode == "register":

                    self.set_mode("login")

                else:

                    self.set_mode("login")

                return

            # --------------------------------------------------
            # TextEdit
            #
            # Передаём клик только тому полю,
            # в которое действительно попала мышь.
            # --------------------------------------------------

            edits = [
                self.nickname_edit,
                self.password_edit,
                self.repeat_password_edit,
                self.first_name_edit,
                self.last_name_edit
            ]

            for edit in edits:

                if edit is not None:

                    if edit.rect.collidepoint(event.pos):

                        # Сначала снимаем фокус со всех полей
                        self._clear_focus()

                        # Затем передаем клик выбранному полю
                        edit.handle_event(event)

                        return

            # --------------------------------------------------
            # Клик вне полей
            #
            # Снимаем фокус со всех TextEdit.
            # --------------------------------------------------

            self._clear_focus()
            return

        # --------------------------------------------------
        # Tab — переход между полями
        # --------------------------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_TAB:

                self._focus_next_edit(
                    backward=bool(
                        event.mod & pygame.KMOD_SHIFT
                    )
                )

                return

        # --------------------------------------------------
        # Keyboard / text input / mouse wheel
        #
        # Передаём всем TextEdit.
        # Только сфокусированный TextEdit
        # реально обработает клавиатуру.
        # --------------------------------------------------

        edits = [
            self.nickname_edit,
            self.password_edit,
            self.repeat_password_edit,
            self.first_name_edit,
            self.last_name_edit
        ]

        for edit in edits:

            if edit is not None:
                edit.handle_event(event)

    # ==================================================
    # LOGIN
    # ==================================================

    def _login(self):

        nickname = (
            self.nickname_edit
            .get_text()
            .strip()
        )

        password = (
            self.password_edit
            .get_text()
        )

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        if not nickname:

            self.message = "Enter nickname"
            self.message_type = StatusMessage.WARNING
            return

        if not password:

            self.message = "Enter password"
            self.message_type = StatusMessage.WARNING
            return

        # --------------------------------------------------
        # API
        # --------------------------------------------------

        try:

            user = self.api_client.login(
                nickname=nickname,
                password=password
            )

        except Exception as e:

            self.message = str(e)
            self.message_type = StatusMessage.ERROR
            return

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        self.session.set_user(
            user["user_id"],
            user["nickname"]
        )

        self.result = {
            "action": "login",
            "user": user
        }

        self.message = "Login successful"
        self.message_type = StatusMessage.SUCCESS

        self._clear_focus()

    # ==================================================
    # REGISTER
    # ==================================================

    def _register(self):

        nickname = (
            self.nickname_edit
            .get_text()
            .strip()
        )

        password = (
            self.password_edit
            .get_text()
        )

        repeat_password = (
            self.repeat_password_edit
            .get_text()
        )

        first_name = (
            self.first_name_edit
            .get_text()
            .strip()
        )

        last_name = (
            self.last_name_edit
            .get_text()
            .strip()
        )

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        if not nickname:

            self.message = "Enter nickname"
            self.message_type = StatusMessage.WARNING
            return

        if not password:

            self.message = "Enter password"
            self.message_type = StatusMessage.WARNING
            return

        if password != repeat_password:

            self.message = "Passwords do not match"
            self.message_type = StatusMessage.WARNING
            return

        # --------------------------------------------------
        # API
        # --------------------------------------------------

        try:

            user = self.api_client.register(
                nickname=nickname,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

        except Exception as e:

            self.message = str(e)
            self.message_type = StatusMessage.ERROR
            return

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        self.session.set_user(
            user["user_id"],
            user["nickname"]
        )

        self.result = {
            "action": "register",
            "user": user
        }

        self.message = "Registration successful"
        self.message_type = StatusMessage.SUCCESS

        self._clear_focus()

    # ==================================================
    # CHANGE PASSWORD
    # ==================================================

    def _change_password(self):

        current_password = (
            self.password_edit
            .get_text()
        )

        new_password = (
            self.repeat_password_edit
            .get_text()
        )

        repeat_password = (
            self.first_name_edit
            .get_text()
        )

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        if not current_password:

            self.message = "Enter current password"
            self.message_type = StatusMessage.WARNING
            return

        if not new_password:

            self.message = "Enter new password"
            self.message_type = StatusMessage.WARNING
            return

        if not repeat_password:

            self.message = "Repeat new password"
            self.message_type = StatusMessage.WARNING
            return

        if new_password != repeat_password:

            self.message = "Passwords do not match"
            self.message_type = StatusMessage.WARNING
            return

        # --------------------------------------------------
        # Current user
        # --------------------------------------------------

        user_id = self.session.user_id

        if not user_id:

            self.message = "User is not logged in"
            self.message_type = StatusMessage.WARNING
            return

        # --------------------------------------------------
        # API
        # --------------------------------------------------

        try:

            result = self.api_client.change_password(
                user_id=user_id,
                current_password=current_password,
                new_password=new_password
            )

        except Exception as e:

            self.message = str(e)
            self.message_type = StatusMessage.ERROR
            return

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        self.result = {
            "action": "change_password",
            "result": result
        }

        self.message = "Password changed successfully"
        self.message_type = StatusMessage.SUCCESS

        self._clear_focus()

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        if not self.visible:
            return

        # ==================================================
        # Background
        # ==================================================

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BACKGROUND_COLOR,
            self.rect,
            border_radius=Theme.DIALOG_RADIUS
        )

        # ==================================================
        # Border
        # ==================================================

        pygame.draw.rect(
            screen,
            Theme.TB_FOCUS_BORDER_COLOR,
            self.rect,
            width=Theme.TB_BORDER_WIDTH,
            border_radius=Theme.DIALOG_RADIUS
        )

        # ==================================================
        # Title
        # ==================================================

        if self.mode == "login":

            title_text = "Login"

        elif self.mode == "register":

            title_text = "Register"

        else:

            title_text = "Change password"

        title = self.title_font.render(
            title_text,
            True,
            Theme.DIALOG_TITLE_COLOR
        )

        title_rect = title.get_rect(
            centerx=self.rect.centerx,
            top=self.rect.y + 15
        )

        screen.blit(
            title,
            title_rect
        )

        # ==================================================
        # Close X
        # ==================================================

        x = self.close_rect

        pygame.draw.line(
            screen,
            Theme.DIALOG_TITLE_COLOR,
            (x.left + 5, x.top + 5),
            (x.right - 5, x.bottom - 5),
            2
        )

        pygame.draw.line(
            screen,
            Theme.DIALOG_TITLE_COLOR,
            (x.right - 5, x.top + 5),
            (x.left + 5, x.bottom - 5),
            2
        )

        # ==================================================
        # Captions
        # ==================================================

        if self.mode == "change_password":

            self._draw_caption(
                screen,
                "Current password",
                self.password_rect
            )

            self._draw_caption(
                screen,
                "New password",
                self.repeat_password_rect
            )

            self._draw_caption(
                screen,
                "Repeat new password",
                self.first_name_rect
            )

        else:

            self._draw_caption(
                screen,
                "Nickname",
                self.nickname_rect
            )

            self._draw_caption(
                screen,
                "Password",
                self.password_rect
            )

            if self.mode == "register":

                self._draw_caption(
                    screen,
                    "Repeat password",
                    self.repeat_password_rect
                )

                self._draw_caption(
                    screen,
                    "First name",
                    self.first_name_rect
                )

                self._draw_caption(
                    screen,
                    "Last name",
                    self.last_name_rect
                )

        # ==================================================
        # TextEdit
        # ==================================================

        for edit in self._get_edits():

            if edit is not None:
                edit.draw(screen)

        # ==================================================
        # Action button
        # ==================================================

        if self.mode == "login":

            action_text = "Login"

        elif self.mode == "register":

            action_text = "Register"

        else:

            action_text = "Change password"

        pygame.draw.rect(
            screen,
            Theme.TB_BACKGROUND_COLOR,
            self.action_rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            Theme.TB_FOCUS_BORDER_COLOR,
            self.action_rect,
            Theme.TB_BORDER_WIDTH,
            border_radius=6
        )

        text = self.caption_font.render(
            action_text,
            True,
            Theme.DIALOG_TITLE_COLOR
        )

        text_rect = text.get_rect(
            center=self.action_rect.center
        )

        screen.blit(
            text,
            text_rect
        )

        # ==================================================
        # Switch
        # ==================================================

        if self.mode == "login":

            switch_text = "Create account"

        else:

            switch_text = "Back to login"

        pygame.draw.rect(
            screen,
            Theme.TB_FOCUS_BORDER_COLOR,
            self.switch_rect,
            Theme.TB_BORDER_WIDTH,
            border_radius=6
        )

        text = self.message_font.render(
            switch_text,
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        text_rect = text.get_rect(
            center=self.switch_rect.center
        )

        screen.blit(
            text,
            text_rect
        )

        # ==================================================
        # Status message
        # ==================================================

        if self.message:

            status_message = StatusMessage(
                message=self.message,
                message_type=self.message_type,
                position=(
                    self.rect.x + 35,
                    self.rect.bottom - 28
                ),
                font=self.message_font
            )

            status_message.draw(screen)

    # ==================================================
    # CAPTION
    # ==================================================

    def _draw_caption(
        self,
        screen,
        text,
        rect
    ):

        if rect is None:
            return

        caption = self.caption_font.render(
            text,
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                rect.x,
                rect.y - 24
            )
        )

    # ==================================================
    # FOCUS
    # ==================================================

    def _focus_next_edit(self, backward=False):

        edits = [
            edit
            for edit in self._get_edits()
            if edit is not None
        ]

        if not edits:
            return

        current_index = -1

        for index, edit in enumerate(edits):

            if edit.focused:
                current_index = index
                break

        # Если сейчас ни одно поле не имеет фокуса
        if current_index == -1:

            next_index = (
                len(edits) - 1
                if backward
                else 0
            )

        else:

            if backward:

                next_index = (
                    current_index - 1
                ) % len(edits)

            else:

                next_index = (
                    current_index + 1
                ) % len(edits)

        # Снимаем фокус со всех полей
        self._clear_focus()

        # Устанавливаем новый фокус
        edits[next_index].focused = True

        pygame.key.start_text_input()