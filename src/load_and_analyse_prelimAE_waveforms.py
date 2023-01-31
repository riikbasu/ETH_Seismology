"""
Example processing script for loading and analysing AE waveform data from the prelimAE array of the FEAR project
"""
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import obspy
import numpy as np
from scipy import signal
import tqdm
from obspy.signal.trigger import classic_sta_lta
from obspy.signal.trigger import plot_trigger

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
    amplitude_phase_spectra_overlay
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
start_time_long = '2022-12-05T18:30:00.000000Z'
end_time_long = '2022-12-05T18:45:00.000000Z'

# Import Long Waveforms
st_long = project.waveforms.get_waveforms(
    channel_ids=[
        "XB.01.01.001",
        "XB.01.02.001",
        "XB.01.03.001",
        "XB.01.04.001",
        "XB.01.05.001",
        "XB.01.06.001",
        "XB.01.07.001",
        "XB.01.08.001",
    ],
    start_time=UTCDateTime(start_time_long),
    end_time=UTCDateTime(end_time_long),
)

# # Short Data Parameters
# start_time_short = '2022-12-05T18:41:52.9790000Z'
# end_time_short = '2022-12-05T18:41:52.989000Z'
# #
# # Short Data Parameters
# start_time_short = '2022-12-05T18:41:52.000000Z'
# end_time_short = '2022-12-05T18:41:54.000000Z'

# # Short Data Parameters
# start_time_short = '2022-12-05T18:38:10.940000Z'
# end_time_short = '2022-12-05T18:38:11.040000Z'

# Import Short Waveforms
# st_short = project.waveforms.get_waveforms(
#     channel_ids=[
#         "XB.01.01.001",
#         "XB.01.02.001",
#         "XB.01.03.001",
#         "XB.01.04.001",
#         "XB.01.05.001",
#         "XB.01.06.001",
#         "XB.01.07.001",
#         "XB.01.08.001",
#         ],
#     start_time=UTCDateTime(start_time_short),
#     end_time=UTCDateTime(end_time_short),
# )
#
# start_time_short1 = '2022-12-05T18:41:52.989000Z'
# end_time_short1 = '2022-12-05T18:41:52.999000Z'
#
# # Short Data Parameters
# start_time_short1 = '2022-12-05T18:38:10.940000Z'
# end_time_short1 = '2022-12-05T18:38:11.040000Z'

# st_short1 = project.waveforms.get_waveforms(
#     channel_ids=[
#         "XB.01.01.001",
#         "XB.01.02.001",
#         "XB.01.03.001",
#         "XB.01.04.001",
#         "XB.01.05.001",
#         "XB.01.06.001",
#         "XB.01.07.001",
#         "XB.01.08.001",
#     ],
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
#
# # Get 2nd Trace (Channel 4)
# trace_long1 = st_long[1]

# # Filter lowpass frequency
# trace_long = filter_frequency_lowpass_and_display(trace_long)

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
# # ObsPy dayplot of the long data
# trace_long1.plot(type="dayplot", title="Dayplot of the Long Input Data - Channel 3", interval=1,
#                 right_vertical_labels=False,
#                 vertical_scaling_range=15e2,
#                 horizontal_scaling_range=1,
#                 one_tick_per_line=True,
#                 color=['k', 'r', 'b', 'g'], show_y_UTC_label=False,
#                 # events={'min_magnitude': 50}
#                 )

# # Plot the long trace
# fig, axs = plt.subplots(nrows=1, ncols=1)
# plot_trace(trace_long, axs)
# plt.show()

# # Amplitude, Phase Spectra and Spectrogram of the long data are not plotted
#
#
# # Short Data Workflow

# # Visualise multiple traces
# fig = plot_time_waveform(st_short)
# fig.suptitle("Input Stream of Data: " + "time-waveform \nstarttime: " + str(st_short[0].stats.starttime), fontsize=10)
# fig.show()

# # Visualise multiple traces
# fig = plot_time_waveform(st_short1)
# fig.suptitle("Input Stream of Data: " + "time-waveform \nstarttime: " + str(st_short1[0].stats.starttime), fontsize=10)
# fig.show()

# # Get 1st Trace (Channel 3)
# trace_short = st_short[1]
# fig = plot_trace(trace_short)
# plt.show()
# trace_short1 = st_short1[1]
#
# # Get 2 traces from different channels in same stream
# trace_short = st_short[0]
# trace_short1 = st_short[1]
#
# Plot the Trace, Amplitude and Phase Spectra of the short data
# plot_trace_with_spectra_hann(trace_short)
# plot_trace_with_spectra_hann(trace_short1)
#
# # Spectrogram of the short data
# trace_short.spectrogram(log=True, title="Spectrogram of the Short Input Data", cmap='plasma')
#
# # Compare Amplitude Spectra
# amplitude_phase_spectra_overlay(trace_short, 'Channel 3', trace_short1, 'Channel 1')
# amplitude_phase_spectra_overlay(trace_short, 'With Ventilation', trace_short1, 'Without Ventilation')
# trace_amplitude_phase_spectra_overlay(trace_short, 'With Event', trace_short1, 'Without Event')
#
# # Helper function to compute intervals over the project.
# intervals = util.compute_intervals(
#     project=project, interval_length_in_seconds=0.1, interval_overlap_in_seconds=0.05
# )

# for interval_start, interval_end in tqdm.tqdm(intervals):
#     # Run the trigger only on a few waveforms.

# # Classic STA/LTA
# cft1 = classic_sta_lta(trace_short.data, 70, 700)
# plot_trigger(trace_short, cft1, 1.5, 0.5)
