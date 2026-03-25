import numpy as np
import math
import units

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

    dx = units.WINDOW_X / 12
    dy = units.WINDOW_Y / 12

    u = mx / dx
    v = my / dy

    B = math.floor(u - v / 2)
    C = math.floor(u + v / 2)

    col_triangle = B + C
    row_triangle = math.floor(v)
    d1 = col_triangle % 7
    d2 = row_triangle % 12

    return {
        "pitch": units.note_to_midi(d1, d2),
        "velocity": 100 + (abs(sx) + abs(sy)) // 2
    }
