import numpy as np
import matplotlib.pyplot as plt

import wave
import cmath

import time # Used to calculate the time spent on DFT

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def fourier_transform(path_to_signal = "../data/input_signal.wav"):
    with wave.open(path_to_signal, 'rb') as wf:

        SAMPLE_FORMAT = wf.getsampwidth() # Sound depth
        RATE = wf.getframerate() # Sampling rate
        N_FRAMES = wf.getnframes() # The number of frames

        data_signal = np.frombuffer(wf.readframes(N_FRAMES), dtype=types[SAMPLE_FORMAT]) # Reading the signal from the file and converting bytes to int
        
        # One of the properties of the discrete Fourier transform: symmetry with respect to the Nyquist frequency (the rule applies to a real signal).
        # We will consider the Fourier transform from 0 to the Nyquist frequency, and not from 0 to the Sampling frequency. 
        # To get the Fourier transform from 0 to the Sampling frequency, you need to mirror image the Fourier transform from 0 to the Nyquist frequency.
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
        
        # Preparing a path to save the Fourier transform graph and the name of the Fourier transform graph
        path_to_save_fourier_transform_graph = list()
        name_fourier_transform_graph = list("fourier_transform_graph_")

        if path_to_signal.count('/') > 0:
            count = path_to_signal.count('/')
            stop = 0
            for i in path_to_signal:
                if stop != count:
                    if i != '/':
                        path_to_save_fourier_transform_graph.append(i)
                    else:
                        path_to_save_fourier_transform_graph.append(i)
                        stop += 1
                else:
                    if i != '.':
                        name_fourier_transform_graph.append(i)
                    else:
                        name_fourier_transform_graph.append(i + "png")
                        break
            path_to_save_fourier_transform_graph = ''.join(path_to_save_fourier_transform_graph + name_fourier_transform_graph)
        else:
            for i in path_to_signal:
                if i != '.':
                    name_fourier_transform_graph.append(i)
                else:
                    name_fourier_transform_graph.append(i + "png")
                    break
            path_to_save_fourier_transform_graph = ''.join(path_to_save_fourier_transform_graph + name_fourier_transform_graph)

        name_fourier_transform_graph.remove('.png')
        name_fourier_transform_graph[0] = "F"
        for i in range(len(name_fourier_transform_graph)):
            if name_fourier_transform_graph[i] == "_":
                name_fourier_transform_graph[i] = " "
        name_fourier_transform_graph = ''.join(name_fourier_transform_graph)

        # Plotting the Fourier transform graph
        plt.stem(frequency, amplitude)
        plt.title(name_fourier_transform_graph)
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')
        plt.grid(alpha=0.1)
        plt.savefig(path_to_save_fourier_transform_graph)
        plt.show()

        return (FT, amplitude, frequency)

if __name__ == "__main__":
    fourier_transform()
