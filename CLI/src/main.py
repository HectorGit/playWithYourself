# IMPORT PYTHON LIBRARIES
import sys


# IMPORT MIR LIBRARIES
sys.path.append('../lib')
import librosa
import pymir
import midiutil


# IMPORT OUR MIR FUNCTIONS
sys.path.append('functions')
import utils
import dictionaries
import beatDetection
import chordPrediction
import midiConversion
import midiFileCreation


show_diagnostics, settings, save = utils.set_defaults()
print(	'\nWelcome to Play With Yourself Music Accompaniment Tool.'
		'\nType help for a list of valid commands')

while(True):
	cmd = raw_input('\nWhat would you like to do?\n')
	cmd, show_diagnostics, settings, save = utils.process_command(cmd, show_diagnostics, settings, save);
	if (cmd == 'load_yes'):
		UI_instrument_notes = int(settings['inst1']);			UI_onset_threshold = float((10-int(settings['busy']))/10.0);
		UI_instrument_chords = int(settings['inst2']);			UI_dynamic_threshold = float(settings['dyn']/10.0);
		UI_instrument_beats = int(settings['inst3']);			UI_beat_windowSize = float(settings['window']/10.0); #300 msec
		UI_beat_pattern = int(settings['pattern']);				UI_chord_style = int(settings['style']);
		UI_time_signature = int(settings['timeSig']);			y, sr = librosa.load(settings['filename'])


		# TRACK BEATS
		onsets, beats, volume_notes, times, tempo, msec_tempo = beatDetection.track_beats(y, sr, UI_onset_threshold, UI_dynamic_threshold, UI_beat_windowSize)
		beatDetection.plot_beats_and_onsets(onsets, beats, times, show_diagnostics)


		# PREDICT CHORDS
		notes, reg_notes, startTimes_notes, endTimes_notes, frameIndex_notes = chordPrediction.get_chords(settings['filename'], times[beats], times)
		chords, reg_chords, startTimes_chords, endTimes_chords, frameIndex_chords, volume_chords = midiConversion.determine_durations(list(notes), list(reg_notes), list(startTimes_notes), list(endTimes_notes), frameIndex_notes, list(volume_notes))
		chordPrediction.print_chords_and_times(chords, startTimes_chords, endTimes_chords, frameIndex_chords, times, show_diagnostics)
		startTimes_beats, endTimes_beats, volume_beats = beatDetection.alter_beats(startTimes_notes, endTimes_notes, volume_notes, msec_tempo, UI_beat_windowSize, settings['speed'])


		# NOTES TO MIDI
		midi_notes = midiConversion.convert_note_to_midi(notes, reg_notes)
		midi_chords = midiConversion.convert_chord_to_midi(chords, reg_chords, UI_chord_style)
		midi_beats = midiConversion.convert_beat_to_midi(notes, UI_beat_pattern, UI_time_signature, UI_instrument_beats, reg_notes, settings['speed'])


		# WRITE MIDI
		midi_tracks = [midi_notes, midi_chords, midi_beats]
		startTimes = [startTimes_notes, startTimes_chords, startTimes_beats]
		endTimes = [endTimes_notes, endTimes_chords, endTimes_beats]
		UI_instrument = [UI_instrument_notes, UI_instrument_chords, UI_instrument_beats]
		volumes = [volume_notes, volume_chords, volume_beats]
		duration = [0]*len(midi_tracks); program = [0]*len(midi_tracks); volume = [0]*len(midi_tracks);
		for i in range(len(midi_tracks)):
			duration[i], program[i], volume[i] = midiFileCreation.build_track(UI_instrument[i], midi_tracks[i], startTimes[i], endTimes[i], volumes[i], msec_tempo, UI_dynamic_threshold)
		midiFileCreation.write_midi_file(settings['filename'], midi_tracks, program, duration, tempo[0], volume)


		# PREVIEW
		utils.preview(filename=settings['filename'],length=settings['preview'])
		utils.clean(filename=settings['filename'])
