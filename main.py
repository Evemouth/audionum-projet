import pygame
import pygame.midi
import time
import math
import numpy as np
import units
from sound import draw_to_sound, draw_to_note_rectangle, draw_to_note_triangle, draw_to_note_triangle_adaptative, draw_to_note_hexagonal
from parser import parse_midi_file

pygame.init()
pygame.midi.init()
screen = pygame.display.set_mode((units.WINDOW_X, units.WINDOW_Y))
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont(None, 35)


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

INPUT_FILE = "au_clair_de_la_lune.mid"
parsed_midi = parse_midi_file(INPUT_FILE)

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
    draw_hex_grid(surface)

def draw_to_note(mouse_position: tuple[int, int], mouse_speed: tuple[int, int], width: int, color: str) -> dict:
    return draw_to_note_hexagonal(mouse_position, mouse_speed, width, color)
    # return draw_to_note_triangle_adaptative(parsed_midi, mouse_position, mouse_speed, width, color)

def draw_hexagon(surface, color, center_x, center_y, radius, border_width=1):
    """Calcule et dessine un polygone hexagonal."""
    points = []
    for i in range(6):
        # L'angle pour des hexagones "pointes en haut" commence à -30 degrés
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg

        # On calcule les coordonnées (x, y) de chaque sommet
        px = center_x + radius * math.cos(angle_rad)
        py = center_y + radius * math.sin(angle_rad)
        points.append((px, py))

    pygame.draw.polygon(surface, color, points, border_width)


def draw_hex_grid(surface):
    """Dessine un pavage hexagonal sur tout l'écran."""
    # On définit la taille de l'hexagone (son rayon)
    # Tu peux l'ajuster selon la résolution de ta fenêtre
    R = units.WINDOW_X // 20

    # Calcul des dimensions selon les formules mathématiques
    hex_width = math.sqrt(3) * R
    hex_height = 2 * R

    # On calcule combien de colonnes et de lignes il faut pour remplir l'écran
    # On ajoute +2 pour être sûr de bien couvrir les bords
    cols = int(units.WINDOW_X / hex_width) + 2
    rows = int(units.WINDOW_Y / (hex_height * 0.75)) + 2

    for row in range(rows):
        for col in range(cols):
            # Position X de base
            x = col * hex_width

            # Position Y : on descend de 3/4 de la hauteur à chaque ligne
            y = row * hex_height * 0.75

            # Décalage : si la ligne est impaire, on décale tout d'un demi-hexagone à droite
            if row % 2 == 1:
                x += hex_width / 2

            # On dessine l'hexagone ("lightgray" pour la couleur, 1 pour l'épaisseur du trait)
            draw_hexagon(surface, "lightgray", x, y, R, 1)

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

    screen.blit(font.render(f"Fichier : {INPUT_FILE}", True, "black"), (10, 10))
    screen.blit(font.render(f"Première note : {parsed_midi['first_note']}", True, "black"), (10, 40))
    screen.blit(font.render(f"Notes les plus présentes : {parsed_midi['sorted_notes'][0]} et {parsed_midi['sorted_notes'][1]}", True, "black"), (10, 70))
    screen.blit(font.render(f"Intervalles les plus présents : {list(parsed_midi['tones'].keys())[0]} et {list(parsed_midi['tones'].keys())[1]}", True, "black"), (10, 100))


    pygame.display.flip()

    clock.tick(60)

pygame.midi.quit()
pygame.quit()
