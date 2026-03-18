import numpy as np
import math
import units
from miditoolkit.midi import parser

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

def draw_to_note(mouse_position: tuple[int, int], mouse_speed: tuple[int, int], width: int, color: str) -> dict:
    lettre = int((mouse_position[0] / units.WINDOW_X) * 7) % 7
    octave = int((mouse_position[1] / units.WINDOW_Y) * 12) % 12
    return {
        "pitch": units.note_to_midi(lettre, octave),
        "velocity": 100 + (abs(mouse_speed[0]) + abs(mouse_speed[1])) // 2
    }
