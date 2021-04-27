# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:22:18 2019

@author: catam
"""
import numpy as np
import matplotlib.pyplot as plt

from numpy import array, log, linspace, arange
from numpy.linalg import norm
from numpy.fft import fft, fftshift, ifft, ifftshift
from scipy.signal import stft, istft, get_window
import soundfile as sf

# Use the file with whales sounds
filename = 'la3 220hz.wav'

# Turn into a matrix
data, fe = sf.read(filename)
fe = float(fe)
T = arange(0, len(data)/fe, 1/fe)



## Compare Fourier transforms
N = len(data)
f = arange(-fe/2, fe/2, fe/N)

# Compute Fourier transform
X = fft(data)
Xf = fftshift(X)

ModXf = np.abs(Xf)/np.max(np.abs(Xf))

plt.figure()
plt.plot(f, ModXf, label = 'Original')
plt.title('Amplitude Spectrum of bell signal')
plt.xlabel('f (Hz)')
plt.ylabel('|Mod(f)|')
plt.show(block=True)













