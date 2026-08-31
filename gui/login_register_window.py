
import pygame

from gui.theme import Theme
from gui.widgets.text_edit import TextEdit


class LoginRegisterWindow:
    """Общее окно Login / Register."""

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

        if mode not in ("login", "register"):
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

        # ==================================================
        # Fonts
        # ==================================================

        self.title_font = pygame.font.Font(
            None,
            28
        )

        self.caption_font = pygame.font.Font(
            None,
            20
        )

        self.message_font = pygame.font.Font(
            None,
            18
        )

        self.edit_font = pygame.font.Font(
            None,
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

        if mode not in ("login", "register"):
            raise ValueError(
                "Invalid LoginRegisterWindow mode"
            )

        self.mode = mode
        self.message = ""
        self.result = None

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
            self.edit_font
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
                self.edit_font
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

            self.repeat_password_rect = None
            self.repeat_password_edit = None

            self.first_name_rect = None
            self.first_name_edit = None

            self.last_name_rect = None
            self.last_name_edit = None

        # ==================================================
        # Action button
        # ==================================================

        self.action_rect = pygame.Rect(
            self.rect.centerx - 70,
            y,
            140,
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

        # ==================================================
        # Window close
        # ==================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # --------------------------------------------------
                # Close
                # --------------------------------------------------

                if self.close_rect.collidepoint(
                    event.pos
                ):
                    self.hide()
                    return

                # --------------------------------------------------
                # Action button
                # --------------------------------------------------

                if self.action_rect.collidepoint(
                    event.pos
                ):

                    self._clear_focus()

                    if self.mode == "login":
                        self._login()
                    else:
                        self._register()

                    return

                # --------------------------------------------------
                # Switch mode
                # --------------------------------------------------

                if self.switch_rect.collidepoint(
                    event.pos
                ):

                    if self.mode == "login":
                        self.set_mode("register")
                    else:
                        self.set_mode("login")

                    return

        # ==================================================
        # Pass event to TextEdit
        # ==================================================

        for edit in self._get_edits():

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
            return

        if not password:

            self.message = "Enter password"
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
            return

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        self.result = {
            "action": "login",
            "user": user
        }

        self.message = "Login successful"

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
            return

        if not password:

            self.message = "Enter password"
            return

        if password != repeat_password:

            self.message = "Passwords do not match"
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
            return

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        self.result = {
            "action": "register",
            "user": user
        }

        self.message = "Registration successful"

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
            Theme.DIALOG_BORDER_COLOR,
            self.rect,
            width=Theme.TB_BORDER_WIDTH,
            border_radius=Theme.DIALOG_RADIUS
        )

        # ==================================================
        # Title
        # ==================================================

        title_text = (
            "Login"
            if self.mode == "login"
            else "Register"
        )

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

        action_text = (
            "Login"
            if self.mode == "login"
            else "Register"
        )

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BORDER_COLOR,
            self.action_rect,
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

        switch_text = (
            "Create account"
            if self.mode == "login"
            else "Back to login"
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
        # Message
        # ==================================================

        if self.message:

            text = self.message_font.render(
                self.message,
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            text_rect = text.get_rect(
                centerx=self.rect.centerx,
                bottom=self.rect.bottom - 15
            )

            screen.blit(
                text,
                text_rect
            )

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
