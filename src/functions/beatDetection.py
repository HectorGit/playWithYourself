import librosa
import numpy as np
import matplotlib.pyplot as plt

import utils

def alter_beats(s, e, msec_tempo, UI_window):
	a = [s[0]]; b = []
	for i in range(len(e)):
		est_next_beat = round(s[0] + (msec_tempo*(i+1)), 3)
		near_e, idx_e = utils.find_nearest(e, est_next_beat)
		near_s, idx_s = utils.find_nearest(s, est_next_beat)

		if (est_next_beat >= e[-1]):
			b.append(e[-1])
			break;
		elif ((abs(est_next_beat - near_e) < UI_window)):
			a.append(near_e)
			b.append(near_e)
		else:
			a.append(est_next_beat)
			b.append(est_next_beat)
	return a, b

def plot_beats_and_onsets(onsets, beats, times, show):
	if (not show): return times
	print "...Plotting beats and onsets"
	
	plt.figure(figsize=(8, 4));
	plt.plot(times, onsets,label='Onset strength');
	plt.vlines(times[beats], 0, 1, alpha=0.5, color='r',linestyle='--', label='Beats');
	
	plt.legend(frameon=True, framealpha=0.75);
	plt.xlim(0, times[-1]);
	plt.show();

def track_beats(y, sr, UI_onset, UI_dynamic, UI_window):
	print "...Tracking onsets"
	onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median);
	
	onsets = librosa.util.normalize(onset_env)
	times = librosa.frames_to_time(np.arange(len(onsets)));
	tempo = librosa.beat.beat_track(y=y, sr=sr); msec_tempo = 60/tempo[0]
	
	beats = []
	for i in range(1, len(onsets)-1):
		if ((onsets[i] > onsets[i-1] and onsets[i] > onsets[i+1]) and onsets[i] > UI_onset):
			beats.append(i)
	
	i = 1; j = 0;
	while (i < len(times[beats])):
		beat_length = times[beats][i]-times[beats][j]
		if(beat_length < UI_window):
			if(times[beats][j] < times[beats][i]): 
				del beats[j]
			else: 
				del beats[i]
			i += 1; j += 1
		i += 1; j += 1

	volume = onsets[beats]*UI_dynamic*127
	
	return onsets, beats, volume, times, tempo, msec_tempo

	