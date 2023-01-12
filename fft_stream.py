import numpy as np
from obspy.core import Stream, Trace


def fft_all_traces(stream, averages=1):
    xy_list = []
    for i, tr in enumerate(stream.traces):
        xy_list.append(fft_stream(stream, i, averages))
    return xy_list


def fft_stream(stream, trace_nr, averages=1):
    # obspy.signal.freqattributes(stream.traces[1])
    # obspy.signal

    # toDo: this plots but freezes. needed?
    # stream.traces[1].spectrogram(log=True, title='BW.RJOB ' + str(stream.traces[1].stats.starttime))

    # toDo: FFT testing going on here.
    # https://www.earthinversion.com/techniques/signal-denoising-using-fast-fourier-transform/
    dt = 1/200e3
    n = len(stream.traces[trace_nr].data)
    fhat = np.fft.fft(stream.traces[trace_nr].data, n)
    psd = fhat * np.conj(fhat)/n
    freq = (1/(dt*n)) * np.arange(n)  # frequency array
    idxs_half = np.arange(1, np.floor(n/2), dtype=np.int32)  # first half index

    # return freq[idxs_half], np.abs(psd[idxs_half])
    # xy = {"x": freq[idxs_half], "y": np.abs(psd[idxs_half])}

    # toDo: moving average testing going on here.
    # https://stackoverflow.com/questions/14313510/how-to-calculate-rolling-moving-average-using-python-numpy-scipy
    ret = np.cumsum(psd)
    n = averages
    ret[n:] = ret[n:] - ret[:-n]
    psd2 = ret[n - 1:] / n

    """
    stream = Stream()
    stream += Trace(np.abs(psd2[idxs_half]))  # , header=self.stats_handling.get_stats())
    return stream
    """
    xy = {"x": freq[idxs_half], "y": np.abs(psd2[idxs_half])}
    return xy
