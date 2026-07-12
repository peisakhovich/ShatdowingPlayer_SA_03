import pygame
import pygame_gui


print("pygame version:", pygame.version.ver)
print("pygame_gui imported OK")

pygame.init()

screen = pygame.display.set_mode((400, 300))

pygame.display.set_caption(
    "SA_03 Environment Test"
)

manager = pygame_gui.UIManager(
    (400, 300)
)


running = True
clock = pygame.time.Clock()


while running:

    time_delta = clock.tick(60) / 1000

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)


    manager.update(time_delta)

    screen.fill(
        pygame.Color("#202020")
    )

    manager.draw_ui(screen)

    pygame.display.update()


pygame.quit()