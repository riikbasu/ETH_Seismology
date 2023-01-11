"""
Example processing script.
"""
import logging
from obspy import UTCDateTime
from obspy.imaging.spectrogram import spectrogram

import obspy
import tqdm
import numpy as np
# import matplotlib as mpl
# mpl.use('TkAgg')  # or can use 'TkAgg','Qt5Agg' whatever you have/prefer
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fftshift

# Import from the DUGSeis library.
from DUGseis.dug_seis.project.project import DUGSeisProject
from DUGseis.dug_seis import util
from aurem.pickers import AIC, REC

from DUGseis.dug_seis.event_processing.detection.dug_trigger import dug_trigger
from DUGseis.dug_seis.event_processing.picking.dug_picker import dug_picker
from DUGseis.dug_seis.event_processing.location.locate_homogeneous import (
    locate_in_homogeneous_background_medium,
)
from DUGseis.dug_seis.event_processing.magnitudes.amplitude_based_magnitudes import (
    amplitude_based_relative_magnitude,
)
from DUGseis.dug_seis.plotting.plotting import (
    plot_waveform_characteristic_function_magnitude,
    plot_time_waveform,
    plot_waveform_characteristic_function, plot_waveform_fft_amplitude,
)
from obspy.signal.trigger import plot_trigger
from obspy.signal.trigger import classic_sta_lta
from obspy.signal.trigger import z_detect
from obspy.signal.trigger import recursive_sta_lta
from obspy.signal.trigger import carl_sta_trig
from obspy.signal.trigger import delayed_sta_lta

# The logging is optional, but useful.
util.setup_logging_to_file(
    # folder=".",
    # If folder is not specified it will not log to a file but only to stdout.
    folder=None,
    log_level="info",
)
logger = logging.getLogger(__name__)

# Load the DUGSeis project.
project = DUGSeisProject(config="run_processing_FEAR_stations.yaml")

# Helper function to compute intervals over the project.
# intervals = util.compute_intervals(
#     project=project, interval_length_in_seconds=0.1, interval_overlap_in_seconds=0.1
# )
# project.config['temporal_range']['start_time'] = UTCDateTime('2022-12-07T12:00:17.600000Z')
# project.config['temporal_range']['end_time'] = UTCDateTime('2022-12-07T12:00:17.700000Z')
#
# total_event_count = 0

# for interval_start, interval_end in tqdm.tqdm(intervals):
# Run the trigger only on a few waveforms.

# Short Data of 2 msec
st_triggering = project.waveforms.get_waveforms(
    channel_ids=[
        # "XB.01.01.001",
        # "XB.01.02.001",
        # "XB.01.03.001",
        "XB.01.04.001",
        # "XB.01.05.001",
        # "XB.01.06.001",
        # "XB.01.07.001",
        # "XB.01.08.001",
    ],
    start_time=UTCDateTime('2022-12-07T12:00:17.637000Z'),
    end_time=UTCDateTime('2022-12-07T12:00:17.639000Z'),
)
trace = st_triggering[0]

# Long Data of 2 sec
st_triggering_long = project.waveforms.get_waveforms(
    channel_ids=[
        # "XB.01.01.001",
        # "XB.01.02.001",
        # "XB.01.03.001",
        "XB.01.04.001",
        # "XB.01.05.001",
        # "XB.01.06.001",
        # "XB.01.07.001",
        # "XB.01.08.001",
    ],
    start_time=UTCDateTime('2022-12-07T12:00:00.00000Z'),
    end_time=UTCDateTime('2022-12-07T12:10:00.000000Z'),
)
trace_long = st_triggering_long[0]

# ObsPy dayplot of the long data
trace_long.plot(type="dayplot", title="Dayplot of the Long Input Data", interval=1, right_vertical_labels=False,
                vertical_scaling_range=15e2,
                horizontal_scaling_range=1,
                one_tick_per_line=True,
                color=['k', 'r', 'b', 'g'], show_y_UTC_label=False,
                # events={'min_magnitude': 50}
                )

# Get noise levels, standard obspy
# st_triggering.plot()
# st_triggering.plot(type="dayplot", interval=1, right_vertical_labels=False,
#         vertical_scaling_range=5e3, one_tick_per_line=True,
#         color=['k', 'r', 'b', 'g'], show_y_UTC_label=False,
#         events={'min_magnitude': 6.5})

# Standard Matlplotlib plotting routine
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(trace.times("matplotlib"), trace.data, "b-")
# ax.set_xlim(UTCDateTime('2022-12-07T12:00:15.000000Z'),UTCDateTime('2022-12-07T12:00:20.000000Z'))
ax.xaxis_date()
fig.autofmt_xdate()
plt.ylabel('Amplitude')
plt.xlabel('Time [hh:mm:ss:msec]')
plt.title('Input Waveform Time Series - First Event')
plt.show()

# Amplitude and Phase Spectra
df = trace.stats.sampling_rate  # Sampling Rate
fNy = df / 2.0  # Nyquist frequency
trace_f = np.fft.rfft(trace)  # transform the signal into frequency domain
fig = plt.figure()
plt.title('Input Waveform Amplitude and Phase Spectra')
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
ax_amp_sp = fig.add_subplot(2, 1, 1)
freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
ax_amp_sp.plot(freq, abs(trace_f), 'k', label="Original frequencies")
plt.ylabel('Amplitude')

ax_ph_sp = fig.add_subplot(2, 1, 2)
ax_ph_sp.plot(freq, np.angle(trace_f), 'r')
plt.ylabel('Phase')
plt.xlabel('Frequency [Hz]')
plt.show()

# Spectrogram
# ax_sp = fig.add_subplot(3, 1, 3)
# spectrogram(trace.data, trace.stats.sampling_rate, wlen=0.002, axis=ax_sp, log=True, title="Spectrogram")
trace.spectrogram(log=True, title="Spectrogram of Input Data", cmap='plasma')

# Plot spectrogram
# x = trace.data
# fs = np.round(trace.stats.sampling_rate)
# f, t, Sxx = signal.spectrogram(x, fs)
# plt.pcolormesh(t, f, Sxx, shading='gouraud')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()

# Amplitude Spectra - not working from dug_seis plotting
# fig_amp_spectra = plot_waveform_fft_amplitude(st_triggering, int(5 * df), int(10 * df))
# fig_amp_spectra.show()

# custom plotting incl. characteristic function
fig_waveform_cf = plot_waveform_characteristic_function(st_triggering, 70, 700)
fig_waveform_cf.show()

# Classic STA/LTA
cft1 = classic_sta_lta(trace.data, 20, 100)
plot_trigger(trace, cft1, 1.4, 0.5)

# Z Detect
# cft2 = z_detect(trace.data, int( df/500))
# plot_trigger(trace, cft2, 2, 0.5)

# Recursive STA/LTA
# cft3 = recursive_sta_lta(trace.data, int(df/50), int(df/500))
# plot_trigger(trace, cft3, 1.5, 0.5)

# Carl STA Trigger
# cft4 = carl_sta_trig(trace.data, int(5 * df), int(10 * df), 0.8, 0.8)
# plot_trigger(trace, cft4, 20.0, -20.0)

# Delayed STA/LTA
# cft5 = delayed_sta_lta(trace.data, int(5 * df), int(10 * df))
# plot_trigger(trace, cft5, 5, 10)

#     Standard DUGSeis trigger.
#     detected_events = dug_trigger(
#     st=st_triggering,
#     # Helps with classification.
#     active_triggering_channel="XB.01.09.001",
#     minimum_time_between_events_in_seconds=0.015,
#     max_spread_electronic_interference_in_seconds=2e-5,
#     # Passed on the coincidence trigger.
#     conincidence_trigger_opts={
#         "trigger_type": "recstalta",
#         "thr_on": 2.5,
#         "thr_off": 2.0,
#         "thr_coincidence_sum": 2,
#         # The time windows are given in seconds.
#         "sta": 1.0 / 200000.0 * 70,
#         "lta": 1.0 / 200000.0 * 700,
#         "trigger_off_extension": 0.01,
#         "details": True,
#     },
# )

# logger.info(
#     f"Found {len(detected_events)} event candidates in interval "
#     f"{interval_start}-{interval_end}."
# )
#
# if not detected_events:
#     continue

# # Now loop over the detected events.
# added_event_count = 0
# all_channels = sorted(project.channels.keys())

# for event_candidate in detected_events:
#     # Get the waveforms for the event processing. Note that this could
#     # use the same channels as for the initial trigger or different ones.
#     st_event = project.waveforms.get_waveforms(
#         # All but the first because that is the active triggering channel
#         # here.
#         channel_ids=[
#             "XB.01.01.001",
#             "XB.01.02.001",
#             "XB.01.03.001",
#             "XB.01.04.001",
#             "XB.01.05.001",
#             "XB.01.06.001",
#             "XB.01.07.001",
#             "XB.01.08.001",
#         ],
#         start_time=event_candidate["time"] - 5e-3,
#         end_time=event_candidate["time"] + 35e-3,
#     )
#
#     # Optionally remove the instrument response if necessary.
#     # Requires StationXML files where this is possible.
#     # st_event.remove_response(inventory=project.inventory, output="VEL")
#
#     st_window = 70
#     lt_window = 700
#     tr_on = 3.5
#     tr_off = 2.0
#
#     picks = dug_picker(
#         st=st_event,
#         pick_algorithm="sta_lta",
#         picker_opts={
#             # Here given as samples.
#             "st_window": st_window,
#             "lt_window": lt_window,
#             "threshold_on": tr_on,
#             "threshold_off": tr_off,
#         },
#     )
#
#     # We want at least three picks, otherwise we don't designate it an event.
#     if len(picks) < 3:
#         # Optionally save the picks to the database as unassociated picks.
#         # if picks:
#         #    project.db.add_object(picks)
#         continue
#
#     # refine recSTA/LTA picks here
#     st_event_copy = st_event.copy()
#     win_pre = 0.0025
#     win_post = 0.0025
#     for index, pick in enumerate(picks):
#         trace_1 = st_event_copy.select(id=pick.waveform_id.id)[0]
#         trace_1 = trace_1.trim(
#             starttime=pick.time - win_pre, endtime=pick.time + win_post
#         )
#
#         recobj = REC(trace_1)
#         recobj.work()
#         idx_REC = recobj.get_pick_index()
#         pt = recobj.get_pick()
#         # only take refined pick when delta below 0.8 * window pre STA/LTA pick
#         if np.abs(picks[index].time - pt) <= 0.8 * win_pre:
#             picks[index].time = pt
#
#     # locate event
#     event = locate_in_homogeneous_background_medium(
#         picks=picks,
#         coordinates=project.cartesian_coordinates,
#         velocity=5400.0,
#         damping=0.01,
#         local_to_global_coordinates=project.local_to_global_coordinates,
#     )
#
#     # Write the classification as a comment.
#     event.comments = [
#         obspy.core.event.Comment(
#             text=f"Classification: {event_candidate['classification']}"
#         )
#     ]
#
#     # Could optionally do a QA step here.
#     if event.origins[0].time_errors.uncertainty > 5e-4:
#         logger.info(
#             "Rejected event. Time error too large: "
#             f"{event.origins[0].time_errors.uncertainty}"
#         )
#         continue
#
#     # Add the event to the project.
#     # event.write("out.xml", format="quakeml", validate=True) # validate current event quakeml
#     added_event_count += 1
#     project.db.add_object(event)
# logger.info(
#     f"Successfully located {added_event_count} of "
#     f"{len(detected_events)} event(s)."
# )
# total_event_count += added_event_count

# logger.info("DONE.")
# logger.info(f"Found {total_event_count} events.")

# Possibly dump the database as a list of quakeml files.
# project.db.dump_as_quakeml_files(folder="quakeml")
