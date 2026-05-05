import pygame
import pygame.midi
import time
import numpy as np
import sys

import units
from sound import draw_to_sound, draw_to_note_hexagonal_adaptative, hex_points_to_notes, draw_grid_notes
from parser import parse_midi_file
from grid import draw_grid

pygame.init()
pygame.midi.init()
screen = pygame.display.set_mode((units.WINDOW_X, units.WINDOW_Y))
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont('freeserif', 30, bold=True)

midi_out_id = pygame.midi.get_default_output_id()
print(f"Using MIDI output ID: {midi_out_id}")

midi_out = pygame.midi.Output(midi_out_id, 0)
midi_out.set_instrument(0)
current_notes = [None, None, None]

mouse_down = False
previous_mouse_pos = None
width = 20
color = "black"

MIDI = True

PALETTE_COLORS = ["black", "red", "orange", "yellow", "green", "blue", "purple", "white"]
PALETTE_SIZE = 40
PALETTE_MARGIN = 5
PALETTE_X = PALETTE_MARGIN

if (len(sys.argv) > 1):
    INPUT_FILE = sys.argv[1]
else:
    INPUT_FILE = "get_lucky.mid"

screen.fill("white")
draw_grid(screen)

parsed_midi = parse_midi_file(INPUT_FILE)
hex_points_to_notes(parsed_midi)

font_small = pygame.font.SysFont('Arial', 15, bold=True)
draw_grid_notes(screen, font_small)

def draw_palette(surface, selected_color):
    total_height = len(PALETTE_COLORS) * PALETTE_SIZE + (len(PALETTE_COLORS) - 1) * PALETTE_MARGIN
    for i in range(len(PALETTE_COLORS)):
        y = (units.WINDOW_Y - total_height) // 2 + i * (PALETTE_SIZE + PALETTE_MARGIN)
        cx = PALETTE_X + PALETTE_SIZE // 2
        cy = y + PALETTE_SIZE // 2
        radius = PALETTE_SIZE // 2
        pygame.draw.circle(surface, PALETTE_COLORS[i], (cx, cy), radius)
        pygame.draw.circle(surface, "black", (cx, cy), radius, width=3)
        if PALETTE_COLORS[i] == selected_color:
            pygame.draw.circle(surface, "gray", (cx, cy), radius, 3)

def draw_to_note(mouse_position: tuple[int, int], mouse_speed: tuple[int, int], width: int, color: str) -> dict:
    return draw_to_note_hexagonal_adaptative(mouse_position, mouse_speed, width, color)

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
                draw_grid(screen)
                draw_grid_notes(screen, font_small)
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
                if MIDI and current_notes != [None, None, None]:
                    for pitch in current_notes:
                        if pitch is not None:
                            midi_out.note_off(pitch, 100)
                current_notes = [None, None, None]

    if mouse_down:
        pygame.draw.circle(screen, color, pygame.mouse.get_pos(), width // 2)
        if previous_mouse_pos is not None:
            pygame.draw.line(screen, color, previous_mouse_pos, pygame.mouse.get_pos(), width)

        previous_mouse_pos = pygame.mouse.get_pos()

        if MIDI:
            sound = draw_to_note(pygame.mouse.get_pos(), pygame.mouse.get_rel(), width, color)
            if sound["pitches"] != current_notes:
                if current_notes != [None, None, None]:
                    for pitch in current_notes:
                        midi_out.note_off(pitch, 100)
                midi_out.set_instrument(units.instruments[PALETTE_COLORS.index(color)])
                for pitch in sound["pitches"]:
                    midi_out.note_on(pitch, 100)
                current_notes = sound["pitches"]
        else:
            sound = draw_to_sound(pygame.mouse.get_pos(), pygame.mouse.get_rel(), width, color)
            pygame.sndarray.make_sound(sound.astype(np.int16)).play()

    draw_palette(screen, color)

    info_texts = [
        font.render(f"Fichier : {INPUT_FILE}", True, "black"),
        font.render(f"Première note : {units.midi_to_note(parsed_midi['first_note'])}", True, "black"),
        font.render(f"Notes les plus présentes : {units.midi_to_note(parsed_midi['sorted_notes'][0][0])} et {units.midi_to_note(parsed_midi['sorted_notes'][1][0])}" if isinstance(parsed_midi['sorted_notes'][0], tuple) else f"Notes les plus présentes : {units.midi_to_note(parsed_midi['sorted_notes'][0])} et {units.midi_to_note(parsed_midi['sorted_notes'][1])}", True, "black"),
        font.render(f"Intervalles les plus présents : {list(parsed_midi['tones'].keys())[0]} et {list(parsed_midi['tones'].keys())[1]}", True, "black")
    ]

    bg_rect = pygame.Rect(5, 5, max(t.get_width() for t in info_texts) + 20, len(info_texts) * 30 + 10)
    pygame.draw.rect(screen, "white", bg_rect)
    pygame.draw.rect(screen, "black", bg_rect, width=3, border_radius=5)

    for i, t in enumerate(info_texts):
        screen.blit(t, (15, 10 + i * 30))

    pygame.display.flip()

    clock.tick(60)

pygame.midi.quit()
pygame.quit()
