'''
This module is used to calculate the discrete Fourier transform, normalize the result of this transformation and plot the result on a graph (the graph is plotted if necessary).
The calculation of the discrete Fourier transform is parallelized into 8 cores. If there are fewer or more cores, this will not cause problems.
The discrete Fourier transform is calculated for a signal stored in a file with the extension ".wav". If necessary, the discrete Fourier transform graph will be displayed on the screen and saved to a file with the extension ".png".
''' 

import multiprocessing
import cmath
import time # Used to calculate the time spent on DFT

import numpy as np

import wave_worker
import building_a_fourier_transform_graph

def DFT(index_start, index_stop, N_FRAMES, data_signal):

    '''
    This function is used to calculate the discrete Fourier transform when parallelizing calculations. (note: This function is used in conjunction with the "fourier_transform_in_parallel" function. The "DFT" function is not used separately.)
    The following parameters are passed to the function:
        index_start (dtype="numpy.uint32") - index of the beginning of the calculation; 
        index_stop (dtype="numpy.uint32") - index of the end of the calculation;
        N_FRAMES ("int") - the number of frames;
        data_signal ("numpy.ndarray" with dtype=Depends_on_SAMPLE_FORMAT) - signal data.
    The result of the function:
        Return values:
            FT ("numpy.ndarray" with dtype="numpy.complex128") - values of the discrete Fourier transform (from index_start to the index_stop).
    '''

    # Discrete Fourier transform (DFT)
    FT = np.zeros(shape=(int(N_FRAMES/2) + 1), dtype=np.complex128)
    
    for i in range(index_start, index_stop):
        precomp = 2*cmath.pi*i/N_FRAMES
        FT[i] = sum(data_signal[j] * (cmath.cos(precomp * j) - 1j * cmath.sin(precomp * j)) for j in range(N_FRAMES))
    else:
        print(f"DFT progress: +{12.5}% \t Iteration: {'%6d' % index_start} -> {'%6d' % i}\{int(N_FRAMES/2) + 1} completed.")
    
    return FT

def fourier_transform_in_parallel(path_to_signal = "../data/input_signal.wav", need_to_plot = False):
    
    '''
    This function allows you to calculate the discrete Fourier transform (parallelizing calculations by 8 cores) for a signal from a file with the extension ".wav", normalize the result of this transformation and plot the result on a graph (the graph is plotted if necessary).
    The following parameters are passed to the function:
        path_to_signal ("str") - the path where the file is stored and its name with the extension ".wav". (example: "../the_path_where_the_file_is_stored/file_name.wav");
        need_to_plot ("bool") - if "True", the "building_a_fourier_transform_graph" function will be called, if "False", the "building_a_fourier_transform_graph" function will not be called. The function "building_a_fourier_transform_graph" plots the graph of the discrete Fourier transform.
    The result of the function:
        Return values:
            FT ("numpy.ndarray" with dtype="numpy.complex128") - values of the discrete Fourier transform (from 0 to the Nyquist frequency);
            amplitude ("numpy.ndarray" with dtype="numpy.float64") - signal amplitude;
            frequency ("numpy.ndarray" with dtype="numpy.float64") - signal frequency in hertz.
        Discrete Fourier transform graph (if "need_to_plot" = True):
            Please refer to the result of the "building_a_fourier_transform_graph" function implemented in the "building_a_fourier_transform_graph.py" file.
    '''

    # Checking for the correctness of the input data
    if type(path_to_signal) != str or '.wav' not in path_to_signal:
        path_to_signal = "../data/input_signal.wav"
        print(f'The path to the signal for fourier_transform_in_parallel is specified incorrectly. The default value is set:\n\t path_to_signal = "{path_to_signal}"')
    else:
        path_to_signal = "./" + path_to_signal

    if type(need_to_plot) != bool:
        need_to_plot = False
        print(f'The boolean key value "need_to_plot" is specified incorrectly. The default value is set:\n\t need_to_plot = "{need_to_plot}"')

    data_signal, N_FRAMES, RATE, CHANNELS, SAMPLE_FORMAT = wave_worker.wave_read(path_to_signal)

    # One of the properties of the discrete Fourier transform: symmetry with respect to the Nyquist frequency (the rule applies to a real signal).
    # We will consider the Fourier transform from 0 to the Nyquist frequency, and not from 0 to the Sampling frequency. 
    # To get the Fourier transform from 0 to the Sampling frequency, you need to mirror image the complex conjugate numbers from the Fourier transform starting from the first element to the penultimate element.
    Nyquist_frequency = int(RATE/2)
    index_Nyquist_frequency = int(N_FRAMES/2) + 1

    FT = np.zeros(shape=index_Nyquist_frequency, dtype=np.complex128) # Declaring an array for the Fourier transform

    print(f"Info about Fourier transform:")
    print(f"\tSampling rate = {RATE}")
    print(f"\tNyquist frequency = {Nyquist_frequency}")
    print(f"\tRequired number of iterations for the Fourier transform = {index_Nyquist_frequency}")

    print(f"The beginning of the calculation of the discrete Fourier transform.")
    print(f"DFT progress: {0}% \t Iteration: {0}\{index_Nyquist_frequency}")
    start_time = time.time() # Starting the stopwatch

    # Creating calculation intervals for each core
    step = int(index_Nyquist_frequency/8)
    interval = np.zeros(9, dtype=np.uint32)
    interval[0] = 0
    for i in range(1, 8):
        interval[i] = interval[i-1] + step
    interval[8] = index_Nyquist_frequency

    # Parallelization of DFT calculation on 8 cores. (If there are fewer or more cores, this is not a problem)
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        temp = p.starmap(DFT, [(interval[0], interval[1], N_FRAMES, data_signal),
                                (interval[1], interval[2], N_FRAMES, data_signal),
                                (interval[2], interval[3], N_FRAMES, data_signal),
                                (interval[3], interval[4], N_FRAMES, data_signal),
                                (interval[4], interval[5], N_FRAMES, data_signal),
                                (interval[5], interval[6], N_FRAMES, data_signal),
                                (interval[6], interval[7], N_FRAMES, data_signal),
                                (interval[7], interval[8], N_FRAMES, data_signal)])

    # Assembling data from a parallel computation into a single data array
    for i in range(len(interval)-1):
        for j in range(interval[i], interval[i+1]):
            FT[j]=temp[i][j]

    end_time = time.time() - start_time # Stopping the stopwatch
    print(f"DFT progress: {100}% \t Iteration: {index_Nyquist_frequency}\{index_Nyquist_frequency}")
    print(f"The end of the calculation of the discrete Fourier transform. Time spent {'%.3f' % end_time} seconds.\n")

    amplitude = abs(FT) # Unnormalized signal amplitude
    amplitude = 2*amplitude/N_FRAMES # Normalized signal amplitude

    # Declaring an array of frequencies of the signal spectrum
    frequency = np.arange(index_Nyquist_frequency) * RATE / N_FRAMES

    if need_to_plot == True:
        building_a_fourier_transform_graph.building_a_fourier_transform_graph(frequency, amplitude, path_to_signal) # Plotting a discrete Fourier transform

    return (FT, amplitude, frequency)

if __name__ == "__main__":
    multiprocessing.freeze_support() # Enable support for multiprocessing
    fourier_transform_in_parallel()
