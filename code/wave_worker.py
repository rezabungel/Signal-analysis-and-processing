'''
This module is used for working with wave files.
'''

import wave

import pyaudio
import numpy as np

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def convert_to_int16(frames):

    '''
    The "convert_to_int16" function converts "numpy.ndarray" with a type other than dtype="numpy.int16" to "numpy.ndarray" with dtype="numpy.int16".
    The following parameters are passed to the function:
        frames ("numpy.ndarray" with dtype unequal "numpy.int16") - value of the signal data with dtype unequal "numpy.int16".
    The result of the function:
        Return values:
            frames ("numpy.ndarray" with dtype="numpy.int16") - value of the signal data with dtype="numpy.int16".
    '''

    print(f'The "convert_to_int16" function has been launched.')
    if frames.max() <= 32767 and frames.min() >= -32768:
        # The frames values fall within the range of "numpy.int16" values. (Conversion without problems)
        save_old_type = frames.dtype
        frames = frames.astype(np.int16)
        print(f'The type of the passed variable was changed from "numpy.{save_old_type}" to "numpy.{frames.dtype}" without any problems.')
        return frames
    else:
        # The frames values do not fall within the range of "numpy.int16" values. (Conversion with data change)
        print(f'The values of the passed variable that are not in the range of "numpy.int16" will be changed:')
        print(f'\tAll values greater than 32767 will be replaced with 32767;')
        print(f'\tAll values less than -32768 will be replaced with -32768.')
        save_old_type = frames.dtype
        frames[frames > 32767] = 32767 # All values greater than 32767 will be replaced with 32767
        frames[frames < -32768] = -32768 # All values less than -32768 will be replaced with -32768
        frames = frames.astype(np.int16)
        print(f'The type of the passed variable was changed from "numpy.{save_old_type}" to "numpy.{frames.dtype}" with data change.')
        return frames

def wave_write(FILENAME, FRAMES, RATE, CHANNELS):

    '''
    This function is used to write data to a wave file.
        Note: If the file does not exist, it will be created; if the file exists, its content will be overwritten.
    The following parameters are passed to the function:
        FILENAME ("str") - path to save the file and its name with ".wav" extension. (example: "../the_path_to_save_the_file/name_of_the_saved_file.wav");
        FRAMES ("bytes" или "numpy.ndarray" with dtype="numpy.int16") - value of the signal data:
            If the data type is "bytes":
                Two bytes per number.
            If the data type is "numpy.ndarray":
                If a FRAMES with a dtype that is not "numpy.int16", then the signal data will be converted to this type using the "convert_to_int16" function.
        RATE ("int" and greater than 0) - sampling rate in hertz. (note: 44100 is enough for a voice); 
        CHANNELS ("int" and greater than 0) - number of audio tracks. (note: use 1 (mono sound)).
    The result of the function will be a saved wave file according to the provided parameters.
    '''

    SAMPLE_FORMAT = pyaudio.paInt16 # Sound depth = 16 bits = 2 bytes

    if type(FRAMES) == np.ndarray:
        # Checking "FRAMES" for compliance with the type "numpy.int16".
        if (FRAMES.dtype != np.int16):
            FRAMES = convert_to_int16(FRAMES)
        
        # Converting int to bytes for further writing to the ".wav" file.
        FRAMES = FRAMES.tobytes()

    elif type(FRAMES) != bytes:
        raise TypeError('Writing data to the wave file is not possible due to an incorrect data type for "FRAMES". Expected data types are "bytes" or "numpy.ndarray".')

    # Creating ".wav" file and writing signal data to it in bytes.
    with wave.open(FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(FRAMES)

def wave_read(FILENAME):

    '''
    This function is used to read data from a wave file.
    The following parameters are passed to the function:
        FILENAME ("str") - the path where the file is stored and its name with the extension ".wav". (example: "../the_path_where_the_file_is_stored/file_name.wav").
    The result of the function:
        Return values:
            data_signal ("numpy.ndarray" with dtype="np.int<depends on the sound depth>") - value of the signal data;
            N_FRAMES ("int") - number of frames;
            RATE ("int") - sampling rate in hertz;
            CHANNELS ("int") - number of audio tracks;
            SAMPLE_FORMAT ("int") - sound depth.
    '''

    with wave.open(FILENAME, 'rb') as wf:
        SAMPLE_FORMAT = wf.getsampwidth()
        CHANNELS = wf.getnchannels()
        RATE = wf.getframerate()
        N_FRAMES = wf.getnframes()
        data_signal = np.frombuffer(wf.readframes(N_FRAMES), dtype=types[SAMPLE_FORMAT]) # Reading the signal from the file and converting bytes to int

    return data_signal, N_FRAMES, RATE, CHANNELS, SAMPLE_FORMAT

if __name__ == "__main__":
    filename = "../data/test.wav"
    data_signal = np.array([5, 31, 14, -4, -8, -14, 15, 54, 57, 45, 16, -17, -49, -82, -71, -53, -27, -8, -37, -91, -122, -130, -126, -114, -102])
    rate = 44100
    channels = 1
    wave_write("../data/test.wav", data_signal, rate, channels)

    print(f"\nThe data read from the file:")
    print(wave_read(filename))
