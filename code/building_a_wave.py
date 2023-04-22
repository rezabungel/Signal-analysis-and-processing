'''
This module is used to display the waveform on the graph.
Signal from a file with the extension ".wav" will be displayed on the graph. This graph will be shown on the screen and saved to a file with the extension ".png".
'''

import numpy as np
import matplotlib.pyplot as plt

import wave

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def building_a_wave(path_to_signal = "../data/input_signal.wav"):

    '''
    This function allows you to plot the signal.
    The following parameters are passed to the function:
        path_to_signal ("str") - the path where the file is stored and its name with the extension ".wav". (example: "../the_path_where_the_file_is_stored/file_name.wav").
    The result of the function will be a plotted signal graph. This graph will be shown on the screen and saved with the extension ".png".
        The save path will be taken from the path_to_signal parameter with the name of the saved file changed. (note: "graph_" will be added before the file name and the extension will be changed from ".wav" to ".png"). (example: "../the_path_where_the_file_is_stored/graph_file_name.png").
    '''

    with wave.open(path_to_signal, 'rb') as wf:

        SAMPLE_FORMAT = wf.getsampwidth() # Sound depth
        CHANNELS = wf.getnchannels() # Number of channels
        RATE = wf.getframerate() # Sampling rate
        N_FRAMES = wf.getnframes() # The number of frames

        print(f"Info about signal:")
        print(f"\tSAMPLE_FORMAT = {SAMPLE_FORMAT}")
        print(f"\tCHANNELS = {CHANNELS}")
        print(f"\tRATE = {RATE}")
        print(f"\tN_FRAMES = {N_FRAMES}")
        print(f"\tSignal time {N_FRAMES/RATE} seconds\n")

        data_signal = np.frombuffer(wf.readframes(N_FRAMES), dtype=types[SAMPLE_FORMAT]) # Reading the signal from the file and converting bytes to int
        time = np.linspace(0.0, N_FRAMES/RATE, num=N_FRAMES) # Time for the X axis

        # Preparing a path to save the signal graph and the name of the signal graph
        path_to_save_signal_graph = list()
        name_signal_graph = list("graph_")

        if path_to_signal.count('/') > 0:
            count = path_to_signal.count('/')
            stop = 0
            for i in path_to_signal:
                if stop != count:
                    if i != '/':
                        path_to_save_signal_graph.append(i)
                    else:
                        path_to_save_signal_graph.append(i)
                        stop += 1
                else:
                    if i != '.':
                        name_signal_graph.append(i)
                    else:
                        name_signal_graph.append(i + "png")
                        break
            path_to_save_signal_graph = ''.join(path_to_save_signal_graph + name_signal_graph)
        else:
            for i in path_to_signal:
                if i != '.':
                    name_signal_graph.append(i)
                else:
                    name_signal_graph.append(i + "png")
                    break
            path_to_save_signal_graph = ''.join(path_to_save_signal_graph + name_signal_graph)

        name_signal_graph.remove('.png')
        name_signal_graph[0] = "G"
        for i in range(len(name_signal_graph)):
            if name_signal_graph[i] == "_":
                name_signal_graph[i] = " "
        name_signal_graph = ''.join(name_signal_graph)

        # Plotting the signal graph
        plt.plot(time, data_signal)
        plt.title(name_signal_graph)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.grid(alpha=0.1)
        plt.savefig(path_to_save_signal_graph)
        plt.show()


if __name__ == "__main__":
    building_a_wave()
