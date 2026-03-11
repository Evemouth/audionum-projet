import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

mouse_down = False
previous_mouse_pos = None

screen.fill("white")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_c:
                running = False
            elif event.key == pygame.K_s:
                pygame.image.save(screen, "dessin.png")
            elif event.key == pygame.K_DELETE:
                screen.fill("white")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
                previous_mouse_pos = None

    if mouse_down:
        pygame.draw.circle(screen, "black", pygame.mouse.get_pos(), 9)
        if previous_mouse_pos is not None:
            pygame.draw.line(screen, "black", previous_mouse_pos, pygame.mouse.get_pos(), 20)
        previous_mouse_pos = pygame.mouse.get_pos()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
