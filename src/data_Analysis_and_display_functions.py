import matplotlib.pyplot as plt
import numpy as np

# Import from the DUGSeis library.
from DUGseis.dug_seis.project.project import DUGSeisProject
from DUGseis.dug_seis import util


# plot_trace does not return fig, but called from a fig axis
def plot_trace(trace, ax=None, title_fig='Trace Time Series'):
    # Plot Trace Time Series
    ax = ax or plt.gca()
    fig, = ax.plot(trace.times("matplotlib"), trace, "b-")
    ax.xaxis_date()
    ax.figure.autofmt_xdate()
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.title(title_fig)
    return fig


# def plot_trace(trace, ax=None, title_fig='Trace Time Series'):
#     # Plot Trace Time Series
#     ax = ax or plt.gca()
#     fig, = ax.plot(trace.times("matplotlib"), trace, "b-")
#     ax.xaxis_date()
#     plt.figure.autofmt_xdate()
#     plt.ylabel('Amplitude')
#     plt.xlabel('Time [hh:mm:ss:msec]')
#     plt.title(title_fig)
#     plt.show()


# plot_amplitude_spectra does not return fig, but called from a fig axis
# def plot_amplitude_spectra(trace, ax=None, title_fig='Amplitude Spectra'):
#     # Amplitude Spectra - Logarithmic Amplitude
#     ax = ax or plt.gca()
#     df = trace.stats.sampling_rate  # Sampling Rate
#     fNy = df / 2.0  # Nyquist frequency
#     trace_f = np.fft.rfft(trace) * (
#             1 / df) * 2  # transform the signal into frequency domain, Amplitude scaling by dt and by 2 for
#     # one-sided spectra
#     freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
#     fig, = ax.plot(freq, abs(trace_f), 'k', label="Original frequencies")
#     plt.ylabel('Amplitude')
#     plt.yscale('log')
#     plt.title(title_fig)
#     plt.show()

def plot_amplitude_spectra(trace, ax=None, title_fig='Amplitude Spectra'):
    # Amplitude Spectra - Logarithmic Amplitude
    ax = ax or plt.gca()
    df = trace.stats.sampling_rate  # Sampling Rate
    fNy = df / 2.0  # Nyquist frequency
    trace_f = np.fft.rfft(trace) * (
            1 / df) * 2  # transform the signal into frequency domain, Amplitude scaling by dt and by 2 for
    # one-sided spectra
    freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
    fig, = ax.plot(freq, abs(trace_f), 'k', label="Original frequencies")
    plt.ylabel('Amplitude')
    plt.yscale('log')
    plt.title(title_fig)
    return fig


def plot_trace_with_spectra(trace):
    # Plot Trace Time Series
    fig = plt.figure(figsize=(10, 15))
    ax = fig.add_subplot(3, 1, 1)
    ax.plot(trace.times("matplotlib"), trace, "b-")
    ax.xaxis_date()
    fig.autofmt_xdate()
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
    ax_amp_sp = fig.add_subplot(3, 1, 2)
    freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
    ax_amp_sp.plot(freq, abs(trace_f), 'k', label="Original frequencies")
    plt.ylabel('Amplitude(log)')
    plt.yscale('log')
    plt.title('Amplitude Spectra')

    ax_ph_sp = fig.add_subplot(3, 1, 3)
    ax_ph_sp.plot(freq, np.angle(trace_f), 'r')
    plt.ylabel('Phase')
    plt.xlabel('Frequency [Hz]')
    plt.title('Phase Spectra')
    plt.tight_layout()
    plt.show()


def nextpow2(N):
    """ Function for finding the next power of 2 """
    n = 1
    while n < N: n *= 2
    return n


def plot_trace_with_spectra_hann(trace):
    # Plot Trace Time Series
    fig = plt.figure(figsize=(10, 15))
    ax = fig.add_subplot(3, 1, 1)
    ax.plot(trace.times("matplotlib"), trace, "b-")
    ax.xaxis_date()
    fig.autofmt_xdate()
    plt.ylabel('Amplitude')
    plt.xlabel('Time [hh:mm:ss:msec]')
    plt.suptitle('Trace with Amplitude and Phase Spectra')
    plt.title('Trace Time Series')

    sampling_rate = trace.stats.sampling_rate
    pad = 2
    trace = trace - np.mean(trace)  # detrend
    hann = np.hanning(len(trace))
    total_length_signal = nextpow2(len(trace) * pad)
    trace_fft = np.fft.fft(trace * hann, n=total_length_signal)
    trace_fft = trace_fft[0:int(total_length_signal / 2 + 1)]
    trace_fft = trace_fft / len(trace)  # normalise
    trace_fft[1:-1] = trace_fft[1:-1] * 2  # single sided, that is why times two
    freq = np.arange(0, sampling_rate / 2 + sampling_rate / total_length_signal, sampling_rate / total_length_signal)
    ax_amp_sp = fig.add_subplot(3, 1, 2)
    ax_amp_sp.plot(freq, abs(trace_fft), 'k', label="Original frequencies")
    plt.ylabel('Amplitude(log)')
    plt.yscale('log')
    plt.title('Amplitude Spectra')

    ax_ph_sp = fig.add_subplot(3, 1, 3)
    ax_ph_sp.plot(freq, np.angle(trace_fft), 'r')
    plt.ylabel('Phase')
    plt.xlabel('Frequency [Hz]')
    plt.title('Phase Spectra')
    plt.tight_layout()
    plt.show()

def filter_frequency_lowpass_and_display(trace):
    # Plot Trace Time Series
    # fig = plt.figure(figsize=(10, 15))
    fig = plt.figure()
    ax = fig.add_subplot(4, 1, 1)
    ax.plot(trace.times("matplotlib"), trace, "b-")
    ax.xaxis_date()
    fig.autofmt_xdate()
    plt.ylabel('Amplitude')
    # plt.xlabel('Time [hh:mm:ss:msec]')
    plt.title('Trace before filtering')

    # Filter Trace
    trace_filter = trace.filter("lowpass", freq=5000, corners=2)

    # Plot Trace Time Series
    ax = fig.add_subplot(4, 1, 2)
    ax.plot(trace_filter.times("matplotlib"), trace_filter, "b-")
    ax.xaxis_date()
    fig.autofmt_xdate()
    plt.ylabel('Amplitude')
    plt.xlabel('Time [hh:mm:ss:msec]')
    plt.title('Trace after filtering')

    # Amplitude Spectra - Logarithmic Amplitude
    df = trace.stats.sampling_rate  # Sampling Rate
    fNy = df / 2.0  # Nyquist frequency
    trace_f = np.fft.rfft(trace) * (
            1 / df) * 2  # transform the signal into frequency domain, Amplitude scaling by dt and
    # by 2 for one-sided spectra
    ax_amp_sp = fig.add_subplot(4, 1, 3)
    freq = np.linspace(0, fNy, len(trace_f))  # frequency axis for plotting
    ax_amp_sp.plot(freq, abs(trace_f), 'k', label="Original frequencies")
    plt.ylabel('Amplitude(log)')
    plt.yscale('log')
    plt.title('Amplitude Spectra before filtering')

        # Amplitude Spectra - Logarithmic Amplitude
    df = trace_filter.stats.sampling_rate  # Sampling Rate
    fNy = df / 2.0  # Nyquist frequency
    trace_filter_f = np.fft.rfft(trace_filter) * (
            1 / df) * 2  # transform the signal into frequency domain, Amplitude scaling by dt and
    # by 2 for one-sided spectra
    ax_amp_sp = fig.add_subplot(4, 1, 4)
    freq = np.linspace(0, fNy, len(trace_filter_f))  # frequency axis for plotting
    ax_amp_sp.plot(freq, abs(trace_filter_f), 'k', label="Original frequencies")
    plt.ylabel('Amplitude(log)')
    plt.yscale('log')
    plt.title('Amplitude Spectra after filtering')
    plt.tight_layout()
    plt.show()
    return trace_filter

# def filter_frequency_lowpass_and_display(trace):
#     fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(6, 10))
#     plot_trace(trace, axs[0], 'Trace before filtering')
#     trace_filter = trace.filter("lowpass", freq=2000, corners=2)
#     plot_trace(trace_filter, axs[1], 'Trace after filtering')
#     plot_amplitude_spectra(trace, axs[2], 'Amplitude Spectra before filtering')
#     plot_amplitude_spectra(trace_filter, axs[3], 'Amplitude Spectra after filtering')
#     # plt.tight_layout()
#     plt.show()


def trim_trace_and_display(trace, start_time, end_time):
    fig, axs = plt.subplots(nrows=2, ncols=1)
    plot_trace(trace, axs[0, 0], 'Trace before trimming')
    trace.trim(start_time, end_time)
    plot_trace(trace, axs[1, 0], 'Trace after trimming')
    plt.tight_layout()  # makes that labels etc. fit nicely
    plt.show()

def compute_and_overlay_amplitude_spectra(trace1, title1, trace2, title2):
    df1 = trace1.stats.sampling_rate  # Sampling Rate
    df2 = trace2.stats.sampling_rate  # Sampling Rate
    fNy1 = df1 / 2.0  # Nyquist frequency
    fNy2 = df2 / 2.0  # Nyquist frequency
    trace_f1 = np.fft.rfft(trace1) * (
            1 / df1) * 2  # transform the signal into frequency domain, Amplitude scaling by dt and
    # by 2 for one-sided spectra
    trace_f2 = np.fft.rfft(trace2) * (
            1 / df2) * 2  # transform the signal into frequency domain, Amplitude scaling by dt and
    # by 2 for one-sided spectra
    freq1 = np.linspace(0, fNy1, len(trace_f1))  # frequency axis for plotting
    plt.plot(freq1, abs(trace_f1), 'k', label="With Event")
    freq2 = np.linspace(0, fNy2, len(trace_f2))  # frequency axis for plotting
    plt.plot(freq2, abs(trace_f2), 'r', label="Without Event")
    plt.legend([title1, title2])
    plt.ylabel('Amplitude(log)')
    plt.xlabel('Frequency')
    plt.yscale('log')
    plt.title('Amplitude Spectra Overlay')
    plt.show()

def amplitude_phase_spectra_overlay(trace1, title1, trace2, title2):
    sampling_rate1 = trace1.stats.sampling_rate
    pad = 2
    trace1 = trace1 - np.mean(trace1)  # detrend
    trace2 = trace2 - np.mean(trace2)  # detrend
    hann = np.hanning(len(trace1))
    total_length_signal = nextpow2(len(trace1) * pad)
    trace1_fft = np.fft.fft(trace1 * hann, n=total_length_signal)
    trace1_fft = trace1_fft[0:int(total_length_signal / 2 + 1)]
    trace1_fft = trace1_fft / len(trace1)  # normalise
    trace1_fft[1:-1] = trace1_fft[1:-1] * 2  # single sided, that is why times two
    trace2_fft = np.fft.fft(trace2 * hann, n=total_length_signal)
    trace2_fft = trace2_fft[0:int(total_length_signal / 2 + 1)]
    trace2_fft = trace2_fft / len(trace2)  # normalise
    trace2_fft[1:-1] = trace2_fft[1:-1] * 2  # single sided, that is why times two
    freq1 = np.arange(0, sampling_rate1 / 2 + sampling_rate1 / total_length_signal, sampling_rate1 / total_length_signal)
    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(freq1, abs(trace1_fft), 'k', label="With Event")
    ax1.plot(freq1, abs(trace2_fft), 'r', label="Without Event")
    plt.legend([title1, title2])
    plt.ylabel('Amplitude (log)')
    # plt.ylabel('Amplitude')
    plt.xlabel('Frequency')
    plt.yscale('log')
    plt.title('Amplitude Spectra Overlay')
    ax_2 = fig.add_subplot(2, 1, 2)
    ax_2.plot(freq1, np.angle(trace1_fft), 'k', label="With Event")
    ax_2.plot(freq1, np.angle(trace2_fft), 'r', label="Without Event")
    plt.legend([title1, title2])
    plt.ylabel('Phase')
    plt.xlabel('Frequency [Hz]')
    plt.title('Phase Spectra')
    plt.tight_layout()
    plt.show()

def trace_amplitude_phase_spectra_overlay(trace1, title1, trace2, title2):
    fig = plt.figure(figsize=(20, 15))
    ax1 = fig.add_subplot(3, 1, 1)
    ax1.plot(trace1.times("matplotlib"), trace1, 'k', label="With Event")
    ax1.plot(trace2.times("matplotlib"), trace2, 'r', label="Without Event")
    plt.legend([title1, title2])
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.title('Trace Time Series')
    sampling_rate1 = trace1.stats.sampling_rate
    sampling_rate2 = trace2.stats.sampling_rate
    pad = 2
    trace1 = trace1 - np.mean(trace1)  # detrend
    trace2 = trace2 - np.mean(trace2)  # detrend
    hann1 = np.hanning(len(trace1))
    hann2 = np.hanning(len(trace2))
    total_length_signal1 = nextpow2(len(trace1) * pad)
    trace1_fft = np.fft.fft(trace1 * hann1, n=total_length_signal1)
    trace1_fft = trace1_fft[0:int(total_length_signal1 / 2 + 1)]
    trace1_fft = trace1_fft / len(trace1)  # normalise
    trace1_fft[1:-1] = trace1_fft[1:-1] * 2  # single sided, that is why times two
    total_length_signal2 = nextpow2(len(trace2) * pad)
    trace2_fft = np.fft.fft(trace2 * hann2, n=total_length_signal2)
    trace2_fft = trace2_fft[0:int(total_length_signal2 / 2 + 1)]
    trace2_fft = trace2_fft / len(trace2)  # normalise
    trace2_fft[1:-1] = trace2_fft[1:-1] * 2  # single sided, that is why times two
    freq1 = np.arange(0, sampling_rate1 / 2 + sampling_rate1 / total_length_signal1,
                      sampling_rate1 / total_length_signal1)
    freq2 = np.arange(0, sampling_rate2 / 2 + sampling_rate2 / total_length_signal2,
                      sampling_rate2 / total_length_signal2)
    ax2 = fig.add_subplot(3, 1, 2)
    ax2.plot(freq1, abs(trace1_fft), 'k', label="With Event")
    ax2.plot(freq2, abs(trace2_fft), 'r', label="Without Event")
    plt.legend([title1, title2])
    plt.ylabel('Amplitude(log)')
    # plt.ylabel('Amplitude')
    plt.xlabel('Frequency')
    plt.yscale('log')
    plt.title('Amplitude Spectra Overlay')
    ax_3 = fig.add_subplot(3, 1, 3)
    ax_3.plot(freq1, np.angle(trace1_fft), 'k', label="With Event")
    ax_3.plot(freq2, np.angle(trace2_fft), 'r', label="Without Event")
    plt.legend([title1, title2])
    plt.ylabel('Phase')
    plt.xlabel('Frequency [Hz]')
    plt.title('Phase Spectra')
    plt.tight_layout()
    plt.show()
