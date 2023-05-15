'''
This module is used to create a signal based on the values of the signal data.
The created signal will be saved to a file with the extension ".wav".
Signal data is the value of the signal in time. The value of the signal data can be obtained from the result of the inverse discrete Fourier transform.
The signal data should be a "numpy.ndarray" with dtype="numpy.int16". If the type is not "numpy.int16", it will be converted to the required type using the "convert_to_int16" function.
'''

import numpy as np

import pyaudio
import wave

SAMPLE_FORMAT = pyaudio.paInt16  # Sound depth = 16 bits = 2 bytes


def convert_to_int16(data_signal):
    '''
    The "convert_to_int16" function converts "numpy.ndarray" with a type other than dtype="numpy.int16" to "numpy.ndarray" with dtype="numpy.int16".
    The following parameters are passed to the function:
        data_signal ("numpy.ndarray" with dtype unequal "numpy.int16") - value of the signal data with dtype unequal "numpy.int16".
    The result of the function:
        Return values:
            data_signal ("numpy.ndarray" with dtype="numpy.int16") - value of the signal data with dtype="numpy.int16".
    '''

    print(f'The "convert_to_int16" function has been launched.')
    if data_signal.max() <= 32767 and data_signal.min() >= -32768:
        # The data_signal values fall within the range of "numpy.int16" values. (Conversion without problems)
        save_old_type = data_signal.dtype
        data_signal = data_signal.astype(np.int16)
        print(f'The type of "data_signal" was changed from "numpy.{save_old_type}" to "numpy.{data_signal.dtype}" without any problems.')
        return data_signal
    else:
        # The data_signal values do not fall within the range of "numpy.int16" values. (Conversion with data change)
        print(f'The values of "data_signal" that are not in the range of "numpy.int16" will be changed:')
        print(f'\tAll values greater than 32767 will be replaced with 32767;')
        print(f'\tAll values less than -32768 will be replaced with -32768.')
        save_old_type = data_signal.dtype
        data_signal[data_signal > 32767] = 32767 # All values greater than 32767 will be replaced with 32767
        data_signal[data_signal < -32768] = -32768 # All values less than -32768 will be replaced with -32768
        data_signal = data_signal.astype(np.int16)
        print(f'The type of "data_signal" was changed from "numpy.{save_old_type}" to "numpy.{data_signal.dtype}" with data change.')
        return data_signal

def creating_a_signal(data_signal,
                      FILENAME="../data/output_signal.wav",
                      RATE=44100,
                      CHANNELS=1):

    '''
    This function allows you to create a signal based on the values of the signal data and save this signal to a file with the extension ".wav".
    The following parameters are passed to the function:
        data_signal ("numpy.ndarray" with dtype="numpy.int16") - the value of the signal data received, for example, after inverse discrete Fourier transform:
            If a data_signal with a dtype that is not "numpy.int16", then the signal data will be converted to this type using the "convert_to_int16" function;
        FILENAME ("str") - path to save the signal and its name with ".wav" extension. (example: "../the_path_to_save_the_signal/name_of_the_saved_signal.wav");
        RATE ("int" and greater than 0) - sampling rate in hertz. (note: 44100 is enough for a voice);
        CHANNELS ("int" and greater than 0) - number of audio tracks. (note: use 1 (mono sound)).
    The result of the function will be a created signal, saved in accordance with the passed parameters.
    '''

    print(f"Signal creation has started.")    

    # Checking for the correctness of the input data
    if type(FILENAME) != str or '.wav' not in FILENAME:
        FILENAME = "../data/output_signal.wav"
        print(f'The filename for creating is set incorrectly. The default value is set:\n\t FILENAME = "{FILENAME}"')

    if type(RATE) != int or RATE <= 0:
        RATE = 44100
        print(f'The sampling rate is set incorrectly. The default value is set:\n\t RATE = {RATE}')

    if type(CHANNELS) != int or CHANNELS <= 0:
        CHANNELS = 1
        print(f'The number of channels is set incorrectly. The default value is set:\n\t CHANNELS = {CHANNELS}')

    # Checking "data_signal" for compliance with the type "numpy.int16".
    if (data_signal.dtype != np.int16):
        data_signal = convert_to_int16(data_signal)

    # Converting int to bytes for further writing to the ".wav" file.
    frames = data_signal.tobytes()

    # Creating ".wav" file and writing the signal data, which has been converted to bytes, into it.
    with wave.open(FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(frames)
        print(f'Finished signal creation. The signal is saved in the "{FILENAME}" file!\n')


if __name__ == "__main__":
    data_signal = np.array([5, 31, 14, -4, -8, -14, 15, 54, 57, 45, 16, -17, -49, -82, -71, -53, -27, -8, -37, -91, -122, -130, -126, -114, -102])
    creating_a_signal(data_signal)
