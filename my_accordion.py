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
##########################   Relation clavier - note   #####################################

def get_note_from(key):
	try:		
		if key.char == 'a':
			note = 'Mi2'

		if key.char == 'é':
			note = 'Fa2'

		elif key.char == 'q':
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

def get_note_from_2(key):
	try:		
		### Main gauche
		if key.char == 'f':
			note = 'La1'

		elif key.char == 'r':
			note = 'La#1'

		elif key.char == "'":
			note = 'Si1'

		elif key.char == 'd':
			note = 'Do2'

		elif key.char == 'e':
			note = 'Do#2'

		elif key.char == '"':
			note = 'Re2'

		elif key.char == 's':
			note = 'Re#2'

		elif key.char == 'z':
			note = 'Mi2'

		elif key.char == "é":
			note = 'Fa2'

		elif key.char == 'q':
			note = 'Fa#2'

		elif key.char == 'a':
			note = 'Sol2'

		elif key.char == '&':
			note = 'Sol#2'


		### Main droite

		elif key.char == '(':
			note = 'Re3'

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
		if key == Key.caps_lock:
			note = 'La2'
		elif key == key.backspace:
			note = 'Re5'
		else:
			note = 'None'
	return note


############################################################################################
################   Relation fréquence (fondamentale) - son   ###############################

def get_sound_from_freq(time, freqs_played):
	new_sound = 0*time
	for freq in freqs_played:
		new_sound += np.sin(2*np.pi*time*freq) \
					+ 0.6 * np.sin(2*np.pi*time*freq*2**(-1)) \
					+ 0.8 * np.sin(2*np.pi*time*freq*2**(1))  \
					+ 0.4 * np.sin(2*np.pi*time*freq*2**(2))  \
					+ 0.4 * np.sin(2*np.pi*time*freq*2**(3))  \
					+ 0.6 * np.sin(2*np.pi*time*freq*2**(7/12))
	return new_sound


############################################################################################
########################   Surveillance du clavier   #######################################

def on_press(key):
	global end, freqs_played, notes_played

	# print("New key : ", key)
	note = get_note_from_2(key)
	frequency = get_freq_from(note)

	if frequency not in freqs_played:
		freqs_played.append(frequency)		
		notes_played.append(note)
		keys_pressed.append(key)

def on_release(key):
	global end, freqs_played, notes_played

	note = get_note_from_2(key)
	frequency = get_freq_from(note)

	if frequency in freqs_played:
		freqs_played.remove(frequency)
		notes_played.remove(note)
		keys_pressed.remove(key)

	if key == Key.esc:
		end = True
		return False

keyboardListener = keyboard.Listener(on_press=on_press, on_release = on_release)
keyboardListener.start()


############################################################################################
#########################   Mise à jour de l'audio   #######################################

def callback(outdata, frames, time, status):
	global start_idx, freqs_played, freqs_played_prev, volume, sample_rate, notes_played
	print("Notes played : ", notes_played)
	# print("Keys pressed : ", keys_pressed)
	# print("with frequencies : ", freqs_played,'\n')
	t = ((start_idx + np.arange(frames)) / sample_rate).reshape(-1,1)
	start_idx += frames  # frames = 384 
	outdata[:] = volume * get_sound_from_freq(t, freqs_played)
	freqs_played_prev = freqs_played


############################################################################################
###################################   MAIN   ###############################################

def main():
	global end, start_idx, freqs_played, notes_played, \
		   keys_pressed, volume, sample_rate, sound, freqs_played_prev
	### Variables initialisation
	volume = 0.1    # range [0.0, 1.0]
	sample_rate = 44100       # sampling rate, Hz, must be integer
	end = False
	start_idx = 0
	freqs_played = []
	freqs_played_prev = []
	notes_played = []
	keys_pressed = []
	sound = np.zeros((384,1))

	with sd.OutputStream(channels=2, callback=callback, samplerate=sample_rate):

		while not end:
			time.sleep(0.2)


########################################################################################
########################################################################################

if __name__ == "__main__":
	main()