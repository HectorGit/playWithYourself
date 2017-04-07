import numpy as np

root_postion = {	'A':[[57,61,64]],
					'Am':[[57,60,64]],
					'Bb':[[58,62,65]],
					'Bbm':[[58,61,65]],
					'Bm':[[59,62,66]],
					'B':[[59,63,66]],
					'Bb':[[59,62,66]],
					'C':[[60,64,67]],
					'Cm':[[60,63,67]],
					'C#':[[61,65,68]],
					'Dbm':[[61,64,68]],
					'D':[[62,66,69]],
					'Dm':[[62,65,69]],
					'Eb':[[63,67,70]],
					'Ebm':[[63,66,70]],
					'E':[[64,68,71]],
					'Em':[[64,67,71]],
					'F':[[65,69,72]],
					'Fm':[[65,68,72]],
					'F#':[[66,70,73]],
					'F#m':[[66,69,73]],
					'F#':[[66,70,73]],
					'F#m':[[66,69,73]],
					'G':[[67,71,74]],
					'Gm':[[67,70,74]],
					'Ab':[[68,72,75]],
					'Abm':[[68,69,75]]}

chord_list = {		'A':[[40,45,49],[45,49,52], [52,57,61]],
					'Am':[[40,45,48], [45,48,52], [52,57,60]],
					'Bb':[[38,41,46], [46,50,53], [53,58,62]],
					'Bbm':[[37,41,46], [46,49,53], [53,58,61]],
					'B':[[39,42,47], [47,51,54], [54,59,63]],
					'Bm':[[38,42,47], [47,50,54], [54,59,62]],
					'C':[[36,40,43], [43,48,52], [48,52,55]],
					'Cm':[[36,39,43], [43,48,51], [48,51,55]],
					'C#':[[37,41,44], [44,49,53], [49,53,56]],
					'Dbm':[[37,40,44], [44,49,52], [49,52,56]],
					'D':[[38,42,45], [45,50,54], [50,54,57]],
					'Dm':[[38,41,45], [45,50,53], [50,53,57]],
					'Eb':[[34,39,43], [43,46,51], [51,55,58]],
					'Ebm':[[34,39,42], [46,51,54], [51,54,58]],
					'E':[[35,40,44], [44,47,52], [47,52,56]],
					'Em':[[35,40,43], [43,47,52], [47,52,57]],
					'F':[[36,41,45], [48,53,57], [48,53,57]],
					'Fm':[[36,41,44], [48,53,56], [48,53,56]],
					'F#':[[37,42,46], [46,49,54], [49,54,58]],
					'F#m':[[37,42,45], [45,49,54], [49,54,57]],
					'G':[[38,43,47], [43,47,50], [50,55,59]],
					'Gm':[[38,43,46], [43,46,50], [50,55,58]],
					'Ab':[[39,44,48], [44,48,51], [51,56,60]],
					'Abm':[[39,44,47], [44,47,51], [51,56,59]]}

beat_list = {	0:[[42,35],[42],[42,38],[42]],
				1:[[42,35],[42],[42,38],[42]]}

def convert_note_to_midi(notes, reg):
	print "...Converting notes to MIDI values"
	midi_notes = [[0]]
	for i in range(len(notes)):
		midi_notes.append([chord_list[notes[i]][(int(reg[i])/2)%3][0]])

	return midi_notes

def convert_chord_to_midi(chords, reg):
	print "...Converting chords to MIDI values"
	midi_chords = [[0,0,0]]
	for i in range(len(chords)):
		midi_chords.append(chord_list[chords[i]][(int(reg[i])/2)%3])

	return midi_chords

def convert_beat_to_midi(beats, pattern=0):
	print "...Converting beats to MIDI values"
	midi_beats = [[0]]
	for i in range(len(beats)):
		midi_beats.append(beat_list[int(pattern)][i%4])

	return midi_beats

def determine_durations(chords, reg, startTimes, endTimes, frameIndex, volume):
	i = 1; j = 0;
	while (i < len(chords)):
		if (chords[i] == chords[j]):
			if (volume[i] > volume[j]):
				volume = np.delete(volume, j)
			else:
				volume = np.delete(volume, i)
			chords = np.delete(chords, i)
			reg = np.delete(reg, i)
			startTimes = np.delete(startTimes, i)
			endTimes = np.delete(endTimes, j)
			frameIndex -= 1
			i -= 1; j -= 1
		i += 1; j += 1

	return chords, reg, startTimes, endTimes, frameIndex, volume





