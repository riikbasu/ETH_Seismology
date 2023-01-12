"""
Example processing script for loading and analysing AE waveform data from the prelimAE array of the FEAR project
"""
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import obspy
import numpy as np
from scipy import signal

# Import from the DUGSeis library.
from DUGseis.dug_seis.project.project import DUGSeisProject
from DUGseis.dug_seis import util

from DUGseis.dug_seis.plotting.plotting import (
    get_time_vector,
    plot_time_waveform,
    plot_waveform_characteristic_function_magnitude,
    plot_waveform_characteristic_function,
)

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

# # Load the DUGSeis project.
# project = DUGSeisProject(config="load_and_analyse_prelimAE_waveforms.yaml")
#
# # Long Data Parameters
# start_time_long = '2022-12-07T12:00:00.00000Z'
# end_time_long = '2022-12-07T12:10:00.000000Z'
#
# # Short Data Parameters
# start_time_short = '2022-12-07T12:00:17.637000Z'
# end_time_short = '2022-12-07T12:00:17.639000Z'
#
# # Import Long Waveforms
# st_long = project.waveforms.get_waveforms(
#     channel_ids=["XB.01.03.001", "XB.01.04.001"],
#     start_time=UTCDateTime(start_time_long),
#     end_time=UTCDateTime(end_time_long),
# )
#
# # %% Visualise multiple traces
# fig = plot_time_waveform(st_long)
# fig.suptitle("Input Stream of Data: " + "time-waveform \nstarttime: " + str(st_long[0].stats.starttime), fontsize=10)
# fig.show()
#
# # Get 1st Trace (Channel 3)
# trace_long = st_long[0]
#
# # ObsPy dayplot of the long data
# trace_long.plot(type="dayplot", title="Dayplot of the Long Input Data - Channel 3", interval=1,
#                 right_vertical_labels=False,
#                 vertical_scaling_range=15e2,
#                 horizontal_scaling_range=1,
#                 one_tick_per_line=True,
#                 color=['k', 'r', 'b', 'g'], show_y_UTC_label=False,
#                 # events={'min_magnitude': 50}
#                 )
#
# # Standard Matlplotlib plotting routine to plot the long trace
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# ax.plot(trace_long.times("matplotlib"), trace_long.data, "b-")
# ax.xaxis_date()
# fig.autofmt_xdate()
# plt.ylabel('Amplitude')
# plt.xlabel('Time [hh:mm:ss:msec]')
# plt.title('Input Waveform Time Series - Long Data - Channel 3')
# plt.show()
#
# # Amplitude and Phase Spectra of the long data
# # df = trace_long.stats.sampling_rate  # Sampling Rate
# # fNy = df / 2.0  # Nyquist frequency
# # trace_f = np.fft.rfft(trace_long)  # transform the signal into frequency domain
# # fig = plt.figure()
# # plt.title('Input Waveform Amplitude and Phase Spectra - Long Data')
# # frame1 = plt.gca()
# # frame1.axes.get_xaxis().set_visible(False)
# # frame1.axes.get_yaxis().set_visible(False)
# # ax_amp_sp = fig.add_subplot(2, 1, 1)
# # freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
# # ax_amp_sp.plot(freq, abs(trace_f), 'k', label="Original frequencies")
# # plt.ylabel('Amplitude')
# #
# # ax_ph_sp = fig.add_subplot(2, 1, 2)
# # ax_ph_sp.plot(freq, np.angle(trace_f), 'r')
# # plt.ylabel('Phase')
# # plt.xlabel('Frequency [Hz]')
# # plt.show()
#
# # Spectrogram of the long data
# # trace_long.spectrogram(log=True, title="Spectrogram of the Long Input Data", cmap='plasma')
#
# # Import Short Waveforms
# st_short = project.waveforms.get_waveforms(
#     channel_ids=["XB.01.03.001", "XB.01.04.001"],
#     start_time=UTCDateTime(start_time_short),
#     end_time=UTCDateTime(end_time_short),
# )
# # Get 1st Trace (Channel 3)
# trace_short = st_short[0]
#
# # Standard Matlplotlib plotting routine to plot the short trace
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# ax.plot(trace_short.times("matplotlib"), trace_short.data, "b-")
# ax.xaxis_date()
# fig.autofmt_xdate()
# plt.ylabel('Amplitude')
# plt.xlabel('Time [hh:mm:ss:msec]')
# plt.title('Input Waveform Time Series - Short Data')
# plt.show()
#
# # Amplitude and Phase Spectra of the short data
# df = trace_short.stats.sampling_rate  # Sampling Rate
# fNy = df / 2.0  # Nyquist frequency
# trace_f = np.fft.rfft(trace_short)  # transform the signal into frequency domain
# fig = plt.figure()
# plt.title('Input Waveform Amplitude and Phase Spectra - Short Data')
# frame1 = plt.gca()
# frame1.axes.get_xaxis().set_visible(False)
# frame1.axes.get_yaxis().set_visible(False)
# ax_amp_sp = fig.add_subplot(2, 1, 1)
# freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
# ax_amp_sp.plot(freq, abs(trace_f), 'k', label="Original frequencies")
# plt.ylabel('Amplitude')
# plt.yscale('log')
# plt.xscale('log')
#
# ax_ph_sp = fig.add_subplot(2, 1, 2)
# ax_ph_sp.plot(freq, np.angle(trace_f), 'r')
# plt.ylabel('Phase')
# plt.xlabel('Frequency [Hz]')
# plt.xscale('log')
# plt.show()
#
# # Spectrogram of the short data
# trace_short.spectrogram(log=True, title="Spectrogram of the Short Input Data", cmap='plasma')
#
# # Filter out high frequencies and check effect on waveform and spectrogram
# trace_short.filter("lowpass", freq=20000, corners=2)
# trace_short.spectrogram(log=True, title="Spectrogram of the Short Input Data after filtering", cmap='plasma')
#
# # Plot the short trace after filtering
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# ax.plot(trace_short.times("matplotlib"), trace_short.data, "b-")
# ax.xaxis_date()
# fig.autofmt_xdate()
# plt.ylabel('Amplitude')
# plt.xlabel('Time [hh:mm:ss:msec]')
# plt.title('Input Waveform Time Series - Short Data - After high-cut filter')
# plt.show()
#
# # Trim to shorter duration - trace
# # ts = tr.stats.starttime
# # tr.trim(ts, ts + 0.1)
#
# # Trim to shorter duration - stream
# # st2 = st.copy()
# # st2.trim(ts, ts + 0.1)
# # fig = plot_time_waveform(st2)
# # fig.show()
#
# # Filter out high frequencies and check effect on waveform and spectrogram - stream
# # st2.filter("lowpass", freq=2000, corners=2)
# # fig = plot_time_waveform(st2)
# # fig.show()
#
# # More interesting plots
# # Customise spectrograms
# # Plot amplitude spectra of multiple time segments in same plot
