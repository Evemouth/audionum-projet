import numpy as np
import math
import units
from grid import hex_points, side

from collections import deque

# Mapping from hexagon centers to MIDI notes
hex_points_notes = {point: None for point in hex_points}
first_point = None

def hex_points_to_notes(parsed_midi: dict):
    global first_point

    first_note = parsed_midi["first_note"]
    tones = list(parsed_midi["tones"].keys())
    int_h = tones[0] 
    int_d = tones[1] 

    # Assign the first MIDI note to the point closest to the center of the window
    center_x, center_y = units.WINDOW_X / 2, units.WINDOW_Y / 2
    root_point = None
    min_dist_sq = float('inf')
    for point in hex_points:
        dist_sq = (point[0] - center_x)**2 + (point[1] - center_y)**2
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            root_point = point 
    first_point = root_point

    # Assign the first MIDI note to this root point
    hex_points_notes[root_point] = first_note

    # Use a breadth-first search to assign notes to points
    queue = deque([root_point]) 
    assigned = {root_point} # Set of points that are assigned to a note

    # Define the distance between hexagon centers
    dx = side * 1.5 
    dy = math.sqrt(3) * side

    while queue:
        curr = queue.popleft()
        curr_note = hex_points_notes[curr]

        # Define the relative positions and intervals for the 6 neighbors in a hex grid
        neighbors_vec = [
            ((dx, 0), int_h), # Right
            ((-dx, 0), -int_h), # Left
            ((dx/2, -dy/2), int_d), # Top right
            ((-dx/2, dy/2), -int_d), # Bottom left
            ((-dx/2, -dy/2), int_d - int_h), # Top left
            ((dx/2, dy/2), int_h - int_d) # Bottom right
        ]

        # For each neighbor, calculate the theoretical position and find the closest actual point
        for delta, interval in neighbors_vec:
            n_pos = (curr[0] + delta[0], curr[1] + delta[1])
            target = min(hex_points, key=lambda p: (p[0] - n_pos[0])**2 + (p[1] - n_pos[1])**2)
            
            dist_check = math.sqrt((target[0] - n_pos[0])**2 + (target[1] - n_pos[1])**2)
            if target not in assigned and dist_check < side * 0.5:
                hex_points_notes[target] = curr_note + interval
                assigned.add(target)
                queue.append(target)
    
def draw_grid_notes(surface, font):
    # Print the MIDI note names on the grid points
    for point, note in hex_points_notes.items():
        if note is not None:
            note_name = units.lettres[note % 12] + str(note // 12 - 1)
            if point == first_point:
                text_surf = font.render(note_name, True, "red") # the first note
            else:
                text_surf = font.render(note_name, True, "black")
            text_rect = text_surf.get_rect(center=point)
            surface.blit(text_surf, text_rect)

def draw_to_sound(mouse_position: tuple[int, int], mouse_speed: tuple[int, int], width: int, color: str) -> np.ndarray:
    frequence_echantillonnage = 44100
    duree = 0.1
    amplitude = 0.3
    frequence_son = 440 + (mouse_position[0] / units.WINDOW_X) * 880 + (mouse_position[1] / units.WINDOW_Y) * 880
    nombre_echantillons = int(frequence_echantillonnage * duree)
    n = np.arange(nombre_echantillons, dtype=np.float64)
    mono = amplitude * np.sin(n * 2 * math.pi * (frequence_son / frequence_echantillonnage))
    mono_int16 = (mono * np.iinfo(np.int16).max).astype(np.int16)
    stereo = np.column_stack((mono_int16, mono_int16))
    return stereo

def draw_to_note_rectangle(mouse_position: tuple[int, int], mouse_speed: tuple[int, int], width: int, color: str) -> dict:
    mx, my = mouse_position
    sx, sy = mouse_speed
    d1 = math.floor((mx / units.WINDOW_X) * 7) % 7
    d2 = math.floor((my / units.WINDOW_Y) * 12) % 12
    return {
        "pitch": units.note_to_midi(d1, d2),
        "velocity": 100 + (abs(sx) + abs(sy)) // 2
    }

def draw_to_note_triangle(mouse_position: tuple[int, int], mouse_speed: tuple[int, int], width: int, color: str) -> dict:
    mx, my = mouse_position
    sx, sy = mouse_speed

    num_columns = 24
    num_rows = 12

    dx = units.WINDOW_X / 12
    dy = units.WINDOW_Y / 12

    u = mx / dx
    v = my / dy

    B = math.floor(u - v / 2)
    C = math.floor(u + v / 2)

    col_triangle = B + C
    row_triangle = math.floor(v)
    d1 = col_triangle - (num_columns // 2)
    d2 = row_triangle - (num_rows // 2)

    return {
        "pitch": 60 + d1 * 4 + d2 * 2,
        "velocity": 100 + (abs(sx) + abs(sy)) // 2
    }

def draw_to_note_triangle_adaptative(parsed_midi: dict, mouse_position: tuple[int, int], mouse_speed: tuple[int, int], width: int, color: str) -> dict:
    mx, my = mouse_position
    sx, sy = mouse_speed

    num_columns = 24
    num_rows = 12

    dx = units.WINDOW_X / 12
    dy = units.WINDOW_Y / 12

    u = mx / dx
    v = my / dy

    B = math.floor(u - v / 2)
    C = math.floor(u + v / 2)

    col_triangle = B + C
    row_triangle = math.floor(v)
    d1 = col_triangle - (num_columns // 2)
    d2 = row_triangle - (num_rows // 2)

    return {
        "pitch": parsed_midi["first_note"] + d1 * list(parsed_midi["sorted_notes"].keys())[0] + d2 * list(parsed_midi["sorted_notes"].keys())[1],
        "velocity": 100 + (abs(sx) + abs(sy)) // 2
    }

def draw_to_note_hexagonal(mouse_position: tuple[int, int], mouse_speed: tuple[int, int], width: int, color: str) -> dict:
    mx, my = mouse_position
    sx, sy = mouse_speed

    R = units.WINDOW_X / 20

    q_frac = (math.sqrt(3)/3 * mx - 1/3 * my) / R
    r_frac = (2/3 * my) / R

    x = q_frac
    z = r_frac
    y = -x - z

    rx = round(x)
    ry = round(y)
    rz = round(z)

    x_diff = abs(rx - x)
    y_diff = abs(ry - y)
    z_diff = abs(rz - z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry

    q = rx
    r = rz
    pitch = 60 + (q * 4) + (r * 7)
    pitch = max(0, min(127, int(pitch)))

    return {
        "pitch": pitch,
        "velocity": 100 + (abs(sx) + abs(sy)) // 2
    }

def draw_to_note_hexagonal_adaptative(parsed_midi: dict, mouse_position: tuple[int, int], mouse_speed: tuple[int, int], width: int, color: str) -> dict:
    mx, my = mouse_position
    sx, sy = mouse_speed

    # Search for the 3 closest hexagon points to the mouse position
    closest_points = sorted(hex_points, key=lambda p: (p[0] - mx)**2 + (p[1] - my)**2)[:3]

    # Assign MIDI notes to these points based on their distance to the mouse position
    pitches = []
    for p in closest_points:
        note = hex_points_notes.get(p)
        if note is not None:
            pitches.append(max(0, min(127, int(note)))) # Ensure MIDI note is within valid range (0-127)

    # Calculate velocity based on mouse speed
    base_velocity = 100 + (abs(sx) + abs(sy)) // 2
    
    return {
        "pitches": pitches,
        "velocity": min(127, base_velocity)
    }    