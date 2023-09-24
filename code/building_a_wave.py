'''
This module is used to display the waveform on the graph.
Signal from a file with the extension ".wav" will be displayed on the graph. This graph will be shown on the screen and saved to a file with the extension ".png".
'''

import numpy as np
import matplotlib.pyplot as plt

import wave_worker

def building_a_wave(path_to_signal = "../data/input_signal.wav"):

    '''
    This function allows you to plot the signal.
    The following parameters are passed to the function:
        path_to_signal ("str") - the path where the file is stored and its name with the extension ".wav". (example: "../the_path_where_the_file_is_stored/file_name.wav").
    The result of the function will be a plotted signal graph. This graph will be shown on the screen and saved with the extension ".png".
        The save path will be taken from the path_to_signal parameter with the name of the saved file changed. (note: "graph_" will be added before the file name and the extension will be changed from ".wav" to ".png"). (example: "../the_path_where_the_file_is_stored/graph_file_name.png").
    '''

    # Checking for the correctness of the input data
    if type(path_to_signal) != str or '.wav' not in path_to_signal:
        path_to_signal = "../data/input_signal.wav"
        print(f'The path to the signal for building_a_wave is specified incorrectly. The default value is set:\n\t path_to_signal = "{path_to_signal}"')
    else:
        path_to_signal = "./" + path_to_signal

    data_signal, N_FRAMES, RATE, CHANNELS, SAMPLE_FORMAT = wave_worker.wave_read(path_to_signal)

    print(f"Info about signal:")
    print(f"\tSAMPLE_FORMAT = {SAMPLE_FORMAT}")
    print(f"\tCHANNELS = {CHANNELS}")
    print(f"\tRATE = {RATE}")
    print(f"\tN_FRAMES = {N_FRAMES}")
    print(f"\tSignal time {N_FRAMES/RATE} seconds\n")

    time = np.linspace(0.0, N_FRAMES/RATE, num=N_FRAMES) # Time for the X axis

    # Preparing the name and path to save the signal graph
    name_signal_graph = "graph_" + path_to_signal.split(r'/')[-1].split(r'.')[0] # "graph_ + file name without extension
    path_to_save_signal_graph = "/".join(path_to_signal.split(r'/')[0: -1]) + "/" + name_signal_graph + ".png" # " path to save the graph + "/" + name_signal_graph + extension
    
    # Preparing the name of the graph for the graph title
    name_signal_graph = name_signal_graph.split('_')
    name_signal_graph[0] = name_signal_graph[0].capitalize()
    name_signal_graph = " ".join(name_signal_graph)

    # Plotting the signal graph
    if max(time) <= 0.1:
        # If the recording duration is less than or equal to 0.1 seconds, only one graph will be plotted, representing the entire signal.
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(14, 8))
        axes.plot(time, data_signal)
        axes.set_title(name_signal_graph, fontsize=10)
        axes.set_xlabel('Time', fontsize=10)
        axes.set_ylabel('Amplitude', fontsize=10)
        axes.grid(alpha=0.1)
    else:
        # If the recording duration is greater than 0.1 seconds, two graphs will be plotted. 
        #   The first graph will represent the entire signal, and the second graph will represent this signal in the range from 0.0 to 0.1 seconds.
        #   The graph in the range from 0.0 to 0.1 seconds is very convenient for analyzing generated signals.
        #   Note: in fact, the range will not be exactly up to 0.1 seconds, but close to it.
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 8))

        axes[0].plot(time, data_signal)
        axes[0].set_title(name_signal_graph, fontsize=10)
        axes[0].set_xlabel('Time', fontsize=10)
        axes[0].set_ylabel('Amplitude', fontsize=10)
        axes[0].grid(alpha=0.1)

        name_signal_graph += ' (in the range from 0.0 to 0.1)'
        time = time[time<0.10001]

        axes[1].plot(time, data_signal[:len(time)])
        axes[1].set_title(name_signal_graph, fontsize=10)
        axes[1].set_xlabel('Time', fontsize=10)
        axes[1].set_ylabel('Amplitude', fontsize=10)
        axes[1].grid(alpha=0.1)

    plt.subplots_adjust(hspace = 0.3)
    plt.savefig(path_to_save_signal_graph)
    plt.show()

if __name__ == "__main__":
    building_a_wave()
