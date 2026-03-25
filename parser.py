import mido

def parse_midi_file(file_path):
  mid = mido.MidiFile(file_path)
  print(f"Durée totale : {mid.length} secondes")

  for i, track in enumerate(mid.tracks):
      print(f"--- PISTE {i}: {track.name} ---")
      
      for msg in track:
          if msg.type == 'note_on':
              if msg.velocity > 0:
                print(f"Note: {msg.note} | Velocité: {msg.velocity} | Temps: {msg.time}")
              else:
                print(f"Fin de note: {msg.note}")
          elif msg.type == 'note_off':
              print(f"Fin de note: {msg.note}")

parse_midi_file('au_clair_de_la_lune.mid')
