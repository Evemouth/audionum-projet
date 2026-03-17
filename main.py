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

PALETTE_COLORS = ["black", "red", "orange", "yellow", "green", "blue", "purple", "white"]
PALETTE_SIZE = 40
PALETTE_MARGIN = 5
PALETTE_X = PALETTE_MARGIN 

def draw_palette(surface, selected_color):
    total_height = len(PALETTE_COLORS) * PALETTE_SIZE + (len(PALETTE_COLORS) - 1) * PALETTE_MARGIN
    for i in range(len(PALETTE_COLORS)):
        y = (units.WINDOW_Y - total_height) // 2 + i * (PALETTE_SIZE + PALETTE_MARGIN)
        cx = PALETTE_X + PALETTE_SIZE // 2
        cy = y + PALETTE_SIZE // 2
        radius = PALETTE_SIZE // 2
        pygame.draw.circle(surface, PALETTE_COLORS[i], (cx, cy), radius)
        if PALETTE_COLORS[i] == selected_color:
            pygame.draw.circle(surface, "gray", (cx, cy), radius, 3)

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
                mx, my = pygame.mouse.get_pos()
                clicked_palette = False
                total_height = len(PALETTE_COLORS) * PALETTE_SIZE + (len(PALETTE_COLORS) - 1) * PALETTE_MARGIN
                for i in range(len(PALETTE_COLORS)):
                    y = (units.WINDOW_Y - total_height) // 2 + i * (PALETTE_SIZE + PALETTE_MARGIN)
                    cx = PALETTE_X + PALETTE_SIZE // 2
                    cy = y + PALETTE_SIZE // 2
                    radius = PALETTE_SIZE // 2
                    if (mx - cx)**2 + (my - cy)**2 <= radius**2:
                        color = PALETTE_COLORS[i]
                        clicked_palette = True
                        break
                if not clicked_palette:
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

    draw_palette(screen, color)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()