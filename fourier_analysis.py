import pandas as pd
import numpy as np
from netCDF4 import Dataset, num2date
import nctoolkit as nc
import matplotlib.pyplot as plt
from plot_functions import data_manipulation
from numpy.fft import fftfreq
from scipy.fftpack import *

#Note I was inspired here by https://tiofaizintio.medium.com/extract-seasonality-patterns-from-climate-data-with-fast-fourier-transform-fft-de479303f01

data_path  = '/Users/charliecameron/CodingHub/Uni/Data_driven_processes/Data_modelling/data_sets/data_aus.nc'
#Now we can create an instance using the data_manipulation class
data_class = data_manipulation(data_path)
total_df = data_class.total_rainfall
#Create date_rf to just contain rf_mm and date columns
prec = total_df[['date','rf_mm']]

# Calculate the time step (assuming monthly data)
dt = 1  # Monthly data

# Number of data points
n = prec.shape[0]

# Perform FFT on the rainfall data
F = np.fft.fft(prec['rf_mm'])

# Generate frequencies
w = np.fft.fftfreq(n, dt)


# Filter out positive frequencies. This is because FFT is symmetrical so we only need to analyse the positive indices
indices = np.where(w > 0)
w_pos = w[indices] #The frequencies correspond to each data point (increasing by month)
F_pos = F[indices] #The fast fourier transformation of the data
T = 1/w_pos

#Sort the list in terms of periods, with the highest F_pos to lowest
sorted_periods = T[np.argsort(np.abs(F_pos))][::-1]
print("The top underlying monthly periods are given below in decreasing order:") 
print(sorted_periods[0:5])







#Find the top periods

# Plot the periodogram (FFT result)
fig, ax = plt.subplots(2, 1, figsize=(10, 8))

# Plot against positive frequencies
ax[0].plot(w_pos, np.abs(F_pos))
ax[0].set_xlabel('Frequency (cycles/month)', fontsize=13)
ax[0].set_ylabel('Magnitude', fontsize=13)
ax[0].set_title('Periodogram (FFT Result)', fontsize=15)
ax[0].tick_params(labelsize=13)



# Plot against periods
ax[1].plot(T, np.abs(F_pos))
ax[1].set_xlabel('Period (months)', fontsize=13)
ax[1].set_ylabel('Magnitude', fontsize=13)
ax[1].set_title('Periodogram (FFT Result)', fontsize=15)
ax[1].tick_params(labelsize=13)
#Set limit 
ax[1].set_xlim(0, 24)
plt.tight_layout()
plt.show()