# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:18:06 2020

@author: catam
"""
import sounddevice as sd
import numpy as np
import time
from pynput import keyboard
from pynput.keyboard import Key


############################################################################################
#########################  Relation notes - fréquences  ####################################

def get_freq_from(note):
	if note == "None":
		return 0
	else:
		gamme = ['Do', 'Do#', 'Re', 'Re#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
		note_index = gamme.index(note[:-1])
		note_scale = eval(note[-1])		
		note_freq = 440 * 2**((note_scale-3)+(note_index-9)/12)
		return note_freq

############################################################################################
############################   Keyboard monitoring   #######################################

def get_note_from(key):
	try:
		if key.char == 'q':
			note = 'Fa#2'

		elif key.char == 'z':
			note = 'Sol2'

		elif key.char == '"':
			note = 'Sol#2'

		elif key.char == 's':
			note = 'La2'

		elif key.char == 'e':
			note = 'La#2'

		elif key.char == "'":
			note = 'Si2'

		elif key.char == 'd':
			note = 'Do3'

		elif key.char == 'r':
			note = 'Do#3'

		elif key.char == '(':
			note = 'Re3'

		elif key.char == 'f':
			note = 'Re#3'

		elif key.char == 't':
			note = 'Mi3'

		elif key.char == '-':
			note = 'Fa3'

		elif key.char == 'g':
			note = 'Fa#3'

		elif key.char == 'y':
			note = 'Sol3'

		elif key.char == 'è':
			note = 'Sol#3'

		elif key.char == 'h':
			note = 'La3'

		elif key.char == 'u':
			note = 'La#3'

		elif key.char == '_':
			note = 'Si3'

		elif key.char == 'j':
			note = 'Do4'
			
		elif key.char == 'i':
			note = 'Do#4'

		elif key.char == 'ç':
			note = 'Re4'

		elif key.char == 'k':
			note = 'Re#4'

		elif key.char == 'o':
			note = 'Mi4'

		elif key.char == 'à':
			note = 'Fa4'

		elif key.char == 'l':
			note = 'Fa#4'

		elif key.char == 'p':
			note = 'Sol4'

		elif key.char == ')':
			note = 'Sol#4'

		elif key.char == 'm':
			note = 'La4'

		elif key.char == '^':
			note = 'La#4'

		elif key.char == '=':
			note = 'Si4'

		elif key.char == 'ù':
			note = 'Do5'

		elif key.char == '$':
			note = 'Do#5'

		else:
			note = 'None'
	except:
		if key == key.backspace:
			note = 'Re5'
		else:
			note = 'None'
	return note


def get_sound_from_freq(time, freqs_played):
	sound = 0*time
	for freq in freqs_played:
		sound += np.sin(2*np.pi*time*freq)
	return sound



def on_press(key):
	global end, freqs_played

	note = get_note_from(key)
	frequency = get_freq_from(note)

	if frequency not in freqs_played:
		freqs_played.append(frequency)


def on_release(key):
	global end, freqs_played

	note = get_note_from(key)
	frequency = get_freq_from(note)

	if frequency in freqs_played:
		freqs_played.remove(frequency)

	if key == Key.esc:
		end = True
		return False



keyboardListener = keyboard.Listener(on_press=on_press, on_release = on_release)
keyboardListener.start()


############################################################################################
###################################   MAIN   ###############################################


def callback(outdata, frames, time, status):
	global start_idx, freqs_played, volume, sample_rate

	t = ((start_idx + np.arange(frames)) / sample_rate).reshape(-1,1)
	start_idx += frames  # frames = 384 
	outdata[:] = volume * get_sound_from_freq(t, freqs_played)
	# print("Played: ", freqs_played)



def main():
	global end, start_idx, freqs_played, volume, sample_rate

	### Variables initialisation
	volume = 0.5    # range [0.0, 1.0]
	sample_rate = 44100       # sampling rate, Hz, must be integer
	end = False
	start_idx = 0
	freqs_played = []


	with sd.OutputStream(channels=2, callback=callback, samplerate=sample_rate):

		while not end:
			time.sleep(0.2)


########################################################################################
########################################################################################

if __name__ == "__main__":
	main()