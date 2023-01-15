import matplotlib.pyplot as plt
import numpy as np

# Synthetic Dataset Workflow

# Create Sinusoid Signal
start_time = 0
end_time = 1
sampling = 0.01
time = np.arange(start_time, end_time, sampling)
Amplitude = 20
frequency = 5
signal_sin = Amplitude * np.sin(2 * np.pi * frequency * time)

#Plot
fig = plt.figure()
ax = fig.add_subplot(3, 1, 1)
ax.plot(time, signal_sin, "b-")
plt.ylabel('Amplitude')
plt.xlabel('Time')
plt.title('Input Waveform Time Series - Sinusoid')

# Amplitude and Phase Spectra
df = 1/sampling  # Sampling Rate
fNy = df / 2.0  # Nyquist frequency
trace_f = np.fft.rfft(signal_sin) * sampling * 2 # transform the signal into frequency domain
ax_amp_sp = fig.add_subplot(3, 1, 2)
freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
ax_amp_sp.plot(freq, abs(trace_f), 'k', label="Original frequencies")
plt.ylabel('Amplitude')

ax_ph_sp = fig.add_subplot(3, 1, 3)
ax_ph_sp.plot(freq, np.angle(trace_f), 'r')
plt.ylabel('Phase')
plt.xlabel('Frequency [Hz]')
plt.show()

# Spectrogram
signal_sin.spectrogram(log=True, title="Spectrogram of the Sinusoid", cmap='plasma')
