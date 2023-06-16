'''
This module is used to calculate the discrete Fourier transform, normalize the result of this transformation and plot the result on a graph (the graph is plotted if necessary).
The discrete Fourier transform is calculated for a signal stored in a file with the extension ".wav". If necessary, the discrete Fourier transform graph will be displayed on the screen and saved to a file with the extension ".png".
''' 

import numpy as np

import wave
import cmath

import time # Used to calculate the time spent on DFT

import building_a_fourier_transform_graph

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def fourier_transform(path_to_signal = "../data/input_signal.wav", need_to_plot = False):

    '''
    This function allows you to calculate the discrete Fourier transform for a signal from a file with the extension ".wav", normalize the result of this transformation and plot the result on a graph (the graph is plotted if necessary).
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

        to_track_progress = int(index_Nyquist_frequency/10)
        progress = 0

        FT = np.zeros(shape=index_Nyquist_frequency, dtype=np.complex128) # Declaring an array for the Fourier transform

        print(f"Info about Fourier transform:")
        print(f"\tSampling rate = {RATE}")
        print(f"\tNyquist frequency = {Nyquist_frequency}")
        print(f"\tRequired number of iterations for the Fourier transform = {index_Nyquist_frequency}")

        print(f"The beginning of the calculation of the discrete Fourier transform.")
        print(f"DFT progress: {progress}% \t Iteration: {0}\{index_Nyquist_frequency}")
        start_time = time.time() # Starting the stopwatch

        # Discrete Fourier transform (DFT)
        for i in range(index_Nyquist_frequency):
            if i==to_track_progress and progress < 90:
                progress +=10
                print(f"DFT progress: {progress}% \t Iteration: {to_track_progress}\{index_Nyquist_frequency}")
                to_track_progress += int(index_Nyquist_frequency/10)
            for j in range(N_FRAMES):
                FT[i] += data_signal[j] * (cmath.cos((2*cmath.pi*i*j)/N_FRAMES)-1j*cmath.sin((2*cmath.pi*i*j)/N_FRAMES)) 
    
        end_time = time.time() - start_time # Stopping the stopwatch
        print(f"DFT progress: {100}% \t Iteration: {index_Nyquist_frequency}\{index_Nyquist_frequency}")
        print(f"The end of the calculation of the discrete Fourier transform. Time spent {'%.3f' % end_time} seconds.\n")
        
        amplitude = abs(FT) # Unnormalized signal amplitude
        amplitude = 2*amplitude/N_FRAMES # Normalized signal amplitude

        frequency = np.zeros(shape=index_Nyquist_frequency) # Declaring an array of frequencies of the signal spectrum
        for i in range(index_Nyquist_frequency):
            frequency[i] = i*RATE / N_FRAMES
        
        if need_to_plot == True:
            building_a_fourier_transform_graph.building_a_fourier_transform_graph(frequency, amplitude, path_to_signal) # Plotting a discrete Fourier transform

        return (FT, amplitude, frequency)

if __name__ == "__main__":
    fourier_transform()
