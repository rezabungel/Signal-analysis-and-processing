'''
This module is used for plotting the graph of discrete Fourier transform.
The data for plotting the graph is passed from the functions "fourier_transform" or "fourier_transform_in_parallel", so they don't need to be validated for correctness.
The discrete Fourier transform graph will be displayed on the screen and saved to a file with the extension ".png".
'''

import numpy as np
import matplotlib.pyplot as plt

def building_a_fourier_transform_graph(frequency, amplitude, path_to_signal="../data/input_signal.wav"):
    
    '''
    This function allows you to plot the graph of the discrete Fourier transform.
    The following parameters are passed to the function:
        frequency ("numpy.ndarray" with dtype unequal "numpy.float64") - signal frequency data;
        amplitude ("numpy.ndarray" with dtype unequal "numpy.float64") - signal amplitude data;
        path_to_signal ("str") - the path where the file is stored and its name with the extension ".wav". (example: "../the_path_where_the_file_is_stored/file_name.wav").
    The result of the function:
        The discrete Fourier transform graph will be shown on the screen;
        The discrete Fourier transform graph will be saved in a file with the extension ".png". The save path will be taken from the path_to_signal parameter with the name of the saved file changed. (note: "fourier_transform_graph_" will be added before the file name and the extension will be changed from ".wav" to ".png"). (example: "../the_path_where_the_file_is_stored/fourier_transform_graph_file_name.png").
    '''

    # Preparing the name of the discrete Fourier transform graph and the path to save the discrete Fourier transform graph.
    name_fourier_transform_graph = "fourier_transform_graph_" + path_to_signal.split(r'/')[-1].split(r'.')[0] # "fourier_transform_graph_" + file name without extension
    path_to_save_fourier_transform_graph = "/".join(path_to_signal.split(r'/')[0: -1]) + "/" + name_fourier_transform_graph + ".png" # path to save the graph + "/" + name_fourier_transform_graph + extension
    
    # Preparing the name of the graph for the graph title.
    name_fourier_transform_graph = name_fourier_transform_graph.split('_')
    name_fourier_transform_graph[0] = name_fourier_transform_graph[0].capitalize()
    name_fourier_transform_graph = " ".join(name_fourier_transform_graph)

    # Plotting the discrete Fourier transform graph
    plt.stem(frequency, amplitude)
    plt.title(name_fourier_transform_graph)
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.grid(alpha=0.1)
    plt.savefig(path_to_save_fourier_transform_graph)
    plt.show()

if __name__ == "__main__":
    frequency = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
    amplitude = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]
    path_to_signal = "../data/test.wav"
    
    building_a_fourier_transform_graph(frequency, amplitude, path_to_signal)
