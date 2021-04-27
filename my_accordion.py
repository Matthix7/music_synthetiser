# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:18:06 2020

@author: catam
"""
import simpleaudio as sa
import numpy as np
import time
from pynput import keyboard
from pynput.keyboard import Key


############################################################################################
#########################  Relation notes - fréquences  ####################################
note_to_freq = {'None' : 0,
				'Do3' : 261.63,
				'Re3' : 293.66,
				'Mi3' : 329.63,
				'Fa3' : 349.23,
				'Sol3' : 392.0,
				'La3' : 440.00,
				'Si3' : 493.88,
				'Do4' : 523.25}


############################################################################################
############################   Keyboard monitoring   #######################################

def get_note_from(key):
	try:
		if key.char == 'd':
			note = 'Do3'

		if key.char == '(':
			note = 'Re3'

		if key.char == 't':
			note = 'Mi3'

		if key.char == '-':
			note = 'Fa3'

		if key.char == 'y':
			note = 'Sol3'

		if key.char == 'h':
			note = 'La3'

		if key.char == '_':
			note = 'Si3'

		if key.char == 'j':
			note = 'Do4'
			
		else:
			note = 'None'
	except:
		note = 'None'
	return note


def on_press(key):
	global note, sound, notes_pressed, end

	note = get_note_from(key)
	if note not in notes_pressed:
		notes_pressed.append(note)
		frequency = note_to_freq[note]
		note_sound = (np.sin(2*np.pi*np.arange(fs*duration)*frequency/fs))
		sound += note_sound


def on_release(key):
	global note, sound, notes_pressed, end

	note = get_note_from(key)
	if note in notes_pressed:
		notes_pressed.remove(note)
		frequency = note_to_freq[note]
		note_sound = (np.sin(2*np.pi*np.arange(fs*duration)*frequency/fs))
		sound -= note_sound

	if key == Key.esc:
		end = True
		return False



keyboardListener = keyboard.Listener(on_press=on_press, on_release = on_release)
keyboardListener.start()


############################################################################################
###################################   MAIN   ###############################################

def main():
	### Variables initialisation
	volume = 0.5    # range [0.0, 1.0]
	sample_rate = 44100       # sampling rate, Hz, must be integer
	duration = 0.5   # in seconds, may be float
	note = 'None'
	end = False
	notes_pressed = []
	t = np.linspace(0, duration, int(duration * sample_rate), False)
	sound = np.sin(440*t*2*np.pi)


	while not end:
	# start playback
		play_obj = sa.play_buffer((sound * 32767 / np.max(np.abs(sound))).astype(np.int16), 1, 2, sample_rate)
		play_obj.wait_done()

	# wait for playback to finish before exiting
	play_obj.wait_done()



########################################################################################
########################################################################################

if __name__ == "__main__":
	main()