'''
This module is used to calculate the discrete Fourier transform, normalize the result of this transformation and plot the result on a graph (the graph is plotted if necessary).
The discrete Fourier transform is computed using the fast Fourier transform algorithm. (note: For "fft" the amount of data must be a power of two.)
The discrete Fourier transform is calculated for a signal stored in a file with the extension ".wav". If necessary, the discrete Fourier transform graph will be displayed on the screen and saved to a file with the extension ".png".
'''

import numpy as np

import wave
import cmath

import time # Used to calculate the time spent on FFT

import building_a_fourier_transform_graph
import isPowerOfTwo

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def fft(data_signal):
    
    '''
    This function is used to calculate the discrete Fourier transform using the fast Fourier transform algorithm. (note: It is used for "fast_fourier_transform" but can also be used independently.)
    The following parameters are passed to the function:
        data_signal ("numpy.ndarray" with dtype=Depends_on_SAMPLE_FORMAT) - signal data. (note: the amount of data should be a power of two)
    The result of the function:
        Return values:
            FT ("numpy.ndarray" with dtype="numpy.complex128") - values of the discrete Fourier transform
            or
            -1 ("int") - if the amount of data is not a power of two.
    '''

    # Checking that the amount of data corresponds to a power of two.
    if not isPowerOfTwo.isPowerOfTwo(len(data_signal)):
        print(f'The amount of data does not correspond to a power of two (the "fft" function cannot be used).')
        print(f"The function terminates with a return of -1.")
        return -1

    n = len(data_signal) # n is a power of 2
    if n == 1:
        return data_signal
    omega = cmath.cos(2*cmath.pi/n) - 1j*cmath.sin(2*cmath.pi/n)
    data_signal_even, data_signal_odd = data_signal[::2], data_signal[1::2]
    y_even, y_odd = fft(data_signal_even), fft(data_signal_odd)
    FT = np.zeros(shape=n, dtype=np.complex128)
    for i in range(int(n/2)):
        FT[i] = y_even[i]+(omega**i)*y_odd[i]
        FT[i+int(n/2)] = y_even[i]-(omega**i)*y_odd[i]
    return FT

def fast_fourier_transform(path_to_signal="../data/input_signal.wav", need_to_plot=False):
    
    '''
    This function allows you to calculate the discrete Fourier transform (using the fast Fourier transform algorithm (function "fft")) for a signal from a file with the extension ".wav", normalize the result of this transformation and plot the result on a graph (the graph is plotted if necessary).
    The following parameters are passed to the function:
        path_to_signal ("str") - the path where the file is stored and its name with the extension ".wav". (example: "../the_path_where_the_file_is_stored/file_name.wav") (note: The amount of data in this file must be a power of two.);
        need_to_plot ("bool") - if "True", the "building_a_fourier_transform_graph" function will be called, if "False", the "building_a_fourier_transform_graph" function will not be called. The function "building_a_fourier_transform_graph" plots the graph of the discrete Fourier transform.
    The result of the function:
        Return values:
            FT ("numpy.ndarray" with dtype="numpy.complex128") - values of the discrete Fourier transform (from 0 to the Nyquist frequency);
            amplitude ("numpy.ndarray" with dtype="numpy.float64") - signal amplitude;
            frequency ("numpy.ndarray" with dtype="numpy.float64") - signal frequency in hertz;
            or
            -1 ("int") - if the amount of data is not a power of two.
        Discrete Fourier transform graph (if "need_to_plot" = True):
            Please refer to the result of the "building_a_fourier_transform_graph" function implemented in the "building_a_fourier_transform_graph.py" file.
    '''

    # Checking for the correctness of the input data
    if type(path_to_signal) != str or '.wav' not in path_to_signal:
        path_to_signal = "../data/input_signal.wav"
        print(f'The path to the signal for fourier_transform is specified incorrectly. The default value is set:\n\t path_to_signal = "{path_to_signal}"')
    else:
        path_to_signal = "./" + path_to_signal

    if type(need_to_plot) != bool:
        need_to_plot = False
        print(f'The boolean key value "need_to_plot" is specified incorrectly. The default value is set:\n\t need_to_plot = "{need_to_plot}"')

    with wave.open(path_to_signal, 'rb') as wf:
        SAMPLE_FORMAT = wf.getsampwidth() # Sound depth
        RATE = wf.getframerate() # Sampling rate
        N_FRAMES = wf.getnframes() # The number of frames
        data_signal = np.frombuffer(wf.readframes(N_FRAMES), dtype=types[SAMPLE_FORMAT]) # Reading the signal from the file and converting bytes to int

    # One of the properties of the discrete Fourier transform: symmetry with respect to the Nyquist frequency (the rule applies to a real signal).
    # We will consider the Fourier transform from 0 to the Nyquist frequency, and not from 0 to the Sampling frequency.
    # To get the Fourier transform from 0 to the Sampling frequency, you need to mirror image the complex conjugate numbers from the Fourier transform starting from the first element to the penultimate element.
    Nyquist_frequency = int(RATE/2)
    index_Nyquist_frequency = int(N_FRAMES/2) + 1

    print(f"Info about Fourier transform:")
    print(f"\tSampling rate = {RATE}")
    print(f"\tNyquist frequency = {Nyquist_frequency}")

    print(f"The beginning of the calculation of the fast Fourier transform.")
    print(f"FFT progress...")
    start_time = time.time() # Starting the stopwatch

    FT = fft(data_signal)

    if type(FT) == int:
        return -1

    FT = FT[:index_Nyquist_frequency]

    end_time = time.time() - start_time # Stopping the stopwatch
    print(f"The end of the calculation of the fast Fourier transform. Time spent {'%.3f' % end_time} seconds.\n")

    amplitude = abs(FT) # Unnormalized signal amplitude
    amplitude = 2*amplitude/N_FRAMES # Normalized signal amplitude

    # Declaring an array of frequencies of the signal spectrum
    frequency = np.arange(index_Nyquist_frequency) * RATE / N_FRAMES

    if need_to_plot == True:
        building_a_fourier_transform_graph.building_a_fourier_transform_graph(frequency, amplitude, path_to_signal) # Plotting a discrete Fourier transform

    return (FT, amplitude, frequency)

if __name__ == "__main__":
    fast_fourier_transform()
    fft([1, 2, 3, 4, 5, 6, 7, 8])
