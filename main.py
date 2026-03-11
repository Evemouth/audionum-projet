import pygame
import time
import numpy as np
import units
from sound import draw_to_sound

pygame.init()
screen = pygame.display.set_mode((units.WINDOW_X, units.WINDOW_Y))
clock = pygame.time.Clock()
running = True

mouse_down = False
previous_mouse_pos = None
width = 20
color = "black"

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
                pygame.image.save(screen, f"dessins/dessin_{time.time()}.png")
            elif (event.key in (pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_z)) and not mouse_down:
                screen.fill("white")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
                previous_mouse_pos = None

    if mouse_down:
        pygame.draw.circle(screen, color, pygame.mouse.get_pos(), width // 2)
        if previous_mouse_pos is not None:
            pygame.draw.line(screen, color, previous_mouse_pos, pygame.mouse.get_pos(), width)
        previous_mouse_pos = pygame.mouse.get_pos()
        sound = draw_to_sound(pygame.mouse.get_pos(), pygame.mouse.get_rel(), width, color)
        pygame.sndarray.make_sound(sound.astype(np.int16)).play()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
