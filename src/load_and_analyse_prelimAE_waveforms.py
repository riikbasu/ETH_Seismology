"""
Example processing script for loading and analysing AE waveform data from the prelimAE array of the FEAR project
"""
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import obspy
import numpy as np
from scipy import signal

# Import from Function file
from src.data_Analysis_and_display_functions import (
    plot_trace,
    plot_amplitude_spectra,
    plot_trace_with_spectra,
    filter_frequency_lowpass_and_display,
    trim_trace_and_display,
    compute_and_overlay_amplitude_spectra,
    trace_amplitude_phase_spectra_overlay
)

# Import from the DUGSeis library.
from DUGseis.dug_seis.project.project import DUGSeisProject
from DUGseis.dug_seis import util

from DUGseis.dug_seis.plotting.plotting import (
    get_time_vector,
    plot_time_waveform,
    plot_waveform_characteristic_function_magnitude,
    plot_waveform_characteristic_function,
)

# Load the DUGSeis project.
project = DUGSeisProject(config="load_and_analyse_prelimAE_waveforms.yaml")

# Long Data Parameters
start_time_long = '2022-12-10T22:30:00.00000Z'
end_time_long = '2022-12-10T22:45:00.000000Z'

# Import Long Waveforms
st_long = project.waveforms.get_waveforms(
    channel_ids=["XB.01.03.001", "XB.01.04.001"],
    start_time=UTCDateTime(start_time_long),
    end_time=UTCDateTime(end_time_long),
)

# # Short Data Parameters
# start_time_short = '2022-12-07T15:32:37.653200Z'
# end_time_short = '2022-12-07T15:32:37.655200Z'
#
# # Import Short Waveforms
# st_short = project.waveforms.get_waveforms(
#     channel_ids=["XB.01.03.001", "XB.01.04.001"],
#     start_time=UTCDateTime(start_time_short),
#     end_time=UTCDateTime(end_time_short),
# )
# #
# start_time_short1 = '2022-12-07T15:32:37.655200Z'
# end_time_short1 = '2022-12-07T15:32:37.657200Z'
#
# st_short1 = project.waveforms.get_waveforms(
#     channel_ids=["XB.01.03.001", "XB.01.04.001"],
#     start_time=UTCDateTime(start_time_short1),
#     end_time=UTCDateTime(end_time_short1),
# )

# # Long Data Workflow
# # Visualise multiple traces
# fig = plot_time_waveform(st_long)
# fig.suptitle("Input Stream of Data: " + "time-waveform \nstarttime: " + str(st_long[0].stats.starttime), fontsize=10)
# fig.show()
#
# Get 1st Trace (Channel 3)
trace_long = st_long[0]

# ObsPy dayplot of the long data
trace_long.plot(type="dayplot", title="Dayplot of the Long Input Data - Channel 3", interval=1,
                right_vertical_labels=False,
                vertical_scaling_range=15e2,
                horizontal_scaling_range=1,
                one_tick_per_line=True,
                color=['k', 'r', 'b', 'g'], show_y_UTC_label=False,
                # events={'min_magnitude': 50}
                )
#
# # Plot the long trace
# fig, axs = plt.subplots(nrows=1, ncols=1)
# plot_trace(trace_long, axs)
# plt.show()
#
# # Amplitude, Phase Spectra and Spectrogram of the long data are not plotted
#
#
# # Short Data Workflow
# # Get 1st Trace (Channel 3)
# trace_short = st_short[0]
# trace_short1 = st_short1[0]
#
# # Plot the Trace, Amplitude and Phase Spectra of the short data
# plot_trace_with_spectra(trace_short)
# plot_trace_with_spectra(trace_short1)
#
# # Spectrogram of the short data
# trace_short.spectrogram(log=True, title="Spectrogram of the Short Input Data", cmap='plasma')
#
# # Filter lowpass frequency
# filter_frequency_lowpass_and_display(trace_short)
#
# # Compare Amplitude Spectra
# trace_amplitude_phase_spectra_overlay(trace_short, trace_short1)

