import matplotlib.pyplot as plt
import numpy as np
# Import from Function file
from src.data_Analysis_and_display_functions import (
    plot_trace,
    plot_amplitude_spectra,
    plot_trace_with_spectra,
    plot_trace_with_spectra_hann,
    filter_frequency_lowpass_and_display,
    trim_trace_and_display,
    compute_and_overlay_amplitude_spectra,
    trace_amplitude_phase_spectra_overlay,
    amplitude_phase_spectra_overlay,
    nextpow2,
)

# Synthetic Dataset Workflow

# Create Sinusoid Signal
start_time = 0
end_time = 1
sampling_time = 0.01
time = np.arange(start_time, end_time, sampling_time)
Amplitude = 20
frequency = 5
signal = Amplitude * np.sin(2 * np.pi * frequency * time) + Amplitude * np.sin(2 * np.pi * 2*frequency * time)

fig = plt.figure(figsize=(10, 15))
ax = fig.add_subplot(3, 1, 1)
ax.plot(time, signal, "b-")
# ax.xaxis_date()
# fig.autofmt_xdate()
plt.ylabel('Amplitude')
plt.xlabel('Time')
plt.suptitle('Trace with Amplitude and Phase Spectra')
plt.title('Trace Time Series')

sampling_freq = 1/sampling_time
pad = 2
signal = signal - np.mean(signal)  # detrend
hann = np.hanning(len(signal))
total_length_signal = nextpow2(len(signal) * pad)
trace_fft = np.fft.fft(signal * hann, n=total_length_signal)
trace_fft = trace_fft[0:int(total_length_signal / 2 + 1)]
trace_fft = trace_fft / len(signal)  # normalise
trace_fft[1:-1] = trace_fft[1:-1] * 2  # single sided, that is why times two
freq = np.arange(0, sampling_freq / 2 + sampling_freq / total_length_signal, sampling_freq / total_length_signal)
ax_amp_sp = fig.add_subplot(3, 1, 2)
ax_amp_sp.plot(freq, abs(trace_fft), 'k', label="Original frequencies")
plt.ylabel('Amplitude')
# plt.yscale('log')
plt.title('Amplitude Spectra')

ax_ph_sp = fig.add_subplot(3, 1, 3)
ax_ph_sp.plot(freq, np.angle(trace_fft), 'r')
plt.ylabel('Phase')
plt.xlabel('Frequency [Hz]')
plt.title('Phase Spectra')
plt.tight_layout()
plt.show()
#
# #Plot
# fig = plt.figure()
# ax = fig.add_subplot(3, 1, 1)
# ax.plot(time, signal, "b-")
# plt.ylabel('Amplitude')
# plt.xlabel('Time')
# plt.title('Input Waveform Time Series - Sinusoid')
#
# # Amplitude and Phase Spectra
# df = 1/sampling_time  # Sampling Rate
# fNy = df / 2.0  # Nyquist frequency
# trace_f = np.fft.rfft(signal) * sampling_time * 2 # transform the signal into frequency domain
# ax_amp_sp = fig.add_subplot(3, 1, 2)
# freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
# ax_amp_sp.plot(freq, abs(trace_f), 'k', label="Original frequencies")
# plt.ylabel('Amplitude')
#
# ax_ph_sp = fig.add_subplot(3, 1, 3)
# ax_ph_sp.plot(freq, np.angle(trace_f), 'r')
# plt.ylabel('Phase')
# plt.xlabel('Frequency [Hz]')
# plt.show()
#
# # Spectrogram
# signal_sin.spectrogram(log=True, title="Spectrogram of the Sinusoid", cmap='plasma')
