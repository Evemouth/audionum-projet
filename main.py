import pygame
import pygame.midi
import time
import numpy as np
import units
from sound import draw_to_sound, draw_to_note_rectangle, draw_to_note_triangle

pygame.init()
pygame.midi.init()
screen = pygame.display.set_mode((units.WINDOW_X, units.WINDOW_Y))
clock = pygame.time.Clock()
running = True

midi_out_id = pygame.midi.get_default_output_id()
print(f"Using MIDI output ID: {midi_out_id}")

midi_out = pygame.midi.Output(midi_out_id, 0)
midi_out.set_instrument(0)
current_note = 0


mouse_down = False
previous_mouse_pos = None
width = 20
color = "black"

MIDI = True

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

def draw_rectangle_grid(surface):
    for x in range(0, units.WINDOW_X, units.WINDOW_X//7):
        pygame.draw.line(surface, "lightgray", (x, 0), (x, units.WINDOW_Y))
    for y in range(0, units.WINDOW_Y, units.WINDOW_Y//12):
        pygame.draw.line(surface, "lightgray", (0, y), (units.WINDOW_X, y))

def draw_triangle_grid(surface):
    dx = units.WINDOW_X // 12
    dy = units.WINDOW_Y // 12

    for y in range(0, units.WINDOW_Y + dy, dy):
        pygame.draw.line(surface, "lightgray", (0, y), (units.WINDOW_X, y))

    offset_x = 6 * dx

    for x in range(-offset_x, units.WINDOW_X + offset_x, dx):
        pygame.draw.line(surface, "lightgray", (x, 0), (x + offset_x, units.WINDOW_Y))
        pygame.draw.line(surface, "lightgray", (x, 0), (x - offset_x, units.WINDOW_Y))

def draw_grid(surface):
    draw_triangle_grid(surface)

def draw_to_note(mouse_position: tuple[int, int], mouse_speed: tuple[int, int], width: int, color: str) -> dict:
    return draw_to_note_triangle(mouse_position, mouse_speed, width, color)

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
                current_note = None

    if mouse_down:
        pygame.draw.circle(screen, color, pygame.mouse.get_pos(), width // 2)
        if previous_mouse_pos is not None:
            pygame.draw.line(screen, color, previous_mouse_pos, pygame.mouse.get_pos(), width)
        previous_mouse_pos = pygame.mouse.get_pos()
        if MIDI:
            sound = draw_to_note(pygame.mouse.get_pos(), pygame.mouse.get_rel(), width, color)
            if sound["pitch"] != current_note:
                if current_note is not None:
                    midi_out.note_off(current_note, 100)
                midi_out.set_instrument(PALETTE_COLORS.index(color) * 2)
                midi_out.note_on(sound["pitch"], 100)
                current_note = sound["pitch"]
        else:
            sound = draw_to_sound(pygame.mouse.get_pos(), pygame.mouse.get_rel(), width, color)
            pygame.sndarray.make_sound(sound.astype(np.int16)).play()

    draw_grid(screen)
    draw_palette(screen, color)
    pygame.display.flip()

    clock.tick(60)

pygame.midi.quit()
pygame.quit()
