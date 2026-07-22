import pygame


class ExitDialog:

    def __init__(self, screen_rect):

        width = 400
        height = 180

        x = (
            screen_rect.width - width
        ) // 2

        y = (
            screen_rect.height - height
        ) // 2


        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )


        self.visible = True


        # кнопки

        self.yes_button = pygame.Rect(
            x + 60,
            y + 110,
            100,
            40
        )


        self.no_button = pygame.Rect(
            x + 240,
            y + 110,
            100,
            40
        )


        self.font = pygame.font.SysFont(
            None,
            28
        )


    def handle_event(self, event):

        if not self.visible:
            return None


        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.yes_button.collidepoint(
                    event.pos):

                return "exit"


            if self.no_button.collidepoint(
                    event.pos):

                return "cancel"


        return None



    def draw(self, screen):

        if not self.visible:
            return


        # затемнение фона

        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 120)
        )

        screen.blit(
            overlay,
            (0, 0)
        )


        # окно

        pygame.draw.rect(
            screen,
            (50, 50, 50),
            self.rect
        )


        pygame.draw.rect(
            screen,
            (180, 180, 180),
            self.rect,
            2
        )


        # текст

        text = self.font.render(
            "Выйти из приложения?",
            True,
            (255,255,255)
        )


        text_rect = text.get_rect(
            center=(
                self.rect.centerx,
                self.rect.y + 50
            )
        )


        screen.blit(
            text,
            text_rect
        )


        # кнопки

        pygame.draw.rect(
            screen,
            (70,120,70),
            self.yes_button
        )


        pygame.draw.rect(
            screen,
            (120,70,70),
            self.no_button
        )


        yes = self.font.render(
            "Да",
            True,
            (255,255,255)
        )

        no = self.font.render(
            "Нет",
            True,
            (255,255,255)
        )


        screen.blit(
            yes,
            yes.get_rect(
                center=self.yes_button.center
            )
        )


        screen.blit(
            no,
            no.get_rect(
                center=self.no_button.center
            )
        )