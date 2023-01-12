# -------------------------------------------------------------------------
# Jonas Junker, 05.10.2021, junkerj@student.ethz.ch
# copied and adapted matlab script to python 26.4.2022
# -------------------------------------------------------------------------
# Function to compare and plot the noise introduced at the AE system at
# various pumping levels. Creates a figure with time domain samples for
# each pumping level in the left panel and a PSD plot in the right panel of
# the figure. The PSD is the median of 300 subsamples of the introduced
# length.
# -------------------------------------------------------------------------
# INPUTS:
#  - pump: Struct with the structs of the different pumping intensities
#  included.
#  - time_window: length of the subsamples in ms.
#  - pumpinglevels: string vector, describing all the used pumping levels
#  - pumpname: character vector, giving the name of the pump
#  - sensor_name: character vector, name of the sensor that is analyzed
#  (goes into the figure title and name)
# -------------------------------------------------------------------------
# OUTPUTS:
#   - Figure as described above
# -------------------------------------------------------------------------

import numpy as np


def psd_with_median(data, time_window, type_of_analysis="median", n_points=300):
    xy_list = []
    # Prepare for the FFT, create the time snippets
    Fs = 200e3     # Sampling frequency
    dt = 1/Fs  # Sampling interval
    Fnyq = 1/(2*dt)  # Nyquist frequency
    idx_windows = int(Fs*time_window)  # Indexes of data in time window

    start_idx = 0  # Index of first sample to take
    end_idx = len(data) - idx_windows - 1  # start index of last time window

    # create num_point subsamples of the data to analyze
    # n_points = 300
    idx_start = np.linspace(start_idx, end_idx, n_points)

    # Select all time snippets
    time_snippets = []
    signal_snippets = []
    signal_snippets_normalized = []
    for i in range(0, n_points):
        # take_indexes = idx_start(i):idx_start(i)+idx_windows-1
        # print(f"type(i): {type(i)}, type(idx_windows): {type(idx_windows)}")
        take_indexes = range(round(idx_start[i]), round(idx_start[i])+idx_windows)
        if len(take_indexes) != np.around(idx_windows):
            print(f"error: len(take_indexes) {len(take_indexes)} != {np.around(idx_windows)} np.around(idx_windows)")

        # time_snippets(pl,i,:) = pump(pl).time{1,1}(take_indexes)';
        if i % 20 == 0:
            print(f"{i}, ", end='')
        time_snippets.append(take_indexes)
        # signal_snippets(pl,i,:) = pump(pl).data{1,1}(take_indexes)';
        signal_snippets.append(data[take_indexes])
        # signal_snippets_normalized(pl,i,:) = signal_snippets(pl,i,:) - mean(signal_snippets(pl,i,:));
        signal_snippets_normalized.append(signal_snippets[i] - np.mean(signal_snippets[i]))
    print(".")

    # Plot the data to check if everything is loaded correctly and that the
    # snippets are evenly distributed
    """
    for i, x in enumerate(time_snippets):
        xy = {"x": time_snippets[i], "y": signal_snippets_normalized[i]}
        xy_list.append(xy)
    return xy_list
    """

    # Add the PSD of the individual snippets to the PSD plot
    signal_ps = []
    signal_ff_individual = []
    print(f"step: x/{n_points}: ")
    for i in range(0, n_points):
        L = len(signal_snippets_normalized[i])
        N = len(signal_snippets_normalized[i])
        ff_temp = np.fft.fft(signal_snippets_normalized[i])
        Nf = round(N/2)

        # pp = abs(ff_temp(1:Nf)) .* abs(ff_temp(1:Nf));
        pp = np.multiply(abs(ff_temp[0:Nf]), abs(ff_temp[0:Nf]))

        signal_ps.append(1/(N*N) * pp)  # Power spectrum of the signal
        signal_ff_individual.append(np.linspace(0, Fnyq, Nf))  # Frequency vector
        if i % 20 == 0:
            print(f"{i}, ", end='')
    print(".")
    print(f"signal_ps:{len(signal_ps)}x{len(signal_ps[0])}")
    # Calculate the Median or mean value
    if type_of_analysis == "median":
        print("median")
        signal_me_ = np.median(signal_ps, 0)
    elif type_of_analysis == "mean":
        print("mean")
        signal_me_ = np.mean(signal_ps, 0)
    else:
        print(f"psd_with_filter: something went wrong, filter: {type_of_analysis} unknown.")

    signal_ff = signal_ff_individual[0]

    print(f"x signal_ff:{len(signal_ff)}, y signal_me_:{len(signal_me_)}")
    xy = {"x": signal_ff, "y": signal_me_}
    xy_list.append(xy)
    return xy_list

    # load a single time snippet
    if True:
        take_indexes = range(0, int(time_window*Fs))  # Indexes to take
        time_snippets = take_indexes             # Create time vector
        signal_snippets = data[take_indexes]     # Create signal vector
        signal_snippets_normalized = signal_snippets - np.mean(signal_snippets)  # The mean the signal vector
        print(f"Signal mean is {np.mean(signal_snippets)}")
        N = len(signal_snippets)
        # Calculate powerspectra
        ff_temp = np.fft.fft(signal_snippets_normalized)
        Nf = round(N/2)
        pp = np.multiply(abs(ff_temp[0:Nf]), abs(ff_temp[0:Nf]))

        signal_ps = 1/(N*N) * pp  # Power spectrum of the signal
        signal_ff = np.linspace(0, Fnyq, Nf)  # Frequency vector
        print(len(signal_ps))
        print(f"Zeroth bin is {signal_ps[1]}")
