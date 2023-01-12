import matplotlib.pyplot as plt
import numpy as np

# Import from the DUGSeis library.
from DUGseis.dug_seis.project.project import DUGSeisProject
from DUGseis.dug_seis import util


def plot_trace(trace, ax=None, title_fig='Trace Time Series'):
    # Plot Trace Time Series
    ax = ax or plt.gca()
    ax.plot(trace.times("matplotlib"), trace, "b-")
    # ax.xaxis_date()
    # fig.autofmt_xdate()
    plt.ylabel('Amplitude')
    plt.xlabel('Time [hh:mm:ss:msec]')
    plt.title(title_fig)


def plot_amplitude_spectra(trace, ax=None, title_fig='Amplitude Spectra'):
    # Amplitude Spectra - Logarithmic Amplitude
    ax = ax or plt.gca()
    df = trace.stats.sampling_rate  # Sampling Rate
    fNy = df / 2.0  # Nyquist frequency
    trace_f = np.fft.rfft(trace) * (
                1 / df) * 2  # transform the signal into frequency domain, Amplitude scaling by dt and by 2 for
    # one-sided spectra
    # frame1 = plt.gca()
    # frame1.axes.get_xaxis().set_visible(False)
    # frame1.axes.get_yaxis().set_visible(False)
    freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
    ax.plot(freq, abs(trace_f), 'k', label="Original frequencies")
    plt.ylabel('Amplitude')
    plt.yscale('log')
    plt.title(title_fig)


def plot_trace_with_spectra(trace):
    # Plot Trace Time Series
    fig = plt.figure()
    ax = fig.add_subplot(3, 1, 1)
    ax.plot(trace.times("matplotlib"), trace, "b-")
    # ax.xaxis_date()
    # fig.autofmt_xdate()
    plt.ylabel('Amplitude')
    plt.xlabel('Time [hh:mm:ss:msec]')
    plt.suptitle('Trace with Amplitude and Phase Spectra')
    plt.title('Trace Time Series')

    # Amplitude and Phase Spectra - Logarithmic Amplitude
    df = trace.stats.sampling_rate  # Sampling Rate
    fNy = df / 2.0  # Nyquist frequency
    trace_f = np.fft.rfft(trace) * (
                1 / df) * 2  # transform the signal into frequency domain, Amplitude scaling by dt and
    # by 2 for one-sided spectra
    # frame1 = plt.gca()
    # frame1.axes.get_xaxis().set_visible(False)
    # frame1.axes.get_yaxis().set_visible(False)
    ax_amp_sp = fig.add_subplot(3, 1, 2)
    freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
    ax_amp_sp.plot(freq, abs(trace_f), 'k', label="Original frequencies")
    plt.ylabel('Amplitude')
    plt.yscale('log')
    plt.title('Amplitude Spectra')

    ax_ph_sp = fig.add_subplot(3, 1, 3)
    ax_ph_sp.plot(freq, np.angle(trace_f), 'r')
    plt.ylabel('Phase')
    plt.xlabel('Frequency [Hz]')
    plt.title('Phase Spectra')
    plt.show()


def filter_frequency_lowpass_and_display(trace):
    fig, axs = plt.subplots(nrows=4, ncols=1)
    plot_trace(trace, axs[0], 'Trace before filtering')
    plot_trace(trace, axs[2], 'Amplitude Spectra before filtering')
    trace.filter("lowpass", freq=2000, corners=2)
    plot_trace(trace, axs[1], 'Trace after filtering')
    plot_trace(trace, axs[3], 'Amplitude Spectra after filtering')

def trim_trace_and_display(trace, start_time, end_time):
    fig, axs = plt.subplots(nrows=2, ncols=1)
    plot_trace(trace, axs[0], 'Trace before trimming')
    trace.trim(start_time, end_time)
    plot_trace(trace, axs[1], 'Trace after trimming')
