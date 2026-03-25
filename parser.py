import mido

# Fonction pour parser un fichier MIDI et afficher les notes
def parse_midi_file(file_path):
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
                if freq_note.get(msg.note) == None:
                   freq_note[msg.note] = 0
                freq_note[msg.note] += 1

                if previous_note != None:
                  tone = abs(previous_note - msg.note)
                  if freq_tone.get(tone) == None:
                    freq_tone[tone] = 0
                  freq_tone[tone] += 1
                  
                previous_note = msg.note

              else:
                print(f"Fin de note: {msg.note}")
          elif msg.type == 'note_off':
              print(f"Fin de note: {msg.note}")

  freq_note = list(dict(sorted(freq_note.items(), key=lambda item: item[1], reverse=True)).keys())[0]
  freq_tone = dict(sorted(freq_tone.items(), key=lambda item: item[1], reverse=True))
  
  return (freq_note, freq_tone) 

print("ECART ET NOTE PRINCIPALE : ", parse_midi_file('au_clair_de_la_lune.mid'))

