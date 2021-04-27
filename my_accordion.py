# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:18:06 2020

@author: catam
"""
import pyaudio
import numpy as np
from time import sleep, time


note_to_freq = {'Do3' : 261.63,
				'Re3' : 293.66,
				'Mi3' : 329.63,
				'Fa3' : 349.23,
				'Sol3' : 392.0,
				'La3' : 440.00,
				'Si3' : 493.88}


start_time = time()

p = pyaudio.PyAudio()

volume = 0.    # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 0.5   # in seconds, may be float
freq = 200

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)


for note in note_to_freq:
	frequency = note_to_freq[note]
	sound = (np.sin(2*np.pi*np.arange(fs*duration)*frequency/fs)).astype(np.float32)
	print("Playing "+note)
	stream.write(volume*sound)

stream.stop_stream()
stream.close()

p.terminate()