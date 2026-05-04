WINDOW_X = 1800
WINDOW_Y = 1000

lettres = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# 0 : Acoustic Grand Piano
# 24 : Acoustic Guitar (nylon)
# 40 : Violin
# 56 : Trumpet
# 73 : Flute
# 13 : Xylophone
# 114 : Steel Drums
# 48 : String Ensemble 1
instruments = [0, 24, 40, 56, 73, 13, 114, 48]

def note_to_midi(note_index : int, octave : int) -> int:
    return (octave + 1) * 12 + note_index

def midi_to_note(midi_note : int) -> str:
    return lettres[midi_note % 12] + str(midi_note // 12 - 1)
