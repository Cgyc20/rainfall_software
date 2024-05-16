import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fftfreq
from scipy.fftpack import *

#Note I was inspired here by https://tiofaizintio.medium.com/extract-seasonality-patterns-from-climate-data-with-fast-fourier-transform-fft-de479303f01

class fourier_analysis:
    def __init__(self,month,rainfall):
        self.month = month
        self.rainfall = rainfall 

        self.dt = 1  # Monthly data


    def fft_alg(self):

        y =fft(self.rainfall)

        return y

    def find_freq(self):
        n = len(self.rainfall)
        F = np.fft.fft(self.rainfall)
        w = np.fft.fftfreq(n, self.dt)

        # Filter out positive frequencies
        indices = np.where(w > 0)
        self.w_pos = w[indices]
        self.F_pos = F[indices]

        # Calculate phase
        self.phase = np.angle(self.F_pos)

        self.T = 1/self.w_pos
        sorted_indices = np.argsort(np.abs(self.F_pos))[::-1]

        # The sorted amplitudes 
        self.sorted_amp = np.abs(self.F_pos[sorted_indices])
        # And sorted frequencies
        self.sorted_freq = self.w_pos[sorted_indices]
        # And sorted phases
        self.sorted_phase = self.phase[sorted_indices]

        return self.sorted_amp, self.sorted_freq, self.sorted_phase
        
    def plot_freq(self):

        _, ax = plt.subplots(2, 1, figsize=(6, 4))

# Plot against positive frequencies
        ax[0].plot(self.w_pos, np.abs(self.F_pos))
        ax[0].set_xlabel('Frequency (cycles/month)', fontsize=13)
        ax[0].set_ylabel('Magnitude', fontsize=13)
        ax[0].set_title('Periodogram (FFT Result)', fontsize=15)
        ax[0].tick_params(labelsize=13)


        # Plot against periods
        ax[1].plot(self.T, np.abs(self.F_pos))
        ax[1].set_xlabel('Period (months)', fontsize=13)
        ax[1].set_ylabel('Magnitude', fontsize=13)
        ax[1].set_title('Periodogram (FFT Result)', fontsize=15)
        ax[1].tick_params(labelsize=13)
        #Set limit 
        ax[1].set_xlim(0, 24)
        plt.tight_layout()
        plt.show()


        

