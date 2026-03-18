WINDOW_X = 1800
WINDOW_Y = 1000

lettres = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def note_to_midi(note_index : int, octave : int) -> int:
    return (octave + 1) * 12 + note_index
