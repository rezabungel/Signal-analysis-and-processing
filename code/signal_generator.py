'''
This module is used for generating signals and recording them into a file with a ".wav" extension.
Generation is done through combinations of sinusoids with specified frequencies.
'''

import math

import numpy as np

import wave_worker
import isPowerOfTwo

def note(frequency): # y = sin(2*math.pi*frequency*x)

    '''
    This function is used to define a sine wave of the form sin(2*pi*frequency*x).
    The following parameters are passed to the function:
        frequency ("int" or "float") - the frequency of the sine wave.
    The result of the function:
        Return values:
            The lambda function is math.sin(2*math.pi*frequency*x), where the lambda function takes a parameter x.
    
    For example, when 440 Hz is passed, it returns a lambda function representing the musical note A.
    '''

    return lambda x: math.sin(2*math.pi*frequency*x) 

def signal_generator_sum(FILENAME = "../data/generated_signal_sum.wav", SECONDS = 5.0, RATE = 44100, FREQUENCIES = None):

    '''
    This function allows you to generate a signal composed of a sum of sinusoids with specified frequencies and save it to a file.
    The following parameters are passed to the function:
        FILENAME ("str") - path to save the file and its name with ".wav" extension. (example: "../the_path_to_save_the_file/name_of_the_saved_file.wav");
        SECONDS ("float" and greater than 0) - recording duration of the generated signal in seconds (note: The "int" type is supported, it will be cast to the "float" type.);
        RATE ("int" and greater than 0) - sampling rate in hertz (note: 44100 hertz is the standard CD quality.);
        FREQUENCIES ("list" or "tuple" with elements of "int" or "float" (may use a combination of "int" and "float")) - collection of frequencies that will be used for generating sine waves of the form sin(2*pi*frequency*x).
    The result of the function will be a recorded generated signal (where the generated signal is the sum of sinusoids with different frequencies, i.e., sin(...) + sin(...) + ...) and saved in accordance with the passed parameters.
    '''

    print(f"Signal generation from the given frequencies has started.")

    # Checking for the correctness of the input data
    if type(FILENAME) != str or '.wav' not in FILENAME:
        FILENAME = "../data/generated_signal_sum.wav"
        print(f'The filename for recording the generated signal is set incorrectly. The default value is set:\n\t FILENAME = "{FILENAME}"')
    else:
        FILENAME = "./" + FILENAME

    if type(SECONDS) == int and SECONDS > 0:
        SECONDS = float(SECONDS)
    elif type(SECONDS) != float or SECONDS <= 0:
        SECONDS = 5.0
        print(f'The recording duration of the generated signal is set incorrectly. The default value is set:\n\t SECONDS = {SECONDS}')
    SECONDS = round(SECONDS, 2)

    if type(RATE) != int or RATE <= 0:
        RATE = 44100
        print(f'The sampling rate is set incorrectly. The default value is set:\n\t RATE = {RATE}')

    if type(FREQUENCIES) == list or type(FREQUENCIES) == tuple:
        if len(FREQUENCIES) == 0:
            FREQUENCIES = (440, 556, 659)
            print(f'The frequencies are set incorrectly. The number of elements in frequencies should be greater than 0. The default value is set:\n\t FREQUENCIES = {FREQUENCIES}')
        elif not all(True if type(frequency) == int or type(frequency) == float else False for frequency in FREQUENCIES):
            FREQUENCIES = (440, 556, 659)
            print(f'The frequencies are set incorrectly. The elements in the collection can be either int or float, or a mix of both. The default value is set:\n\t FREQUENCIES = {FREQUENCIES}')
    else:
        print(f'The frequencies are set incorrectly. Frequencies is of type {type(FREQUENCIES)}, but it should be a list or tuple.', end=' ')
        FREQUENCIES = (440, 556, 659)
        print(f'The default value is set:\n\t FREQUENCIES = {FREQUENCIES}')

    CHUNK = 1024 # The number of frames per one "request" to the microphone -> It is used here for the correct operation of the `isPowerOfTwo_DataVolume` function.
    CHANNELS = 1 # The number of audio tracks -> It is used here for the correct operation of the `wave_write` function.

    # Checking if the volume of recorded data matches a power of two. (If it doesn't match, it can be corrected by changing the recording duration.)
    SECONDS = isPowerOfTwo.isPowerOfTwo_DataVolume(SECONDS, RATE, CHUNK)
    
    time = np.linspace(0, SECONDS, int(RATE / CHUNK * SECONDS)*CHUNK)
    data_signal = np.zeros(shape=time.size)

    for frequency in FREQUENCIES:
        musical_note = note(frequency)
        data_signal += np.array([musical_note(t) for t in time])

    # Normalize the signal data
    data_signal /= np.max(np.abs(data_signal))

    # Scaling audio data to 16-bit format: Multiplying by 32767 and converting to the np.int16 type.
    data_signal *= 32767 # 32767 is the maximum value that can be represented in the np.int16 format, which is used for audio signals.
    data_signal = data_signal.astype(np.int16)

    # Converting int to bytes for further writing to the ".wav" file.
    frames = data_signal.tobytes()

    # Save the generated data in a WAV file
    wave_worker.wave_write(FILENAME, frames, RATE, CHANNELS)

    print(f'Finished signal generation. The signal is saved in the "{FILENAME}" file!\n')


def signal_generator_sequence(FILENAME = "../data/generated_signal_sequence.wav", SECONDS = 5.0, RATE = 44100, FREQUENCIES = None):

    '''
    This function allows you to generate a signal composed of a sequence of sinusoids with specified frequencies and save it to a file.
    The following parameters are passed to the function:
        FILENAME ("str") - path to save the file and its name with ".wav" extension. (example: "../the_path_to_save_the_file/name_of_the_saved_file.wav");
        SECONDS ("float" and greater than 0) - recording duration of the generated signal in seconds (note: The "int" type is supported, it will be cast to the "float" type.);
        RATE ("int" and greater than 0) - sampling rate in hertz (note: 44100 hertz is the standard CD quality.);
        FREQUENCIES ("list" or "tuple" with elements of "int" or "float" (may use a combination of "int" and "float")) - collection of frequencies that will be used for generating sine waves of the form sin(2*pi*frequency*x).
    The result of the function will be a recorded generated signal (where the generated signal consists of sequences of sinusoids with the different frequencies, i.e., sin(...), sin(...), ... (the duration of playing one sinusoidis determined as SECONDS/len(FREQUENCIES))) and saved according to the provided parameters.
    '''

    print(f"Signal generation from the given frequencies has started.")

    # Checking for the correctness of the input data
    if type(FILENAME) != str or '.wav' not in FILENAME:
        FILENAME = "../data/generated_signal_sequence.wav"
        print(f'The filename for recording the generated signal is set incorrectly. The default value is set:\n\t FILENAME = "{FILENAME}"')
    else:
        FILENAME = "./" + FILENAME

    if type(SECONDS) == int and SECONDS > 0:
        SECONDS = float(SECONDS)
    elif type(SECONDS) != float or SECONDS <= 0:
        SECONDS = 5.0
        print(f'The recording duration of the generated signal is set incorrectly. The default value is set:\n\t SECONDS = {SECONDS}')
    SECONDS = round(SECONDS, 2)

    if type(RATE) != int or RATE <= 0:
        RATE = 44100
        print(f'The sampling rate is set incorrectly. The default value is set:\n\t RATE = {RATE}')

    if type(FREQUENCIES) == list or type(FREQUENCIES) == tuple:
        if len(FREQUENCIES) == 0:
            FREQUENCIES = (440, 556, 659)
            print(f'The frequencies are set incorrectly. The number of elements in frequencies should be greater than 0. The default value is set:\n\t FREQUENCIES = {FREQUENCIES}')
        elif not all(True if type(frequency) == int or type(frequency) == float else False for frequency in FREQUENCIES):
            FREQUENCIES = (440, 556, 659)
            print(f'The frequencies are set incorrectly. The elements in the collection can be either int or float, or a mix of both. The default value is set:\n\t FREQUENCIES = {FREQUENCIES}')
    else:
        print(f'The frequencies are set incorrectly. Frequencies is of type {type(FREQUENCIES)}, but it should be a list or tuple.', end=' ')
        FREQUENCIES = (440, 556, 659)
        print(f'The default value is set:\n\t FREQUENCIES = {FREQUENCIES}')

    CHUNK = 1024 # The number of frames per one "request" to the microphone -> It is used here for the correct operation of the `isPowerOfTwo_DataVolume` function.
    CHANNELS = 1 # The number of audio tracks -> It is used here for the correct operation of the `wave_write` function.

    # Checking if the volume of recorded data matches a power of two. (If it doesn't match, it can be corrected by changing the recording duration.)
    SECONDS = isPowerOfTwo.isPowerOfTwo_DataVolume(SECONDS, RATE, CHUNK)

    time = np.linspace(0, SECONDS, int(RATE / CHUNK * SECONDS)*CHUNK)
    data_signal = np.zeros(shape=time.size)

    for i in range(len(FREQUENCIES)):
        if i != len(FREQUENCIES)-1:
            for t in range(int(len(time)/len(FREQUENCIES))*i, int(len(time)/len(FREQUENCIES))*(i+1)):
                musical_note = note(FREQUENCIES[i])
                data_signal[t] = musical_note(time[t]) 
        else:
            for t in range(int(len(time)/len(FREQUENCIES))*i, len(time)):
                musical_note = note(FREQUENCIES[i])
                data_signal[t] = musical_note(time[t])

    # Normalize the signal data
    data_signal /= np.max(np.abs(data_signal))

    # Scaling audio data to 16-bit format: Multiplying by 32767 and converting to the np.int16 type.
    data_signal *= 32767 # 32767 is the maximum value that can be represented in the np.int16 format, which is used for audio signals.
    data_signal = data_signal.astype(np.int16)

    # Converting int to bytes for further writing to the ".wav" file.
    frames = data_signal.tobytes()

    # Save the generated data in a WAV file
    wave_worker.wave_write(FILENAME, frames, RATE, CHANNELS)

    print(f'Finished signal generation. The signal is saved in the "{FILENAME}" file!\n')

if __name__ == '__main__':
    path_to_save_signal = "../data/test_generated_signal_sum.wav"
    seconds = 5.95
    rate = 44100
    A = 440 # 440 - Frequency of the note A
    C = 554 # 554 - Frequency of the note C
    E = 659 # 659 - Frequency of the note E
    frequencies = (A, C, E)

    # The result will be a generated signal of the musical note A major.
    signal_generator_sum(path_to_save_signal, seconds, rate, frequencies)

    path_to_save_signal = "../data/test_generated_signal_sequence.wav"
    seconds = 23.78
    rate = 44100
    # Using the notes C, E, G, A, and B in the first octave in the musical standard with A4=440 Hz, the frequencies are as follows:
    C = 261.63 # Hz
    E = 329.63 # Hz
    G = 392.00 # Hz
    A = 440.00 # Hz
    B = 493.88 # Hz
    frequencies = (A,E,A,E,A,G,0,G,0,G,E,G,E,G,A,0,A,0,A,E,A,E,A,G,0,G,0,G,E,G,E,G,A,0,0,A,B,0,B,0,B,0,B,0,B,C,0,C,0,C,0,C,0,C,0,C,B,A,G,A,0,A,0,A,B,0,B,0,B,0,B,0,B,C,0,C,0,C,0,C,0,C,0,C,B,A,G,A)

    signal_generator_sequence(path_to_save_signal, seconds, rate, frequencies)
