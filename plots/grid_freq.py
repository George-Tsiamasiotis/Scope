import seaborn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scope import Q
from numpy.fft import fft, fftfreq
from scipy.signal import savgol_filter

plt.rcParams["text.usetex"] = True

fig_kw = {"figsize": (9, 6), "dpi": 120, "layout": "constrained"}


file = np.load("./data/grid_freq.npz")

df = pd.DataFrame({"time": file.get("times"), "frequency": file.get("measurements")})
df = df.where((df["frequency"] > 49.5) & (df["frequency"] < 50.5))


###########
# Histogram
###########

fig, ax = plt.subplots(**fig_kw)
seaborn.histplot(data=df, x="frequency", element="bars", kde=True)
ax.axvline(50, c="red")
ax.set_title("Frequency distribution")
ax.set_xlabel("$Frequency[Hz]$")
ax.set_ylabel("$Counts$")
plt.show(block=True)

############
# Timeseries
############

_, ax = plt.subplots(**fig_kw)
smooth = savgol_filter(df["frequency"], window_length=20, polyorder=5)
ax.plot(df["time"], df["frequency"], c="blue", linewidth=0.8, zorder=-2)
ax.plot(df["time"], smooth, c="red", linewidth=1.5)
ax.set_title("Frequency time-series")
ax.axhline(50, c="red")
ax.set_xlabel("$time$")
ax.set_ylabel("$Frequency[Hz]$")
plt.show(block=True)

##################
# Resample and FFT
##################

interval = "10s"
dfr = df.resample(interval, on="time").mean().reset_index()
interval = Q(interval).to("seconds")


n = len(dfr)
fourier = fft(dfr["frequency"] - dfr["frequency"].mean()) / n
fourier = np.abs(fourier)
freq = fftfreq(len(fourier))
# remove DC bias and normalize
fourier = fourier[freq > 0]
freq = freq[freq > 0]

_, ax = plt.subplots(**fig_kw)
markers, lines, base = ax.stem(freq, fourier)
markers.set_marker(".")
lines.set_linewidth(0.6)
ax.set_title("Fourier analysis")
ax.set_xlabel("$Frequency [Hz]$")
ax.set_ylabel("$Amplitude$")
ax.grid(True)
plt.show(block=True)

plt.close()
