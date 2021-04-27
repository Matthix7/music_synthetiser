# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:18:06 2020
Changed architecture to OOP on Mon Apr 19 22:30:00 2021

@author: Matthieu Bouveron
"""

import sounddevice as sd
import numpy as np
import time
import time as ti
from pynput import keyboard
from pynput.keyboard import Key
import clavier_une_main
import clavier_deux_mains





class Accordion():
	gamme = ['Do', 'Do#', 'Re', 'Re#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
	
	def __init__(self, sound_library, configuration):
		### Variables initialisation
		self.volume = 0.05    # range [0.0, 1.0], keep low to avoid saturation
		self.end = False
		self.start_idx = 0
		self.freqs_played = []
		self.freqs_crescendo = dict() # {freq : [press_time, volume, current_volume]}
		self.freqs_decrescendo = dict() # {freq : [release_time, volume, current_volume]}
		self.notes_played = []
		self.keys_pressed = []
		self.volumes_of_notes = {}
		self.sound = np.zeros((384,1))
		self.sample_rate = 44100

		self.keyboardListener = keyboard.Listener(on_press=self.on_press, on_release = self.on_release)
		self.keyboardListener.start()

		self.sound_library = sound_library
		if sound_library == "diapason":
			self.crescendo_duration = 1
			self.decrescendo_duration = 2
		if sound_library == "accordion":
			self.crescendo_duration = 0.01
			self.decrescendo_duration = 0.2
		if sound_library == "carillon":
			self.crescendo_duration = 0.01
			self.decrescendo_duration = 0.8
		if sound_library == "orgue_synthé":
			self.crescendo_duration = 0.05
			self.decrescendo_duration = 0.2



		self.keyboard_configuration = configuration

		if self.keyboard_configuration == "une_main":
			self.keys_to_notes = clavier_une_main.clavier 
		elif kself.eyboard_configuration == "deux_mains":
			self.keys_to_notes = clavier_deux_mains.clavier 
		else:
			raise Exception("Configuration not understood.")



	############################################################################################
	#########################  Relation notes - fréquences  ####################################

	def get_freq_from_note(self, note):
		if note == "None":
			return 0
		else:
			note_index = self.gamme.index(note[:-1])
			note_scale = eval(note[-1])  -1	# constant to adjust scale	
			note_freq = 440 * 2**((note_scale-3)+(note_index-9)/12)
			return note_freq


	############################################################################################
	############################   Keyboard monitoring   #######################################

	def get_note_from_key(self, key):
		try :
			if key in self.keys_to_notes.keys():
				note = self.keys_to_notes[key]
			elif key.char in self.keys_to_notes.keys():
				note = self.keys_to_notes[key.char]
			return note
		except:
			return 'None'


	def get_sound_from_freq(self, sample_time):
		new_sound = 0*sample_time
		harmonics = self.get_harmonics(self.sound_library) 
		crescendo_ended = []
		decrescendo_ended = []
		# print(self.freqs_crescendo, self.freqs_played, self.freqs_decrescendo)

		for freq in self.freqs_played:
			new_sound += np.sin(2*np.pi*sample_time*freq)
			for alpha_n, power in harmonics:
				new_sound += power * np.sin(2*np.pi*sample_time*freq*alpha_n)


		for freq in self.freqs_crescendo:
			press_time, initial_volume, current_volume = self.freqs_crescendo[freq]
			volume = 1 - (1-initial_volume) * np.exp(-(time.time()-press_time)/self.crescendo_duration)
			self.freqs_crescendo[freq][2] = volume
			new_sound += volume * np.sin(2*np.pi*sample_time*freq)
			for alpha_n, power in harmonics:
				new_sound += volume * power * np.sin(2*np.pi*sample_time*freq*alpha_n)
			if volume > 0.99:
				crescendo_ended.append(freq)

		for freq in crescendo_ended:
			del self.freqs_crescendo[freq]
			self.freqs_played.append(freq)


		for freq in self.freqs_decrescendo: 
			release_time, initial_volume, current_volume = self.freqs_decrescendo[freq]
			volume = initial_volume * np.exp(-(time.time()-release_time)/self.decrescendo_duration)
			self.freqs_decrescendo[freq][2] = volume
			new_sound += volume * np.sin(2*np.pi*sample_time*freq)
			for alpha_n, power in harmonics:
				new_sound += volume * power * np.sin(2*np.pi*sample_time*freq*alpha_n)
			if volume < 0.01:
				decrescendo_ended.append(freq)

		for freq in decrescendo_ended:
			del self.freqs_decrescendo[freq]

		return new_sound



	def on_press(self, key):
		note = self.get_note_from_key(key)
		frequency = self.get_freq_from_note(note)

		if frequency not in self.freqs_crescendo.keys() and frequency not in self.freqs_played:
			volume = 0
			if frequency in self.freqs_decrescendo:
				volume = self.freqs_decrescendo[frequency][2]
			self.freqs_crescendo[frequency] = [time.time(), volume, volume]
			self.keys_pressed.append(key)
			self.notes_played.append(note)
			self.freqs_decrescendo.pop(frequency, None)


	def on_release(self, key):
		note = self.get_note_from_key(key)
		frequency = self.get_freq_from_note(note)

		if frequency not in self.freqs_decrescendo.keys():
			volume = 1
			if frequency in self.freqs_crescendo:
				volume = self.freqs_crescendo[frequency][2]
			self.freqs_decrescendo[frequency] = [time.time(), volume, volume]
			self.keys_pressed.remove(key)
			self.notes_played.remove(note)	
			self.freqs_crescendo.pop(frequency, None)
			if frequency in self.freqs_played:
				self.freqs_played.remove(frequency)

		if key == Key.esc:
			self.end = True
			return False



	def get_harmonics(self, instrument):
		if instrument == "diapason":
			harmonics = []

		if instrument == "carillon":
			harmonics = [(0.5,0.552), (1.2,0.75), (1.5,0.08), (2,0.88), (2.5,0.12), (2.6,0.05), (2.7,0.15), \
					 (3,0.47), (3.3,0.08), (3.7,0.06), (5.1,0.11), (6.3,0.19), (7.6,0.1), (8.7,0.03)]

		if instrument == "accordéon":
			harmonics = [(2.0, 0.18), (3.0, 1.11), (4.0, 0.47), (5.0, 0.20), (6.0, 0.36), (7.0, 0.48), \
						 (8.0, 0.22), (9.0, 0.13), (10.0, 0.06), (11.0, 0.054), (12.0, 0.045), (13.0, 0.036), \
						 (14.0, 0.038), (16.0, 0.027), (17.0, 0.033), (18.0, 0.033)]


		if instrument == "orgue_synthé":
			harmonics = [(0.5, 0.7), (1.5, 0.6), (2.0, 0.5), (2.5, 0.14), (3.0, 1.11), (4.0, 0.47), (5.0, 0.20), (6.0, 0.36), \
						 (7.0, 0.48), (8.0, 0.22), (9.0, 0.13), (10.0, 0.06), (11.0, 0.054)]

		return harmonics






############################################################################################
###################################   MAIN   ###############################################


	def sound_generation_callback(self, outdata, frames, time, status):
		print("Notes played : ", self.notes_played)
		t = ((self.start_idx + np.arange(frames)) / self.sample_rate).reshape(-1,1)
		self.start_idx += frames  # frames = 384 
		outdata[:] = self.volume * self.get_sound_from_freq(t)





########################################################################################
########################################################################################

if __name__ == "__main__":
	# "diapason", "accordion", "carillon", "orgue_synthé"
	# "une_main", "deux_mains"
	my_accordion = Accordion(sound_library = "orgue_synthé", configuration = "une_main")

	with sd.OutputStream(channels=2, callback=my_accordion.sound_generation_callback, samplerate=my_accordion.sample_rate):

		while not my_accordion.end:
			time.sleep(0.1)