import mido

# Fonction pour parser un fichier MIDI et afficher les notes
def print_midi_file(file_path):
  freq_note = {}
  freq_tone = {}

  previous_note = None

  mid = mido.MidiFile(file_path)
  print(f"Durée totale : {mid.length} secondes")

  for i, track in enumerate(mid.tracks):
      print(f"--- PISTE {i}: {track.name} ---")

      for msg in track:
          if msg.type == 'note_on':
              if msg.velocity > 0:
                print(f"Note: {msg.note} | Velocité: {msg.velocity} | Temps: {msg.time}")

                # Comptage des notes
                if freq_note.get(msg.note) is None:
                   freq_note[msg.note] = 0
                freq_note[msg.note] += 1

                if previous_note is not None:
                  tone = abs(previous_note - msg.note)
                  if freq_tone.get(tone) is None:
                    freq_tone[tone] = 0
                  freq_tone[tone] += 1

                previous_note = msg.note

              else:
                print(f"Fin de note: {msg.note}")
          elif msg.type == 'note_off':
              print(f"Fin de note: {msg.note}")

  for track in mid.tracks:
      for msg in track:
          if msg.type == 'program_change':
              print(f"Instrument: {msg.program}")
  freq_note = list(dict(sorted(freq_note.items(), key=lambda item: item[1], reverse=True)).keys())[0]
  freq_tone = dict(sorted(freq_tone.items(), key=lambda item: item[1], reverse=True))

  return (freq_note, freq_tone)

def parse_midi_file(file_path):
    freq_note = {}
    freq_tone = {}
    first_note = None
    previous_note = None

    mid = mido.MidiFile(file_path)
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                if first_note is None:
                    first_note = msg.note

                if freq_note.get(msg.note) is None:
                    freq_note[msg.note] = 0
                freq_note[msg.note] += 1

                if previous_note is not None:
                    tone = abs(previous_note - msg.note)
                    if freq_tone.get(tone) is None:
                        freq_tone[tone] = 0
                    freq_tone[tone] += 1
                previous_note = msg.note

    sort_note = sorted(freq_note.items(), key=lambda item: item[1], reverse=True)
    print("Notes triées par fréquence : ", sort_note)
    freq_tone = dict(sorted(freq_tone.items(), key=lambda item: item[1], reverse=True))
    freq_tone.pop(0, None)

    return {
        "first_note": first_note,
        "sorted_notes": sort_note[0],
        "tones": freq_tone,
        "instrument": [msg.program for track in mid.tracks for msg in track if msg.type == 'program_change'][0]
    }

if __name__ == "__main__":
    print(parse_midi_file('calabria.mid'))
    print_midi_file('calabria.mid')

