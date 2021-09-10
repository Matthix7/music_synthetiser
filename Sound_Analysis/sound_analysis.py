# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:22:18 2019

@author: catam
"""
import numpy as np
import matplotlib.pyplot as plt

from numpy import arange
from numpy.fft import fft, fftshift
import soundfile as sf

# Use the file with whales sounds
filename = 'piano_la4_440hz.wav'

# Turn into a matrix
data, fe = sf.read(filename)
fe = float(fe)
T = arange(0, len(data)/fe, 1/fe)


# Compare Fourier transforms
N = len(data)
f = arange(-fe/2, fe/2, fe/N)

# Compute Fourier transform
X = fft(data)
Xf = fftshift(X)

ModXf = np.abs(Xf)/np.max(np.abs(Xf))

plt.figure()
plt.plot(f, ModXf, label='Original')
plt.title('Amplitude Spectrum of signal')
plt.xlabel('f (Hz)')
plt.ylabel('|Mod(f)|')
plt.show(block=True)
