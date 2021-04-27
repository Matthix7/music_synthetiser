# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:18:06 2020

@author: catam
"""
import pyaudio
import numpy as np
import time
from pynput import keyboard
from pynput.keyboard import Key


note_to_freq = {'None' : 0,
				'Do3' : 261.63,
				'Re3' : 293.66,
				'Mi3' : 329.63,
				'Fa3' : 349.23,
				'Sol3' : 392.0,
				'La3' : 440.00,
				'Si3' : 493.88,
				'Do4' : 523.25}

### Variables initialisation
volume = 0.5    # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.5   # in seconds, may be float
note = 'None'
end = False
sound = 0*np.arange(fs*duration)
notes_pressed = []

### Keyboard monitoring

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

### PyAudio setup
p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
	global sound
	data = sound.astype(np.float32)
	return (data, pyaudio.paContinue)

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True,
                stream_callback=callback)

stream.start_stream()

########################################################################################
################################## MAIN ################################################
while not end and stream.is_active():
    time.sleep(1)                 
########################################################################################
########################################################################################


### Release
stream.stop_stream()
stream.close()
p.terminate()