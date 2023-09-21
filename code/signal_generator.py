'''
This module is used to ...
'''

import pyaudio
import wave
import math

import numpy as np

import isPowerOfTwo

SAMPLE_FORMAT = pyaudio.paInt16 # Sound depth = 16 bits = 2 bytes

def signal_generator(FILENAME = "../data/generated_signal.wav", SECONDS = 5.0, RATE = 44100, FREQUENCIES = None):
    
    '''
    This function allows you to ...
    '''

    # A function is created to return a lambda function of a signal (for example, when 440Hz is passed, it returns a function the musical note A).
    def note(hertz): # y = sin(2*math.pi*hertz*x)
        return lambda x: math.sin(2*math.pi*hertz*x) 

    print(f"Signal generation from the given frequencies has started.")

    # Checking for the correctness of the input data
    if type(FILENAME) != str or '.wav' not in FILENAME:
        FILENAME = "../data/generated_signal.wav"
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
        elif not all(True if type(hertz) == int or type(hertz) == float else False for hertz in FREQUENCIES):
            FREQUENCIES = (440, 556, 659)
            print(f'The frequencies are set incorrectly. The elements in the collection can be either int or float, or a mix of both. The default value is set:\n\t FREQUENCIES = {FREQUENCIES}')
    else:
        print(f'The frequencies are set incorrectly. Frequencies is of type {type(FREQUENCIES)}, but it should be a list or tuple.', end=' ')
        FREQUENCIES = (440, 556, 659)
        print(f'The default value is set:\n\t FREQUENCIES = {FREQUENCIES}')

    CHUNK = 1024 # The number of frames per one "request" to the microphone -> It is used here for the correct operation of the `isPowerOfTwo_DataVolume` function.

    # Checking if the volume of recorded data matches a power of two. (If it doesn't match, it can be corrected by changing the recording duration.)
    SECONDS = isPowerOfTwo.isPowerOfTwo_DataVolume(SECONDS, RATE, CHUNK)
    
    time = np.linspace(0, SECONDS, int(RATE / CHUNK * SECONDS)*CHUNK)
    data_signal = np.zeros(shape=time.size)

    for hertz in FREQUENCIES:
        musical_note = note(hertz)
        data_signal += np.array([musical_note(t) for t in time])

    # Normalize the signal data
    data_signal /= np.max(np.abs(data_signal))

    # Scaling audio data to 16-bit format: Multiplying by 32767 and converting to the np.int16 type.
    data_signal *= 32767 # 32767 is the maximum value that can be represented in the np.int16 format, which is used for audio signals.
    data_signal = data_signal.astype(np.int16)

    # Converting int to bytes for further writing to the ".wav" file.
    frames = data_signal.tobytes()

    # Creating ".wav" file and writing the signal data, which has been converted to bytes, into it.
    with wave.open(FILENAME, 'wb') as wf:
        wf.setnchannels(1) # Set the number of channels (1 = mono sound)
        wf.setsampwidth(pyaudio.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(frames)

    print(f'Finished signal generation. The signal is saved in the "{FILENAME}" file!\n')

if __name__ == '__main__':
    path_to_save_signal = "../data/test_generated_signal.wav"
    seconds = 5.95
    rate = 44100
    A = 440 # 440 - Frequency of the note A
    C = 554 # 554 - Frequency of the note C
    E = 659 # 659 - Frequency of the note E
    frequencies = (A, C, E)

    # The result will be a generated signal of the musical note A major.
    signal_generator(path_to_save_signal, seconds, rate, frequencies)
