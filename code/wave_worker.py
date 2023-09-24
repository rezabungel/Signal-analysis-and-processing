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

def wave_concatenate(FILENAMES = None, FILENAME_Output = "../data/concatenated_signal.wav"):

    '''
    This function is used to concatenate wave files into a single file.
        note: The sample rates, channel counts, and sample formats of the concatenated files must be identical.
    The following parameters are passed to the function:
        FILENAMES ("list" or "tuple" with elements of "str") - elements are the paths where the files are stored with their names and the ".wav" extension (example of one of the elements: "../the_path_where_the_file_is_stored/file_name.wav");
        FILENAME_Output ("str") - path to save the file and its name with ".wav" extension. (example: "../the_path_to_save_the_file/name_of_the_saved_file.wav").
    The result of the function will be the concatenation of wave files into one, and the concatenated file will be saved.
        Note: The concatenation order matches the order of elements in FILENAMES.
    '''

    # Checking for the correctness of the input data
    if type(FILENAMES) == list or type(FILENAMES) == tuple:   
        if len(FILENAMES) == 0:
            raise ValueError(f'The FILENAMES are set incorrectly. The number of elements in FILENAMES should be greater than 0.')
        
        if not all(type(file_name) == str for file_name in FILENAMES):
            raise TypeError(f'The FILENAMES are set incorrectly. The elements in the collection must be of type "str".')
        
        if not all('.wav' in file_name for file_name in FILENAMES):
            raise ValueError(f'The FILENAMES are set incorrectly. The elements of the collection must contain the path to the file, the filename, and its ".wav" extension.')

        FILENAMES = ["./" + file_name for file_name in FILENAMES ]
    else:
        raise TypeError(f'The FILENAMES are set incorrectly. FILENAMES is of type {type(FILENAMES)}, but it should be a list or tuple.')

    if type(FILENAME_Output) != str or '.wav' not in FILENAME_Output:
        FILENAME_Output = "../data/concatenated_signal.wav"
        print(f'The filename for the concatenated signal is set incorrectly. The default value is set:\n\t FILENAME_Output = "{FILENAME_Output}"')
    else:
        FILENAME_Output = "./" + FILENAME_Output

    frames = np.array([], dtype=np.int16)
    rate = []
    channels = []
    sample_format = []

    for file_name in FILENAMES:
        data_signal, N_FRAMES, RATE, CHANNELS, SAMPLE_FORMAT = wave_read(file_name)
        
        frames = np.concatenate([frames, data_signal])
        rate.append(RATE)
        channels.append(CHANNELS)
        sample_format.append(SAMPLE_FORMAT)

    if len(set(rate)) == 1 and len(set(channels)) == 1 and len(set(sample_format)) == 1:
        wave_write(FILENAME_Output, frames, rate[0], channels[0])
    else:
        raise ValueError(f'Invalid audio parameters: different sample rates, channel counts, or sample formats in the concatenated signals.')

if __name__ == "__main__":
    filename = "../data/test.wav"
    data_signal = np.array([5, 31, 14, -4, -8, -14, 15, 54, 57, 45, 16, -17, -49, -82, -71, -53, -27, -8, -37, -91, -122, -130, -126, -114, -102])
    rate = 44100
    channels = 1
    wave_write("../data/test.wav", data_signal, rate, channels)

    print(f"\nThe data read from the file:")
    print(wave_read(filename))

    filename_out = "../data/test_out.wav"
    wave_concatenate([filename, filename], filename_out)

    print(f"\nThe data read from the file after their concatenation:")
    print(wave_read(filename_out))
