'''
This module is used to record the signal.
The signal is recorded from your microphone and saved to a file with the extension ".wav".
'''

import pyaudio

import wave_worker
import isPowerOfTwo

SAMPLE_FORMAT = pyaudio.paInt16  # Sound depth = 16 bits = 2 bytes

def signal_recording(FILENAME = "../data/input_signal.wav", # FILENAME must contain the path and file name of the record. FILENAME must end in ".wav"
                     SECONDS = 5.0, # Recording duration
                     RATE = 44100, # Sampling rate - number of frames per second
                     CHUNK = 1024, # The number of frames per one "request" to the microphone (read in pieces)
                     CHANNELS = 1, # Mono
                    ):

    '''
    This function allows you to record a signal using a microphone.
    The following parameters are passed to the function:
        FILENAME ("str") - path to save the file and its name with ".wav" extension. (example: "../the_path_to_save_the_file/name_of_the_saved_file.wav");
        SECONDS ("float" and greater than 0) - recording duration in seconds (note: The "int" type is supported, it will be cast to the "float" type.);
        RATE ("int" and greater than 0) - sampling rate in hertz. (note: 44100 is enough for a voice);
        CHUNK ("int", greater than 0 and a power of two) - number of frames per one "request" to the microphone. (note: 1024 is enough for a voice);
        CHANNELS ("int" and greater than 0) - number of audio tracks. (note: use 1 (mono sound)).
    The result of the function will be a recorded signal, saved in accordance with the passed parameters.
    '''

    # Checking for the correctness of the input data
    if type(FILENAME) != str or '.wav' not in FILENAME:
        FILENAME = "../data/input_signal.wav"
        print(f'The filename for recording is set incorrectly. The default value is set:\n\t FILENAME = "{FILENAME}"')
    else:
        FILENAME = "./" + FILENAME

    if type(SECONDS) == int and SECONDS > 0:
        SECONDS = float(SECONDS)
    elif type(SECONDS) != float or SECONDS <= 0:
        SECONDS = 5.0
        print(f'The recording duration is set incorrectly. The default value is set:\n\t SECONDS = {SECONDS}')
    SECONDS = round(SECONDS, 2)

    if type(RATE) != int or RATE <= 0:
        RATE = 44100
        print(f'The sampling rate is set incorrectly. The default value is set:\n\t RATE = {RATE}')

    if type(CHUNK) != int or CHUNK <= 0 or not isPowerOfTwo.isPowerOfTwo(CHUNK):
        CHUNK = 1024
        print(f'The number of frames per one "request" to the microphone is set incorrectly. The default value is set:\n\t CHUNK = {CHUNK}')

    if type(CHANNELS) != int or CHANNELS <= 0:
        CHANNELS = 1
        print(f'The number of channels is set incorrectly. The default value is set:\n\t CHANNELS = {CHANNELS}')

    # Checking if the volume of recorded data matches a power of two. (If it doesn't match, it can be corrected by changing the recording duration.)
    SECONDS = isPowerOfTwo.isPowerOfTwo_DataVolume(SECONDS, RATE, CHUNK)

    audio = pyaudio.PyAudio() # Initialize PyAudio object

    while True: # The loop runs until the correct data is entered
        try:
            # Selecting a recording device
            print(f"List of available devices:")
            for i in range(audio.get_device_count()):
                print(f"\t{i} {audio.get_device_info_by_index(i)['name']}")

            while True:
                input_device = int(input('Select the index of the recording device: '))
                if (input_device >= 0) and (input_device <= i):
                    break
                else:
                    print(f"Invalid input. Non-existent index.")
                    print(f"List of available devices:")
                    for i in range(audio.get_device_count()):
                        print(f"\t{i} {audio.get_device_info_by_index(i)['name']}")

            # Open the stream to read data from the recording device and set the parameters
            stream = audio.open(format=SAMPLE_FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                frames_per_buffer=CHUNK,
                                input_device_index=input_device,
                                input=True)
            break

        except ValueError:
            print(f"Invalid input. You didn't enter a number.")
        except OSError:
            print(f"Invalid recording device.")
    
    frames = [] # Declaring an array for storing frames

    print(f"Recording...")

    for i in range(0, int(RATE / CHUNK * SECONDS)): # RATE / CHUNK - number of requests per second
        data = stream.read(CHUNK) # reading a string of bytes long CHUNK * SAMPLE_FORMAT
        frames.append(data)

    frames = b''.join(frames)
    print(f"Finished recording!\n")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    audio.terminate() # Audio System Close

    # Save the recorded data in a WAV file
    wave_worker.wave_write(FILENAME, frames, RATE, CHANNELS)

if __name__ == "__main__":
    signal_recording()
